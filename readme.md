# 🏥 City Hospital — Sarah AI Receptionist

> An AI-powered, voice-based hospital appointment system. Talk naturally to **Sarah**, your virtual receptionist, and she'll book your appointment, check slot availability, and send you an email confirmation — all hands-free.

---

## 🎬 Demo

> *Patient speaks → Sarah listens → Appointment booked → Email sent*

![Sarah AI Receptionist](./1777219119573_image.png)

---

## ✨ Features

- 🎙️ **Voice-First Interface** — Speak naturally using your browser's microphone; no typing needed
- 🤖 **AI-Powered Conversations** — Groq LLaMA 3.3 70B handles intent understanding and multi-turn dialogue
- 📅 **Real-Time Slot Checking** — Instantly checks and books available appointment slots
- 📧 **Email Confirmation** — Sends an automated confirmation email upon successful booking
- 🗣️ **Text-to-Speech Replies** — Sarah responds with a lifelike voice using Google TTS
- 🌐 **Multilingual Support** — English (India), Hindi, and Telugu
- 💾 **SQLite Database** — Lightweight, zero-config persistent storage
- 🔄 **Animated Visual Feedback** — Beautiful glowing ring shows listening / thinking / speaking states

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI + Uvicorn |
| **AI / LLM** | Groq API (LLaMA 3.3 70B) |
| **Speech-to-Text** | Web Speech API (browser-native) |
| **Text-to-Speech** | gTTS (Google Text-to-Speech) |
| **Database** | SQLite3 |
| **Email** | Python smtplib (SMTP) |
| **Frontend** | HTML + Tailwind CSS + Vanilla JS |

---

## 📁 Project Structure

```
ai-hospital-assistant/
├── app.py                  # FastAPI backend — agent logic, tools, TTS, email
├── frontend.html           # Single-page voice UI
├── appointments_poc.db     # SQLite database (auto-created)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/thepunitchaudhary/ai-hospital-assistant.git
cd ai-hospital-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here

SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

> 💡 **Gmail users:** Use an [App Password](https://myaccount.google.com/apppasswords) instead of your regular password.

### 4. Run the Server

```bash
python app.py
```

Then open your browser at **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🗣️ How It Works

```
Patient visits the web app
        │
        ▼
Enters name + email → Clicks "Start Voice Call"
        │
        ▼
Browser captures voice (Web Speech API)
        │
        ▼
Text sent to FastAPI backend → Groq LLM processes intent
        │
        ├─ list_doctors_tool()    → Returns available doctors
        ├─ check_slot_tool()      → Checks if slot is free
        └─ book_appointment_tool() → Books + sends confirmation email
        │
        ▼
gTTS converts reply to audio → Sarah speaks back to patient
```

---

## 👩‍⚕️ Available Doctors (Seed Data)

| Doctor | Specialty |
|---|---|
| Dr. Meera Patel | Cardiology |
| Dr. Arjun Rao | Neurology |

> Doctors can be added directly to the SQLite database.

---

## 🔮 Future Improvements

- [ ] User authentication (register / login)
- [ ] Admin dashboard to manage doctors and appointments
- [ ] Support for more languages and regional accents
- [ ] Calendar integration (Google Calendar / Outlook)
- [ ] SMS notifications via Twilio
- [ ] Docker containerization for easy deployment
- [ ] Deployment to Railway / Render / AWS

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Punit Chaudhary**  
🔗 [github.com/thepunitchaudhary](https://github.com/thepunitchaudhary)

---

*Built with ❤️ using FastAPI, Groq AI, and a passion for making healthcare more accessible.*
