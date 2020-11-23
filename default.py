import sys

# fix for python importerror bug
import _strptime  # noqa: F401

from future.moves.urllib.parse import parse_qsl

from aussieaddonscommon import utils

from resources.lib import menu
from resources.lib import play
from resources.lib import stream_auth

import xbmcaddon

import xbmcgui

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring:
    """
    params = dict(parse_qsl(paramstring))
    utils.log('Running with params: {0}'.format(params))
    if params:
        if params['action'] == 'listcategories':
            if params['category'] == 'Live Matches':
                menu.list_matches(params, live=True)
            elif params['category'] == 'Settings':
                addon.openSettings()
            else:
                menu.list_videos(params)
        elif params['action'] in ['listvideos', 'listmatches']:
            play.play_video(params)
        elif params['action'] == 'clearticket':
            stream_auth.clear_ticket()
        elif params['action'] == 'open_ia_settings':
            try:
                import drmhelper
                if drmhelper.check_inputstream(drm=False):
                    ia = drmhelper.get_addon()
                    ia.openSettings()
                else:
                    utils.dialog_message(
                        "Can't open inputstream.adaptive settings")
            except Exception:
                utils.dialog_message(
                    "Can't open inputstream.adaptive settings")
    else:
        menu.list_categories()


if __name__ == '__main__':
    if addon.getSetting('firstrun') == 'true':
        xbmcgui.Dialog().ok(addonname, ('Please choose your subscription type '
                                        'and enter your NRL Live Pass '
                                        'username and password to access the '
                                        'content in this service.'))
        addon.openSettings()
        addon.setSetting('firstrun', 'false')
    router(sys.argv[2][1:])
