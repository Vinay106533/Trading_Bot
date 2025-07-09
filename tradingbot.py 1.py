import logging
from binance.client import Client
from binance.enums import *
import sys

# Setup logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def _init_(self, api_key, api_secret, testnet=True):
        try:
            self.client = Client(api_key, api_secret)
            if testnet:
                self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            logging.info("Client initialized successfully.")
        except Exception as e:
            logging.error(f"Client initialization failed: {e}")
            sys.exit("Error initializing Binance client.")

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == ORDER_TYPE_MARKET:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            elif order_type == ORDER_TYPE_LIMIT:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            else:
                raise ValueError("Unsupported order type")

            logging.info(f"Order placed: {order}")
            return order

        except Exception as e:
            logging.error(f"Order placement failed: {e}")
            return None

def get_user_input():
    print("=== Binance Futures Trading Bot ===")
    symbol = input("Enter trading pair (e.g., BTCUSDT): ").strip().upper()
    side_input = input("Enter side (BUY/SELL): ").strip().upper()
    order_type_input = input("Enter order type (MARKET/LIMIT): ").strip().upper()
    quantity = input("Enter quantity: ").strip()

    price = None
    if order_type_input == "LIMIT":
        price = input("Enter limit price: ").strip()

    # Validate inputs
    try:
        quantity = float(quantity)
        if price:
            price = float(price)
    except ValueError:
        print("Invalid number format.")
        sys.exit(1)

    # Convert enums
    if side_input not in ["BUY", "SELL"]:
        print("Invalid side. Must be BUY or SELL.")
        sys.exit(1)
    if order_type_input not in ["MARKET", "LIMIT"]:
        print("Invalid order type. Must be MARKET or LIMIT.")
        sys.exit(1)

    side_enum = SIDE_BUY if side_input == "BUY" else SIDE_SELL
    order_type_enum = ORDER_TYPE_MARKET if order_type_input == "MARKET" else ORDER_TYPE_LIMIT

    return symbol, side_enum, order_type_enum, quantity, price

if _name_ == "_main_":
    # Replace these with your Testnet credentials
    API_KEY = "your_api_key_here"
    API_SECRET = "your_api_secret_here"

    bot = BasicBot(API_KEY, API_SECRET)

    symbol, side, order_type, quantity, price = get_user_input()

    order = bot.place_order(symbol, side, order_type, quantity, price)

    if order:
        print("✅ Order placed successfully:")
        print(order)
    else:
        print("❌ Order placement failed. Check log for details.")
