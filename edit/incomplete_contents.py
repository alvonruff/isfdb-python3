#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 419 $
#     Date: $Date: 2019-05-15 10:54:53 -0400 (Wed, 15 May 2019) $


from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *


def PrintTableColumns(columns, user):
        print '<table class="generic_table">'
        print '<tr class="table2">'
        for column in columns:
                if not column:
                        data = '&nbsp;'
                else:
                        data = column
                print '<td><b>%s</b></td>' % data
         print '</tr>'

if __name__ == '__main__':

        report_type = SESSION.Parameter(0, 'str', None, ('decade', 'year', 'month', 'unknown'))
        date_range = SESSION.Parameter (1, 'int')
        if report_type == 'decade':
                if len(str(date_range)) != 3:
                        SESSION.DisplayError('Decade Must be a 3-Digit Number')
                display_range = '%s0s' % date_range
        elif report_type == 'year':
                if len(str(date_range)) != 4:
                        SESSION.DisplayError('Year Must be a 4-Digit Number')
                display_range = date_range
        elif report_type == 'month':
                if len(str(date_range)) != 6:
                        SESSION.DisplayError('Month Must Be a YYYYMM value')
                display_range = '%s-%s' % (str(date_range)[:4], str(date_range)[4:6])
        elif report_type == 'unknown':
                display_range = '0000-00'
        report_id = SESSION.Parameter(2, 'int', None, (277, ))

        PrintPreSearch('Publications with Incomplete Contents')
        PrintNavBar('edit/incomplete_contents.cgi', 0)

        print '<h3>Date range: %s</h3>' % display_range
        query = """select c.cleanup_id, p.*
                from pubs p, notes n, cleanup c
                where p.note_id = n.note_id
                and n.note_note like '%%{{Incomplete}}%%'
                and c.record_id = p.pub_id
                and c.report_type = 277
                and c.record_id_2 like '%d%%'
                """ % date_range
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print 'No eligible publications for the specified date range'
                PrintPostSearch(0, 0, 0, 0, 0, 0)
                sys.exit(0)

        user = User()
        user.load()
        user.load_moderator_flag()

        PrintTableColumns(('', 'Title', 'Authors', 'Pub. Date', 'Type', '1st Edition', 'Publisher', 'Note',), user)
        record = result.fetch_row()
        count = 1
        bgcolor = 1
        while record:
                cleanup_id = record[0][0]
                pub_data = record[0][1:]
                pub_id = pub_data[PUB_PUBID]
                pub_title = pub_data[PUB_TITLE]
                pub_date = pub_data[PUB_YEAR]
                pub_type = pub_data[PUB_CTYPE]
                publisher_id = pub_data[PUB_PUBLISHER]
                note_id = pub_data[PUB_NOTE]
                note_note = SQLgetNotes(note_id)
                authors = SQLPubBriefAuthorRecords(pub_id)
                publisher = SQLGetPublisher(publisher_id)
                referral_id = SQLgetTitleReferral(pub_id, pub_data[PUB_CTYPE])
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'
                print '<td>%d</td>' % count
                print '<td>%s</td>' % ISFDBLink("pl.cgi", pub_id, pub_title)
                print '<td>%s</td>' % LIBbuildRecordList('author', authors)
                print '<td>%s</td>' % pub_date
                print '<td>%s</td>' % pub_type[:4]

                referral_column = 0
                if referral_id:
                        referral_title = SQLloadTitle(referral_id)
                        if referral_title[TITLE_YEAR] != pub_date:
                                print '<td>%s</td>' % referral_title[TITLE_YEAR]
                                referral_column = 1
                if not referral_column:
                        print '<td>&nbsp;</td>'

                if publisher:
                        print '<td>%s</td>' % ISFDBLink('publisher.cgi', publisher_id, publisher[PUBLISHER_NAME])
                else:
                        print '<td>&nbsp;</td>'
                print '<td>%s</td>' % FormatNote(note_note)
                print '</tr>'
                count += 1
                bgcolor ^= 1
                record = result.fetch_row()
        
        PrintPostSearch(0, 0, 0, 0, 0)
