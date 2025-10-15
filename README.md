# 🏥 SymptoCare - AI-Powered Medical Recommendation System

A comprehensive machine learning-based health recommendation system that provides intelligent medical insights based on symptom analysis with enhanced medical data for 405+ diseases.

## 🌟 Overview

SymptoCare leverages advanced machine learning algorithms to analyze user symptoms and provide personalized health recommendations. The system offers a complete health management solution with predictive capabilities, comprehensive medical data, and actionable insights for better healthcare decisions.

## ✨ Key Features

### 🔍 Advanced Symptom Analysis
- Intelligent symptom input through intuitive web interface
- TF-IDF vectorization for accurate text processing
- LinearSVC classifier for high-precision disease prediction
- Support for 405+ diseases with comprehensive symptom mapping

### 💊 Comprehensive Medical Recommendations
Our enhanced system provides detailed recommendations including:
- **Medications**: Evidence-based pharmaceutical recommendations
- **Precautions**: Detailed preventive measures and safety guidelines
- **Exercise**: Customized workout plans and physical therapy suggestions
- **Dietary Plans**: Nutritional guidance and therapeutic diets
- **Disease Information**: Comprehensive descriptions and severity assessments

### 🌐 Modern Web Interface
- Responsive Flask-based web application
- Bootstrap 5.3.1 integration for modern UI/UX
- Voice input capabilities for accessibility
- Real-time prediction results

## 🔬 Technical Implementation

### Machine Learning Pipeline
- **Algorithm**: LinearSVC (Linear Support Vector Classifier)
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Training Data**: Enhanced dataset with 405+ diseases and comprehensive symptom patterns
- **Accuracy**: High-precision predictions with SMOTE balancing for improved performance
- **Model Persistence**: Serialized using joblib for optimal ML model storage

### 🛠️ Technology Stack
- **Backend**: Python 3.x, Flask 2.3.2
- **Machine Learning**: 
  - scikit-learn 1.3.0 (LinearSVC, TF-IDF)
  - pandas 2.0.3 (Data processing)
  - numpy 1.24.3 (Numerical computing)
  - joblib (Model serialization)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.1, JavaScript
- **Data Storage**: Enhanced CSV datasets with comprehensive medical information
- **Web Server**: Werkzeug 2.3.6 WSGI server

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/Astitva-16/medi_recommend.git
cd medi_recommend
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Train the machine learning model (if not already trained):
```bash
python medicine_rec_train.py
```

4. Run the application:
```bash
python main.py
```

5. Open your browser and navigate to `http://localhost:5000`
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to `http://localhost:5000`

## 🚀 Usage

1. **Access the Web Interface**: Open the application in your browser at `http://localhost:5000`
2. **Input Symptoms**: Enter your symptoms using the intuitive interface or voice input feature
3. **Get AI Predictions**: The ML model analyzes your input using TF-IDF and LinearSVC
4. **Review Comprehensive Recommendations**: Receive personalized suggestions for:
   - Evidence-based medications
   - Detailed precautionary measures
   - Customized exercise routines
   - Therapeutic dietary plans

## 📊 Enhanced Dataset Information

The system uses multiple comprehensive CSV datasets with enhanced medical data:

### Core Datasets
- `Diseases_Symptoms.csv`: Enhanced dataset with 405+ diseases and comprehensive medical information
- `Training.csv`: Main training dataset for ML model
- `symtoms_df.csv`: Symptom information and severity mapping
- `Symptom-severity.csv`: Symptom severity classifications
- `disease_diagnosis.csv`: Disease diagnosis mappings
- `train-00000-of-00001.csv`: Additional training data
- `test-00000-of-00001.csv`: Test dataset

### Medical Recommendations
- `medications.csv`: Comprehensive medication database with dosages and interactions
- `diets.csv`: Therapeutic dietary recommendations and nutritional guidance
- `workout_df.csv`: Customized exercise suggestions and physical therapy
- `precautions_df.csv`: Detailed precautionary measures and safety guidelines
- `description.csv`: Comprehensive disease descriptions and medical information
- `treatment_lookup.csv`: Treatment mapping and lookup table

