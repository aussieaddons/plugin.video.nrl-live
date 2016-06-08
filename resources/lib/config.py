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

# Bitrates for Adobe HDS streams - 0 is max (2400)
HDS_REPLAY_QUALITY =   {'0': 168,
                        '1': 236,
                        '2': 400,
                        '3': 700,
                        '4': 1100,
                        '5': 1800,
                        '6': 0}

# url to send our Digital Pass info to
LOGIN_URL = ('https://mis-live-nrl.yinzcam.com/V1/Auth/Subscription?ff=mobile'
            '&mnc=1&app_version=3.0.0&carrier=Telstra+Mobile&version=4.3'
            '&width=1080&height=1776&os_version=5.1&mcc=505'
            '&application=NRL_LIVE&os=Android&format=XML')

# XML template to insert username and password into
LOGIN_DATA =("<?xml version='1.0' encoding='UTF-8'?><Subscriber><Product/>"
            "<AppId/><Type>TDI</Type><Receipt/><User>{0}</User><Password>"
            "{1}</Password></Subscriber>")

# url used to request ooyala token
EMBED_TOKEN_URL =('https://mis-live-nrl.yinzcam.com/V1/Auth/MediaToken?id={0}'
            '&ff=mobile&mnc=1&app_version=3.0.0&carrier=Telstra+Mobile'
            '&version=4.3&width=1794&height=1080&os_version=5.1&mcc=505'
            '&application=NRL_LIVE&os=Android&format=XML')

# url used to request playlist
AUTH_URL = ('http://player.ooyala.com/sas/player_api/v1/authorization/'
            'embed_code/{0}/{1}?device=android_html&domain=http://'
            'nrl.production.NRL%20Live.androidphone&embedToken={2}'
            '&supportedFormats=wv_wvm,mp4,wv_hls,m3u8,wv_mp4')

# main url for xml that contains all our video metadata            
XML_URL =  ('http://app-live-nrl.yinzcam.com/V1/Media/VideoList?&mediaTypes=V&'
            '&compId={0}{1}&category={2}&year={3}&carrier=Telstra+Mobile'
            '&height=1776&error=26&os=Android&a=-184.41070&ff=mobile'
            '&mnc=1&b=113.84670&app_version=3.0.1&version=4.3&width=1080'
            '&os_version=5.1&mcc=505&application=NRL_LIVE')
            
# url for xml that contains match scores
SCORE_URL = ('http://app-live-nrl.yinzcam.com/V1/Game/Scores?carrier='
            'Telstra+Mobile&height=1776&error=11&os=Android&a=-184.41070'
            '&ff=mobile&mnc=1&b=113.84670&app_version=3.0.1&version=4.3'
            '&width=1080&os_version=5.1&mcc=505&application=NRL_LIVE')

# url for xml that contains video metadata for recent/news/misc videos
SHORTLIST_URL = ('http://app-live-nrl.yinzcam.com/V1/Media/ShortList?carrier='
                'Telstra+Mobile&height=1776&error=11&os=Android&a=-184.41070'
                '&ff=mobile&mnc=1&b=113.84670&app_version=3.0.1&version=4.3'
                '&width=1080&os_version=5.1&mcc=505&application=NRL_LIVE')

# used for HDS metadata retrieval
SMIL_URL = "http://player.ooyala.com/nuplayer?embedCode={0}"

# not sure that these are needed atm??
HEADERS = { 'User-Agent' : ('Dalvik/2.1.0 (Linux; U; '
            'Android 5.1; HTC_0PJA10 Build/LMY47O)') }

# ooyala provider indentifier code used in contructing request uris            
PCODE = 'BudDUxOt2GEh8L5PMMpcbz1wJFwm'

YEARS = ['2013', '2014', '2015', '2016']

CATEGORIES = {'1 Live matches': 'LiveMatches',
                '2 Full Match Replays': 'Matches',
                '3 Press Conferences': 'PC',
                '4 Match Highlights': 'Highlights',
                '5 Magic Moments': 'MagicMoments',
                '6 Recent/News': 'ShortList'}

COMPS = {'1 Telstra Premiership': '1',
            '2 State of Origin' : '30',
            '3 Auckland Nines'  : '20',
            '4 All Stars'       : '51',
            '5 World Club Series': '42',
            '6 International Tests': '40',
            '7 Country v City'  : '50',
            '8 State or Origin U20': '31',
            '9 Four Nations'    : '41'}
            
