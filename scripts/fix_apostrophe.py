#!_PYTHONLOC
# -*- coding: cp1252 -*-
from __future__ import print_function
# All 3 of these lines above want to be first in the file. The coding line is more
# important that the print function, so keep print statements simple in this file.

#
#     (C) COPYRIGHT 2009-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1264 $
#     Date: $Date: 2026-02-21 11:58:41 -0500 (Sat, 21 Feb 2026) $

import sys
if sys.version_info.major == 3:
        PYTHONVER = "python3"
elif sys.version_info.major == 2:
        PYTHONVER = "python2"

import cgi
import os
import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        query_main = "select title_id,title_title from titles where title_title like '%\’%'"
        if PYTHONVER == "python3":
                unicode_bytes = query_main.encode('utf-8')
                query_main = unicode_bytes.decode('latin-1')

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query_main)
        titles = CNX.DB_FETCHONE()
        if titles == None:
                print("No candidates to fix")
                sys.exit(0)

        for title in titles:
                title_id = title[0]
                title_title = title[1]
                new_title = CNX.DB_ESCAPE_STRING(str.replace(title_title,'\x92',"'"))
                #print(new_title)
                update = "update titles set title_title = '%s' where title_id = '%d'" % (new_title,title_id)
                print(update)
                if debug == 0:
                        CNX.DB_QUERY(update)
