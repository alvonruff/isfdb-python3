#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
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

def convertEllipses(title):
    # First convert ". . . ." to "...."
    while ". . . ." in title:
        title = title.replace(". . . .", "....")
    # Then convert ". . ." to "..."
    while ". . ." in title:
        title = title.replace(". . .", "...")
    print title
    return title

if __name__ == '__main__':

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    # Retrieve all titles with ". . ."
    query = "select title_id, title_title from titles where title_title like '%. . .%'"
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    titles = []
    while record:
        titles.append(record[0])
        record = result.fetch_row()

    for title in titles:
        title_id = int(title[0])
        title_title = title[1]
        new_title = convertEllipses(title_title)
        update = "update titles set title_title='%s' where title_id=%d" % (db.escape_string(new_title), title_id)
        db.query(update)

    # Retrieve all publication records with ". . ."
    query = "select pub_id, pub_title from pubs where pub_title like '%. . .%'"
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    titles = []
    while record:
        titles.append(record[0])
        record = result.fetch_row()

    for title in titles:
        title_id = int(title[0])
        title_title = title[1]
        new_title = convertEllipses(title_title)
        update = "update pubs set pub_title='%s' where pub_id=%d" % (db.escape_string(new_title), title_id)
        db.query(update)

