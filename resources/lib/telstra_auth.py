import binascii
import json
import os
import re
import requests
import uuid
import xbmcgui

from future.moves.urllib.parse import urlparse, urlsplit, parse_qsl

from resources.lib import config

from aussieaddonscommon.exceptions import AussieAddonsException
from aussieaddonscommon import session as custom_session
from aussieaddonscommon import utils

import xml.etree.ElementTree as ET


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
    session = custom_session.Session(force_tlsv1=False)
    auth_resp = session.get(config.NRL_AUTH, allow_redirects=False)

    xsrf = auth_resp.cookies['XSRF-TOKEN']
    session.headers.update({'x-xsrf-token': xsrf})

    data = {'emailAddress': '{0}'.format(username),
            'password': '{0}'.format(password)}
    login_resp = session.post(config.NRL_LOGIN, json=data)
    login_resp_json = json.loads(login_resp.text)
    if not login_resp_json.get('success') == True:  # noqa: E712
        raise TelstraAuthException(
            'Login failed for nrl.com: {0}'.format(
                login_resp_json.get('error')))

    auth2_resp = session.get(config.NRL_AUTH, allow_redirects=False)
    redirect_url = auth2_resp.headers.get('Location')
    redirect_pieces = urlsplit(redirect_url)
    redirect_query = dict(parse_qsl(redirect_pieces.query))
    code = redirect_query.get('code')
    token_form = {'code': code}
    token_form.update(config.TOKEN_DATA)
    session.headers = {}
    session.cookies.clear()
    token_resp = session.post(config.NRL_TOKEN, data=token_form)
    refresh_token = json.loads(token_resp.text).get('refresh_token')
    session.headers.update({'Content-Type': 'application/xml',
                            'Accept': 'application/json, text/plain, */*'})
    ticket_signon = session.post(
        config.YINZCAM_AUTH_URL,
        data=config.NEW_LOGIN_DATA2.format(refresh_token))
    ticket = json.loads(ticket_signon.text).get('Ticket')

    # check validity of subscription
    session.headers.update({'X-YinzCam-Ticket': ticket})
    sub_status = session.get(config.STATUS_URL)
    status_json = json.loads(sub_status.text)
    if status_json.get('Valid') != 'true':
        raise TelstraAuthException('NRL.com login failed: {0}'.format(
            status_json.get('Reason')))
    return ticket


