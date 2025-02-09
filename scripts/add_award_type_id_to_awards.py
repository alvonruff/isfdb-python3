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

if __name__ == '__main__':

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    # Retrieve all award types and create a dictionary of award type IDs by award code
    query = "select award_type_id, award_type_code from award_types"
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    codes = {}
    while record:
        id = record[0][0]
        code = record[0][1]
        codes[code] = id
        record = result.fetch_row()
    print codes

    for code in codes:
        id = codes[code]
        update = "update awards set award_type_id=%d where award_ttype='%s'" % (id, code)
        print update
        db.query(update)
