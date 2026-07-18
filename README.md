# MediSense AI 🏥🤖

**[🌐 Live Demo — Try it here!](https://medisense-ai-9mnr.onrender.com/)**

MediSense is an advanced, production-ready, AI-powered healthcare diagnostics platform. It provides sophisticated machine learning predictions for major diseases (Diabetes, Liver Disease, Breast Cancer, Heart Disease, Kidney Disease) and integrates Google Gemini AI for symptom analysis, medical document processing, and an interactive health assistant.

## ✨ Key Features

### 🔬 Machine Learning Diagnostics
- Pre-trained robust scikit-learn/XGBoost models integrated via `joblib`.
- Predicts disease risk based on clinical and laboratory input data.
- Handles missing data gracefully by injecting baseline medical averages to avoid input errors.
- Clean, non-technical UI tailored for both patients and medical professionals.

### 🧠 Gemini AI Integration
- **Health Assistant:** Conversational AI capable of answering health-related queries using Google's `gemini-2.5-flash` model.
- **Symptom Analyzer:** Analyzes a list of user-provided symptoms to suggest possible medical conditions with structured reasoning.
- **Document & Prescription AI:** Analyzes uploaded medical PDFs, X-Rays, or prescriptions to summarize complex medical jargon into easy-to-understand insights.
- **Rate Limited:** Highly secure custom rate-limiting (`@gemini_rate_limit`) to prevent API abuse (5 requests / 30 minutes).

### 🔒 Enterprise-Grade Security & Authentication
- Secure registration and login flow.
- Configured with strict 2-minute (`PASSWORD_RESET_TIMEOUT = 120`) email password reset tokens.
- Custom rate-limited password reset endpoint (max 3 requests / 30 minutes) to prevent email spam.
- Fully configured SMTP email integration for transactional emails.
- Auto-logout AFK session timeouts.

## 🛠️ Technology Stack
- **Backend:** Django 5, Python 3
- **Machine Learning:** Scikit-Learn, XGBoost, Pandas, Joblib
- **Generative AI:** Google Generative AI SDK (`google-generativeai`)
- **Frontend:** HTML5, CSS3 (Custom Responsive Design), Vanilla JavaScript
- **Database:** SQLite (Development) / PostgreSQL (Production via Supabase)
- **Deployment:** Render (Web Service + PostgreSQL)

## 🚀 Local Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/arpitchaudhary14/CodeAlpha_DiseasePredictionSystem.git
cd CodeAlpha_DiseasePredictionSystem
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file and create a new `.env` file in the root directory.
```bash
cp .env.example .env
```
Fill in the following variables in your `.env` file:
- `SECRET_KEY`: Your Django secret key.
- `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`: Your Gmail credentials (App Password).
- `GEMINI_API_KEY`: Your Google AI Studio API key (Required for AI features).
- `GMAIL_WEBHOOK_URL`: Google Apps Script Webhook URL (Required for emails on Render — see Deployment Note below).

> **Deployment Note:** Platforms like Render block SMTP ports on free tier. For emails to work in production, create a Google Apps Script Web App and add its URL as `GMAIL_WEBHOOK_URL` in your environment variables.

### 5. Run Migrations & Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 6. Access the Application
Open your browser and navigate to `http://127.0.0.1:8000/`.

## ⚠️ Disclaimer
**MediSense is designed for educational, informational, and preliminary analytical purposes only.** The AI predictions and models do not constitute professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

---
© 2026 MediSense AI. Powered by ResoNate. A [CodeAlpha](https://www.codealpha.tech) Internship Project.
