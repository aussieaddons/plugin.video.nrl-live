import base64
import config
import json
import re
import requests
import StringIO
import telstra_auth
import urllib
import xbmcaddon
import xml.etree.ElementTree as ET

from aussieaddonscommon.exceptions import AussieAddonsException
from aussieaddonscommon import session
from aussieaddonscommon import utils

try:
    import StorageServer
except:
    utils.log("script.common.plugin.cache not found!")
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer(config.ADDON_ID, 1)
sess = session.Session()
addon = xbmcaddon.Addon()
telstra_username = addon.getSetting('LIVE_USERNAME')
telstra_password = addon.getSetting('LIVE_PASSWORD')
nrl_username = addon.getSetting('NRL_USERNAME')
nrl_password = addon.getSetting('NRL_PASSWORD')


def clear_ticket():
    """
    Remove stored ticket from cache storage
    """
    cache.delete('NRLTICKET')
    utils.dialog_message('Login token removed')


def get_user_ticket():
    """
    send user login info and retrieve ticket for session
    """
    stored_ticket = cache.get('NRLTICKET')
    if stored_ticket != '':
        utils.log('Using ticket: {0}******'.format(stored_ticket[:-6]))
        return stored_ticket
    sub_type = int(addon.getSetting('SUBSCRIPTION_TYPE'))

    if sub_type == 1:
        ticket = telstra_auth.get_free_token(telstra_username,
                                             telstra_password)
    elif sub_type == 2:  # mobile activated subscription
            ticket = telstra_auth.get_mobile_token()
    else:
        ticket = telstra_auth.get_paid_token(nrl_username,
                                             nrl_password)
    cache.set('NRLTICKET', ticket)
    return ticket


def create_nrl_userid_xml(user_id):
    """
    create a small xml file to send with http POST
    when starting a new video request
    """
    root = ET.Element('Subscription')
    ut = ET.SubElement(root, 'UserToken')
    ut.text = user_id
    fakefile = StringIO.StringIO()
    tree = ET.ElementTree(root)
    tree.write(fakefile, encoding='UTF-8')
    output = fakefile.getvalue()
    return output


def get_embed_token(login_ticket, videoId):
    """
    send our user token to get our embed token, including api key
    """
    url = config.EMBED_TOKEN_URL.format(videoId)
    try:
        headers = {}
        headers.update({'X-YinzCam-AppID': 'NRL_LIVE',
                        'X-YinzCam-Ticket': login_ticket,
                        'Content-Type': 'application/xml',
                        'Accept': 'application/xml',
                        'Accept-Encoding': 'gzip',
                        'User-Agent': config.USER_AGENT,
                        'Connection': 'close'})
        sess.headers = headers
        try:
            req = sess.get(url, verify=False)
            xml = req.text
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                cache.delete('NRLTICKET')
                raise AussieAddonsException('Login token has expired, '
                                            'please try again.')
            elif e.response.status_code == 403:
                cache.delete('NRLTICKET')
                tree = ET.fromstring(e.response.text)
                msg = str(tree.find('UserMessage').find('Content').text)
                raise AussieAddonsException(msg)
            else:
                raise e
        try:
            tree = ET.fromstring(xml)
        except ET.ParseError as e:
            utils.log('Embed token response is: {0}'.format(xml))
            cache.delete('NRLTICKET')
            raise e
        if tree.find('ErrorCode') is not None:
            utils.log('Errorcode found: {0}'.format(xml))
            raise AussieAddonsException('Login token has expired, '
                                        'please try again.')
        token = tree.find('VideoToken').text
    except AussieAddonsException as e:
        cache.delete('NRLTICKET')
        raise e
    return token


def get_secure_token(secure_url, videoId):
    """
    send our embed token back with a few other url encoded parameters
    """
    sess.headers = {'Accept-Encoding': 'gzip', 'User-Agent': config.USER_AGENT}
    res = sess.get(secure_url)
    data = res.text
    try:
        parsed_json = json.loads(data)
        token = (parsed_json['authorization_data'][videoId]
                 ['streams'][0]['url']['data'])
    except KeyError:
        utils.log('Parsed json data: {0}'.format(parsed_json))
        try:
            auth_msg = parsed_json['authorization_data'][videoId]['message']
            if auth_msg == 'unauthorized location':
                country = parsed_json['user_info']['country']
                raise AussieAddonsException(
                    'Unauthorised location for streaming. '
                    'Detected location is: {0}. '
                    'Please check VPN/smart DNS settings '
                    ' and try again'.format(country))
            else:
                raise Exception('Error: {0}'.format(auth_msg))
        except Exception as e:
            raise e
    return base64.b64decode(token)


def get_m3u8_streams(secure_token_url):
    """
    fetch our m3u8 file which contains streams of various qualities
    """
    res = sess.get(secure_token_url)
    data = res.text.splitlines()
    return data


def parse_m3u8_streams(data, live, secure_token_url):
    """
    Parse the retrieved m3u8 stream list into a list of dictionaries
    then return the url for the highest quality stream. Different
    handling is required of live m3u8 files as they seem to only contain
    the destination filename and not the domain/path.
    """
    qual = int(addon.getSetting('LIVEQUALITY'))
    if qual == config.MAX_LIVEQUAL:
        qual = -1
    # fix for values too high from previous API config
    if qual > config.MAX_LIVEQUAL:
        addon.setSetting('LIVEQUALITY', str(config.MAX_LIVEQUAL))
        qual = -1

    m3u_list = []
    base_url = secure_token_url[:secure_token_url.rfind('/') + 1]
    base_domain = secure_token_url[:secure_token_url.find('/', 8) + 1]
    m3u8_lines = iter(data)
    for line in m3u8_lines:
            stream_inf = '#EXT-X-STREAM-INF:'
            if line.startswith(stream_inf):
                line = line[len(stream_inf):]
            else:
                continue

            csv_list = re.split(',(?=(?:(?:[^"]*"){2})*[^"]*$)', line)
            linelist = [i.split('=') for i in csv_list]

            uri = next(m3u8_lines)

            if uri.startswith('/'):
                linelist.append(['URL', base_domain + uri])
            elif uri.find('://') == -1:
                linelist.append(['URL', base_url + uri])
            else:
                linelist.append(['URL', uri])
            m3u_list.append(dict((i[0], i[1]) for i in linelist))
    sorted_m3u_list = sorted(m3u_list, key=lambda k: int(k['BANDWIDTH']))
    try:
        stream = sorted_m3u_list[qual]['URL']
    except IndexError as e:
        utils.log('Quality setting: {0}'.format(qual))
        utils.log('Sorted m3u8 list: {0}'.format(sorted_m3u_list))
        raise e
    return stream


def get_m3u8_playlist(video_id, pcode, live):
    """
    Main function to call other functions that will return us our m3u8 HLS
    playlist as a string, which we can then write to a file for Kodi
    to use
    """
    if pcode == '':
        pcode = config.PCODE
    login_ticket = get_user_ticket()
    embed_token = get_embed_token(login_ticket, video_id)
    authorize_url = config.AUTH_URL.format(pcode,
                                           video_id,
                                           urllib.quote_plus(embed_token))
    secure_token_url = get_secure_token(authorize_url, video_id)
    return secure_token_url
