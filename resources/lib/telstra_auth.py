import config
import datetime
import json
import re
import requests
import urllib
import urlparse
import uuid
import xbmcgui

import os, binascii

from aussieaddonscommon.exceptions import AussieAddonsException
from aussieaddonscommon import session as custom_session
from aussieaddonscommon import utils

import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


class TelstraAuthException(AussieAddonsException):
    """Telstra Auth exception
    This exception can be thrown with the reportable arg set which can
    determine whether or not it is allowed to be sent as an automatic
    error report
    """
    pass


def make_hex32():
    return binascii.b2a_hex(os.urandom(16))


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
    login_resp_json = json.loads(login_resp.text)
    if not login_resp_json.get('success') == True:  # noqa: E712
        raise AussieAddonsException(
            'Login failed for nrl.com: {0}'.format(
                login_resp_json.get('error')))

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
    ticket_signon = session.post(
        config.YINZCAM_AUTH_URL,
        data=config.NEW_LOGIN_DATA2.format(refresh_token))
    ticket = json.loads(ticket_signon.text).get('Ticket')
    return ticket


def get_free_token(username, password):
    """
    Obtain a valid token from Telstra/Yinzcam, will be used to make
    requests for Ooyala embed tokens
    """
    #time_format = '%Y-%m-%dT%H:%M:%SZ'
    #current_time = datetime.datetime.utcnow()
    #req_time = current_time - datetime.timedelta(0, 30)
    #invis_time = req_time + datetime.timedelta(0, 2)
    adid = uuid.uuid4()
    deviceid = uuid.uuid4()
    #sessionid = uuid.uuid4()
    #minorid = uuid.uuid4()
    
    session = custom_session.Session(force_tlsv1=True)
    
    #analytics_data = config.ANALYTICS_DATA.format(
    #    sessionid=sessionid,
    #    adid=adid,
    #    deviceid=deviceid,
    #    minorid=minorid,
    #    time=req_time.strftime(time_format),
    #    invisibletime=invis_time.strftime(time_format),
    #    currenttime=current_time.strftime(time_format))
        
    #session.post(config.ANALYTICS_URL, data=analytics_data)
    
    prog_dialog = xbmcgui.DialogProgress()
    prog_dialog.create('Logging in with Telstra ID')
    prog_dialog.update(1, 'Obtaining user token')

    # Send our first login request to Yinzcam, recieve (unactivated) token
    # and 'msisdn' URL

    session.headers = config.YINZCAM_AUTH_HEADERS
    ticket_resp = session.post(config.YINZCAM_AUTH_URL,
                               data=config.NEW_LOGIN_DATA1.format(
                                adid=adid, deviceid=deviceid))
    ticket_xml = ET.fromstring(ticket_resp.text)
    ticket = ticket_xml.find('Ticket').text
    session.headers = {}
    session.headers.update({'X-YinzCam-Ticket': ticket})
    yinz_resp = session.get(config.YINZCAM_AUTH_URL2)
    jsondata = json.loads(yinz_resp.text)
    token = jsondata.get('TpUid')
    if not token:
        raise TelstraAuthException('Unable to get token from NRL API')
    spc_url = jsondata.get('Url')
    #msisdn_url = msisdn_url.replace('?tpUID', '.html?device=mobile&tpUID')
    
    session.headers = config.SPC_HEADERS
    spc_resp = session.get(spc_url)
    
    sso_token_match = re.search('ssoClientId = "(\w+)"', spc_resp.text)
    #callback_match = re.search('defaultReturnUrl = "(\w+)"', spc_resp.text)
    try:
        sso_token = sso_token_match.group(1)
        callback_url = 'https://hub.telstra.com.au/offers/content/cached/callback.html'
        #callback_url = callback_match.group(1)
    except AttributeError as e:
        utils.log('SPC login response: {0}'.format(spc_resp.text))
        raise e
    
    prog_dialog.update(20, 'Signing on to telstra.com')
    
    
    
    sso_params = {'client_id': sso_token,
              'redirect_uri': callback_url,
              'response_type': 'id_token token',
              'scope': 'openid email profile phone telstra.user.sso.profile',
              'prompt': 'none',
              'state': make_hex32(),
              'nonce': make_hex32()}
    
    sso_resp = session.get(config.SSO_URL, params=sso_params)
    print sso_resp.text
    sso_params.pop('prompt')
    sso_params.update({'state': make_hex32(),
              'nonce': make_hex32()})
    sso_resp2 = session.get(config.SSO_URL, params=sso_params)
    goto_url = dict(urlparse.parse_qsl(
                    urlparse.urlsplit(sso_resp2.url)[3]))['goto']
    
        
    #telstra_cookies = session.cookies
    # Sign in to telstra.com to recieve cookies, get the SAML auth, and
    # modify the escape characters so we can send it back later
    session.headers.update(config.SIGNON_HEADERS)
    signon_data = config.SIGNON_DATA
    signon_data = {'username': username, 'password': password, 'goto': goto_url}
    
    #session.cookies = telstra_cookies
    #print telstra_cookies
    try:
        signon = session.post(config.SIGNON_URL, data=signon_data)
    except requests.exceptions.HTTPError as e:
        sso_url = e.response.url
        telstra_cookies = {}
        for cookie in session.cookies:
            telstra_cookies.update({cookie.name: cookie.value})
        print telstra_cookies
    print sso_url
    sso_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, '
                                  'deflate',
               'Accept-Language': 'en-AU,en-US;q=0.9',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Cookie': 'BPSESSION={0}'.format(telstra_cookies['BPSESSION']),
               'Referer': 'https://signon.telstra.com.au/login?goto=https%3A%2F%2Fapi.telstra.com%2Fv1%2Fsso%2Fidpcallback%3Fcbs%3DeyJhbGciOiJIUzI1NiJ9.eyJjYWxsYmFja19zdGF0ZSI6IjEyMjcyMDQ3LWU3N2ItNGRiZC1hNGZiLTBlYTcwMDMyYmRlMSIsImF1ZCI6InJhYSIsImV4cCI6MTUyMDczNTMyMTk0OCwiaWF0IjoxNTIwNjQ4OTIxOTQ4fQ.-I05HQE9eIpRS0LLSYB_pJ4iVKZZzyziVYarvjCe_2o%26app_name%3DOne%20Place%20portal',
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
    session.headers = sso_headers
    s2 = session.get(sso_url)

    """signon_pieces = urlparse.urlsplit(signon.url)
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
    saml_base64 = urllib.quote(saml_response)"""
    prog_dialog.update(40, 'Obtaining API token')

    # Send the SAML login data and retrieve the auth token from the response
    """session.headers = config.SAML_LOGIN_HEADERS
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
        raise e"""
    prog_dialog.update(60, 'Determining eligible services')

    # 'Order' the subscription package to activate our token/login
    offer_id = dict(urlparse.parse_qsl(
                    urlparse.urlsplit(spc_url)[3]))['offerId']
    media_order_headers = config.MEDIA_ORDER_HEADERS
    media_order_headers.update(
        {'Authorization': 'Bearer {0}'.format(sso_token)})#,
         #'Referer': confirm_url})
    session.headers = media_order_headers
    
    
    entitlements = session.get(config.ENTITLEMENTS_URL)
    #for ent in json.loads(entitlements.text).get('entitlements'):
    #    if ent.get('status') == 'Active':
    #        token = ent.get('pai')
    #        ph_no = ent.get('serviceId').replace('61', '0')
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
        ph_no = None
        for offer in offers_list:
            if offer.get('name') != 'NRL Live Pass':
                continue
            data = offer.get('productOfferingAttributes')
            ph_no = [x['value'] for x in data if x['name'] == 'ServiceId'][0]
        if not ph_no:
            raise TelstraAuthException(
                'Unable to determine if you have any eligible services. '
                'Please ensure there is an eligible service linked to '
                'your Telstra ID to redeem the free offer. Please visit '
                '{0} for further instructions'.format(config.HUB_URL))
    except Exception as e:
        raise e
    prog_dialog.update(80, 'Obtaining Live Pass')
    order_data = config.MEDIA_ORDER_JSON.format(ph_no, offer_id, token)
    order = session.post(config.MEDIA_ORDER_URL, data=order_data, allow_redirects=False)
    order_get = session.get(config.MEDIA_ORDER_URL)
    
    
    # check to make sure order has been placed correctly
    if order.status_code == 201:
        try:
            order_json = json.loads(order.text)
            status = order_json['data'].get('status') == 'COMPLETE'
            if status:
                utils.log('Order status complete')
        except:
            utils.log('Unable to check status of order, continuing anyway')
    
    
    session.headers={                                                                     'Accept': 'application/json',
                                                                           'Accept-Encoding': 'gzip',
                                                                           'Connection': 'Keep-Alive',
                                                                           'User-Agent': 'okhttp/3.4.1',
                                                                           'X-YinzCam-AppID': 'NRL_LIVE',
                                                                           'X-YinzCam-Ticket': ticket}

    
    sub_status = session.get(config.STATUS_URL)
    print sub_status.text
    prof_data = session.post(config.YINZCAM_PROFILE, json=config.PROFILE_DATA)
    print prof_data.url
    session.close()
    prog_dialog.update(100, 'Finished!')
    prog_dialog.close()
    return ticket
