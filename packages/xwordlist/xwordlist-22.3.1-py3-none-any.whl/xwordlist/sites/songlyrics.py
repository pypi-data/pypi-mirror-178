from ..xwl import WebExtract


class SongLyrics(WebExtract):
    LYRIC_URL = 'http://www.songlyrics.com/{artist}/{song_name}lyrics/'
    PARSEDICT = {
        'id': 'songLyricsDiv',
    }
    WEBEXTRACT = 'text'

