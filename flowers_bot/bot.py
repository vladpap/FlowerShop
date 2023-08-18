import os

import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, update, KeyboardButton, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from environs import Env

logging.basicConfig(filename='bt.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
env = Env()
env.read_env(override=True)

BOT_TOKEN = env.str('TG_TOKEN')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowers_bot.settings')

# import django
# from django.conf import settings
#
# if not settings.configured:
#     django.setup()

# from bot.models import Event


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
catalog = [
    {'img': 'PILimage', 'id_boucet': [1, 2, 3, 4, 5, 6, 7, 8, 9]},
    {'img': 'PILimage_1', 'id_boucet': [10, 11, 12, 13, 14, 15, 16, 17, 18]},
    {'img': 'PILimage_2', 'id_boucet': [19, 20, 21, 22, 23, 24, 25]}
]
users_1 = {'id': 422100905, 'first_name': 'Слава', 'phone': +79199834767, 'address': 'улица Комсомольская, 9'}

START, CHOOSE_EVENT, CHOOSE_AMOUNT, ORDER_FLOWERS, DISTRIBUTION, CONTACT_DETAILS = range(6)
contact_details = {}


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
    # if description:
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=description['image'],
                           caption=f"Цена: {description['price']} руб.\nОписание: {description['description']}")
    keyboard = [[KeyboardButton('Заказать выбранный букет'), KeyboardButton('Каталог'),
                 KeyboardButton('Консультация')]]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Хотите еще что-то более уникальное?'
                              'Подберите букет из коллекции или закажите консультацию флориста',
                              reply_markup=reply_markup)
    return DISTRIBUTION


def order_processing(update, context):
    client = update.message.from_user
    user_id = client.id
    for users_1['id'] in users_1:
        if users_1['id'] == user_id:
            # За место return True тут будет стоять другая строка состояния отличная от CONTACT_DETAILS
            return True
        # return False
    update.message.reply_text('Введите Ваше Имя')
    return CONTACT_DETAILS


def save_name(update, context):
    contact_details['name'] = update.message.text
    update.message.reply_text('Отлично! Теперь введите свой телефон.')
    return save_phone


def save_phone(update, context):
    contact_details['phone'] = update.message.text
    update.message.reply_text('Спасибо! Адрес доставки?')
    return save_address


def save_address(update, context):
    contact_details['address'] = update.message.text
    reply_keyboard = [['Ближайшие числа', 'Ввести самому']]
    update.message.reply_text('На какую дату нужна доставка?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                              )


def consultation(update, context):
    update.message.reply_text('Нажал консультация')


def catalog_bouquet(update, context):
    keyboard = []
    for coloring in catalog[0]['id_boucet']:
        button = KeyboardButton(str(coloring))
        keyboard.append(button)
    next_button = KeyboardButton("Далее")
    keyboard.append(next_button)
    reply_markup = ReplyKeyboardMarkup(keyboard=[[button] for button in keyboard], resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите номер букета", reply_markup=reply_markup)


def main():
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher
    logic_conversation = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            CHOOSE_EVENT: [MessageHandler(Filters.text & ~Filters.command, event_clarification)],
            CHOOSE_AMOUNT: [MessageHandler(Filters.text & ~Filters.command, choose_amount)],
            ORDER_FLOWERS: [MessageHandler(Filters.text & ~Filters.command, order_flowers)],
            DISTRIBUTION: [MessageHandler(Filters.regex('Заказать выбранный букет'), order_processing),
                           MessageHandler(Filters.regex('Консультация'), consultation),
                           MessageHandler(Filters.regex('Каталог'), catalog_bouquet)],
            CONTACT_DETAILS: [MessageHandler(Filters.text & ~Filters.command, save_name),
                              MessageHandler(Filters.text, save_phone),
                              MessageHandler(Filters.text, save_address)]


        },
        fallbacks=[]
    )
    dispatcher.add_handler(logic_conversation)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
