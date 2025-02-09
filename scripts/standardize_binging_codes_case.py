#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2014/01/10 04:12:16 $


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

    BINDINGS = ('unknown','hc','tp','pb','ph','digest','dos','ebook','webzine','pulp','bedsheet','tabloid','A4','A5','quarto','octavo','audio CD','audio MP3 CD','audio cassette','audio LP','digital audio player','digital audio download','other')
    for binding in BINDINGS:
        update = "update pubs set pub_ptype='%s' where pub_ptype = '%s'" % (binding, binding)
        print update
        db.query(update)
