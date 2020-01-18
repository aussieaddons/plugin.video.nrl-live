# flake8: noqa

NAME = 'NRL Live'
ADDON_ID = 'plugin.video.nrl-live'

GITHUB_API_URL = 'https://api.github.com/repos/glennguy/plugin.video.nrl-live'
ISSUE_API_URL = GITHUB_API_URL + '/issues'
ISSUE_API_AUTH = 'eGJtY2JvdDo1OTQxNTJjMTBhZGFiNGRlN2M0YWZkZDYwZGQ5NDFkNWY4YmIzOGFj'
GIST_API_URL = 'https://api.github.com/gists'

MAX_LIVEQUAL = 4
MAX_REPLAYQUAL = 6

USER_AGENT = 'Dalvik/2.1.0 (Linux; U; Android 6.0; HTC One_M8 Build/MRA58K.H15)'
USER_AGENT_LONG = 'Mozilla/5.0 (Linux; Android 6.0; HTC One_M8 Build/MRA58K.H15; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36'

# url to send our Digital Pass info to
LOGIN_URL = ('https://signon-live-nrl.yinzcam.com/V1/Auth/Subscription?ff=mobile'
            '&mnc=1&app_version=3.3.0&carrier=&version=4.7'
            '&width=1080&height=1776&os_version=6.0&mcc=505'
            '&application=NRL_LIVE&os=Android')

# XML template to insert username and password into
LOGIN_DATA ='<Subscriber><Type>TDI</Type><User>{0}</User><Password>{1}</Password><Email>{0}</Email><AdobeCheckResult>0</AdobeCheckResult></Subscriber>'

# url used to request ooyala token
EMBED_TOKEN_URL = 'https://signon-live-nrl.yinzcam.com/subscription/videotoken?embed_code={0}&mnc=0&ff=mobile&app_version=4.1.0&carrier=&version=5.1&width=1080&height=1776&mcc=0&application=NRL_LIVE&os=Android&format=XML'

# url used to request playlist
AUTH_URL = 'http://player.ooyala.com/sas/player_api/v1/authorization/embed_code/{0}/{1}?device=android_html&domain=https%3A%2F%2Fnrl.official.production.android&embedToken={2}&supportedFormats=dash%2Cakamai_hd2_vod_hls%2Cmp4%2Cm3u8%2Chls%2Cakamai_hd2_hls'

# main url for xml that contains all our video metadata
VIDEO_URL =  'https://app-live-nrl.yinzcam.com/V1/Media/LongList?mnc=0&ff=mobile&app_version=4.5.0&carrier=&version=6.0&height=1776&width=1080&mcc=0&application=NRL_LIVE&os=Android'

# url for xml that contains match scores
SCORE_URL = 'https://app-live-nrl.yinzcam.com/V1/Game/Scores?compId=1&a=0&ff=mobile&mnc=0&b=0&app_version=4.4.0&carrier=&version=5.2&width=1080&height=1776&mcc=0&application=NRL_LIVE&error=100000000&os=Android'

TOPICS_URL = 'http://app-live-nrl.yinzcam.com/V1/Media/ShortList?categoryId={0}&mnc=0&ff=mobile&app_version=4.5.0&carrier=&version=6.0&height=1776&width=1080&mcc=0&application=NRL_LIVE&os=Android'

# url for xml that contains video metadata for recent/news/misc videos
SHORTLIST_URL = 'http://app-live-nrl.yinzcam.com/V1/Media/ShortList?{0}mnc=0&ff=mobile&app_version=4.0.4&carrier=&version=5.0&width=1080&height=1776&mcc=0&application=NRL_LIVE&os=Android'


MEDIA_URL = 'http://app-live-nrl.yinzcam.com/V1/Media/News/{0}?age=over18&mnc=0&ff=mobile&app_version=4.0.4&carrier=&version=5.0&width=1080&height=1776&mcc=0&application=NRL_LIVE&os=Android'

MEDIA_ITEM_URL = 'https://app-live-nrl.yinzcam.com/V1/Media/Item/{0}?ff=mobile&mnc=0&app_version=4.3.0&carrier=&version=5.2&width=1080&height=1776&mcc=0&application=NRL_LIVE&os=Android'

