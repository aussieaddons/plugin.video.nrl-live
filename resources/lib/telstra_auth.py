import config
import json
import re
import requests
import urllib
import urlparse
import uuid
import xbmcgui

from aussieaddonscommon.exceptions import AussieAddonsException
from aussieaddonscommon import session as custom_session
from aussieaddonscommon import utils

from bs4 import BeautifulSoup


class TelstraAuthException(AussieAddonsException):
    """Telstra Auth exception
    This exception can be thrown with the reportable arg set which can
    determine whether or not it is allowed to be sent as an automatic
    error report
    """
    pass


def get_paid_token(username, password):
    """
    Obtain a valid token from Telstra/Yinzcam, will be used to make
    requests for Ooyala embed tokens
    """
    session = custom_session.Session()
    auth_resp = session.get(config.NRL_AUTH, allow_redirects=False)
    
    xsrf = auth_resp.cookies['XSRF-TOKEN']
    session.headers.update({'x-xsrf-token': xsrf})
    
    data = {'emailAddress': '{0}'.format(username),
            'password': '{0}'.format(password)}
    login_resp = session.post(config.NRL_LOGIN, json=data)
    if not json.loads(login_resp.text).get('success') == True:
        raise AussieAddonsException('Login failed')
    
    auth2_resp = session.get(config.NRL_AUTH, allow_redirects=False)
    redirect_url = auth2_resp.headers.get('Location')
    redirect_pieces = urlparse.urlsplit(redirect_url)
    redirect_query = dict(urlparse.parse_qsl(redirect_pieces.query))
    code = redirect_query.get('code')
    token_form = {'code': code}
    token_form.update(config.TOKEN_DATA)
    session.headers = {}
    session.cookies.clear()
    token_resp = session.post(config.NRL_TOKEN, data=token_form)
    refresh_token = json.loads(token_resp.text).get('refresh_token')
    session.headers.update({'Content-Type': 'application/xml'})
    ticket_signon = session.post(config.YINZCAM_AUTH_URL, data=config.NEW_LOGIN_DATA2.format(refresh_token))
    ticket = json.loads(ticket_signon.text).get('Ticket')
    return ticket


def get_free_token(username, password):
    """
    Obtain a valid token from Telstra/Yinzcam, will be used to make
    requests for Ooyala embed tokens
    """
    session = custom_session.Session(force_tlsv1=True)

    prog_dialog = xbmcgui.DialogProgress()
    prog_dialog.create('Logging in with Telstra ID')
    prog_dialog.update(1, 'Obtaining user token')

    # Send our first login request to Yinzcam, recieve (unactivated) token
    # and 'msisdn' URL

    session.headers = config.YINZCAM_AUTH_HEADERS
    ticket_resp = session.post(config.YINZCAM_AUTH_URL,
                             data=config.NEW_LOGIN_DATA1.format(uuid.uuid4()))
    ticket = json.loads(ticket_resp.text).get('Ticket')
    session.headers = {}
    session.headers.update({'X-YinzCam-Ticket': ticket})
    yinz_resp = session.get(config.YINZCAM_AUTH_URL2)
    jsondata = json.loads(yinz_resp.text)
    token = urllib.quote_plus(jsondata.get('TpUid'))
    if not token:
        raise TelstraAuthException('Unable to get token from NRL API')
    msisdn_url = jsondata.get('Url')
    msisdn_url = msisdn_url.replace('?tpUID', '.html?device=mobile&tpUID')
    prog_dialog.update(20, 'Signing on to telstra.com')

    # Sign in to telstra.com to recieve cookies, get the SAML auth, and
    # modify the escape characters so we can send it back later
    session.headers = config.SIGNON_HEADERS
    signon_data = config.SIGNON_DATA
    signon_data.update({'username': username, 'password': password})
    signon = session.post(config.SIGNON_URL, data=signon_data)

    signon_pieces = urlparse.urlsplit(signon.url)
    signon_query = dict(urlparse.parse_qsl(signon_pieces.query))

    utils.log('Sign-on result: %s' % signon_query)

    if 'errorcode' in signon_query:
        if signon_query['errorcode'] == '0':
            raise TelstraAuthException('Please enter your username '
                                       'in the settings')
        if signon_query['errorcode'] == '1':
            raise TelstraAuthException('Please enter your password '
                                       'in the settings')
        if signon_query['errorcode'] == '2':
            raise TelstraAuthException('Please enter your username and '
                                       'password in the settings')
        if signon_query['errorcode'] == '3':
            raise TelstraAuthException('Please check your username and '
                                       'password in the settings')
    soup = BeautifulSoup(signon.text, 'html.parser')
    saml_response = soup.find(attrs={'name': 'SAMLResponse'}).get('value')
    saml_base64 = urllib.quote(saml_response)
    prog_dialog.update(40, 'Obtaining API token')

    # Send the SAML login data and retrieve the auth token from the response
    session.headers = config.SAML_LOGIN_HEADERS
    session.cookies.set('saml_request_path', msisdn_url)
    saml_data = 'SAMLResponse=' + saml_base64
    utils.log('Fetching stream auth token: {0}'.format(config.SAML_LOGIN_URL))
    saml_login = session.post(config.SAML_LOGIN_URL, data=saml_data)

    confirm_url = saml_login.url
    auth_token_match = re.search('apiToken = "(\w+)"', saml_login.text)
    try:
        auth_token = auth_token_match.group(1)
    except AttributeError as e:
        utils.log('SAML login response: {0}'.format(saml_login.text))
        raise e
    prog_dialog.update(60, 'Determining eligible services')

    # 'Order' the subscription package to activate our token/login
    offer_id = dict(urlparse.parse_qsl(
                    urlparse.urlsplit(msisdn_url)[3]))['offerId']
    media_order_headers = config.MEDIA_ORDER_HEADERS
    media_order_headers.update(
        {'Authorization': 'Bearer {0}'.format(auth_token),
         'Referer': confirm_url})
    session.headers = media_order_headers
    # First check if there are any eligible services attached to the account
    try:
        offers = session.get(config.OFFERS_URL)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            message = json.loads(e.response.text).get('userMessage')
            message += (' Please visit {0} '.format(config.HUB_URL) +
                        'for further instructions to link your mobile '
                        'service to the supplied Telstra ID')
            raise TelstraAuthException(message)
        else:
            raise TelstraAuthException(e.response.status_code)
    try:
        offer_data = json.loads(offers.text)
        offers_list = offer_data['data']['offers']
        for offer in offers_list:
            if offer.get('name') != 'NRL Live Pass':
                continue
            data = offer.get('productOfferingAttributes')
            ph_no = [x['value'] for x in data if x['name'] == 'ServiceId'][0]
            if 'ph_no' not in locals():
                raise TelstraAuthException(
                    'Unable to determine if you have any eligible services. '
                    'Please ensure there is an eligible service linked to '
                    'your Telstra ID to redeem the free offer. Please visit '
                    '{0} for further instructions'.format(config.HUB_URL))
    except Exception as e:
        raise e
    prog_dialog.update(80, 'Obtaining Live Pass')
    order_data = config.MEDIA_ORDER_JSON.format(ph_no, offer_id, token)
    order = session.post(config.MEDIA_ORDER_URL, data=order_data)
    # check to make sure order has been placed correctly
    if order.status_code == 201:
        try:
            order_json = json.loads(order.text)
            status = order_json['data'].get('status') == 'COMPLETE'
            if status:
                utils.log('Order status complete')
        except:
            utils.log('Unable to check status of order, continuing anyway')

    session.close()
    prog_dialog.update(100, 'Finished!')
    prog_dialog.close()
    return ticket
