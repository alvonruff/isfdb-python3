#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2017-2026   Ahasuerus, Al von Ruff
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
from SQLparsing import *

debug = 0

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

    query = """select p.pub_id, n.note_id, n.note_note from notes n, pubs p
             where p.note_id = n.note_id and n.note_note like '<br>_ {{ASIN|__________}}.\n%'"""

    CNX = MYSQL_CONNECTOR()
    CNX.DB_QUERY(query)
    record = CNX.DB_FETCHMANY()
    num = CNX.DB_NUMROWS()
    count = 0
    while record:
            pub_id = record[0][0]
            note_id = record[0][1]
            note_note = record[0][2]
            count += 1
            asin = note_note[13:23]
            new_note = note_note[27:]
            print(count, asin, pub_id, new_note[:20])
            record = CNX.DB_FETCHMANY()
            insert = """insert into identifiers (identifier_type_id, identifier_value, pub_id)
                     values(1, '%s', %d)""" % (CNX.DB_ESCAPE_STRING(asin), int(pub_id))
            if debug == 0:
                CNX.DB_QUERY(insert)
            else:
                print(insert)
            update = "update notes set note_note='%s' where note_id=%d" % (CNX.DB_ESCAPE_STRING(new_note), int(note_id))
            if debug == 0:
                CNX.DB_QUERY(update)
            else:
                print(update)
