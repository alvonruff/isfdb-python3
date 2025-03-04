#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 713 $
#     Date: $Date: 2021-08-27 10:38:44 -0400 (Fri, 27 Aug 2021) $

from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from library import *

def PrintTableHeaders():
        print('<table class="generic_table">')
        print('<tr class="generic_table_header">')
        for column in ('#', 'Publication', 'Suspect URL', 'Click Once Resolved'):
                print('<th>%s</th>' % column)
        print('</tr>')

def PrintPubRecord(count, pub_id, url, pub_title, bgcolor):
        if bgcolor:
                print('<tr align=left class="table1">')
        else:
                print('<tr align=left class="table2">')

        print('<td>%d</td>' % (count))
        print('<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title))
        print('<td>%s</td>' % (url))
        print('<td>%s</td>' % ISFDBLink('mod/resolve_bad_url.cgi', pub_id, 'Click Once Resolved'))
        print('</tr>')

if __name__ == '__main__':

        PrintPreMod('Publications with Suspect Images')
        PrintNavBar()

        query = """select bad_images.pub_id, bad_images.image_url, pubs.pub_title
                from bad_images, pubs
                where pubs.pub_id=bad_images.pub_id
                order by pubs.pub_title"""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        num = CNX.DB_NUMROWS()

        if num:
                PrintTableHeaders()
                record = CNX.DB_FETCHMANY()
                bgcolor = 1
                count = 1
                while record:
                        pub_id = record[0][0]
                        url = record[0][1]
                        pub_title = record[0][2]
                        PrintPubRecord(count, pub_id, url, pub_title, bgcolor)
                        record = CNX.DB_FETCHMANY()
                        bgcolor ^= 1
                        count += 1

                print('</table>')
        else:
                print('<h2>No publications with bad images found</h2>')

        PrintPostMod(0)
