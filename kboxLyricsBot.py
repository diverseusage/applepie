from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bs4 import BeautifulSoup
import requests
import os

#Global variables
botToken = os.environ['BOT_TOKEN']
rootPage = os.environ['LYRICS_SOURCE_WEBSITE']

def start(bot, update):
    keyboard = [[InlineKeyboardButton("Top Hits", callback_data='Top Hits')],
                [InlineKeyboardButton("Top Artists", callback_data='Top Artists')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(start_message.format(update.message.from_user.first_name),reply_markup=reply_markup)

start_message ="""Hello {}
Please enter the singer followed by the title of the song. 
e.g. the chainsmokers closer
To get your youtube playlist, 
1. Add @youtube
2. Sign in to your youtube account by entering /auth 
3. Enter /setting 
4. Toggle to 'Suggest liked video' button
5. Click 'Save & go to chat' button """ + botToken

def button(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
						
def getSoupObject(url):
	requestResult = requests.get(url)
	requestHtmlContent = requestResult.content
	soupObj = BeautifulSoup(requestHtmlContent, "html.parser")
	return soupObj
		
def generateSiteFromInput(bot, update):
	inputMessage = update.message.text
	inputMessageTrim = inputMessage.strip()
	processedMessage = inputMessageTrim.replace(' ', '-')
	
	finalUrl = rootPage + processedMessage + "-lyrics"
	return finalUrl
	
def getRawLyrics(bot, update):
	finalUrl = generateSiteFromInput(bot, update)
	soup = getSoupObject(finalUrl)		
	rawLyrics = soup.lyrics
	return rawLyrics
	
def displayLyrics(bot, update):
	rawLyrics = getRawLyrics(bot, update)
	for tag in rawLyrics.find_all('a'):
		tag.replaceWith(tag.text)
	
	finalLyrics = rawLyrics.get_text().rstrip()
	update.message.reply_text(finalLyrics)
	

updater = Updater(botToken)

updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(MessageHandler(Filters.text, displayLyrics))



updater.start_polling()
updater.idle()