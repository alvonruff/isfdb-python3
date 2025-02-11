#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 783 $
#     Date: $Date: 2021-10-15 13:56:50 -0400 (Fri, 15 Oct 2021) $

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
