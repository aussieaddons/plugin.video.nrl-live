from __future__ import absolute_import, unicode_literals

import io
import os
import re
import sys
try:
    import mock
except ImportError:
    import unittest.mock as mock

from future.moves.urllib.parse import parse_qsl

import responses

import testtools

import resources.lib.config as config
from resources.tests.fakes import fakes


def escape_regex(s):
    escaped = re.escape(s)
    return escaped.replace('\\{', '{').replace('\\}', '}')


class PlayTests(testtools.TestCase):
    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/AUTH.json'), 'rb') as f:
            self.AUTH_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/json/STREAM_API.json'), 'rb') as f:
            self.STREAM_API_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/json/VIDEOTOKEN.json'), 'rb') as f:
            self.VIDEOTOKEN_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/EMBED_TOKEN.xml'),
                  'rb') as f:
            self.EMBED_TOKEN_XML = io.BytesIO(f.read()).read()

    @responses.activate
    @mock.patch('resources.lib.stream_auth.cache.get')
    @mock.patch('xbmcgui.ListItem')
    @mock.patch('sys.argv',
                ['plugin://plugin.video.nrl-live/',
                 '2',
                 '?action=listmatches&dummy=None&match_id=None&title=Match '
                 'Highlights: Titans v '
                 'Broncos&video_id=123456',
                 'resume:false'])
    def test_play_video(self, mock_listitem, mock_ticket):
        escaped_auth_url = re.escape(
            config.AUTH_URL).replace('\\{', '{').replace('\\}', '}')
        auth_url = re.compile(escaped_auth_url.format('.*', '.*', '.*'))
        responses.add(responses.GET, auth_url,
                      body=self.AUTH_JSON, status=200)

        escaped_embed_url = re.escape(
            config.EMBED_TOKEN_URL).replace('\\{', '{').replace('\\}', '}')
        embed_url = re.compile(escaped_embed_url.format('.*'))
        responses.add(responses.GET, embed_url,
                      body=self.EMBED_TOKEN_XML, status=200)

        escaped_stream_url = re.escape(
            config.STREAM_API_URL).replace('\\{', '{').replace('\\}', '}')
        escaped_stream_url = escaped_stream_url.replace('\\_', '_')
        stream_url = re.compile(escaped_stream_url.format(video_id='.*'))
        responses.add(responses.GET, stream_url,
                      body=self.STREAM_API_JSON, status=200)

        responses.add(responses.GET,
                      config.MEDIA_AUTH_URL.format(embed_code='123456'),
                      body=self.VIDEOTOKEN_JSON)

        mock_ticket.return_value = 'foobar123456'
        mock_listitem.side_effect = fakes.FakeListItem
        params = dict(parse_qsl(sys.argv[2][1:]))
        mock_plugin = fakes.FakePlugin()
        with mock.patch.dict('sys.modules', xbmcplugin=mock_plugin):
            import resources.lib.play as play
            play.play_video(params)
            self.assertEqual(fakes.M3U8_URL.decode(),
                             mock_plugin.resolved[2].getPath())
