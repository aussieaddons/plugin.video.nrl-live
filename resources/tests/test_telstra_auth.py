from __future__ import absolute_import, unicode_literals

import io
import json
import os
try:
    import mock
except ImportError:
    import unittest.mock as mock

import responses

import testtools

import resources.lib.config as config
import resources.lib.telstra_auth as telstra_auth
from resources.tests.fakes import fakes


class TelstraAuthTests(testtools.TestCase):
    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/NRL_TOKEN.json'),
                  'rb') as f:
            self.NRL_TOKEN_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/json/OFFERS_RESP.json'),
                  'rb') as f:
            self.OFFERS_RESP_JSON = io.BytesIO(f.read()).read()
        with open(
                os.path.join(cwd, 'fakes/json/OFFERS_FAIL_RESP.json'),
                'rb') as f:
            self.OFFERS_FAIL_RESP_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/json/ORDER_RESP.json'),
                  'rb') as f:
            self.ORDER_RESP_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/json/STATUS_RESP.json'),
                  'rb') as f:
            self.STATUS_RESP_JSON = io.BytesIO(f.read()).read()
        with open(
                os.path.join(cwd, 'fakes/json/STATUS_FAIL_RESP.json'),
                'rb') as f:
            self.STATUS_FAIL_RESP_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/YINZCAM_AUTH_RESP.xml'),
                  'rb') as f:
            self.YINZCAM_AUTH_RESP_XML = io.BytesIO(f.read()).read()
        with open(
                os.path.join(cwd, 'fakes/json/YINZCAM_AUTH_RESP.json'),
                'rb') as f:
            self.YINZCAM_AUTH_RESP_JSON = io.BytesIO(f.read()).read()
        with open(
                os.path.join(cwd, 'fakes/json/YINZCAM_AUTH2_RESP.json'),
                'rb') as f:
            self.YINZCAM_AUTH2_RESP_JSON = io.BytesIO(f.read()).read()
        with open(
                os.path.join(cwd, 'fakes/html/SPC_RESP.html'),
                'rb') as f:
            self.SPC_RESP_HTML = io.BytesIO(f.read()).read()

    @responses.activate
    def test_get_paid_token(self):
        def auth_callback(request):
            headers = {}
            if 'x-xsrf-token' in request.headers:
                location = fakes.AUTH_REDIRECT_CODE_URL
            else:
                headers.update({'Set-Cookie': fakes.FAKE_XSRF_COOKIE})
                location = fakes.AUTH_REDIRECT_URL
            headers.update({'Location': location})
            return (302, headers, '')

        def login_callback(request):
            payload = json.loads(request.body)
            if (payload.get('emailAddress') == 'foo' and payload.get(
                    'password') == 'bar'):
                body = json.dumps({'success': True})
            else:
                body = json.dumps(
                    {'success': False,
                     'error': 'Invalid email address or password'})
            return (200, {}, body)

        responses.add_callback(responses.GET, config.NRL_AUTH,
                               callback=auth_callback)
        responses.add_callback(responses.POST, config.NRL_LOGIN,
                               callback=login_callback)
        responses.add(responses.POST, config.NRL_TOKEN,
                      body=self.NRL_TOKEN_JSON,
                      status=200)
        responses.add(responses.POST, config.YINZCAM_AUTH_URL.format(
            json.loads(self.NRL_TOKEN_JSON).get('refresh_token')),
                      body=self.YINZCAM_AUTH_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.STATUS_URL,
                      body=self.STATUS_RESP_JSON,
                      status=200)
        observed = telstra_auth.get_paid_token('foo', 'bar')
        self.assertEqual('ticket123', observed)

    @responses.activate
    def test_get_paid_token_fail_userpass(self):
        def auth_callback(request):
            headers = {}
            if 'x-xsrf-token' in request.headers:
                location = fakes.AUTH_REDIRECT_CODE_URL
            else:
                headers.update({'Set-Cookie': fakes.FAKE_XSRF_COOKIE})
                location = fakes.AUTH_REDIRECT_URL
            headers.update({'Location': location})
            return (302, headers, '')

        def login_callback(request):
            payload = json.loads(request.body)
            if (payload.get('emailAddress') == 'foo' and payload.get(
                    'password') == 'bar'):
                body = json.dumps({'success': True})
            else:
                body = json.dumps(
                    {'success': False,
                     'error': 'Invalid email address or password'})
            return (200, {}, body)

        responses.add_callback(responses.GET, config.NRL_AUTH,
                               callback=auth_callback)
        responses.add_callback(responses.POST, config.NRL_LOGIN,
                               callback=login_callback)
        responses.add(responses.POST, config.NRL_TOKEN,
                      body=self.NRL_TOKEN_JSON,
                      status=200)
        responses.add(responses.POST, config.YINZCAM_AUTH_URL.format(
            json.loads(self.NRL_TOKEN_JSON).get('refresh_token')),
                      body=self.YINZCAM_AUTH_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.STATUS_URL,
                      body=self.STATUS_RESP_JSON,
                      status=200)
        self.assertRaises(telstra_auth.TelstraAuthException,
                          telstra_auth.get_paid_token, 'foo', 'wrongpassword')

    @responses.activate
    def test_get_paid_token_fail_status(self):
        def auth_callback(request):
            headers = {}
            if 'x-xsrf-token' in request.headers:
                location = fakes.AUTH_REDIRECT_CODE_URL
            else:
                headers.update({'Set-Cookie': fakes.FAKE_XSRF_COOKIE})
                location = fakes.AUTH_REDIRECT_URL
            headers.update({'Location': location})
            return (302, headers, '')

        def login_callback(request):
            payload = json.loads(request.body)
            if (payload.get('emailAddress') == 'foo' and payload.get(
                    'password') == 'bar'):
                body = json.dumps({'success': True})
            else:
                body = json.dumps(
                    {'success': False,
                     'error': 'Invalid email address or password'})
            return (200, {}, body)

        responses.add_callback(responses.GET, config.NRL_AUTH,
                               callback=auth_callback)
        responses.add_callback(responses.POST, config.NRL_LOGIN,
                               callback=login_callback)
        responses.add(responses.POST, config.NRL_TOKEN,
                      body=self.NRL_TOKEN_JSON,
                      status=200)
        responses.add(responses.POST, config.YINZCAM_AUTH_URL.format(
            json.loads(self.NRL_TOKEN_JSON).get('refresh_token')),
                      body=self.YINZCAM_AUTH_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.STATUS_URL,
                      body=self.STATUS_FAIL_RESP_JSON,
                      status=200)
        self.assertRaises(telstra_auth.TelstraAuthException,
                          telstra_auth.get_paid_token, 'foo', 'bar')

    @responses.activate
    @mock.patch('os.urandom')
    @mock.patch('uuid.uuid4')
    def test_get_free_token(self, mock_uuid, mock_random):
        mock_uuid.side_effect = fakes.FAKE_UUID
        mock_random.side_effect = fakes.FAKE_RANDOM
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET,
                      json.loads(self.YINZCAM_AUTH2_RESP_JSON).get('Url'),
                      body=self.SPC_RESP_HTML,
                      status=200)
        responses.add(responses.GET, config.SSO_URL,
                      headers={'Location': fakes.SSO_AUTH_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_AUTH_REDIRECT_URL,
                      status=200)
        responses.add(responses.POST, config.SIGNON_URL,
                      headers={'Set-Cookie': fakes.FAKE_BPSESSION_COOKIE,
                               'Location': fakes.SIGNON_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_URL,
                      headers={'Location': fakes.SSO_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_REDIRECT_URL,
                      status=200)
        responses.add(responses.GET, config.OFFERS_URL,
                      body=self.OFFERS_RESP_JSON,
                      status=200)
        responses.add(responses.POST, config.MEDIA_ORDER_URL,
                      body=self.ORDER_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.YINZ_CALLBACK_URL.format(
            json.loads(self.YINZCAM_AUTH2_RESP_JSON).get('TpUid')),
                      headers={'Location': 'foo://bar'},
                      status=200)
        responses.add(responses.GET, config.STATUS_URL,
                      body=self.STATUS_RESP_JSON,
                      status=200)
        observed = telstra_auth.get_free_token('foo', 'bar')
        self.assertEqual('ticket123', observed)

    @responses.activate
    @mock.patch('os.urandom')
    @mock.patch('uuid.uuid4')
    def test_get_free_token_fail_userpass(self, mock_uuid, mock_random):
        mock_uuid.side_effect = fakes.FAKE_UUID
        mock_random.side_effect = fakes.FAKE_RANDOM
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET,
                      json.loads(self.YINZCAM_AUTH2_RESP_JSON).get('Url'),
                      body=self.SPC_RESP_HTML,
                      status=200)
        responses.add(responses.GET, config.SSO_URL,
                      headers={'Location': fakes.SSO_AUTH_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_AUTH_REDIRECT_URL,
                      status=200)
        responses.add(responses.POST, config.SIGNON_URL,
                      headers={'Set-Cookie': fakes.FAKE_BPSESSION_COOKIE,
                               'Location': fakes.SIGNON_FAIL_REDIRECT_URL},
                      status=302)
        self.assertRaises(telstra_auth.TelstraAuthException,
                          telstra_auth.get_free_token, 'foo', 'wrongpassword')

    @responses.activate
    @mock.patch('os.urandom')
    @mock.patch('uuid.uuid4')
    def test_get_free_token_fail_no_offer(self, mock_uuid, mock_random):
        mock_uuid.side_effect = fakes.FAKE_UUID
        mock_random.side_effect = fakes.FAKE_RANDOM
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET,
                      json.loads(self.YINZCAM_AUTH2_RESP_JSON).get('Url'),
                      body=self.SPC_RESP_HTML,
                      status=200)
        responses.add(responses.GET, config.SSO_URL,
                      headers={'Location': fakes.SSO_AUTH_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_AUTH_REDIRECT_URL,
                      status=200)
        responses.add(responses.POST, config.SIGNON_URL,
                      headers={'Set-Cookie': fakes.FAKE_BPSESSION_COOKIE,
                               'Location': fakes.SIGNON_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_URL,
                      headers={'Location': fakes.SSO_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_REDIRECT_URL,
                      status=200)
        responses.add(responses.GET, config.OFFERS_URL,
                      body=self.OFFERS_FAIL_RESP_JSON,
                      status=200)
        self.assertRaises(telstra_auth.TelstraAuthException,
                          telstra_auth.get_free_token, 'foo', 'bar')

    @responses.activate
    @mock.patch('os.urandom')
    @mock.patch('uuid.uuid4')
    def test_get_free_token_fail_no_eligible(self, mock_uuid, mock_random):
        mock_uuid.side_effect = fakes.FAKE_UUID
        mock_random.side_effect = fakes.FAKE_RANDOM
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET,
                      json.loads(self.YINZCAM_AUTH2_RESP_JSON).get('Url'),
                      body=self.SPC_RESP_HTML,
                      status=200)
        responses.add(responses.GET, config.SSO_URL,
                      headers={'Location': fakes.SSO_AUTH_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_AUTH_REDIRECT_URL,
                      status=200)
        responses.add(responses.POST, config.SIGNON_URL,
                      headers={'Set-Cookie': fakes.FAKE_BPSESSION_COOKIE,
                               'Location': fakes.SIGNON_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_URL,
                      headers={'Location': fakes.SSO_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_REDIRECT_URL,
                      status=200)
        responses.add(responses.GET, config.OFFERS_URL,
                      json={'userMessage': 'No eligible services'},
                      status=404)
        self.assertRaises(telstra_auth.TelstraAuthException,
                          telstra_auth.get_free_token, 'foo', 'bar')

    @responses.activate
    @mock.patch('os.urandom')
    @mock.patch('uuid.uuid4')
    def test_get_free_token_fail_not_activated(self, mock_uuid, mock_random):
        mock_uuid.side_effect = fakes.FAKE_UUID
        mock_random.side_effect = fakes.FAKE_RANDOM
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET,
                      json.loads(self.YINZCAM_AUTH2_RESP_JSON).get('Url'),
                      body=self.SPC_RESP_HTML,
                      status=200)
        responses.add(responses.GET, config.SSO_URL,
                      headers={'Location': fakes.SSO_AUTH_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_AUTH_REDIRECT_URL,
                      status=200)
        responses.add(responses.POST, config.SIGNON_URL,
                      headers={'Set-Cookie': fakes.FAKE_BPSESSION_COOKIE,
                               'Location': fakes.SIGNON_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_URL,
                      headers={'Location': fakes.SSO_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.SSO_REDIRECT_URL,
                      status=200)
        responses.add(responses.GET, config.OFFERS_URL,
                      body=self.OFFERS_RESP_JSON,
                      status=200)
        responses.add(responses.POST, config.MEDIA_ORDER_URL,
                      body=self.ORDER_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.YINZ_CALLBACK_URL.format(
            json.loads(self.YINZCAM_AUTH2_RESP_JSON).get('TpUid')),
                      headers={'Location': 'foo://bar'},
                      status=200)
        responses.add(responses.GET, config.STATUS_URL,
                      body=self.STATUS_FAIL_RESP_JSON,
                      status=200)
        self.assertRaises(telstra_auth.TelstraAuthException,
                          telstra_auth.get_free_token, 'foo', 'bar')

    @responses.activate
    @mock.patch('uuid.uuid4')
    def test_get_mobile_token(self, mock_uuid):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE},
                      status=200)
        responses.add(responses.POST, config.OAUTH_URL,
                      body=self.NRL_TOKEN_JSON,
                      status=200)
        responses.add(responses.GET, config.OLD_OFFERS_URL,
                      body=self.OFFERS_RESP_JSON,
                      status=200)
        responses.add(responses.POST, config.OLD_MEDIA_ORDER_URL,
                      body=self.ORDER_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.YINZ_CALLBACK_URL.format(
            json.loads(self.YINZCAM_AUTH2_RESP_JSON).get('TpUid')),
                      headers={'Location': 'foo://bar'},
                      status=200)
        responses.add(responses.GET, config.STATUS_URL,
                      body=self.STATUS_RESP_JSON,
                      status=200)
        observed = telstra_auth.get_mobile_token()
        self.assertEqual('ticket123', observed)

    @responses.activate
    @mock.patch('uuid.uuid4')
    def test_get_mobile_token_fail_no_mobile_data(self, mock_uuid):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE_NO_DATA},
                      status=204)
        self.assertRaises(telstra_auth.TelstraAuthException,
                          telstra_auth.get_mobile_token)

    @responses.activate
    @mock.patch('uuid.uuid4')
    def test_get_mobile_token_fail_no_offer(self, mock_uuid):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE},
                      status=200)
        responses.add(responses.POST, config.OAUTH_URL,
                      body=self.NRL_TOKEN_JSON,
                      status=200)
        responses.add(responses.GET, config.OLD_OFFERS_URL,
                      body=self.OFFERS_FAIL_RESP_JSON,
                      status=200)
        self.assertRaises(telstra_auth.TelstraAuthException,
                          telstra_auth.get_mobile_token)

    @responses.activate
    @mock.patch('uuid.uuid4')
    def test_get_mobile_token_fail_no_eligible(self, mock_uuid):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE},
                      status=200)
        responses.add(responses.POST, config.OAUTH_URL,
                      body=self.NRL_TOKEN_JSON,
                      status=200)
        responses.add(responses.GET, config.OLD_OFFERS_URL,
                      json={'userMessage': 'No eligible services'},
                      status=404)
        self.assertRaises(telstra_auth.TelstraAuthException,
                          telstra_auth.get_mobile_token)

    @responses.activate
    @mock.patch('uuid.uuid4')
    def test_get_mobile_token_fail_activation(self, mock_uuid):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE},
                      status=200)
        responses.add(responses.POST, config.OAUTH_URL,
                      body=self.NRL_TOKEN_JSON,
                      status=200)
        responses.add(responses.GET, config.OLD_OFFERS_URL,
                      body=self.OFFERS_RESP_JSON,
                      status=200)
        responses.add(responses.POST, config.OLD_MEDIA_ORDER_URL,
                      body=self.ORDER_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.YINZ_CALLBACK_URL.format(
            json.loads(self.YINZCAM_AUTH2_RESP_JSON).get('TpUid')),
                      headers={'Location': 'foo://bar'},
                      status=200)
        responses.add(responses.GET, config.STATUS_URL,
                      body=self.STATUS_FAIL_RESP_JSON,
                      status=200)
        self.assertRaises(telstra_auth.TelstraAuthException,
                          telstra_auth.get_mobile_token)
