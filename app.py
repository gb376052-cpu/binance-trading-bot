import streamlit as st
import os
from bot.client import BinanceTestnetClient
from bot.orders import OrderManager
from bot.validators import InputValidator

st.set_page_config(page_title="Binance Mobile Trading Bot", page_icon="📈", layout="centered")

st.title("📈 Binance Futures Testnet Trading Bot")
st.write("Apne mobile phone ya laptop se kahin bhi trades execute karein!")

with st.form("trading_form"):
    st.subheader("🔑 API Credentials")
    api_key = st.text_input("Binance API Key", type="password", value=os.getenv("BINANCE_API_KEY", ""))
    api_secret = st.text_input("Binance API Secret", type="password", value=os.getenv("BINANCE_API_SECRET", ""))

    st.subheader("📊 Order Details")
    symbol = st.text_input("Symbol", value="BTCUSDT")
    side = st.selectbox("Side", ["BUY", "SELL"])
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
    quantity = st.text_input("Quantity", value="0.01")
    price = st.text_input("Price (Only for LIMIT orders)", value="")

    submitted = st.form_submit_button("🚀 Place Order")

if submitted:
    try:
        if not api_key or not api_secret:
            st.error("Please enter your Binance API Key and Secret!")
        else:
            client = BinanceTestnetClient(api_key, api_secret)
            manager = OrderManager(client)
            
            val_symbol = InputValidator.validate_symbol(symbol)
            val_side = InputValidator.validate_side(side)
            val_type = InputValidator.validate_order_type(order_type)
            val_qty = InputValidator.validate_quantity(quantity)
            val_price = InputValidator.validate_price(val_type, price if price else None)
            
            response = manager.place_order(
                symbol=val_symbol,
                side=val_side,
                order_type=val_type,
                quantity=val_qty,
                price=val_price
            )
            
            st.success("✅ Order Placed Successfully!")
            st.json({
                "Order ID": response.get('orderId'),
                "Symbol": response.get('symbol'),
                "Status": response.get('status'),
                "Side": response.get('side'),
                "Type": response.get('type'),
                "Executed Qty": response.get('executedQty')
            })
            
            st.markdown("[🔗 Open Binance Testnet Dashboard](https://testnet.binancefuture.com)", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")