import hmac
import hashlib
import time
import requests
import urllib.parse
import logging

class BinanceTestnetClient:
    def __init__(self, api_key: str, api_secret: str):
        # Correct Binance Futures Testnet base URL
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = api_key
        self.api_secret = api_secret
        self.logger = logging.getLogger("TradingBotLogger")

    def _generate_signature(self, query_string: str) -> str:
        """Generate HMAC SHA256 signature for secure Binance API requests."""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def send_signed_request(self, http_method: str, endpoint: str, payload: dict = None):
        """Send a signed request to Binance Futures Testnet API."""
        if payload is None:
            payload = {}

        # Add timestamp required by Binance
        payload['timestamp'] = int(time.time() * 1000)
        
        query_string = urllib.parse.urlencode(payload)
        signature = self._generate_signature(query_string)
        
        # Append signature to query string
        query_string += f"&signature={signature}"
        
        url = f"{self.base_url}{endpoint}?{query_string}"
        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        self.logger.info(f"Sending {http_method} request to {endpoint} with payload: {payload}")

        try:
            if http_method == 'POST':
                response = requests.post(url, headers=headers)
            elif http_method == 'GET':
                response = requests.get(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {http_method}")

            data = response.json()
            if response.status_code != 200:
                self.logger.error(f"API Error: {data}")
                raise Exception(f"Binance API Error: {data}")

            self.logger.info(f"API Response: {data}")
            return data

        except Exception as e:
            self.logger.error(f"Network or execution error: {str(e)}")
            raise e