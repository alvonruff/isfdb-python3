#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020-2025   Ahasuerus
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


if __name__ == '__main__':

        awardtype_id = SESSION.Parameter(0, 'int')

        PrintHeader('Award Type Edit History')
        PrintNavbar('awardtype_history', 0, 0, 'awardtype_history.cgi', awardtype_id)

        print """<h3>The list below displays the following types of submissions: New Award Type,
                Edit Award Type, Delete Award Type. The submission which created this award type
                is displayed if the award type was created after 2016-10-24.</h3>"""

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d, %d)
                order by sub_reviewed desc
                """ % (awardtype_id, MOD_AWARD_TYPE_NEW, MOD_AWARD_TYPE_UPDATE, MOD_AWARD_TYPE_DELETE)
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h3>No submission data on file for this award type.</h3>'
        else:
                ISFDBprintSubmissionTable(result, 'I')

        PrintTrailer('awardtype_history', 0, 0)

