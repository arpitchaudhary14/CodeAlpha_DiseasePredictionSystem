from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import views as auth_views
from functools import wraps

from .models import PredictionHistory, SymptomAnalysisHistory, DocumentAnalysisHistory, UserProfile, HealthAssistantHistory
from .utils import save_prediction_history
from .forms import (
    DiabetesForm, HeartForm, KidneyForm, LiverForm, BreastCancerForm, CustomUserCreationForm, SymptomAnalyzerForm, DocumentUploadForm, UserProfileForm, HealthAssistantForm
)
from .ml.predictor import (
    predict_diabetes, predict_heart, predict_kidney, 
    predict_liver, predict_breast_cancer
)
from .ml.symptom_analyzer import analyze_symptoms_with_llm
from .ml.document_analyzer import analyze_medical_document
from .ml.assistant import ask_health_assistant
from .ml.feature_meta import get_feature_meta
import markdown

# --- Public Views ---
def landing_view(request):
    return render(request, 'pages/landing.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'Unknown User')
        email = request.POST.get('email', 'No Email')
        message = request.POST.get('message', 'No Message')
        
        subject = f"MediSense Contact Form: Message from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER], # Send to the admin inbox
                fail_silently=False,
            )
            messages.success(request, 'Thank you! Your message has been sent. We will get back to you shortly.')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
            
        return redirect('dashboard') if request.user.is_authenticated else redirect('landing')

    return render(request, 'pages/contact.html')

def privacy_view(request):
    return render(request, 'pages/privacy.html')

def terms_view(request):
    return render(request, 'pages/terms.html')

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        confirm_username = request.POST.get('confirm_username')
        if confirm_username == request.user.username:
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('landing')
        else:
            messages.error(request, 'Username confirmation did not match. Account deletion aborted.')
    return redirect('profile')

# --- Authentication Views ---
class RateLimitedPasswordResetView(auth_views.PasswordResetView):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        client_ip = request.META.get('REMOTE_ADDR')
        
        if email:
            # Rate limit by email and IP
            cache_key = f'password_reset_{email}_{client_ip}'
            attempts = cache.get(cache_key, 0)
            
            if attempts >= 3:
                messages.error(request, 'Too many requests. Please wait 30 minutes before trying again.')
                return redirect('password_reset')
            
            # Increment attempts and set cache for 30 minutes
            cache.set(cache_key, attempts + 1, 60 * 30)
            
        return super().post(request, *args, **kwargs)

def gemini_rate_limit(limit=5, timeout=1800):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method == 'POST':
                client_ip = request.META.get('REMOTE_ADDR')
                user_identifier = request.user.id if request.user.is_authenticated else client_ip
                cache_key = f'gemini_rate_limit_{user_identifier}'
                
                attempts = cache.get(cache_key, 0)
                if attempts >= limit:
                    messages.error(request, 'You have reached the limit for AI requests (5 per 30 mins). Please try again later.')
                    return redirect('dashboard')
                
                cache.set(cache_key, attempts + 1, timeout)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to MediSense!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have successfully logged out.')
    return redirect('login')

@login_required
def profile_view(request):
    # Ensure profile exists
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
        
    return render(request, 'auth/profile.html', {'form': form, 'profile': profile})

# --- Dashboard & History Views ---
@login_required
def dashboard_view(request):
    recent_history = PredictionHistory.objects.filter(user=request.user)[:5]
    return render(request, 'pages/dashboard.html', {'recent_history': recent_history})

@login_required
def history_view(request):
    model_filter = request.GET.get('model', '')
    if model_filter:
        history = PredictionHistory.objects.filter(user=request.user, disease=model_filter).order_by('-created_at')
    else:
        history = PredictionHistory.objects.filter(user=request.user).order_by('-created_at')
        
    return render(request, 'pages/history.html', {'history': history, 'current_filter': model_filter})

