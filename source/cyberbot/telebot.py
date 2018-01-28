from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bs4 import BeautifulSoup
import requests
import os

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
    rootPage = os.environ['LYRICS_SOURCE_URL']

    def __init__(self, bot_token):
        self.token = bot_token
        self.run_update()

    def start(self, bot, update):
        keyboard = [[InlineKeyboardButton("Top Hits", callback_data='Top Hits')],
                    [InlineKeyboardButton("Top Artists", callback_data='Top Artists')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(self.START_MESSAGE.format(update.message.from_user.first_name), reply_markup=reply_markup)

    def get_soup_object(self, url):
        request_result = requests.get(url)
        request_html_content = request_result.content
        soup_obj = BeautifulSoup(request_html_content, "html.parser")
        return soup_obj

    def generate_site_from_input(self, bot, update):
        input_message = update.message.text
        input_message_trim = input_message.strip()
        processed_message = input_message_trim.replace(' ', '-')

        final_url = self.rootPage + processed_message + "-lyrics"
        return final_url

    def get_raw_lyrics(self, bot, update):
        final_url = self.generate_site_from_input(bot, update)
        soup = self.get_soup_object(final_url)
        raw_lyrics = soup.lyrics
        return raw_lyrics

    def display_lyrics(self, bot, update):
        raw_lyrics = self.get_raw_lyrics(bot, update)
        for tag in raw_lyrics.find_all('a'):
            tag.replaceWith(tag.text)
        final_lyrics = raw_lyrics.get_text().rstrip()
        update.message.reply_text(final_lyrics)

    def run_update(self):
        updater = Updater(self.token)

        updater.dispatcher.add_handler(CommandHandler('start', self.start))

        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.display_lyrics))

        updater.start_polling()
        updater.idle()
