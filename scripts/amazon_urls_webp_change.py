#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $
 
import MySQLdb
from localdefs import *

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
    query = """select pub_id, pub_frontimage from pubs where pub_frontimage like '%amazon\.%\/W\/WEBP_402378-T%'"""

    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    count = 0
    while record:
        pub_id = record[0][0]
        pub_frontimage = record[0][1]
        url_segments = pub_frontimage.split('https://')[1]

        new_url_list = url_segments.split('/images/W/WEBP_402378-T1/')
        new_url = '/'.join(new_url_list)
        new_url_list = new_url.split('/images/W/WEBP_402378-T2/')
        new_url = 'https://%s'% '/'.join(new_url_list)

        update = """update pubs set pub_frontimage = '%s' where pub_id = %d""" % (db.escape_string(new_url), pub_id)
        db.query(update)
        record = result.fetch_row()
        count += 1
    print count
