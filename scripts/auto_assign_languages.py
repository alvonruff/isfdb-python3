#!_PYTHONLOC
#
#     (C) COPYRIGHT 2016   Ahasuerus
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

    query = "select title_id from titles where title_language is null"
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    num = result.num_rows()
    count = 0
    update_count = 0
    while record:
            title_id = record[0][0]
            count += 1
            print "Processed ",count
            query2 = """select distinct t.title_language
                        from titles t, pub_content pc1, pub_content pc2
                        where pc1.title_id = %d
                        and pc1.pub_id = pc2.pub_id
                        and pc1.title_id != pc2.title_id
                        and pc2.title_id = t.title_id
                        and t.title_language is not null
                        and t.title_language !=''""" % (int(title_id))
            db.query(query2)
            result2 = db.store_result()
            record2 = result2.fetch_row()
            num2 = result2.num_rows()
            if num2 == 1:
                language = record2[0][0]
                update_count += 1
                update = "update titles set title_language=%d where title_id=%d" % (int(language), int(title_id))
                db.query(update)
            record = result.fetch_row()

    print "Count of updated titles: ",update_count
