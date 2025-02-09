#!_PYTHONLOC
#
#     (C) COPYRIGHT 2022   Ahasuerus
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
    query = """select webpage_id, url from webpages where url like 'http://sf-encyclopedia.uk/fe.php?nm=%'"""

    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    while record:
        webpage_id = record[0][0]
        url = record[0][1]
        new_url = 'https://sf-encyclopedia.com/fe/%s' % url.split('fe.php?nm=')[1]
        update = """update webpages set url = '%s' where webpage_id = %d""" % (db.escape_string(new_url), webpage_id)
        db.query(update)
        record = result.fetch_row()
