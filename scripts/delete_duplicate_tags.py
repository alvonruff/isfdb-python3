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

if __name__ == '__main__':

        # Find all duplicate tags
        query = "select tag_id,title_id,user_id,count(*) as xx from tag_mapping group by tag_id,title_id,user_id having xx > 1"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        tag_count = CNX.DB_NUMROWS()
        record = CNX.DB_FETCHMANY()
        tags = []
        while record:
                tags.append(record[0])
                record = CNX.DB_FETCHMANY()
        row_count = 0
        for tag in tags:
                tag_id = tag[0]
                title_id = tag[1]
                user_id = tag[2]
                row_count += int(tag[3])
                update = "delete from tag_mapping where tag_id=%d and title_id=%d and user_id=%d" % (int(tag_id), int(title_id), int(user_id))
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
                update = "insert into tag_mapping(tag_id, title_id, user_id) values(%d, %d, %d)" % (int(tag_id), int(title_id), int(user_id))
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
        print("Total processed: %d rows in %d tags" % (row_count, tag_count))
