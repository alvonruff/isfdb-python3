#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1.1 $
#         Date: $Date: 2014/01/22 03:17:48 $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

def one_table(table, id, title):
        # Replace adjacent spaces with a single space in a given table
        query = "select %s, %s from %s where %s like '%%  %%'" % (id, title, table, title)

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        row = CNX.DB_FETCHONE()
        count = 0
        for record in row:
                count += 1
                old_title = record[1]
                new_title = " ".join(old_title.split())
                title_id = int(record[0])
                update = "update %s set %s='%s' where %s=%d" % (table, title, CNX.DB_ESCAPE_STRING(new_title), id, title_id)
                print(update)
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
        print("Total %s processed: %d" % (table, count))
        return

if __name__ == '__main__':

        one_table('titles', 'title_id', 'title_title')
        one_table('pubs', 'pub_id', 'pub_title')
