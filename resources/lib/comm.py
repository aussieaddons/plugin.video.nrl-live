import base64
import datetime
import hashlib
import json
import re
import time
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

from future.moves.urllib.parse import quote

from aussieaddonscommon import session
from aussieaddonscommon import utils

from resources.lib import classes
from resources.lib import config


def get_tz_delta():
    delta = (time.mktime(time.localtime()) -
             time.mktime(time.gmtime())) / 3600
    if time.localtime().tm_isdst:
        delta += 1
    return delta

def get_airtime(timestamp):
    try:
        delta = get_tz_delta()
        ts = datetime.datetime.fromtimestamp(
            time.mktime(time.strptime(timestamp[:-1], "%Y-%m-%dT%H:%M:%S")))
        ts += datetime.timedelta(hours=delta)
        return ts.strftime("%A %d %b @ %I:%M %p").replace(' 0', ' ')
    except OverflowError:
        return ''


def fetch_url(url, remove_bom=True, headers=None):
    """
    HTTP GET on url, remove byte order mark
    """
    with session.Session() as sess:
        if headers:
            sess.headers.update(headers)
        resp = sess.get(url)
        if remove_bom:
            resp.encoding = 'utf-8-sig'
        return resp.text.encode("utf-8")


def get_authorization():
    tm = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    ts = tm.strftime("%Y-%m-%dT%H:00")
    auth_str = config.STREAM_AUTH_SECRET + ts
    m = hashlib.sha1()
    m.update(bytes(auth_str))
    password = base64.b64encode(m.digest())
    auth = 'mobile-app-nrl:{0}'.format(password)
    return base64.b64encode(auth)


def list_matches(params):
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
            g.title = utils.ensure_ascii(gm.find('Title').text)
            desc = gm.find('Description')
            if desc is not None:
                if desc.text is not None:
                    g.desc = gm.find('Description').text.encode('ascii',
                                                                'replace')
            # remove PSA videos
            if g.title.startswith('Better Choices'):
                continue
            g.video_id = gm.find('Video').attrib['Id']

            # keep live videos out of other submenus and vice versa
            if not gm.find('LiveNow').text:
                continue

            g.thumb = gm.find('FullImageUrl').text
            game_date = utils.ensure_ascii(gm.find('Date').text)
            g.time = game_date[game_date.find('  ')+2:]
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
    category = params.get('category')
    if category in ['Match Highlights', 'Match Replays']:
        data_url = config.TOPICS_URL.format(
            quote(config.CATEGORY_LOOKUP[category]))
    else:
        data_url = config.VIDEO_URL
    tree = ET.fromstring(fetch_url(data_url))
    listing = []
    for section in tree.findall('MediaSection'):
        for item in section:
            if not item.attrib['Type'] == 'V':
                continue
            v = classes.Video()
            v.desc = item.find('Description').text
            v.title = item.find('Title').text
            v.time = item.find('Timestamp').text
            video_id = item.find('Video')
            if video_id is not None:
                #v.p_code = video_id.attrib.get('PCode')
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
                v.p_code = item.find('Video').attrib.get('PCode')
                v.thumb = item.find('FullImageUrl').text
                v.link_id = item.find('Id').text
                v.live = 'true'
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


def get_stream_url(video_id):
    headers = {'authorization': 'basic {0}'.format(get_authorization())}
    data = fetch_url(config.STREAM_API_URL.format(video_id=video_id),
                     headers=headers)
    hls_url = json.loads(data).get('hls')
    return str(hls_url.replace('[[FILTER]]', 'nrl-vidset-ms'))
