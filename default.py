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
import time
import datetime

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import urllib
import urllib2
from urlparse import parse_qsl
import xml.etree.ElementTree as ET
import cookielib

addon = xbmcaddon.Addon()
cwd = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
BASE_RESOURCE_PATH = os.path.join(cwd, 'resources', 'lib')
sys.path.append(BASE_RESOURCE_PATH)

import config
import ooyalahelper
from f4mproxy.F4mProxy import f4mProxyHelper

_url = sys.argv[0]
_handle = int(sys.argv[1])

addonname = addon.getAddonInfo('name')
addonPath = xbmcaddon.Addon().getAddonInfo("path")
fanart = os.path.join(addonPath, 'fanart.jpg')
username = addon.getSetting('username')
password = addon.getSetting('password')


class game():
    """ object that contains all the info for a particular match
        eventually will try to make this script more OO"""
    def __init__(self):
        self.videoID = None
        self.thumbLarge = None
        self.title = None
        self.live = None
        self.time = None
        self.matchID = None
        self.score = None
        self.desc = None

def get_upcoming():
    """ similar to get_score but this time we are searching for upcoming live
        match info"""
    xbmc.log("Fetching URL: ".format(config.SCORE_URL))
    response = urllib2.urlopen(config.SCORE_URL)
    tree = ET.fromstring(response.read())
    listing = []
    
    for elem in tree.findall("Day"):
        for subelem in elem.findall("Game"):
            if subelem.find('PercentComplete').text == '0':
                home = subelem.find('HomeTeam').attrib['FullName']
                away = subelem.find('AwayTeam').attrib['FullName']
                timestamp = subelem.find('Timestamp').text
                #convert zulu to local time
                delta = (time.mktime(
                        time.localtime()) - time.mktime(time.gmtime())) / 3600
                ts = datetime.datetime.fromtimestamp(
                    time.mktime(time.strptime(timestamp[:-1],
                     "%Y-%m-%dT%H:%M:%S")))
                ts += datetime.timedelta(hours=delta)
                airTime = ts.strftime("%A @ %I:%M %p")
                returnString = ('[COLOR red]Upcoming:[COLOR] '
                                '{0} v {1} - [COLOR yellow]{2}[/COLOR]')
                listing.append(returnString.format(home, away, airTime)) 
    return listing

def get_score(matchID):
    """fetch score xml and return the scores for corresponding match IDs"""
    xbmc.log("Fetching URL: ".format(config.SCORE_URL))
    response = urllib2.urlopen(config.SCORE_URL)
    tree = ET.fromstring(response.read())
    
    for elem in tree.findall("Day"):
        for subelem in elem.findall("Game"):     
            if subelem.attrib['Id'] == str(matchID):
                homeScore =  str(subelem.find('HomeTeam').attrib['Score'])
                awayScore = str(subelem.find('AwayTeam').attrib['Score'])
                return '[COLOR yellow]{0} - {1}[/COLOR]'.format(
            homeScore,awayScore)        
    
def get_url(category, year, comp, rnd, shortList):
    """ retrieve our xml file for processing"""
    if rnd == -1:
        rnd = ''
    else: rnd = '&round={0}'.format(rnd)
    if shortList == False:
        fullUrl = config.XML_URL.format(comp, rnd, category, year)
    else:
        fullUrl = config.SHORTLIST_URL
    xbmc.log("Fetching URL: ".format(fullUrl))
    response = urllib2.urlopen(fullUrl)
    return response.read()

