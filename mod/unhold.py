#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2026   Ahasuerus and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1260 $
#     Date: $Date: 2026-02-18 08:27:14 -0500 (Wed, 18 Feb 2026) $

from isfdb import *
from SQLparsing import *
from library import *
from login import GetUserData

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')
        (reviewerid, username, usertoken) = GetUserData()

        # Check that the submission is new
        if SQLloadState(submission) != 'N':
                SESSION.DisplayError('Submission %d is not in NEW state' % submission)

        hold_id = SQLGetSubmissionHoldId(submission)
        if not hold_id:
                SESSION.DisplayError('Submission %d is not on hold' % submission)

        # Only holding moderators and bureaucrats can unhold submissions
        if (int(hold_id) != int(reviewerid)) and not SQLisUserBureaucrat(reviewerid):
                SESSION.DisplayError('Submission is currently on hold by %s' % WikiLink(SQLgetUserName(hold_id)))

        update = "update submissions set sub_holdid=0 where sub_id=%d" % submission
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)
        ISFDBLocalRedirect('mod/submission_review.cgi?%d' % submission)
