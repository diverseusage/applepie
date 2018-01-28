from bs4 import BeautifulSoup
import requests


class MusicMatch():
    def __init__(self):
        self.url = "https://www.musixmatch.com/"

    def get_soup_object(self, final_url):
        request_result = requests.get(final_url)
        request_html_content = request_result.content
        soup_obj = BeautifulSoup(request_html_content, "html.parser")
        return soup_obj

    def generate_site_from_input(self, message):
        input_message = message
        input_message_trim = input_message.strip()
        processed_message = input_message_trim.replace(' ', '-')

        final_url = self.url + processed_message + "-lyrics"
        return final_url

    def get_raw_lyrics(self, message):
        final_url = self.generate_site_from_input(message)
        soup = self.get_soup_object(final_url)
        raw_lyrics = soup.lyrics
        return raw_lyrics

    def display_lyrics(self, message):
        raw_lyrics = self.get_raw_lyrics(message)
        for tag in raw_lyrics.find_all('a'):
            tag.replaceWith(tag.text)
        final_lyrics = raw_lyrics.get_text().rstrip()
        return final_lyrics
