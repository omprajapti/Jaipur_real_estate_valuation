import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Jaipur AI Property Valuator", layout="centered")

@st.cache_resource
def load_model():
    # If the model file doesn't exist in the cloud server yet, train it on the spot!
    if not os.path.exists("model.pkl"):
        st.info("⚙️ Model file not found in the cloud server environment. Running training pipeline automatically...")
        try:
            import train_model
            train_model.train_valuation_model() # This generates model.pkl right inside the server container
            st.success("✅ Training complete! Model loaded successfully.")
        except Exception as e:
            st.error(f"Failed to auto-train model: {e}")
            return None
            
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None

model = load_model()

# Header updated for Jaipur
st.title("🏡 Intelligent Property Valuation System — Jaipur")
st.write("Enter the property specifications below to estimate the fair market price in Jaipur.")
st.markdown("---")

if model is None:
    st.error("❌ Error: `model.pkl` not found! Please run `train_model.py` first to train and save the machine learning model.")
else:
    st.subheader("📋 Property Specifications")
    col1, col2 = st.columns(2)
    
    with col1:
        # Localities updated to match Jaipur dataset exactly
        locality = st.selectbox(
            "Select Locality",
            ["Malviya Nagar", "Vaishali Nagar", "Mansarovar", "Jagatpura", "C-Scheme", "Tonk Road"]
        )
        area_sqft = st.number_input("Total Area (in Sq. Ft.)", min_value=300, max_value=5000, value=1200, step=50)
        
    with col2:
        bhk_count = st.slider("Number of BHK (Bedrooms)", min_value=1, max_value=4, value=2)
        baths = st.slider("Number of Bathrooms", min_value=1, max_value=4, value=2)
        
    property_age = st.selectbox(
        "Age of the Property",
        ["Brand New", "1-3 Years", "5 Years Old", "10+ Years", "Unknown"]
    )

    st.markdown("---")

    if st.button("Calculate Estimated Valuation", type="primary"):
        input_data = pd.DataFrame([{
            'locality': locality,
            'area_sqft': float(area_sqft),
            'bhk_count': float(bhk_count),
            'baths': float(baths),
            'property_age': property_age
        }])
        
        try:
            prediction = model.predict(input_data)[0]
            
            st.subheader("📊 Estimated Market Value:")
            if prediction >= 10_000_000:
                formatted_price = f"₹ {prediction / 10_000_000:.2f} Crore"
            else:
                formatted_price = f"₹ {prediction / 100_000:.2f} Lakh"
                
            st.success(f"### {formatted_price}")
            st.caption("Note: This estimation is powered by an XGBoost Machine Learning pipeline based on localized historical trends.")
            
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")