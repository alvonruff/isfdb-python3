#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2016-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1.1 $
#         Date: $Date: 2016/06/28 22:56:54 $


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

        # Delete all records for report type 96 from the cleanup table
        delete = "delete from cleanup where report_type=96"

        CNX = MYSQL_CONNECTOR()
        if debug == 0:
                CNX.DB_QUERY(delete)
        else:
                print(delete)
        
        # Retrieve all COVERART titles with a "Cover: " prefix
        query = """select title_id, title_title from titles
                           where title_ttype = 'COVERART'
                           and title_title like 'Cover: %'"""
        CNX.DB_QUERY(query)

        if not CNX.DB_NUMROWS():
                print("No COVERART titles with a 'Cover: ' prefix on file.")
                sys.exit(0)

        record = CNX.DB_FETCHMANY()
        while record:
                title_id = record[0][0]
                old_title = record[0][1]
                new_title = old_title[7:]
                print(old_title)
                print(new_title)
                update = "update titles set title_title = '%s' where title_id = %d" % (CNX.DB_ESCAPE_STRING(new_title), title_id)
                print(update)
                print(" ")
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
                record = CNX.DB_FETCHMANY()
        print('Updated %d titles' % int(CNX.DB_NUMROWS()))
