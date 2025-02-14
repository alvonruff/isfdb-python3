#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus, Al von Ruff
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
import operator


if __name__ == '__main__':

        display_year = 0
        decade = 0
        title_types = (('Titles', ''),
                       ('Novels', 'NOVEL'),
                       ('Short Fiction', 'SHORTFICTION'),
                       ('Collections', 'COLLECTION'),
                       ('Anthologies', 'ANTHOLOGY'),
                       ('Non-Fiction', 'NONFICTION'),
                       ('Other Title Types', ''))
        type_id = SESSION.Parameter(0, 'int', None, (0, 1, 2, 3, 4, 5, 6))
        type_tuple = title_types[type_id]
        displayed_type = type_tuple[0]
        title_type = type_tuple[1]

        span = SESSION.Parameter(1, 'str', None, ('all', 'decade', 'year', 'pre1950'))
        if span == 'all':
                header = 'Highest Ranked %s of All Time' % displayed_type
        elif span == 'decade':
                decade = SESSION.Parameter(2, 'int')
                header = 'Highest Ranked %s of the %ds' % (displayed_type, decade)
        elif span == 'year':
                display_year = SESSION.Parameter(2, 'int')
                header = 'Highest Ranked %s published in %s' % (displayed_type, display_year)
        elif span == 'pre1950':
                header = 'Highest Ranked %s Prior to 1950' % displayed_type

        PrintHeader(header)
        PrintNavbar('top', 0, 0, 'most_popular.cgi', 0)

        print('<h3>This report is generated once a day</h3>')

        query = """select title_id, score, year, title_type from award_titles_report where 1 """
        if span == 'year':
                query += ' and year=%d' % display_year
        elif span == 'decade':
                query += ' and decade=%d' % decade
        elif span == 'pre1950':
                query += ' and decade="pre1950"'
        if title_type:
                query += ' and title_type = "%s"' % title_type
        elif displayed_type == 'Other Title Types':
                query += ' and title_type not in ("NOVEL", "SHORTFICTION", "COLLECTION", "ANTHOLOGY", "NONFICTION")'
        query += ' order by score desc, year desc limit 500'

        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print('<h3>No awards or nominations for the specified period</h3>')
                PrintTrailer('top', 0, 0)
                sys.exit(0)

        print("""<b>Note</b>: Some recent awards are yet to be integrated into the database.<br>
                <b>Scoring</b>: Wins are worth 50 points, nominations and second places are worth
                35 points. For polls, third and lower places are worth (33-poll position) points.""")
        # Print the table headers        
        print('<table class="seriesgrid">')
        print('<tr>')
        print('<th>Place</th>')
        print('<th>Score</th>')
        if span != 'year':
                print('<th>Year</th>')
        print('<th>Title</th>')
        print('<th>Type</th>')
        print('<th>Authors</th>')
        print('</tr>')
        record = result.fetch_row()
        bgcolor = 0
        place = 0
        while record:
                title_id = record[0][0]
                score = record[0][1]
                year = record[0][2]
                title_type = record[0][3]
                title_title = SQLgetTitle(title_id)
                print('<tr align=left class="table%d">' % (bgcolor + 1))
                print('<td>%d</td>' % (place + 1))
                print('<td>%d</td>' % score)
                # Display the year of the title unless we are displaying the data for just one year
                if span != 'year':
                        display_year = unicode(year)
                        if display_year == '0':
                                display_year = '0000'
                        print('<td>%s</td>' % ISFDBconvertYear(display_year))
                print('<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title))
                print('<td>%s</td>' % title_type)
                print('<td>')
                PrintAllAuthors(title_id)
                print('</td>')
                print('</tr>')
                record = result.fetch_row()
                place += 1
                bgcolor = bgcolor ^ 1
        print('</table>')
        
        PrintTrailer('top', 0, 0)

