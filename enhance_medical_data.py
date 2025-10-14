import pandas as pd
import json
import re

# Medical knowledge base extracted from authoritative sources
medical_knowledge = {
    # Cardiovascular Diseases
    "cardiovascular": {
        "precautions": [
            "Monitor blood pressure regularly",
            "Follow a heart-healthy diet (low sodium, low saturated fat)",
            "Maintain healthy cholesterol levels",
            "Avoid smoking and excessive alcohol consumption"
        ],
        "medications": [
            "ACE inhibitors (Lisinopril, Enalapril)",
            "Beta-blockers (Metoprolol, Atenolol)",
            "Calcium channel blockers (Amlodipine)",
            "Statins (Atorvastatin, Simvastatin)"
        ],
        "exercises": [
            "Moderate aerobic exercise 30 minutes daily",
            "Walking or light jogging",
            "Swimming or water aerobics",
            "Cycling on level terrain"
        ]
    },
    
    # Diabetes and Metabolic Disorders
    "diabetes": {
        "precautions": [
            "Monitor blood glucose levels regularly",
            "Follow prescribed meal plans and timing",
            "Maintain proper foot care and hygiene",
            "Keep emergency glucose sources available"
        ],
        "medications": [
            "Metformin for blood sugar control",
            "Insulin (rapid-acting, long-acting)",
            "Sulfonylureas (Glipizide, Glyburide)",
            "DPP-4 inhibitors (Sitagliptin)"
        ],
        "exercises": [
            "Regular moderate exercise 30 minutes daily",
            "Brisk walking after meals",
            "Resistance training 2-3 times per week",
            "Flexibility and balance exercises"
        ]
    },
    
    # Respiratory Disorders
    "respiratory": {
        "precautions": [
            "Avoid triggers like allergens and pollutants",
            "Get annual flu vaccinations",
            "Practice proper hand hygiene",
            "Use air purifiers when needed"
        ],
        "medications": [
            "Bronchodilators (Albuterol, Salmeterol)",
            "Corticosteroids (Prednisone, Fluticasone)",
            "Antibiotics for bacterial infections",
            "Expectorants and mucolytics"
        ],
        "exercises": [
            "Breathing exercises and techniques",
            "Low-intensity aerobic activities",
            "Pulmonary rehabilitation programs",
            "Gentle yoga and stretching"
        ]
    },
    
    # Neurological Disorders
    "neurological": {
        "precautions": [
            "Take medications consistently as prescribed",
            "Maintain regular sleep schedule",
            "Avoid known seizure triggers",
            "Wear medical identification when appropriate"
        ],
        "medications": [
            "Anticonvulsants (Phenytoin, Carbamazepine)",
            "Dopamine agonists (Levodopa)",
            "Cholinesterase inhibitors (Donepezil)",
            "Muscle relaxants (Baclofen)"
        ],
        "exercises": [
            "Physical therapy exercises",
            "Range of motion exercises",
            "Balance and coordination training",
            "Cognitive rehabilitation activities"
        ]
    },
    
    # Musculoskeletal Disorders
    "musculoskeletal": {
        "precautions": [
            "Maintain good posture",
            "Use proper body mechanics",
            "Avoid repetitive strain",
            "Apply heat/cold therapy as appropriate"
        ],
        "medications": [
            "NSAIDs (Ibuprofen, Naproxen)",
            "Topical analgesics (Capsaicin cream)",
            "Muscle relaxants (Cyclobenzaprine)",
            "Disease-modifying antirheumatic drugs (DMARDs)"
        ],
        "exercises": [
            "Low-impact aerobic exercises",
            "Strengthening exercises",
            "Flexibility and stretching routines",
            "Water-based exercises"
        ]
    },
    
    # Mental Health Disorders
    "mental_health": {
        "precautions": [
            "Maintain regular therapy appointments",
            "Practice stress management techniques",
            "Maintain social connections",
            "Monitor mood changes and triggers"
        ],
        "medications": [
            "SSRIs (Sertraline, Fluoxetine)",
            "SNRIs (Venlafaxine, Duloxetine)",
            "Mood stabilizers (Lithium, Valproate)",
            "Antipsychotics (Risperidone, Olanzapine)"
        ],
        "exercises": [
            "Regular aerobic exercise",
            "Yoga and mindfulness practices",
            "Recreational activities and hobbies",
            "Social and group activities"
        ]
    },
    
    # Gastrointestinal Disorders
    "gastrointestinal": {
        "precautions": [
            "Follow dietary modifications",
            "Avoid trigger foods",
            "Maintain proper hydration",
            "Practice good food hygiene"
        ],
        "medications": [
            "Proton pump inhibitors (Omeprazole)",
            "H2 receptor blockers (Ranitidine)",
            "Antispasmodics (Dicyclomine)",
            "Probiotics and digestive enzymes"
        ],
        "exercises": [
            "Light walking after meals",
            "Gentle abdominal exercises",
            "Stress-reduction activities",
            "Pelvic floor exercises"
        ]
    },
    
    # Infectious Diseases
    "infectious": {
        "precautions": [
            "Complete full course of antibiotics",
            "Practice proper isolation measures",
            "Maintain good hygiene practices",
            "Boost immune system with proper nutrition"
        ],
        "medications": [
            "Antibiotics (Amoxicillin, Azithromycin)",
            "Antivirals (Acyclovir, Oseltamivir)",
            "Antifungals (Fluconazole, Clotrimazole)",
            "Supportive medications for symptoms"
        ],
        "exercises": [
            "Rest and gradual return to activity",
            "Light stretching when appropriate",
            "Breathing exercises",
            "Immune-boosting activities when recovered"
        ]
    },
    
    # Endocrine Disorders
    "endocrine": {
        "precautions": [
            "Regular hormone level monitoring",
            "Consistent medication timing",
            "Dietary modifications as prescribed",
            "Regular medical follow-ups"
        ],
        "medications": [
            "Hormone replacement therapy",
            "Thyroid medications (Levothyroxine)",
            "Corticosteroids (Hydrocortisone)",
            "Insulin and glucose-regulating drugs"
        ],
        "exercises": [
            "Regular moderate exercise",
            "Weight-bearing exercises",
            "Flexibility training",
            "Stress management activities"
        ]
    },
    
    # General/Default category
    "general": {
        "precautions": [
            "Follow medical advice and treatment plans",
            "Maintain regular medical check-ups",
            "Practice good hygiene and health habits",
            "Monitor symptoms and report changes"
        ],
        "medications": [
            "Over-the-counter pain relievers as needed",
            "Prescription medications as directed",
            "Vitamins and supplements if recommended",
            "Topical treatments for local symptoms"
        ],
        "exercises": [
            "Light to moderate physical activity",
            "Stretching and flexibility exercises",
            "Walking and gentle movements",
            "Rest and recovery as needed"
        ]
    }
}

