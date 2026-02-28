#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2026   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1251 $
#     Date: $Date: 2026-02-10 15:00:23 -0500 (Tue, 10 Feb 2026) $


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
        outstr = str.replace(outstr, '<', '&lt;')
        outstr = str.replace(outstr, '>', '&gt;')
        outstr = str.replace(outstr, '\n', '<br>')

        print(outstr)

        print('<p>')
        print(ISFDBLinkNoName('view_submission.cgi', submission_id, 'Public View', False, 'class="approval"'))
        (userid, username, usertoken) = GetUserData()
        # If the user is a moderator
        if SQLisUserModerator(userid):
                print(' %s' % ISFDBLink('mod/submission_review.cgi', submission_id, 'Moderator View', False, 'class="approval"'))

        PrintTrailer('dumpxml', 0, 0)
