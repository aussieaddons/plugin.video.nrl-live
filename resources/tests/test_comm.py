from __future__ import absolute_import, unicode_literals
from future.utils import string_types
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

import comm
import config


class UtilsTests(testtools.TestCase):

    def test_get_airtime(self):
        ts = '2019-03-14T00:58:00Z'
        expected = 'Thursday 14 Mar @ 10:58 AM'
        self.assertEqual(expected, comm.get_airtime(ts))

    @responses.activate
    def test_fetch_url(self):
        responses.add(responses.GET, 'http://foo.bar/',
                      body=u'\ufeffHello World', status=200)
        observed = comm.fetch_url('http://foo.bar/')
        self.assertEqual(observed, 'Hello World')

    @responses.activate
    def test_list_matches(self):
        responses.add(responses.GET, config.VIDEO_URL,
                      body=fakes.MATCH_XML, status=200)
        listing = comm.list_matches({})
        self.assertEqual(4, len(listing))
        self.assertEqual('Full', listing[0].title[:4])

    @responses.activate
    def test_get_upcoming(self):
        responses.add(responses.GET, config.SCORE_URL,
                      body=fakes.SCORE_XML, status=200)
        listing = comm.get_upcoming()
        self.assertEqual(3, len(listing))
        self.assertIn('Roosters', listing[0].title)

    @responses.activate
    def test_get_score(self):
        responses.add(responses.GET, config.SCORE_URL,
                      body=fakes.SCORE_XML, status=200)
        score = comm.get_score(fakes.COMPLETED_MATCH_ID)
        self.assertEqual('[COLOR yellow]14 - 16[/COLOR]', score)

    @responses.activate
    def test_get_videos(self):
        responses.add(responses.GET, config.VIDEO_URL,
                      body=fakes.VIDEO_XML, status=200)
        videos = comm.get_videos({'category': 'Videos'})
        self.assertEqual(10, len(videos))
        self.assertEqual('1sbmc0aTE6v-w-7izv-_5ch2tP4ojgeY',
                         videos[4].video_id)

    @responses.activate
    def test_get_box_numbers(self):
        responses.add(responses.GET, config.HOME_URL, body=fakes.HOME_XML, status=200)
        observed = comm.get_box_numbers()
        self.assertEqual(['12345', '45678'], observed)


    @responses.activate
    @mock.patch('comm.get_box_numbers')
    def test_get_live_matches(self, mock_box_list):
        url = re.compile(config.BOX_URL.format('.*'))
        responses.add(responses.GET, url, body=fakes.BOX_XML, status=200)
        mock_box_list.return_value = ['12345']
        observed = comm.get_live_matches()
        self.assertEqual(1, len(observed))
        self.assertEqual('true', observed[0].live)
