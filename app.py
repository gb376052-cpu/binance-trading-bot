import streamlit as st
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

# --- Page Configuration ---
st.set_page_config(
    page_title="Binance Futures Testnet Bot",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Binance Futures Testnet Trading Bot")

# --- Sidebar for User API Keys ---
st.sidebar.header("🔑 Binance API Credentials")
user_api_key = st.sidebar.text_input("API Key", type="password")
user_secret_key = st.sidebar.text_input("Secret Key", type="password")

st.sidebar.markdown("---")
st.sidebar.markdown("Don't have keys? Get them from [Binance Futures Testnet](https://testnet.binancefuture.com/)")

BASE_URL = "https://testnet.binancefuture.com"

def send_signed_request(method, path, params=None):
    if params is None:
        params = {}
    
    # Check if user entered keys
    if not user_api_key or not user_secret_key:
        return {"error": "Please enter your Binance API Key and Secret Key in the sidebar!"}

    params['timestamp'] = int(time.time() * 1000)
    query_string = urlencode(params)
    
    signature = hmac.new(
        user_secret_key.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    params['signature'] = signature
    
    headers = {
        'X-MBX-APIKEY': user_api_key
    }
    
    url = f"{BASE_URL}{path}?{urlencode(params)}"
    
    if method == 'POST':
        response = requests.post(url, headers=headers)
    elif method == 'GET':
        response = requests.get(url, headers=headers)
    else:
        return {"error": "Invalid method"}
        
    try:
        return response.json()
    except Exception:
        return {"error": response.text}

# --- UI Form ---
st.subheader("Place an Order")

with st.form("trading_form"):
    symbol = st.text_input("Trading Symbol", value="BTCUSDT").upper()
    side = st.selectbox("Side", ["BUY", "SELL"])
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
    
    quantity = st.number_input("Quantity", min_value=0.001, value=0.001, format="%.3f")
    
    price = 0.0
    if order_type == "LIMIT":
        price = st.number_input("Limit Price", min_value=0.0, value=50000.0, format="%.2f")

    submitted = st.form_submit_button("Execute Order")

    if submitted:
        if not user_api_key or not user_secret_key:
            st.error("⚠️ Please enter your API Key and Secret Key in the sidebar first!")
        elif not symbol:
            st.error("Please enter a valid symbol.")
        else:
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }
            
            if order_type == "LIMIT":
                params["price"] = price
                params["timeInForce"] = "GTC"
                
            with st.spinner("Executing order on Binance Testnet..."):
                result = send_signed_request('POST', '/fapi/v1/order', params)
                
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success("Order Placed Successfully!")
                st.json(result)
