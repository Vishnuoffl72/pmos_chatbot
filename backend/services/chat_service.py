import pandas as pd
import numpy as np
import os
import re

# Global variable to hold computed statistics
STATS = {}

def init_chat_service():
    global STATS
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, 'data', 'pmos_data.xlsx')
        
        if not os.path.exists(data_path):
            print("Dataset not found for chat statistics.")
            return

        df = pd.read_excel(data_path)
        
        # Target variable
        target_col = df.columns[10]
        pmos_yes = df[df[target_col].astype(str).str.lower() == 'yes']
        pmos_no = df[df[target_col].astype(str).str.lower() == 'no']
        total_valid = len(pmos_yes) + len(pmos_no)
        
        STATS['total_respondents'] = len(df)
        STATS['total_valid'] = total_valid
        STATS['pmos_count'] = len(pmos_yes)
        STATS['prevalence'] = round((len(pmos_yes) / total_valid) * 100, 2) if total_valid > 0 else 0
        
        # Age group stats
        age_col = df.columns[2]
        df['Age_Num'] = pd.to_numeric(df[age_col], errors='coerce')
        pmos_yes_df = pmos_yes.copy()
        pmos_yes_df['Age_Num'] = pd.to_numeric(pmos_yes_df[age_col], errors='coerce')
        
        STATS['age_groups'] = {}
        bins = [17, 21, 26, 31, 36, 41]
        labels = ['17-20', '21-25', '26-30', '31-35', '36-40']
        if not pmos_yes_df['Age_Num'].isna().all():
            pmos_yes_df['age_group'] = pd.cut(pmos_yes_df['Age_Num'], bins=bins, labels=labels, right=False)
            age_counts = pmos_yes_df['age_group'].value_counts()
            for label in labels:
                STATS['age_groups'][label] = int(age_counts.get(label, 0))
        
        # BMI stats
        df['Weight_Num'] = pd.to_numeric(df[df.columns[3]], errors='coerce')
        df['Height_Num'] = pd.to_numeric(df[df.columns[4]], errors='coerce')
        df['BMI'] = df['Weight_Num'] / ((df['Height_Num'] / 100) ** 2)
        
        pmos_bmi = df[df[target_col].astype(str).str.lower() == 'yes']['BMI'].dropna()
        STATS['avg_bmi_pmos'] = round(pmos_bmi.mean(), 1) if len(pmos_bmi) > 0 else 'N/A'
        non_pmos_bmi = df[df[target_col].astype(str).str.lower() == 'no']['BMI'].dropna()
        STATS['avg_bmi_non_pmos'] = round(non_pmos_bmi.mean(), 1) if len(non_pmos_bmi) > 0 else 'N/A'
        
        # Symptom distribution among PMOS women
        symptom_col = df.columns[18]
        if len(pmos_yes) > 0:
            symptom_counts = pmos_yes[symptom_col].value_counts()
            STATS['symptom_distribution'] = {str(k): int(v) for k, v in symptom_counts.items()}
            STATS['top_symptom'] = str(symptom_counts.index[0]) if len(symptom_counts) > 0 else "N/A"
        
        # Family history correlation
        fam_col = df.columns[11]
        if len(pmos_yes) > 0:
            fam_yes = len(pmos_yes[pmos_yes[fam_col].astype(str).str.lower() == 'yes'])
            STATS['family_history_pct'] = round((fam_yes / len(pmos_yes)) * 100, 2)
        else:
            STATS['family_history_pct'] = 0
        
        # Menstrual irregularity
        period_col = df.columns[9]
        if len(pmos_yes) > 0:
            irreg = len(pmos_yes[pmos_yes[period_col].astype(str).str.lower() == 'irregular'])
            STATS['irregular_pct'] = round((irreg / len(pmos_yes)) * 100, 2)
        else:
            STATS['irregular_pct'] = 0
        
        # Junk food stats
        junk_col = df.columns[13]
        if len(pmos_yes) > 0:
            junk_counts = pmos_yes[junk_col].value_counts()
            STATS['junk_food_pmos'] = {str(k): int(v) for k, v in junk_counts.items()}
        
        # Exercise stats
        exercise_col = df.columns[16]
        if len(pmos_yes) > 0:
            ex_counts = pmos_yes[exercise_col].value_counts()
            STATS['exercise_pmos'] = {str(k): int(v) for k, v in ex_counts.items()}
            no_exercise = len(pmos_yes[pmos_yes[exercise_col].astype(str).str.contains('No Regular', case=False, na=False)])
            STATS['no_exercise_pct'] = round((no_exercise / len(pmos_yes)) * 100, 2)
        
        # Sleep stats
        sleep_col = df.columns[19]
        if len(pmos_yes) > 0:
            sleep_counts = pmos_yes[sleep_col].value_counts()
            STATS['sleep_pmos'] = {str(k): int(v) for k, v in sleep_counts.items()}
        
        # Mood stats
        mood_col = df.columns[17]
        if len(pmos_yes) > 0:
            mood_counts = pmos_yes[mood_col].value_counts()
            STATS['mood_pmos'] = {str(k): int(v) for k, v in mood_counts.items()}
        
        print("Chat service statistics initialized successfully.")
        print(f"  Total respondents: {STATS['total_respondents']}")
        print(f"  PMOS prevalence: {STATS['prevalence']}%")
    except Exception as e:
        print(f"Error initializing chat service: {str(e)}")
        import traceback
        traceback.print_exc()

