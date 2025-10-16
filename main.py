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
causes = pd.read_csv(os.path.join(BASE_DIR, "causes.csv"))

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
except (FileNotFoundError, ImportError, Exception) as e:
    print(f"⚠️ Warning: Could not load ML model ({e}). Using fallback mode.")
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
    
    # Get causes
    causelist = safe_lookup(causes, 'Disease', dis, ['Cause_1', 'Cause_2', 'Cause_3', 'Cause_4', 'Cause_5'])
    
    # Try to get enhanced treatment info if available
    if treatment_lookup is not None:
        enhanced_match = treatment_lookup[treatment_lookup['Name'].str.lower().str.contains(dis.lower(), regex=False, na=False)]
        if not enhanced_match.empty:
            treatment_info = enhanced_match['Treatments'].iloc[0]
            if pd.notna(treatment_info) and treatment_info.strip():
                # Add enhanced treatment to medications if available
                med.insert(0, f"Enhanced Treatment: {treatment_info}")

    return desc, [pre], med, die, wrkout, causelist

# Model Prediction function - Updated for new ML model
def get_predicted_value(patient_symptoms):
    """
    New prediction function using your trained joblib model
    """
    if model_pipeline is None:
        # Fallback: return a sample disease for demonstration
        if 'fever' in str(patient_symptoms).lower() or 'headache' in str(patient_symptoms).lower():
            return "Common Cold"
        elif 'stomach' in str(patient_symptoms).lower() or 'nausea' in str(patient_symptoms).lower():
            return "Gastritis"
        else:
            return "General Health Checkup Recommended"
    
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
            dis_des, precautions, medications, rec_diet, workout, disease_causes = helper(predicted_disease)

            my_precautions = []
            if precautions and len(precautions) > 0:
                for i in precautions[0]:
                    if i and str(i).strip() and str(i) != 'nan':  # Only add non-empty precautions
                        my_precautions.append(i)

            # Prepare clean data for template
            clean_medications = [med for med in medications if med and str(med).strip() and str(med) != 'nan']
            clean_diet = [diet for diet in rec_diet if diet and str(diet).strip() and str(diet) != 'nan']
            clean_workout = [work for work in workout if work and str(work).strip() and str(work) != 'nan']
            clean_causes = [cause for cause in disease_causes if cause and str(cause).strip() and str(cause) != 'nan']

            return render_template('index.html', 
                                   predicted_disease=predicted_disease, 
                                   dis_des=dis_des,
                                   my_precautions=my_precautions, 
                                   medications=clean_medications, 
                                   my_diet=clean_diet,
                                   workout=clean_workout,
                                   disease_causes=clean_causes,
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

# Find nearby doctors/clinics route
@app.route('/find-doctors', methods=['POST'])
def find_doctors():
    """
    Endpoint to find nearby doctors/clinics based on user's location
    Uses Google Places API
    """
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not latitude or not longitude:
            return jsonify({'error': 'Location coordinates are required'}), 400
        
        # In a production environment, you would use Google Places API here
        # For now, we'll return mock data that you can replace with actual API calls
        
        # Example of what the Google Places API call would look like:
        # import requests
        # API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'
        # url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        # params = {
        #     'location': f'{latitude},{longitude}',
        #     'radius': 5000,  # 5km radius
        #     'type': 'doctor|hospital|health',
        #     'key': API_KEY
        # }
        # response = requests.get(url, params=params)
        # places = response.json().get('results', [])
        
        # Mock data for demonstration (replace with actual API call)
        mock_doctors = [
            {
                'name': 'City Medical Center',
                'address': '123 Main Street',
                'phone': '+1 (555) 123-4567',
                'rating': 4.5,
                'distance': '0.8 km',
                'type': 'Hospital',
                'open_now': True
            },
            {
                'name': 'Dr. Sarah Johnson - General Physician',
                'address': '456 Oak Avenue',
                'phone': '+1 (555) 234-5678',
                'rating': 4.8,
                'distance': '1.2 km',
                'type': 'Clinic',
                'open_now': True
            },
            {
                'name': 'HealthCare Plus Clinic',
                'address': '789 Pine Road',
                'phone': '+1 (555) 345-6789',
                'rating': 4.3,
                'distance': '1.5 km',
                'type': 'Clinic',
                'open_now': False
            },
            {
                'name': 'Emergency Medical Services',
                'address': '321 Elm Street',
                'phone': '+1 (555) 456-7890',
                'rating': 4.6,
                'distance': '2.1 km',
                'type': 'Hospital',
                'open_now': True
            },
            {
                'name': 'Dr. Michael Chen - Specialist',
                'address': '654 Maple Drive',
                'phone': '+1 (555) 567-8901',
                'rating': 4.9,
                'distance': '2.8 km',
                'type': 'Clinic',
                'open_now': True
            }
        ]
        
        return jsonify({
            'success': True,
            'doctors': mock_doctors,
            'location': {
                'latitude': latitude,
                'longitude': longitude
            }
        })
        
    except Exception as e:
        print(f"Error finding doctors: {e}")
        return jsonify({'error': 'An error occurred while searching for doctors'}), 500

# Pharmacy search route
@app.route('/pharmacy_search', methods=['POST'])
def pharmacy_search():
    """
    Search for pharmacies based on location or city name
    """
    try:
        data = request.get_json()
        search_type = data.get('search_type')
        
        if search_type == 'coordinates':
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            if not latitude or not longitude:
                return jsonify({'success': False, 'error': 'Invalid coordinates'})
            
            pharmacies = search_pharmacies_by_coordinates(latitude, longitude)
            
        elif search_type == 'city':
            city = data.get('city')
            
            if not city:
                return jsonify({'success': False, 'error': 'City name is required'})
            
            pharmacies = search_pharmacies_by_city(city)
            
        else:
            return jsonify({'success': False, 'error': 'Invalid search type'})
        
        return jsonify({
            'success': True,
            'pharmacies': pharmacies,
            'count': len(pharmacies)
        })
        
    except Exception as e:
        print(f"❌ Pharmacy search error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to search pharmacies. Please try again.'
        })

