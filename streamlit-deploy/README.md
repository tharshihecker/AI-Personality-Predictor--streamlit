# Personality Test App - Streamlit Version

A comprehensive personality testing application built with Streamlit and MongoDB Atlas.

## Features

- 🧠 **Personality Assessment** - 10-factor personality test with ML prediction
- 👤 **User Authentication** - Secure login/signup with password hashing
- 📊 **Interactive Results** - Beautiful visualizations with Plotly
- 📈 **Test History** - Complete history tracking with statistics
- 🎯 **Personalized Advice** - Career suggestions and development tips
- 🔒 **MongoDB Atlas** - Cloud database integration
- 📱 **Responsive Design** - Works on all devices

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MongoDB Atlas
- **ML Models**: Scikit-learn, Joblib
- **Visualization**: Plotly
- **Authentication**: Bcrypt
- **Deployment**: Streamlit Community Cloud

## Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd personality-test-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - Navigate to `http://localhost:8501`

## File Structure

```
personality-test-app/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies  
├── features.json            # ML feature definitions
├── README.md               # This file
├── DEPLOYMENT_GUIDE.md     # Deployment instructions
└── joblib/
    ├── final_gnb_personality_model.joblib
    └── personality_label_encoder.joblib
```

## Database Schema

### Users Collection
```javascript
{
  "_id": ObjectId,
  "name": "User Name",
  "email": "user@example.com", 
  "password_hash": "bcrypt_hash",
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Personality Tests Collection
```javascript
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "features": {
    "party_liking": 7.5,
    "public_speaking_comfort": 6.2,
    // ... other features
  },
  "prediction": "Extrovert",
  "confidence": 0.85,
  "probabilities": {
    "Extrovert": 0.85,
    "Introvert": 0.10, 
    "Ambivert": 0.05
  },
  "created_at": ISODate
}
```

## App Pages

1. **Authentication** - Login/Signup
2. **Dashboard** - User overview and statistics
3. **Personality Test** - Interactive assessment form
4. **Results** - Detailed analysis and advice
5. **History** - Previous test results
6. **Profile** - User statistics and charts

## Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions on deploying to Streamlit Community Cloud.

## License

This project is licensed under the MIT License.