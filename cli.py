import os
import sys
import logging
import argparse
import webbrowser
from dotenv import load_dotenv

# Ensure the current directory is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("[DEBUG] Script execution started...")

try:
    from bot.client import BinanceTestnetClient
    from bot.validators import InputValidator
    from bot.orders import OrderManager
    print("[DEBUG] All bot modules imported successfully.")
except Exception as e:
    print(f"[CRITICAL ERROR] Failed to import modules: {e}")
    sys.exit(1)

# Setup Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/trading.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
logging.getLogger().addHandler(console_handler)

# Load environment variables
load_dotenv()

def main():
    print("[DEBUG] Inside main() function.")
    parser = argparse.ArgumentParser(description="Binance Futures Testnet CLI Trading Bot")
    parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, help="Order side: BUY or SELL")
    parser.add_argument("--type", type=str, required=True, help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", type=str, required=True, help="Order quantity")
    parser.add_argument("--price", type=str, default=None, help="Order price (Required for LIMIT orders)")

    args = parser.parse_args()
    print("[DEBUG] Arguments parsed successfully.")

    print("\n--- Binance Futures Testnet Trading Bot ---")

    try:
        # 1. Validate Inputs
        symbol = InputValidator.validate_symbol(args.symbol)
        side = InputValidator.validate_side(args.side)
        order_type = InputValidator.validate_order_type(args.type)
        quantity = InputValidator.validate_quantity(args.quantity)
        price = InputValidator.validate_price(order_type, args.price)
        print("[DEBUG] Inputs validated successfully.")

        # 2. Get API Credentials from Environment Variables
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            print("[ERROR] API Key or Secret not found! Please set them in a .env file.")
            return

        # 3. Initialize Client and Order Manager
        client = BinanceTestnetClient(api_key, api_secret)
        order_manager = OrderManager(client)

        print(f"Placing {order_type} {side} order for {quantity} {symbol}...")

        # 4. Execute Order
        response = order_manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )

        # 5. Print Clear Output Summary
        print("\n✅ Order Placed Successfully!")
        print("----------------------------------------")
        print(f"Order ID       : {response.get('orderId')}")
        print(f"Symbol         : {response.get('symbol')}")
        print(f"Status         : {response.get('status')}")
        print(f"Side           : {response.get('side')}")
        print(f"Type           : {response.get('type')}")
        print(f"Executed Qty   : {response.get('executedQty')}")
        print(f"Avg Price      : {response.get('avgPrice', price if price else 'Market')}")
        print("----------------------------------------\n")

        # 6. Automatically Open Binance Futures Testnet in Browser
        webbrowser.open("https://testnet.binancefuture.com")
        print("🌐 Opened Binance Futures Testnet in your browser successfully.")

    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}\n")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()