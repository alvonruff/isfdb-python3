#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2020-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 571 $
#     Date: $Date: 2020-11-19 15:53:08 -0500 (Thu, 19 Nov 2020) $


from isfdb import *
from common import *
from login import *
from SQLparsing import *


if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)

        PrintHeader('My Secondary Verifications')
        PrintNavbar('my_secondary_verifications', 0, 0, 'my_secondary_verifications.cgi', 0)

        user = User()
        user.load()
        if not user.id:
                print('<h3>You must be logged in to view your secondary verifications</h3>')
                PrintTrailer('my_secondary_verifications', 0, 0)
                sys.exit(0)

        per_page = 200
        # First select 200 verification IDs -- needs to be done as a separate query since the SQL optimizer
        # in MySQL 5.0 is not always smart enough to use all available indices for multi-table queries
        query = """select verification.* from verification
                where ver_status = 1
                and user_id = %d
                order by ver_time desc
                limit %d, %d""" % (int(user.id), start, per_page)

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        SQLlog("my_secondary_verifications::query: %s" % query)
        if CNX.DB_NUMROWS():
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
        print('<th>Time</th>')
        print('</tr>')

        color = 0
        count = start
        for ver in ver_set:
                pub_id = ver[VERIF_PUB_ID]
                verifier_id = ver[VERIF_USER_ID]
                verification_id = ver[VERIF_REF_ID]
                verification_time = ver[VERIF_TIME]
                query = """select r.reference_label, p.pub_title
                           from reference r, pubs p
                           where r.reference_id = %d
                           and p.pub_id = %d""" % (verification_id, pub_id)
                CNX.DB_QUERY(query)
                SQLlog("my_secondary_verifications::query: %s" % query)
                record = CNX.DB_FETCHMANY()
                color = color ^ 1
                while record:
                        count += 1
                        reference_name = record[0][0]
                        pub_title = record[0][1]
                        if color:
                                print('<tr align=left class="table1">')
                        else:
                                print('<tr align=left class="table2">')
                        print('<td>%d</td>' % count)
                        print('<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title))
                        print('<td>%s</td>' % reference_name)
                        print('<td>%s</td>' % verification_time)
                        print('</tr>')
                        record = CNX.DB_FETCHMANY()

        print('</table>')
        if result0.num_rows() > (per_page - 1):
                print('<p> [%s]' % ISFDBLink('my_secondary_verifications.cgi', start + per_page, 'MORE'))

        PrintTrailer('my_secondary_verifications', 0, 0)

