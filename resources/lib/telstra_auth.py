import base64
import binascii
import hashlib
import json
import os
import random
import re
import uuid
import xml.etree.ElementTree as ET

from future.moves.urllib.parse import parse_qsl, urlparse, urlsplit

import requests

from aussieaddonscommon import session as custom_session
from aussieaddonscommon import utils
from aussieaddonscommon.exceptions import AussieAddonsException

from resources.lib import config

import xbmcgui


class TelstraAuthException(AussieAddonsException):
    """Telstra Auth exception
    This exception can be thrown with the reportable arg set which can
    determine whether or not it is allowed to be sent as an automatic
    error report
    """
    pass


class TelstraAuth(object):
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.session = custom_session.Session(force_tlsv1=False)
        self.prog_dialog = xbmcgui.DialogProgress()

    def get_code_verifier(self):
        letters = 'abcdef0123456789'
        verifier = ''.join(random.choice(letters) for i in range(64))
        return verifier.encode('utf-8')

    def get_code_challenge(self, verifier):
        code_challenge_digest = hashlib.sha256(verifier).digest()
        code_challenge = base64.b64encode(code_challenge_digest, b'-_').rstrip(
            b'=')
        return code_challenge

    def create_dialog(self, msg):
        self.prog_dialog.create(msg)

    def get_paid_token(self):
        """
        Obtain a valid token from Telstra/Yinzcam, will be used to make
        requests for Ooyala embed tokens
        """
        session = custom_session.Session(force_tlsv1=False)
        self.code_verifier = self.get_code_verifier()
        params = config.NRL_AUTH_PARAMS
        params.update({'scope': base64.b64encode(os.urandom(16)).rstrip('='),
                       'code_challenge': self.get_code_challenge(
                           self.code_verifier)})
        auth_resp = session.get(config.NRL_AUTH, params=params, allow_redirects=False)

        xsrf = auth_resp.cookies['XSRF-TOKEN']
        session.headers.update({'x-xsrf-token': xsrf})

        data = {'emailAddress': '{0}'.format(self.username),
                'password': '{0}'.format(self.password)}
        login_resp = session.post(config.NRL_LOGIN, json=data)
        login_resp_json = json.loads(login_resp.text)
        if not login_resp_json.get('success') == True:  # noqa: E712
            raise TelstraAuthException(
                'Login failed for nrl.com: {0}'.format(
                    login_resp_json.get('error')))

        auth2_resp = session.get(config.NRL_AUTH_ACCEPT,
                                 params=params,
                                 allow_redirects=False)
        redirect_url = auth2_resp.headers.get('location')
        redirect_pieces = urlsplit(redirect_url)
        redirect_query = dict(parse_qsl(redirect_pieces.query))
        code = redirect_query.get('code')
        token_form = {'code': code,
                      'code_verifier': self.code_verifier}
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

    def set_ticket(self):
        adid = uuid.uuid4()
        deviceid = uuid.uuid4()
        self.session.headers = config.YINZCAM_AUTH_HEADERS
        ticket_resp = self.session.post(config.YINZCAM_AUTH_URL,
                                        data=config.NEW_LOGIN_DATA1.format(
                                            adid=adid, deviceid=deviceid))
        ticket_xml = ET.fromstring(ticket_resp.text)
        self.ticket = ticket_xml.find('Ticket').text
        self.session.headers = {'Accept': 'application/json, text/plain, */*'}
        self.session.headers.update({'X-YinzCam-Ticket': self.ticket})

    def set_spc_url_and_tpuid(self):
        """
        Send ticket back and get 'sports pass confirmation' URL and 'TpUid'
        :return:
        """
        yinz_resp = self.session.get(config.YINZCAM_AUTH_URL2)
        jsondata = json.loads(yinz_resp.text)
        self.token = jsondata.get('TpUid')
        self.spc_url = jsondata.get('Url')
        if not self.token or not self.spc_url:
            raise TelstraAuthException(
                'Unable to get token/spc url from NRL API')

    def set_sso_client_id(self):
        """
        GET to our spc url and receive SSO client ID
        :return:
        """
        self.session.headers = config.SPC_HEADERS
        spc_resp = self.session.get(self.spc_url)
        sso_token_match = re.search('ssoClientId = "(\\w+)"', spc_resp.text)
        try:
            self.sso_client_id = sso_token_match.group(1)
        except AttributeError as e:
            utils.log('SPC login response: {0}'.format(spc_resp.text))
            raise e

    def set_identity_path_token(self):
        self.code_verifier = self.get_code_verifier()
        myid_oauth_params = dict(config.MYID_AUTH_PARAMS)
        myid_oauth_params.update({'client_id': self.sso_client_id,
                                  'state': binascii.b2a_hex(os.urandom(16)),
                                  'code_challenge': self.get_code_challenge(
                                      self.code_verifier)})
        myid_auth = self.session.get(config.MYID_AUTHORIZATION_URL,
                                     params=myid_oauth_params)

        identify_path_match = re.search('action="/identity/as/(\\w+)/',
                                        myid_auth.text)
        try:
            self.identify_path_token = identify_path_match.group(1)
        except AttributeError as e:
            raise e

    def set_myid_auth_resume_resp_text(self):
        myid_auth_resume_data = dict(config.MYID_AUTH_RESUME_DATA)
        myid_auth_resume_data.update(
            {'pf.username': self.username, 'pf.pass': self.password})
        myid_auth_resume = self.session.post(
            config.MYID_RESUME_AUTHORIZATION_URL.format(
                self.identify_path_token),
            data=myid_auth_resume_data)
        self.myid_auth_resume_resp_text = myid_auth_resume.text

    def validate_myid_auth(self):
        auth_page_title_match = re.search('<title>(.*?)</title>',
                                          self.myid_auth_resume_resp_text)
        try:
            auth_page_title = auth_page_title_match.group(1)
            if auth_page_title == 'Sign in to Telstra with your Telstra ID':
                raise TelstraAuthException(
                    'Invalid Telstra ID username or password')
        except AttributeError as e:
            raise e

    def signon_to_sso_sessions(self):
        sso_session_cookie = self.session.cookies.get_dict().get('SSOSession')
        for url in config.SSO_SESSION_HANDLER_URLS:
            self.session.post(url, data={'SSOCookie': sso_session_cookie})

    def set_callback_code(self):
        """
        get oauth code
        :return:
        """
        myid_signon_proceed = self.session.get(
            config.MYID_RESUME_AUTHORIZATION_URL.format(
                self.identify_path_token),
            params={'ctfr-proceed': 'true'})
        query = urlparse(myid_signon_proceed.url).query
        self.callback_code = dict(parse_qsl(query)).get('code')

    def set_bearer_token(self):
        """
        finally get access token
        :return:
        """
        token_params = dict(config.MYID_TOKEN_PARAMS)

        token_params.update({'client_id': self.sso_client_id,
                             'code': self.callback_code,
                             'code_verifier': self.code_verifier})
        token_resp = self.session.post(config.MYID_TOKEN_URL,
                                       data=token_params)
        self.bearer_token = json.loads(token_resp.text).get('access_token')

    def set_offers_resp(self):
        """
        First check if there are any eligible services attached to the
        account
        :return:
        """
        media_order_headers = config.MEDIA_ORDER_HEADERS

        media_order_headers.update(
            {'Authorization': 'Bearer {0}'.format(self.bearer_token)})
        self.session.headers = media_order_headers

        try:
            self.offers = self.session.get(config.OFFERS_URL)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                message = json.loads(e.response.text).get('userMessage')
                message += (' Please visit {0} '.format(config.HUB_URL) +
                            'for further instructions to link your mobile '
                            'service to the supplied Telstra ID')
                raise TelstraAuthException(message)
            else:
                raise TelstraAuthException(e)

    def set_ph_no_list(self):
        try:
            offer_data = json.loads(self.offers.text)
            offers_list = offer_data['data']['offers']
            self.ph_no_list = []

            for offer in offers_list:
                if offer.get('name') != 'NRL Live Pass':
                    continue
                data = offer.get('productOfferingAttributes')
                serv_id = \
                    [x['value'] for x in data if x['name'] == 'ServiceId'][0]
                self.ph_no_list.append(serv_id)

            if len(self.ph_no_list) == 0:
                raise TelstraAuthException(
                    'Unable to determine if you have any eligible services. '
                    'Please ensure there is an eligible service linked to '
                    'your Telstra ID to redeem the free offer. Please visit '
                    '{0} for further instructions'.format(config.HUB_URL))
        except Exception as e:
            raise e

    def _order(self, ph_no):
        try:
            order_data = config.MEDIA_ORDER_JSON.format(ph_no,
                                                        config.OFFER_ID,
                                                        self.token)
            order = self.session.post(config.MEDIA_ORDER_URL,
                                      data=order_data)
            self.last_order_response = order
            # check to make sure order has been placed correctly
            if order.status_code == 201:
                try:
                    order_json = json.loads(order.text)
                    status = order_json['data'].get('status') == 'COMPLETE'
                    if status:
                        utils.log('Order status complete')
                        return True
                except Exception:
                    utils.log(
                        'Unable to check status of order, continuing')
        except requests.exceptions.HTTPError as e:
            utils.log(
                'Error {0} on order post'.format(e.response.status_code))
            self.last_order_response = e.response

    def order_subscription(self):
        """
        'Order' the subscription package to activate the service
        :return:
        """
        for ph_no in self.ph_no_list:
            if self._order(ph_no):
                break

        if str(self.last_order_response.status_code)[0] != '2':
            self.last_order_response.raise_for_status()

    def register_ticket(self):
        """
        Register the ticket
        :return:
        """
        self.session.headers = {'Accept': 'application/json',
                                'Accept-Encoding': 'gzip',
                                'Connection': 'Keep-Alive',
                                'User-Agent': 'okhttp/3.4.1',
                                'X-YinzCam-AppID': 'NRL_LIVE',
                                'X-YinzCam-Ticket': self.ticket}
        self.session.get(config.YINZ_CALLBACK_URL.format(self.token),
                         allow_redirects=False)

    def confirm_subscription(self):
        """
        Confirm everything has gone well
        :return:
        """
        sub_status = self.session.get(config.STATUS_URL)
        status_json = json.loads(sub_status.text)
        if status_json.get('Valid') != 'true':
            raise TelstraAuthException(
                'Telstra ID activation failed: {0}'.format(
                    status_json.get('Reason')))

    def get_free_token(self):
        """
        Obtain a valid token from Telstra/Yinzcam, will be used to make
        requests for Ooyala embed tokens
        """
        self.create_dialog('Activating live pass via free offer')

        self.prog_dialog.update(1, 'Obtaining user ticket')
        self.set_ticket()
        self.set_spc_url_and_tpuid()

        self.prog_dialog.update(16, 'Getting SSO Client ID')
        self.set_sso_client_id()

        self.prog_dialog.update(40,
                                'Signing in with Telstra ID username/password')
        self.set_identity_path_token()
        self.set_myid_auth_resume_resp_text()
        self.validate_myid_auth()
        self.signon_to_sso_sessions()

        self.prog_dialog.update(50, 'Getting OAuth access token')
        self.set_callback_code()
        self.set_bearer_token()

        self.prog_dialog.update(60, 'Determining eligible services')
        self.set_offers_resp()
        self.set_ph_no_list()

        self.prog_dialog.update(80, 'Activating live pass on service')
        self.order_subscription()

        self.prog_dialog.update(83, 'Registering live pass with ticket')
        self.register_ticket()

        self.prog_dialog.update(95, 'Checking status of Live Pass')
        self.confirm_subscription()

        self.session.close()
        self.prog_dialog.update(100, 'Finished!')
        self.prog_dialog.close()
        return self.ticket

    # Mobile
    def set_mobile_id(self):
        mobile_userid_resp = self.session.get(config.MOBILE_ID_URL)
        mobile_userid_cookies = mobile_userid_resp.cookies.get_dict()
        self.mobile_userid = mobile_userid_cookies.get('GUID_S')
        if not self.mobile_userid or mobile_userid_cookies.get('nouid'):
            raise TelstraAuthException(
                'Not connected to Telstra Mobile network. '
                'Please disable WiFi and enable mobile '
                'data if on a Telstra mobile device, or '
                "connect this device's WiFi to a device "
                'that is on the Telstra Mobile network '
                'and try again.')

    def set_mobile_bearer_token(self):
        data = config.MOBILE_TOKEN_PARAMS
        data.update({'x-user-id': self.mobile_userid})
        mobile_token_resp = self.session.post(config.MOBILE_OAUTH_URL,
                                              data=data)
        self.bearer_token = json.loads(mobile_token_resp.text).get(
            'access_token')

    def get_mobile_token(self):
        self.prog_dialog.create('Activating live pass via mobile network')

        self.prog_dialog.update(1, 'Obtaining user ticket')
        self.set_ticket()
        self.set_spc_url_and_tpuid()

        self.prog_dialog.update(20, 'Obtaining mobile token')
        self.set_mobile_id()
        self.set_mobile_bearer_token()

        self.prog_dialog.update(40, 'Determining eligible services')
        self.set_offers_resp()
        self.set_ph_no_list()

        self.prog_dialog.update(60, 'Activating live pass on service')
        self.order_subscription()

        self.prog_dialog.update(80, 'Registering live pass with ticket')
        self.register_ticket()

        self.prog_dialog.update(95, 'Checking status of Live Pass')
        self.confirm_subscription()

        self.session.close()
        self.prog_dialog.update(100, 'Finished!')
        self.prog_dialog.close()
        return self.ticket
