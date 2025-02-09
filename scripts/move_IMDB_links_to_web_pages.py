#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2014/01/16 05:09:33 $


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

    query = "select author_id,author_imdb from authors where author_imdb!=''"
    db.query(query)
    result_main = db.store_result()
    with_imdb = result_main.fetch_row(0)
    for pair in with_imdb:
        author_id = pair[0]
        url = pair[1]
        update = "insert into webpages (author_id, url) values('%s', '%s')" % (author_id, db.escape_string(url))
        print update
        db.query(update)

    update = "update authors set author_imdb = NULL"
    db.query(update)
    
