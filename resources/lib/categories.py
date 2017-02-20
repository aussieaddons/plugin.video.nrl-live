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
import config
import sys

_handle = int(sys.argv[1])
_url = sys.argv[0]

def list_categories():
    listing = []
    categories = config.CATEGORIES
    for category in sorted(categories.keys()):
        li = xbmcgui.ListItem(category[2:])
        urlString = '{0}?action=listcategories&category={1}'
        url = urlString.format(_url, categories[category])
        is_folder = True
        listing.append((url, li, is_folder))
        
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)