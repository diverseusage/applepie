from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bs4 import BeautifulSoup
import requests
import os

# Global variables
botToken = os.environ['BOT_TOKEN']
rootPage = os.environ['LYRICS_SOURCE_URL']


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Top Hits", callback_data='Top Hits')],
                [InlineKeyboardButton("Top Artists", callback_data='Top Artists')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(start_message.format(update.message.from_user.first_name), reply_markup=reply_markup)


start_message = """Hello {}
Please enter the singer followed by the title of the song. 
e.g. the chainsmokers closer
To get your youtube playlist, 
1. Add @youtube
2. Sign in to your youtube account by entering /auth 
3. Enter /setting 
4. Toggle to 'Suggest liked video' button
5. Click 'Save & go to chat' button """


def button(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)


def get_soup_object(url):
    request_result = requests.get(url)
    request_html_content = request_result.content
    soup_obj = BeautifulSoup(request_html_content, "html.parser")
    return soup_obj


def generate_site_from_input(bot, update):
    input_message = update.message.text
    input_message_trim = input_message.strip()
    processed_message = input_message_trim.replace(' ', '-')

    final_url = rootPage + processed_message + "-lyrics"
    return final_url


def get_raw_lyrics(bot, update):
    final_url = generate_site_from_input(bot, update)
    soup = get_soup_object(final_url)
    raw_lyrics = soup.lyrics
    return raw_lyrics


def display_lyrics(bot, update):
    raw_lyrics = get_raw_lyrics(bot, update)
    for tag in raw_lyrics.find_all('a'):
        tag.replaceWith(tag.text)

    final_lyrics = raw_lyrics.get_text().rstrip()
    update.message.reply_text(final_lyrics)


updater = Updater(botToken)

updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(MessageHandler(Filters.text, display_lyrics))

updater.start_polling()
updater.idle()
