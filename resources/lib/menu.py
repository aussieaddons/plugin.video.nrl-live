import comm
import config
import datetime
import os
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
from aussieaddonscommon import utils

_handle = int(sys.argv[1])
_url = sys.argv[0]
addonPath = xbmcaddon.Addon().getAddonInfo("path")


def get_round_no():
    """ calculate what the current NRL round is"""
    date = datetime.date.today()
    r1 = datetime.date(2017, 3, 2)
    dateDelta = datetime.date.toordinal(date) - datetime.date.toordinal(r1)
    if datetime.date.toordinal(date) >= 736453:  # 2 weeks between rd 9 and 10
        round_no = dateDelta // 7
    else:
        round_no = (dateDelta // 7) + 1
    if round_no > 30:
        return 30
    else:
        return round_no

def list_rounds(params):
    """ create list of rounds for the season. If in current year then only
        create to current date"""
    try:
        listing = []
        params['action'] = 'listrounds'
        if params['year'] == '2017':
            no_of_rounds = get_round_no()
        else:
            no_of_rounds = 30
        for i in range(no_of_rounds, 0, -1):
            params['rnd'] = str(i)
            if i <= 26:
                li = xbmcgui.ListItem('Round ' + str(i))
            elif i == 27:
                li = xbmcgui.ListItem('Finals Week 1')
            elif i == 28:
                li = xbmcgui.ListItem('Semi Finals')
            elif i == 29:
                li = xbmcgui.ListItem('Preliminary Finals')
            elif i == 30:
                li = xbmcgui.ListItem('Grand Final')
            url = '{0}?{1}'.format(_url, utils.make_url(params))
            is_folder = True
            listing.append((url, li, is_folder))

        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)
    except Exception:
        utils.handle_error('Unable to list rounds')


def list_years(params):
    """ create a list of the years that match replays are currently
        available for"""
    try:
        listing = []
        params['action'] = 'listyears'
        for year in config.YEARS:
            params['year'] = year
            li = xbmcgui.ListItem(str(year))
            url = '{0}?{1}'.format(_url, utils.make_url(params))
            is_folder = True
            listing.append((url, li, is_folder))

        xbmcplugin.addDirectoryItems(_handle,
                                     sorted(listing, reverse=True),
                                     len(listing))
        xbmcplugin.endOfDirectory(_handle)
    except Exception:
        utils.handle_error('Unable to list years')


def list_videos(params):
    """ make our list of videos"""
    try:
        video_list = comm.get_videos(params)
        listing = []
        for v in video_list:
            li = xbmcgui.ListItem(v.title)
            li.setProperty('IsPlayable', 'true')
            li.setInfo('video', {'plot': v.desc, 'plotoutline': v.desc})
            url = '{0}?action=listvideos{1}'.format(_url, v.make_kodi_url())
            is_folder = False
            listing.append((url, li, is_folder))

        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)
    except Exception:
        utils.handle_error('Unable to list comps')


def list_categories():
    try:
        #categories = []
        #categories.append('Live Matches')
        #for entry in comm.get_categories():
            #categories.append(entry)
        #categories.append('Settings')
        
        listing = []
        for category in config.CATEGORIES:
            li = xbmcgui.ListItem(category)
            urlString = '{0}?action=listcategories&category={1}'
            url = urlString.format(_url, category)
            is_folder = True
            listing.append((url, li, is_folder))

        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)
    except Exception:
        utils.handle_error('Unable to make categories list')


def list_matches(params, live=False):
    """
    """
    try:
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
                li = xbmcgui.ListItem(event.title, iconImage=thumb)
                url = '{0}?action=listmatches{1}'.format(
                    _url, event.make_kodi_url())
                is_folder = False
                listing.append((url, li, is_folder))
            xbmcplugin.addSortMethod(
                _handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)

        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)
    except Exception:
        utils.handle_error('Unable to fetch match list')
