import comm
import config
import os
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin
from aussieaddonscommon import utils

addonPath = xbmcaddon.Addon().getAddonInfo("path")


def list_categories():
    try:
        handle = int(sys.argv[1])
        plugin_url = sys.argv[0]
        listing = []
        for category in config.CATEGORIES:
            li = xbmcgui.ListItem(category)
            urlString = '{0}?action=listcategories&category={1}'
            url = urlString.format(plugin_url, category)
            is_folder = True
            listing.append((url, li, is_folder))
        xbmcplugin.addDirectoryItems(handle, listing, len(listing))
        xbmcplugin.endOfDirectory(handle)
    except Exception:
        utils.handle_error('Unable to make categories list')
        raise


def list_videos(params):
    """ make our list of videos"""
    try:
        handle = int(sys.argv[1])
        plugin_url = sys.argv[0]
        video_list = comm.get_videos(params)
        listing = []
        for v in video_list:
            li = xbmcgui.ListItem(v.title, thumbnailImage=v.thumb)
            li.setProperty('IsPlayable', 'true')
            li.setInfo('video', {'plot': v.desc, 'plotoutline': v.desc})
            url = '{0}?action=listvideos{1}'.format(plugin_url,
                                                    v.make_kodi_url())
            is_folder = False
            listing.append((url, li, is_folder))

        xbmcplugin.addDirectoryItems(handle, listing, len(listing))
        xbmcplugin.endOfDirectory(handle)
    except Exception:
        utils.handle_error('Unable to list comps')
        raise


def list_matches(params, live=False):
    """
    """
    try:
        handle = int(sys.argv[1])
        plugin_url = sys.argv[0]
        listing = []
        if not live:
            matches = comm.list_matches(params)
        else:
            matches = comm.get_live_matches()

        for m in matches:
            li = xbmcgui.ListItem(label=str(m.title), iconImage=m.thumb,
                                  thumbnailImage=m.thumb)
            url = '{0}?action=listmatches{1}'.format(plugin_url,
                                                     m.make_kodi_url())
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
                    plugin_url, event.make_kodi_url())
                is_folder = False
                listing.append((url, li, is_folder))
            xbmcplugin.addSortMethod(
                handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)

        xbmcplugin.addDirectoryItems(handle, listing, len(listing))
        xbmcplugin.endOfDirectory(handle)
    except Exception:
        utils.handle_error('Unable to fetch match list')
        raise
