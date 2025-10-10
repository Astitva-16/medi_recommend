import joblib
import re
import pandas as pd

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

if __name__ == '__main__':
    try:
        # Load the trained model and vectorizer
        pipeline = joblib.load('disease_model.joblib')
        print("Disease Prediction Model loaded successfully.")
        print("Enter your symptoms below to get a prediction.")
        print("Type 'exit' to quit the program.\n")

        while True:
            # Get user input
            user_input = input("Enter symptoms: ")
            
            if user_input.lower() == 'exit':
                break
            
            if not user_input.strip():
                print("Please enter some symptoms.")
                continue

            # Get the prediction
            prediction = predict_disease_from_symptoms(user_input, pipeline)
            print(f"Predicted Disease: {prediction}\n")

    except FileNotFoundError:
        print("Error: 'disease_model.joblib' not found.")
        print("Please run the 'train_model.py' script first to train and save the model.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
