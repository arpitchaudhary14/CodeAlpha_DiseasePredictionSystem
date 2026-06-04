import os
from pathlib import Path
from django.conf import settings

# Attempt to use Django settings BASE_DIR, fallback to generic pathlib for standalone testing
try:
    BASE_DIR = settings.BASE_DIR
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Model Paths Configuration
MODEL_PATHS = {
    'diabetes': os.path.join(BASE_DIR, 'models', 'diabetes_model.pkl'),
    'heart': os.path.join(BASE_DIR, 'models', 'heart_model.pkl'),
    'kidney': os.path.join(BASE_DIR, 'models', 'kidney_model.pkl'),
    'liver': os.path.join(BASE_DIR, 'models', 'liver_model.pkl'),
    'breast_cancer': os.path.join(BASE_DIR, 'models', 'breast_cancer_model.pkl'),
}

# Single Source of Truth for Feature Columns (as used in ML training)
FEATURE_COLUMNS = {
    'diabetes': [
        'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 
        'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies', 
        'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth', 
        'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income'
    ],
    'heart': [
        'State', 'Sex', 'GeneralHealth', 'PhysicalHealthDays', 'MentalHealthDays', 
        'LastCheckupTime', 'PhysicalActivities', 'SleepHours', 'RemovedTeeth', 
        'HadAngina', 'HadStroke', 'HadAsthma', 'HadSkinCancer', 'HadCOPD', 
        'HadDepressiveDisorder', 'HadKidneyDisease', 'HadArthritis', 'HadDiabetes', 
        'DeafOrHardOfHearing', 'BlindOrVisionDifficulty', 'DifficultyConcentrating', 
        'DifficultyWalking', 'DifficultyDressingBathing', 'DifficultyErrands', 
        'SmokerStatus', 'ECigaretteUsage', 'ChestScan', 'RaceEthnicityCategory', 
        'AgeCategory', 'HeightInMeters', 'WeightInKilograms', 'BMI', 'AlcoholDrinkers', 
        'HIVTesting', 'FluVaxLast12', 'PneumoVaxEver', 'TetanusLast10Tdap', 
        'HighRiskLastYear', 'CovidPos'
    ],
    'kidney': [
        'Age of the patient', 'Blood pressure (mm/Hg)', 'Specific gravity of urine', 
        'Albumin in urine', 'Sugar in urine', 'Red blood cells in urine', 'Pus cells in urine', 
        'Pus cell clumps in urine', 'Bacteria in urine', 'Random blood glucose level (mg/dl)', 
        'Blood urea (mg/dl)', 'Serum creatinine (mg/dl)', 'Sodium level (mEq/L)', 
        'Potassium level (mEq/L)', 'Hemoglobin level (gms)', 'Packed cell volume (%)', 
        'White blood cell count (cells/cumm)', 'Red blood cell count (millions/cumm)', 
        'Hypertension (yes/no)', 'Diabetes mellitus (yes/no)', 'Coronary artery disease (yes/no)', 
        'Appetite (good/poor)', 'Pedal edema (yes/no)', 'Anemia (yes/no)', 
        'Estimated Glomerular Filtration Rate (eGFR)', 'Urine protein-to-creatinine ratio', 
        'Urine output (ml/day)', 'Serum albumin level', 'Cholesterol level', 
        'Parathyroid hormone (PTH) level', 'Serum calcium level', 'Serum phosphate level', 
        'Family history of chronic kidney disease', 'Smoking status', 'Body Mass Index (BMI)', 
        'Physical activity level', 'Duration of diabetes mellitus (years)', 
        'Duration of hypertension (years)', 'Cystatin C level', 'Urinary sediment microscopy results', 
        'C-reactive protein (CRP) level', 'Interleukin-6 (IL-6) level'
    ],
    'liver': [
        'Age of the patient', 'Gender of the patient', 'Total Bilirubin', 
        'Direct Bilirubin', 'Alkphos Alkaline Phosphotase', 'Sgpt Alamine Aminotransferase', 
        'Sgot Aspartate Aminotransferase', 'Total Protiens', 'ALB Albumin', 
        'A/G Ratio Albumin and Globulin Ratio'
    ],
    'breast_cancer': [
        'mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 
        'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 
        'mean fractal dimension', 'radius error', 'texture error', 'perimeter error', 
        'area error', 'smoothness error', 'compactness error', 'concavity error', 
        'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius', 
        'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 
        'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 
        'worst fractal dimension'
    ]
}
