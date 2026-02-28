#!_PYTHONLOC
#
#         (C) COPYRIGHT 2017-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1264 $
#         Date: $Date: 2026-02-21 11:58:41 -0500 (Sat, 21 Feb 2026) $


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

        query = """select a2.author_id, a1.author_language
                                from authors a1, authors a2, pseudonyms p
                                where a1.author_id = p.author_id
                                and p.pseudonym = a2.author_id
                                and a2.author_language is null
                                and a1.author_language is not null
                        """
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        num = CNX.DB_NUMROWS()
        count = 0
        while record:
                        author_id = record[0][0]
                        language = record[0][1]
                        count += 1
                        print count, author_id, language
                        update = "update authors set author_language=%d where author_id=%d" % (int(language), int(author_id))
                        if debug == 0:
                                CNX.DB_QUERY(update)
                        else:
                                print update
                        record = CNX.DB_FETCHMANY()
