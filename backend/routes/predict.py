from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.prediction_service import predict

router = APIRouter()

class PredictionInput(BaseModel):
    Age: float
    Weight: float
    Height: float
    age_of_first_period: float
    residential_location: str
    marital_status: str
    menstrual_regularity: str
    family_history: str
    junk_food_freq: str
    chicken_freq: str
    food_pattern: str
    exercise_freq: str
    mood_issues: str
    symptoms: str
    sleep_hours: str
    sleep_issues: str
    pregnancy_status: str
    num_children: float

@router.post("/")
async def get_prediction(input_data: PredictionInput):
    try:
        data_dict = input_data.dict()
        result = predict(data_dict)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
            
        # Add general recommendations based on risk level
        risk_level = result.get("risk_level", "Unknown")
        if risk_level == "Low":
            result["recommendations"] = [
                "Maintain your current healthy lifestyle.",
                "Continue regular physical exercise and balanced diet.",
                "Schedule routine health checkups annually."
            ]
        elif risk_level == "Moderate":
            result["recommendations"] = [
                "Consider reviewing your diet — reduce junk food and processed foods.",
                "Increase physical activity to at least 3-4 times a week.",
                "Monitor your menstrual cycle for irregularities.",
                "Consult a healthcare provider if symptoms worsen."
            ]
        elif risk_level == "High":
            result["recommendations"] = [
                "Consult a gynecologist or endocrinologist for proper diagnosis.",
                "Focus on weight management through diet and regular exercise.",
                "Monitor hormonal symptoms and menstrual irregularities closely.",
                "Manage stress through yoga, meditation, or counseling.",
                "Get blood tests for hormonal levels (testosterone, insulin, thyroid)."
            ]
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