def search_pharmacies_by_coordinates(lat, lng):
    """
    Search for pharmacies using coordinates
    For now, this returns sample data. In production, you would use Google Places API or similar.
    """
    # Sample data for demonstration
    sample_pharmacies = [
        {
            'name': 'HealthPlus Pharmacy',
            'address': f'123 Main St, Near ({lat:.4f}, {lng:.4f})',
            'phone': '+1-555-0123',
            'rating': 4.5,
            'distance': '0.2 miles'
        },
        {
            'name': 'MediCare Drugstore',
            'address': f'456 Oak Ave, Near ({lat:.4f}, {lng:.4f})',
            'phone': '+1-555-0456',
            'rating': 4.2,
            'distance': '0.5 miles'
        },
        {
            'name': 'Quick Pharmacy',
            'address': f'789 Pine Rd, Near ({lat:.4f}, {lng:.4f})',
            'phone': '+1-555-0789',
            'rating': 4.0,
            'distance': '0.8 miles'
        }
    ]
    
    # TODO: Replace with actual API call
    # Example: Google Places API, Yelp API, or OpenStreetMap Overpass API
    # places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    # params = {
    #     'location': f'{lat},{lng}',
    #     'radius': 5000,
    #     'type': 'pharmacy',
    #     'key': 'YOUR_GOOGLE_PLACES_API_KEY'
    # }
    
    return sample_pharmacies

def search_pharmacies_by_city(city):
    """
    Search for pharmacies using city name
    For now, this returns sample data. In production, you would geocode the city first.
    """
    # Sample data for demonstration
    sample_pharmacies = [
        {
            'name': f'{city} Central Pharmacy',
            'address': f'100 Central St, {city}',
            'phone': '+1-555-1000',
            'rating': 4.3,
            'distance': '1.2 miles'
        },
        {
            'name': f'{city} Family Drugstore',
            'address': f'250 Market St, {city}',
            'phone': '+1-555-2500',
            'rating': 4.1,
            'distance': '1.8 miles'
        },
        {
            'name': f'Express Pharmacy - {city}',
            'address': f'380 Broadway, {city}',
            'phone': '+1-555-3800',
            'rating': 4.4,
            'distance': '2.1 miles'
        },
        {
            'name': f'{city} Medical Pharmacy',
            'address': f'500 Health Plaza, {city}',
            'phone': '+1-555-5000',
            'rating': 4.6,
            'distance': '2.5 miles'
        }
    ]
    
    # TODO: Replace with actual API implementation
    # 1. Geocode city name to get coordinates
    # 2. Use coordinates to search for nearby pharmacies
    # geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json"
    # places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    return sample_pharmacies


if __name__ == '__main__':

    app.run(debug=True)