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
from f4mproxy.F4mProxy import f4mProxyHelper
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
        stream_method = addon.getSetting('streammethod')
        if stream_method == '':
            addon.setSetting('streammethod', 'HLS (Lower quality)')
        
        live = params['live'] == 'true'
        video_id = params['video_id']
        if stream_method == 'HLS (Lower quality)' or live:
            
            playlist = ooyalahelper.get_m3u8_playlist(video_id, live)
            play_item = xbmcgui.ListItem(path=playlist)
            xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
        
        elif stream_method == 'HDS (Higher quality, no seeking)':
            ooyalahelper.get_nrl_user_token()
            qual = addon.getSetting('HDSQUALITY')
            smil = ooyalahelper.fetch_nrl_smil(video_id)            
            url = ooyalahelper.get_nrl_hds_url(smil)
            player=f4mProxyHelper()
            urltoplay,item=player.playF4mLink(url, '', setResolved=True, 
                                        maxbitrate=config.HDS_REPLAY_QUALITY[qual])
            play_item = xbmcgui.ListItem(path=urltoplay)
            xbmcplugin.setResolvedUrl(_handle, True, play_item)
    except Exception as e:
        utils.handle_error('', e)