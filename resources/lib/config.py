# flake8: noqa

NAME = 'NRL Live'
ADDON_ID = 'plugin.video.nrl-live'

GITHUB_API_URL = 'https://api.github.com/repos/glennguy/plugin.video.nrl-live'
ISSUE_API_URL = GITHUB_API_URL + '/issues'
ISSUE_API_AUTH = 'eGJtY2JvdDo1OTQxNTJjMTBhZGFiNGRlN2M0YWZkZDYwZGQ5NDFkNWY4YmIzOGFj'
GIST_API_URL = 'https://api.github.com/gists'

MAX_LIVEQUAL = 4
MAX_REPLAYQUAL = 7

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
VIDEO_URL =  'http://app-live-nrl.yinzcam.com/V1/Media/VideoList?&mediaTypes=V&carrier=&height=1776&error=100000000&os=Android&a=0&ff=mobile&mnc=0&b=0&app_version=4.0.4&version=5.0&width=1080&mcc=0&application=NRL_LIVE'

# url for xml that contains match scores
SCORE_URL = ('http://app-live-nrl.yinzcam.com/V1/Game/Scores?carrier='
            'Telstra+Mobile&height=1776&error=11&os=Android&a=-184.41070'
            '&ff=mobile&mnc=1&b=113.84670&app_version=3.0.1&version=4.3'
            '&width=1080&os_version=5.1&mcc=505&application=NRL_LIVE')

HIGHLIGHTS_URL = 'http://app-live-nrl.yinzcam.com/V1/Media/ShortList?categoryId=Match%20Highlights&mnc=0&ff=mobile&app_version=4.0.4&carrier=&version=5.0&width=1080&height=1776&mcc=0&application=NRL_LIVE&os=Android'

# url for xml that contains video metadata for recent/news/misc videos
SHORTLIST_URL = 'http://app-live-nrl.yinzcam.com/V1/Media/ShortList?{0}mnc=0&ff=mobile&app_version=4.0.4&carrier=&version=5.0&width=1080&height=1776&mcc=0&application=NRL_LIVE&os=Android'


MEDIA_URL = 'http://app-live-nrl.yinzcam.com/V1/Media/News/{0}?age=over18&mnc=0&ff=mobile&app_version=4.0.4&carrier=&version=5.0&width=1080&height=1776&mcc=0&application=NRL_LIVE&os=Android'

BOX_URL = 'https://app-live-nrl.yinzcam.com/V1/Game/Box/{0}?mnc=0&ff=mobile&app_version=4.1.0&carrier=&version=5.1&width=1080&height=1776&mcc=0&application=NRL_LIVE&os=Android'

HOME_URL = 'https://app-live-nrl.yinzcam.com/V1/Home/Index?carrier=&height=1776&error=100000000&os=Android&a=0&ff=mobile&mnc=0&b=0&app_version=4.1.0&version=5.1&width=1080&mcc=0&application=NRL_LIVE'

# used for HDS metadata retrieval
SMIL_URL = "http://player.ooyala.com/nuplayer?embedCode={0}"

# ooyala provider indentifier code used in contructing request uris
PCODE = 'BudDUxOt2GEh8L5PMMpcbz1wJFwm'

YEARS = ['2013', '2014', '2015', '2016', '2017']

CATEGORIES = ['Live Matches', 'Match Highlights', 'Videos', 'Settings']

COMPS = {'1 Telstra Premiership': '1',
            '2 State of Origin': '30',
            '3 Auckland Nines': '20',
            '4 All Stars': '51',
            '5 World Club Series': '42',
            '6 International Tests': '40',
            '7 Country v City': '50',
            '8 State or Origin U20': '31',
            '9 Four Nations': '41'}


# New auth config for 2017

NRL_AUTH = 'https://www.nrl.com/account/authorize?response_type=code&scope=openid%20email%20profile%20offline_access&client_id=nrlapp-ios&redirect_uri=https://redirect.nrl-live.app.openid.yinzcam.com'

NRL_LOGIN = 'https://www.nrl.com/account/login'

NRL_TOKEN = 'https://www.nrl.com/account/token'

TOKEN_DATA = {'client_id': 'nrlapp-ios',
              'grant_type': 'authorization_code',
              'redirect_uri': 'https://redirect.nrl-live.app.openid.yinzcam.com'}


NEW_LOGIN_DATA1 = '<TicketRequest><Anonymous><AppId>NRL_LIVE</AppId><VendorId>{adid}</VendorId><InstallId>{deviceid}</InstallId></Anonymous></TicketRequest>'

NEW_LOGIN_DATA2 = '<TicketRequest><NRLAccount><AppId>NRL_LIVE</AppId><RefreshToken>{0}</RefreshToken></NRLAccount></TicketRequest>'


ANALYTICS_URL = 'https://analytics-live-nrl.yinzcam.com/analytics/report?ff=mobile&carrier=Telstra+Mobile&mnc=1&os=Android&application=NRL_LIVE&app_version=4.1.0&width=1080&mcc=505&version=5.1&height=1794'