@login_required
def delete_history_item_view(request, item_id):
    if request.method == 'POST':
        item = PredictionHistory.objects.filter(id=item_id, user=request.user).first()
        if item:
            item.delete()
            messages.success(request, 'History record deleted.')
        else:
            messages.error(request, 'Record not found.')
    return redirect('history')

@login_required
def delete_all_history_view(request):
    if request.method == 'POST':
        PredictionHistory.objects.filter(user=request.user).delete()
        messages.success(request, 'All prediction history has been cleared.')
    return redirect('history')

# --- Prediction Core Logic ---
def _handle_prediction(request, FormClass, predict_func, disease_name, title, description):
    result = None
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            try:
                # Get clean dict of features
                feature_dict = form.cleaned_data
                
                # Apply defaults for any missing values
                for key, val in feature_dict.items():
                    if val is None or val == '':
                        meta = get_feature_meta(key)
                        feature_dict[key] = meta.get('default', 0)
                
                # Execute ML logic
                result = predict_func(feature_dict)
                
                # Save to database
                save_prediction_history(request.user, disease_name, result, feature_dict)
                
                messages.success(request, f'{title} Prediction completed successfully.')
            except Exception as e:
                messages.error(request, f'Error during prediction: {str(e)}')
    else:
        form = FormClass()
        
    context = {
        'form': form,
        'title': title,
        'description': description,
        'result': result
    }
    return render(request, 'pages/prediction.html', context)

# --- Disease Specific Views ---
@login_required
def predict_diabetes_view(request):
    return _handle_prediction(
        request, DiabetesForm, predict_diabetes, 'diabetes',
        'Diabetes Risk Prediction',
        'Enter patient demographics and health indicators to predict diabetes risk using our XGBoost model.'
    )

@login_required
def predict_heart_view(request):
    return _handle_prediction(
        request, HeartForm, predict_heart, 'heart',
        'Heart Disease Prediction',
        'Analyze cardiovascular risk factors to assess the likelihood of heart disease using our robust model.'
    )

@login_required
def predict_kidney_view(request):
    return _handle_prediction(
        request, KidneyForm, predict_kidney, 'kidney',
        'Kidney Disease Prediction',
        'Predict the stage/risk of chronic kidney disease based on comprehensive lab results.'
    )

@login_required
def predict_liver_view(request):
    return _handle_prediction(
        request, LiverForm, predict_liver, 'liver',
        'Liver Disease Prediction',
        'Assess liver health parameters (Bilirubin, Albumin, etc.) to detect potential liver disease.'
    )

@login_required
def predict_breast_cancer_view(request):
    return _handle_prediction(
        request, BreastCancerForm, predict_breast_cancer, 'breast_cancer',
        'Breast Cancer Prediction',
        'Analyze cell nucleus features extracted from digitized images to predict benign or malignant status.'
    )

# --- AI Symptom Analyzer View ---
@login_required
@gemini_rate_limit(limit=5, timeout=1800)
def analyze_symptoms_view(request):
    result = None
    if request.method == 'POST':
        form = SymptomAnalyzerForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data.get('symptoms')
            duration = form.cleaned_data.get('duration')
            severity = form.cleaned_data.get('severity')
            additional_notes = form.cleaned_data.get('additional_notes')
            
            try:
                # Call LLM
                ai_response = analyze_symptoms_with_llm(
                    symptoms, duration, severity, additional_notes
                )
                
                # Save History
                SymptomAnalysisHistory.objects.create(
                    user=request.user,
                    symptoms=symptoms,
                    duration=duration,
                    severity=severity,
                    additional_notes=additional_notes,
                    ai_response=ai_response
                )
                
                # Render the markdown response to HTML for safe display
                result = markdown.markdown(ai_response)
                messages.success(request, 'Symptoms analyzed successfully.')
            except Exception as e:
                messages.error(request, f'Error analyzing symptoms: {str(e)}')
    else:
        form = SymptomAnalyzerForm()
        
    context = {
        'form': form,
        'title': 'AI Symptom Analyzer',
        'description': 'Describe your symptoms in detail to receive an AI-powered assessment, potential conditions, and recommended next steps.',
        'result': result
    }
    return render(request, 'pages/symptom_analyzer.html', context)

