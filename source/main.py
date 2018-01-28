import os

from cyberbot.telebot import Telebot


def main():
    telebot = Telebot(os.environ['BOT_TOKEN'])
    telebot.run_update()


if __name__ == "__main__":
    main()
