#!_PYTHONLOC
#
#     (C) COPYRIGHT 2016-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 654 $
#     Date: $Date: 2021-06-19 22:44:19 -0400 (Sat, 19 Jun 2021) $


from SQLparsing import *
from isfdb import *
from library import *
from isfdblib import *


if __name__ == '__main__':

        publisher_id = SESSION.Parameter(0, 'int')
        publisher = SQLGetPublisher(publisher_id)
        if not publisher:
                SESSION.DisplayError('Record Does Not Exist')

        PrintPreSearch('Non-Latin Titles for Publisher: %s' % publisher[PUBLISHER_NAME])
        PrintNavBar('edit/publisher_exceptions.cgi', publisher_id)

        query = "select pub_id, pub_title from pubs where publisher_id = %d" % publisher_id
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        pubs_list = []
        while record:
                pub_id = record[0][0]
                pub_title = record[0][1]
                pubs_list.append(pub_id)
                record = result.fetch_row()

        in_clause = list_to_in_clause(pubs_list)

        query = """select distinct t.title_id, pc.pub_id
                from pub_content pc, titles t, languages l
                where pc.pub_id in (%s)
                and pc.title_id = t.title_id
                and t.title_language = l.lang_id
                and l.latin_script = 'No'
                order by t.title_title""" % in_clause
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        titles = {}
        while record:
                title_id = record[0][0]
                pub_id = record[0][1]
                if title_id not in titles:
                        titles[title_id] = []
                titles[title_id].append(pub_id)
                record = result.fetch_row()

        if not titles:
                print('<h2>No exceptions found</h2>')
        else:
                print('<table class="generic_table">')
                print('<tr class="generic_table_header">')
                print('<th>Title</th>')
                print('<th>Title Type</th>')
                print('<th>Title Language</th>')
                print('<th>Publication(s)</th>')
                for title_id in titles:
                        title = SQLloadTitle(title_id)
                        print('<tr>')
                        print('<td>%s</td>' % ISFDBLink('title.cgi', title_id, title[TITLE_TITLE]))
                        print('<td>%s</td>' % title[TITLE_TTYPE])
                        if title[TITLE_LANGUAGE]:
                                print('<td>%s</td>' % LANGUAGES[int(title[TITLE_LANGUAGE])])
                        else:
                                print('<td>&nbsp;</td>')
                        print('<td>')
                        pubs = titles[title_id]
                        for pub_id in pubs:
                                pub = SQLGetPubById(pub_id)
                                print(ISFDBLink('pl.cgi', pub_id, pub[PUB_TITLE]))
                                print('<br>')
                        print('</td>')
                        print('</tr>')
                print('</table>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)