# --- AI Document Analyzer View ---
@login_required
@gemini_rate_limit(limit=5, timeout=1800)
def document_analysis_view(request):
    result = None
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document_type = form.cleaned_data.get('document_type')
            uploaded_file = form.cleaned_data.get('document_file')
            
            try:
                # Read file into memory
                file_bytes = uploaded_file.read()
                mime_type = uploaded_file.content_type
                file_name = uploaded_file.name
                
                # Gemini natively parses pdf, txt, png, jpeg.
                # If it's a docx, we handle it if needed, else we rely on the prompt to error out if unsupported.
                # (We restricted accept attributes in the form to .pdf,.txt,.png,.jpg,.jpeg)
                
                # Call LLM
                ai_response = analyze_medical_document(
                    file_bytes=file_bytes,
                    mime_type=mime_type,
                    document_type=document_type
                )
                
                # Save History (no raw file saved!)
                DocumentAnalysisHistory.objects.create(
                    user=request.user,
                    document_type=document_type,
                    file_name=file_name,
                    ai_response=ai_response
                )
                
                # Render markdown to safe HTML
                result = markdown.markdown(ai_response)
                messages.success(request, 'Document analyzed successfully.')
            except Exception as e:
                messages.error(request, f'Error processing document: {str(e)}')
    else:
        initial_data = {}
        doc_type = request.GET.get('type')
        if doc_type in ['general_report', 'lab_report', 'prescription']:
            initial_data['document_type'] = doc_type
        form = DocumentUploadForm(initial=initial_data)
        
    # Dynamically set title and description based on selected type
    effective_doc_type = request.POST.get('document_type') if request.method == 'POST' else request.GET.get('type')
    
    title = 'Document Intelligence'
    description = 'Upload your medical report, lab results, or prescription for secure AI analysis.'
    
    if effective_doc_type == 'prescription':
        title = 'Prescription Reader'
        description = 'Upload your handwritten or printed prescription to extract medicines and dosages.'
    elif effective_doc_type == 'lab_report':
        title = 'Lab Report Analyzer'
        description = 'Upload your CBC, KFT, LFT, or other blood test reports for AI interpretation.'

    context = {
        'form': form,
        'title': title,
        'description': description,
        'result': result
    }
    return render(request, 'pages/document_analyzer.html', context)

# --- AI Health Assistant View ---
@login_required
@gemini_rate_limit(limit=5, timeout=1800)
def health_assistant_view(request):
    result = None
    if request.method == 'POST':
        form = HealthAssistantForm(request.POST)
        if form.is_valid():
            user_query = form.cleaned_data.get('query')
            
            try:
                # Optionally fetch some recent history context for the LLM
                recent_history = PredictionHistory.objects.filter(user=request.user).order_by('-created_at')[:3]
                context_str = ""
                if recent_history.exists():
                    context_str = "User's Recent Medical Predictions:\n"
                    for h in recent_history:
                        context_str += f"- {h.disease.title()} Risk: {h.probability*100:.1f}%\n"
                
                # Call LLM
                ai_response = ask_health_assistant(user_query, context_str)
                
                # Save History
                HealthAssistantHistory.objects.create(
                    user=request.user,
                    user_query=user_query,
                    ai_response=ai_response
                )
                
                # Render markdown to HTML
                result = markdown.markdown(ai_response)
                messages.success(request, 'Assistant responded successfully.')
            except Exception as e:
                messages.error(request, f'Error from assistant: {str(e)}')
    else:
        form = HealthAssistantForm()
        
    context = {
        'form': form,
        'title': 'AI Health Assistant',
        'description': 'Ask any health-related questions. The assistant is aware of your recent prediction results.',
        'result': result
    }
    return render(request, 'pages/assistant.html', context)

