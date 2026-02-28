#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2019-2026   Ahasuerus, Al von Ruff
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

if __name__ == '__main__':

        # Retrieve Amazon cover scans with extraneous formatting
        query = "select pub_id, pub_frontimage from pubs where pub_frontimage like 'http://%amazon.com/images/P/%.01.LZZZZZZZ.jpg'"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        pubs = {}
        while record:
                pub_id = record[0][0]
                image = record[0][1]
                pubs[pub_id] = '%s.jpg' % image.split('.01.LZZZZZZZ.jpg')[0]
                record = CNX.DB_FETCHMANY()
        print(CNX.DB_NUMROWS())

        for pub_id in pubs:
                image = pubs[pub_id]
                update = "update pubs set pub_frontimage = '%s' where pub_id = %d" % (CNX.DB_ESCAPE_STRING(pubs[pub_id]), pub_id)
                print(update)
                if debug == 0:
                        CNX.DB_QUERY(update)
