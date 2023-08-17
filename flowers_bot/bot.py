import os

from telegram.ext import Updater, CommandHandler
from environs import Env


env = Env()
env.read_env(override=True)

BOT_TOKEN = env.str('TG_TOKEN')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowers_bot.settings')

import django
from django.conf import settings

if not settings.configured:
    django.setup()

from bot.models import Event


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text='I"m a bot, please talk to me!')

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