# Disease categorization based on medical knowledge
disease_categories = {
    # Cardiovascular
    "cardiovascular": [
        "coronary atherosclerosis", "hypertensive heart disease", "heart block", 
        "mitral valve disease", "hypertrophic obstructive cardiomyopathy", "pericarditis",
        "thoracic aortic aneurysm", "vasculitis", "heart", "cardiac", "vascular",
        "hypertension", "blood pressure"
    ],
    
    # Diabetes and Metabolic
    "diabetes": [
        "type 2 diabetes", "gestational diabetes", "hypoglycemia", "insulin",
        "diabetes", "diabetic", "glucose", "hyperglycemia", "metabolic"
    ],
    
    # Respiratory
    "respiratory": [
        "bronchitis", "pneumonia", "emphysema", "cystic fibrosis", "asthma",
        "pulmonary", "lung", "respiratory", "breathing", "cough", "broncho"
    ],
    
    # Neurological
    "neurological": [
        "parkinson", "alzheimer", "epilepsy", "seizure", "migraine", "headache",
        "neuropathy", "encephalitis", "myasthenia gravis", "multiple sclerosis",
        "neurological", "nerve", "brain", "neurological", "paralysis"
    ],
    
    # Musculoskeletal
    "musculoskeletal": [
        "arthritis", "osteoporosis", "fracture", "bone", "joint", "muscle",
        "rheumatoid", "osteo", "muscular", "skeletal", "spine", "back pain"
    ],
    
    # Mental Health
    "mental_health": [
        "depression", "anxiety", "panic", "bipolar", "schizophrenia",
        "mental", "psychiatric", "psychological", "mood", "stress"
    ],
    
    # Gastrointestinal
    "gastrointestinal": [
        "gastroenteritis", "gerd", "ulcer", "colitis", "crohn", "gastro",
        "intestinal", "bowel", "stomach", "digestive", "hepatitis", "liver"
    ],
    
    # Infectious
    "infectious": [
        "infection", "bacterial", "viral", "fungal", "parasitic", "sepsis",
        "influenza", "pneumonia", "tuberculosis", "meningitis", "abscess"
    ],
    
    # Endocrine
    "endocrine": [
        "thyroid", "hormone", "pituitary", "adrenal", "endocrine",
        "hypothyroidism", "hyperthyroidism", "cushings", "addison"
    ]
}

