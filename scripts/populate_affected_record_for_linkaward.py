#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus
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
from library import *

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
    query = """select sub_id, sub_data from submissions
        where sub_type=30
        and sub_state='I'
        and affected_record_id is null"""
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    while record:
        sub_id = record[0][0]
        sub_data = record[0][1]
        doc = minidom.parseString(XMLunescape2(sub_data))
        merge = doc.getElementsByTagName('LinkAward')
        record_id = GetElementValue(merge, 'Award')
        print(sub_id, record_id)
        update = "update submissions set affected_record_id = %d where sub_id = %d" % (int(record_id), int(sub_id))
        db.query(update)
        record = result.fetch_row()
    print("Total processed: %d" % int(result.num_rows()))

