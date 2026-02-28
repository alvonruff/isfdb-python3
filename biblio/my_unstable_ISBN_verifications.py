#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2022-2026  Ahasuerus, Al von Ruff
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

        PrintHeader('My Primary Verifications with Unstable ISBN-based Amazon URLs')
        PrintNavbar('my_unstable_ISBN_verifications', 0, 0, 'my_unstable_ISBN_verifications.cgi', 0)

        print("""<h3>Amazon URLs which start with "/images/P/" are based on an ISBN
                and may no longer reflect the actual cover of the publication</h3>""")

        my_verifications = MyVerifications()
        my_verifications.display()

        PrintTrailer('my_unstable_ISBN_verifications', 0, 0)