def categorize_disease(disease_name):
    """Categorize disease based on name patterns"""
    disease_lower = disease_name.lower()
    
    for category, keywords in disease_categories.items():
        for keyword in keywords:
            if keyword in disease_lower:
                return category
    
    return "general"

def get_medical_info(disease_name, info_type):
    """Get medical information for a disease"""
    category = categorize_disease(disease_name)
    
    if category in medical_knowledge:
        return medical_knowledge[category].get(info_type, medical_knowledge["general"][info_type])
    else:
        return medical_knowledge["general"][info_type]

def enhance_precautions_data():
    """Enhance precautions data"""
    try:
        # Read existing data
        diseases_df = pd.read_csv('Diseases_Symptoms.csv')
        precautions_df = pd.read_csv('precautions_df.csv')
        
        # Get existing diseases in precautions
        existing_diseases = set(precautions_df['Disease'].tolist())
        
        # Find missing diseases
        all_diseases = set(diseases_df['Name'].tolist())
        missing_diseases = all_diseases - existing_diseases
        
        print(f"Adding precautions for {len(missing_diseases)} diseases...")
        
        # Add missing diseases
        new_rows = []
        for disease in missing_diseases:
            precautions = get_medical_info(disease, 'precautions')
            
            # Pad with empty strings if needed
            while len(precautions) < 4:
                precautions.append("")
            
            new_row = {
                'Disease': disease,
                'Precaution_1': precautions[0],
                'Precaution_2': precautions[1],
                'Precaution_3': precautions[2],
                'Precaution_4': precautions[3]
            }
            new_rows.append(new_row)
        
        # Create new dataframe and combine
        new_precautions_df = pd.DataFrame(new_rows)
        enhanced_precautions_df = pd.concat([precautions_df, new_precautions_df], ignore_index=True)
        
        # Save enhanced data
        enhanced_precautions_df.to_csv('precautions_df.csv', index=False)
        print(f"Enhanced precautions saved. Total entries: {len(enhanced_precautions_df)}")
        
    except Exception as e:
        print(f"Error enhancing precautions: {e}")

