import telegram
import os

my_token = os.environ.get("TELEGRAM_TOKEN")
bot = telegram.Bot(token=my_token)


def send_text(content):
    bot.sendMessage(chat_id="-1001296760710", text=content)


def send_admin(content):
    bot.sendMessage(chat_id="-1001460896740", text=content)