BOX_URL = 'https://app-live-nrl.yinzcam.com/V1/Game/Box/{0}?mnc=0&ff=mobile&app_version=4.1.0&carrier=&version=5.1&width=1080&height=1776&mcc=0&application=NRL_LIVE&os=Android'

HOME_URL = 'https://app-live-nrl.yinzcam.com/V1/Home/Index?a=0&ff=mobile&mnc=0&b=0&app_version=4.3.0&carrier=&version=5.2&width=1080&height=1776&mcc=0&application=NRL_LIVE&error=100000000&os=Android'

STREAM_API_URL = 'https://www.nrl.com/api/videos/{video_id}/streams'

STREAM_AUTH_SECRET = 'wT8FhLpxmi8lrjGYJxCbJfzp7hr'

# ooyala provider indentifier code used in contructing request uris
PCODE = 'BjZ2oyOsA0g9SvHHgrgYMEu0p1j1'

CATEGORIES = ['Live Matches', 'Match Highlights', 'Match Replays', 'Videos', 'Settings']

CATEGORY_LOOKUP = {'Match Highlights': 'Match Highlight',
                   'Match Replays': 'Full Match Replay'}

# New auth config for 2018

NRL_AUTH = 'https://www.nrl.com/account/authorize?response_type=code&scope=openid%20email%20profile%20offline_access&client_id=nrlapp-ios&redirect_uri=https://redirect.nrl-live.app.openid.yinzcam.com'

NRL_LOGIN = 'https://www.nrl.com/account/login'

NRL_TOKEN = 'https://www.nrl.com/account/token'

TOKEN_DATA = {'client_id': 'nrlapp-ios',
              'grant_type': 'authorization_code',
              'redirect_uri': 'https://redirect.nrl-live.app.openid.yinzcam.com'}


NEW_LOGIN_DATA1 = '<TicketRequest><Anonymous><AppId>NRL_LIVE</AppId><VendorId>{adid}</VendorId><InstallId>{deviceid}</InstallId></Anonymous></TicketRequest>'

NEW_LOGIN_DATA2 = '<TicketRequest><NRLAccount><AppId>NRL_LIVE</AppId><RefreshToken>{0}</RefreshToken></NRLAccount></TicketRequest>'

STATUS_URL = 'https://signon-live-nrl.yinzcam.com/subscription/status?application=NRL_LIVE'

YINZCAM_AUTH_URL = 'https://signon-live-nrl.yinzcam.com/ticket?ff=mobile&carrier=Telstra+Mobile&mnc=1&os=Android&application=NRL_LIVE&app_version=4.1.0&width=1080&mcc=505&version=5.1&height=1794'

YINZCAM_AUTH_URL2 = 'https://signon-live-nrl.yinzcam.com/telstra/oneplace/url?application=NRL_LIVE'

YINZCAM_AUTH_HEADERS = {'Content-Type': 'application/xml',
                        'Accept': 'application/xml',
                        'Connection': 'close',
                        'Content-Length': 'placeholder',
                        'User-Agent': USER_AGENT,
                        'Host': 'signon-live-nrl.yinzcam.com',
                        'Accept-Encoding': 'gzip'}

SIGNON_HEADERS = {'Connection': 'keep-alive',
                  'Cache-Control': 'max-age=0',
                  'Origin': 'https://signon.telstra.com.au',
                  'User-Agent': USER_AGENT_LONG,
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Referer': 'https://signon.telstra.com.au/login?goto=https%3A%2F%2Fapi.telstra.com%2Fv1%2Fsso%2Fidpcallback%3Fcbs%3DeyJhbGciOiJIUzI1NiJ9.eyJjYWxsYmFja19zdGF0ZSI6IjEyMjcyMDQ3LWU3N2ItNGRiZC1hNGZiLTBlYTcwMDMyYmRlMSIsImF1ZCI6InJhYSIsImV4cCI6MTUyMDczNTMyMTk0OCwiaWF0IjoxNTIwNjQ4OTIxOTQ4fQ.-I05HQE9eIpRS0LLSYB_pJ4iVKZZzyziVYarvjCe_2o%26app_name%3DOne%20Place%20portal',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'en-AU,en-US;q=0.8',
                  'X-Requested-With': 'com.telstra.nrl'}

SIGNON_URL = 'https://signon.telstra.com.au/login'

SIGNON_DATA = {'goto': 'https://signon.telstra.com/federation/saml2?SPID=telstramedia',
               'gotoOnFail': '',
               'username': None,
               'password': None}

