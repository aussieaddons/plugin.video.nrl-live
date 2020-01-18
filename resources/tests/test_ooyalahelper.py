from __future__ import absolute_import, unicode_literals

import io
import os
try:
    import mock
except ImportError:
    import unittest.mock as mock

from future.moves.urllib.parse import quote_plus

import responses

import testtools

import resources.lib.config as config
import resources.lib.ooyalahelper as ooyalahelper
from resources.tests.fakes import fakes


class OoyalahelperTests(testtools.TestCase):
    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/xml/EMBED_TOKEN.xml'),
                  'rb') as f:
            self.EMBED_TOKEN_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/EMBED_TOKEN_FAIL.xml'),
                  'rb') as f:
            self.EMBED_TOKEN_FAIL_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/json/AUTH.json'),
                  'rb') as f:
            self.AUTH_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/json/AUTH_FAILED.json'),
                  'rb') as f:
            self.AUTH_FAILED_JSON = io.BytesIO(f.read()).read()

    @mock.patch('resources.lib.ooyalahelper.cache.delete')
    def test_clear_ticket(self, mock_delete):
        ooyalahelper.clear_ticket()
        mock_delete.assert_called_with('NRLTICKET')

    @mock.patch('resources.lib.ooyalahelper.cache.get')
    def test_get_user_ticket_cached(self, mock_ticket):
        mock_ticket.return_value = 'foobar123456'
        observed = ooyalahelper.get_user_ticket()
        self.assertEqual('foobar123456', observed)

    @mock.patch(
        'resources.lib.ooyalahelper.telstra_auth.TelstraAuth.get_free_token')
    @mock.patch('resources.lib.ooyalahelper.addon.getSetting')
    @mock.patch('resources.lib.ooyalahelper.cache.get')
    def test_get_user_ticket_free(self, mock_ticket, mock_sub_type,
                                  mock_token):
        mock_ticket.return_value = ''
        mock_sub_type.return_value = '1'
        mock_token.return_value = 'foobar456789'

    @mock.patch(
        'resources.lib.ooyalahelper.telstra_auth.TelstraAuth.get_mobile_token')
    @mock.patch('resources.lib.ooyalahelper.addon.getSetting')
    @mock.patch('resources.lib.ooyalahelper.cache.get')
    def test_get_user_ticket_mobile(self, mock_ticket, mock_sub_type,
                                    mock_token):
        mock_ticket.return_value = ''
        mock_sub_type.return_value = '2'
        mock_token.return_value = 'foobar654321'
        observed = ooyalahelper.get_user_ticket()
        self.assertEqual('foobar654321', observed)

    @mock.patch(
        'resources.lib.ooyalahelper.telstra_auth.TelstraAuth.get_paid_token')
    @mock.patch('resources.lib.ooyalahelper.addon.getSetting')
    @mock.patch('resources.lib.ooyalahelper.cache.get')
    def test_get_user_ticket_paid(self, mock_ticket, mock_sub_type,
                                  mock_token):
        mock_ticket.return_value = ''
        mock_sub_type.return_value = '0'
        mock_token.return_value = 'foobar987654'
        observed = ooyalahelper.get_user_ticket()
        self.assertEqual('foobar987654', observed)

    @responses.activate
    @mock.patch('resources.lib.ooyalahelper.cache.delete')
    def test_get_embed_token(self, mock_delete):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, config.EMBED_TOKEN_URL.format('foo'),
                     body=self.EMBED_TOKEN_XML, status=200)
            observed = ooyalahelper.get_embed_token('bar123', 'foo')
            self.assertEqual('http://foobar.com/video', observed)

    @responses.activate
    @mock.patch('resources.lib.ooyalahelper.cache.delete')
    def test_get_embed_token_fail_401(self, mock_delete):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, config.EMBED_TOKEN_URL.format('foo'),
                     body=self.EMBED_TOKEN_XML, status=401)
            self.assertRaises(ooyalahelper.AussieAddonsException,
                              ooyalahelper.get_embed_token, 'bar123', 'foo')
            mock_delete.assert_called_with('NRLTICKET')

    @responses.activate
    @mock.patch('resources.lib.ooyalahelper.cache.delete')
    def test_get_embed_token_fail_403(self, mock_delete):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, config.EMBED_TOKEN_URL.format('foo'),
                     body=self.EMBED_TOKEN_FAIL_XML, status=403)
            self.assertRaises(ooyalahelper.AussieAddonsException,
                              ooyalahelper.get_embed_token, 'bar123', 'foo')
            mock_delete.assert_called_with('NRLTICKET')

    @responses.activate
    @mock.patch('resources.lib.ooyalahelper.cache.delete')
    def test_get_embed_token_fail_404(self, mock_delete):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, config.EMBED_TOKEN_URL.format('foo'),
                     body=self.EMBED_TOKEN_FAIL_XML, status=404)
            self.assertRaises(
                ooyalahelper.session.requests.exceptions.HTTPError,
                ooyalahelper.get_embed_token, 'bar123', 'foo')
            mock_delete.assert_called_with('NRLTICKET')

    @responses.activate
    @mock.patch('resources.lib.ooyalahelper.cache.delete')
    def test_get_embed_token_fail_errorcode(self, mock_delete):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, config.EMBED_TOKEN_URL.format('foo'),
                     body=self.EMBED_TOKEN_FAIL_XML, status=200)
            self.assertRaises(ooyalahelper.AussieAddonsException,
                              ooyalahelper.get_embed_token, 'bar123', 'foo')
            mock_delete.assert_called_with('NRLTICKET')

    @responses.activate
    @mock.patch('resources.lib.ooyalahelper.cache.delete')
    def test_get_embed_token_fail_parseerror(self, mock_delete):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, config.EMBED_TOKEN_URL.format('foo'),
                     body='not valid xml', status=200)
            self.assertRaises(ooyalahelper.ET.ParseError,
                              ooyalahelper.get_embed_token, 'bar123', 'foo')
            mock_delete.assert_called_with('NRLTICKET')

    @testtools.skip("Ooyalahelper may no longer be needed...")
    @responses.activate
    def test_get_secure_token(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'https://foo.bar/', body=self.AUTH_JSON,
                     status=200)
            observed = ooyalahelper.get_secure_token('https://foo.bar/',
                                                     fakes.VIDEO_ID)
            self.assertEqual(fakes.M3U8_URL, observed)

    @responses.activate
    def test_get_secure_token_fail_keyerror(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'https://foo.bar/',
                     body=self.AUTH_FAILED_JSON,
                     status=200)
            self.assertRaises(ooyalahelper.AussieAddonsException,
                              ooyalahelper.get_secure_token,
                              'https://foo.bar/',
                              fakes.VIDEO_ID)

    @testtools.skip("Ooyalahelper may no longer be needed...")
    @responses.activate
    @mock.patch('resources.lib.ooyalahelper.cache.get')
    def test_get_m3u8_playlist(self, mock_ticket):
        mock_ticket.return_value = 'foobar123456'
        auth_url = config.AUTH_URL.format(
            config.PCODE, fakes.VIDEO_ID,
            quote_plus('http://foobar.com/video'))
        responses.add(responses.GET, auth_url,
                      body=self.AUTH_JSON, status=200)
        responses.add(responses.GET,
                      config.EMBED_TOKEN_URL.format(fakes.VIDEO_ID),
                      body=self.EMBED_TOKEN_XML, status=200)
        observed = ooyalahelper.get_m3u8_playlist(fakes.VIDEO_ID, '')
        self.assertEqual(fakes.M3U8_URL, observed)
