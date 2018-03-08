import classes
import config
import datetime
import json
import re
import time
import xml.etree.ElementTree as ET

from aussieaddonscommon import utils
from aussieaddonscommon import session

from bs4 import BeautifulSoup


def get_airtime(timestamp):
    try:
        delta = (time.mktime(time.localtime()) -
                 time.mktime(time.gmtime())) / 3600
        if time.localtime().tm_isdst:
            delta += 1
        ts = datetime.datetime.fromtimestamp(
            time.mktime(time.strptime(timestamp[:-1], "%Y-%m-%dT%H:%M:%S")))
        ts += datetime.timedelta(hours=delta)
        return ts.strftime("%A %d %b @ %I:%M %p").replace(' 0', ' ')
    except OverflowError:
        return ''


def fetch_url(url):
    """
    HTTP GET on url, remove byte order mark
    """
    with session.Session() as sess:
        resp = sess.get(url)
        return resp.text.encode("utf-8")


def list_matches(params, live=False):
    """ go through our xml file and retrive all we need to pass to kodi"""
    data = fetch_url(config.VIDEO_URL)
    tree = ET.fromstring(data)
    listing = []
    for elem in tree.findall("MediaSection"):
        for gm in elem.findall('Item'):
            # remove items with no video eg. news articles
            if not gm.attrib['Type'] == 'V':
                continue
            g = classes.Video()
            g.title = gm.find('Title').text.encode('ascii', 'replace')
            desc = gm.find('Description')
            if desc:
                if desc.text is not None:
                    g.desc = gm.find('Description').text.encode('ascii',
                                                                'replace')
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
            game_date = utils.ensure_ascii(gm.find('Date').text)
            g.time = game_date[game_date.find('  ')+2:]
            # add game start time and current score to live match entries
            if g.live:
                # only use live videos that are actual matches
                if gm.find('NavigateUrl') is not None:
                    id_string = gm.find('NavigateUrl').text
                    start = id_string.find('=')+1
                    end = id_string.find('&')
                    g.match_id = id_string[start:end]
                    g.score = get_score(g.match_id)
                    title = '[COLOR green][LIVE NOW:][/COLOR] {0} {1}'
                    g.title = title.format(
                        g.title.replace(' LIVE', ''), g.score)
            listing.append(g)
    return listing


def get_upcoming():
    """ similar to get_score but this time we are searching for upcoming live
        match info"""
    tree = ET.fromstring(fetch_url(config.SCORE_URL))
    listing = []
    for elem in tree.findall("Day"):
        for subelem in elem.findall("Game"):
            if subelem.find('PercentComplete').text == '0':
                g = classes.Video()
                home = subelem.find('HomeTeam').attrib['Name']
                away = subelem.find('AwayTeam').attrib['Name']
                timestamp = subelem.find('Timestamp').text
                # convert zulu to local time
                airtime = get_airtime(timestamp)
                title = ('[COLOR red]Upcoming:[/COLOR] '
                         '{0} v {1} - [COLOR yellow]{2}[/COLOR]')
                g.title = title.format(home, away, airtime)
                g.dummy = True
                listing.append(g)
    return listing


def get_score(match_id):
    """fetch score xml and return the scores for corresponding match IDs"""
    tree = ET.fromstring(fetch_url(config.SCORE_URL))
    for elem in tree.findall("Day"):
        for subelem in elem.findall("Game"):
            if subelem.attrib['Id'] == str(match_id):
                home_score = str(subelem.find('HomeTeam').attrib['Score'])
                away_score = str(subelem.find('AwayTeam').attrib['Score'])
                return '[COLOR yellow]{0} - {1}[/COLOR]'.format(
                    home_score, away_score)


def get_videos(params):
    if params.get('category') == 'Match Highlights':
        data_url = config.HIGHLIGHTS_URL
    else:
        data_url = config.VIDEO_URL
    tree = ET.fromstring(fetch_url(data_url))
    listing = []
    for item in tree.find('MediaSection'):
        v = classes.Video()
        v.desc = item.find('Description').text
        v.title = item.find('Title').text
        v.time = item.find('Timestamp').text
        video_id = item.find('Video')
        if video_id is not None:
            v.video_id = video_id.attrib.get('Id')
        v.thumb = item.find('FullImageUrl').text
        v.link_id = item.find('Id').text
        listing.append(v)
    return listing


def get_replay_playlist(params):
    data_url = config.MEDIA_URL.format(params.get('link_id'))
    tree = ET.fromstring(fetch_url(data_url))
    html_data = tree.find('StoryHtml').text
    soup = BeautifulSoup(html_data, 'html.parser')
    src = soup.findAll(id=re.compile("^ls_embed"))[0].get('src')
    ls_soup = BeautifulSoup(fetch_url(src), 'html.parser')
    ls_text = ls_soup.findAll(
        'script', string=re.compile("^window.config"))[0].string
    ls_json = json.loads(ls_text[ls_text.find('{'):ls_text.rfind('}') + 1])
    stream_json = ls_json.get('event').get('feed').get('data')
    stream = stream_json[0].get('data').get('secure_m3u8_url')
    return stream


def get_live_matches():
    listing = []
    for box in get_box_numbers():
        tree = ET.fromstring(fetch_url(config.BOX_URL.format(box)))
        if tree.find('LiveVideo') is not None:
            for item in tree.find('LiveVideo').findall('Item'):
                v = classes.Video()
                v.title = item.find('Title').text
                v.time = item.find('Timestamp').text
                v.video_id = item.find('Video').attrib.get('Id')
                v.thumb = item.find('FullImageUrl').text
                v.link_id = item.find('Id').text
                listing.append(v)
    return listing
    
def get_box_numbers():
    tree = ET.fromstring(fetch_url(config.HOME_URL))
    listing = []
    for item in tree.find('HeadlineItems'):
        if item.attrib['Type'] == 'BoxScore':
            listing.append(item.attrib['Id'])
    return listing

def get_categories():
    tree = ET.fromstring(fetch_url(config.SHORTLIST_URL.format('')))
    listing = []
    for item in tree.find('Filters').find('Filter').find('FilterItems'):
        listing.append(item.attrib['Id'])
    return listing


def get_url(params, live=False):
    """ retrieve our xml file for processing"""
    category = params['category']
    if 'rnd' not in params:
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
    return fetch_url(fullUrl)