def get_response(message: str) -> str:
    msg = message.lower().strip()
    
    # Check for specific topics FIRST, then fall back to general PMOS definition
    
    # 1. Symptoms
    if re.search(r'\b(symptoms?|signs?|indications?)\b', msg):
        dist = STATS.get('symptom_distribution', {})
        dist_str = "\n".join([f"  • {k}: {v} cases" for k, v in dist.items()])
        return (f"Common symptoms of PMOS include irregular periods, weight gain, acne, "
                f"hirsutism (excess facial/body hair growth), and hair thinning.\n\n"
                f"From our dataset of {STATS.get('pmos_count', 0)} diagnosed women, "
                f"the symptom distribution is:\n{dist_str}\n\n"
                f"If you experience multiple symptoms, consider consulting a healthcare provider.")
    
    # 2. Diet / Food
    if re.search(r'\b(diets?|foods?|junk|chicken|eat|eating|nutrition|meals?)\b', msg):
        junk = STATS.get('junk_food_pmos', {})
        junk_str = ", ".join([f"{k}: {v}" for k, v in junk.items()])
        return (f"Diet plays a significant role in PMOS. High intake of processed foods, "
                f"sugary items, and junk food can worsen insulin resistance.\n\n"
                f"Among women diagnosed with PMOS in our data, junk food consumption was:\n"
                f"  {junk_str}\n\n"
                f"Recommendations: Focus on whole grains, lean proteins, vegetables, and healthy fats. "
                f"Limit processed foods, sugary drinks, and excessive dairy.")
    
    # 3. Exercise
    if re.search(r'\b(exercises?|exercising|workouts?|gym|yoga|walk|walking|physical|fitness)\b', msg):
        no_ex = STATS.get('no_exercise_pct', 0)
        ex_dist = STATS.get('exercise_pmos', {})
        ex_str = ", ".join([f"{k}: {v}" for k, v in ex_dist.items()])
        return (f"Regular physical activity is crucial for managing PMOS — it improves insulin "
                f"sensitivity, aids weight management, and balances hormones.\n\n"
                f"In our dataset, {no_ex}% of PMOS-diagnosed women reported no regular exercise.\n"
                f"Exercise breakdown: {ex_str}\n\n"
                f"Aim for at least 150 minutes of moderate exercise per week (brisk walking, yoga, swimming).")
    
    # 4. Sleep
    if re.search(r'\b(sleep|sleeping|insomnia|rest|fatigue|tired|fatigued)\b', msg):
        sleep = STATS.get('sleep_pmos', {})
        sleep_str = ", ".join([f"{k}: {v}" for k, v in sleep.items()])
        return (f"Sleep quality significantly affects PMOS. Poor sleep disrupts cortisol and insulin, "
                f"worsening hormonal imbalance.\n\n"
                f"Sleep hours among PMOS-diagnosed women:\n  {sleep_str}\n\n"
                f"Tips: Aim for 7-8 hours of quality sleep. Maintain a consistent schedule, "
                f"avoid screens before bed, and create a dark, cool sleep environment.")
    
    # 5. Age
    if re.search(r'\bage\b', msg) and not re.search(r'\b(menstrual|period|cycle)\b', msg):
        age_groups = STATS.get('age_groups', {})
        age_str = ", ".join([f"{k}: {v} cases" for k, v in age_groups.items()])
        return (f"PMOS can affect women across all reproductive ages (17-40).\n\n"
                f"From our dataset, PMOS cases by age group:\n  {age_str}\n\n"
                f"Early detection and management are key regardless of age.")
    
    # 6. Weight / BMI
    if re.search(r'\b(weights?|bmi|obese|obesity|overweight|fat|thin|underweight)\b', msg):
        avg_pmos = STATS.get('avg_bmi_pmos', 'N/A')
        avg_non = STATS.get('avg_bmi_non_pmos', 'N/A')
        return (f"Weight and BMI are closely linked to PMOS. Higher BMI worsens insulin resistance, "
                f"which exacerbates hormonal imbalance.\n\n"
                f"From our data:\n"
                f"  • Average BMI of PMOS-diagnosed women: {avg_pmos}\n"
                f"  • Average BMI of non-PMOS women: {avg_non}\n\n"
                f"Even a 5-10% weight loss can significantly improve symptoms and hormonal balance.")
    
    # 7. Menstrual / Periods
    if re.search(r'\b(menstrual|periods?|cycles?|irregular|irregularity|regular)\b', msg):
        irreg = STATS.get('irregular_pct', 0)
        return (f"Menstrual irregularity is one of the primary indicators of PMOS.\n\n"
                f"In our dataset, {irreg}% of women diagnosed with PMOS reported irregular periods.\n\n"
                f"Irregular periods in PMOS are caused by anovulation (failure to ovulate regularly). "
                f"If your periods are consistently irregular, consider getting evaluated by a gynecologist.")
    
    # 8. Family History / Genetics
    if re.search(r'\b(family|families|genetic|genetics|hereditary|mother|mothers|sister|sisters|grandmother|grandmothers)\b', msg):
        fam = STATS.get('family_history_pct', 0)
        return (f"Genetics play a significant role in PMOS. It tends to run in families.\n\n"
                f"In our dataset, {fam}% of women diagnosed with PMOS also had a family member "
                f"(mother, sister, or grandmother) with the condition.\n\n"
                f"If PMOS runs in your family, proactive screening and lifestyle management are recommended.")
    
    # 9. Mood / Mental Health
    if re.search(r'\b(mood|moods|depress|depression|depressive|stress|anxiety|mental|emotions?|emotional)\b', msg):
        mood = STATS.get('mood_pmos', {})
        mood_str = ", ".join([f"{k}: {v}" for k, v in mood.items()])
        return (f"PMOS and mental health are closely connected. Hormonal imbalances can cause "
                f"mood swings, anxiety, and depression.\n\n"
                f"Mood patterns among PMOS-diagnosed women in our data:\n  {mood_str}\n\n"
                f"Tips: Practice stress management (yoga, meditation), seek professional support if needed, "
                f"and regular exercise can significantly improve mood.")
    
    # 10. Pregnancy / Fertility
    if re.search(r'\b(pregnant|pregnancy|pregnancies|fertility|fertile|conceive|baby|babies|child|children)\b', msg):
        return (f"PMOS can affect fertility due to irregular ovulation, making it harder to conceive.\n\n"
                f"However, PMOS does NOT mean infertility. With proper medical guidance "
                f"(medications like Clomiphene, lifestyle changes, or assisted reproduction), "
                f"many women with PMOS have healthy pregnancies.\n\n"
                f"If you're planning a pregnancy and have PMOS, consult a reproductive endocrinologist.")
    
    # 11. Risk Factors / Prevention
    if re.search(r'\b(risks?|prevent|prevention|avoid|causes?|factors?|chance|chances)\b', msg):
        return (f"Key risk factors for PMOS include:\n"
                f"  • Family history of PMOS/PCOS\n"
                f"  • High BMI / Obesity\n"
                f"  • Sedentary lifestyle\n"
                f"  • Poor diet (high sugar, processed foods)\n"
                f"  • Chronic stress and poor sleep\n\n"
                f"Prevention tips: Maintain a healthy weight, eat balanced meals, exercise regularly "
                f"(150+ min/week), manage stress, and get 7-8 hours of sleep.")
    
    # 12. Treatment
    if re.search(r'\b(treat|treatment|treatments|cure|medicine|medicines|medication|medications|therapy|manage|management)\b', msg):
        return (f"PMOS management typically involves:\n\n"
                f"  • Lifestyle changes: Diet, exercise, weight management\n"
                f"  • Medications: Birth control pills (to regulate periods), Metformin (for insulin resistance), "
                f"anti-androgens (for excess hair/acne)\n"
                f"  • Supplements: Inositol, Vitamin D, Omega-3\n"
                f"  • Mental health support: Counseling, stress management\n\n"
                f"There is no 'cure' for PMOS, but symptoms can be effectively managed. "
                f"Consult a healthcare provider for a personalized treatment plan.")
    
    # 13. General PMOS definition (checked LAST so specific topics take priority)
    if re.search(r'\b(pmos|pcos|pcod|what is|tell me about|explain)\b', msg):
        prevalence = STATS.get('prevalence', 'a significant percentage')
        return (f"PMOS (Polyendocrine Metabolic Ovarian Syndrome), previously known as PCOS, "
                f"is a hormonal disorder affecting women of reproductive age (17-40). "
                f"It's characterized by:\n\n"
                f"  • Hormonal imbalances (excess androgens)\n"
                f"  • Irregular or absent menstrual periods\n"
                f"  • Metabolic issues (insulin resistance)\n"
                f"  • Symptoms like acne, hair growth, weight gain\n\n"
                f"Based on our dataset of {STATS.get('total_valid', 0)} respondents, "
                f"{prevalence}% were diagnosed with PMOS.\n\n"
                f"You can ask me about specific topics like symptoms, diet, exercise, sleep, "
                f"family history, or risk factors!")
    
    # 14. Greetings
    if re.search(r'\b(hi|hello|hey|greetings|good morning|good evening)\b', msg):
        return (f"Hello! 👋 I'm your PMOS Health Assistant. I can answer questions about "
                f"Polyendocrine Metabolic Ovarian Syndrome based on our research data of "
                f"{STATS.get('total_respondents', 0)} women.\n\n"
                f"Try asking about:\n"
                f"  • What is PMOS?\n"
                f"  • Common symptoms\n"
                f"  • Diet and PMOS\n"
                f"  • Exercise recommendations\n"
                f"  • Sleep and PMOS\n"
                f"  • Risk factors\n"
                f"  • Family history\n"
                f"  • Treatment options")
    
    # 15. Thanks
    if re.search(r'\b(thank|thanks|thx)\b', msg):
        return "You're welcome! Feel free to ask any other questions about PMOS. I'm here to help! 😊"
    
    # Default fallback
    return (f"I'm your PMOS Health Assistant! I can help you with information about "
            f"Polyendocrine Metabolic Ovarian Syndrome.\n\n"
            f"Try asking about:\n"
            f"  • What is PMOS?\n"
            f"  • Symptoms of PMOS\n"
            f"  • Diet and nutrition\n"
            f"  • Exercise and fitness\n"
            f"  • Sleep and PMOS\n"
            f"  • Weight and BMI\n"
            f"  • Menstrual irregularity\n"
            f"  • Family history\n"
            f"  • Risk factors\n"
            f"  • Treatment options\n"
            f"  • Pregnancy and fertility\n\n"
            f"How can I help you today?")
