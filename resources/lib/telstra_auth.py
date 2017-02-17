#-------------------------------------------------------------------------------
import requests
import collections
import json
import urlparse
import urllib
import config
import re
from bs4 import BeautifulSoup


class SortedHTTPAdapter(requests.adapters.HTTPAdapter):
    def add_headers(self, request, **kwargs):
        if 'header_order' in globals():
            header_list = request.headers.items()
            for item in header_list: 
                if item[0] not in header_order:
                    header_list.remove(item)
            request.headers = collections.OrderedDict(
                sorted(header_list, key=lambda x: header_order.index(x[0])))

        
def get_token(username, password, phone_number):
    """ Obtain a valid token from Telstra/Yinzcam, will be used to make requests for 
        Ooyala embed tokens"""
    session = requests.Session()
    session.verify = False
    session.mount("https://", SortedHTTPAdapter())
    global header_order
        
    # Send our first login request to Yinzcam, recieve (unactivated) token
    # and 'msisdn' URL
    
    header_order = config.YINZCAM_AUTH_ORDER
    session.headers = config.YINZCAM_AUTH_HEADERS
    auth_resp = session.post(config.YINZCAM_AUTH_URL, data=config.NEW_LOGIN_DATA1)
    jsondata = json.loads(auth_resp.text)
    token = jsondata.get('UserToken')
    msisdn_url = jsondata.get('MsisdnUrl')
    del header_order
    ### 116
    
    # Sign in to telstra.com to recieve cookies, get the SAML auth, and 
    # modify the escape characters so we can send it back later
    session.headers = config.SIGNON_HEADERS
    signon_data = config.SIGNON_DATA
    signon_data.update({'username': username, 'password': password})
    signon = session.post(config.SIGNON_URL, data=signon_data)
    soup = BeautifulSoup(signon.text, 'html.parser')
    saml_response = soup.find(attrs={'name': 'SAMLResponse'}).get('value')
    saml_base64 = urllib.quote(saml_response)

    
    # Send the SAML login data and retrieve the auth token from the response
    session.headers = config.SAML_LOGIN_HEADERS
    session.cookies.set('saml_request_path', msisdn_url)
    saml_login = session.post(config.SAML_LOGIN_URL, 
                            data='SAMLResponse={0}'.format(saml_base64))
    confirm_url = saml_login.url
    auth_token_match = re.search('apiToken = "(\w+)"', saml_login.text)
    auth_token = auth_token_match.group(1)
    
    # 'Order' the subscription package to activate our token/login
    offer_id = dict(urlparse.parse_qsl(urlparse.urlsplit(msisdn_url)[3]))['offerId']
    media_order_headers = config.MEDIA_ORDER_HEADERS
    media_order_headers.update({'Authorization': 'Bearer {0}'.format(auth_token), 
                                'Referer': confirm_url})
    session.headers = media_order_headers
    session.post(config.MEDIA_ORDER_URL, data=config.MEDIA_ORDER_JSON.format(
                                                phone_number, offer_id, token))

    # Sign in to Yinzcam with our activated token. Token is valid for 28 days
    header_order = config.YINZCAM_AUTH_ORDER
    session.headers = config.YINZCAM_AUTH_HEADERS
    session.post(config.YINZCAM_AUTH_URL, 
                data=config.NEW_LOGIN_DATA2.format(token))
    del header_order

    return token