#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2017-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1 $
#         Date: $Date: 2017/12/12 05:27:28 $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        query = "select pub_id, pub_isbn from pubs where pub_isbn like '#%'"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        count = 0
        while record:
                count += 1
                pub_id = record[0][0]
                # Strip the leading # sign from the catalog ID
                catalog_id = record[0][1][1:]
                print(count, catalog_id, pub_id)
                update = "update pubs set pub_catalog='%s', pub_isbn=NULL where pub_id=%d" % (CNX.DB_ESCAPE_STRING(catalog_id), pub_id)
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
                record = CNX.DB_FETCHMANY()
