#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 957 $
#     Date: $Date: 2022-07-13 09:59:00 -0400 (Wed, 13 Jul 2022) $


from isfdb import *
from common import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        submission_id = SESSION.Parameter(0, 'int')
        submission_body = SQLloadSubmission(submission_id)
        if not submission_body:
                SESSION.DisplayError('Submission number %d not found in the submission queue</h2>' % submission_id)

        PrintHeader('Raw XML View')
        PrintNavbar('dumpxml', 0, 0, 0, 0)

        outstr = submission_body[SUB_DATA]
        outstr = string.replace(outstr, '<', '&lt;')
        outstr = string.replace(outstr, '>', '&gt;')
        outstr = string.replace(outstr, '\n', '<br>')

        print outstr

        print '<p>'
        print ISFDBLinkNoName('view_submission.cgi', submission_id, 'Public View', False, 'class="approval"')
        (userid, username, usertoken) = GetUserData()
        # If the user is a moderator
        if SQLisUserModerator(userid):
                print ' %s' % ISFDBLink('mod/submission_review.cgi', submission_id, 'Moderator View', False, 'class="approval"')

        PrintTrailer('dumpxml', 0, 0)
