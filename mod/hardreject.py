#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2022   Al von Ruff, Ahasuerus and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1003 $
#     Date: $Date: 2022-09-15 14:36:33 -0400 (Thu, 15 Sep 2022) $


from isfdb import *
from common import *
from isfdblib import *
from library import *
from SQLparsing import *


if __name__ == '__main__':

        sub_id = SESSION.Parameter(0, 'int')

        PrintPreMod('Reject Submission')
        PrintNavBar()

        # Retrieve user information for the moderator tring to reject this submission
	(reviewerid, username, usertoken) = GetUserData()

        # Retrieve submission data
	query = "select * from submissions where sub_id=%d" % int(sub_id)
	db.query(query)
	result = db.store_result()
	if result.num_rows() == 0:
		print '<h3>Specified submission ID does not exist</h3>'
		PrintPostMod()
		sys.exit(0)

        record = result.fetch_row()
        # If the submission is on hold, determine who the holding moderator is
        holder_id = record[0][SUB_HOLDID]
        if holder_id:
                # If the current user is neither the holding moderator nor a bureaucrat,
                # display a message explaining what needs to be done and abort
                if (int(holder_id) != int(reviewerid)) and (SQLisUserBureaucrat(reviewerid) == 0):
                        holder_name = SQLgetUserName(holder_id)
                        print '''<h3> This submission is currently held by %s.
                        Please contact the holding moderator to discuss the submission. If the holding moderator is
                        inactive, please post on the Moderator Noticeboard and a bureaucrat will hard reject the
                        submission.</h3>''' % WikiLink(holder_name)
                        PrintPostMod(0)
                        sys.exit(0)

        # If the submission was created by another moderator, do not allow rejection unless the current
        # user is a bureaucrat
        submitter_id = record[0][SUB_SUBMITTER]
        if ((int(submitter_id) != int(reviewerid))
            and (SQLisUserModerator(submitter_id) == 1)
            and not SQLisUserBureaucrat(reviewerid)):
                submitter_name = SQLgetUserName(submitter_id)
                print '''<h3> This submission was created by %s, another moderator.
                Please contact the submitter to discuss the submission. If the submitting moderator is
                inactive, please post on the Moderator Noticeboard and a bureaucrat will hard reject the
                submission.</h3>''' % WikiLink(submitter_name)
                PrintPostMod(0)
                sys.exit(0)

	update = """update submissions
                set sub_state='R', sub_reason='Forced', sub_reviewer=%d, sub_reviewed=NOW(), sub_holdid=0
                where sub_id=%d""" % (int(reviewerid), int(sub_id))
	print '<ul>'
        print '<li> ', update
	db.query(update)
        print '</ul>'
	print '<p>'
	PrintSubmissionLinks(sub_id, reviewerid)
	PrintPostMod(0)
