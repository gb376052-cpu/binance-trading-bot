import logging

class OrderManager:
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger("TradingBotLogger")

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        """Place a Market or Limit order on Binance Futures Testnet."""
        endpoint = "/fapi/v1/order"
        
        payload = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }

        if order_type == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders.")
            payload["price"] = price
            payload["timeInForce"] = "GTC"  # Good Till Cancelled is mandatory for limit orders on Binance

        self.logger.info(f"Preparing to place {order_type} {side} order for {quantity} {symbol}")
        
        try:
            response = self.client.send_signed_request("POST", endpoint, payload)
            return response
        except Exception as e:
            self.logger.error(f"Failed to place order: {str(e)}")
            raise e