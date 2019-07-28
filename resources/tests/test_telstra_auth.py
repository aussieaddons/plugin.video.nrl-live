from __future__ import absolute_import, unicode_literals
from future.utils import string_types
from collections import OrderedDict
import json

from resources.tests import fakes

try:
    import mock
except ImportError:
    import unittest.mock as mock

import re
import responses
import testtools
import traceback
import xbmc

from future.moves.urllib.parse import parse_qsl

import config
import telstra_auth

class Telstra_authTests(testtools.TestCase):

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

        responses.add_callback(responses.GET, config.NRL_AUTH,
                      callback=auth_callback)

        responses.add(responses.POST, config.NRL_LOGIN,
                  body=json.dumps({'success': True}),
                  status=200)
        responses.add(responses.POST, config.NRL_TOKEN,
                      body=json.dumps(fakes.NRL_TOKEN_JSON),
                      status=200)
        responses.add(responses.POST, config.YINZCAM_AUTH_URL.format(
            fakes.NRL_TOKEN_JSON.get('refresh_token')),
                      body=json.dumps(fakes.YINZCAM_AUTH_RESP_JSON),
                      status=200)
        responses.add(responses.GET, config.STATUS_URL,
                      body=json.dumps(fakes.STATUS_RESP_JSON),
                      status=200)
        observed = telstra_auth.get_paid_token('foo', 'bar')
        self.assertEqual('ticket123', observed)

    @responses.activate
    @mock.patch('os.urandom')
    @mock.patch('uuid.uuid4')
    def test_get_free_token(self, mock_uuid, mock_random):
        mock_uuid.side_effect = fakes.FAKE_UUID
        mock_random.side_effect = fakes.FAKE_RANDOM
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=fakes.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=json.dumps(fakes.YINZCAM_AUTH2_RESP),
                      status=200)
        responses.add(responses.GET, fakes.YINZCAM_AUTH2_RESP.get('Url'),
                      body=fakes.SPC_RESP_HTML,
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
                      body=json.dumps(fakes.OFFERS_RESP_JSON),
                      status=200)
        responses.add(responses.POST, config.MEDIA_ORDER_URL,
                      body=json.dumps(fakes.ORDER_RESP_JSON),
                      status=200)
        responses.add(responses.GET, config.YINZ_CALLBACK_URL.format(
            fakes.YINZCAM_AUTH2_RESP.get('TpUid')),
                      headers={'Location': 'foo://bar'},
                      status=200)
        responses.add(responses.GET, config.STATUS_URL,
                      body=json.dumps(fakes.STATUS_RESP_JSON),
                      status=200)
        observed = telstra_auth.get_free_token('foo', 'bar')
        self.assertEqual('ticket123', observed)

    @responses.activate
    @mock.patch('uuid.uuid4')
    def test_get_mobile_token(self, mock_uuid):
        responses.add(responses.POST, config.YINZCAM_AUTH_URL,
                      body=fakes.YINZCAM_AUTH_RESP_XML,
                      status=200)
        responses.add(responses.GET, config.YINZCAM_AUTH_URL2,
                      body=json.dumps(fakes.YINZCAM_AUTH2_RESP),
                      status=200)
        responses.add(responses.GET, config.MOBILE_ID_URL,
                      headers={'Set-Cookie': fakes.FAKE_MOBILE_COOKIE},
                      status=200)
        responses.add(responses.POST, config.OAUTH_URL,
                      body=json.dumps(fakes.NRL_TOKEN_JSON),
                      status=200)
        responses.add(responses.GET, config.OLD_OFFERS_URL,
                      body=json.dumps(fakes.OFFERS_RESP_JSON),
                      status=200)
        responses.add(responses.POST, config.OLD_MEDIA_ORDER_URL,
                      body=json.dumps(fakes.ORDER_RESP_JSON),
                      status=200)
        responses.add(responses.GET, config.YINZ_CALLBACK_URL.format(
            fakes.YINZCAM_AUTH2_RESP.get('TpUid')),
                      headers={'Location': 'foo://bar'},
                      status=200)
        responses.add(responses.GET, config.STATUS_URL,
                      body=json.dumps(fakes.STATUS_RESP_JSON),
                      status=200)
        observed = telstra_auth.get_mobile_token()
        self.assertEqual('ticket123', observed)