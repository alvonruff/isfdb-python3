#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


import cgi
import sys
import os
import string
import MySQLdb
from localdefs import *

def Date_or_None(s):
    return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)


if __name__ == '__main__':

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    # Find all duplicate tags
    query = "select tag_id,title_id,user_id,count(*) as xx from tag_mapping group by tag_id,title_id,user_id having xx > 1"
    db.query(query)
    result = db.store_result()
    tag_count = result.num_rows()
    record = result.fetch_row()
    tags = []
    while record:
            tags.append(record[0])
            record = result.fetch_row()
    row_count = 0
    for tag in tags:
            tag_id = tag[0]
            title_id = tag[1]
            user_id = tag[2]
            row_count += int(tag[3])
            update = "delete from tag_mapping where tag_id=%d and title_id=%d and user_id=%d" % (int(tag_id), int(title_id), int(user_id))
            db.query(update)
            update = "insert into tag_mapping(tag_id, title_id, user_id) values(%d, %d, %d)" % (int(tag_id), int(title_id), int(user_id))
            db.query(update)
    print("Total processed: %d rows in %d tags" % (row_count, tag_count))
