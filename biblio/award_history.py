#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2020-2026   Ahasuerus, Al von Ruff
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

        award_id = SESSION.Parameter(0, 'int')

        PrintHeader('Award Edit History')
        PrintNavbar('award_history', 0, 0, 'award_history.cgi', award_id)

        print("""<h3>The list below displays the following types of submissions: Add Award,
                Edit Award, Delete Award, Link Award. The submission which created this
                award is displayed if the award was created after 2016-10-24.</h3>""")

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d, %d, %d)
                order by sub_reviewed desc
                """ % (award_id, MOD_AWARD_NEW, MOD_AWARD_UPDATE, MOD_AWARD_DELETE, MOD_AWARD_LINK)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        SQLlog("award_history::query: %s" % query)
        if not CNX.DB_NUMROWS():
                print('<h3>No submission data on file for this award.</h3>')
        else:
                ISFDBprintSubmissionTable(CNX, 'I')

        PrintTrailer('award_history', 0, 0)

