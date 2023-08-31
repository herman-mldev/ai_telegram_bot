from typing import Final
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from security.tokenManager import TokenManager
from commands.commands import Commands
from handlers.handlers import Handlers
from handlers.Errors.errors import Errors


class MainModule:
    def __init__(self):
        self.TOKEN_PATH: Final = "./security/token.txt"
        self.BOT_USERNAME: Final = "@ai_for_tinkoff_bot"

        self.tokenManager = TokenManager()


    def runBot(self):
        TOKEN = self.tokenManager.parseToken(self.TOKEN_PATH)
        if TOKEN is None:
            raise f"Token is {TOKEN}, provide a file with the token..."
        
        print("Bot has been started...")
        handlers = Handlers(self.BOT_USERNAME)
        
        app = Application.builder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", Commands.startCommand))
        app.add_handler(CommandHandler("help", Commands.helpCommand))
        app.add_handler(CommandHandler("train", Commands.trainCommand))

        app.add_handler(MessageHandler(filters.TEXT, handlers.handleMessage))

        app.add_error_handler(Errors.error)
        print("Polling...")
        app.run_polling(poll_interval=3)


if __name__ == "__main__":
    mainModule = MainModule()
    mainModule.runBot()