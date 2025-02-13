#!_PYTHONLOC
#
#     (C) COPYRIGHT 2024-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $
 
import MySQLdb
from localdefs import *
import sys

def Date_or_None(s):
    return s

def IsfdbConvSetup():
    import MySQLdb.converters
    IsfdbConv = MySQLdb.converters.conversions
    IsfdbConv[10] = Date_or_None
    return(IsfdbConv)

if __name__ == "__main__":

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    domains = {}
    query = """select pub_id, pub_frontimage from pubs where pub_frontimage like '%amazon%/images/W/MEDIAX%/images/I/%'"""

    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    count = 0
    while record:
        pub_id = record[0][0]
        pub_frontimage = record[0][1]
        new_url_list = pub_frontimage.split('/images/W/MEDIAX')
        first_segment = new_url_list[0]
        second_segment = new_url_list[1].split('/images/')[1]
        new_url = first_segment + '/images/' + second_segment
        print new_url
        update = """update pubs set pub_frontimage = '%s' where pub_id = %d""" % (db.escape_string(new_url), pub_id)
        db.query(update)
        record = result.fetch_row()
        count += 1
    print count
