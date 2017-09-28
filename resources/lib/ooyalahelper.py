import base64
import config
import json
import StringIO
import telstra_auth
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
username = addon.getSetting('LIVE_USERNAME')
password = addon.getSetting('LIVE_PASSWORD')


def clear_token():
    """
    Remove stored token from cache storage
    """
    cache.delete('NRLTOKEN')


def get_user_token():
    """
    send user login info and retrieve token for session
    """
    stored_token = cache.get('NRLTOKEN')
    if stored_token != '':
        utils.log('Using token: {0}******'.format(stored_token[:-6]))
        return stored_token

    free_sub = int(addon.getSetting('SUBSCRIPTION_TYPE'))

    if free_sub:
        token = telstra_auth.get_free_token(username, password)
    else:
        login_resp = telstra_auth.get_paid_token(username, password)
        json_data = json.loads(login_resp)
        if 'ErrorCode' in json_data:
            if json_data.get('ErrorCode') == 'MIS_EMPTY':
                raise AussieAddonsException('No paid subscription found '
                                            'on this Telstra ID')
            if json_data.get('ErrorCode') in ['1', '5']:
                raise AussieAddonsException('Please check your username '
                                            'and password in the settings')
            raise Exception(json_data.get('ErrorMessage'))
        token = json_data.get('UserToken')
    cache.set('NRLTOKEN', token)
    utils.log('Using token: {0}******'.format(token[:-6]))
    return token


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


def get_embed_token(userToken, videoId):
    """
    send our user token to get our embed token, including api key
    """
    data = create_nrl_userid_xml(userToken)
    url = config.EMBED_TOKEN_URL.format(videoId)
    try:
        req = sess.post(
            url, data=data, headers=config.YINZCAM_AUTH_HEADERS, verify=False)
        xml = req.text[1:]
        try:
            tree = ET.fromstring(xml)
        except ET.ParseError as e:
            utils.log('Embed token response is: {0}'.format(xml))
            cache.delete('NRLTOKEN')
            raise e
        if tree.find('ErrorCode') is not None:
            utils.log('Errorcode found: {0}'.format(xml))
            raise AussieAddonsException()
        token = tree.find('Token').text
    except AussieAddonsException:
        cache.delete('NRLTOKEN')
        raise Exception('Login token has expired, please try again')
    return token


def get_secure_token(secure_url, videoId):
    """
    send our embed token back with a few other url encoded parameters
    """
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
                raise Exception('Unauthorised location for streaming. '
                                'Detected location is: {0}. '
                                'Please check VPN/smart DNS settings '
                                ' and try again'.format(country))
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
    if live:
        qual = int(addon.getSetting('LIVEQUALITY'))
        if qual == config.MAX_LIVEQUAL:
            qual = -1
        # fix for values too high from previous API config
        if qual > config.MAX_LIVEQUAL:
            addon.setSetting('LIVEQUALITY', str(config.MAX_LIVEQUAL))
            qual = -1
    else:
        qual = int(addon.getSetting('REPLAYQUALITY'))
        if qual == config.MAX_REPLAYQUAL:
            qual = -1
        # fix for values too high from previous API config
        if qual > config.MAX_REPLAYQUAL:
            addon.setSetting('REPLAYQUALITY', str(config.MAX_REPLAYQUAL))
            qual = -1

    if '#EXT-X-VERSION:3' in data:
        data.remove('#EXT-X-VERSION:3')
    count = 1
    m3u_list = []
    prepend_live = secure_token_url[:secure_token_url.find('index-root')]
    while count < len(data):
        line = data[count]
        line = line.strip('#EXT-X-STREAM-INF:')
        line = line.strip('PROGRAM-ID=1,')
        line = line[:line.find('CODECS')]

        if line.endswith(','):
            line = line[:-1]

        line = line.strip()
        line = line.split(',')
        linelist = [i.split('=') for i in line]

        if not live:
            linelist.append(['URL', data[count+1]])
        else:
            linelist.append(['URL', prepend_live+data[count+1]])

        m3u_list.append(dict((i[0], i[1]) for i in linelist))
        count += 2

    sorted_m3u_list = sorted(m3u_list, key=lambda k: int(k['BANDWIDTH']))
    try:
        stream = sorted_m3u_list[qual]['URL']
    except IndexError as e:
        utils.log('Quality setting: {0}'.format(qual))
        utils.log('Sorted m3u8 list: {0}'.format(sorted_m3u_list))
        raise e
    return stream


def get_m3u8_playlist(video_id, live):
    """
    Main function to call other functions that will return us our m3u8 HLS
    playlist as a string, which we can then write to a file for Kodi
    to use
    """
    login_token = get_user_token()
    embed_token = get_embed_token(login_token, video_id)
    authorize_url = config.AUTH_URL.format(config.PCODE, video_id, embed_token)
    secure_token_url = get_secure_token(authorize_url, video_id)

    if 'chunklist.m3u8' in secure_token_url:
        return secure_token_url

    m3u8_data = get_m3u8_streams(secure_token_url)
    m3u8_playlist_url = parse_m3u8_streams(m3u8_data, live, secure_token_url)
    return m3u8_playlist_url
