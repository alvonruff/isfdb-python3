#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2014/09/10 20:20:28 $


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

    # First delete all old images that are associated with pubs that no longer exist
    delete = " delete from bad_images where not exists (select 1 from pubs where bad_images.pub_id=pubs.pub_id)"
    db.query(delete)
    
    # Open the flat file with bad image URLs and read in its content
    fd = open('BadImages')
    lines = fd.readlines()
    fd.close();
    for line in lines:
        oneline = line.strip()
        onelist = oneline.split(',')
        pubid = onelist[0]
        url = onelist[1]
        print(pubid, url)
        update = "insert into bad_images (pub_id, image_url) values(%d,'%s')" % (int(pubid), db.escape_string(url))
        print(update)
        db.query(update)
    sys.exit(0)
