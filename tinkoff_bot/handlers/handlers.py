from telegram import Update
from telegram.ext import ContextTypes
import requests


class Handlers:
    def __init__(self, BOT_USERNAME: str):
        self.BOT_USERNAME = BOT_USERNAME
        
        
    async def handleResponse(self, text: str) -> str:
        processed: str = text.lower()
    
        if "привет" in processed:
            return "Здравствуйте, нам очень приятно, что вы выбрали именно Tinkoff, поверьте - мы вас не подведем, даже в столь тяжелые времена!"
        elif "добрый день" in processed:
            return "Здравствуйте, нам очень приятно, что вы выбрали именно Tinkoff, поверьте - мы вас не подведем, даже в столь тяжелые времена!"
        else:
            modelResponse = await self.dilevery(processed)
            return modelResponse


    async def handleMessage(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        messageType: str = update.message.chat.type
        text: str = update.message.text

        print(f"User ({update.message.chat.id}) in {messageType}: \"{text}\"")

        if messageType == "group":
            if self.BOT_USERNAME in text:
                newText: str = text.replace(self.BOT_USERNAME, "").strip()
                response: str = await self.handleResponse(newText)
        else:
            response: str = await self.handleResponse(text)

        if response is not None:
            print("Bot:", response)
            await update.message.reply_text(response)


    async def dilevery(self, message):
        serverUrl = "http://0.0.0.0:5000/delivery"
        payload = {"message": message}

        response = requests.post(serverUrl, json=payload)
        if response.status_code == 200:
            return response.json().get("response")
        else:
            return "Server error"