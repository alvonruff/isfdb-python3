#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2014/06/09 02:26:28 $


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

    # Retrieve all award categories for each award type IDs
    query = "select distinct award_type_id, award_atype from awards order by award_type_id"
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    pairs = []
    while record:
        pairs.append(record[0])
        record = result.fetch_row()

    for pair in pairs:
        award_cat_type_id = int(pair[0])
        award_cat_name = pair[1]
        insert = "insert into award_cats (award_cat_name, award_cat_type_id) values('%s',%d)" % (db.escape_string(award_cat_name), award_cat_type_id)
        db.query(insert)
        award_cat_id = int(db.insert_id())
        update = "update awards set award_cat_id=%d where award_type_id=%d and award_atype='%s'" % (award_cat_id, award_cat_type_id, db.escape_string(award_cat_name))
        db.query(update)

    query = "update awards set award_atype=NULL"
    db.query(query)
