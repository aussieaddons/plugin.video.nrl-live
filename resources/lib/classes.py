import unicodedata
from builtins import str
from collections import OrderedDict

from future.moves.urllib.parse import parse_qsl, quote_plus, unquote_plus

from aussieaddonscommon import utils


class Video():
    """ object that contains all the info for a particular match
        eventually will try to make this script more OO"""
    def __init__(self):
        self.video_id = None
        self.account_id = None
        self.policy_key = None
        self.type = None
        self.thumb = None
        self.title = None
        self.live = None
        self.time = None
        self.desc = None
        self.dummy = None
        self.link_id = None

    def make_kodi_url(self):
        d_original = OrderedDict(
            sorted(self.__dict__.items(), key=lambda x: x[0]))
        d = d_original.copy()
        for key, value in d_original.items():
            if not value:
                d.pop(key)
                continue
            if isinstance(value, str):
                d[key] = unicodedata.normalize(
                    'NFKD', value).encode('ascii', 'ignore').decode('utf-8')
        url = ''
        for key in d.keys():
            if isinstance(d[key], (str, bytes)):
                val = quote_plus(d[key])
            else:
                val = d[key]
            url += '&{0}={1}'.format(key, val)
        url += '&addon_version={0}'.format(utils.get_addon_version())
        return url

    def parse_kodi_url(self, url):
        params = dict(parse_qsl(url))
        params.pop('addon_version', '')
        for item in params.keys():
            setattr(self, item, unquote_plus(params[item]))

    def parse_params(self, params):
        for item in params.keys():
            setattr(self, item, unquote_plus(params[item]))
