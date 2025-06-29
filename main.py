import configparser
from binance.spot import Spot
import datetime

# Load API keys from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

api_key = config["keys"]["api_key"]
api_secret = config["keys"]["api_secret"]
url = config["urls"]["url"]  

# Initialize Binance Spot client
client = Spot(api_key=api_key, api_secret=api_secret, base_url=url)

def get_earliest_data(symbol, interval):
    try:
        # Get the first available kline
        klines = client.klines(
            symbol=symbol,
            interval=interval,
            limit=1,
            startTime=0  # Earliest possible time
        )
        
        if klines:
            oldest_timestamp = klines[0][0]
            oldest_date = datetime.datetime.utcfromtimestamp(oldest_timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
            return oldest_date
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Example usage
symbol = "BTCUSDT"
interval = "1d"  # Daily candles
earliest_date = get_earliest_data(symbol, interval)

if earliest_date:
    print(f"Earliest data for {symbol}: {earliest_date}")
else:
    print(f"No historical data found for {symbol}")
