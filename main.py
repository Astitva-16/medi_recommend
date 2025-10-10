from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import joblib
import os
import re


# Resolve paths relative to this file so the app works no matter the CWD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# flask app (use absolute folders for templates/static)
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

# Import the prediction function from your new model
def preprocess_text(text):
    """Cleans and standardizes text for prediction."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def predict_disease_from_symptoms(symptoms_text, model_pipeline):
    """
    Predicts the disease from a string of symptoms.
    
    Args:
        symptoms_text (str): A string containing symptoms.
        model_pipeline (dict): A dictionary containing the loaded model and vectorizer.
        
    Returns:
        str: The predicted disease name.
    """
    # Clean the input text
    cleaned_symptoms = preprocess_text(symptoms_text)
    
    # Vectorize the input using the loaded vectorizer
    vectorizer = model_pipeline['vectorizer']
    symptoms_tfidf = vectorizer.transform([cleaned_symptoms])
    
    # Predict using the loaded model
    model = model_pipeline['model']
    predicted_disease = model.predict(symptoms_tfidf)
    
    return predicted_disease[0].title()

# load databasedataset===================================
sym_des = pd.read_csv(os.path.join(BASE_DIR, "symtoms_df.csv"))
precautions = pd.read_csv(os.path.join(BASE_DIR, "precautions_df.csv"))
workout = pd.read_csv(os.path.join(BASE_DIR, "workout_df.csv"))
description = pd.read_csv(os.path.join(BASE_DIR, "description.csv"))
medications = pd.read_csv(os.path.join(BASE_DIR, 'medications.csv'))
diets = pd.read_csv(os.path.join(BASE_DIR, "diets.csv"))

# Load your new treatment lookup for enhanced recommendations
try:
    treatment_lookup = pd.read_csv(os.path.join(BASE_DIR, "treatment_lookup.csv"))
    print("✅ Enhanced treatment lookup loaded successfully")
except FileNotFoundError:
    treatment_lookup = None
    print("⚠️ Treatment lookup not found, using basic recommendations")

# load new model===========================================
try:
    model_pipeline = joblib.load(os.path.join(BASE_DIR, 'disease_model.joblib'))
    print("✅ New ML model loaded successfully from disease_model.joblib")
except FileNotFoundError:
    print("❌ Error: disease_model.joblib not found. Please run the training script first.")
    model_pipeline = None


#============================================================
# custome and helping functions
#==========================helper funtions================
def helper(dis):
    """Enhanced helper function with better disease matching"""
    # Normalize disease name for better matching
    dis_normalized = dis.lower().strip()
    
    # Try exact match first
    desc_match = description[description['Disease'].str.lower() == dis_normalized]
    if desc_match.empty:
        # Try partial match
        desc_match = description[description['Disease'].str.lower().str.contains(dis_normalized, regex=False, na=False)]
    
    if not desc_match.empty:
        desc = desc_match['Description'].iloc[0]
    else:
        desc = f"Information about {dis} is being updated in our database."
    
    # Similar approach for other data
    def safe_lookup(df, disease_col, disease_name, data_cols):
        """Safely lookup data with fallback"""
        exact_match = df[df[disease_col].str.lower() == disease_name.lower()]
        if exact_match.empty:
            partial_match = df[df[disease_col].str.lower().str.contains(disease_name.lower(), regex=False, na=False)]
            if not partial_match.empty:
                return partial_match[data_cols].iloc[0].dropna().tolist()
            else:
                return ["Consult a healthcare professional for specific guidance."]
        return exact_match[data_cols].iloc[0].dropna().tolist()
    
    # Get precautions
    pre = safe_lookup(precautions, 'Disease', dis, ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4'])
    
    # Get medications
    med = safe_lookup(medications, 'Disease', dis, ['Medication'])
    
    # Get diet
    die = safe_lookup(diets, 'Disease', dis, ['Diet'])
    
    # Get workout
    wrkout = safe_lookup(workout, 'disease', dis, ['workout'])
    
    # Try to get enhanced treatment info if available
    if treatment_lookup is not None:
        enhanced_match = treatment_lookup[treatment_lookup['Name'].str.lower().str.contains(dis.lower(), regex=False, na=False)]
        if not enhanced_match.empty:
            treatment_info = enhanced_match['Treatments'].iloc[0]
            if pd.notna(treatment_info) and treatment_info.strip():
                # Add enhanced treatment to medications if available
                med.insert(0, f"Enhanced Treatment: {treatment_info}")

    return desc, [pre], med, die, wrkout

# Model Prediction function - Updated for new ML model
def get_predicted_value(patient_symptoms):
    """
    New prediction function using your trained joblib model
    """
    if model_pipeline is None:
        return "Model not available. Please train the model first."
    
    # Convert symptoms list to text format for the new model
    symptoms_text = ", ".join(patient_symptoms)
    
    # Use the new model for prediction
    try:
        predicted_disease = predict_disease_from_symptoms(symptoms_text, model_pipeline)
        return predicted_disease
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Unable to predict. Please check your symptoms."

# Legacy function kept for compatibility (now uses new model)
def get_predicted_value_legacy(patient_symptoms):
    """
    Legacy prediction function converted to use new model
    This maintains compatibility with existing symptom processing
    """
    return get_predicted_value(patient_symptoms)




# creating routes========================================


@app.route("/")
def index():
    # Get some common symptoms to show as examples
    common_symptoms = ['itching', 'cough', 'high_fever', 'headache', 'stomach_pain', 'vomiting', 
                      'fatigue', 'chest_pain', 'nausea', 'dizziness', 'back_pain', 'joint_pain']
    return render_template("index.html", common_symptoms=common_symptoms)

@app.route('/symptoms')
def show_symptoms():
    """Display information about using symptoms with the new model"""
    return render_template("symptoms.html", 
                         info="Our new AI model can understand natural language symptom descriptions. Just describe how you feel!")

# Define a route for the prediction
@app.route('/predict', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        print(f"Raw symptoms input: '{symptoms}'")
        
        if not symptoms or symptoms.strip() == "" or symptoms == "Symptoms":
            message = "Please enter your symptoms to get a medical prediction."
            common_symptoms = ['itching', 'cough', 'high_fever', 'headache', 'stomach_pain', 'vomiting', 
                              'fatigue', 'chest_pain', 'nausea', 'dizziness', 'back_pain', 'joint_pain']
            return render_template('index.html', message=message, common_symptoms=common_symptoms)

        try:
            # Use the new model for prediction - it handles natural language input
            predicted_disease = get_predicted_value([symptoms])  # Pass as list for compatibility
            
            if "not available" in predicted_disease.lower() or "unable to predict" in predicted_disease.lower():
                message = "Unable to predict disease. Please check your symptoms and try again."
                common_symptoms = ['itching', 'cough', 'high_fever', 'headache', 'stomach_pain', 'vomiting', 
                                  'fatigue', 'chest_pain', 'nausea', 'dizziness', 'back_pain', 'joint_pain']
                return render_template('index.html', message=message, common_symptoms=common_symptoms)
            
            print(f"✅ Predicted disease: {predicted_disease}")
            
            # Get additional information about the disease
            dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

            my_precautions = []
            if precautions and len(precautions) > 0:
                for i in precautions[0]:
                    if i and str(i).strip() and str(i) != 'nan':  # Only add non-empty precautions
                        my_precautions.append(i)

            # Prepare clean data for template
            clean_medications = [med for med in medications if med and str(med).strip() and str(med) != 'nan']
            clean_diet = [diet for diet in rec_diet if diet and str(diet).strip() and str(diet) != 'nan']
            clean_workout = [work for work in workout if work and str(work).strip() and str(work) != 'nan']

            return render_template('index.html', 
                                   predicted_disease=predicted_disease, 
                                   dis_des=dis_des,
                                   my_precautions=my_precautions, 
                                   medications=clean_medications, 
                                   my_diet=clean_diet,
                                   workout=clean_workout, 
                                   user_symptoms=symptoms)

        except Exception as e:
            print(f"❌ Prediction error: {e}")
            message = f"An error occurred during prediction. Please try again with different symptoms."
            common_symptoms = ['itching', 'cough', 'high_fever', 'headache', 'stomach_pain', 'vomiting', 
                              'fatigue', 'chest_pain', 'nausea', 'dizziness', 'back_pain', 'joint_pain']
            return render_template('index.html', message=message, common_symptoms=common_symptoms)

    # GET request - show the form
    common_symptoms = ['itching', 'cough', 'high_fever', 'headache', 'stomach_pain', 'vomiting', 
                      'fatigue', 'chest_pain', 'nausea', 'dizziness', 'back_pain', 'joint_pain']
    return render_template('index.html', common_symptoms=common_symptoms)



# about view funtion and path
@app.route('/about')
def about():
    return render_template("about.html")
# contact view funtion and path
@app.route('/contact')
def contact():
    return render_template("contact.html")

# developer view funtion and path
@app.route('/developer')
def developer():
    return render_template("developer.html")

# about view funtion and path
@app.route('/blog')
def blog():
    return render_template("blog.html")


if __name__ == '__main__':

    app.run(debug=True)