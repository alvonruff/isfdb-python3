#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2017-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1 $
#     Date: $Date: 2017/12/12 05:27:28 $


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

    query = "select pub_id, pub_isbn from pubs where pub_isbn like '#%'"
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    count = 0
    while record:
        count += 1
        pub_id = record[0][0]
        # Strip the leading # sign from the catalog ID
        catalog_id = record[0][1][1:]
        print(count, catalog_id, pub_id)
        update = "update pubs set pub_catalog='%s', pub_isbn=NULL where pub_id=%d" % (db.escape_string(catalog_id), pub_id)
        db.query(update)
        record = result.fetch_row()