def get_free_token(username, password):
    """
    Obtain a valid token from Telstra/Yinzcam, will be used to make
    requests for Ooyala embed tokens
    """
    session = custom_session.Session(force_tlsv1=False)
    prog_dialog = xbmcgui.DialogProgress()
    prog_dialog.create('Logging in with Telstra ID')

    # Send our first login request to Yinzcam, recieve (unactivated) ticket
    prog_dialog.update(1, 'Obtaining user ticket')
    adid = uuid.uuid4()
    deviceid = uuid.uuid4()
    session.headers = config.YINZCAM_AUTH_HEADERS
    ticket_resp = session.post(config.YINZCAM_AUTH_URL,
                               data=config.NEW_LOGIN_DATA1.format(
                                adid=adid, deviceid=deviceid))
    ticket_xml = ET.fromstring(ticket_resp.text)
    ticket = ticket_xml.find('Ticket').text
    session.headers = {'Accept': 'application/json, text/plain, */*'}
    session.headers.update({'X-YinzCam-Ticket': ticket})

    # Send ticket back and get 'sports pass confirmation' URL and 'TpUid'
    yinz_resp = session.get(config.YINZCAM_AUTH_URL2)
    jsondata = json.loads(yinz_resp.text)
    token = jsondata.get('TpUid')
    spc_url = jsondata.get('Url')
    if not token or not spc_url:
        raise TelstraAuthException('Unable to get token/spc url from NRL API')

    prog_dialog.update(16, 'Getting SSO Client ID')
    # GET to our spc url and receive SSO client ID
    session.headers = config.SPC_HEADERS
    spc_resp = session.get(spc_url)
    sso_token_match = re.search('ssoClientId = "(\w+)"', spc_resp.text)
    try:
        sso_token = sso_token_match.group(1)
    except AttributeError as e:
        utils.log('SPC login response: {0}'.format(spc_resp.text))
        raise e

    # Sign in to telstra.com with our SSO client id to get the url
    # for retrieving the bearer token for media orders
    prog_dialog.update(33, 'Signing on to telstra.com')
    sso_params = config.SSO_PARAMS
    sso_params.update({'client_id': sso_token,
                       'state': binascii.hexlify(os.urandom(16)),
                       'nonce': binascii.hexlify(os.urandom(16))})

    sso_auth_resp = session.get(config.SSO_URL, params=sso_params)
    sso_url = dict(parse_qsl(urlsplit(sso_auth_resp.url)[3])).get('goto')

    # login to telstra.com.au and get our BPSESSION cookie
    session.headers.update(config.SIGNON_HEADERS)
    signon_data = config.SIGNON_DATA
    signon_data = {'username': username, 'password': password, 'goto': sso_url}
    signon = session.post(config.SIGNON_URL,
                          data=signon_data,
                          allow_redirects=False)
    bp_session = session.cookies.get_dict().get('BPSESSION')

    # check signon is valid (correct username/password)

    signon_pieces = urlsplit(signon.headers.get('Location'))
    signon_query = dict(parse_qsl(signon_pieces.query))

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
            raise TelstraAuthException('Invalid Telstra ID username/password. '
                                       'Please check your username and '
                                       'password in the settings')

    # Use BPSESSION cookie to ask for bearer token
    sso_headers = config.SSO_HEADERS
    sso_headers.update({'Cookie': 'BPSESSION={0}'.format(bp_session)})
    session.headers = sso_headers
    sso_token_resp = session.get(sso_url)
    bearer_token = dict(parse_qsl(
                    urlsplit(sso_token_resp.url)[4]))['access_token']

    # First check if there are any eligible services attached to the account
    prog_dialog.update(50, 'Determining eligible services')
    offer_id = dict(parse_qsl(urlsplit(spc_url)[3]))['offerId']
    media_order_headers = config.MEDIA_ORDER_HEADERS
    media_order_headers.update(
        {'Authorization': 'Bearer {0}'.format(bearer_token)})
    session.headers = media_order_headers
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

    # 'Order' the subscription package to activate the service
    prog_dialog.update(66, 'Activating live pass on service')
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

    # Register the ticket
    prog_dialog.update(83, 'Registering live pass with ticket')
    session.headers = {'Accept': 'application/json',
                       'Accept-Encoding': 'gzip',
                       'Connection': 'Keep-Alive',
                       'User-Agent': 'okhttp/3.4.1',
                       'X-YinzCam-AppID': 'NRL_LIVE',
                       'X-YinzCam-Ticket': ticket}
    session.get(config.YINZ_CALLBACK_URL.format(token), allow_redirects=False)

    # Confirm everything has gone well
    prog_dialog.update(100, 'Checking status of Live Pass')
    sub_status = session.get(config.STATUS_URL)
    status_json = json.loads(sub_status.text)
    if status_json.get('Valid') != 'true':
        raise TelstraAuthException('Telstra ID activation failed: {0}'.format(
            status_json.get('Reason')))
    session.close()
    prog_dialog.update(100, 'Finished!')
    prog_dialog.close()
    return ticket


