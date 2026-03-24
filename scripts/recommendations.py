# ============================================
# LIVER DISEASE RECOMMENDATIONS ENGINE
# ============================================
# Provides personalized diet, precautions, and lifestyle recommendations

RECOMMENDATIONS = {
    "Grade_1": {
        "title": "Mild Hepatic Steatosis (Grade 1)",
        "description": "Early stage fatty liver disease - reversible with lifestyle changes",
        
        # Recovery Steps (combined what to do and what not to do)
        "recovery_steps": [
            "Follow a low-fat, low-sugar diet to reduce liver fat accumulation",
            "Exercise for at least 30 minutes daily to maintain healthy weight",
            "Lose 5-10% of your body weight gradually through diet and exercise",
            "Include plenty of vegetables and fruits in your daily meals",
            "Drink green tea regularly as it helps reduce fat accumulation in the liver",
            "Schedule regular liver function tests every 3 months for monitoring",
            "Stay hydrated by drinking 8-10 glasses of water daily",
            "Consume foods rich in vitamin E such as nuts and spinach",
            "Add omega-3 fatty acids to your diet from sources like salmon and flaxseed",
            "Ensure adequate sleep of 7-8 hours nightly for liver regeneration",
            "Avoid alcohol completely to prevent further liver damage",
            "Limit fried and greasy foods that increase liver workload",
            "Avoid sugary drinks and sodas that contribute to fat buildup",
            "Reduce consumption of processed foods and red meat",
            "Avoid fast food and junk food entirely during recovery"
        ],
        
        # Diet recommendations
        "diet": {
            "foods_to_eat": [
                "Leafy green vegetables (spinach, kale)",
                "Fruits (apples, berries, oranges)",
                "Whole grains (oats, brown rice)",
                "Lean proteins (chicken, fish, tofu)",
                "Legumes (beans, lentils)",
                "Nuts and seeds",
                "Olive oil",
                "Garlic and onions"
            ],
            "foods_to_avoid": [
                "Alcohol",
                "Fried foods",
                "Sugary foods and drinks",
                "White bread and pasta",
                "Red meat",
                "Full-fat dairy",
                "Canned foods",
                "Condiments with added sugar"
            ],
            "meal_tips": [
                "Eat small, frequent meals throughout the day",
                "Avoid eating within 3 hours of bedtime",
                "Drink water before meals to aid digestion",
                "Include protein in every meal for sustained energy"
            ]
        },
        
        # Follow-up timeline
        "follow_up": "Schedule liver function tests every 3-6 months for proper monitoring",
        "recovery_time": "3-6 months with proper lifestyle changes"
    },
    
    "Grade_2": {
        "title": "Moderate Hepatic Steatosis (Grade 2)",
        "description": "Moderate fatty liver disease - requires immediate lifestyle changes and medical attention",
        
        # Recovery Steps
        "recovery_steps": [
            "Schedule an appointment with your liver specialist for consultation and follow-up care",
            "Follow a strict low-fat, low-carb diet immediately",
            "Exercise 45-60 minutes daily under medical supervision",
            "Lose 10% of your body weight gradually",
            "Monitor blood sugar and cholesterol levels regularly",
            "Eat small, frequent meals throughout the day",
            "Include detoxifying foods such as lemon and ginger in your diet",
            "Take all prescribed medications regularly as directed",
            "Undergo ultrasound examination every 6 months",
            "Consider liver supplements only after consulting your doctor"
        ],
        
        # Diet recommendations
        "diet": {
            "foods_to_eat": [
                "Boiled or grilled chicken (skinless)",
                "Steamed vegetables",
                "Fresh fruits",
                "Brown rice and quinoa",
                "Fresh fish (not fried)",
                "Egg whites",
                "Low-fat yogurt",
                "Cucumber and celery"
            ],
            "foods_to_avoid": [
                "All alcoholic beverages",
                "Fried chicken and fried fish",
                "Pizza and pasta with heavy sauces",
                "Ice cream and frozen desserts",
                "Chocolate and confectionery",
                "Chips, crackers, and packaged snacks",
                "Fruit juices with added sugar",
                "Canned soups and processed foods"
            ],
            "meal_tips": [
                "Prepare meals at home using healthy cooking methods",
                "Use minimal oil - prefer steaming or boiling",
                "Avoid all condiments and bottled sauces",
                "Include plenty of fiber in your diet"
            ]
        },
        
        # Follow-up timeline
        "follow_up": "Schedule regular appointments with your liver specialist for consultation and ongoing care",
        "recovery_time": "6-12 months with strict adherence to lifestyle changes"
    },
    
    "Healthy": {
        "title": "Healthy Liver",
        "description": "Your liver is healthy! Keep it that way with these preventive measures",
        
        # Recovery Steps (preventive measures combined)
        "recovery_steps": [
            "Maintain a healthy weight through regular exercise and balanced nutrition",
            "Exercise regularly for at least 30 minutes, 5 days per week",
            "Eat a balanced diet rich in vegetables, fruits, and whole grains",
            "Drink alcohol in moderation or avoid completely for optimal liver health",
            "Stay hydrated by drinking adequate water throughout the day",
            "Get vaccinated for hepatitis A and B to protect your liver",
            "Practice safe food handling and proper hygiene",
            "Get regular health checkups including liver function tests",
            "Include liver-friendly foods such as leafy greens, garlic, and green tea in your diet",
            "Manage stress levels through meditation, yoga, or relaxation techniques",
            "Avoid consuming excessive alcohol that can damage liver cells",
            "Stay away from illicit drug use and never share needles",
            "Avoid exposure to environmental toxins and harmful chemicals",
            "Do not eat raw or undercooked shellfish",
            "Avoid crash diets and rapid weight loss that strain the liver"
        ],
        
        # Diet recommendations
        "diet": {
            "foods_to_eat": [
                "Leafy green vegetables",
                "Cruciferous vegetables (broccoli, cauliflower)",
                "Berries and citrus fruits",
                "Grapefruit",
                "Garlic",
                "Green tea",
                "Nuts and seeds",
                "Olive oil"
            ],
            "foods_to_avoid": [
                "Excessive alcohol",
                "Fatty and fried foods",
                "Sugary foods and beverages",
                "Processed and packaged foods",
                "Foods high in salt",
                "Raw or undercooked shellfish"
            ],
            "meal_tips": [
                "Eat a varied, balanced diet with plenty of colors",
                "Include fiber-rich foods in every meal",
                "Limit portion sizes to maintain healthy weight",
                "Drink water between meals rather than with meals",
                "Avoid eating heavy meals late at night"
            ]
        },
        
        # Follow-up timeline
        "follow_up": "Schedule annual health checkups with liver function tests for ongoing monitoring",
        "recovery_time": "Maintain healthy habits for life"
    }
}


