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


import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import comm
import sys
import os
import urlparse

_url = sys.argv[0]
_handle = int(sys.argv[1])
addonPath = xbmcaddon.Addon().getAddonInfo("path")

def make_matches_list(params, live=False):
    """
    """
    listing = []
    matches = comm.list_matches(params, live)
            
    for m in matches:
        li = xbmcgui.ListItem(label=str(m.title), iconImage=m.thumb,
                                    thumbnailImage=m.thumb)
        url = '{0}?action=listmatches{1}'.format(_url, m.make_kodi_url())
        is_folder = False
        li.setProperty('IsPlayable', 'true')
        li.setInfo('video', {'plot': m.desc, 'plotoutline': m.desc})
        listing.append((url, li, is_folder))
    
    if live:
        upcoming = comm.get_upcoming()
        for event in upcoming:
            thumb = os.path.join(addonPath, 'resources', 'soon.jpg')
            li = xbmcgui.ListItem(event.title, iconImage = thumb)
            url = '{0}?action=listmatches{1}'.format(_url, event.make_kodi_url())
            is_folder = False
            listing.append((url, li, is_folder))
        xbmcplugin.addSortMethod(_handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)