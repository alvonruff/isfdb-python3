#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2013-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 901 $
#     Date: $Date: 2022-04-04 15:24:03 -0400 (Mon, 04 Apr 2022) $


from SQLparsing import *
from biblio import *
from common import PrintAllAuthors
from library import ISFDBconvertYear


if __name__ == '__main__':

        query = 'select title_id, year, reviews from most_reviewed'
        display_year = ''
        decade = ''
        report_type = SESSION.Parameter(0, 'str', None, ('all', 'decade', 'year', 'pre1900'))
        if report_type == 'all':
                header = 'Most-Reviewed Titles of All Time'
        elif report_type == 'decade':
                decade = SESSION.Parameter(1, 'int')
                query += ' where decade=%d' % decade
                header = 'Most-Reviewed Titles of the %ss' % decade
        elif report_type == 'year':
                display_year = SESSION.Parameter(1, 'int')
                query += ' where year=%d' % display_year
                header = 'Most-Reviewed Titles of %s' % display_year
        elif report_type == 'pre1900':
                query += ' where decade="pre1900"'
                header = 'Most-Reviewed Titles Prior to 1900'
        query += ' order by reviews desc limit 500'

        PrintHeader('Most-Reviewed Titles Details')
        PrintNavbar('top', 0, 0, 'most_reviewed.cgi', 0)

        print('<h3>%s</h3>' % header)

        print('<h3>This report is generated once a day</h3>')

        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print('<h3>This report is currently unavailable. It will be regenerated overnight.</h3>')
        else:
                # Print the table headers        
                print('<table class="seriesgrid">')
                print('<tr>')
                print('<th>Count</th>')
                print('<th>Reviews</th>')
                if report_type != 'year':
                        print('<th>Year</th>')
                print('<th>Title</th>')
                print('<th>Type</th>')
                print('<th>Authors</th>')
                print('</tr>')
                record = result.fetch_row()
                bgcolor = 0
                count = 1
                while record:
                        title_id = record[0][0]
                        year = record[0][1]
                        reviews = record[0][2]
                        print('<tr align=left class="table%d">' % (bgcolor+1))
                        print('<td>%d</td>' % count)
                        print('<td>%d</td>' % reviews)
                        # Display the year of the title unless we are displaying the data for just one year
                        if report_type != 'year':
                                display_year = unicode(year)
                                if display_year == '0':
                                        display_year = '0000'
                                print('<td>%s</td>' % ISFDBconvertYear(display_year))
                        # Retrieve this record's title and type
                        title_data = SQLloadTitle(title_id)
                        print('<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_data[TITLE_TITLE]))
                        print('<td>%s</td>' % title_data[TITLE_TTYPE])
                        print('<td>')
                        PrintAllAuthors(title_id)
                        print('</td>')
                        print('</tr>')
                        record = result.fetch_row()
                        bgcolor = bgcolor ^ 1
                        count += 1
                print('</table>')
        
        PrintTrailer('top', 0, 0)

