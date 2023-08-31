from telegram import Update
from telegram.ext import ContextTypes
import requests



class Commands:
    async def helpCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("""
/start - Начать диалог
/help - Возможные комманды
/train - Обучить модель
        """)

    async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("""
Добро пожаловать в TinkoffSupportAI!
Как я вам могу помочь?
        """)

    async def trainCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Загрузка, пожалуйста, соблюдайте терпение, спасибо...")
        serverUrl = "http://0.0.0.0:5000/train"
        response = requests.get(serverUrl)
        if response.status_code == 200:
            await update.message.reply_text("Обучение прошло успешно!")
        else:
            await update.message.reply_text("Ошибка при обучении, попробуйте позже...")