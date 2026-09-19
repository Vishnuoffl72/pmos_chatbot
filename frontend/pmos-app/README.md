# PMOS Health Assistant — Frontend (Angular)

Modern, responsive web application for the **PMOS (Polyendocrine Metabolic Ovarian Syndrome)** college project.

Built using **Angular 19** standalone components with a clean medical/health theme (Teal palette).

---

## 🛠️ Prerequisites
- **Node.js**: v18+ (tested on Node v24)
- **npm**: v9+ (tested on npm 11)

---

## 🚀 Quick Start Instructions

### 1. Open Terminal and Navigate to Frontend Directory
```powershell
cd "E:\web dev\PMOS Proj\frontend\pmos-app"
```

### 2. Install Dependencies (if not already installed)
```powershell
npm install
```

### 3. Start the Angular Development Server
```powershell
npm start
```
or:
```powershell
npx ng serve --port 4200
```

### 4. Open in Browser
Visit **[http://localhost:4200](http://localhost:4200)** in your browser.

> **Note**: Make sure your FastAPI backend is running on `http://localhost:8000` so chat queries and risk assessments can communicate with the server.

---

## 💻 Application Features & Pages

### 1. Home (`/`)
- Hero banner introducing the PMOS research study.
- Quick navigation cards to **Chatbot** and **Risk Assessment**.
- PMOS awareness statistics and medical overview.

### 2. Chatbot (`/chat`)
- Interactive health assistant conversational interface.
- Instant topic suggestions (Common symptoms, Diet, Exercise, Sleep, Treatment).
- Typing indicator and auto-scrolling conversation history.
- Communicates directly with the backend FastAPI `/api/chat` endpoint.

### 3. Risk Predictor (`/predict`)
- Multi-section health intake form:
  - **Section 1**: Basic Demographics (Age, Weight, Height, Location, Marital Status)
  - **Section 2**: Menstrual & Reproductive Health (Cycle Regularity, Age at First Period, Pregnancy, Children)
  - **Section 3**: Family History of PMOS / PCOS
  - **Section 4**: Dietary & Lifestyle Habits (Junk Food, Chicken Consumption, Eating Pattern, Exercise)
  - **Section 5**: Mental & Hormonal Symptoms (Mood/Depression, Acne, Hirsutism, Hair Loss)
  - **Section 6**: Sleep Patterns & Sleep Quality (Hours, Insomnia, Snoring, Fatigue)
- Dynamic Risk Result Panel:
  - Color-coded Circular Risk Gauge (Low = Green, Moderate = Amber, High = Red)
  - Precise Risk Percentage
  - Top contributing factors identified by the Random Forest model
  - Personalized health & lifestyle recommendations
  - "Try Again" option to test new values

---

## 📦 Production Build
To create a production-optimized build:
```powershell
npm run build
```
The compiled files will be located in the `dist/pmos-app` folder.
