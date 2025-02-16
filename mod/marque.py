#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 920 $
#     Date: $Date: 2022-05-25 19:40:18 -0400 (Wed, 25 May 2022) $


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
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        total_authors = record[0][0]
        maxauthors = total_authors / 50

        update = 'update authors set author_marque = 0'
        db.query(update)

        authors = []
        for author in SESSION.special_authors_to_ignore:
                authors.append(db.escape_string(author))
        authors_to_ignore = list_to_in_clause(authors)
        query = """select author_id, author_views, author_canonical
                from authors
                where author_views > 0
                and author_canonical NOT IN (%s)
                order by author_views
                desc limit %d""" % (authors_to_ignore, maxauthors)
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        print('<ol>')

        while record:
                print('<li>%d - %s' % (record[0][1], record[0][2]))
                update = 'update authors set author_marque=1 where author_id=%d' % int(record[0][0])
                db.query(update)
                record = result.fetch_row()

        print('</ol>')
        PrintPostMod(0)
