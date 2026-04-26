import secrets
from fastapi import APIRouter, HTTPException, Depends

from database import get_conn
from models import RegisterReq, LoginReq
from utils import hash_password, verify_password, generate_token, get_token_user, send_welcome_email

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(req: RegisterReq):
    conn = get_conn()
    cur  = conn.cursor()

    if cur.execute("SELECT id FROM users WHERE email=?", (req.email,)).fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    token = generate_token()
    cur.execute(
        "INSERT INTO users (full_name, email, phone, password_hash, auth_token) VALUES (?,?,?,?,?)",
        (req.full_name, req.email, req.phone, hash_password(req.password), token)
    )
    user_id = cur.lastrowid
    conn.commit()
    conn.close()

    send_welcome_email(req.email, req.full_name)

    return {
        "success": True,
        "token": token,
        "user": {"id": user_id, "full_name": req.full_name, "email": req.email}
    }


@router.post("/login")
def login(req: LoginReq):
    conn = get_conn()
    cur  = conn.cursor()

    user = cur.execute(
        "SELECT id, full_name, email, phone, password_hash FROM users WHERE email=?",
        (req.email.lower().strip(),)
    ).fetchone()

    if not user or not verify_password(req.password, user[4]):
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = generate_token()
    cur.execute("UPDATE users SET auth_token=? WHERE id=?", (token, user[0]))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "token": token,
        "user": {"id": user[0], "full_name": user[1], "email": user[2], "phone": user[3]}
    }


@router.get("/appointments/{user_id}")
def get_appointments(user_id: int, token_user_id: int = Depends(get_token_user)):
    if token_user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = get_conn()
    cur  = conn.cursor()
    rows = cur.execute(
        "SELECT id, doctor_name, appointment_date, appointment_time, status, created_at "
        "FROM appointments WHERE user_id=? ORDER BY id DESC",
        (user_id,)
    ).fetchall()
    conn.close()

    return {"appointments": [
        {"id": r[0], "doctor": r[1], "date": r[2], "time": r[3], "status": r[4], "created_at": r[5]}
        for r in rows
    ]}


@router.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int, token_user_id: int = Depends(get_token_user)):
    conn = get_conn()
    cur  = conn.cursor()

    row = cur.execute("SELECT user_id FROM appointments WHERE id=?", (appointment_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Appointment not found")

    if row[0] != token_user_id:
        conn.close()
        raise HTTPException(status_code=403, detail="Access denied")

    cur.execute("UPDATE appointments SET status='CANCELLED' WHERE id=?", (appointment_id,))
    conn.commit()
    conn.close()

    return {"success": True}