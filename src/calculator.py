import pandas as pd
from ta.momentum import RSIIndicator
from pybit.unified_trading import HTTP
import time
from logger_config import setup_logging
setup_logging()
import logging

# 1h -> 3600000 ms

TIME = 18 # in hours at least 15 to have enough data for RSI calculation

session = HTTP(testnet=True)

# fetches spot K-line data for SOL/USDT pair
def fetch_spot_data(symbol="SOLUSDT", interval="60"):
    '''Fetches spot K-line data for the given symbol and interval. Returns the close values.'''
    try:
        hours = 3600000 * TIME
        response = session.get_kline(category="linear",
                                     symbol=symbol,
                                     interval=interval,
                                     start=int(time.time() * 1000) - hours,
                                     end=int(time.time() * 1000),
                                     limit=200)
        
        if response != None and 'ret_msg' in response:
            logging.error(f"An error occurred while fetching spot data: {response['ret_msg']}")
            return None

        response_df = pd.DataFrame(response['result']['list'])
        response_df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover']
        response_df = response_df.astype(float)
        close_values_data = response_df.sort_values(by='timestamp') # sort the data by timestamp to get the correct order for RSI calculation
        
        logging.info(f"Data fetched successfully. Latest close value: {close_values_data['close'].iloc[-1]}")

        return close_values_data['close']
    
    except Exception as e:
        logging.error(f"An error occurred while fetching spot data: {e}")

# calculate RSI for spot data
def fetch_spot_rsi(symbol="SOLUSDT", interval="60"):
    '''Calculates the RSI for the given symbol and interval. Returns the latest RSI value.'''
    try:
        close_prices = fetch_spot_data(symbol=symbol, interval=interval)
        if close_prices is None:
            logging.error("An error occurred while fetching spot data.")
            return None
        
        rsi = RSIIndicator(close=close_prices, window=15, fillna=True)
        close_prices['rsi'] = rsi.rsi()

        logging.info(f"Latest RSI value: {close_prices['rsi'].iloc[-1]}")

        return close_prices['rsi'].iloc[-1] # return the latest RSI value
    
    except Exception as e:
        logging.error(f"An error occurred while calculating RSI: {e}") 

fetch_spot_rsi()
