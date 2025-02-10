#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 351 $
#     Date: $Date: 2021-06-03 18:49:17 -0500 (Sat, 16 Feb 2019) $


from SQLparsing import *
from common import *
from library import *
from login import *

if __name__ == '__main__':

        publisher_id = SESSION.Parameter(0, 'int')
        publisher_name = SQLgetPublisherName(publisher_id)
        if not publisher_name:
                SESSION.DisplayError('Specified Publisher Does Not Exist')

        author_id = SESSION.Parameter(1, 'int')
        author_data = SQLloadAuthorData(author_id)
        if not author_data:
                SESSION.DisplayError('Specified Author Does Not Exist')
        author_name = author_data[AUTHOR_CANONICAL]

        PrintHeader('Publications for Author %s Published by %s' % (author_name, publisher_name))
        PrintNavbar('publisher_one_author', publisher_id, publisher_id, 'publisher_one_author.cgi', 0)

        print ISFDBLinkNoName('publisher.cgi', publisher_id, 'Return to the publisher page')
        print ' %s ' % SESSION.ui.bullet
        print ISFDBLink('publisher_authors.cgi', '%d+name' % publisher_id, 'Return to the Authors for Publisher %s page' % publisher_name)
        print """<p>The statistics below count the number of publications for the
                specified author. They do not include individual titles (stories, poems, etc.)
                contained in publications. Each edition of a book increments the count.
                Only the currently selected form of the author's name is counted, e.g.
                'Mary Shelley' does not include books published as by 'Mary W. Shelley'."""

        pubs = SQLGetPubsForAuthorPublisher(publisher_id, author_id)
        decades = {}
        years = {}
        for pub in pubs:
                pub_date = pub[PUB_YEAR]
                year = int(pub_date[:4])
                decade = year/10
                years[year] = years.get(year, 0) + 1
                decades[decade] = decades.get(decade, 0) + 1

        table = ISFDBTable()
        table.display_count = 0
        table.headers = ['Decade', 'Years']
        table.headers_colspan = [1, 13]
        table.table_css = 'seriesgrid'
        for decade in sorted(decades):
                if decade == 888:
                        row = ['unpublished (%d)' % decades[decade]]
                        for x in range(0,10):
                                row.append('-')
                elif decade:
                        row = ['%ds (%d)' % (decade * 10, decades[decade])]
                        for year in range(decade * 10, decade * 10 + 10):
                                if year in years:
                                        cell_display = '%d (%d)' % (year, years[year])
                                else:
                                        cell_display = '-'
                                row.append(cell_display)
                else:
                        row = ['unknown (%d)' % decades[decade]]
                        for x in range(0,10):
                                row.append('-')
                table.rows.append(row)
        table.PrintTable()
        print '<p>'
        PrintPubsTable(pubs, 'publisher')

        PrintTrailer('publisher_one_author', publisher_id, publisher_id)
