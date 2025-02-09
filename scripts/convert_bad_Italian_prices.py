#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus
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
    query = """select pub_id, pub_price from pubs where pub_price like '% Lit'"""
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    while record:
        pub_id = record[0][0]
        pub_price = record[0][1]
        numeric_price = pub_price.split(' Lit')[0]
        new_price = 'Lit %s' % numeric_price
        print 'ID: ', pub_id
        print 'Old: ', numeric_price
        print 'New: ', new_price
        update = "update pubs set pub_price = '%s' where pub_id = %d" % (db.escape_string(new_price), int(pub_id))
        db.query(update)
        record = result.fetch_row()
    print "Total processed: %d" % int(result.num_rows())

