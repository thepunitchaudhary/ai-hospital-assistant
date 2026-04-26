City Hospital – Sarah AI Receptionist (v2 with Login)
======================================================

WHAT'S NEW IN v2
----------------
✅ Patient Login / Register system
✅ Password hashing (secure)
✅ Patient Dashboard with appointment history
✅ Appointments linked to user accounts
✅ Welcome email on registration
✅ Auth tokens stored in browser (stays logged in)
✅ Refresh appointments after every voice call

SETUP (100% FREE)
-----------------
1. Install dependencies:
   pip install -r requirements.txt

2. Create a .env file in the SAME folder as app.py:

   GROQ_API_KEY=your_groq_key_here
   SMTP_EMAIL=your_gmail@gmail.com
   SMTP_PASSWORD=your_gmail_app_password_here

   WHERE TO GET THESE:
   ───────────────────
   GROQ_API_KEY  → https://console.groq.com  (free, sign up)
   SMTP_EMAIL    → your Gmail address
   SMTP_PASSWORD → Gmail App Password (NOT your real password)
                   Get it: Google Account → Security
                   → 2-Step Verification → App Passwords
                   → Select app: Mail, device: Windows
                   → Copy the 16-character password

3. Run the server:
   python app.py

4. Open your browser:
   http://127.0.0.1:8000

HOW IT WORKS NOW
----------------
1. User goes to the website
2. Registers with name, email, phone, password
3. Receives a welcome email ✅
4. Logs in → sees their personal dashboard
5. Clicks "Start Voice Call with Sarah"
6. Books appointment by speaking naturally
7. Appointment saved & confirmation email sent ✅
8. Dashboard refreshes showing new appointment

DEPARTMENTS
-----------
- Cardiology  → Dr. Meera Patel
- Neurology   → Dr. Arjun Rao
- Orthopedics → Dr. Priya Nair

DEPLOYMENT (FREE)
-----------------
1. Push to GitHub (don't include .env file!)
2. Go to render.com → New → Web Service
3. Connect your GitHub repo
4. Start command: uvicorn app:app --host 0.0.0.0 --port 10000
5. Add env vars in Render dashboard (Environment tab)
6. Your app is live at: https://your-app.onrender.com

IMPORTANT
---------
⚠️  Change API_URL in frontend.html line:
    const API = "http://127.0.0.1:8000";
    to your Render URL when deploying:
    const API = "https://your-app.onrender.com";