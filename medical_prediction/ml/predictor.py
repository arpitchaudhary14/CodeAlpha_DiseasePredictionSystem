import pandas as pd
from typing import Dict, Any
from .config import FEATURE_COLUMNS
from .model_loader import ModelLoader

def _prepare_input(disease_name: str, feature_dict: Dict[str, Any]) -> pd.DataFrame:
    """
    Internal helper to validate input dictionary against the exact feature columns
    used during model training, and convert it into a Pandas DataFrame.
    """
    required_cols = FEATURE_COLUMNS[disease_name]
    
    # Check for missing columns
    missing_cols = [col for col in required_cols if col not in feature_dict]
    if missing_cols:
        raise ValueError(f"Missing required features for {disease_name}: {missing_cols}")
        
    # Convert to DataFrame ensuring exact column order
    df = pd.DataFrame([feature_dict])
    df = df[required_cols]
    
    # Ensure numeric types where appropriate (Pandas handles inferring, but we ensure no generic objects if possible)
    return df

def _generate_response(prediction: int, probability: float, labels: tuple) -> dict:
    """
    Standardizes the prediction response format.
    labels: Tuple of (Negative_Label, Positive_Label) e.g., ('Low Risk', 'High Risk')
    """
    label = labels[1] if prediction == 1 else labels[0]
    return {
        "prediction": int(prediction),
        "label": label,
        "probability": round(float(probability), 4)
    }

def predict_diabetes(feature_dict: Dict[str, Any]) -> dict:
    model = ModelLoader.get_model('diabetes')
    df = _prepare_input('diabetes', feature_dict)
    
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    return _generate_response(prediction, probability, ("Negative", "Positive"))

def predict_heart(feature_dict: Dict[str, Any]) -> dict:
    model = ModelLoader.get_model('heart')
    df = _prepare_input('heart', feature_dict)
    
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    return _generate_response(prediction, probability, ("Low Risk", "High Risk"))

def predict_kidney(feature_dict: Dict[str, Any]) -> dict:
    model = ModelLoader.get_model('kidney')
    df = _prepare_input('kidney', feature_dict)
    
    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]
    
    # Kidney uses LabelEncoder mapping:
    # 0: High_Risk, 1: Low_Risk, 2: Moderate_Risk, 3: No_Disease, 4: Severe_Disease
    labels_map = {
        0: "High Risk",
        1: "Low Risk",
        2: "Moderate Risk",
        3: "No Disease",
        4: "Severe Disease"
    }
    
    label = labels_map.get(prediction, "Unknown")
    probability = probabilities.max()
    
    return {
        "prediction": int(prediction),
        "label": label,
        "probability": round(float(probability), 4)
    }

def predict_liver(feature_dict: Dict[str, Any]) -> dict:
    model = ModelLoader.get_model('liver')
    df = _prepare_input('liver', feature_dict)
    
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    return _generate_response(prediction, probability, ("Negative", "Positive"))

def predict_breast_cancer(feature_dict: Dict[str, Any]) -> dict:
    model = ModelLoader.get_model('breast_cancer')
    df = _prepare_input('breast_cancer', feature_dict)
    
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    # Sklearn load_breast_cancer maps 0 to Malignant, 1 to Benign.
    # We will output Malignant for 0 and Benign for 1.
    label = "Benign" if prediction == 1 else "Malignant"
    return {
        "prediction": int(prediction),
        "label": label,
        "probability": round(float(probability), 4)
    }
