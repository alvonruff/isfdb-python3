#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 641 $
#     Date: $Date: 2021-06-17 13:27:32 -0400 (Thu, 17 Jun 2021) $


from isfdb import *
from common import *
from library import *
from SQLparsing import *


if __name__ == '__main__':

        submission_id = SESSION.Parameter(0, 'int')
        submission_body = SQLloadSubmission(submission_id)
	if not submission_body:
                SESSION.DisplayError('Submission ID %d is not present' % submission_id)

	if submission_body[SUB_STATE] != 'N':
                SESSION.DisplayError('Submission %d is not in NEW state' % submission_id)

	(myID, username, usertoken) = GetUserData()

	if int(submission_body[SUB_SUBMITTER]) != int(myID):
                SESSION.DisplayError("Submissions created by other users can't be cancelled!")

	PrintHeader('Submission Cancellation')
	PrintNavbar('cancelsubmission', 0, 0, 'cancelsubmission.cgi', 0)

        print '<ul>'

	reason = 'Cancelled by the submitter'
	update = """update submissions
                set sub_state='R', sub_reason='%s', sub_reviewer=%d, sub_reviewed=NOW(), sub_holdid=0
                where sub_id=%d""" % (db.escape_string(reason), int(myID), submission_id)
        print '<li> ', update
	db.query(update)

        print '</ul><p><hr>'

	print 'Record %d has been moved to the Rejected state.<br>' % submission_id
	print '<b>Reason:</b> ', reason

	print '<p><hr>'

	PrintTrailer('cancelsubmission', 0, 0)
