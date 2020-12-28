import config
from telegram.ext import Updater, CommandHandler

# Telegram API
# access  bot via token
updater = Updater(token=config.telegram_bot_api_key)
dispatcher = updater.dispatcher

def start(update,context):
    update.message.reply_text('Hello, This is a telegram to twitter bot')


def runner():

    # handlers
    start_handler = CommandHandler('start', start)

    # handle dispatcher
    dispatcher.add_handler(start_handler)

    # run
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    runner()