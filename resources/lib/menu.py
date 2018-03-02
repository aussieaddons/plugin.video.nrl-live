import comm
import config
import os
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
from aussieaddonscommon import utils

_handle = int(sys.argv[1])
_url = sys.argv[0]
addonPath = xbmcaddon.Addon().getAddonInfo("path")


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
            li = xbmcgui.ListItem(v.title, thumbnailImage=v.thumb)
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
