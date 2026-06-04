import logging
from django.contrib.auth.models import User
from .models import PredictionHistory

logger = logging.getLogger(__name__)

def save_prediction_history(user: User, disease_name: str, result: dict, feature_dict: dict) -> PredictionHistory:
    """
    Helper function to automatically capture ML layer outputs and save them to the database.
    This maintains a strict separation of concerns, keeping the ML predictor functions pure.
    
    Args:
        user (User): The Django User object making the request (can be None for anonymous).
        disease_name (str): The name of the disease model used (e.g., 'diabetes').
        result (dict): The output from the ML predictor (containing 'prediction', 'label', 'probability').
        feature_dict (dict): The raw input dictionary submitted to the predictor.
        
    Returns:
        PredictionHistory: The created database record.
    """
    try:
        # If user is not authenticated (e.g., anonymous), set to None
        db_user = user if user and user.is_authenticated else None
        
        history_record = PredictionHistory.objects.create(
            user=db_user,
            disease=disease_name,
            prediction=result.get('prediction'),
            label=result.get('label'),
            probability=result.get('probability'),
            input_data=feature_dict
        )
        
        logger.info(f"Saved prediction history for {disease_name} (ID: {history_record.id})")
        return history_record
        
    except Exception as e:
        # We don't want a database error to crash the user's prediction result screen
        logger.error(f"Failed to save prediction history for {disease_name}: {str(e)}")
        return None
