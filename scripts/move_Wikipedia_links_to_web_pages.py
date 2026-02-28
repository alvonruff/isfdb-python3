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
#         Date: $Date: 2014/01/17 05:27:28 $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

def one_type(field, table = ''):
        if table == '':
                table = field
        query = "select %s_id,%s_wikipedia from %s where %s_wikipedia is not null" % (field, field, table, field)

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        with_wikipedia = CNX.DB_FETCHONE()
        if with_wikipedia == None:
                sys.exit(0)

        for pair in with_wikipedia:
                id = pair[0]
                url = pair[1]
                update = "insert into webpages (%s_id, url) values('%s', '%s')" % (field, id, CNX.DB_ESCAPE_STRING(url))
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)

        update = "update %s set %s_wikipedia = NULL" % (table, field)
        if debug == 0:
                CNX.DB_QUERY(update)
        else:
                print(update)
        print(table, "done")
        

if __name__ == '__main__':

        one_type('author', 'authors')

        one_type('award_type', 'award_types')

        one_type('publisher', 'publishers')

        one_type('pub_series')

        one_type('title', 'titles')
