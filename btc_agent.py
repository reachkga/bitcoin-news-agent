import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv(override=True)

# Initialize Supabase client
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase = create_client(supabase_url, supabase_key)

def get_and_store_btc_price():
    try:
        # CoinGecko API endpoint for Bitcoin price in USD
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd"
        }
        
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Extract the price from the response
        data = response.json()
        btc_price = data["bitcoin"]["usd"]
        
        # Prepare data for Supabase - using correct column names
        price_data = {
            "price": btc_price,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Insert data into Supabase
        result = supabase.table('btc_price').insert(price_data).execute()
        
        print(f"Current Bitcoin Price: ${btc_price:,.2f} USD")
        print("Price successfully stored in database")
        return btc_price
        
    except requests.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None
    except Exception as e:
        print(f"Error storing data in Supabase: {e}")
        return None

if __name__ == "__main__":
    get_and_store_btc_price() 