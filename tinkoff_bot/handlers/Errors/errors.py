from telegram import Update
from telegram.ext import ContextTypes


class Errors:
    def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f"Возникла ошибка: \"{update}\" по причине: \"{context.error}\"")