### Model Files
- `disease_model.joblib`: Trained LinearSVC model with TF-IDF vectorizer
- `medicine_rec_train.py`: Model training pipeline with SMOTE balancing
- `medicine_rec_prediction.py`: Standalone prediction module
- `enhance_medical_data.py`: Medical data enhancement script

## 📁 Project Structure

```
medi_recommend/
├── main.py                      # Flask web application
├── medicine_rec_train.py        # ML model training pipeline
├── medicine_rec_prediction.py   # Standalone prediction module
├── disease_model.joblib         # Trained LinearSVC model with TF-IDF
├── enhance_medical_data.py      # Medical data enhancement script
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── README_NEW.md               # Additional documentation
├── .gitignore                  # Git ignore file
├── .gitattributes              # Git attributes
├── templates/                   # HTML templates
│   ├── index.html              # Main interface
│   ├── about.html              # About page
│   ├── blog.html               # Blog page
│   └── contact.html            # Contact page
├── static/                     # Static assets
│   └── css/
│       └── theme.css           # Custom styling
└── CSV datasets/               # Enhanced medical datasets
    ├── Diseases_Symptoms.csv   # 405+ diseases with enhanced data
    ├── Training.csv            # ML training dataset
    ├── disease_diagnosis.csv   # Disease diagnosis mappings
    ├── train-00000-of-00001.csv # Additional training data
    ├── test-00000-of-00001.csv # Test dataset
    ├── medications.csv         # Comprehensive medication database
    ├── precautions_df.csv      # Detailed precautionary measures
    ├── workout_df.csv          # Exercise recommendations
    ├── diets.csv              # Dietary suggestions
    ├── treatment_lookup.csv    # Treatment mapping table
    ├── symtoms_df.csv         # Symptom classifications
    ├── Symptom-severity.csv   # Symptom severity data
    └── description.csv         # Disease descriptions
```

## 🎯 Model Performance

- **Algorithm**: LinearSVC with TF-IDF vectorization
- **Training**: Enhanced dataset with SMOTE balancing for improved accuracy
- **Diseases**: 405+ diseases with comprehensive symptom mapping
- **Features**: Text-based symptom processing with advanced NLP techniques
- **Serialization**: joblib for efficient model storage and loading

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas for contribution:
- Additional disease data and symptoms
- UI/UX improvements
- Model accuracy enhancements
- API development
- Mobile application development

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

**Important**: This system is for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns and before making any healthcare decisions.

## 📈 Project Statistics

- **Total Files**: 30 files
- **Project Size**: 152.28 MB
- **CSV Datasets**: 13 comprehensive medical datasets
- **Diseases Covered**: 405+ with enhanced medical data
- **Templates**: 4 HTML templates with responsive design
- **Core Modules**: 
  - Flask web application (main.py)
  - ML training pipeline (medicine_rec_train.py)
  - Prediction module (medicine_rec_prediction.py)
  - Data enhancement script (enhance_medical_data.py)

## 🔗 Technical Details

**Enhanced Medical Data**: Comprehensive web-researched medical information including:
- Evidence-based medication recommendations
- Detailed precautionary measures and safety guidelines
- Therapeutic exercise and workout routines
- Nutritional guidance and dietary recommendations

**Machine Learning Pipeline**: 
- TF-IDF vectorization for symptom text processing
- LinearSVC classification for disease prediction
- joblib serialization for optimal model performance
- SMOTE balancing for improved accuracy across disease classes

---

**Data Source**: Enhanced CSV datasets with comprehensive medical information
**ML Model**: LinearSVC with TF-IDF (disease_model.joblib) trained on symptom-disease mappings
**Framework**: Flask 2.3.2 with Bootstrap 5.3.1 frontend


