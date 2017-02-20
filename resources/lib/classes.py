# Copyright 2016 Glenn Guy
# This file is part of NRL Live Kodi Addon
#
# NRL Live is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NRL Live is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NRL Live.  If not, see <http://www.gnu.org/licenses/>.

import urlparse
import unicodedata
import urllib


class game():
    """ object that contains all the info for a particular match
        eventually will try to make this script more OO"""
    def __init__(self):
        self.video_id = None
        self.thumb = None
        self.title = None
        self.live = None
        self.time = None
        self.match_id = None
        self.score = None
        self.desc = None
        self.dummy = None
        
    def make_kodi_url(self):
        d = self.__dict__
        for key, value in d.iteritems():
            if isinstance(value, unicode):
                d[key] = unicodedata.normalize('NFKD', value).encode('ascii','ignore')
        url = ''
        if d['thumb']:      d['thumb'] = urllib.quote_plus(d['thumb'])
        for item in d.keys():
            url += '&{0}={1}'.format(item, d[item])    
        return url    
    
    
    def parse_kodi_url(self, url):
        params = urlparse.parse_qsl(url)
        for item in params.keys():
            setattr(self, item, urllib.unquote_plus(params[item]))