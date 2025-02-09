#!_PYTHONLOC
#
#     (C) COPYRIGHT 2017   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2017/06/30 19:51:14 $


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
             where p.note_id = n.note_id and n.note_note regexp 
             '^(<br>)*OCLC: \<a href=\"http:\/\/www.worldcat.org\/oclc\/[[:digit:]]{1,11}"\>[[:digit:]]{1,11}\<\/a>$'"""
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    num = result.num_rows()
    count = 0
    while record:
        pub_id = int(record[0][0])
        note_id = int(record[0][1])
        note_note = record[0][2]
        record = result.fetch_row()
        count += 1
        two_numbers = note_note.lower().split('/oclc/')[1].split('</a>')[0]
        number_list = two_numbers.split('">')
        if number_list[0] != number_list[1]:
            print pub_id, number_list
            continue
        oclc_id = number_list[0]
        print oclc_id
        insert = """insert into identifiers (identifier_type_id, identifier_value, pub_id)
                     values(12, '%s', %d)""" % (db.escape_string(oclc_id), pub_id)
        db.query(insert)
        delete = "delete from notes where note_id=%d" % note_id
        db.query(delete)
        update = "update pubs set note_id=NULL where pub_id=%d" % pub_id
        db.query(update)
        
##        update = "update notes set note_note='%s' where note_id=%d" % (db.escape_string(new_note), int(note_id))
##        db.query(update)