# --- AI Analytics & Health Timeline View ---
import json
from collections import defaultdict

@login_required
def analytics_dashboard_view(request):
    histories = PredictionHistory.objects.filter(user=request.user).order_by('created_at')
    
    if not histories.exists():
        messages.info(request, "Not enough prediction data to generate analytics. Please take some risk assessments first.")
        return redirect('dashboard')

    # 1. Aggregate Data
    disease_map = defaultdict(list)
    for h in histories:
        disease_map[h.disease].append(h)
        
    latest_risks = {}
    trends = []
    
    for disease, records in disease_map.items():
        latest_record = records[-1]
        latest_risks[disease] = latest_record.probability
        
        # Calculate Trend
        if len(records) > 1:
            prev_record = records[-2]
            delta = latest_record.probability - prev_record.probability
            if abs(delta) > 0.05: # Only log significant changes > 5%
                status = "worsened" if delta > 0 else "improved"
                trends.append({
                    'disease': disease.replace('_', ' ').title(),
                    'date': latest_record.created_at,
                    'delta': delta * 100,
                    'status': status,
                    'message': f"{disease.replace('_', ' ').title()} risk {status} by {abs(delta*100):.1f}%"
                })

    # Sort trends chronologically descending
    trends.sort(key=lambda x: x['date'], reverse=True)
    
    # 2. Overall Health Score (100 - average risk)
    if latest_risks:
        avg_risk = sum(latest_risks.values()) / len(latest_risks)
        health_score = int(100 - (avg_risk * 100))
    else:
        health_score = 100
        
    # 3. Highest/Lowest Risk
    highest_disease = max(latest_risks, key=latest_risks.get) if latest_risks else None
    lowest_disease = min(latest_risks, key=latest_risks.get) if latest_risks else None

    # 4. Timeline Data for Chart.js
    # We will build a unified timeline chart showing all diseases over time
    chart_labels = []
    chart_datasets = {
        'diabetes': [], 'heart': [], 'kidney': [], 'liver': [], 'breast_cancer': []
    }
    
    # Extract unique dates formatted as YYYY-MM-DD
    unique_dates = []
    for h in histories:
        date_str = h.created_at.strftime('%Y-%m-%d')
        if date_str not in unique_dates:
            unique_dates.append(date_str)
            
    chart_labels = unique_dates
    
    # For each date and each disease, find the max probability on that date (or carry over previous if missing)
    current_state = {d: 0.0 for d in chart_datasets.keys()}
    for date_str in chart_labels:
        # Find all records on this date
        day_records = [h for h in histories if h.created_at.strftime('%Y-%m-%d') == date_str]
        for h in day_records:
            if h.disease in current_state:
                current_state[h.disease] = h.probability
                
        # Append state to datasets
        for d in chart_datasets.keys():
            chart_datasets[d].append(current_state[d] * 100) # Convert to percentage

    context = {
        'health_score': health_score,
        'highest_disease': highest_disease.replace('_', ' ').title() if highest_disease else "None",
        'highest_risk_val': (latest_risks.get(highest_disease, 0) * 100) if highest_disease else 0,
        'lowest_disease': lowest_disease.replace('_', ' ').title() if lowest_disease else "None",
        'lowest_risk_val': (latest_risks.get(lowest_disease, 0) * 100) if lowest_disease else 0,
        'trends': trends[:5], # Top 5 recent trends
        'radar_labels': json.dumps([d.replace('_', ' ').title() for d in latest_risks.keys()]),
        'radar_data': json.dumps([v * 100 for v in latest_risks.values()]),
        'line_labels': json.dumps(chart_labels),
        'line_datasets': json.dumps(chart_datasets)
    }
    return render(request, 'pages/analytics.html', context)
