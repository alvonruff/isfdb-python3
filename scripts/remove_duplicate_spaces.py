#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2014/01/22 03:17:48 $


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

def one_table(table, id, title):
    # Replace adjacent spaces with a single space in a given table
    query = "select %s, %s from %s where %s like '%%  %%'" % (id, title, table, title)
    db.query(query)
    result_main = db.store_result()
    row = result_main.fetch_row(0)
    count = 0
    for record in row:
        count += 1
        old_title = record[1]
        new_title = " ".join(old_title.split())
        title_id = int(record[0])
        update = "update %s set %s='%s' where %s=%d" % (table, title, db.escape_string(new_title), id, title_id)
        print(update)
        db.query(update)
    print("Total %s processed: %d" % (table, count))
    return

if __name__ == '__main__':

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    one_table('titles', 'title_id', 'title_title')
    one_table('pubs', 'pub_id', 'pub_title')
