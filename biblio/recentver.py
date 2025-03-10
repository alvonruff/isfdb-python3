#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1003 $
#     Date: $Date: 2022-09-15 14:36:33 -0400 (Thu, 15 Sep 2022) $


import sys
from isfdb import *
from common import *
from login import *
from SQLparsing import *


if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)

        PrintHeader('Recently Added Secondary Verifications')
        PrintNavbar('recentver', 0, 0, 'recentver.cgi', 0)

        per_page = 200
        # First select 200 verification IDs -- needs to be done as a separate query since the SQL optimizer
        # in MySQL 5.0 is not always smart enough to use all available indices for multi-table queries
        query = "select verification.* from verification where ver_status = 1 order by ver_time desc limit %d, %d" % (start, per_page)

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        firstNumRows = CNX.DB_NUMROWS()
        if firstNumRows == 0:
                print('<h3>No verifications present</h3>')
                PrintTrailer('recentver', 0, 0)
                sys.exit(0)
        ver = CNX.DB_FETCHMANY()
        ver_set = []
        while ver:
                ver_set.append(ver[0])
                ver = CNX.DB_FETCHMANY()

        print('<table cellpadding=3 class="generic_table">')
        print('<tr class="generic_table_header">')
        print('<th>#</th>')
        print('<th>Publication Title</th>')
        print('<th>Reference</th>')
        print('<th>User</th>')
        print('<th>Time</th>')
        print('</tr>')

        color = 0
        count = start
        for ver in ver_set:
                pub_id = ver[VERIF_PUB_ID]
                verifier_id = ver[VERIF_USER_ID]
                verification_id = ver[VERIF_REF_ID]
                verification_time = ver[VERIF_TIME]
                query = """select r.reference_label, mu.user_name, p.pub_title
                           from reference r, mw_user mu, pubs p
                           where r.reference_id = %d
                           and mu.user_id = %d
                           and p.pub_id = %d""" % (verification_id, verifier_id, pub_id)
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                color = color ^ 1
                while record:
                        count += 1
                        reference_name = record[0][0]
                        user_name = record[0][1]
                        pub_title = record[0][2]
                        if color:
                                print('<tr align=left class="table1">')
                        else:
                                print('<tr align=left class="table2">')
                        print('<td>%d</td>' % count)
                        print('<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title))
                        print('<td>%s</td>' % reference_name)
                        print('<td>%s</td>' % WikiLink(user_name))
                        print('<td>%s</td>' % verification_time)
                        print('</tr>')
                        record = CNX.DB_FETCHMANY()

        print('</table>')
        if firstNumRows > (per_page - 1):
                print('<p> [%s]' % ISFDBLink('recentver.cgi', start + per_page, 'MORE'))

        PrintTrailer('recentver', 0, 0)

