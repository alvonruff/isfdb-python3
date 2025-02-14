#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2019-12-01 19:57:53 -0400 (Tue, 31 Oct 2017) $


from isfdb import *
from common import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        publisher_id = SESSION.Parameter(0, 'int')

        PrintHeader('Publisher Edit History')
        PrintNavbar('publisher_history', 0, 0, 'publisher_history.cgi', publisher_id)

        print("""<h3>The list below displays Edit Publisher and Publisher Merge submissions for this publisher.
                Note that publisher records are created and deleted automatically when
                publications are created/edited/deleted; related
                submissions are not displayed on this page.</h3>""")

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d)
                order by sub_reviewed desc
                """ % (publisher_id, MOD_PUBLISHER_UPDATE, MOD_PUBLISHER_MERGE)
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print('<h3>No submission data on file for this publisher.</h3>')
        else:
                ISFDBprintSubmissionTable(result, 'I')

        PrintTrailer('publisher_history', 0, 0)

