#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2013-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1.1 $
#         Date: $Date: 2013/06/03 06:31:14 $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        # Find all duplicate rows in the title_relationships table
        query_main = "select * from title_relationships group by title_id,review_id having count(*)>1 order by review_id;"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query_main)
        row = CNX.DB_FETCHONE()

        try:
                print(len(row))
        except:
            print("Total duplicate title_relationship entries processed : 0")
            sys.exit(0)

        count = 0
        for record in row:
                print(record)
                count += 1
                # Remove ALL rows for this title/review combination
                delete = "delete from title_relationships where title_id=%d and review_id=%d;" % (int(record[1]), int(record[2]))
                print(delete)
                if debug == 0:
                        CNX.DB_QUERY(delete)
                # Insert a new record for this title/review combination into the table
                insert = "insert into title_relationships (title_id, review_id) values(%d,%d);" % (int(record[1]), int(record[2]))
                print(insert)
                if debug == 0:
                        CNX.DB_QUERY(insert)
        print("Total duplicate title_relationship entries processed : %d" % (count))
