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
import re
import traceback
import time
import datetime
import unicodedata
import urllib
import textwrap
import xbmc
import xbmcgui
import config
import issue_reporter
from exception import NRLException
from telstra_auth import TelstraAuthException

pattern = re.compile("&(\w+?);")

# This is a throwaway variable to deal with a python bug with strptime:
#   ImportError: Failed to import _strptime because the import lockis
#   held by another thread.
throwaway = time.strptime('20140101', '%Y%m%d')


def get_airtime(timestamp):
    delta = (time.mktime(time.localtime()) - time.mktime(time.gmtime())) / 3600
    if time.daylight:
        delta += 1
    ts = datetime.datetime.fromtimestamp(time.mktime(
                                         time.strptime(timestamp[:-1],
                                                       "%Y-%m-%dT%H:%M:%S")))
    ts += datetime.timedelta(hours=delta)
    return ts.strftime("%A @ %I:%M %p").replace(' 0', ' ')


def make_url(d):
    pairs = []
    for k, v in d.iteritems():
        k = urllib.quote_plus(k)
        v = ensure_ascii(v)
        v = urllib.quote_plus(v)
        pairs.append("%s=%s" % (k, v))
    return "&".join(pairs)


def ensure_ascii(s):
    if isinstance(s, unicode):
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    else:
        return s


def log(s):
    xbmc.log("[%s v%s] %s" % (config.NAME, config.VERSION, s),
             level=xbmc.LOGNOTICE)


def get_round_no():
    """ calculate what the current NRL round is"""
    date = datetime.date.today()
    r1 = datetime.date(2017, 3, 2)
    dateDelta = datetime.date.toordinal(date) - datetime.date.toordinal(r1)
    if datetime.date.toordinal(date) >= 736453:  # 2 weeks between rd 9 and 10
        return (dateDelta // 7)
    else:
        return (dateDelta // 7) + 1


def dialog_error(err=None):
    # Generate a list of lines for use in XBMC dialog
    content = []
    exc_type, exc_value, exc_tb = sys.exc_info()
    content.append("%s v%s Error" % (config.NAME, config.VERSION))
    content.append(str(exc_value))
    return content


def dialog_message(msg, title=None):
    if not title:
        title = "%s v%s" % (config.NAME, config.VERSION)
    # Add title to the first pos of the textwrap list
    content = textwrap.wrap(msg, 60)
    content.insert(0, title)
    return content


def get_platform():
    """ Work through a list of possible platform types and return the first
        match. Ordering of items is important as some match more thant one
        type.

        E.g. Android will match both Android and Linux
    """
    platforms = [
        "Android",
        "Linux.RaspberryPi",
        "Linux",
        "XBOX",
        "Windows",
        "ATV2",
        "IOS",
        "OSX",
        "Darwin",
    ]

    for platform in platforms:
        if xbmc.getCondVisibility('System.Platform.'+platform):
            return platform
    return "Unknown"


def get_xbmc_build():
    return xbmc.getInfoLabel("System.BuildVersion")


def get_xbmc_version():
    build = get_xbmc_build()
    # Keep the version number, and strip the rest
    version = build.split(' ')[0]
    return version


def get_xbmc_major_version():
    """ Return the major version number of the running XBMC
    """
    version = get_xbmc_version().split('.')[0]
    return int(version)


def log_xbmc_platform_version():
    """ Log our XBMC version and platform for debugging
    """
    version = get_xbmc_version()
    platform = get_platform()
    log("XBMC/Kodi %s running on %s" % (version, platform))


def get_file_dir():
    """ Make our addon working directory if it doesn't exist and
        return it.
    """
    filedir = os.path.join(xbmc.translatePath('special://temp/'),
                           config.ADDON_ID)
    if not os.path.isdir(filedir):
        os.mkdir(filedir)
    return filedir


def save_last_error_report(trace):
    """ Save a copy of our last error report
    """
    try:
        rfile = os.path.join(get_file_dir(), 'last_report_error.txt')
        with open(rfile, 'w') as f:
            f.write(trace)
    except:
        log("Error writing error report file")


def can_send_error(trace):
    """ Check to see if our new error message is different from the last
        successful error report. If it is, or the file doesn't exist, then
        we'll return True
    """
    try:
        rfile = os.path.join(get_file_dir(), 'last_report_error.txt')

        if not os.path.isfile(rfile):
            return True
        else:
            f = open(rfile, 'r')
            report = f.read()
            if report != trace:
                return True
    except:
        log("Error checking error report file")

    log("Not allowing error report. Last report matches this one")
    return False


def handle_error(msg, exc=None):
    traceback_str = traceback.format_exc()
    log(traceback_str)
    report_issue = False

    # Don't show any dialogs when user cancels
    if traceback_str.find('SystemExit') > 0:
        return

    d = xbmcgui.Dialog()
    if d:
        message = dialog_error(msg)

        # Work out if we should allow an error report
        send_error = can_send_error(traceback_str)

        # Some transient network errors we don't want any reports about
        if ((traceback_str.find('The read operation timed out') > 0) or
                (traceback_str.find('IncompleteRead') > 0) or
                (traceback_str.find('HTTP Error 404: Not Found') > 0)):
            send_error = False

        # Any non-fatal errors, don't allow issue reporting
        if (isinstance(exc, NRLException) or
                isinstance(exc, TelstraAuthException)):
            send_error = False

        if send_error:
            latest_version = issue_reporter.get_latest_version()
            version_string = '.'.join([str(i) for i in latest_version])
            if not issue_reporter.is_latest_version(config.VERSION,
                                                    latest_version):
                message.append("Your version of this add-on is outdated. "
                               "Please try upgrading to the latest version: "
                               "v%s" % version_string)
                d.ok(*message)
                return

            # Only report if we haven't done one already
            try:
                message.append("Would you like to automatically "
                               "report this error?")
                report_issue = d.yesno(*message)
            except:
                message.append("If this error continues to occur, "
                               "please report it to our issue tracker.")
                d.ok(*message)
        else:
            # Just show the message
            d.ok(*message)

    if report_issue:
        log("Reporting issue to GitHub...")
        issue_url = issue_reporter.report_issue(traceback_str)
        if issue_url:
            # Split the url here to make sure it fits in our dialog
            split_url = issue_url.replace('/xbmc', ' /xbmc')
            d.ok("%s v%s Error" % (config.NAME, config.VERSION),
                 "Thanks! Your issue has been reported to: %s" % split_url)
            # Touch our file to prevent more than one error report
            save_last_error_report(traceback_str)
