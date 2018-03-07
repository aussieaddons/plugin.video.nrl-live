import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
from urlparse import parse_qsl

# fix for python importerror bug
import _strptime  # noqa: F401

from aussieaddonscommon import utils

addon = xbmcaddon.Addon()
cwd = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
BASE_RESOURCE_PATH = os.path.join(cwd, 'resources', 'lib')
sys.path.append(BASE_RESOURCE_PATH)

import menu  # noqa: E402
import ooyalahelper  # noqa: E402
import play  # noqa: E402

_url = sys.argv[0]
_handle = int(sys.argv[1])
addonname = addon.getAddonInfo('name')
addonPath = xbmcaddon.Addon().getAddonInfo("path")
fanart = os.path.join(addonPath, 'fanart.jpg')


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
            ooyalahelper.clear_ticket()
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
