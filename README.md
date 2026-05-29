#  Kenya Real Estate Price Predictor

An end-to-end Machine Learning project that predicts property prices
across Kenya using a Random Forest Regressor.

##  Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/real-estate-price-prediction.git
cd real-estate-price-prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the notebook first to train and save the model
#    Open notebook/Real_Estate_Prediction.ipynb and run all cells

# 4. Start the Flask server
python app.py

# 5. Open client/index.html in your browser
```

##  Test the API (curl)

```bash
curl -X POST http://127.0.0.1:5000/predict_home_price \
  -H "Content-Type: application/json" \
  -d '{
    "bedrooms": 4,
    "property_type": "Villa",
    "location": "Karen",
    "has_gym": 0,
    "en_suite": 1,
    "swimming_pool": 1,
    "has_dsq": 0,
    "has_garden": 1
  }'
```

##  Deploy to Render

1. Push to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo
4. Set **Start Command**: `gunicorn app:app`
5. Set **Build Command**: `pip install -r requirements.txt`
6. Deploy — copy your live URL into `client/index.html` → `const API = 'your-url'`
