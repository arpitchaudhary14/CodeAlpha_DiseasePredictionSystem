import os
import google.generativeai as genai
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_medical_document(file_bytes, mime_type, document_type):
    """
    Takes file bytes, determines the mime type, and constructs a precise 
    prompt based on the document_type to query Gemini 1.5 Flash.
    Returns the raw markdown text response.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return ("**Error:** GEMINI_API_KEY is missing or invalid. Please configure your `.env` file.\n\n"
                "To get an API key, visit Google AI Studio.")

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 1. Base Guardrails
        base_disclaimer = "> **Disclaimer:** This is not a medical diagnosis and I cannot prescribe treatment. Please consult a qualified healthcare professional before making any medical decisions.\n\n"
        
        # 2. Dynamic Prompt Construction
        if document_type == 'general_report':
            prompt = """
            You are an advanced AI Medical Report Explainer.
            Analyze the attached medical report and provide a highly structured, objective summary.
            
            IMPORTANT RULES:
            1. Do not provide a diagnosis.
            2. Do not prescribe treatment.
            
            Output format (use Markdown headings):
            ### Summary
            (A brief 3-4 sentence summary of the report in simple language)
            
            ### Important Findings
            (Bullet points of key findings)
            
            ### Abnormal Values / Concerns
            (Highlight any abnormalities or state 'No significant abnormalities found')
            
            ### Medical Terms Explained
            (List 3-5 complex medical terms found in the report and explain them in simple English)
            
            ### Suggested Follow-Up Questions
            (3 questions the patient should ask their doctor)
            """
        elif document_type == 'lab_report':
            prompt = """
            You are an AI Lab Report Interpreter.
            Analyze the attached lab report (e.g., CBC, KFT, LFT, Lipid, Blood Sugar, Thyroid).
            
            IMPORTANT RULES:
            1. Do not provide a diagnosis.
            2. Do not prescribe treatment.
            
            Output format (use Markdown headings):
            ### Overall Assessment
            (A brief, easy-to-understand summary of the overall lab results)
            
            ### Normal Values
            (List key markers that fall within the standard healthy range)
            
            ### Abnormal Values
            (List markers that are high/low compared to standard ranges. Provide the standard range for context)
            
            ### What These Values Mean
            (Explain the function of the abnormal markers in simple terms)
            
            ### Questions To Discuss With Your Doctor
            (2-3 actionable questions based on these specific results)
            """
        elif document_type == 'prescription':
            prompt = """
            You are an AI Prescription Reader.
            Read the attached prescription image or PDF.
            
            IMPORTANT RULES:
            1. Clearly indicate uncertainty if the handwriting is unclear (e.g., "[Unclear - please verify]").
            2. Never recommend medication changes.
            3. Never replace doctor advice.
            
            Output format (use Markdown headings):
            > **Notice:** This information is extracted from a prescription and may contain OCR errors due to handwriting. Please verify with your healthcare provider.
            
            ### Medicines
            (List each medicine found)
            
            ### Dosage
            (State the dosage for each medicine)
            
            ### Frequency
            (State how often it should be taken)
            
            ### Instructions
            (E.g., Before food, after food, etc.)
            
            ### Warnings / Notes
            (Any additional doctor notes or general warnings about these medications)
            """
        else:
            return "**Error:** Invalid document type selected."
        
        # 3. Construct the Payload
        # Gemini 1.5 Flash natively accepts inline data for pdf, png, jpeg, webp
        # If the file is plain text, we decode it.
        
        if mime_type.startswith('text/'):
            text_content = file_bytes.decode('utf-8', errors='ignore')
            contents = [prompt, text_content]
        else:
            # Map docx to application/vnd.openxmlformats-officedocument.wordprocessingml.document
            # But Gemini vision natively supports pdf and images. If it's a docx, we will try text extraction 
            # in the view, but here we assume it's pdf or image.
            document_part = {
                "mime_type": mime_type,
                "data": file_bytes
            }
            contents = [prompt, document_part]
            
        # 4. Generate Response
        response = model.generate_content(contents)
        
        # Append base disclaimer if it's not a prescription (prescription has custom notice)
        final_text = response.text
        if document_type != 'prescription':
            final_text = base_disclaimer + final_text
            
        return final_text
        
    except Exception as e:
        return f"**Error during analysis:** {str(e)}\n\nPlease ensure your API key is valid and the file is not corrupted."
