#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1264 $
#         Date: $Date: 2026-02-21 11:58:41 -0500 (Sat, 21 Feb 2026) $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

def convertEllipses(title):
        # First convert ". . . ." to "...."
        while ". . . ." in title:
                title = title.replace(". . . .", "....")
        # Then convert ". . ." to "..."
        while ". . ." in title:
                title = title.replace(". . .", "...")
        print(title)
        return title

if __name__ == '__main__':

        # Retrieve all titles with ". . ."
        query = "select title_id, title_title from titles where title_title like '%. . .%'"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        titles = []
        while record:
                titles.append(record[0])
                record = CNX.DB_FETCHMANY()

        for title in titles:
                title_id = int(title[0])
                title_title = title[1]
                new_title = convertEllipses(title_title)
                update = "update titles set title_title='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(new_title), title_id)
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)

        # Retrieve all publication records with ". . ."
        query = "select pub_id, pub_title from pubs where pub_title like '%. . .%'"
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        titles = []
        while record:
                titles.append(record[0])
                record = CNX.DB_FETCHMANY()

        for title in titles:
                title_id = int(title[0])
                title_title = title[1]
                new_title = convertEllipses(title_title)
                update = "update pubs set pub_title='%s' where pub_id=%d" % (CNX.DB_ESCAPE_STRING(new_title), title_id)
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)

