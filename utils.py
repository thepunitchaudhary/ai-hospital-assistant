import os
import asyncio
import io
import base64
import smtplib
import threading
from datetime import datetime, timedelta
from email.mime.text import MIMEText

import bcrypt
import secrets
from gtts import gTTS
from dateutil import parser as dateparser
from fastapi import Header, HTTPException

from database import get_conn


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def generate_token() -> str:
    return secrets.token_hex(32)


def get_token_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ", 1)[1]
    conn  = get_conn()
    cur   = conn.cursor()
    row   = cur.execute("SELECT id FROM users WHERE auth_token=?", (token,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid token")
    return row[0]


def resolve_date(text: str) -> str:
    today = datetime.today()
    lower = text.lower().strip()

    day_map = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
    }

    if lower == "today":
        return today.strftime("%Y-%m-%d")
    if lower == "tomorrow":
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")

    for day_name, weekday in day_map.items():
        if day_name in lower:
            days_ahead = weekday - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            if "next" in lower:
                days_ahead += 7
            return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    try:
        parsed = dateparser.parse(text, dayfirst=True)
        if parsed:
            return parsed.strftime("%Y-%m-%d")
    except Exception:
        pass

    return text


async def speak(text: str):
    try:
        def run():
            fp = io.BytesIO()
            gTTS(text=text, lang="en", tld="co.in").write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        data = await asyncio.to_thread(run)
        return base64.b64encode(data).decode()
    except Exception as e:
        print("TTS ERROR:", e)
        return None


def _send(to_email: str, subject: str, body: str):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASSWORD"))
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"]    = os.getenv("SMTP_EMAIL")
        msg["To"]      = to_email
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("EMAIL ERROR:", e)


def send_confirmation_email(to_email: str, name: str, doctor: str, date: str, time: str):
    if not to_email:
        return
    body = f"""Hello {name},

Your appointment is confirmed ✅

Doctor : {doctor}
Date   : {date}
Time   : {time}

City Hospital
"""
    threading.Thread(
        target=_send,
        args=(to_email, "Appointment Confirmation – City Hospital", body),
        daemon=True
    ).start()


def send_welcome_email(to_email: str, name: str):
    if not to_email:
        return
    body = f"""Hello {name},

Welcome to City Hospital! 🏥

Your account has been created successfully.
You can now book appointments with our doctors:
- Dr. Meera Patel (Cardiology)
- Dr. Arjun Rao (Neurology)
- Dr. Priya Nair (Orthopedics)

City Hospital Team
"""
    threading.Thread(
        target=_send,
        args=(to_email, "Welcome to City Hospital – Account Created", body),
        daemon=True
    ).start()