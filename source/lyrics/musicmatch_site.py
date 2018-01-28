from lyrics.lyrics_source import LyricsSource
from bs4 import BeautifulSoup
import requests


class MusicMatch(LyricsSource):
    def __init__(self):
        super().__init__('https://www.musixmatch.com/')

    def get_soup_object(self, url):
        request_result = requests.get(url)
        request_html_content = request_result.content
        soup_obj = BeautifulSoup(request_html_content, "html.parser")
        return soup_obj

    def generate_site_from_input(self, bot, update):
        input_message = update.message.text
        input_message_trim = input_message.strip()
        processed_message = input_message_trim.replace(' ', '-')

        final_url = self.url + processed_message + "-lyrics"
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
