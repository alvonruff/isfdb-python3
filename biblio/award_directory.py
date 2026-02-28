#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


import sys
import os
import string
from SQLparsing import *
from common import *


if __name__ == '__main__':

        PrintHeader('Award Directory')
        PrintNavbar('directory', 0, 0, 'award_directory.cgi', 0)

        print('For the current status of the award data entry project see the <a href="%s://%s/index.php/Awards">Wiki Awards page</a>' % (PROTOCOL, WIKILOC))
        print('<p>')
        results = SQLSearchAwards('')
        PrintAwardResults(results, 10000)

        print('<p>')

        PrintTrailer('directory', 0, 0)
