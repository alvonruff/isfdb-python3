#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2020-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 477 $
#     Date: $Date: 2019-12-01 20:16:10 -0500 (Sun, 01 Dec 2019) $


import string
import sys
from isfdb import *
from common import *
from login import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        PrintHeader('My Verifications')
        PrintNavbar('my_verifications_menu', 0, 0, 'my_verifications_menu.cgi', 0)

        (userid, username, usertoken) = GetUserData()

        print('<ul>')
        print('<li>%s' % ISFDBLink('userver.cgi', '', 'My Primary Verifications'))
        print('<li>%s' % ISFDBLink('changed_verified_pubs.cgi', '', 'My Changed Primary Verifications'))
        if SQLChangedVerifications(userid):
                print(' <span class="inverted">New!</span>')
        print('<li>%s' % ISFDBLink('my_unstable_ISBN_verifications.cgi', '', 'My Primary Verifications with Unstable ISBN-based Amazon URLs'))
        print('<li>%s' % ISFDBLink('my_unstable_verifications.cgi', '', 'My Primary Verifications with Possibly Unstable "/G/" Amazon URLs'))
        print('<li>%s' % ISFDBLink('my_secondary_verifications.cgi', '', 'My Secondary Verifications'))
        print('<li>%s' % ISFDBLink('my_removed_secondary_verifications.cgi', '', 'My Removed Secondary Verifications'))
        print('</ul>')

        PrintTrailer('my_verifications_menu', 0, 0)

