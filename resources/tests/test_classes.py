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


import classes

class UtilsTests(testtools.TestCase):

    def test_make_kodi_url(self):
        video = classes.Video()
        attrs = OrderedDict(sorted(fakes.FAKE_VIDEO_ATTRS.items(), key=lambda x: x[0]))
        for k, v in attrs.iteritems():
            setattr(video, k, v)
        self.assertEqual(fakes.FAKE_VIDEO_URL, video.make_kodi_url())

    def test_parse_kodi_url(self):
        video = classes.Video()
        video.parse_kodi_url(fakes.FAKE_VIDEO_URL)
        observed = video.make_kodi_url()
        self.assertEqual(fakes.FAKE_VIDEO_URL, observed)

