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


class NRLException(Exception):
    """ A Not Fatal Exception is used for certain conditions where we do not
        want to give users an option to send an error report
    """
    pass


class TelstraAuthException(Exception):
    """ A Not Fatal Exception is used for certain conditions where we do not
        want to give users an option to send an error report
    """
    pass
