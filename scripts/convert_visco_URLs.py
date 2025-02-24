#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2016-2025   Ahasuerus, Al von Ruff
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

def list_to_in_clause(id_list):
        in_clause = ''
        for id_value in id_list:
                id_string = str(id_value)
                if not in_clause:
                        in_clause = "'%s'" % id_string
                else:
                        in_clause += ",'%s'" % id_string
        return in_clause


if __name__ == '__main__':

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    # Retrieve all pub IDs and pub URLs with old Visco URLs
    query = """select pub_id, pub_frontimage from pubs
               where pub_frontimage like 'http://www.sfcovers.net/Magazines/%'"""
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    pubs = []
    while record:
        pubs.append(record[0])
        record = result.fetch_row()
    if not pubs:
        print("No old Visco URLs on file. Exiting.")
        sys.exit(0)
    for pub in pubs:
        pub_id = pub[0]
        old_url = pub[1]
        new_url = str.replace(old_url, 'http://www.sfcovers.net/Magazines/', 'http://www.philsp.com/visco/Magazines/')
        print(old_url)
        print(new_url)
        update = "update pubs set pub_frontimage = '%s' where pub_id = %d" % (new_url, pub_id)
        print(update)
        print(" ")
        db.query(update)
    print('Updated %d pubs' % len(pubs))
