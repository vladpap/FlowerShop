import os

import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, update, KeyboardButton, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
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
logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

events = [{'id': 1, 'text': 'День рождения'},
          {'id': 2, 'text': 'Юбилей'},
          {'id': 3, 'text': 'Свидание'},
          {'id': 4, 'text': '1 сентября'},
          {'id': 4, 'text': 'На свадьбу'},
          {'id': 4, 'text': '8 марта'},
          {'id': 4, 'text': 'С новосельем'},
          {'id': 4, 'text': 'Другой повод'},
          ]
cost_of_flowers = [{'id': 1, 'text': '500'},
                   {'id': 2, 'text': '1000'},
                   {'id': 3, 'text': '2000'},
                   {'id': 4, 'text': 'Больше'},
                   {'id': 4, 'text': 'Не важно'}
                   ]
flowers = [{'id': 1, 'price': '500', 'description': 'Этот букет несет в себе',
            'image': 'https://mykaleidoscope.ru/uploads/posts/2022-06/1656330320_1-mykaleidoscope-ru-p-buket-s-fioletovimi-tsvetami-krasivo-foto-1.jpg'},
           {'id': 2, 'price': '1000', 'description': 'оставить равнодушных очень много сердец'},
           {'id': 3, 'price': '2000', 'description': 'равнодушных очень много'}
           ]

START, CHOOSE_EVENT, CHOOSE_AMOUNT, ORDER_FLOWERS = range(4)

def start_command(update, context):
    reply_keyboard = [[event['text']] for event in events]
    update.message.reply_text('К какому событию готовимся? Выберите один из вариантов, либо укажите свой.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOOSE_EVENT


def cost_clarification(update, context):
    reply_keyboard = [[cost['text']] for cost in cost_of_flowers]
    return ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def event_clarification(update, context):
    text = update.message.text
    if text == 'Другой повод':
        update.message.reply_text('Какой повод?')
        return CHOOSE_AMOUNT
    else:
        update.message.reply_text('На какую сумму рассчитываете?', reply_markup=cost_clarification(update, context))
        return ORDER_FLOWERS


def choose_amount(update, context):
    update.message.reply_text('На какую сумму рассчитываете?', reply_markup=cost_clarification(update, context))
    return ORDER_FLOWERS


def order_flowers(update, context):
    bouquet_id = 1
    description = next((bouquet for bouquet in flowers if bouquet['id'] == bouquet_id), None)
    if description:
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=description['image'],
                               caption=f"Цена: {description['price']} руб.\n Описание: {description['description']}")
    else:
        update.message.reply_text('Букет не найден.')
    keyboard = [['Заказать букет'], ['Каталог'], ['Консультация']]


def main():
    # load_dotenv()
    tg_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher
    logic_conversation = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            CHOOSE_EVENT: [MessageHandler(Filters.text & ~Filters.command, event_clarification)],
            CHOOSE_AMOUNT: [MessageHandler(Filters.text & ~Filters.command, choose_amount)],
            ORDER_FLOWERS: [MessageHandler(Filters.text & ~Filters.command, order_flowers),
                            ],
        },
        fallbacks=[]
    )
    dispatcher.add_handler(logic_conversation)
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, order_button_suggestion))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
