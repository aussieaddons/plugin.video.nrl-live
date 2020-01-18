import sys

from aussieaddonscommon import utils

from resources.lib import comm
from resources.lib import ooyalahelper

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
        if params.get('live') != 'true':
            playlist = comm.get_stream_url(video_id)
        else:
            pcode = ''
            if 'p_code' in params:
                pcode = params['p_code']
            playlist = ooyalahelper.get_m3u8_playlist(video_id, pcode)

        play_item = xbmcgui.ListItem(path=playlist)
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

    except Exception:
        utils.handle_error('Unable to play video')
        raise
