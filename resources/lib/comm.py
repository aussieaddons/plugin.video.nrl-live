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

import xml.etree.ElementTree as ET
import classes
import xbmc
import urllib2
import utils
import config
import time
import datetime


def list_matches(params, live=False):
    """ go through our xml file and retrive all we need to pass to kodi"""
    data = get_url(params, live)
    tree = ET.fromstring(data)
    listing = []
    for elem in tree.findall("MediaSection"):
        for gm in elem.findall('Item'):
            # remove items with no video eg. news articles
            if not gm.attrib['Type'] == 'V':
                continue
            g = classes.game()       
            g.title = gm.find('Title').text.encode('ascii', 'replace')
            if gm.find('Description'):
                g.desc = gm.find('Description').text.encode('ascii', 'replace')
            # remove PSA videos
            if g.title.startswith('Better Choices'):
                continue
            g.video_id = gm.find('Video').attrib['Id']
            g.live = gm.find('LiveNow').text
            # keep live videos out of other submenus and vice versa
            if not live and g.live == 'true':
                continue
            if live and g.live == 'false':
                continue
            g.thumb = gm.find('FullImageUrl').text
            g.time = utils.ensure_ascii(gm.find('Date').text)
            # add game start time and current score to live match entries
            if g.live: 
                # only use live videos that are actual matches
                if gm.find('NavigateUrl'):
                    id_string = gm.find('NavigateUrl').text
                    start = id_string.find('=')+1
                    end = id_string.find('&')
                    g.match_id = id_string[start:end]
                    g.score = get_score(g.match_id)
                    g.title = '[COLOR red]Live Now:[/COLOR] {0} @{1} {2}'.format(
                    g.title, g.time[g.time.find(chr(128)):], g.score)    
            listing.append(g)
    return listing

def get_upcoming():
    """ similar to get_score but this time we are searching for upcoming live
        match info"""
    utils.log("Fetching URL: ".format(config.SCORE_URL))
    response = urllib2.urlopen(config.SCORE_URL)
    tree = ET.fromstring(response.read())
    listing = []
    
    for elem in tree.findall("Day"):
        for subelem in elem.findall("Game"):
            if subelem.find('PercentComplete').text == '0':
                g = classes.game()
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
                g.title = returnString.format(home, away, airTime)
                g.dummy = True
                listing.append(g)
    return listing

def get_score(match_id):
    """fetch score xml and return the scores for corresponding match IDs"""
    utils.log("Fetching URL: ".format(config.SCORE_URL))
    response = urllib2.urlopen(config.SCORE_URL)
    tree = ET.fromstring(response.read())

    for elem in tree.findall("Day"):
        for subelem in elem.findall("Game"):     
            if subelem.attrib['Id'] == str(match_id):
                home_score =  str(subelem.find('HomeTeam').attrib['Score'])
                away_score = str(subelem.find('AwayTeam').attrib['Score'])
                return '[COLOR yellow]{0} - {1}[/COLOR]'.format(
            home_score,away_score)        

def get_url(params, live=False):
    """ retrieve our xml file for processing"""
    category = params['category']
    if not 'rnd' in params:
        params['rnd'] = 1
    if params['rnd'] == -1:
        rnd = ''
    else: 
        rnd = '&round={0}'.format(params['rnd'])
    
    if live:
        category = 'Matches'
        params.update({'comp': 1, 'year': 2017})

    if params['category'] == 'shortlist':
        fullUrl = config.SHORTLIST_URL
    else:
        fullUrl = config.XML_URL.format(params['comp'], 
                                        rnd, 
                                        category, 
                                        params['year'])

    utils.log("Fetching URL: ".format(fullUrl))
    response = urllib2.urlopen(fullUrl)
    return response.read()