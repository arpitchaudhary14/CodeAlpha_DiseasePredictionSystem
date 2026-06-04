import os
import google.generativeai as genai
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_symptoms_with_llm(symptoms, duration, severity, additional_notes=""):
    """
    Takes patient symptoms and context, constructs a prompt, and queries the Gemini LLM.
    Returns the raw markdown text response.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return ("**Error:** GEMINI_API_KEY is missing or invalid. Please configure your `.env` file.\n\n"
                "To get an API key, visit Google AI Studio.")

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
You are an advanced medical AI Symptom Analyzer. Your goal is to analyze the user's symptoms and provide a highly structured, objective assessment.

IMPORTANT RULES:
1. You MUST NOT claim to provide a definitive diagnosis.
2. You MUST include this exact disclaimer at the very beginning of your response: 
   "> **Disclaimer:** This is not a medical diagnosis. Please consult a qualified healthcare professional."
3. Format your response clearly using Markdown headings.

Patient Input:
- Symptoms: {symptoms}
- Duration: {duration}
- Severity: {severity}
- Additional Notes: {additional_notes if additional_notes else "None provided."}

Please output your analysis exactly in this format:

> **Disclaimer:** This is not a medical diagnosis. Please consult a qualified healthcare professional.

### Possible Conditions
(List 2-4 possible conditions based on the symptoms)
- Condition 1
- Condition 2

### Confidence
(State exactly one: Low / Medium / High, based on the specificity of the symptoms)

### Reasoning
(Provide a brief, 2-3 sentence clinical reasoning explaining why these conditions are suspected based on the provided symptoms, duration, and severity.)

### Recommendations & Next Steps
(List 3 actionable, non-prescriptive next steps, such as resting, hydration, or scheduling a doctor's appointment.)

### Emergency Warning Signs
(List 2-3 severe symptoms that would require immediate emergency medical attention given the context.)
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"**Error during analysis:** {str(e)}\n\nPlease ensure your API key is valid and you have internet connectivity."
