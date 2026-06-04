from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class PredictionHistory(models.Model):
    """
    Model to store historical records of machine learning predictions.
    It links each prediction to a user and logs the exact inputs and outputs.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='predictions')
    disease = models.CharField(max_length=100, help_text="Name of the disease model used (e.g., 'diabetes', 'heart')")
    prediction = models.IntegerField(help_text="The raw numerical prediction output (e.g., 0, 1, 2)")
    label = models.CharField(max_length=50, help_text="The human-readable label mapped from the prediction (e.g., 'High Risk')")
    probability = models.FloatField(help_text="The confidence probability score from the model")
    input_data = models.JSONField(help_text="The raw feature dictionary submitted by the user")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Prediction Histories"

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - {self.disease.capitalize()} Prediction ({self.label})"

class SymptomAnalysisHistory(models.Model):
    """
    Model to store historical records of LLM-based symptom analysis.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='symptom_analyses')
    symptoms = models.TextField(help_text="The symptoms described by the user")
    duration = models.CharField(max_length=100, help_text="Duration of symptoms")
    severity = models.CharField(max_length=50, help_text="Severity level (Low, Medium, High, Severe)")
    additional_notes = models.TextField(blank=True, null=True, help_text="Any additional context provided")
    
    # Store the generated response from the AI
    ai_response = models.TextField(help_text="The raw markdown response from the LLM")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Symptom Analysis Histories"

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - Symptom Analysis on {self.created_at.strftime('%Y-%m-%d')}"

class DocumentAnalysisHistory(models.Model):
    """
    Model to store historical records of LLM-based medical document analysis.
    Raw files are NOT stored for privacy and HIPAA compliance reasons.
    """
    DOCUMENT_TYPES = [
        ('general_report', 'General Medical Report'),
        ('lab_report', 'Lab Report (CBC, KFT, LFT, etc.)'),
        ('prescription', 'Prescription Reader'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='document_analyses')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file_name = models.CharField(max_length=255, help_text="Original file name uploaded (for reference only)")
    
    # Store the generated response from the AI
    ai_response = models.TextField(help_text="The raw markdown response from the LLM")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Document Analysis Histories"

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - {self.get_document_type_display()} on {self.created_at.strftime('%Y-%m-%d')}"

class HealthAssistantHistory(models.Model):
    """
    Model to store historical records of questions asked to the Health Assistant AI.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='health_assistant_queries')
    user_query = models.TextField(help_text="The question asked by the user")
    ai_response = models.TextField(help_text="The raw markdown response from the AI assistant")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Health Assistant Histories"

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - Assistant Query on {self.created_at.strftime('%Y-%m-%d')}"
