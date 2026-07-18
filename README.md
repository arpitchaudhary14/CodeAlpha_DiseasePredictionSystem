# 🏥 MediSense AI - Intelligent Healthcare Diagnostics

MediSense AI is a full-stack, AI-powered healthcare platform that combines machine learning models with Google's Gemini AI to provide intelligent disease risk prediction, symptom analysis, medical document interpretation, and an interactive health assistant.

Designed with security, usability, and scalability in mind, the platform offers a seamless experience for both patients and healthcare enthusiasts while showcasing modern AI integration in web applications.

---

# ✨ Features

## 🔬 AI-Powered Disease Prediction

- Predicts the likelihood of multiple diseases using trained Machine Learning models.
- Supports prediction for:
  - Diabetes
  - Heart Disease
  - Breast Cancer
  - Kidney Disease
  - Liver Disease
- Built using pre-trained **Scikit-Learn** and **XGBoost** models.
- Automatically handles missing clinical values using medically appropriate baseline averages.
- Simple, intuitive interface for quick and accurate predictions.

---

## 🤖 Gemini AI Integration

### 💬 AI Health Assistant
- Conversational healthcare chatbot powered by **Google Gemini 2.5 Flash**.
- Answers general health-related questions in natural language.

### 🩺 Symptom Analyzer
- Analyzes user-provided symptoms.
- Suggests possible medical conditions with structured AI-generated explanations.

### 📄 Medical Document Analyzer
- Upload medical reports, prescriptions, or laboratory PDFs.
- AI summarizes complex medical terminology into easy-to-understand insights.

### ⚡ Secure API Usage
- Custom rate limiting protects Gemini API endpoints from excessive requests.
- Maximum **5 AI requests every 30 minutes** per user.

---

# 🔐 Security Features

- Secure user registration and authentication
- Email-based password reset
- Short-lived password reset tokens
- Rate-limited password reset requests
- Automatic inactive session logout
- Secure SMTP/Webhook email integration

---

# 🛠 Technology Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Django 5, Python 3 |
| **Machine Learning** | Scikit-Learn, XGBoost, Pandas, Joblib |
| **Generative AI** | Google Gemini API (`gemini-2.5-flash`) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Database** | SQLite (Development), PostgreSQL via Supabase |
| **Deployment** | Render |

---

# 🚀 Local Installation

## 1. Clone the Repository

```bash
git clone <repository_url>
cd CodeAlpha_DiseasePredictionSystem
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_django_secret_key

EMAIL_HOST_USER=your_email@gmail.com

EMAIL_HOST_PASSWORD=your_16_digit_app_password

GEMINI_API_KEY=your_google_ai_studio_api_key

GMAIL_WEBHOOK_URL=your_google_apps_script_webhook_url
```

> **Deployment Note**
>
> Free hosting platforms such as Render restrict SMTP access. To enable email functionality in production, configure a Google Apps Script Webhook and provide its URL using `GMAIL_WEBHOOK_URL`.

---

## 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Run the Development Server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

---

# 🧠 Machine Learning Models

The application uses multiple pre-trained Machine Learning models for disease prediction.

- Diabetes Prediction
- Heart Disease Prediction
- Breast Cancer Prediction
- Kidney Disease Prediction
- Liver Disease Prediction

All models are serialized using **Joblib** for fast inference and production deployment.

---

# 📌 Future Improvements

- Medical history tracking
- Personalized health recommendations
- Doctor appointment integration
- Multi-language AI support
- PDF report generation
- REST API for third-party healthcare applications

---

# ⚠️ Disclaimer

**MediSense AI is intended for educational and demonstration purposes only.**

The predictions, AI-generated analyses, and recommendations provided by this application should **not** be considered professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional before making medical decisions.

---

# 📄 License

© 2026 **MediSense AI**. All Rights Reserved.

Developed as a **CodeAlpha Internship Project**.