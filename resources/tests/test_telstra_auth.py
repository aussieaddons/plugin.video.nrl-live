from __future__ import absolute_import, unicode_literals

import io
import json
import os
import re
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
        with open(os.path.join(cwd, 'fakes/json/MYID_TOKEN_RESP.json'),
                  'rb') as f:
            self.MYID_TOKEN_RESP_JSON = io.BytesIO(f.read()).read()
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
        with open(
                os.path.join(cwd, 'fakes/html/MYID_AUTH_RESP.html'),
                'rb') as f:
            self.MYID_AUTH_RESP_HTML = io.BytesIO(f.read()).read()
        with open(
                os.path.join(cwd, 'fakes/html/MYID_RESUME_AUTH_RESP.html'),
                'rb') as f:
            self.MYID_RESUME_AUTH_RESP_HTML = io.BytesIO(f.read()).read()

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
        responses.add(responses.GET, re.compile(config.NRL_AUTH_ACCEPT),
                      body='',
                      headers={'location': 'http://foo.bar/?code=abc'})
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
        auth = telstra_auth.TelstraAuth('foo', 'bar')
        observed = auth.get_paid_token()
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
        auth = telstra_auth.TelstraAuth('foo', 'wrongpassword')
        self.assertRaises(telstra_auth.TelstraAuthException,
                          auth.get_paid_token)

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
        responses.add(responses.GET, re.compile(config.NRL_AUTH_ACCEPT),
                      body='',
                      headers={'location': 'http://foo.bar/?code=abc'})
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
        auth = telstra_auth.TelstraAuth('foo', 'bar')
        self.assertRaises(telstra_auth.TelstraAuthException,
                          auth.get_paid_token)

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
        responses.add(responses.GET, config.MYID_AUTHORIZATION_URL,
                      body=self.MYID_AUTH_RESP_HTML,
                      status=200)
        responses.add(responses.POST,
                      config.MYID_RESUME_AUTHORIZATION_URL.format('ABCDE'),
                      body=self.MYID_RESUME_AUTH_RESP_HTML,
                      status=200)
        for url in config.SSO_SESSION_HANDLER_URLS:
            responses.add(responses.POST, url,
                          json={'status': 'success'},
                          status=200)

        responses.add(responses.GET,
                      '{0}{1}'.format(
                          config.MYID_RESUME_AUTHORIZATION_URL.format('ABCDE'),
                          '?ctfr-proceed=true'),
                      headers={'Set-Cookie': fakes.FAKE_BPSESSION_COOKIE,
                               'Location':
                                   fakes.MYID_RESUME_AUTH_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.MYID_RESUME_AUTH_REDIRECT_URL,
                      status=200)
        responses.add(responses.POST, config.MYID_TOKEN_URL,
                      body=self.MYID_TOKEN_RESP_JSON,
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
        auth = telstra_auth.TelstraAuth('foo', 'bar')
        observed = auth.get_free_token()
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
        responses.add(responses.GET, config.MYID_AUTHORIZATION_URL,
                      body=self.MYID_AUTH_RESP_HTML,
                      status=200)
        responses.add(responses.POST,
                      config.MYID_RESUME_AUTHORIZATION_URL.format('ABCDE'),
                      body=self.MYID_AUTH_RESP_HTML,
                      status=200)
        auth = telstra_auth.TelstraAuth('foo', 'wrongpassword')
        self.assertRaises(telstra_auth.TelstraAuthException,
                          auth.get_free_token)

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
        responses.add(responses.GET, config.MYID_AUTHORIZATION_URL,
                      body=self.MYID_AUTH_RESP_HTML,
                      status=200)
        responses.add(responses.POST,
                      config.MYID_RESUME_AUTHORIZATION_URL.format('ABCDE'),
                      body=self.MYID_RESUME_AUTH_RESP_HTML,
                      status=200)
        for url in config.SSO_SESSION_HANDLER_URLS:
            responses.add(responses.POST, url,
                          json={'status': 'success'},
                          status=200)

        responses.add(responses.GET,
                      '{0}{1}'.format(
                          config.MYID_RESUME_AUTHORIZATION_URL.format('ABCDE'),
                          '?ctfr-proceed=true'),
                      headers={'Set-Cookie': fakes.FAKE_BPSESSION_COOKIE,
                               'Location':
                                   fakes.MYID_RESUME_AUTH_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.MYID_RESUME_AUTH_REDIRECT_URL,
                      status=200)
        responses.add(responses.POST, config.MYID_TOKEN_URL,
                      body=self.MYID_TOKEN_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.OFFERS_URL,
                      body=self.OFFERS_FAIL_RESP_JSON,
                      status=200)
        auth = telstra_auth.TelstraAuth('foo', 'bar')
        self.assertRaises(telstra_auth.TelstraAuthException,
                          auth.get_free_token)

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
        responses.add(responses.GET, config.MYID_AUTHORIZATION_URL,
                      body=self.MYID_AUTH_RESP_HTML,
                      status=200)
        responses.add(responses.POST,
                      config.MYID_RESUME_AUTHORIZATION_URL.format('ABCDE'),
                      body=self.MYID_RESUME_AUTH_RESP_HTML,
                      status=200)
        for url in config.SSO_SESSION_HANDLER_URLS:
            responses.add(responses.POST, url,
                          json={'status': 'success'},
                          status=200)

        responses.add(responses.GET,
                      '{0}{1}'.format(
                          config.MYID_RESUME_AUTHORIZATION_URL.format('ABCDE'),
                          '?ctfr-proceed=true'),
                      headers={'Set-Cookie': fakes.FAKE_BPSESSION_COOKIE,
                               'Location':
                                   fakes.MYID_RESUME_AUTH_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.MYID_RESUME_AUTH_REDIRECT_URL,
                      status=200)
        responses.add(responses.POST, config.MYID_TOKEN_URL,
                      body=self.MYID_TOKEN_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.OFFERS_URL,
                      json={'userMessage': 'No eligible services'},
                      status=404)
        auth = telstra_auth.TelstraAuth('foo', 'bar')
        self.assertRaises(telstra_auth.TelstraAuthException,
                          auth.get_free_token)

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
        responses.add(responses.GET, config.MYID_AUTHORIZATION_URL,
                      body=self.MYID_AUTH_RESP_HTML,
                      status=200)
        responses.add(responses.POST,
                      config.MYID_RESUME_AUTHORIZATION_URL.format('ABCDE'),
                      body=self.MYID_RESUME_AUTH_RESP_HTML,
                      status=200)
        for url in config.SSO_SESSION_HANDLER_URLS:
            responses.add(responses.POST, url,
                          json={'status': 'success'},
                          status=200)

        responses.add(responses.GET,
                      '{0}{1}'.format(
                          config.MYID_RESUME_AUTHORIZATION_URL.format('ABCDE'),
                          '?ctfr-proceed=true'),
                      headers={'Set-Cookie': fakes.FAKE_BPSESSION_COOKIE,
                               'Location':
                                   fakes.MYID_RESUME_AUTH_REDIRECT_URL},
                      status=302)
        responses.add(responses.GET, fakes.MYID_RESUME_AUTH_REDIRECT_URL,
                      status=200)
        responses.add(responses.POST, config.MYID_TOKEN_URL,
                      body=self.MYID_TOKEN_RESP_JSON,
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
        auth = telstra_auth.TelstraAuth('foo', 'bar')
        self.assertRaises(telstra_auth.TelstraAuthException,
                          auth.get_free_token)

    @responses.activate
    def test_get_mobile_token(self):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE},
                      status=200)
        responses.add(responses.POST, config.MOBILE_OAUTH_URL,
                      body=self.NRL_TOKEN_JSON,
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
        auth = telstra_auth.TelstraAuth()
        observed = auth.get_mobile_token()
        self.assertEqual('ticket123', observed)

    @responses.activate
    def test_get_mobile_token_fail_no_mobile_data(self):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE_NO_DATA},
                      status=204)
        auth = telstra_auth.TelstraAuth()
        self.assertRaises(telstra_auth.TelstraAuthException,
                          auth.get_mobile_token)

    @responses.activate
    def test_get_mobile_token_fail_no_offer(self):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE},
                      status=200)
        responses.add(responses.POST, config.MOBILE_OAUTH_URL,
                      body=self.NRL_TOKEN_JSON,
                      status=200)
        responses.add(responses.GET, config.OFFERS_URL,
                      body=self.OFFERS_FAIL_RESP_JSON,
                      status=200)
        auth = telstra_auth.TelstraAuth()
        self.assertRaises(telstra_auth.TelstraAuthException,
                          auth.get_mobile_token)

    @responses.activate
    def test_get_mobile_token_fail_no_eligible(self):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE},
                      status=200)
        responses.add(responses.POST, config.MOBILE_OAUTH_URL,
                      body=self.NRL_TOKEN_JSON,
                      status=200)
        responses.add(responses.GET, config.OFFERS_URL,
                      json={'userMessage': 'No eligible services'},
                      status=404)
        auth = telstra_auth.TelstraAuth()
        self.assertRaises(telstra_auth.TelstraAuthException,
                          auth.get_mobile_token)

    @responses.activate
    def test_get_mobile_token_fail_activation(self):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=self.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=self.YINZCAM_AUTH2_RESP_JSON,
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE},
                      status=200)
        responses.add(responses.POST, config.MOBILE_OAUTH_URL,
                      body=self.NRL_TOKEN_JSON,
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
        auth = telstra_auth.TelstraAuth()
        self.assertRaises(telstra_auth.TelstraAuthException,
                          auth.get_mobile_token)
