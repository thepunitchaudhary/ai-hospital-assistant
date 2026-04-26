import os
import re
import uuid
import json
import asyncio
from datetime import datetime
from fastapi import APIRouter

from groq import Groq

from database import get_conn
from models import MessageReq
from utils import speak, resolve_date, send_confirmation_email

router = APIRouter(prefix="/agent")

MODEL  = "llama-3.1-8b-instant"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SESSIONS    = {}
SESSION_TTL = 1800


def purge_old_sessions():
    now     = datetime.utcnow().timestamp()
    expired = [k for k, v in SESSIONS.items() if now - v.get("ts", now) > SESSION_TTL]
    for k in expired:
        del SESSIONS[k]


def _new_session_data():
    return {
        "name": None, "email": None, "user_id": None,
        "doctor": None, "date": None, "time": None,
        "active": False, "done": False,
        "ts": datetime.utcnow().timestamp()
    }


def extract_with_llm(text: str):
    try:
        prompt = (
            'Extract booking details from this message and return ONLY valid JSON.\n'
            'Fields: doctor (one of "Dr. Meera Patel (Cardiology)", "Dr. Arjun Rao (Neurology)", '
            '"Dr. Priya Nair (Orthopedics)", or null), date (as written or null), time (as written or null).\n'
            f'Message: "{text}"\n'
            'Return only JSON like: {"doctor": null, "date": "tomorrow", "time": "10 AM"}'
        )
        res = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )
        raw  = res.choices[0].message.content.strip()
        raw  = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(raw)
        return data.get("doctor"), data.get("date"), data.get("time")
    except Exception:
        return extract_fallback(text)


def extract_fallback(text: str):
    lower = text.lower()
    doctor = None
    if "cardio" in lower:
        doctor = "Dr. Meera Patel (Cardiology)"
    elif "neuro" in lower:
        doctor = "Dr. Arjun Rao (Neurology)"
    elif "ortho" in lower:
        doctor = "Dr. Priya Nair (Orthopedics)"

    time_match = re.search(r'\b(\d{1,2}(:\d{2})?\s?(am|pm))\b', lower, re.IGNORECASE)
    time_val   = time_match.group().strip().upper() if time_match else None

    date_val = None
    for kw in ["tomorrow", "today", "monday", "tuesday", "wednesday",
                "thursday", "friday", "saturday", "sunday", "next"]:
        if kw in lower:
            date_val = kw
            break

    if not date_val:
        m = re.search(
            r'\b(\d{1,2}(st|nd|rd|th)?[\s\-/](jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*'
            r'|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*[\s\-/]\d{1,2}'
            r'|\d{1,2}[\/\-]\d{1,2}([\/\-]\d{2,4})?)\b',
            lower
        )
        if m:
            date_val = m.group().strip()

    return doctor, date_val, time_val


def book_appointment(user_id, name, email, doctor, date, time) -> bool:
    conn = get_conn()
    cur  = conn.cursor()

    clash = cur.execute(
        "SELECT id FROM appointments WHERE doctor_name=? AND appointment_date=? AND appointment_time=? AND status='CONFIRMED'",
        (doctor, date, time)
    ).fetchone()

    if clash:
        conn.close()
        return False

    cur.execute(
        "INSERT INTO appointments (user_id, patient_name, doctor_name, appointment_date, appointment_time, patient_email, status) "
        "VALUES (?,?,?,?,?,?,?)",
        (user_id, name, doctor, date, time, email, "CONFIRMED")
    )
    conn.commit()
    conn.close()
    send_confirmation_email(email, name, doctor, date, time)
    return True


@router.post("/new_session")
def new_session():
    purge_old_sessions()
    sid = str(uuid.uuid4())
    SESSIONS[sid] = _new_session_data()
    return {"session_id": sid}


@router.post("/message")
async def message(req: MessageReq):
    purge_old_sessions()

    s = SESSIONS.setdefault(req.session_id, _new_session_data())
    s["ts"] = datetime.utcnow().timestamp()

    if req.name:    s["name"]    = req.name
    if req.email:   s["email"]   = req.email
    if req.user_id: s["user_id"] = req.user_id

    user_text = req.text.lower().strip()

    greeting_triggers = {"hello", "hi", "hey", "start", ""}
    if user_text in greeting_triggers:
        text  = (
            f"Hello {s['name'] or 'there'}! I'm Sarah, the AI receptionist at City Hospital. "
            "How can I help you today? You can ask me to book an appointment with our "
            "Cardiology, Neurology, or Orthopedics departments."
        )
        audio = await speak(text)
        return {"text": text, "audio": audio}

    if any(x in user_text for x in ["book", "appointment", "schedule", "doctor", "visit", "consult", "see a"]):
        s["active"] = True

    doctor, date_val, time_val = await asyncio.to_thread(extract_with_llm, req.text)

    if doctor:   s["doctor"] = doctor
    if date_val: s["date"]   = await asyncio.to_thread(resolve_date, date_val)
    if time_val: s["time"]   = time_val

    if s["active"] and not s["done"]:
        if not s["doctor"]:
            text = "Sure! Which department would you like? We have Cardiology, Neurology, and Orthopedics."
        elif not s["date"]:
            text = f"Great, I'll book you with {s['doctor']}. What date works for you? You can say tomorrow, Monday, or a specific date."
        elif not s["time"]:
            text = f"And what time works for you on {s['date']}? For example, 10 AM or 3 PM."
        else:
            success = await asyncio.to_thread(
                book_appointment, s["user_id"], s["name"], s["email"],
                s["doctor"], s["date"], s["time"]
            )
            s["done"] = True
            if success:
                text = (
                    f"All done, {s['name'] or 'there'}! "
                    f"Your appointment with {s['doctor']} is confirmed on {s['date']} at {s['time']}. "
                    "A confirmation email has been sent. Is there anything else I can help you with?"
                )
            else:
                s["time"] = None
                s["done"] = False
                text = (
                    f"Sorry, {s['doctor']} already has a booking at that time on {s['date']}. "
                    "Could you pick a different time?"
                )
        audio = await speak(text)
        return {"text": text, "audio": audio}

    if s["done"]:
        if any(x in user_text for x in ["another", "new", "more", "else", "again"]):
            s.update({"doctor": None, "date": None, "time": None, "active": False, "done": False})
            text = "Of course! Would you like to book another appointment? Just tell me the department and preferred date."
        else:
            text = "Your appointment is confirmed. Take care and feel better soon! Goodbye."
        audio = await speak(text)
        return {"text": text, "audio": audio}

    try:
        res  = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Sarah, a friendly AI receptionist at City Hospital. "
                        "Keep answers short, warm, and helpful. "
                        "If asked about anything unrelated to hospitals or health, politely redirect."
                    )
                },
                {"role": "user", "content": req.text}
            ]
        )
        text = res.choices[0].message.content
    except Exception as e:
        print("GROQ ERROR:", e)
        text = "I'm sorry, I didn't quite catch that. Could you please repeat?"

    audio = await speak(text)
    return {"text": text, "audio": audio}