OFFERS_URL = 'https://tapi.telstra.com/v1/media-products/catalogues/media/offers?category=nrl'

HUB_URL = 'http://hub.telstra.com.au/sp2017-nrl-app'

MYID_AUTHORIZATION_URL = 'https://myid.telstra.com/identity/as/authorization.oauth2'

MYID_TOKEN_URL = 'https://myid.telstra.com/identity/as/token.oauth2'

MYID_TOKEN_PARAMS = {
    'redirect_uri': 'https://hub.telstra.com.au/offers/content/cached'
                    '/callback.html',
    'grant_type': 'authorization_code'
}

MYID_RESUME_AUTHORIZATION_URL = 'https://myid.telstra.com/identity/as/{0}/resume/as/authorization.ping'

MYID_AUTH_RESUME_DATA = {
    'pf.rememberUsername': 'on',
    'pf.ok': 'clicked',
    'pf.cancel': '',
    'pf.adapterId': 'upAdapter'
}

SSO_SESSION_HANDLER_URLS = [
    'https://signon.telstra.com/SSOSessionHandler',
    'https://signon.bigpond.com/SSOSessionHandler',
    'https://signon.telstra.com.au/SSOSessionHandler'
]

MYID_AUTH_PARAMS = {
    'redirect_uri': 'https://hub.telstra.com.au/offers/content/cached'
                    '/callback.html',
    'response_type': 'code',
    'scope': 'openid app.oneplace',
    'code_challenge_method': 'S256',
    'response_mode': 'query'}

MYID_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, '
                       'deflate',
    'Accept-Language': 'en-AU,en-US;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'X-Requested-With': 'com.telstra.nrl'}

SPC_HEADERS = {'Accept': 'text/html,application/xhtml+xml,'
                         'application/xml;q=0.9,image/webp,image/apng,'
                         '*/*;q=0.8',
               'Accept-Encoding': 'gzip, '
                                  'deflate',
               'Accept-Language': 'en-AU,en-US;q=0.9',
               'User-Agent': USER_AGENT_LONG,
               'X-Requested-With': 'com.telstra.nrl'}


MEDIA_ORDER_HEADERS = {'Content-Type': 'application/json',
                       'Accept': 'application/json, text/plain, */*',
                       'Connection': 'keep-alive',
                       'Origin': 'https://hub.telstra.com.au',
                       'User-Agent': USER_AGENT_LONG,
                       'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'en-AU,en-US;q=0.8',
                       'X-Requested-With': 'com.telstra.nrl'}

MEDIA_ORDER_URL = 'https://tapi.telstra.com/v1/media-commerce/orders?category=nrl'

MEDIA_ORDER_JSON = '{{"serviceId":"{0}","serviceType":"MSISDN","offer":{{"id":"{1}"}},"pai":"{2}"}}'

YINZ_CALLBACK_URL = 'https://signon-live-nrl.yinzcam.com/telstra/oneplace/callback/NRL_LIVE?type=SportPassConfirmation&statusCode=200&tpUID={0}'

#Mobile Auth
OFFER_ID = '69b1f3e1-5196-4a57-9a46-472d20b78bc8'

OAUTH_HEADERS = {'User-Agent': 'AFL(Android) / 40656',
                 'Accept-Encoding': 'gzip'}

MOBILE_OAUTH_URL = 'https://tapi.telstra.com/v1/media-commerce/oauth/token'

MOBILE_ID_URL = 'http://medrx.telstra.com.au/online.php'

MOBILE_CLIENT_ID = '4twlIr9DB2ga3lEjsxjxfivI4bNqIAG0'

MOBILE_CLIENT_SECRET = 'UhTzt1XPpIXUhqPD'

MOBILE_TOKEN_PARAMS = {'client_id': MOBILE_CLIENT_ID,
                      'client_secret': MOBILE_CLIENT_SECRET,
                      'grant_type': 'client_credentials',
                      'scope': 'MEDIA-ENTITLEMENTS-API MEDIA-PRODUCTS-API MEDIA-COMMERCE-API MY-OFFERS-BFF',
                      'x-user-idp': 'NGP'}

MOBILE_ORDER_JSON = {"offer": {"id":OFFER_ID}, "serviceType":"MSISDN"}
