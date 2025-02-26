from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import yfinance as yf
import pandas as pd

# Replace with your actual bot token
TELEGRAM_BOT_TOKEN = "8186936471:AAFL6SS_8jziIeB_KJ81ASo8527gYhKfJK4"

# Function to fetch stock data and calculate 200 EMA
def get_ema(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    df = stock.history(period="1y")

    if df.empty:
        return "No data found for this stock."

    df["EMA_200"] = df["Close"].ewm(span=200, adjust=False).mean()
    latest_ema = df["EMA_200"].iloc[-1]
    return round(latest_ema, 2)

# Command handler for Nifty 50
async def nifty(update: Update, context: CallbackContext):
    ema = get_ema("^NSEI")
    await update.message.reply_text(f"Nifty 50 - 200 EMA: {ema}")

# Command handler for Bank Nifty
async def bank_nifty(update: Update, context: CallbackContext):
    ema = get_ema("^NSEBANK")
    await update.message.reply_text(f"Bank Nifty - 200 EMA: {ema}")

# Setup Telegram bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("nifty", nifty))
    app.add_handler(CommandHandler("banknifty", bank_nifty))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
