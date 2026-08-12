class InputValidator:
    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """Validate trading symbol (e.g., BTCUSDT)."""
        if not symbol or not symbol.isalnum():
            raise ValueError("Invalid symbol. Example: BTCUSDT")
        return symbol.upper()

    @staticmethod
    def validate_side(side: str) -> str:
        """Validate order side (BUY or SELL)."""
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Invalid side. Must be either BUY or SELL.")
        return side

    @staticmethod
    def validate_order_type(order_type: str) -> str:
        """Validate order type (MARKET or LIMIT)."""
        order_type = order_type.upper()
        if order_type not in ["MARKET", "LIMIT"]:
            raise ValueError("Invalid order type. Must be either MARKET or LIMIT.")
        return order_type

    @staticmethod
    def validate_quantity(quantity) -> float:
        """Validate order quantity."""
        try:
            qty = float(quantity)
            if qty <= 0:
                raise ValueError
            return qty
        except ValueError:
            raise ValueError("Invalid quantity. Must be a positive number.")

    @staticmethod
    def validate_price(order_type: str, price=None) -> float:
        """Validate price (mandatory for LIMIT orders)."""
        if order_type == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders.")
            try:
                prc = float(price)
                if prc <= 0:
                    raise ValueError
                return prc
            except ValueError:
                raise ValueError("Invalid price. Must be a positive number.")
        return price