#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1239 $
#     Date: $Date: 2026-02-06 08:43:24 -0500 (Fri, 06 Feb 2026) $

import sys
from isfdb import *
from isfdblib import *
from SQLparsing import *
from library import *
from sfe3 import Sfe3

if __name__ == '__main__':
        PrintPreSearch('SFE Author Articles without a matching SFE URL in ISFDB Author Records')
        PrintNavBar('edit/sfe3_authors.cgi', 0)

        sfe3 = Sfe3()
        sfe3.display_report()
        PrintPostSearch(0, 0, 0, 0, 0, 0)
