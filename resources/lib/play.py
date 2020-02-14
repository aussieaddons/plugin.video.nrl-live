import sys

from aussieaddonscommon import utils

from resources.lib import comm
from resources.lib import stream_auth

import xbmcaddon

import xbmcgui

import xbmcplugin

addon = xbmcaddon.Addon()
_handle = int(sys.argv[1])


def play_video(params):
    """
    Play a video by the provided path.
    :param path: str
    """
    if 'dummy' in params:
        if params['dummy'] == 'True':
            return

    try:
        video_id = params['video_id']
        playlist = comm.get_stream_url(video_id)
        play_item = xbmcgui.ListItem(path=playlist)
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

    except Exception:
        utils.handle_error('Unable to play video')
        raise
