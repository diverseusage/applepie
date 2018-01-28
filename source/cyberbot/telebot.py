from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import os

from lyrics.lyrics_manager import LyricsManager


class Telebot:
    START_MESSAGE = """Hello {}
        Please enter the singer followed by the title of the song. 
        e.g. the chainsmokers closer
        To get your youtube playlist, 
        1. Add @youtube
        2. Sign in to your youtube account by entering /auth 
        3. Enter /setting 
        4. Toggle to 'Suggest liked video' button
        5. Click 'Save & go to chat' button """

    # def button(self, bot, update):
    #     query = update.callback_query
    #     bot.editMessageText(text="Selected option: %s" % query.data,
    #                         chat_id=query.message.chat_id,
    #                         message_id=query.message.message_id)

    def start(self, bot, update):
        keyboard = [[InlineKeyboardButton("Top Hits", callback_data='Top Hits')],
                    [InlineKeyboardButton("Top Artists", callback_data='Top Artists')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(self.START_MESSAGE.format(update.message.from_user.first_name), reply_markup=reply_markup)

    def display(self, bot, update):
        lyrics_manager = LyricsManager()
        message = update.message.text
        update.message.reply_text(lyrics_manager.display_lyrics(message))

    def run_update(self):
        updater = Updater(self.token)

        updater.dispatcher.add_handler(CommandHandler('start', self.start))

        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.display))

        updater.start_polling()
        updater.idle()
