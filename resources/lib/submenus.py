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
import sys
import config
import utils

_handle = int(sys.argv[1])
_url = sys.argv[0]

def list_rounds(params):
    """ create list of rounds for the season. If in current year then only
        create to current date"""
    listing = []
    params['action'] = 'listrounds'
    if params['year'] == '2017':
        no_of_rounds = utils.get_round_no()
    else:
        no_of_rounds = 30
    for i in range(no_of_rounds, 0, -1):
        params['rnd'] = str(i)
        if i <= 26:
            li = xbmcgui.ListItem('Round '+ str(i))
        elif i == 27:
            li = xbmcgui.ListItem('Finals Week 1')
        elif i == 28:
            li = xbmcgui.ListItem('Semi Finals')
        elif i == 29:
            li = xbmcgui.ListItem('Preliminary Finals')
        elif i == 30:
            li = xbmcgui.ListItem('Grand Final')
        url = '{0}?{1}'.format(_url, utils.make_url(params))
        #urlString = (   '{0}?action=listrounds&category={1}'
        #                '&year={2}&comp={3}&rnd={4}')
        #url = urlString.format(_url, category, year, comp, i)
        is_folder = True
        listing.append((url, li, is_folder))
    
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)
    
def list_years(params):
    """ create a list of the years that match replays are currently
        available for"""
    listing = []
    params['action'] = 'listyears'
    for year in config.YEARS:
        params['year'] = year
        li = xbmcgui.ListItem(str(year))
        url = '{0}?{1}'.format(_url, utils.make_url(params))
        is_folder = True
        listing.append((url, li, is_folder))
        
    xbmcplugin.addDirectoryItems(_handle, sorted(listing, reverse=True), 
                                len(listing))
    xbmcplugin.endOfDirectory(_handle)

def list_comps(params):
    """ make our list of competition categories"""
    listing = []
    params['action'] = 'listcomps'
    comps = config.COMPS
    for comp in sorted(comps.keys()):
        params['comp'] = comps[comp]
        li = xbmcgui.ListItem(comp[2:])
        url = '{0}?{1}'.format(_url, utils.make_url(params))
        is_folder = True
        listing.append((url, li, is_folder))
        
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)      