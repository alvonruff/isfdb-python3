#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2017-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1003 $
#     Date: $Date: 2022-09-15 14:36:33 -0400 (Thu, 15 Sep 2022) $


from isfdb import *
from common import *
from SQLparsing import *


if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)

        PrintHeader('Recent Primary Verifications')
        PrintNavbar('recent', 0, 0, 'recent_primary_ver.cgi', 0)

        # First select 200 verification IDs -- needs to be done as a separate query since the SQL optimizer
        # in MySQL 5.0 is not always smart enough to use all available indices for multi-table queries
        query = "select * from primary_verifications order by ver_time desc limit %d,200" % start

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() == 0:
                print('<h3>No primary verifications present</h3>')
                PrintTrailer('recent', 0, 0)
                sys.exit(0)
        ver = CNX.DB_FETCHMANY()
        ver_set = []
        while ver:
                ver_set.append(ver[0])
                ver = CNX.DB_FETCHMANY()

        print('<table cellpadding=3 class="generic_table">')
        print('<tr class="generic_table_header">')
        print('<th>Publication Title</th>')
        print('<th>User</th>')
        print('<th>Time</th>')
        print('<th>Transient</th>')
        print('</tr>')

        color = 0
        for ver in ver_set:
                pub_id = ver[PRIM_VERIF_PUB_ID]
                query = """select mu.user_name, p.pub_title
                           from mw_user mu, pubs p
                           where mu.user_id=%d
                           and p.pub_id=%d""" % (ver[PRIM_VERIF_USER_ID], pub_id)
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                color = color ^ 1
                while record:
                        user_name = record[0][0]
                        pub_title = record[0][1]
                        if color:
                                print('<tr align=left class="table1">')
                        else:
                                print('<tr align=left class="table2">')
                        print('<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title))
                        print('<td>%s</td>' % WikiLink(user_name))
                        print('<td>%s</td>' % ver[PRIM_VERIF_TIME])
                        if ver[PRIM_VERIF_TRANSIENT]:
                                print('<td>Yes</td>')
                        else:
                                print('<td>&nbsp;</td>')
                        print('</tr>')
                        record = CNX.DB_FETCHMANY()

        print('</table>')
        print('<p> %s' % ISFDBLinkNoName('recent_primary_ver.cgi', start+200, 'MORE', True))

        PrintTrailer('recent', 0, 0)

