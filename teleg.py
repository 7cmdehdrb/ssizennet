import telegram
import os

my_token = os.environ.get("TELEGRAM_TOKEN")
bot = telegram.Bot(token=my_token)
normal_id = os.environ.get("NORMAL_ID")
admin_id = os.environ.get("ADMIN_ID")


def send_text(content):
    bot.sendMessage(chat_id=normal_id, text=content)


def send_admin(content):
    bot.sendMessage(chat_id=admin_id, text=content)