def enhance_medications_data():
    """Enhance medications data"""
    try:
        # Read existing data
        diseases_df = pd.read_csv('Diseases_Symptoms.csv')
        medications_df = pd.read_csv('medications.csv')
        
        # Get existing diseases in medications
        existing_diseases = set(medications_df['Disease'].tolist())
        
        # Find missing diseases
        all_diseases = set(diseases_df['Name'].tolist())
        missing_diseases = all_diseases - existing_diseases
        
        print(f"Adding medications for {len(missing_diseases)} diseases...")
        
        # Add missing diseases
        new_rows = []
        for disease in missing_diseases:
            medications = get_medical_info(disease, 'medications')
            medication_text = "; ".join(medications)
            
            new_row = {
                'Disease': disease,
                'Medication': medication_text
            }
            new_rows.append(new_row)
        
        # Create new dataframe and combine
        new_medications_df = pd.DataFrame(new_rows)
        enhanced_medications_df = pd.concat([medications_df, new_medications_df], ignore_index=True)
        
        # Save enhanced data
        enhanced_medications_df.to_csv('medications.csv', index=False)
        print(f"Enhanced medications saved. Total entries: {len(enhanced_medications_df)}")
        
    except Exception as e:
        print(f"Error enhancing medications: {e}")

def enhance_workout_data():
    """Enhance workout/exercise data"""
    try:
        # Read existing data
        diseases_df = pd.read_csv('Diseases_Symptoms.csv')
        workout_df = pd.read_csv('workout_df.csv')
        
        # Get existing diseases in workout (using lowercase 'disease' column)
        existing_diseases = set(workout_df['disease'].tolist())
        
        # Find missing diseases
        all_diseases = set(diseases_df['Name'].tolist())
        missing_diseases = all_diseases - existing_diseases
        
        print(f"Adding exercises for {len(missing_diseases)} diseases...")
        
        # Add missing diseases
        new_rows = []
        for disease in missing_diseases:
            exercises = get_medical_info(disease, 'exercises')
            exercise_text = "; ".join(exercises)
            
            new_row = {
                'disease': disease,
                'workout': exercise_text
            }
            new_rows.append(new_row)
        
        # Create new dataframe and combine
        new_workout_df = pd.DataFrame(new_rows)
        enhanced_workout_df = pd.concat([workout_df, new_workout_df], ignore_index=True)
        
        # Save enhanced data
        enhanced_workout_df.to_csv('workout_df.csv', index=False)
        print(f"Enhanced workouts saved. Total entries: {len(enhanced_workout_df)}")
        
    except Exception as e:
        print(f"Error enhancing workouts: {e}")

def main():
    """Main function to enhance all medical data"""
    print("Starting comprehensive medical data enhancement...")
    print("=" * 60)
    
    # Enhance all data files
    enhance_precautions_data()
    print()
    
    enhance_medications_data()
    print()
    
    enhance_workout_data()
    print()
    
    # Final summary
    print("=" * 60)
    print("Enhancement complete! Summary:")
    
    try:
        diseases_df = pd.read_csv('Diseases_Symptoms.csv')
        precautions_df = pd.read_csv('precautions_df.csv')
        medications_df = pd.read_csv('medications.csv')
        workout_df = pd.read_csv('workout_df.csv')
        
        print(f"Total diseases: {len(diseases_df)}")
        print(f"Diseases with precautions: {len(precautions_df)}")
        print(f"Diseases with medications: {len(medications_df)}")
        print(f"Diseases with exercises: {len(workout_df)}")
        
        # Check coverage
        diseases_with_precautions = len(precautions_df) / len(diseases_df) * 100
        diseases_with_medications = len(medications_df) / len(diseases_df) * 100
        diseases_with_exercises = len(workout_df) / len(diseases_df) * 100
        
        print(f"\nCoverage:")
        print(f"Precautions: {diseases_with_precautions:.1f}%")
        print(f"Medications: {diseases_with_medications:.1f}%")
        print(f"Exercises: {diseases_with_exercises:.1f}%")
        
    except Exception as e:
        print(f"Error generating summary: {e}")

if __name__ == "__main__":
    main()