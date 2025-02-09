#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 638 $
#     Date: $Date: 2021-06-16 17:19:39 -0400 (Wed, 16 Jun 2021) $


from SQLparsing import *
from biblio import *
from common import PrintAllAuthors
import operator


def printTableBody(author_dict):
	bgcolor = 0
        count = 0
        for author_id in sorted(author_dict, key=author_dict.get, reverse=True):
                score = author_dict[author_id]
                print '<tr align=left class="table%d">' % (bgcolor+1)
                print '<td>%d</td>' % (count+1)
                print '<td>%d</td>' % score
                print '<td>'
                author_data = SQLloadAuthorData(author_id)
                print ISFDBLink('ea.cgi', author_data[AUTHOR_ID], author_data[AUTHOR_CANONICAL])
                print '</td>'
                print '</tr>'
                bgcolor = bgcolor ^ 1
                count += 1
                if count > 499:
                        break


if __name__ == '__main__':

        decade = 0
        title_types = (('Authors and Editors', ''),
                       ('Novel Authors', 'NOVEL'),
                       ('Short Fiction Authors', 'SHORTFICTION'),
                       ('Collection Authors', 'COLLECTION'),
                       ('Anthology Editors', 'ANTHOLOGY'),
                       ('Non-Fiction Authors', 'NONFICTION'),
                       ('Other Title Types Authors', ''))

        type_id = SESSION.Parameter(0, 'int', None, (0, 1, 2, 3, 4, 5, 6))
        type_tuple = title_types[type_id]
        displayed_type = type_tuple[0]
        title_type = type_tuple[1]

        span = SESSION.Parameter(1, 'str', None, ('all', 'decade', 'pre1950'))
        if span == 'all':
                header = 'Highest Ranked %s of All Time' % displayed_type
        elif span == 'decade':
                decade = SESSION.Parameter(2, 'int')
                header = 'Highest Ranked %s of the %ds' % (displayed_type, decade)
        elif span == 'pre1950':
                header = 'Highest Ranked %s Prior to 1950' % displayed_type

	PrintHeader(header)
	PrintNavbar('top', 0, 0, 'popular_authors.cgi', 0)

        query = """select title_id, score from award_titles_report where 1 """
        if span == 'decade':
                query += ' and decade=%d' % decade
        elif span == 'pre1950':
                query += ' and decade="pre1950"'
        if title_type:
                query += ' and title_type = "%s"' % title_type
        elif displayed_type == 'Other Title Types Authors':
                query += ' and title_type not in ("NOVEL", "SHORTFICTION", "COLLECTION", "ANTHOLOGY", "NONFICTION")'

        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h3>No %s with awards or nominations for the specified period</h3>' % displayed_type
                PrintTrailer('top', 0, 0)
                sys.exit(0)

        # Initialize the dictionary which will list scores by title_id
        title_dict = {}
        record = result.fetch_row()
        while record:
                title_id = str(record[0][0])
                title_dict[title_id] = record[0][1]
                record = result.fetch_row()

        # Retrieve the author IDs for the identified titles
        query = "select title_id, author_id from canonical_author where ca_status=1 and title_id in (%s)" % dict_to_in_clause(title_dict)
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()
        author_dict = {}
	while record:
                title_id = str(record[0][0])
                author_id = record[0][1]
                score = title_dict[title_id]
                author_dict[author_id] = author_dict.get(author_id, 0) + score
        	record = result.fetch_row()

        print '<h3>This report is generated once a day</h3>'
        print '<b>Note</b>: Some recent awards are yet to be integrated into the database. Only title-based awards are used for ranking purposes.<br>'
        print '<b>Scoring</b>: Wins are worth 50 points, nominations and second places are worth 35 points. For polls, third and lower places are worth (33-poll position) points.'
        # Print the table headers        
        print '<table class="seriesgrid">'
        print '<tr>'
        print '<th>Place</th>'
        print '<th>Score</th>'
        if type != 4:
                print '<th>Author</th>'
        else:
                print '<th>Editor</th>'
        print '</tr>'
        printTableBody(author_dict)
        print '</table>'
	
	PrintTrailer('top', 0, 0)

