import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_model():
    print("Loading data...")
    # Get absolute path to the data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'pmos_data.xlsx')
    
    # Load dataset
    df = pd.read_excel(data_path)
    
    # Column indices based on requirements
    # 2: Age, 3: Weight, 4: Height, 6: Residential location, 7: Marital Status
    # 8: Age of first menstrual cycle, 9: Menstrual cycle regularity, 10: Diagnosed with PMOS
    # 11: Family history, 13: Junk food freq, 14: Chicken consumption, 15: Food pattern
    # 16: Exercise frequency, 17: Mood issues, 18: Hormonal symptoms, 19: Sleep hours
    # 20: Sleep issues, 21: Pregnancy status, 22: Number of children
    
    # Let's map column indices to readable names to make it easier
    col_names = {
        df.columns[2]: 'Age',
        df.columns[3]: 'Weight',
        df.columns[4]: 'Height',
        df.columns[6]: 'residential_location',
        df.columns[7]: 'marital_status',
        df.columns[8]: 'age_of_first_period',
        df.columns[9]: 'menstrual_regularity',
        df.columns[10]: 'target_pmos',
        df.columns[11]: 'family_history',
        df.columns[13]: 'junk_food_freq',
        df.columns[14]: 'chicken_freq',
        df.columns[15]: 'food_pattern',
        df.columns[16]: 'exercise_freq',
        df.columns[17]: 'mood_issues',
        df.columns[18]: 'symptoms',
        df.columns[19]: 'sleep_hours',
        df.columns[20]: 'sleep_issues',
        df.columns[21]: 'pregnancy_status',
        df.columns[22]: 'num_children'
    }
    
    df = df.rename(columns=col_names)
    
    # Filter for necessary columns
    features = ['Age', 'Weight', 'Height', 'residential_location', 'marital_status',
                'age_of_first_period', 'menstrual_regularity', 'target_pmos',
                'family_history', 'junk_food_freq', 'chicken_freq', 'food_pattern',
                'exercise_freq', 'mood_issues', 'symptoms', 'sleep_hours', 'sleep_issues',
                'pregnancy_status', 'num_children']
    
    df = df[features].copy()
    
    # Drop rows where target is 'Unsure' and map Yes=1, No=0
    df = df[df['target_pmos'].str.lower() != 'unsure']
    df['target_pmos'] = df['target_pmos'].apply(lambda x: 1 if str(x).lower() == 'yes' else 0)
    
    # Handle missing values by forward fill or basic imputation
    df = df.fillna(method='ffill').fillna(method='bfill')
    
    # Feature Engineering
    # 1. Calculate BMI
    # Handle possible non-numeric values in Weight/Height gracefully
    df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce').fillna(df['Weight'].mode()[0])
    df['Height'] = pd.to_numeric(df['Height'], errors='coerce').fillna(df['Height'].mode()[0])
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(df['Age'].mode()[0])
    df['age_of_first_period'] = pd.to_numeric(df['age_of_first_period'], errors='coerce').fillna(df['age_of_first_period'].mode()[0])
    df['num_children'] = pd.to_numeric(df['num_children'], errors='coerce').fillna(0)
    
    df['BMI'] = df['Weight'] / ((df['Height'] / 100) ** 2)
    
    # 2. Sleep issues count
    df['sleep_issues_count'] = df['sleep_issues'].apply(lambda x: len(str(x).split(',')) if pd.notnull(x) and str(x).strip() != 'None' else 0)
    
    # Final feature list
    final_features = ['Age', 'Weight', 'Height', 'BMI', 'age_of_first_period', 
                      'residential_location', 'marital_status', 'menstrual_regularity', 
                      'family_history', 'junk_food_freq', 'chicken_freq', 'food_pattern', 
                      'exercise_freq', 'mood_issues', 'symptoms', 'sleep_hours', 
                      'sleep_issues_count', 'pregnancy_status', 'num_children']
    
    categorical_cols = ['residential_location', 'marital_status', 'menstrual_regularity', 
                        'family_history', 'junk_food_freq', 'chicken_freq', 'food_pattern', 
                        'exercise_freq', 'mood_issues', 'symptoms', 'sleep_hours', 
                        'pregnancy_status']
    
    # Ensure categorical columns are strings
    for col in categorical_cols:
        df[col] = df[col].astype(str)
        
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
        
    X = df[final_features]
    y = df['target_pmos']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    save_path = os.path.join(base_dir, 'model', 'pmos_model.pkl')
    print(f"Saving model to {save_path}...")
    joblib.dump({
        'model': model,
        'encoders': encoders,
        'feature_names': final_features
    }, save_path)
    print("Model saved successfully.")

if __name__ == "__main__":
    train_model()
