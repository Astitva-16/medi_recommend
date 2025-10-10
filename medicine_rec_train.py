import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import warnings
import numpy as np

warnings.filterwarnings('ignore')

# --- 1. Data Loading and Preprocessing ---

def preprocess_text(text):
    """Cleans and standardizes text for modeling."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_training_data():
    """Loads, merges, and cleans the training data from multiple sources."""
    print("--- Loading Training Data ---")
    
    # Load the large training dataset
    large_train_file = 'train-00000-of-00001.csv'
    try:
        print(f"Loading {large_train_file}...")
        df1 = pd.read_csv(large_train_file)
        df1['symptoms'] = df1['text'].str.extract(r'symptoms: (.*?)\s*may indicate', expand=False)
        df1 = df1[['symptoms', 'diagnosis']].dropna()
        df1.rename(columns={'diagnosis': 'disease'}, inplace=True)
    except FileNotFoundError:
        print(f"Warning: '{large_train_file}' not found. Skipping.")
        df1 = pd.DataFrame(columns=['symptoms', 'disease'])

    # Load second dataset
    try:
        df2 = pd.read_csv('Diseases_Symptoms.csv')
        df2 = df2[['Symptoms', 'Name']].dropna()
        df2.rename(columns={'Symptoms': 'symptoms', 'Name': 'disease'}, inplace=True)
    except FileNotFoundError:
        print("Warning: 'Diseases_Symptoms.csv' not found. Skipping.")
        df2 = pd.DataFrame(columns=['symptoms', 'disease'])

    # Load third dataset
    try:
        df3 = pd.read_csv('disease_diagnosis.csv')
        symptom_cols = ['Symptom_1', 'Symptom_2', 'Symptom_3']
        df3['symptoms'] = df3[symptom_cols].apply(lambda row: ', '.join(row.dropna()), axis=1)
        df3 = df3[['symptoms', 'Diagnosis']].dropna()
        df3.rename(columns={'Diagnosis': 'disease'}, inplace=True)
    except FileNotFoundError:
        print("Warning: 'disease_diagnosis.csv' not found. Skipping.")
        df3 = pd.DataFrame(columns=['symptoms', 'disease'])

    # Combine all training dataframes
    train_df = pd.concat([df1, df2, df3], ignore_index=True)
    
    # Preprocess text
    train_df['symptoms'] = train_df['symptoms'].apply(preprocess_text)
    train_df['disease'] = train_df['disease'].apply(preprocess_text)
    train_df = train_df[train_df['symptoms'] != '']

    # Filter rare diseases based *only* on training data
    print("Filtering out very rare diseases (less than 2 occurrences in training set)...")
    disease_counts = train_df['disease'].value_counts()
    diseases_to_keep = disease_counts[disease_counts >= 2].index
    original_rows = len(train_df)
    train_df = train_df[train_df['disease'].isin(diseases_to_keep)]
    print(f"Removed {original_rows - len(train_df)} rows belonging to rare diseases from training data.")
    
    print(f"Total training data records: {len(train_df)}")
    return train_df, diseases_to_keep

def load_testing_data(diseases_to_keep):
    """Loads and cleans the testing data, ensuring it aligns with training data."""
    print("\n--- Loading Testing Data ---")
    test_file = 'test-00000-of-00001.csv'
    try:
        test_df = pd.read_csv(test_file)
        test_df['symptoms'] = test_df['text'].str.extract(r'symptoms: (.*?)\s*may indicate', expand=False)
        test_df = test_df[['symptoms', 'diagnosis']].dropna()
        test_df.rename(columns={'diagnosis': 'disease'}, inplace=True)
        
        # Preprocess text
        test_df['symptoms'] = test_df['symptoms'].apply(preprocess_text)
        test_df['disease'] = test_df['disease'].apply(preprocess_text)
        
        # Filter test data to only include diseases present in the training set
        original_rows = len(test_df)
        test_df = test_df[test_df['disease'].isin(diseases_to_keep)]
        print(f"Removed {original_rows - len(test_df)} rows from test data for diseases not in the training set.")

        print(f"Total testing data records: {len(test_df)}")
        return test_df
    except FileNotFoundError:
        print(f"Error: Test file '{test_file}' not found. Cannot proceed with evaluation.")
        return pd.DataFrame()

# --- 2. Model Training ---

def train_and_evaluate(X_train, y_train, X_test, y_test):
    """Trains the model, evaluates it, and saves it."""
    
    print("\n--- Model Training and Evaluation ---")
    print("Vectorizing text data...")
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    print("Applying SMOTE to handle data imbalance...")
    class_counts = y_train.value_counts()
    min_class_count = class_counts.min()

    if min_class_count > 1:
        k_neighbors_dynamic = min_class_count - 1
        print(f"Smallest class has {min_class_count} samples. Setting SMOTE k_neighbors to {k_neighbors_dynamic}.")
        smote = SMOTE(random_state=42, k_neighbors=k_neighbors_dynamic)
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train_tfidf, y_train)
        print(f"Data resampled. Original train size: {X_train_tfidf.shape[0]}, Resampled train size: {X_train_resampled.shape[0]}")
    else:
        print("Skipping SMOTE: The smallest class has only 1 sample, not enough for resampling.")
        X_train_resampled, y_train_resampled = X_train_tfidf, y_train

    # Using our best performing model: LinearSVC
    print("Training the LinearSVC model...")
    model = LinearSVC(random_state=42)
    model.fit(X_train_resampled, y_train_resampled)

    # Evaluation
    print("\n--- Model Evaluation ---")
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Confusion Matrix Analysis
    print("\n--- Confusion Matrix Analysis (Top 15 Errors) ---")
    labels = sorted(list(set(y_test) | set(y_pred)))
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    errors = []
    for i, true_label in enumerate(labels):
        for j, predicted_label in enumerate(labels):
            if i != j and cm[i, j] > 0:
                errors.append((true_label, predicted_label, cm[i, j]))
    errors.sort(key=lambda x: x[2], reverse=True)
    
    if not errors:
        print("No misclassifications found on the test set!")
    else:
        print("Actual Disease -> Predicted Disease (Count of Errors)")
        print("-" * 50)
        for true, pred, count in errors[:15]:
            print(f"{true} -> {pred} ({count})")

    # Save the Model and Vectorizer
    model_pipeline = { 'model': model, 'vectorizer': vectorizer }
    joblib.dump(model_pipeline, 'disease_model.joblib')
    print("\nModel and vectorizer saved to 'disease_model.joblib'")


if __name__ == '__main__':
    train_df, diseases_to_keep = load_training_data()
    test_df = load_testing_data(diseases_to_keep)

    if not train_df.empty and not test_df.empty:
        # Ensure test set doesn't have labels the training set has never seen
        y_train_unique = set(train_df['disease'])
        test_df = test_df[test_df['disease'].isin(y_train_unique)]
        
        X_train = train_df['symptoms']
        y_train = train_df['disease']
        X_test = test_df['symptoms']
        y_test = test_df['disease']
        
        train_and_evaluate(X_train, y_train, X_test, y_test)
    else:
        print("Training or testing data is empty. Halting execution.")

