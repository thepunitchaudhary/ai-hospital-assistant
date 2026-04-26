# 🏥 City Hospital – Sarah AI Receptionist

An AI-powered voice-based hospital assistant that allows patients to **register, log in, and book appointments using natural voice interaction**. Built with a full-stack architecture and deployable on cloud platforms.

---

## 🚀 Features

* 🔐 **Secure Authentication**

  * User registration & login
  * Password hashing for security

* 🎙️ **AI Voice Assistant (Sarah)**

  * Book appointments using natural speech
  * Powered by Groq AI

* 📅 **Smart Appointment System**

  * Book, store, and retrieve appointments
  * Linked with user accounts

* 📊 **Patient Dashboard**

  * View appointment history
  * Auto-refresh after booking

* 📧 **Email Notifications**

  * Welcome email on registration
  * Appointment confirmation emails

* 🌐 **Persistent Login**

  * Token-based authentication
  * User stays logged in

---

## 🏥 Departments & Doctors

| Department  | Doctor          |
| ----------- | --------------- |
| Cardiology  | Dr. Meera Patel |
| Neurology   | Dr. Arjun Rao   |
| Orthopedics | Dr. Priya Nair  |

---

## ⚙️ Tech Stack

* **Backend:** FastAPI (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **AI Integration:** Groq API
* **Email Service:** SMTP (Gmail)

---

## 📂 Project Structure

```
AI Hospital Assistant/
│
├── app.py
├── auth.py
├── database.py
├── models.py
├── utils.py
├── agent.py
├── frontend.html
├── requirements.txt
├── .env (not uploaded to GitHub)
└── README.md
```

---

## 🛠️ Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Create `.env` File

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_groq_api_key
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
```

---

### 🔑 How to Get Credentials

* **GROQ API Key:** https://console.groq.com
* **SMTP Email:** Your Gmail address
* **SMTP Password:**

  * Go to Google Account → Security
  * Enable 2-Step Verification
  * Generate App Password (Mail, Windows)

---

### 3️⃣ Run the Application

```bash
python app.py
```

---

### 4️⃣ Open in Browser

```
http://127.0.0.1:8000
```

---

## 🌐 Deployment (Render)

1. Push project to GitHub
2. Go to **Render.com → New Web Service**
3. Connect your GitHub repository
4. Use the following start command:

```bash
uvicorn app:app --host 0.0.0.0 --port 10000
```

5. Add environment variables in Render dashboard
6. Click **Deploy**

---

## ⚠️ Important Configuration

Update API URL in `frontend.html`:

```javascript
const API = "https://your-app.onrender.com";
```

---

## 🎯 Key Highlights

* Built a **real-world AI healthcare assistant**
* Implemented **secure authentication system**
* Integrated **voice-based AI booking system**
* Developed a **full-stack deployable web application**
* Designed **user-friendly dashboard interface**

---

## 📸 Future Improvements

* 🎨 Modern UI with animations
* 📱 Mobile responsive design
* 🔔 Real-time notifications
* 🧠 Advanced AI conversation handling

---

## 🤝 Contributing

Feel free to fork this project and improve it. Contributions are welcome!

---

## 📧 Contact

For any queries or collaboration:

* 📩 Email: [your_email@gmail.com](mailto:your_email@gmail.com)
* 💼 LinkedIn: your_linkedin_profile

---

⭐ If you like this project, don’t forget to **star the repo!**
