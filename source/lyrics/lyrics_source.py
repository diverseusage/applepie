from lyrics.musicmatch_site import MusicMatch


class LyricsSource:
    UNKNOWN_LYRICS_SOURCE = "UNKNOWN"

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "URL: " + self.url

    def display_lyrics(self, bot, update):
        music_match = MusicMatch()
        return music_match.display_lyrics(bot, update)
