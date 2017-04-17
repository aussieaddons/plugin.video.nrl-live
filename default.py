# Copyright 2016 Glenn Guy
# This file is part of NRL Live Kodi Addon
#
# NRL Live is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NRL Live is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NRL Live.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
from urlparse import parse_qsl

addon = xbmcaddon.Addon()
cwd = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
BASE_RESOURCE_PATH = os.path.join(cwd, 'resources', 'lib')
sys.path.append(BASE_RESOURCE_PATH)

import ooyalahelper  # noqa: E402
import play  # noqa: E402
import matches  # noqa: E402
import submenus  # noqa: E402
import categories  # noqa: E402

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
                matches.make_matches_list(params, live=True)
            elif params['category'] == 'shortlist':
                matches.make_matches_list(params)
            elif params['category'] == 'settings':
                addon.openSettings()
            else:
                submenus.list_years(params)
        elif params['action'] == 'listyears':
            submenus.list_comps(params)
        elif params['action'] == 'listcomps':
            if params['comp'] == '1':
                submenus.list_rounds(params)
            else:
                matches.make_matches_list(params)
        elif params['action'] == 'listrounds':
            matches.make_matches_list(params)
        elif params['action'] == 'listmatches':
            play.play_video(params)
        elif params['action'] == 'cleartoken':
            ooyalahelper.clear_token()
    else:
        categories.list_categories()


if __name__ == '__main__':
    if addon.getSetting('firstrun') == 'true':
        xbmcgui.Dialog().ok(addonname, ('Please enter your NRL Digital '
                                        'Pass (Telstra ID) username and '
                                        'password to access the content in '
                                        'this service.'))
        addon.openSettings()
        addon.setSetting('firstrun', 'false')
    router(sys.argv[2][1:])
