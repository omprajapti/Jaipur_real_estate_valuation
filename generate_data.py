import csv
import random
import os

NUM_PROPERTIES = 500
OUTPUT_FILE = "raw_real_estate_data.csv"

# Jaipur prominent residential localities with realistic baseline price multipliers (per sq ft)
LOCALITIES = {
    "Malviya Nagar": 7500,
    "Vaishali Nagar": 6000,
    "Mansarovar": 5200,
    "Jagatpura": 4200,
    "C-Scheme": 12000,   # Premium high-end zone
    "Tonk Road": 5800
}

def generate_raw_data():
    print(f"Generating {NUM_PROPERTIES} raw, messy real estate records for Jaipur...")
    
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["property_title", "locality", "area_sqft", "bhk_count", "baths", "property_age", "price_raw"])
        
        for i in range(NUM_PROPERTIES):
            locality = random.choice(list(LOCALITIES.keys()))
            base_rate = LOCALITIES[locality]
            
            bhk = random.choice([1, 2, 3, 4])
            if bhk == 1:
                sqft = random.randint(450, 700)
                baths = "1"
            elif bhk == 2:
                sqft = random.randint(800, 1200)
                baths = random.choice(["2", "2", "1"])
            elif bhk == 3:
                sqft = random.randint(1400, 1800)
                baths = random.choice(["3", "3", "2"])
            else: 
                sqft = random.randint(2200, 3500)
                baths = random.choice(["4", "4", "3"])
                
            age = random.choice(["Brand New", "1-3 Years", "5 Years Old", "10+ Years", "Unknown"])
            
            market_variance = random.uniform(0.85, 1.15)
            calculated_price = sqft * base_rate * market_variance
            
            if age == "Brand New":
                calculated_price *= 1.08
            elif age == "10+ Years":
                calculated_price *= 0.82
                
            if random.random() < 0.02: 
                price_str = "Price on Request"
            elif calculated_price >= 10000000: 
                price_str = f"₹ {calculated_price / 10000000:.2f} Cr"
            else:
                price_str = f"₹ {calculated_price / 100000:.1f} Lakh"
                
            area_str = f"{sqft} sqft" if random.random() > 0.1 else f"{sqft} Sq. Yards"
            bhk_str = f"{bhk} BHK" if random.random() > 0.05 else f"{bhk} Bedroom"
            
            if random.random() < 0.05:
                baths = ""
            if random.random() < 0.04:
                locality = locality.upper() if random.random() > 0.5 else locality.lower()
                
            title_str = f"{bhk_str} Apartment for sale in {locality}"
            writer.writerow([title_str, locality, area_str, bhk_str, baths, age, price_str])
            
    print(f"Success! '{OUTPUT_FILE}' has been updated with Jaipur records.")

if __name__ == "__main__":
    generate_raw_data()