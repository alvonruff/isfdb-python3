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
#         Date: $Date: 2014/01/16 05:09:33 $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        query = "select author_id,author_imdb from authors where author_imdb!=''"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        with_imdb = CNX.DB_FETCHONE()
        if with_imdb == None:
                sys.exit(0)

        for pair in with_imdb:
                author_id = pair[0]
                url = pair[1]
                update = "insert into webpages (author_id, url) values('%s', '%s')" % (author_id, CNX.DB_ESCAPE_STRING(url))
                print(update)
                if debug == 0:
                        CNX.DB_QUERY(update)

        update = "update authors set author_imdb = NULL"
        if debug == 0:
                CNX.DB_QUERY(update)
        else:
                print(update)
        
