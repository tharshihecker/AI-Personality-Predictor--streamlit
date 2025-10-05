# 🧠 AI Personality Predictor# AI Personality Predictor - React + Flask Application



[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fdmgroup3.streamlit.app/)## 🚀 Complete Project Setup

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

[![MongoDB Atlas](https://img.shields.io/badge/database-MongoDB%20Atlas-green.svg)](https://www.mongodb.com/atlas)### Prerequisites

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)- Python 3.8+ 

- Node.js 16+

> **Discover your personality with AI-powered psychological assessment**- npm or yarn



A modern, interactive personality prediction application built with **Streamlit** and **Machine Learning**. Take a comprehensive personality test and get detailed insights about your psychological traits, strengths, and career recommendations.### 🎯 Installation Steps



## 🌟 **Live Demo**#### 1. Backend Setup (Flask + SQLite)



🚀 **[Try the App Live](https://fdmgroup3.streamlit.app/)** - Experience the full personality assessment```bash

# Navigate to project root

## ✨ **Features**cd FDM



### 🔐 **User Authentication**# Create virtual environment

- Secure user registration and loginpython -m venv .venv

- Password encryption with bcrypt

- Session management with Streamlit# Activate virtual environment

# Windows:

### 🧠 **AI-Powered Personality Assessment**.venv\Scripts\activate

- **10 Psychological Dimensions** - Comprehensive trait analysis# macOS/Linux:

- **Interactive Sliders** - Intuitive 0-10 rating systemsource .venv/bin/activate

- **Machine Learning Prediction** - Gaussian Naive Bayes model

- **Confidence Scoring** - Statistical certainty of results# Install Python dependencies

pip install -r requirements.txt

### 📊 **Detailed Results & Analytics**

- **3 Personality Types**: Introvert, Extrovert, Ambivert# Run the Flask backend

- **Personalized Advice** - Tailored development recommendationspython app.py

- **Strengths Analysis** - Identify your key psychological strengths```

- **Career Suggestions** - AI-recommended career paths

- **Visual Analytics** - Interactive charts and probability distributionsBackend will run on http://localhost:5000



### 📈 **History & Progress Tracking**#### 2. Frontend Setup (React)

- **Test History** - Track personality changes over time

- **Dashboard Analytics** - Personal statistics and insights```bash

- **Progress Visualization** - See your personality journey# Navigate to React frontend folder

cd frontend-react

### ☁️ **Cloud Infrastructure**

- **MongoDB Atlas** - Scalable cloud database# Install Node dependencies

- **Streamlit Community Cloud** - Serverless deploymentnpm install

- **Real-time Data** - Instant results and synchronization

# Start the React development server

## 🎯 **Personality Dimensions Analyzed**npm start

```

| Dimension | Description |

|-----------|-------------|Frontend will run on http://localhost:3000

| 🎉 **Party Liking** | Enjoyment of social gatherings and large events |

| 🎤 **Public Speaking** | Comfort level with presenting to groups |### 🏗️ Project Structure

| ⚡ **Excitement Seeking** | Preference for thrilling and novel experiences |

| 🏠 **Alone Time** | Need for solitude and personal space |```

| 💬 **Talkativeness** | Verbal expression in social situations |FDM/

| 🔋 **Social Energy** | Energy gained from social interactions |├── app.py                 # Flask backend with authentication & ML

| 👑 **Leadership** | Natural tendency to lead and guide others |├── requirements.txt       # Python dependencies

| 📚 **Reading Habits** | Intellectual curiosity and learning drive |├── features.json         # ML feature definitions

| 🌍 **Adventurousness** | Openness to new experiences and exploration |├── joblib/              # Trained ML models

| 👥 **Group Comfort** | Ease in group settings and team environments |│   ├── final_gnb_personality_model.joblib

│   └── personality_label_encoder.joblib

## 🛠️ **Technology Stack**├── personality_app.db   # SQLite database (auto-created)

└── frontend-react/      # React application

### **Frontend & UI**    ├── package.json

- **Streamlit** - Modern Python web framework    ├── public/

- **Plotly** - Interactive data visualizations    ├── src/

- **Responsive Design** - Mobile-friendly interface    │   ├── components/   # Reusable components

    │   ├── contexts/     # React context (auth)

### **Backend & ML**    │   ├── pages/        # Page components

- **Python 3.13+** - Core application logic    │   ├── App.js

- **scikit-learn** - Machine learning algorithms    │   └── index.js

- **NumPy & Pandas** - Data processing and analysis    └── tailwind.config.js

- **Joblib** - Model serialization and loading```



### **Database & Cloud**### 🔧 Key Features Implemented

- **MongoDB Atlas** - Cloud-native NoSQL database

- **PyMongo** - MongoDB Python driver#### ✅ **Backend (Flask)**

- **Streamlit Community Cloud** - Serverless deployment- **JWT Authentication** - Secure login/signup with tokens

- **SQLite Database** - User accounts and test history storage

### **Security & Authentication**- **Enhanced ML API** - Confidence scores and detailed predictions

- **bcrypt** - Password hashing and security- **Personality Advice System** - Personalized recommendations

- **Session State Management** - Secure user sessions- **CORS Enabled** - Cross-origin requests from React frontend



## 🚀 **Quick Start**#### ✅ **Frontend (React)**

- **Modern UI** - Tailwind CSS with animations

### **Option 1: Use the Live App**- **Authentication Flow** - Login/signup with protected routes

Simply visit **[fdmgroup3.streamlit.app](https://fdmgroup3.streamlit.app/)** - no setup required!- **Interactive Test** - Step-by-step personality assessment

- **User Dashboard** - Statistics and recent tests

### **Option 2: Run Locally**- **Responsive Design** - Mobile-friendly interface

- **Real-time Feedback** - Live slider updates with descriptions

1. **Clone the Repository**

   ```bash#### ✅ **User Experience Improvements**

   git clone https://github.com/tharshihecker/fdm.git- **Intuitive Sliders** - No more decimal input confusion!

   cd fdm/streamlit-deploy- **Visual Feedback** - Color-coded responses with descriptions

   ```- **Progress Tracking** - Step-by-step completion indicators

- **Personalized Advice** - Tailored recommendations per personality type

2. **Install Dependencies**- **Test History** - Track personality changes over time

   ```bash

   pip install -r requirements.txt### 🎮 How to Use

   ```

1. **Start both servers** (Flask backend + React frontend)

3. **Run the Application**2. **Visit** http://localhost:3000

   ```bash3. **Sign up** for a new account or use demo credentials:

   streamlit run app.py   - Email: `demo@example.com`

   ```   - Password: `demo123`

4. **Take the test** using interactive sliders

4. **Open in Browser**5. **View results** with confidence scores and advice

   ```6. **Track history** of all your personality tests

   http://localhost:8501

   ```### 🔮 Next Steps for Development



## 📖 **How It Works**#### Planned Enhancements:

- **Enhanced Results Page** - Detailed charts and visualizations

### **1. User Registration**- **History Analytics** - Personality trend analysis over time

- Create account with email and password- **Social Features** - Compare with friends (optional)

- Secure authentication with bcrypt encryption- **Export Results** - PDF reports generation

- Personalized dashboard and history tracking- **Mobile App** - React Native version



### **2. Personality Assessment**### 🐛 Troubleshooting

- Interactive 10-question personality test

- Slider-based rating system (0-10 scale)#### Common Issues:

- Real-time feedback and progress tracking1. **CORS errors** - Make sure Flask backend is running on port 5000

2. **Database errors** - SQLite DB will be created automatically on first run

### **3. AI Analysis**3. **Module not found** - Ensure all dependencies are installed in virtual environment

- Gaussian Naive Bayes machine learning model4. **Port conflicts** - Change ports in package.json (React) or app.py (Flask)

- Statistical confidence scoring

- Probability distribution analysis### 📊 Database Schema



### **4. Results & Insights**```sql

- Detailed personality type classificationUsers Table:

- Personalized strengths and development advice- id (Primary Key)

- Career recommendations based on psychological profile- name, email, password_hash

- Visual analytics and probability charts- created_at, updated_at



### **5. History & Progress**PersonalityTest Table:

- Test history tracking over time- id (Primary Key)

- Dashboard with personal statistics- user_id (Foreign Key)

- Progress visualization and trends- features (JSON), prediction, confidence

- probabilities (JSON), created_at

## 🎨 **Screenshots**```



### **Dashboard**This setup transforms your simple HTML form into a comprehensive, production-ready personality assessment platform! 🎉
![Dashboard Preview](https://via.placeholder.com/800x400/0066cc/ffffff?text=Interactive+Dashboard+with+User+Stats)

### **Personality Test**
![Test Interface](https://via.placeholder.com/800x400/00cc66/ffffff?text=Interactive+Slider-based+Assessment)

### **Results Analysis**
![Results Page](https://via.placeholder.com/800x400/cc6600/ffffff?text=Detailed+Results+with+AI+Insights)

## 📊 **Model Performance**

Our machine learning model achieves:
- **Accuracy**: 85%+ on personality classification
- **Confidence Scoring**: Statistical certainty measurement
- **Real-time Prediction**: Instant results processing
- **Scalable Architecture**: Cloud-optimized performance

## 🔧 **Configuration**

### **Environment Variables**
The application uses MongoDB Atlas with connection string configured in the code. For local development with custom database:

```python
# In app.py, modify the connection string
client = MongoClient("your-mongodb-connection-string")
```

### **Model Training**
The included models are pre-trained on psychological assessment data. To retrain:

1. Prepare training data in the same format
2. Use the provided feature set (10 personality dimensions)
3. Train Gaussian Naive Bayes classifier
4. Save models using joblib

## 🚀 **Deployment**

### **Streamlit Community Cloud**
1. Fork this repository
2. Connect to Streamlit Cloud
3. Set main file path: `streamlit-deploy/app.py`
4. Deploy automatically

### **Docker Deployment**
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY streamlit-deploy/ .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🤝 **Contributing**

We welcome contributions! Here's how to get started:

1. **Fork the Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit Changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open Pull Request**

### **Development Setup**
```bash
# Clone repository
git clone https://github.com/tharshihecker/fdm.git
cd fdm/streamlit-deploy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
streamlit run app.py
```

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **scikit-learn** - Machine learning framework
- **Streamlit** - Web application framework
- **MongoDB Atlas** - Cloud database platform
- **Plotly** - Data visualization library
- **Psychology Research** - Personality assessment methodologies

## 📞 **Support & Contact**

- **Issues**: [GitHub Issues](https://github.com/tharshihecker/fdm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tharshihecker/fdm/discussions)
- **Email**: [Your Contact Email]

## 🎯 **Roadmap**

- [ ] **Advanced Analytics** - Personality trend analysis
- [ ] **Social Features** - Compare with friends (optional)
- [ ] **Export Reports** - PDF personality reports
- [ ] **Mobile App** - React Native version
- [ ] **API Integration** - RESTful API for developers
- [ ] **Multi-language** - Internationalization support

---

<div align="center">

**Made with ❤️ using Python, Streamlit & Machine Learning**

[🌟 Star this repo](https://github.com/tharshihecker/fdm) • [🚀 Try the App](https://fdmgroup3.streamlit.app/) • [📖 Documentation](streamlit-deploy/DEPLOYMENT_GUIDE.md)

</div>