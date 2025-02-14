#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2007-2025   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 715 $
#     Date: $Date: 2021-08-27 18:27:37 -0400 (Fri, 27 Aug 2021) $


from SQLparsing import *
from common import *
from library import *


if __name__ == '__main__':

        user_id = SESSION.Parameter(0, 'int')
        user_name = SQLgetUserName(user_id)
        if user_name == 'UNKNOWN':
                SESSION.DisplayError('Unknown User')

        PrintHeader("%s's Tags" % user_name)
        PrintNavbar('usertag', 0, 0, 'usertag.cgi', user_id)

        query = """select distinct tag_mapping.tag_id,count(tag_mapping.tag_id) as xx,
                tags.tag_name, tags.tag_status
                from tag_mapping,tags
                where tag_mapping.user_id=%d
                and tags.tag_id=tag_mapping.tag_id
                group by tag_mapping.tag_id
                order by xx desc""" % user_id
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        first = 1
        bgcolor = 1
        while record:
                if first:
                        print('<table class="generic_table">')
                        print('<tr class="generic_table_header">')
                        print('<th>Tag Name</th>')
                        print('<th>Count</th>')
                        print('<th>Private?</th>')
                        print('</tr>')
                        first = 0
                if bgcolor:
                        print('<tr align=left class="table1">')
                else:
                        print('<tr align=left class="table2">')
                print('<td>%s</td>' % ISFDBLink('tag.cgi', record[0][0], record[0][2]))
                print('<td>%s</td>' % ISFDBLink('usertitles.cgi', '%d+%d' % (user_id, record[0][0]), record[0][1]))
                print('<td>')
                if record[0][3]:
                        print('<b>Private</b>')
                else:
                        print('&nbsp;')
                print('</td>')
                print('</tr>')
                bgcolor ^= 1
                record = result.fetch_row()

        print('</table>')
        print('<p><p>')

        PrintTrailer('usertag', user_id, user_id)
