#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2016-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1264 $
#     Date: $Date: 2026-02-21 11:58:41 -0500 (Sat, 21 Feb 2026) $


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

    query = "select title_id from titles where title_language is null"

    CNX = MYSQL_CONNECTOR()
    CNX.DB_QUERY(query)
    record = CNX.DB_FETCHMANY()
    num = CNX.DB_NUMROWS()
    count = 0
    update_count = 0
    while record:
            title_id = record[0][0]
            count += 1
            print("Processed ",count)
            query2 = """select distinct t.title_language
                        from titles t, pub_content pc1, pub_content pc2
                        where pc1.title_id = %d
                        and pc1.pub_id = pc2.pub_id
                        and pc1.title_id != pc2.title_id
                        and pc2.title_id = t.title_id
                        and t.title_language is not null
                        and t.title_language !=''""" % (int(title_id))
            CNX2 = MYSQL_CONNECTOR()
            CNX2.DB_QUERY(query2)
            record2 = CNX2.DB_FETCHMANY()
            num2 = CNX2.DB_NUMROWS()
            if num2 == 1:
                language = record2[0][0]
                update_count += 1
                update = "update titles set title_language=%d where title_id=%d" % (int(language), int(title_id))
                if debug == 0:
                        CNX2.DB_QUERY(update)
                else:
                        print(update)
            record = CNX.DB_FETCHMANY()

    print("Count of updated titles: ",update_count)
