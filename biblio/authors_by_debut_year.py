#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2011-2025   Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 638 $
#     Date: $Date: 2021-06-16 17:19:39 -0400 (Wed, 16 Jun 2021) $


from common import *

if __name__ == '__main__':

        header = 'Authors By Debut Year'
        year = SESSION.Parameter(0, 'int', 0)
        if year > 1899:
                header += ' - %d' % year
        else:
                header += ' - Prior to 1900'
                year = 0

        PrintHeader(header)
        PrintNavbar('authors_by_debut_year', 0, 0, 'authors_by_debut_year.cgi', 0)

        print('<h3>Includes authors with at least 6 novels, short fiction, poems or collections:</h3>')
        print('<table class="generic_table">')
        print('<tr align=left class="table1">')
        print('<th>Debut Year</th>')
        print('<th>Author</th>')
        print('<th>Number of Titles</th>')
        print('</tr>')

        CNX = MYSQL_CONNECTOR()
        if year:
                year_selector = '= %d' % year
        else:
                year_selector = '< 1900'
        query = """select ad.debut_year, ad.author_id, a.author_canonical, ad.title_count
                from authors_by_debut_date ad, authors a
                where ad.debut_year %s
                and ad.author_id = a.author_id
                order by debut_year, a.author_lastname, a.author_canonical""" % CNX.DB_ESCAPE_STRING(year_selector)
        CNX.DB_QUERY(query)
        SQLlog("authors_by_debut_year::query: %s" % query)
        record = CNX.DB_FETCHMANY()
        color = 0
        while record:
                debut_year = record[0][0]
                author_id = record[0][1]
                author_name = record[0][2]
                title_count = record[0][3]
                if color:
                        print('<tr align=left class="table1">')
                else:
                        print('<tr align=left class="table2">')
                print('<td>%s</td>' % debut_year)
                print('<td>%s</td>' % ISFDBLink('ea.cgi', author_id, author_name))
                print('<td>%d</td>' % title_count)
                print('</tr>')
                color = color ^ 1
                record = CNX.DB_FETCHMANY()
        print('</table><p>')

        PrintTrailer('frontpage', 0, 0)
