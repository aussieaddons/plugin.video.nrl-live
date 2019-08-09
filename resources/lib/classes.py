import unicodedata
from builtins import str
from collections import OrderedDict

from future.moves.urllib.parse import parse_qsl, quote_plus, unquote_plus


class Video():
    """ object that contains all the info for a particular match
        eventually will try to make this script more OO"""
    def __init__(self):
        self.video_id = None
        self.thumb = None
        self.title = None
        self.live = None
        self.time = None
        self.desc = None
        self.dummy = None
        self.link_id = None

    def make_kodi_url(self):
        d = OrderedDict(sorted(self.__dict__.items(), key=lambda x: x[0]))
        for key, value in d.items():
            if isinstance(value, str):
                d[key] = unicodedata.normalize(
                    'NFKD', value).encode('ascii', 'ignore').decode('utf-8')
        url = ''
        if d['thumb']:
            d['thumb'] = quote_plus(d['thumb'])
        for item in d.keys():
            url += '&{0}={1}'.format(item, d[item])
        return url

    def parse_kodi_url(self, url):
        params = dict(parse_qsl(url))
        for item in params.keys():
            setattr(self, item, unquote_plus(params[item]))
