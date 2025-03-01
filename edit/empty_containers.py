#!_PYTHONLOC
#
#     (C) COPYRIGHT 2018-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 731 $
#     Date: $Date: 2021-09-02 15:40:49 -0400 (Thu, 02 Sep 2021) $


from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *


def PrintTableColumns(columns, user):
        print('<table class="generic_table">')
        print('<tr class="table2">')
        for column in columns:
                if not column:
                        data = '&nbsp;'
                else:
                        data = column
                # Skip 'Ignore' and 'Resolve' columns if the user is not a moderator
                if ('Ignore' in column or 'Resolve' in column) and not user.moderator:
                        continue
                print("<td><b>%s</b></td>" % data)
        print('</tr>')

if __name__ == '__main__':

        report_type = SESSION.Parameter(0, 'str', None, ('decade', 'year', 'month', 'unknown'))
        date_range = SESSION.Parameter(1, 'int')
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
        report_id = SESSION.Parameter(2, 'int', None, (240, 241, 277))

        if report_id == 240:
                container_names = 'Anthologies and Collections'
        else:
                container_names = 'Magazines'
        PrintPreSearch("%s with no Fiction Titles" % container_names)
        PrintNavBar('edit/empty_container_table.cgi', 0)

        print('<h3>Date range: %s</h3>' % display_range)
        query = """select c.cleanup_id, p.*
                from pubs p, cleanup c
                where c.resolved IS NULL
                and c.report_type = %d
                and c.record_id_2 like '%d%%'
                and c.record_id = p.pub_id
                and p.pub_year != '8888-00-00'
                and NOT EXISTS
                        (select 1 from pub_content pc, titles t
                        where p.pub_id=pc.pub_id 
                        and pc.title_id=t.title_id
                        and t.title_ttype in ('NOVEL', 'SHORTFICTION', 'POEM', 'SERIAL')
                        )
                order by pub_title""" % (report_id, date_range)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if not CNX.DB_NUMROWS():
                print('No eligible publications for the specified date range.')
                print(ISFDBLink('edit/cleanup_report.cgi', report_id, 'Return to the main report'))
                sys.exit(0)

        user = User()
        user.load()
        user.load_moderator_flag()

        if report_id == 240:
                PrintTableColumns(('', 'Title', 'Authors', 'Pub. Date', 'Type', '1st Edition', 'Publisher', 'Note', 'Ignore'), user)
        else:
                PrintTableColumns(('', 'Title', 'Editors', 'Pub. Date', 'Publisher', 'Note', 'Ignore'), user)
        record = CNX.DB_FETCHMANY()
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
                        print('<tr align=left class="table1">')
                else:
                        print('<tr align=left class="table2">')
                print('<td>%d</td>' % count)
                print('<td>%s</td>' % ISFDBLink("pl.cgi", pub_id, pub_title))
                print('<td>%s</td>' % LIBbuildRecordList('author', authors))
                print('<td>%s</td>' % pub_date)
                if report_id == 240:
                        print('<td>%s</td>' % pub_type[:4])

                        referral_column = 0
                        if referral_id:
                                referral_title = SQLloadTitle(referral_id)
                                if referral_title[TITLE_YEAR] != pub_date:
                                        print('<td>%s</td>' % referral_title[TITLE_YEAR])
                                        referral_column = 1
                        if not referral_column:
                                print('<td>&nbsp;</td>')

                if publisher:
                        print('<td>%s</td>' % ISFDBLink('publisher.cgi', publisher_id, publisher[PUBLISHER_NAME]))
                else:
                        print('<td>&nbsp;</td>')
                print('<td>%s</td>' % FormatNote(note_note))
                if user.moderator:
                        print('<td>%s</td>' % ISFDBLink('mod/resolve_empty_containers.cgi', '%d+%s+%d+%d' % (cleanup_id, report_type, date_range, report_id), 'Ignore'))
                print('</tr>')
                count += 1
                bgcolor ^= 1
                record = CNX.DB_FETCHMANY()
        
        PrintPostSearch(0, 0, 0, 0, 0)
