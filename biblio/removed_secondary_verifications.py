#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2017-10-31 19:57:53 -0400 (Tue, 31 Oct 2017) $


from isfdb import *
from common import *
from SQLparsing import *


if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)

        PrintHeader('Recently Removed Secondary Verifications')
        PrintNavbar('removed_secondary_verifications', 0, 0, 'removed_secondary_verifications.cgi', 0)

        per_page = 200
        # First select 200 deleted verification IDs -- needs to be done as a separate query since the SQL optimizer
        # in MySQL 5.0 is not always smart enough to use all available indices for multi-table queries
        query = "select * from deleted_secondary_verifications order by deletion_time desc limit %d, %d" % (start, per_page)

        db.query(query)
        result0 = db.store_result()
        if result0.num_rows() == 0:
                print '<h3>No removed secondary verifications present for the specified ID range</h3>'
                PrintTrailer('removed_secondary_verifications', 0, 0)
                sys.exit(0)
        deleted = result0.fetch_row()
        deleted_verifications = []
        while deleted:
                deleted_verifications.append(deleted[0])
                deleted = result0.fetch_row()

        print '<table cellpadding=3 class="generic_table">'
        print '<tr class="generic_table_header">'
        print '<th>#</th>'
        print '<th>Publication</th>'
        print '<th>Reference</th>'
        print '<th>Original Verifier</th>'
        print '<th>Verification Time</th>'
        print '<th>Deleting Moderator</th>'
        print '<th>Deletion Time</th>'
        print '</tr>'

        color = 0
        count = start
        for deleted in deleted_verifications:
                reference_id = deleted[DEL_VER_REFERENCE_ID]
                verifier_id = deleted[DEL_VER_VERIFIER_ID]
                deleter_id = deleted[DEL_VER_DELETER_ID]
                pub_id = deleted[DEL_VER_PUB_ID]
                verification_time = deleted[DEL_VER_VERIFICATION_TIME]
                deletion_time = deleted[DEL_VER_DELETION_TIME]
                
                query = """select p.pub_title, r.reference_label, u1.user_name, u2.user_name
                           from pubs p, reference r, mw_user u1, mw_user u2
                           where r.reference_id = %d
                           and u1.user_id = %d
                           and u2.user_id = %d
                           and p.pub_id=%d""" % (reference_id, verifier_id, deleter_id, pub_id)
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                color = color ^ 1
                while record:
                        count += 1
                        pub_title = record[0][0]
                        reference_name = record[0][1]
                        verifier_name = record[0][2]
                        deleter_name = record[0][3]
                        if color:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                        print '<td>%s</td>' % reference_name
                        print '<td>%s</td>' % WikiLink(verifier_name)
                        print '<td>%s</td>' % verification_time
                        print '<td>%s</td>' % WikiLink(deleter_name)
                        print '<td>%s</td>' % deletion_time
                        print '</tr>'
                        record = result.fetch_row()

        print '</table>'
        if result0.num_rows() > (per_page - 1):
                print '<p> [%s]' % ISFDBLink('removed_secondary_verifications.cgi', start + per_page, 'MORE')

        PrintTrailer('removed_secondary_verifications', 0, 0)

