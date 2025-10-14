# 🏥 Symptocare - AI-Powered Medical Recommendation System

A personalized medical recommendation system that uses advanced machine learning to predict potential diseases based on symptoms and provides comprehensive health guidance with enhanced medical data for 405+ diseases.

## 🌟 Features

- **🔍 AI-Powered Disease Prediction**: Input symptoms and get accurate disease predictions using LinearSVC and TF-IDF vectorization
- **💊 Evidence-Based Recommendations**: Get comprehensive medicine suggestions, detailed precautions, and therapeutic guidance
- **🏃‍♂️ Personalized Wellness Plans**: Customized workout routines and evidence-based dietary recommendations
- **🌐 Modern Web Interface**: Clean and intuitive Flask-based web application with voice input capabilities
- **📊 Comprehensive Medical Database**: Enhanced dataset covering 405+ diseases with detailed medical information
- **🎯 High Accuracy**: Advanced ML pipeline with SMOTE balancing for improved prediction accuracy

## 🚀 How It Works

1. **📝 Input Symptoms**: Users enter symptoms through the web interface or voice input
2. **🤖 AI Analysis**: TF-IDF vectorization processes text and LinearSVC analyzes symptom patterns
3. **🎯 Disease Prediction**: Advanced ML model predicts potential diseases with confidence scoring
4. **💡 Comprehensive Guidance**: Provides evidence-based medicines, precautions, workouts, and dietary plans

## 🛠️ Technology Stack

### Backend & ML
- **🐍 Python 3.x**: Core programming language
- **🌐 Flask 2.3.2**: Web framework with Werkzeug 2.3.6
- **🤖 scikit-learn 1.3.0**: LinearSVC classifier and TF-IDF vectorization
- **📊 pandas 2.0.3**: Data processing and analysis
- **🔢 numpy 1.24.3**: Numerical computing
- **💾 joblib**: Efficient ML model serialization

### Frontend
- **🎨 HTML5, CSS3**: Modern web standards
- **🎨 Bootstrap 5.3.1**: Responsive UI framework
- **⚡ JavaScript**: Interactive features and voice input
- **📱 Responsive Design**: Mobile-friendly interface

### Data & Models
- **📋 Enhanced CSV datasets**: Comprehensive medical information
- **🧠 disease_model.joblib**: Trained LinearSVC with TF-IDF vectorizer
- **🔄 SMOTE Balancing**: Improved accuracy across disease classes

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

## 🏃‍♂️ Quick Start

1. **📥 Clone the repository**
   ```bash
   git clone https://github.com/Astitva-16/medi_recommend.git
   cd medi_recommend
   ```

2. **📦 Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **🤖 Train the model (if needed)**
   ```bash
   python medicine_rec_train.py
   ```

4. **🚀 Run the application**
   ```bash
   python main.py
   ```

5. **🌐 Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 Usage

1. **🌐 Open the web application** at `http://localhost:5000`
2. **📝 Select your symptoms** from the comprehensive symptom database or use voice input
3. **🤖 Click "Predict"** to get AI-powered disease analysis using LinearSVC
4. **📋 View comprehensive recommendations** including:
   - 🎯 **Predicted diseases** with confidence scores
   - 💊 **Evidence-based medications** with detailed information
   - ⚠️ **Preventive measures** and safety precautions
   - 🏃‍♂️ **Customized workout routines** and physical therapy
   - 🥗 **Therapeutic dietary recommendations** and nutritional guidance

## 🔬 Technical Implementation

### Machine Learning Pipeline
- **Algorithm**: LinearSVC (Linear Support Vector Classifier)
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Training Data**: Enhanced dataset with 405+ diseases and comprehensive symptom patterns
- **Accuracy**: High-precision predictions with SMOTE balancing for improved performance
- **Model Persistence**: Serialized using joblib for optimal ML model storage

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

## 📊 Enhanced Medical Database

### 🔍 Disease Coverage
- **405+ Diseases**: Comprehensive coverage with enhanced medical data
- **Evidence-Based Information**: Web-researched medical recommendations
- **Symptom Mapping**: Detailed symptom-disease relationships
- **Severity Classifications**: Symptom severity and urgency indicators

### 💊 Medical Recommendations
- **Medications**: Pharmaceutical recommendations with dosage information
- **Precautions**: Detailed safety guidelines and preventive measures
- **Exercise**: Therapeutic workouts and physical rehabilitation
- **Nutrition**: Dietary plans and nutritional therapy suggestions

## 🚀 Model Performance

- **🤖 Algorithm**: LinearSVC with TF-IDF vectorization for optimal text processing
- **🎯 Training**: Enhanced dataset with SMOTE balancing for improved accuracy
- **📊 Coverage**: 405+ diseases with comprehensive symptom patterns
- **⚡ Performance**: Fast prediction with joblib serialization
- **🔄 Preprocessing**: Advanced text processing with symptom normalization

## ⚠️ Important Disclaimer

**🏥 Medical Advisory**: This system is designed for educational and informational purposes only. It should **never** be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns and before making any healthcare decisions.

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- 🔬 **Medical Data**: Additional disease information and symptom mappings
- 🎨 **UI/UX**: Interface improvements and accessibility features
- 🤖 **ML Models**: Algorithm enhancements and accuracy improvements
- 📱 **Mobile**: React Native or Flutter mobile applications
- 🔌 **APIs**: RESTful API development for third-party integration

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Astitva Garg** - Created and maintained with ❤️

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

## 🔗 Quick Links

- 🌟 **Star this repository** if you found it helpful!
- 🐛 **Report issues** via GitHub Issues
- 💡 **Feature requests** welcome via Pull Requests
- 📧 **Contact**: Available through GitHub profile

---

**Data Source**: Enhanced CSV datasets with comprehensive medical information
**ML Model**: LinearSVC with TF-IDF (disease_model.joblib) trained on symptom-disease mappings
**Framework**: Flask 2.3.2 with Bootstrap 5.3.1 frontend