def get_recommendations(disease_class):
    """
    Get comprehensive recommendations for a given disease class.
    
    Args:
        disease_class: One of "Grade_1", "Grade_2", "Healthy"
    
    Returns:
        Dictionary with all recommendations
    """
    return RECOMMENDATIONS.get(disease_class, RECOMMENDATIONS["Healthy"])


def format_recommendations(disease_class):
    """
    Format recommendations as HTML for display.
    """
    rec = get_recommendations(disease_class)
    
    # Check if recovery_steps exists (for Grade 1, Grade 2, and Healthy)
    if 'recovery_steps' in rec:
        recovery_html = f"""
        <div class="recovery-steps">
            <h3>{"Recovery Steps" if disease_class != "Healthy" else "Preventive Measures"}</h3>
            <ol>
                {"".join([f"<li>{item}</li>" for item in rec['recovery_steps']])}
            </ol>
        </div>
        """
    
    html = f"""
    <div class="recommendations">
        <h2>{rec['title']}</h2>
        <p class="description">{rec['description']}</p>
        
        {recovery_html}
        
        <div class="diet-section">
            <h3>Diet Recommendations</h3>
            
            <div class="diet-columns">
                <div class="diet-column">
                    <h4>Foods to EAT</h4>
                    <ul>
                        {"".join([f"<li>{item}</li>" for item in rec['diet']['foods_to_eat']])}
                    </ul>
                </div>
                
                <div class="diet-column">
                    <h4>Foods to AVOID</h4>
                    <ul>
                        {"".join([f"<li>{item}</li>" for item in rec['diet']['foods_to_avoid']])}
                    </ul>
                </div>
            </div>
            
            <div class="meal-tips">
                <h4>Meal Tips</h4>
                <ul>
                    {"".join([f"<li>{item}</li>" for item in rec['diet']['meal_tips']])}
                </ul>
            </div>
        </div>
        
        <div class="follow-up">
            <h3>Follow-up Recommendation</h3>
            <p>{rec['follow_up']}</p>
            <p><strong>Expected Recovery Time:</strong> {rec['recovery_time']}</p>
        </div>
    </div>
    """
    
    return html

