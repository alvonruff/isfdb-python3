#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2020-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


from SQLparsing import *
from library import *

debug = 0

if __name__ == '__main__':

        update = "update submissions set sub_holdid = 0 where sub_state in ('I','R')"
        if debug == 0:
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(update)
        else:
                print(update)
