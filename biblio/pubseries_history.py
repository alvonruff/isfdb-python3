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

        pubseries_id = SESSION.Parameter(0, 'int')

        PrintHeader('Publication Series Edit History')
        PrintNavbar('pubseries_history', 0, 0, 'pubseries_history.cgi', pubseries_id)

        print("""<h3>The list below displays Edit Publication Series submissions for this publication series.
                Note that publication series records are created and deleted automatically when
                publications are created/edited/deleted; related
                submissions are not displayed on this page.</h3>""")

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d)
                order by sub_reviewed desc
                """ % (pubseries_id, MOD_PUB_SERIES_UPDATE)
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print('<h3>No submission data on file for this publication series.</h3>')
        else:
                ISFDBprintSubmissionTable(result, 'I')

        PrintTrailer('pubseries_history', 0, 0)

