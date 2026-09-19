import os
import joblib
import pandas as pd
import numpy as np

# Global variables to hold the loaded model and encoders
MODEL_DATA = None

def load_model():
    global MODEL_DATA
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'model', 'pmos_model.pkl')
    if os.path.exists(model_path):
        MODEL_DATA = joblib.load(model_path)
        print("Model loaded successfully.")
    else:
        print("Model file not found. Please train the model first.")

def predict(input_data: dict):
    if MODEL_DATA is None:
        return {"error": "Model not loaded. Please train the model."}
    
    model = MODEL_DATA['model']
    encoders = MODEL_DATA['encoders']
    feature_names = MODEL_DATA['feature_names']
    
    # Process input data
    processed_data = {}
    
    # 1. Direct numeric mappings
    processed_data['Age'] = float(input_data.get('Age', 25))
    processed_data['Weight'] = float(input_data.get('Weight', 60))
    processed_data['Height'] = float(input_data.get('Height', 160))
    processed_data['age_of_first_period'] = float(input_data.get('age_of_first_period', 13))
    processed_data['num_children'] = float(input_data.get('num_children', 0))
    
    # 2. Compute BMI
    processed_data['BMI'] = processed_data['Weight'] / ((processed_data['Height'] / 100) ** 2)
    
    # 3. Compute sleep issues count
    sleep_issues_str = str(input_data.get('sleep_issues', ''))
    processed_data['sleep_issues_count'] = len(sleep_issues_str.split(',')) if sleep_issues_str and sleep_issues_str.strip() != 'None' else 0
    
    # 4. Handle categorical features
    categorical_features = ['residential_location', 'marital_status', 'menstrual_regularity', 
                            'family_history', 'junk_food_freq', 'chicken_freq', 'food_pattern', 
                            'exercise_freq', 'mood_issues', 'symptoms', 'sleep_hours', 'pregnancy_status']
    
    for col in categorical_features:
        val = str(input_data.get(col, 'Unknown'))
        if col in encoders:
            # Handle unseen labels gracefully by assigning an existing class or -1
            try:
                # Get the class mapping
                classes = encoders[col].classes_
                if val in classes:
                    encoded_val = encoders[col].transform([val])[0]
                else:
                    # Fallback to the first class if unknown
                    encoded_val = 0
            except Exception:
                encoded_val = 0
            processed_data[col] = encoded_val
    
    # Create DataFrame for prediction matching the exact feature names
    df = pd.DataFrame([processed_data])[feature_names]
    
    # Get probabilities for Risk Score
    probabilities = model.predict_proba(df)[0]
    risk_score = probabilities[1]  # Probability of class 1 (Yes)
    
    # Determine risk level
    if risk_score < 0.3:
        risk_level = "Low"
    elif risk_score <= 0.6:
        risk_level = "Moderate"
    else:
        risk_level = "High"
        
    # Get contributing factors
    # Multiply feature importances by the current values (normalized) or just show top importances
    importances = model.feature_importances_
    
    # For a simple approach, we can map feature importances and sort them to show top factors
    factors_with_importance = list(zip(feature_names, importances))
    factors_with_importance.sort(key=lambda x: x[1], reverse=True)
    
    # Human-readable feature name mapping
    feature_labels = {
        'Age': 'Age',
        'Weight': 'Weight',
        'Height': 'Height',
        'BMI': 'Body Mass Index (BMI)',
        'age_of_first_period': 'Age of First Menstrual Cycle',
        'residential_location': 'Residential Location',
        'marital_status': 'Marital Status',
        'menstrual_regularity': 'Menstrual Cycle Regularity',
        'family_history': 'Family History of PMOS',
        'junk_food_freq': 'Junk Food Consumption',
        'chicken_freq': 'Chicken Consumption',
        'food_pattern': 'Eating Pattern',
        'exercise_freq': 'Exercise Frequency',
        'mood_issues': 'Mood / Mental Health',
        'symptoms': 'Hormonal Symptoms',
        'sleep_hours': 'Sleep Duration',
        'sleep_issues_count': 'Number of Sleep Issues',
        'pregnancy_status': 'Pregnancy Status',
        'num_children': 'Number of Children'
    }
    
    # Select top 5 factors that contributed to the model
    top_factors = [feature_labels.get(f[0], f[0]) for f in factors_with_importance[:5]]
    
    return {
        "risk_score": float(risk_score),
        "risk_level": risk_level,
        "factors": top_factors
    }
