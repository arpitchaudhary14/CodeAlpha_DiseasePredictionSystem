import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_health_assistant(query, user_history_summary=""):
    """
    Answers a health-related query using Gemini 1.5 Flash.
    Enforces strict medical disclaimers.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return ("**Error:** GEMINI_API_KEY is missing or invalid. Please configure your `.env` file.\n\n"
                "To get an API key, visit Google AI Studio.")

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        You are 'MediSense Health Assistant', an empathetic and knowledgeable AI health assistant.
        
        IMPORTANT RULES:
        1. Always state clearly that you are an AI and cannot provide a medical diagnosis or prescribe treatment.
        2. Give helpful, general health information and context.
        3. Keep your answers concise, structured (use bullet points and bold text), and easy to read.
        
        User's Past Prediction Context (if any):
        {user_history_summary if user_history_summary else "No previous medical prediction context provided."}
        
        User's Question:
        {query}
        """
        
        response = model.generate_content(prompt)
        
        disclaimer = "> **Disclaimer:** I am an AI, not a doctor. This information is for educational purposes and cannot replace professional medical advice. Always consult a healthcare provider for medical decisions.\n\n"
        
        return disclaimer + response.text
        
    except Exception as e:
        return f"**Error during analysis:** {str(e)}\n\nPlease try again later."
