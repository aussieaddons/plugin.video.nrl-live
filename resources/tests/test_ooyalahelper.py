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
import ooyalahelper

class OoyalahelperTests(testtools.TestCase):

    @mock.patch('ooyalahelper.cache.delete')
    def test_clear_ticket(self, mock_delete):
        ooyalahelper.clear_ticket()
        mock_delete.assert_called_with('NRLTICKET')

    def test_get_user_ticket(self):
        with mock.patch('ooyalahelper.cache.get') as ticket:
            ticket.return_value = 'foobar123456'
            observed = ooyalahelper.get_user_ticket()
            self.assertEqual('foobar123456', observed)

        with mock.patch('ooyalahelper.cache.get') as ticket:
            ticket.return_value = ''
            with mock.patch('ooyalahelper.addon.getSetting') as sub_type:
                with mock.patch(
                        'ooyalahelper.telstra_auth.get_free_token') as \
                        free_token:
                    sub_type.return_value = '1'
                    free_token.return_value = 'foobar456789'
                    observed = ooyalahelper.get_user_ticket()
                    self.assertEqual('foobar456789', observed)
                with mock.patch(
                        'ooyalahelper.telstra_auth.get_mobile_token') as \
                        mobile_token:
                    sub_type.return_value = '2'
                    mobile_token.return_value = 'foobar654321'
                    observed = ooyalahelper.get_user_ticket()
                    self.assertEqual('foobar654321', observed)
                with mock.patch(
                        'ooyalahelper.telstra_auth.get_paid_token') as \
                        paid_token:
                    sub_type.return_value = '3'
                    paid_token.return_value = 'foobar987654'
                    observed = ooyalahelper.get_user_ticket()
                    self.assertEqual('foobar987654', observed)

    @responses.activate
    @mock.patch('ooyalahelper.cache.delete')
    def test_get_embed_token(self, mock_delete):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, config.EMBED_TOKEN_URL.format('foo'),
                     body=fakes.EMBED_TOKEN_XML, status=200)
            observed = ooyalahelper.get_embed_token('bar123', 'foo')
            self.assertEqual('http://foobar.com/video', observed)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, config.EMBED_TOKEN_URL.format('foo'),
                     body=fakes.EMBED_TOKEN_XML, status=401)
            self.assertRaises(ooyalahelper.AussieAddonsException,
                              ooyalahelper.get_embed_token, 'bar123', 'foo')
            mock_delete.assert_called_with('NRLTICKET')

    @responses.activate
    def test_get_secure_token(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'https://foo.bar/', body=fakes.AUTH_JSON,
                     status=200)
            observed = ooyalahelper.get_secure_token('https://foo.bar/',
                                                     fakes.VIDEO_ID)
            self.assertEqual(fakes.M3U8_URL, observed)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'https://foo.bar/',
                     body=fakes.AUTH_JSON_FAILED,
                     status=200)
            self.assertRaises(ooyalahelper.AussieAddonsException,
                              ooyalahelper.get_secure_token,
                              'https://foo.bar/',
                              fakes.VIDEO_ID)

    @responses.activate
    @mock.patch('ooyalahelper.cache.get')
    def test_get_m3u8_playlist(self, ticket):
        ticket.return_value = 'foobar123456'
        import urllib
        url = config.AUTH_URL.format(config.PCODE, fakes.VIDEO_ID,
                                     urllib.quote_plus(
                                         'http://foobar.com/video'))
        responses.add(responses.GET, url,
                      body=fakes.AUTH_JSON, status=200)
        responses.add(responses.GET,
                      config.EMBED_TOKEN_URL.format(fakes.VIDEO_ID),
                      body=fakes.EMBED_TOKEN_XML, status=200)
        observed = ooyalahelper.get_m3u8_playlist(fakes.VIDEO_ID, '')
        self.assertEqual(fakes.M3U8_URL, observed)