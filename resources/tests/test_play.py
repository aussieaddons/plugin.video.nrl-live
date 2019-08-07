from __future__ import absolute_import, unicode_literals
from future.utils import string_types
import json

from resources.tests.fakes import fakes

try:
    import mock
except ImportError:
    import unittest.mock as mock

import io
import os
import re
import responses
import testtools
import traceback
import sys

from future.moves.urllib.parse import urlparse, parse_qsl, urlencode
from urllib import unquote_plus

import resources.lib.config as config

def escape_regex(s):
    escaped = re.escape(s)
    return escaped.replace('\{', '{').replace('\}', '}')


class PlayTests(testtools.TestCase):
    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/AUTH.json'), 'r') as f:
            self.AUTH_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/EMBED_TOKEN.xml'),
                  'r') as f:
            self.EMBED_TOKEN_XML = io.BytesIO(f.read()).read()

    @responses.activate
    @mock.patch('resources.lib.ooyalahelper.cache.get')
    @mock.patch('xbmcgui.ListItem')
    @mock.patch('sys.argv',
                ['plugin://plugin.video.nrl-live/',
                 '2',
                 '?action=listmatches&dummy=None&p_code'
                 '=p3ZWsyOiMLEluThqwB_eQUFngsCZ&match_id=None&title=Match '
                 'Highlights: Titans v '
                 'Broncos&video_id=44azdwNDpSWUvfd8F30d55tXY0YH9njH',
                 'resume:false'])
    def test_play_video(self, mock_listitem, mock_ticket):
        escaped_auth_url = re.escape(
            config.AUTH_URL).replace('\{', '{').replace('\}', '}')
        auth_url = re.compile(escaped_auth_url.format('.*', '.*', '.*'))
        responses.add(responses.GET, auth_url,
                      body=self.AUTH_JSON, status=200)

        escaped_embed_url = re.escape(
            config.EMBED_TOKEN_URL).replace('\{', '{').replace('\}', '}')
        embed_url = re.compile(escaped_embed_url.format('.*'))
        responses.add(responses.GET, embed_url,
                      body=self.EMBED_TOKEN_XML, status=200)

        mock_ticket.return_value = 'foobar123456'
        mock_listitem.side_effect = fakes.FakeListItem
        params = dict(parse_qsl(sys.argv[2][1:]))
        mock_plugin = fakes.FakePlugin()
        with mock.patch.dict('sys.modules', xbmcplugin=mock_plugin):
            import resources.lib.play as play
            play.play_video(params)
            self.assertEqual(fakes.M3U8_URL, mock_plugin.resolved[2].getPath())
