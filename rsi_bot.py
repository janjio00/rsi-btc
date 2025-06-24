# rsi_bot.py
import requests
import pandas as pd
import time
from ta.momentum import RSIIndicator
from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_ID, SYMBOL, INTERVAL, LIMIT, THRESHOLD_HIGH, THRESHOLD_LOW

bot = Bot(token=TELEGRAM_TOKEN)

def get_klines(symbol, interval, limit):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'trades', 'taker_base_vol',
        'taker_quote_vol', 'ignore'
    ])
    df['close'] = pd.to_numeric(df['close'])
    return df

def get_rsi(df):
    rsi_indicator = RSIIndicator(close=df['close'], window=14)
    return rsi_indicator.rsi().iloc[-1]

def main():
    last_status = None
    while True:
        try:
            df = get_klines(SYMBOL, INTERVAL, LIMIT)
            rsi = get_rsi(df)
            print(f"RSI attuale: {rsi:.2f}")

            if rsi > THRESHOLD_HIGH and last_status != 'high':
                bot.send_message(chat_id=CHAT_ID, text=f"⚠️ RSI alto ({rsi:.2f}) - BTC/USDT in ipercomprato!")
                last_status = 'high'
            elif rsi < THRESHOLD_LOW and last_status != 'low':
                bot.send_message(chat_id=CHAT_ID, text=f"⚠️ RSI basso ({rsi:.2f}) - BTC/USDT in ipervenduto!")
                last_status = 'low'
            elif THRESHOLD_LOW <= rsi <= THRESHOLD_HIGH:
                last_status = None

            time.sleep(60)

        except Exception as e:
            print("Errore:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()
