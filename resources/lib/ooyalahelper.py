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

# This module contains functions for interacting with the Ooyala API

import urllib
import urllib2
import requests
import cookielib
import ssl

import StringIO
import time
import os
from urlparse import parse_qsl
import xml.etree.ElementTree as ET
import json
import base64

import config
import utils
import xbmcaddon
import xbmc
import telstra_auth
from exception import NRLException

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.poolmanager import PoolManager

# Ignore InsecureRequestWarning warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()
session.verify = False

addon = xbmcaddon.Addon()
username = addon.getSetting('LIVE_USERNAME')
password = addon.getSetting('LIVE_PASSWORD')


def get_nrl_user_token():
    """send user login info and retrieve user id for session"""
    stored_token = addon.getSetting('TOKEN')
    if stored_token != '':
        return stored_token
    
    free_sub = int(addon.getSetting('SUBSCRIPTION_TYPE'))
    
    if free_sub:
        token = telstra_auth.get_free_token(username, password)
        addon.setSetting('TOKEN', token)
        return token
    
    login_resp = telstra_auth.get_paid_token(username, password)
    json_data = json.loads(login_resp)
    if 'ErrorCode' in json_data:
        if json_data.get('ErrorCode') == 'MIS_EMPTY':
            raise Exception('No paid subscription found on this Telstra ID')
        if json_data.get('ErrorCode') == '5':
            raise Exception('Please check your username '
                            'and password in the settings')
        raise Exception(json_data.get('ErrorMessage'))
    token = json_data.get('UserToken')
    addon.setSetting('TOKEN', token)
    utils.log('Using token: {0}******'.format(token[:-6]))
    return token
    

def create_nrl_userid_xml(user_id):
    """ create a small xml file to send with http POST 
        when starting a new video request"""
    root = ET.Element('Subscription')
    ut = ET.SubElement(root, 'UserToken')
    ut.text = user_id
    fakefile = StringIO.StringIO()
    tree = ET.ElementTree(root)
    tree.write(fakefile, encoding='UTF-8')
    output = fakefile.getvalue()
    return output

def fetch_nrl_smil(video_id):
    """ contact ooyala server and retrieve smil data to be decoded"""
    url = config.SMIL_URL.format(video_id)
    utils.log("Fetching URL: {0}".format(url))
    res = session.get(url)
    return res.text

def get_nrl_hds_url(encryptedSmil):
    """ decrypt smil data and return HDS url from the xml data"""
    from ooyala import ooyalaCrypto
    decrypt = ooyalaCrypto.ooyalaCrypto()
    smil_xml = decrypt.ooyalaDecrypt(encryptedSmil)
    tree = ET.fromstring(smil_xml)
    return tree.find('content').find('video').find('httpDynamicStreamUrl').text


def get_nrl_embed_token(userToken, videoId):
    """send our user token to get our embed token, including api key"""
    data = create_nrl_userid_xml(userToken)
    url = config.EMBED_TOKEN_URL.format(videoId)
    utils.log("Fetching URL: {0}".format(url))
    try:
        req = session.post(url, data=data, headers=config.YINZCAM_AUTH_HEADERS, verify=False)
        xml = req.text[1:]
        try:
            tree = ET.fromstring(xml)
        except ET.ParseError as e:
            utils.log('Embed token response is: {0}'.format(xml))
            raise e
        if tree.find('ErrorCode') is not None:
            utils.log('Errorcode found: {0}'.format(xml))
            raise NRLException()
        token = tree.find('Token').text
    except NRLException:
        addon.setSetting('TOKEN', '')
        raise Exception('Login token has expired, please try again')
    return token

#common ooyala functions
 
def get_secure_token(secure_url, videoId):
    """send our embed token back with a few other url encoded parameters"""
    res = session.get(secure_url)
    data = res.text
    try:
        parsed_json = json.loads(data)
        token =  parsed_json['authorization_data'][videoId]['streams'][0]['url']['data']
    except KeyError as e:
        utils.log('Parsed json data: {0}'.format(parsed_json))
        raise e
    return base64.b64decode(token)

def get_m3u8_streams(secure_token_url):
    """ fetch our m3u8 file which contains streams of various qualities"""
    res = session.get(secure_token_url)
    data = res.text.splitlines()
    return data
   
def parse_m3u8_streams(data, live, secure_token_url):
    """ Parse the retrieved m3u8 stream list into a list of dictionaries
        then return the url for the highest quality stream. Different 
        handling is required of live m3u8 files as they seem to only contain
        the destination filename and not the domain/path."""
    if live:
        qual = int(addon.getSetting('LIVEQUALITY'))
        if qual >= 5:
            addon.setSetting('LIVEQUALITY', '4')
            qual = 4
    else:
        qual = int(addon.getSetting('HLSQUALITY'))
        if qual >= 5:
            addon.setSetting('HLSQUALITY', '4')
            qual = 4

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
            linelist.append(['URL',data[count+1]])
        else:
            linelist.append(['URL',prepend_live+data[count+1]])
        
        m3u_list.append(dict((i[0], i[1]) for i in linelist))
        count += 2
    
    sorted_m3u_list = sorted(m3u_list, key=lambda k: int(k['BANDWIDTH']))
    stream = sorted_m3u_list[qual]['URL']
    return stream
   
def get_m3u8_playlist(video_id, live):
    """ Main function to call other functions that will return us our m3u8 HLS
        playlist as a string, which we can then write to a file for Kodi
        to use"""
    login_token = get_nrl_user_token()
    embed_token = get_nrl_embed_token(login_token, video_id)
    authorize_url = config.AUTH_URL.format(config.PCODE, video_id, embed_token)
    secure_token_url = get_secure_token(authorize_url, video_id)

    if 'chunklist.m3u8' in secure_token_url:
        return secure_token_url

    m3u8_data = get_m3u8_streams(secure_token_url)
    m3u8_playlist_url = parse_m3u8_streams(m3u8_data, live, secure_token_url)
    return m3u8_playlist_url