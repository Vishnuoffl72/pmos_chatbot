# PMOS Health Assistant & Risk Prediction System

A college project for the **Statistics Department** studying the **Reproductive and Metabolic Impacts of PMOS (Polyendocrine Metabolic Ovarian Syndrome / PCOS) in Adult Women (Ages 17–40)**.

This project consists of two core features:
1. **Data-Driven Chat Assistant**: Answers user inquiries utilizing statistical distributions and clinical correlations derived directly from the survey research dataset.
2. **AI-Based PMOS Risk Prediction System**: Evaluates patient clinical, hormonal, and lifestyle parameters to predict the risk of PMOS using a Machine Learning classifier (Random Forest) trained on the research survey data.

---

## 🏗️ Architecture & Technology Stack

```
PMOS Proj/
├── backend/                  # FastAPI + Scikit-Learn Python Backend
│   ├── data/                 # Cleaned Research Survey Data (.xlsx)
│   ├── model/                # ML Training Scripts & Saved Model (.pkl)
│   ├── routes/               # API Endpoints (/api/chat, /api/predict)
│   ├── services/             # Prediction Engine & Chat Knowledge Base
│   └── main.py               # Application Entrypoint with CORS
│
└── frontend/                 # Angular 19 Single Page Application
    └── pmos-app/
        └── src/app/
            ├── components/   # Navbar, Home, Chat, Predict
            ├── services/     # Angular ApiService (HttpClient)
            └── app.routes.ts # Frontend Routing
```

- **Frontend**: Angular 19 (Standalone Components, modern CSS with Teal Medical theme)
- **Backend**: FastAPI (Python 3.10+) with Uvicorn
- **Machine Learning**: Scikit-Learn Random Forest Classifier (saved with Joblib)
- **Data Processing**: Pandas, OpenPyXL, NumPy

---

## ⚡ Quick Start: How to Run the Application

To run the full application, open **two terminal windows** (PowerShell or Command Prompt):

### Terminal 1: Backend (FastAPI)
```powershell
# 1. Navigate to the backend folder
cd "E:\web dev\PMOS Proj\backend"

# 2. Install Python requirements (if not done yet)
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

# 3. Start the FastAPI server
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
> The backend will be available at: **http://127.0.0.1:8000**  
> Swagger Documentation: **http://127.0.0.1:8000/docs**

---

### Terminal 2: Frontend (Angular)
```powershell
# 1. Navigate to the frontend app folder
cd "E:\web dev\PMOS Proj\frontend\pmos-app"

# 2. Install npm packages (if not done yet)
npm install

# 3. Start the Angular dev server
npm start
```
> The web application will launch at: **http://localhost:4200**

---

## 🧪 Verified Test Results

All backend endpoints and frontend build processes have been verified:

| Component | Target | Status | Verification Detail |
|---|---|---|---|
| **FastAPI Root** | `GET /` | `200 OK` | Confirms server health & CORS configuration |
| **Chat Service** | `POST /api/chat` | `200 OK` | Tested with questions on symptoms, diet, sleep, workouts, family history, and treatments |
| **Risk Prediction** | `POST /api/predict` | `200 OK` | Evaluated with test inputs; outputs risk level, percentage, top factors, and recommendations |
| **Angular Frontend** | `ng build` | `PASS` | Compiled production bundle (0 errors, 0 warnings) |
| **Angular Dev Server**| `http://localhost:4200` | `200 OK` | Successfully serves Single Page Application |

---

## 📊 Dataset & Model Details
- **Dataset**: `backend/data/pmos_data.xlsx` containing 387 survey responses.
- **Model**: Random Forest Classifier evaluating 19 parameters:
  - Age, Weight, Height, BMI
  - Age of first menstrual cycle, Menstrual regularity
  - Family history of PMOS / PCOS
  - Junk food frequency, Broiler chicken consumption, Meal timing pattern
  - Exercise frequency, Mood/depression severity
  - Physical & hormonal symptoms (Acne, Hirsutism, Hair loss)
  - Sleep duration & Sleep disorder indices
  - Pregnancy history & Number of children

