import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import pickle
import os

# Define file paths
CLEAN_DATA_PATH = "cleaned_real_estate_data.csv"
MODEL_OUTPUT_PATH = "model.pkl"

def train_valuation_model():
    print("🤖 Starting Machine Learning Training Pipeline...")
    
    # 1. Load the clean dataset
    if not os.path.exists(CLEAN_DATA_PATH):
        print(f"❌ Error: {CLEAN_DATA_PATH} not found. Run clean_data.py first!")
        return
        
    df = pd.read_csv(CLEAN_DATA_PATH)
    print(f"📋 Loaded {len(df)} clean records for training.")
    
    # 2. Separate features (X) and target variable (y)
    # We drop 'property_age' if it has too many 'Unknowns', or keep it. Let's use it!
    X = df[['locality', 'area_sqft', 'bhk_count', 'baths', 'property_age']]
    y = df['price']
    
    # 3. Split into Train and Test sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Handle Categorical Data (Text columns like Locality and Age)
    # Machine learning models need numbers, so we convert text categories into binary columns
    categorical_features = ['locality', 'property_age']
    numeric_features = ['area_sqft', 'bhk_count', 'baths']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # 5. Create an End-to-End Pipeline with XGBoost
    # This bundles the data preprocessing and the model together into a single object
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42))
    ])
    
    # 6. Train the model
    print("🏋️‍♂️ Training XGBoost Regressor...")
    model_pipeline.fit(X_train, y_train)
    
    # 7. Evaluate the model
    y_pred = model_pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("\n📊 Model Performance Metrics:")
    print(f"🔹 Mean Absolute Error (MAE): ₹{mae:,.2f}")
    print(f"   (On average, predictions are off by just ₹{mae:,.2f})")
    print(f"🔹 R-squared (R²) Score: {r2:.2f}")
    print(f"   (The model explains {r2*100:.1f}% of the price variance)")
    
    # 8. Save the trained pipeline to a file
    with open(MODEL_OUTPUT_PATH, 'wb') as f:
        pickle.dump(model_pipeline, f)
    print(f"\n💾 Success! Saved trained model pipeline to '{MODEL_OUTPUT_PATH}'")

if __name__ == "__main__":
    train_valuation_model()