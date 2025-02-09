#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2014/04/23 01:51:12 $


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

    # Open the flat file with missing author URLs and read in its content
    fd = open('MissingSFE3')
    lines = fd.readlines()
    fd.close();
    for line in lines:
        oneline = line.strip()
        onelist = oneline.split(',')
        url = onelist[0]
        author_id = onelist[1]
        print url, author_id
        if author_id:
            update = "insert into missing_author_urls (url_type, url, author_id, resolved) values('%d', '%s', '%d', '%d')" % (1, db.escape_string(url), int(author_id), 0)
        else:
            update = "insert into missing_author_urls (url_type, url, resolved) values('%d', '%s', '%d')" % (1, db.escape_string(url), 0)
        print update
        db.query(update)
    sys.exit(0)
