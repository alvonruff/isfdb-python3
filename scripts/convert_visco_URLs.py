#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2016-2026   Ahasuerus, Al von Ruff
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

def list_to_in_clause(id_list):
        in_clause = ''
        for id_value in id_list:
                id_string = str(id_value)
                if not in_clause:
                        in_clause = "'%s'" % id_string
                else:
                        in_clause += ",'%s'" % id_string
        return in_clause


if __name__ == '__main__':

        # Retrieve all pub IDs and pub URLs with old Visco URLs
        query = """select pub_id, pub_frontimage from pubs
                   where pub_frontimage like 'http://www.sfcovers.net/Magazines/%'"""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        pubs = []
        while record:
                pubs.append(record[0])
                record = CNX.DB_FETCHMANY()

        if not pubs:
                print("No old Visco URLs on file. Exiting.")
                sys.exit(0)
        for pub in pubs:
                pub_id = pub[0]
                old_url = pub[1]
                new_url = str.replace(old_url, 'http://www.sfcovers.net/Magazines/', 'http://www.philsp.com/visco/Magazines/')
                print(old_url)
                print(new_url)
                update = "update pubs set pub_frontimage = '%s' where pub_id = %d" % (new_url, pub_id)
                print(update)
                print(" ")
                if debug == 0:
                        CNX.DB_QUERY(update)
        print('Updated %d pubs' % len(pubs))
