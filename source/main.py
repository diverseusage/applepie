
import os

from cyberbot.telebot import Telebot


def button(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)


def main():
    telebot = Telebot(os.environ['BOT_TOKEN'])
    telebot.run_update()


if __name__ == "__main__":
    main()
