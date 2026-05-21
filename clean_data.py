import pandas as pd
import numpy as np

RAW_DATA_PATH = "raw_real_estate_data.csv"
CLEAN_DATA_PATH = "cleaned_real_estate_data.csv"

def clean_real_estate_data():
    print("🚀 Starting Data Cleaning Pipeline...")
    
    # NEW FIXED CODE
    import os
    
    # 1. Load the raw dataset
    if not os.path.exists(RAW_DATA_PATH):
        print(f"❌ Error: {RAW_DATA_PATH} not found. Run generate_data.py first!")
        return
            
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"📋 Loaded {len(df)} raw rows.")

    # 2. Standardize Text Formatting (Localities)
    # Fix casing issues (e.g., 'hsr layout', 'HSR LAYOUT' -> 'HSR Layout')
    df['locality'] = df['locality'].str.strip().str.title()

    # 3. Handle the Target Variable: Raw Price
    print("🧹 Parsing raw price strings...")
    # Drop rows where price is completely missing or 'Price on Request'
    df = df[df['price_raw'].notna()]
    df = df[df['price_raw'] != "Price on Request"]
    
    def parse_price(price_str):
        if pd.isna(price_str):
            return np.nan
        
        # Remove currency symbol and spaces
        cleaned = str(price_str).replace('₹', '').strip()
        
        try:
            if 'Cr' in cleaned:
                val = float(cleaned.replace('Cr', '').strip())
                return val * 10_000_000  # Convert Crore to raw numeric value
            elif 'Lakh' in cleaned:
                val = float(cleaned.replace('Lakh', '').strip())
                return val * 100_000     # Convert Lakh to raw numeric value
            return float(cleaned)
        except ValueError:
            return np.nan

    df['price'] = df['price_raw'].apply(parse_price)
    # Drop any records that failed price conversion
    df = df.dropna(subset=['price'])

    # 4. Clean Area / Square Footage Column
    print("📐 Standardizing area and units...")
    def parse_area(area_str):
        if pd.isna(area_str):
            return np.nan
        cleaned = str(area_str).lower()
        
        try:
            if 'sqft' in cleaned:
                return float(cleaned.replace('sqft', '').strip())
            elif 'sq. yards' in cleaned:
                # 1 Sq Yard = 9 Sq Feet (Standard conversion)
                yards = float(cleaned.replace('sq. yards', '').strip())
                return yards * 9
            # Extract numbers if formatting differs slightly
            return float(''.join(c for c in cleaned if c.isdigit() or c == '.'))
        except ValueError:
            return np.nan

    df['area_sqft'] = df['area_sqft'].apply(parse_area)
    df = df.dropna(subset=['area_sqft'])

    # 5. Clean BHK Count
    # Extract only the numerical value from strings like "3 BHK" or "2 Bedroom"
    df['bhk_count'] = df['bhk_count'].astype(str).str.extract(r'(\d+)').astype(float)
    df = df.dropna(subset=['bhk_count'])

    # 6. Handle Missing Values in Bathrooms (Imputation)
    print("🔧 Handling missing values for bathroom counts...")
    # Convert baths to numeric, forcing errors to NaN
    df['baths'] = pd.to_numeric(df['baths'], errors='coerce')
    
    # Impute missing bathroom counts using the median count for that specific BHK group
    # E.g., if a 3 BHK is missing a bathroom count, give it the median of other 3 BHKs
    df['baths'] = df.groupby('bhk_count')['baths'].transform(lambda x: x.fillna(x.median()))
    
    # If any outliers remain unfilled, fall back to overall median
    df['baths'] = df['baths'].fillna(df['baths'].median())

    # 7. Standardize Categorical Column: Property Age
    df['property_age'] = df['property_age'].fillna('Unknown').str.strip()

    # 8. Drop the old raw columns that we converted
    df = df.drop(columns=['property_title', 'price_raw'])

    # 9. Save Clean Data to CSV
    df.to_csv(CLEAN_DATA_PATH, index=False)
    print(f"✨ Success! Saved {len(df)} perfectly clean rows to '{CLEAN_DATA_PATH}'.")

if __name__ == "__main__":
    clean_real_estate_data()