import unicodedata
import urllib
import urlparse
from collections import OrderedDict


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
        for key, value in d.iteritems():
            if isinstance(value, unicode):
                d[key] = unicodedata.normalize(
                    'NFKD', value).encode('ascii', 'ignore')
        url = ''
        if d['thumb']:
            d['thumb'] = urllib.quote_plus(d['thumb'])
        for item in d.keys():
            url += '&{0}={1}'.format(item, d[item])
        return url

    def parse_kodi_url(self, url):
        params = dict(urlparse.parse_qsl(url))
        for item in params.keys():
            setattr(self, item, urllib.unquote_plus(params[item]))
