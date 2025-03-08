from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from nsetools import Nse
from nsepython import nse_eq, nse_fno, nse_index, nsetools_get_quote
import yfinance as yf
import pandas as pd
import os
import ssl
import certifi
import upstox_client



ssl._create_default_https_context = ssl._create_unverified_context

# Replace with your actual bot token
TELEGRAM_BOT_TOKEN = "8186936471:AAFL6SS_8jziIeB_KJ81ASo8527gYhKfJK4"

# Function to fetch stock data and calculate 200 EMA
def get_ema(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    #df = stock.history(period="1y")
    df = stock.history(interval="15m")  # 60 days of 15-min data


    if df.empty:
        return "No data found for this stock."

    df["EMA_100"] = df["Close"].ewm(span=100, adjust=False).mean()
    df["EMA_200"] = df["Close"].ewm(span=200, adjust=False).mean()

    latest_ema_100 = df["EMA_100"].iloc[-1]
    latest_ema_200 = df["EMA_200"].iloc[-1]

    return round(latest_ema_100, 2), round(latest_ema_200, 2)

# Command handler for Nifty 50
async def nifty(update: Update, context: CallbackContext):
    ema_100, ema_200 = get_ema("^NSEI")
    await update.message.reply_text(f"Nifty 50 - 100 EMA: {ema_100}, 200 EMA: {ema_200}")

# Command handler for Bank Nifty
async def bank_nifty(update: Update, context: CallbackContext):
    ema_100, ema_200 = get_ema("^NSEBANK")
    await update.message.reply_text(f"Bank Nifty - 100 EMA: {ema_100}, 200 EMA: {ema_200}")


# Command handler for Nifty 50
async def nifty(update: Update, context: CallbackContext):
    ema = get_ema("^NSEI")
    await update.message.reply_text(f"Nifty 50 - 200 EMA: {ema}")

# Command handler for Bank Nifty
async def bank_nifty(update: Update, context: CallbackContext):
    ema = get_ema("^NSEBANK")
    await update.message.reply_text(f"Bank Nifty - 200 EMA: {ema}")

#nse = Nse()
#all_stocks = nse.get_stock_codes()

#print(all_stocks)  # List of all NSE stocks

# Setup Telegram bot
#print("Upstox API is installed successfully!")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("nifty", nifty))
    app.add_handler(CommandHandler("banknifty", bank_nifty))

    print("Bot is running...")
    app.run_polling()




if __name__ == "__main__":
    main()
