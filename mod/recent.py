#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2026   Al von Ruff, Ahasuerus, Dirk Stoecker and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1260 $
#     Date: $Date: 2026-02-18 08:27:14 -0500 (Wed, 18 Feb 2026) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)
        status = SESSION.Parameter(1, 'str', 'I', ('I', 'R', 'N', 'P'))

        if status == 'I':
                PrintPreMod('Recent Approvals')
                PrintNavBar()
        elif status == 'R':
                PrintPreMod('Recent Rejections')
                PrintNavBar()
        elif status == 'N':
                PrintPreMod('Recent Pending Submissions')
                PrintNavBar()
        elif status == 'P':
                PrintPreMod('Errored Out and "In Progress" Submissions')
                PrintNavBar()
                print("""<h3>Note: The status of each submission is temporarily changed from "New" to
                        "In Progress" during the approval process. Once a submission has been
                        successfully approved, its status is changed to "Approved". If, on the
                        other hand, the approval process errors out, then the submission remains
                        "In Progress" and is displayed on this page. If a new submission
                        appears on this list, check again in a few seconds to make sure that you
                        didn't catch it while it was in the process of being approved.</h3>""")

        if start:
                query = "select * from submissions use index (state_reviewed) where sub_state='%s' order by sub_reviewed desc limit %d,200;" % (status, start)
        else:
                query = "select * from submissions use index (state_reviewed) where sub_state='%s' order by sub_reviewed desc limit 200;" % (status)

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() == 0:
                print('<h3>No submissions with the specified status present.</h3>')
        else:
                ISFDBprintSubmissionTable(CNX, status)
                print('<p> %s' % ISFDBLinkNoName('mod/recent.cgi','%d+%s' % (start+200, status), 'MORE', True))

        PrintPostMod(0)

