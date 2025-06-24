# get_chat_id.py
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from config import TELEGRAM_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"Il tuo chat_id è: {chat_id}")
    await context.bot.send_message(chat_id=chat_id, text=f"✅ Il tuo chat_id è: {chat_id}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
