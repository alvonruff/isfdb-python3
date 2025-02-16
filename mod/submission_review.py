#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 428 $
#     Date: $Date: 2019-06-12 17:06:29 -0400 (Wed, 12 Jun 2019) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import SQLloadSubmission
from library import *
import viewers

def Approvable(app, submission_id):
        print('<p>')
        # First get the user information for the reviewing/approving moderator
        (reviewer_id, username, usertoken) = GetUserData()
        # Check the current status of the submission
        submission = SQLloadSubmission(submission_id)
        submitter_id = submission[SUB_SUBMITTER]
        hold_id = submission[SUB_HOLDID]
        sub_state = submission[SUB_STATE]
        sub_time = submission[SUB_TIME]
        sub_reviewed = submission[SUB_REVIEWED]
        sub_reviewer = submission[SUB_REVIEWER]
        submitting_user = SQLgetUserName(submitter_id)

        reviewer_is_moderator = SQLisUserModerator(reviewer_id)

        if sub_state in ('I', 'R'):
                print('<h3>This submission was created on %s and ' % sub_time)
                if sub_state == 'R':
                        print('rejected')
                else:
                        print('approved')
                moderator_name = SQLgetUserName(sub_reviewer)
                print(' by %s on %s</h3>' % (WikiLink(moderator_name), sub_reviewed))
                if sub_state == 'R':
                        print('<p>%s' % ISFDBLink('mod/unreject.cgi', submission_id, 'Unreject Submission'))
                return 0

        # Check if the submission was created by another moderator; if so, disallow approving
        if (int(submitter_id) != int(reviewer_id)) and SQLisUserModerator(submitter_id):
                print('<h3>Submission created by %s</h3>' % WikiLink(submitting_user))
                return 0

        wiki_edits = SQLWikiEditCount(submitting_user)
        if wiki_edits < 20:
                print('<h3>New editor with %d Wiki edits.</h3><p>' % wiki_edits)

        # Check if the submission is currently on hold by another moderator
        if hold_id:
                #If the submission is currently on hold by another moderator, don't allow moderation
                if int(hold_id) != int(reviewer_id):
                        holding_user = SQLgetUserName(hold_id)
                        print('<h3>Submission is currently on hold by %s</h3>' % WikiLink(holding_user))
                        # Let bureaucrats unhold submissions held by other moderators
                        if SQLisUserBureaucrat(reviewer_id):
                                print('%s <p>' % ISFDBLinkNoName('mod/unhold.cgi', submission_id, 'UNHOLD', False, 'class="hold" '))
                        return 0
                #If the submission is currently on hold by the reviewing moderator, allow to remove from hold
                print('<h3>Submission is currently on hold by you.</h3><p>')
                print('%s  ' % ISFDBLinkNoName('mod/unhold.cgi', submission_id, 'UNHOLD', False, 'class="hold" '))

        # If the submission is not currently on hold and the reviewer is a moderator as opposed to a self-approver, allow putting it on hold
        elif reviewer_is_moderator:
                print('%s  ' % ISFDBLinkNoName('mod/hold.cgi', submission_id, 'HOLD', False, 'class="hold" '))

        print(ISFDBLinkNoName('mod/%s' % app, submission_id, 'Approve', False, 'class="approval" '))
        DisplayPublicLinks(submission_id)
        PrintSubmissionLinks(submission_id, reviewer_id)
        print('<hr>')
        print('<form METHOD="POST" ACTION="/cgi-bin/mod/reject.cgi">')
        print('<p class="topspace"><b>Rejection Reason</b><p>')
        print('<p class="topspace"><textarea name="reason" rows="4" cols="45"></textarea>')
        print('<input name="sub_id" value="%d" type="HIDDEN">' % int(submission_id))
        print('<p class="topspace"><input id="rejection" type="SUBMIT" value="Reject">')
        print('</form>')
        return 1

def DisplayPublicLinks(submission_id):
        print('<span class="approval"><small>')
        print(ISFDBLinkNoName('view_submission.cgi', submission_id, 'Public View', False, 'class="approval" '))
        print(ISFDBLinkNoName('dumpxml.cgi', submission_id, 'View Raw XML', False, 'class="approval" '))
        print('</small></span>')
        print('<p><br>')

if __name__ == '__main__':

        submission_id = SESSION.Parameter(0, 'int')
        submission = SQLloadSubmission(submission_id)
        if not submission:
                SESSION.DisplayError('Specified Submission Does Not Exist')
        submission_type = submission[SUB_TYPE]
        xml_tag = SUBMAP[submission_type][1]

        # Parse the XML record and get the "true" submission type for display purposes
        doc2 = ISFDBSubmissionDoc(submission[SUB_DATA], xml_tag)
        display_tag = ISFDBSubmissionType(xml_tag, submission_type, doc2)
        displayType = ISFDBSubmissionDisplayType(display_tag, xml_tag, submission_type)

        PrintPreMod('Proposed %s Submission' % displayType)
        PrintNavBar()

        submission_filer = SUBMAP[submission_type][6]
        function_name = SUBMAP[submission_type][5]
        if SUBMAP[submission_type][0] == 0:
                function_to_call = getattr(viewers, function_name)
                submitter = function_to_call(submission_id)
        else:
                from viewers import SubmissionViewer
                submission_viewer = SubmissionViewer(function_name, submission_id)
                submitter = submission_viewer.submitter
        print('<b>Submitted by:</b> %s' % WikiLink(submitter))

        if not Approvable('%s.cgi' % submission_filer, submission_id):
                DisplayPublicLinks(submission_id)

        if submission_filer in ('ca_new', 'pa_new'):
                display_sources(submission_id)
        PrintPostMod(0)
