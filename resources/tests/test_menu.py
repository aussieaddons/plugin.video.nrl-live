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

import config


class MenuTests(testtools.TestCase):

    @classmethod
    def setUpClass(self):
        with open(os.path.join(os.getcwd(), 'fakes/xml/BOX.xml'), 'r') as f:
            self.BOX_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(os.getcwd(), 'fakes/xml/HOME.xml'), 'r') as f:
            self.HOME_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(os.getcwd(), 'fakes/xml/MATCH.xml'), 'r') as f:
            self.MATCH_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(os.getcwd(), 'fakes/xml/SCORE.xml'), 'r') as f:
            self.SCORE_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(os.getcwd(), 'fakes/xml/VIDEO.xml'), 'r') as f:
            self.VIDEO_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(os.getcwd(), 'fakes/xml/EMBED_TOKEN.xml'),
                  'r') as f:
            self.EMBED_TOKEN_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(os.getcwd(), 'fakes/xml/YINZCAM_AUTH_RESP.xml'),
                  'r') as f:
            self.YINZCAM_AUTH_RESP_XML = io.BytesIO(f.read()).read()

    @mock.patch('xbmcgui.ListItem')
    @mock.patch('sys.argv',
                ['plugin://plugin.video.nrl-live/','2','','resume:false'])
    def test_list_categories(self, mock_listitem):
        mock_listitem.side_effect = fakes.FakeListItem
        mock_plugin = fakes.FakePlugin()
        with mock.patch.dict('sys.modules', xbmcplugin=mock_plugin):
            import menu
            menu.list_categories()
            for index, category in enumerate(config.CATEGORIES):
                expected = 'plugin://{addonid}/?{params}'.format(
                    addonid=config.ADDON_ID,
                    params=unquote_plus(urlencode({'action': 'listcategories',
                                                   'category': category})))
                observed = mock_plugin.directory[index].get('url')
                self.assertEqual(expected, observed)

    @responses.activate
    @mock.patch('xbmcgui.ListItem')
    @mock.patch('sys.argv',
                ['plugin://plugin.video.nrl-live/',
                 '2',
                 '?action=listcategories&category=Videos',
                 'resume:false'])
    def test_list_videos_urls(self, mock_listitem):
        responses.add(responses.GET, config.VIDEO_URL,
                      body=self.VIDEO_XML, status=200)
        mock_listitem.side_effect = fakes.FakeListItem
        params = dict(parse_qsl(sys.argv[2][1:]))

        mock_plugin = fakes.FakePlugin()
        with mock.patch.dict('sys.modules', xbmcplugin=mock_plugin):
            import menu
            menu.list_videos(params)
            for index, expected in enumerate(fakes.EXPECTED_VIDEO_TITLES):
                url = mock_plugin.directory[index].get('url')
                url_query = dict(parse_qsl(urlparse(url)[4]))
                observed = url_query.get('title')
                self.assertEqual(expected, observed)

    @responses.activate
    @mock.patch('xbmcgui.ListItem')
    @mock.patch('sys.argv',
                ['plugin://plugin.video.nrl-live/',
                 '2',
                 '?action=listcategories&category=Videos',
                 'resume:false'])
    def test_list_videos_listitem_labels(self, mock_listitem):
        responses.add(responses.GET, config.VIDEO_URL,
                      body=self.VIDEO_XML, status=200)
        mock_listitem.side_effect = fakes.FakeListItem
        params = dict(parse_qsl(sys.argv[2][1:]))

        mock_plugin = fakes.FakePlugin()
        with mock.patch.dict('sys.modules', xbmcplugin=mock_plugin):
            import menu
            menu.list_videos(params)
            for index, expected in enumerate(fakes.EXPECTED_VIDEO_TITLES):
                li = mock_plugin.directory[index].get('listitem')
                self.assertEqual(expected, li.getLabel())

    @responses.activate
    @mock.patch('xbmcgui.ListItem')
    @mock.patch('sys.argv',
                ['plugin://plugin.video.nrl-live/',
                 '2',
                 '?action=listcategories&category=Live Matches',
                 'resume:false'])
    def test_list_matches_live(self, mock_listitem):
        responses.add(responses.GET, config.HOME_URL,
                      body=self.HOME_XML, status=200)
        escaped_box_url = re.escape(
            config.BOX_URL).replace('\{', '{').replace('\}', '}')
        box_url = re.compile(escaped_box_url.format('.*'))
        responses.add(responses.GET, box_url,
                      body=self.BOX_XML, status=200)
        responses.add(responses.GET, config.SCORE_URL,
                      body=self.SCORE_XML, status=200)
        mock_listitem.side_effect = fakes.FakeListItem
        params = dict(parse_qsl(sys.argv[2][1:]))
        mock_plugin = fakes.FakePlugin()
        with mock.patch.dict('sys.modules', xbmcplugin=mock_plugin):
            import menu
            menu.list_matches(params, live=True)
            for index, expected in enumerate(fakes.EXPECTED_LIVE_TITLES):
                url = mock_plugin.directory[index].get('url')
                url_query = dict(parse_qsl(urlparse(url)[4]))
                observed = url_query.get('title')
                self.assertEqual(expected, observed)