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
#     Date: $Date: 2014/01/17 05:27:28 $


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

def one_type(field, table = ''):
    if table == '':
        table = field
    query = "select %s_id,%s_wikipedia from %s where %s_wikipedia is not null" % (field, field, table, field)
    db.query(query)
    result_main = db.store_result()
    with_wikipedia = result_main.fetch_row(0)
    for pair in with_wikipedia:
        id = pair[0]
        url = pair[1]
        update = "insert into webpages (%s_id, url) values('%s', '%s')" % (field, id, db.escape_string(url))
        db.query(update)

    update = "update %s set %s_wikipedia = NULL" % (table, field)
    db.query(update)
    print(table, "done")
    

if __name__ == '__main__':

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    one_type('author', 'authors')
    one_type('award_type', 'award_types')
    one_type('publisher', 'publishers')
    one_type('pub_series')
    one_type('title', 'titles')
