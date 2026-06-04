from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public
    path('', views.landing_view, name='landing'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    
    # Password Reset
    path('password-reset/', views.RateLimitedPasswordResetView.as_view(
        template_name='auth/password_reset_form.html',
        email_template_name='auth/password_reset_email.txt',
        html_email_template_name='auth/password_reset_email.html',
        subject_template_name='auth/password_reset_subject.txt'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
    
    # Dashboard & History
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('history/', views.history_view, name='history'),
    
    # Disease Prediction
    path('predict/diabetes/', views.predict_diabetes_view, name='predict_diabetes'),
    path('predict/heart/', views.predict_heart_view, name='predict_heart'),
    path('predict/kidney/', views.predict_kidney_view, name='predict_kidney'),
    path('predict/liver/', views.predict_liver_view, name='predict_liver'),
    path('predict/breast-cancer/', views.predict_breast_cancer_view, name='predict_breast_cancer'),
    path('predict/symptoms/', views.analyze_symptoms_view, name='symptom_analyzer'),
    path('predict/document/', views.document_analysis_view, name='document_analyzer'),
    path('assistant/', views.health_assistant_view, name='health_assistant'),
    path('analytics/', views.analytics_dashboard_view, name='analytics'),
    path('history/delete/<int:item_id>/', views.delete_history_item_view, name='delete_history_item'),
    path('history/delete-all/', views.delete_all_history_view, name='delete_all_history'),
    path('contact/', views.contact_view, name='contact'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
]
