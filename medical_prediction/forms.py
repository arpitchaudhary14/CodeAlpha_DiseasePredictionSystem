from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from .ml.config import FEATURE_COLUMNS
from .ml.feature_meta import get_feature_meta

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required for account recovery and verification.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

def create_disease_form(disease_name):
    """
    Factory function to dynamically generate a Django form based on the 
    feature columns expected by the ML model.
    """
    if disease_name not in FEATURE_COLUMNS:
        raise ValueError(f"Unknown disease: {disease_name}")
        
    features = FEATURE_COLUMNS[disease_name]
    
    # Create a dictionary of form fields
    fields = {}
    for feature in features:
        meta = get_feature_meta(feature)
        label = meta.get('label', feature)
        choices = meta.get('choices')
        
        # All fields are not required so we can handle missing values
        if choices:
            fields[feature] = forms.ChoiceField(
                label=label, 
                choices=choices, 
                required=False, 
                widget=forms.Select(attrs={'class': 'form-control'})
            )
        else:
            default_val = meta.get('default')
            
            # Prepare widget attributes including min/max
            attrs = {'class': 'form-control'}
            if 'min' in meta:
                attrs['min'] = meta['min']
            if 'max' in meta:
                attrs['max'] = meta['max']
                
            if isinstance(default_val, float):
                attrs['step'] = 'any'
                fields[feature] = forms.FloatField(
                    label=label, 
                    required=False,
                    min_value=meta.get('min'),
                    max_value=meta.get('max'),
                    widget=forms.NumberInput(attrs=attrs)
                )
            elif isinstance(default_val, int):
                fields[feature] = forms.IntegerField(
                    label=label, 
                    required=False,
                    min_value=meta.get('min'),
                    max_value=meta.get('max'),
                    widget=forms.NumberInput(attrs=attrs)
                )
            else:
                fields[feature] = forms.CharField(
                    label=label, 
                    required=False,
                    widget=forms.TextInput(attrs={'class': 'form-control'})
                )
            
    # Dynamically create the Form class
    FormClass = type(f'{disease_name.title()}Form', (forms.Form,), fields)
    return FormClass

# Pre-generate the form classes for import in views
DiabetesForm = create_disease_form('diabetes')
HeartForm = create_disease_form('heart')
KidneyForm = create_disease_form('kidney')
LiverForm = create_disease_form('liver')
BreastCancerForm = create_disease_form('breast_cancer')

class SymptomAnalyzerForm(forms.Form):
    SEVERITY_CHOICES = [
        ('Low', 'Low - Mild discomfort, does not interfere with daily activities'),
        ('Medium', 'Medium - Bothersome, partially interferes with daily activities'),
        ('High', 'High - Severe, significantly limits daily activities'),
        ('Severe', 'Severe - Intolerable, requires immediate attention'),
    ]

    symptoms = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'E.g., Fever, headache, body pain, nausea...'
        }),
        label="Describe your symptoms in detail"
    )
    duration = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'E.g., 3 days, 2 weeks'
        }),
        label="How long have you had these symptoms?"
    )
    severity = forms.ChoiceField(
        choices=SEVERITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Severity of symptoms"
    )
    additional_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any other relevant information (e.g., existing medical conditions, medications)?'
        }),
        label="Additional Notes (Optional)"
    )

class DocumentUploadForm(forms.Form):
    DOCUMENT_TYPES = [
        ('general_report', 'General Medical Report (PDF, TXT, Image)'),
        ('lab_report', 'Lab Report / Blood Test (CBC, KFT, LFT, etc.)'),
        ('prescription', 'Prescription Reader (Image or PDF)'),
    ]

    document_type = forms.ChoiceField(
        choices=DOCUMENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Document Type"
    )
    document_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.txt,.png,.jpg,.jpeg'}),
        label="Upload Document"
    )

class HealthAssistantForm(forms.Form):
    query = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'E.g., What does my high fasting glucose mean? Or, how can I improve my sleep?'
        }),
        label="Ask a health question"
    )
