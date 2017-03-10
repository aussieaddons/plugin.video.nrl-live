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

import xbmcaddon
import xbmcgui
import xbmcplugin
import sys
import config
import ooyalahelper
import utils

addon = xbmcaddon.Addon()
_handle = int(sys.argv[1])

def play_video(params):
    """
    Play a video by the provided path.
    :param path: str
    """
    if 'dummy' in params:
        if params['dummy'] == 'True':
            return
    try:
        live = params['live'] == 'true'
        video_id = params['video_id']
        playlist = ooyalahelper.get_m3u8_playlist(video_id, live)
        play_item = xbmcgui.ListItem(path=playlist)
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
        
    except Exception as e:
        utils.handle_error('', e)