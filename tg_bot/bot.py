from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters

TOKEN = "1025575981:AAEfovCrP97nSWfX4WIPBvImNDHKdINX56U"


def massage_handler(bot: Bot, update: Update):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = "Анонимный пользователь"

    text = update.effective_message.text
    reply_text = f'Привет , {name}! \n\n {text}'

    bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=reply_text
    )


def main():
    print("Bot is started")
    bot = Bot(
        token=TOKEN,
        base_url="https://telegg.ru/orig/bot"
    )
    updater = Updater(
        bot=bot
    )

    handler = MessageHandler(Filters.all, massage_handler)

    updater.dispatcher.add_handler(handler)
    updater.start_polling()
    updater.idle()
    print("Bot is finished")


if __name__ == "__main__":
    main()

