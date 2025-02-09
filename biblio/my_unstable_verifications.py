#!_PYTHONLOC
#
#     (C) COPYRIGHT 2022  Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 714 $
#     Date: $Date: 2021-08-27 16:56:23 -0400 (Fri, 27 Aug 2021) $

from SQLparsing import *
from common import *
from library import *
from login import *
from myverificationsClass import MyVerifications


if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)

	PrintHeader('My Primary Verifications with Possibly Unstable "/G/" Amazon URLs')
	PrintNavbar('my_unstable_verifications', 0, 0, 'my_unstable_verifications.cgi', 0)

        print """<h3>Amazon URLs which start with "/images/G/" are not guaranteed to
                remain the same over time, although it doesn't seem to happen very often</h3>"""

        my_verifications = MyVerifications()
        my_verifications.display()

	PrintTrailer('my_unstable_verifications', 0, 0)

