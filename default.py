import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
from urlparse import parse_qsl

# fix for python importerror bug
import _strptime  # noqa: F401

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
    if params:
        if params['action'] == 'listcategories':
            if params['category'] == 'livematches':
                menu.list_matches(params, live=True)
            elif params['category'] == 'shortlist':
                menu.list_matches(params)
            elif params['category'] == 'settings':
                addon.openSettings()
            else:
                menu.list_years(params)
        elif params['action'] == 'listyears':
            menu.list_comps(params)
        elif params['action'] == 'listcomps':
            if params['comp'] == '1':
                menu.list_rounds(params)
            else:
                menu.list_matches(params)
        elif params['action'] == 'listrounds':
            menu.list_matches(params)
        elif params['action'] == 'listmatches':
            play.play_video(params)
        elif params['action'] == 'cleartoken':
            ooyalahelper.clear_token()
    else:
        menu.list_categories()


if __name__ == '__main__':
    if addon.getSetting('firstrun') == 'true':
        xbmcgui.Dialog().ok(addonname, ('Please enter your NRL Digital '
                                        'Pass (Telstra ID) username and '
                                        'password to access the content in '
                                        'this service.'))
        addon.openSettings()
        addon.setSetting('firstrun', 'false')
    router(sys.argv[2][1:])
