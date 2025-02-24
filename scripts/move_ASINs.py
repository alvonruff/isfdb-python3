#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2017-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2017/05/28 02:28:03 $


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

    query = """select p.pub_id, n.note_id, n.note_note from notes n, pubs p
             where p.note_id = n.note_id and n.note_note like '<br>_ {{ASIN|__________}}.\n%'"""
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    num = result.num_rows()
    count = 0
    while record:
        pub_id = record[0][0]
        note_id = record[0][1]
        note_note = record[0][2]
        count += 1
        asin = note_note[13:23]
        new_note = note_note[27:]
        print(count, asin, pub_id, new_note[:20])
        record = result.fetch_row()
        insert = """insert into identifiers (identifier_type_id, identifier_value, pub_id)
                     values(1, '%s', %d)""" % (db.escape_string(asin), int(pub_id))
        db.query(insert)
        update = "update notes set note_note='%s' where note_id=%d" % (db.escape_string(new_note), int(note_id))
        db.query(update)
