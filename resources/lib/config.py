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

import version

NAME = 'AFL Video'
ADDON_ID = 'plugin.video.nrl-live'
VERSION = version.VERSION

GITHUB_API_URL = 'https://api.github.com/repos/glennguy/plugin.video.nrl-live'
ISSUE_API_URL = GITHUB_API_URL + '/issues'
ISSUE_API_AUTH = 'eGJtY2JvdDo1OTQxNTJjMTBhZGFiNGRlN2M0YWZkZDYwZGQ5NDFkNWY4YmIzOGFj'
GIST_API_URL = 'https://api.github.com/gists'


# Bitrates for Adobe HDS streams - 0 is max (2400)
HDS_REPLAY_QUALITY =   {'0': 168,
                        '1': 236,
                        '2': 400,
                        '3': 700,
                        '4': 1100,
                        '5': 1800,
                        '6': 0}

# url to send our Digital Pass info to
LOGIN_URL = ('https://signon-live-nrl.yinzcam.com/V1/Auth/Subscription?ff=mobile'
            '&mnc=1&app_version=3.3.0&carrier=&version=4.7'
            '&width=1080&height=1776&os_version=6.0&mcc=505'
            '&application=NRL_LIVE&os=Android')

# XML template to insert username and password into
LOGIN_DATA ='<Subscriber><Type>TDI</Type><User>{0}</User><Password>{1}</Password><Email>{0}</Email><AdobeCheckResult>0</AdobeCheckResult></Subscriber>'

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
            '&height=1776&error=20&os=Android&a=-184.41070&ff=mobile'
            '&mnc=1&b=113.84670&app_version=3.3.0&version=4.7&width=1080'
            '&os_version=6.0&mcc=505&application=NRL_LIVE')
            
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
HEADERS = { 'User-Agent' : 'Dalvik/2.1.0 (Linux; U; Android 6.0; HTC One_M8 Build/MRA58K.H15)', 'Content-Type': 'application/xml', 'Accept': 'application/json', 'Accept-Encoding': 'gzip' }

# ooyala provider indentifier code used in contructing request uris            
PCODE = 'BudDUxOt2GEh8L5PMMpcbz1wJFwm'

YEARS = ['2013', '2014', '2015', '2016', '2017']

CATEGORIES = {'1 Live Matches': 'livematches',
                '2 Full Match Replays': 'Matches',
                '3 Press Conferences': 'PC',
                '4 Match Highlights': 'Highlights',
                '5 Plays of the week': 'POW',
                '6 Recent/News': 'shortlist',
                '7 Settings': 'settings'}

COMPS = {'1 Telstra Premiership': '1',
            '2 State of Origin' : '30',
            '3 Auckland Nines'  : '20',
            '4 All Stars'       : '51',
            '5 World Club Series': '42',
            '6 International Tests': '40',
            '7 Country v City'  : '50',
            '8 State or Origin U20': '31',
            '9 Four Nations'    : '41'}
            

# New auth config for 2017

NEW_LOGIN_DATA1 = '<Subscriber><Type>MSISDN</Type><AdobeCheckResult>0</AdobeCheckResult></Subscriber>'

NEW_LOGIN_DATA2 = '<Subscriber><Type>TOKEN</Type><User>{0}</User></Subscriber>'

YINZCAM_AUTH_ORDER = ['Content-Type', 'Accept', 'Connection', 'Content-Length', 'User-Agent', 'Host', 'Accept-Encoding']

YINZCAM_AUTH_URL = 'https://signon-live-nrl.yinzcam.com/v1/Auth/Subscription?ff=mobile&mnc=1&app_version=3.3.0&carrier=Telstra+Mobile&version=4.7&width=1080&height=1776&os_version=6.0&mcc=505&application=NRL_LIVE&os=Android'

YINZCAM_AUTH_HEADERS = {'Content-Type': 'application/xml', 
                        'Accept': 'application/json', 
                        'Connection': 'close', 
                        'Content-Length': 'placeholder', 
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; HTC One_M8 Build/MRA58K.H15)', 
                        'Host': 'signon-live-nrl.yinzcam.com', 
                        'Accept-Encoding': 'gzip'}

SIGNON_HEADERS = {'Host': 'signon.telstra.com', 
                  'Connection': 'keep-alive', 
                  'Cache-Control': 'max-age=0', 
                  'Origin': 'https://signon.telstra.com', 
                  'Upgrade-Insecure-Requests': '1', 
                  'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; HTC One_M8 Build/MRA58K.H15; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36', 
                  'Content-Type': 'application/x-www-form-urlencoded', 
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
                  'Referer': 'https://signon.telstra.com/login?goto=https%3A%2F%2Fsignon.telstra.com%2Ffederation%2Fsaml2%3FSPID%3Dtelstramedia&gotoNoTok=', 
                  'Accept-Encoding': 'gzip, deflate', 
                  'Accept-Language': 'en-AU,en-US;q=0.8'}
                        
SIGNON_URL = 'https://signon.telstra.com/login'

SIGNON_DATA = {'goto': 'https://signon.telstra.com/federation/saml2?SPID=telstramedia', 'gotoOnFail': '', 'username': None, 'password': None}

SAML_LOGIN_URL = 'https://hub.telstra.com.au/login/saml_login'

SAML_LOGIN_HEADERS = {'Host': 'hub.telstra.com.au', 
                      'Connection': 'keep-alive', 
                      'Cache-Control': 'max-age=0', 
                      'Origin': 'https://signon.telstra.com', 
                      'Upgrade-Insecure-Requests': '1', 
                      'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; HTC One_M8 Build/MRA58K.H15; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36', 
                      'Content-Type': 'application/x-www-form-urlencoded', 
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
                      'Referer': 'https://signon.telstra.com/federation/saml2?SPID=telstramedia', 
                      'Accept-Encoding': 'gzip, deflate', 
                      'Accept-Language': 'en-AU,en-US;q=0.8', 
                      'X-Requested-With': 'com.telstra.nrl'}
                        
OFFERS_URL = 'https://api.telstra.com/v1/media-products/catalogues/media/offers?category=nrl'

HUB_URL = 'http://hub.telstra.com.au/sp2017-nrl-app'

MEDIA_ORDER_HEADERS = {'Content-Type': 'application/json', 
                       'Accept': 'application/json, text/plain, */*', 
                       'Host': 'api.telstra.com', 
                       'Connection': 'keep-alive', 
                       'Origin': 'https://hub.telstra.com.au',
                       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; HTC One_M8 Build/MRA58K.H15; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36', 
                       'Accept-Encoding': 'gzip, deflate', 
                       'Accept-Language': 'en-AU,en-US;q=0.8', 
                       'X-Requested-With': 'com.telstra.nrl'}
                        
MEDIA_ORDER_URL = 'https://api.telstra.com/v1/media-commerce/orders'

MEDIA_ORDER_JSON = '{{"serviceId":"{0}","serviceType":"MSISDN","offer":{{"id":"{1}"}},"pai":"{2}"}}'