def get_round_no():
    """ calculate what the current NRL round is"""
    date = datetime.date.today()
    r1 = datetime.date(2016,3,3)
    dateDelta = datetime.date.toordinal(date) - datetime.date.toordinal(r1)
    if datetime.date.toordinal(date) >= 736089: # 2 weeks between rd 9 and 10
        return (dateDelta // 7)
    else: 
        return (dateDelta // 7) + 1

def parse_round(category, year, comp, rnd=-1, live=False, shortList = False):
    """ go through our xml file and retrive all we need to pass to kodi"""
    data = get_url(category, year, comp, rnd, shortList)
    tree = ET.fromstring(data)
    listing = []
    
    if live == True:
        upcoming = get_upcoming()
        
        for event in upcoming:
            thumb = os.path.join(addonPath, 'resources', 'soon.jpg')
            li = xbmcgui.ListItem(event, iconImage = thumb)
            url = ''
            is_folder = False
            listing.append((url, li, is_folder))
        xbmcplugin.addSortMethod(_handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
        
    for elem in tree.findall("MediaSection"):
        
        for gm in elem.findall('Item'):
            
            # remove items with no video eg. news articles
            if not gm.attrib['Type'] == 'V':
                continue
            
            g = game()       
            
            g.title = gm.find('Title').text.encode('ascii', 'replace')
            
            if gm.find('Description'):
                g.desc = gm.find('Description').text.encode('ascii', 'replace')
            
            # remove PSA videos
            if g.title.startswith('Better Choices'):
                continue
            
            g.videoID = gm.find('Video').attrib['Id']
            
            g.live = gm.find('LiveNow').text
            
            # keep live videos out of other submenus and vice versa
            if live == False and g.live == 'true':
                continue
            if live == True and g.live == 'false':
                continue
            
            g.thumbLarge = gm.find('FullImageUrl').text
            
            g.time = gm.find('Date').text.encode('utf-8', 'replace')
            
            # add game start time and current score to live match entries
            if g.live == 'true':
                
                # only use live videos that are actual matches
                if gm.find('NavigateUrl'):
                    idString = gm.find('NavigateUrl').text
                    start = idString.find('=')+1
                    end = idString.find('&')
                    g.matchID = idString[start:end]
                    g.score = get_score(g.matchID)
                    g.title = '[COLOR red]Live Now:[/COLOR] {0} @{1} {2}'.format(
                    g.title, g.time[g.time.find(chr(128)):], g.score)    
                        
            li = xbmcgui.ListItem(label=str(g.title), iconImage=g.thumbLarge,
                                    thumbnailImage=g.thumbLarge)
            url = ('{0}?action=parseround&year={1}&rnd={2}&gm={3}&id={4}'
                    '&live={5}&thumb={6}&time={7}&score={8}'.format(
                    _url, year, rnd, g.title, g.videoID, g.live, 
                    g.thumbLarge, g.time, g.score))
            is_folder = False
            li.setProperty('IsPlayable', 'true')
            li.setInfo('video', {'plot': g.desc, 'plotoutline': g.desc})
            listing.append((url, li, is_folder))
            
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

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

def list_years(category):
    """ create a list of the years that match replays are currently
        available for"""
    listing = []
    for year in config.YEARS:
        li = xbmcgui.ListItem(str(year))
        urlString = '{0}?action=listyears&category={1}&year={2}'
        url = urlString.format(_url, category, year)
        is_folder = True
        listing.append((url, li, is_folder))
        
    xbmcplugin.addDirectoryItems(_handle, sorted(listing, reverse=True), 
                                len(listing))
    xbmcplugin.endOfDirectory(_handle)

def list_comps(category, year):
    """ make our list of competition categories"""
    listing = []
    comps = config.COMPS
    for comp in sorted(comps.keys()):
        li = xbmcgui.ListItem(comp[2:])
        urlString = '{0}?action=listcomps&category={1}&year={2}&comp={3}'
        url = urlString.format(_url, category, year, comps[comp])
        is_folder = True
        listing.append((url, li, is_folder))
        
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def list_rounds(category, year, comp):
    """ create list of rounds for the season. If in current year then only
        create to current date"""
    listing = []
     
    if year == '2016':
        noRounds = get_round_no()
    else:
        noRounds = 30
    for i in range(noRounds, 0, -1):
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
        urlString = (   '{0}?action=listrounds&category={1}'
                        '&year={2}&comp={3}&rnd={4}')
        url = urlString.format(_url, category, year, comp, i)
        is_folder = True
        listing.append((url, li, is_folder))
    
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def play_video(videoId, live):
    """
    Play a video by the provided path.
    :param path: str
    """
    loginToken = ooyalahelper.get_nrl_user_token(username, password)
    
    if loginToken == 'invalid':
        xbmcgui.Dialog().ok(addonname, ('Invalid username/password. '
                                            'Please check your settings and '
                                            'try again.'))
        return
    
    elif loginToken == 'nosub':
        xbmcgui.Dialog().ok(addonname, ('There was no active subscription'
                                            ' found on your NRL Digital Pass'
                                            ' subscription.'))
        return
    
    streamMethod = addon.getSetting('streammethod')

    if streamMethod == 'HLS (Lower quality)' or live == 'true':
        
        playlist = ooyalahelper.get_m3u8_playlist(videoId, live, loginToken, 'NRL')
        play_item = xbmcgui.ListItem(path=playlist)
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
    
    elif streamMethod == 'HDS (Higher quality, no seeking)':
        qual = addon.getSetting('HDSQUALITY')
        smil = ooyalahelper.fetch_nrl_smil(videoId)            
        url = ooyalahelper.get_nrl_hds_url(smil)
        player=f4mProxyHelper()
        urltoplay,item=player.playF4mLink(url, '', setResolved=True, maxbitrate=config.HDS_REPLAY_QUALITY[qual])
        play_item = xbmcgui.ListItem(path=urltoplay)
        xbmcplugin.setResolvedUrl(_handle, True, play_item)
        
    

def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring:
    """
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listcategories':
            if params['category'] == 'LiveMatches':
                parse_round('Matches', 2016, 1, get_round_no(), True)
            elif params['category'] == 'ShortList':
                parse_round(0,0,0,0,False, True)  
            else:
                list_years(params['category'])
        elif params['action'] == 'listyears':
            list_comps(params['category'], params['year'])
        elif params['action'] == 'listcomps':
            if params['comp'] == '1':
                list_rounds(params['category'], params['year'], params['comp'])
            else: parse_round(params['category'], params['year'], 
                                params['comp'], -1)
        elif params['action'] == 'listrounds':
            parse_round(params['category'], params['year'], 
                                params['comp'], params['rnd'])
        elif params['action'] == 'parseround':
            play_video(params['id'], params['live'])
    else:
        list_categories()

if __name__ == '__main__':
    if addon.getSetting('firstrun') == 'true':
        xbmcgui.Dialog().ok(addonname, ('Please enter your NRL Digital '
                                    'Pass (Tesltra ID) username '),(
                                    ' and password to access the content in'
                                    ' this service.'))
        addon.openSettings()
        addon.setSetting('firstrun', 'false')
    router(sys.argv[2][1:])

