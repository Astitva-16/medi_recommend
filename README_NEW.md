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
medi_recommend/ (180.54MB, 67 files)
├── 🔧 Core Application
│   ├── main.py                      # Flask web app (259 lines)
│   ├── medicine_rec_train.py        # ML training pipeline (185 lines)
│   ├── medicine_rec_prediction.py   # Prediction module (65 lines)
│   └── requirements.txt             # Dependencies
├── 🧠 AI Models
│   └── disease_model.joblib         # Trained LinearSVC + TF-IDF
├── 🎨 Frontend
│   ├── templates/
│   │   ├── index.html              # Main interface (1,343 lines)
│   │   ├── about.html              # About page
│   │   ├── blog.html               # Blog page
│   │   └── contact.html            # Contact page
│   └── static/
│       ├── css/theme.css           # Custom styling (151 lines)
│       └── symptocare (1).png       # App logo
└── 📊 Enhanced Medical Data
    ├── Diseases_Symptoms.csv       # 405+ diseases (enhanced)
    ├── Training.csv                # ML training dataset
    ├── medications.csv             # Medication database
    ├── precautions_df.csv          # Safety guidelines
    ├── workout_df.csv              # Exercise recommendations
    ├── diets.csv                   # Dietary suggestions
    ├── symtoms_df.csv              # Symptom classifications
    └── description.csv             # Disease descriptions
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

- 📊 **Total Size**: 180.54MB across 67 files
- 🏥 **Disease Coverage**: 405+ diseases with enhanced medical data
- 💻 **Code Statistics**: 
  - Backend: 509 lines (Flask + ML pipeline)
  - Frontend: 1,343 lines (HTML templates)
  - Styling: 151 lines (CSS)
- 🤖 **ML Model**: LinearSVC with TF-IDF vectorization
- 📦 **Dependencies**: 5 core Python packages

## 🔗 Quick Links

- 🌟 **Star this repository** if you found it helpful!
- 🐛 **Report issues** via GitHub Issues
- 💡 **Feature requests** welcome via Pull Requests
- 📧 **Contact**: Available through GitHub profile

---

**🚀 Built with Flask 2.3.2 | 🤖 Powered by scikit-learn 1.3.0 | 🎨 Styled with Bootstrap 5.3.1**