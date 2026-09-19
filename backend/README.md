# PMOS Health Assistant — Backend (FastAPI + ML)

FastAPI-powered backend and machine learning service for the **PMOS (Polyendocrine Metabolic Ovarian Syndrome)** college project.

---

## 🛠️ Tech Stack & Requirements
- **Python**: 3.10+
- **Framework**: FastAPI + Uvicorn
- **Machine Learning**: Scikit-Learn (Random Forest Classifier), Pandas, NumPy, OpenPyXL
- **Data Source**: `backend/data/pmos_data.xlsx` (survey dataset of 387 respondents)

---

## 🚀 Quick Start Instructions

### 1. Open Terminal and Navigate to Backend
```powershell
cd "E:\web dev\PMOS Proj\backend"
```

### 2. Install Dependencies
Run pip install (using trusted-host flags in case of SSL/proxy certificates on campus/work networks):
```powershell
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

### 3. (Optional) Re-train the Machine Learning Model
The pre-trained model is already saved at `model/pmos_model.pkl`. If you update the dataset or want to retrain:
```powershell
python model/train_model.py
```
This trains a Random Forest Classifier using 19 engineered clinical and lifestyle features and outputs accuracy metrics.

### 4. Start the Backend Server
```powershell
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
or simply:
```powershell
uvicorn main:app --reload --port 8000
```

- Server will start at: **http://127.0.0.1:8000**
- Interactive Swagger API Documentation: **http://127.0.0.1:8000/docs**

---

## 📡 API Endpoints

### 1. Health / Root
- **`GET /`**
- Returns a welcome confirmation message.

### 2. Research Data Chatbot
- **`POST /api/chat`**
- **Request Body**:
  ```json
  {
    "message": "What are common symptoms?"
  }
  ```
- **Response**:
  ```json
  {
    "response": "Common symptoms of PMOS include irregular periods, weight gain, acne..."
  }
  ```
- **Features**: Automatically matches user inquiries against statistical aggregations of the PMOS survey data (symptoms, diet, exercise, sleep, family history, BMI, age distribution, and lifestyle recommendations).

### 3. Risk Prediction
- **`POST /api/predict`**
- **Request Body**:
  ```json
  {
    "Age": 24,
    "Weight": 70,
    "Height": 160,
    "age_of_first_period": 13,
    "residential_location": "Urban (City / Tier-1 or Tier-2 city)",
    "marital_status": "Unmarried",
    "menstrual_regularity": "Irregular",
    "family_history": "Yes",
    "junk_food_freq": "Daily",
    "chicken_freq": "1–2 times a week",
    "food_pattern": "My meal timings vary heavily, and I frequently skip main meals.",
    "exercise_freq": "No Regular Exercise",
    "mood_issues": "Frequently (multiple times a week)",
    "symptoms": "Severe or persistent acne (especially along the jawline or back)",
    "sleep_hours": "5 to 6 hours",
    "sleep_issues": "Difficulty falling asleep, Waking up frequently during the night",
    "pregnancy_status": "No",
    "num_children": 0
  }
  ```
- **Response**:
  ```json
  {
    "risk_score": 0.48,
    "risk_level": "Moderate",
    "factors": [
      "Body Mass Index (BMI)",
      "Menstrual Cycle Regularity",
      "Weight",
      "Height",
      "Age"
    ],
    "recommendations": [
      "Consider reviewing your diet — reduce junk food and processed foods.",
      "Increase physical activity to at least 3-4 times a week.",
      "Monitor your menstrual cycle for irregularities.",
      "Consult a healthcare provider if symptoms worsen."
    ]
  }
  ```

