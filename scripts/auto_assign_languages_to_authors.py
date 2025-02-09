#!_PYTHONLOC
#
#     (C) COPYRIGHT 2017   Ahasuerus
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

    query = """select a2.author_id, a1.author_language
                from authors a1, authors a2, pseudonyms p
                where a1.author_id = p.author_id
                and p.pseudonym = a2.author_id
                and a2.author_language is null
                and a1.author_language is not null
            """
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    num = result.num_rows()
    count = 0
    while record:
            author_id = record[0][0]
            language = record[0][1]
            count += 1
            print count, author_id, language
            update = "update authors set author_language=%d where author_id=%d" % (int(language), int(author_id))
            db.query(update)
            record = result.fetch_row()
