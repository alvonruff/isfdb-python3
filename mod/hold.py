#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2026   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1260 $
#     Date: $Date: 2026-02-18 08:27:14 -0500 (Wed, 18 Feb 2026) $

from isfdb import *
from isfdblib import *
from library import *
from common import *

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Place Submission on Hold')
        PrintNavBar()

        (reviewerid, username, usertoken) = GetUserData()

        hold_id = SQLGetSubmissionHoldId(submission)

        if SQLloadState(submission) != 'N':
                print('<div id="ErrorBox">')
                print("<h3>Submission %d not in NEW state</h3>" % (int(submission)))
                print('</div>')

        else:
                if int(hold_id) == int(reviewerid):
                        print("<h3>Submission is already on hold by you.</h3>")
                elif hold_id:
                        holding_user = SQLgetUserName(hold_id)
                        print('<h3>Submission is already on hold by %s</h3>' % WikiLink(holding_user))
                else:
                        update = "update submissions set sub_holdid=%d where sub_id='%d';" % (int(reviewerid), int(submission))
                        CNX = MYSQL_CONNECTOR()
                        CNX.DB_QUERY(update)
                        print("<h3>Submission %d has been put on hold.</h3>" % int(submission))

        print(ISFDBLink('mod/submission_review.cgi', submission, 'Moderator View', False, 'class="approval" '))
        print(ISFDBLinkNoName('view_submission.cgi', submission, 'Public View', False, 'class="approval" '))
        print('<p><br>')
        PrintSubmissionLinks(submission, reviewerid)

        PrintPostMod(0)
