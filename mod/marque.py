#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2026   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1260 $
#     Date: $Date: 2026-02-18 08:27:14 -0500 (Wed, 18 Feb 2026) $


import sys
import os
import string
from SQLparsing import *
from isfdblib import *
from library import *


if __name__ == '__main__':

        PrintPreMod('ISFDB - Set Marque Authors')
        PrintNavBar()

        #################################
        # Calculate top 2 percent
        #################################
        query = 'select count(author_id) from authors'
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        total_authors = record[0][0]
        maxauthors = total_authors / 50

        update = 'update authors set author_marque = 0'
        CNX.DB_QUERY(update)

        authors = []
        for author in SESSION.special_authors_to_ignore:
                authors.append(CNX.DB_ESCAPE_STRING(author))
        authors_to_ignore = list_to_in_clause(authors)
        query = """select author_id, author_views, author_canonical
                from authors
                where author_views > 0
                and author_canonical NOT IN (%s)
                order by author_views
                desc limit %d""" % (authors_to_ignore, maxauthors)
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        print('<ol>')

        while record:
                print('<li>%d - %s' % (record[0][1], record[0][2]))
                update = 'update authors set author_marque=1 where author_id=%d' % int(record[0][0])
                CNX2 = MYSQL_CONNECTOR()
                CNX2.DB_QUERY(update)
                record = CNX.DB_FETCHMANY()

        print('</ol>')
        PrintPostMod(0)
