import sys

from aussieaddonscommon import utils

from resources.lib import classes
from resources.lib import comm
# from resources.lib import stream_auth

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

    v = classes.Video()
    v.parse_params(params)

    try:
        # ticket = stream_auth.get_user_ticket()
        media_auth_token = None
        # if v.live == 'true':
        #    media_auth_token = stream_auth.get_media_auth_token(
        #        ticket, v.video_id)
        playlist = comm.get_stream_url(v, media_auth_token)
        play_item = xbmcgui.ListItem(path=playlist)
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

    except Exception:
        utils.handle_error('Unable to play video')
        raise