def get_mobile_token():
    session = custom_session.Session(force_tlsv1=False)
    prog_dialog = xbmcgui.DialogProgress()
    prog_dialog.create('Logging in with Telstra ID')

    # Send our first login request to Yinzcam, recieve (unactivated) ticket
    prog_dialog.update(1, 'Obtaining user ticket')
    adid = uuid.uuid4()
    deviceid = uuid.uuid4()
    session.headers = config.YINZCAM_AUTH_HEADERS
    ticket_resp = session.post(config.YINZCAM_AUTH_URL,
                               data=config.NEW_LOGIN_DATA1.format(
                                adid=adid, deviceid=deviceid))
    ticket_xml = ET.fromstring(ticket_resp.text)
    ticket = ticket_xml.find('Ticket').text
    session.headers = {'Accept': 'application/json, text/plain, */*',
                       'X-YinzCam-Ticket': ticket}

    # Send ticket back and get 'sports pass confirmation' URL and 'TpUid'
    yinz_resp = session.get(config.YINZCAM_AUTH_URL2)
    jsondata = json.loads(yinz_resp.text)
    token = jsondata.get('TpUid')
    spc_url = jsondata.get('Url')
    if not token or not spc_url:
        raise TelstraAuthException('Unable to get token/spc url from NRL API')

    prog_dialog.update(20, 'Obtaining mobile token')
    mobile_userid_cookies = session.get(
        config.MOBILE_ID_URL).cookies.get_dict()
    mobile_userid = mobile_userid_cookies.get('GUID_S')

    if not mobile_userid or mobile_userid_cookies.get('nouid'):
        raise TelstraAuthException('Not connected to Telstra Mobile network. '
                                   'Please disable WiFi and enable mobile '
                                   'data if on a Telstra mobile device, or '
                                   "connect this device's WiFi to a device "
                                   'that is on the Telstra Mobile network '
                                   'and try again.')

    data = config.MOBILE_TOKEN_PARAMS
    data.update({'x-user-id': mobile_userid})
    mobile_token_resp = session.post(config.OAUTH_URL, data=data)
    bearer_token = json.loads(mobile_token_resp.text).get('access_token')

    # First check if there are any eligible services attached to the account
    prog_dialog.update(40, 'Determining eligible services')
    session.headers = config.OAUTH_HEADERS
    session.headers.update(
        {'Authorization': 'Bearer {0}'.format(bearer_token)})
    try:
        offers = session.get(config.OLD_OFFERS_URL)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            message = json.loads(e.response.text).get('userMessage')
            raise TelstraAuthException(message)
        else:
            raise TelstraAuthException(e)
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

    # 'Order' the subscription package to activate the service
    prog_dialog.update(60, 'Activating live pass on service')
    order_data = config.MOBILE_ORDER_JSON
    order_data.update({'serviceId': ph_no, 'pai': token})
    order = session.post(config.OLD_MEDIA_ORDER_URL, json=order_data)

    # check to make sure order has been placed correctly
    prog_dialog.update(80, 'Confirming activation')
    if order.status_code == 201:
        try:
            order_json = json.loads(order.text)
            status = order_json['data'].get('status') == 'COMPLETE'
            if status:
                utils.log('Order status complete')
        except:
            utils.log('Unable to check status of order, continuing anyway')
    # Register the ticket
    prog_dialog.update(83, 'Registering live pass with ticket')
    session.headers = {'Accept': 'application/json',
                       'Accept-Encoding': 'gzip',
                       'Connection': 'Keep-Alive',
                       'User-Agent': 'okhttp/3.4.1',
                       'X-YinzCam-AppID': 'NRL_LIVE',
                       'X-YinzCam-Ticket': ticket}
    session.get(config.YINZ_CALLBACK_URL.format(token), allow_redirects=False)

    # Confirm everything has gone well
    prog_dialog.update(100, 'Checking status of Live Pass')
    sub_status = session.get(config.STATUS_URL)
    status_json = json.loads(sub_status.text)
    if status_json.get('Valid') != 'true':
        raise TelstraAuthException('Telstra ID activation failed: {0}'.format(
            status_json.get('Reason')))
    session.close()
    prog_dialog.update(100, 'Finished!')
    prog_dialog.close()
    return ticket