ANALYTICS_DATA = ('<Report><ReportInfo><CurrentTime>{currenttime}</CurrentTime><Version>5</Version><ClientAnalyticsVersion>6</ClientAnalyticsVersion></ReportInfo><Action><Type><Major>INSTALL_ID</Major><Minor>{minorid}</Minor></Type><InVenue>false</InVenue><SortOrder>1</SortOrder><SequenceNum>1</SequenceNum><Session>{sessionid}</Session><Resource><Major></Major><Minor></Minor></Resource><DateTime><Request>{time}</Request></DateTime></Action><Start><Session>{sessionid}</Session>'
'<DateTime>{time}</DateTime><Device><Id>{deviceid}</Id><DeviceAdId>{adid}</DeviceAdId><Manufacturer>Google</Manufacturer><Model>Pixel</Model><Version>8.1.0</Version><Platform>Android</Platform><MNC>1</MNC><MCC>505</MCC><Carrier>Telstra Mobile</Carrier><MDN></MDN><Screen><Width>1080</Width><Height>1794</Height></Screen></Device><Application><Id>NRL_LIVE</Id><Version>4.1.0</Version></Application></Start><Action><Type><Major>V</Major><Minor></Minor></Type><InVenue>false</InVenue><SortOrder>2</SortOrder><SequenceNum>2</SequenceNum>'
'<Session>{sessionid}</Session><Resource><Major>HOME</Major><Minor></Minor></Resource><DateTime><Request>{time}</Request><Invisible>{invisibletime}</Invisible></DateTime></Action><Action><TeamId></TeamId><Type><Major>V</Major><Minor></Minor></Type><InVenue>false</InVenue><SortOrder>3</SortOrder><SequenceNum>3</SequenceNum><Session>{sessionid}</Session><Resource><Major>HOME</Major><Minor></Minor></Resource><DateTime><Request>'
'{time}</Request><Invisible>{invisibletime}</Invisible></DateTime></Action></Report>')

STATUS_URL = 'https://signon-live-nrl.yinzcam.com/subscription/status?application=NRL_LIVE'
YINZCAM_PROFILE = 'https://signon-live-nrl.yinzcam.com/profile2/user/combined/query?application=NRL_LIVE'
PROFILE_DATA = {
    "Field": [
        "name",
        "first_name",
        "last_name",
        "email",
        "birth_date",
        "nrl_favorite_nrl_team",
        "nrl_favorite_state_team",
        "nrl_favorite_national_team",
        "timestamp_create",
        "verified"
    ]
}


YINZCAM_AUTH_ORDER = ['Content-Type', 'Accept', 'Connection', 'Content-Length', 'User-Agent', 'Host', 'Accept-Encoding']

YINZCAM_AUTH_URL = 'https://signon-live-nrl.yinzcam.com/ticket?ff=mobile&carrier=Telstra+Mobile&mnc=1&os=Android&application=NRL_LIVE&app_version=4.1.0&width=1080&mcc=505&version=5.1&height=1794'

YINZCAM_AUTH_URL2 = 'https://signon-live-nrl.yinzcam.com/telstra/oneplace/url?application=NRL_LIVE'

YINZCAM_AUTH_HEADERS = {'Content-Type': 'application/xml',
                        'Accept': 'application/xml',
                        'Connection': 'close',
                        'Content-Length': 'placeholder',
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; HTC One_M8 Build/MRA58K.H15)',
                        'Host': 'signon-live-nrl.yinzcam.com',
                        'Accept-Encoding': 'gzip'}

SIGNON_HEADERS = {'Host': 'signon.telstra.com',
                  'Connection': 'keep-alive',
                  'Cache-Control': 'max-age=0',
                  'Origin': 'https://signon.telstra.com.au',
                  'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; HTC One_M8 Build/MRA58K.H15; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36',
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

SSO_URL = 'https://api.telstra.com/v1/sso/auth'

SPC_HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, '
                                  'deflate',
               'Accept-Language': 'en-AU,en-US;q=0.9',
               'Proxy-Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 '
                             '(Linux; '
                             'Android '
                             '8.1.0; '
                             'Pixel '
                             'Build/OPM1.171019.016; '
                             'wv) '
                             'AppleWebKit/537.36 '
                             '(KHTML, '
                             'like '
                             'Gecko) '
                             'Version/4.0 '
                             'Chrome/64.0.3282.137 '
                             'Mobile '
                             'Safari/537.36',
               'X-Requested-With': 'com.telstra.nrl'}

ENTITLEMENTS_URL = 'https://api.telstra.com/v1/media-entitlements/entitlements?idp=TDI&tenantId=nrl'

MEDIA_ORDER_URL = 'https://api.telstra.com/v1/media-commerce/orders'

MEDIA_ORDER_JSON = '{{"serviceId":"{0}","serviceType":"MSISDN","offer":{{"id":"{1}"}},"pai":"{2}"}}'

YINZ_CALLBACK_URL = 'https://signon-live-nrl.yinzcam.com/telstra/oneplace/callback/NRL_LIVE?type=SportPassConfirmationoffers/p/&statusCode=200&tpUID={0}'
