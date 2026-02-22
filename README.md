🌍 Carbon Footprint Tracker & AI Predictor

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered web application that calculates, predicts, and provides personalized recommendations to reduce your carbon footprint using Machine Learning.

🎯 Features

✅ Real-time Carbon Calculator - Instant footprint estimation based on lifestyle inputs  
✅ ML-Powered Predictions - 4 trained models (Random Forest, XGBoost, Linear Regression, Decision Tree)  
✅ User Segmentation - K-Means clustering into Low/Medium/High emitter categories  
✅ Personalized Recommendations - Cluster-based actionable tips to reduce emissions  
✅ Interactive Analytics - Beautiful Plotly visualizations and charts  
✅ 5-Year Projections - Visualize future emissions with and without lifestyle changes  


📊 Dataset

- Source: Kaggle - Individual Carbon Footprint Dataset
- Size: 10,000 individual profiles
- Features: 19 lifestyle factors (transport, energy, diet, consumption)
- Target: Annual CO₂ emissions (kg/year)
- Range: 306 - 6,447 kg CO₂ per year


 🤖 Machine Learning Models

| Model | R² Score | RMSE (kg CO₂) |
|-------|----------|---------------|
| Random Forest ⭐ | 0.916 | 291 |
| XGBoost | 0.908 | 304 |
| Decision Tree | 0.874 | 356 |
| Linear Regression | 0.823 | 421 |

Best Model: Random Forest (91.6% accuracy)


🚀 Installation & Setup

Clone Repository
```bash
git clone https://github.com/Sowmya-kc/Carbon_Footprint_Tracker.git
cd Carbon_Footprint_Tracker
```

Install Dependencies
```bash
pip install -r requirements.txt
```

Run the Application

```bash
# Step 1: Clean the data
python clean_data.py

# Step 2: Train ML models (2-3 minutes)
python train_models.py

# Step 3: Launch web app
streamlit run app.py
```

Open browser at `http://localhost:8501` 🎉

---

📱 Application Pages

1. 🏠 Home - Project overview and statistics
2. 🧮 Calculator - Interactive carbon footprint calculator
3. 🤖 AI Prediction - ML model predictions and clustering
4. 📊 Analytics - Interactive charts and visualizations
5. 💡 Recommendations - Personalized tips to reduce emissions

---

📂 Project Structure

```
Carbon_Footprint_Tracker/
├── app.py                      # Main Streamlit app
├── clean_data.py               # Data preprocessing
├── train_models.py             # ML model training
├── requirements.txt            # Dependencies
├── data/                       # Dataset files
├── models/                     # Trained ML models
└── pages/                      # Streamlit pages
    ├── home.py
    ├── calculator.py
    ├── predictions.py
    ├── analytics.py
    └── recommendations.py
```

---

🛠️ Tech Stack

- Python 3.10+
- scikit-learn, XGBoost - Machine Learning
- Pandas, NumPy - Data Processing
- Streamlit - Web Framework
- Plotly - Interactive Visualizations

---

🌱 Future Enhancements

- [ ] User authentication and profile management
- [ ] Historical tracking and progress monitoring
- [ ] Mobile app development
- [ ] PDF report generation
- [ ] Real-time IoT data integration

---

👥 Team

Project developed by a team of 3 members for academic purposes.

---

📝 License

This project is licensed under the MIT License.

---

🙏 Acknowledgments

- Dataset: Kaggle Carbon Footprint Dataset
- Emission Factors: IPCC, IEA
- Framework: Streamlit Community

---

Built with 💚 for a sustainable future 🌍
