#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


import viewers
from isfdb import *
from common import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        submission_id = SESSION.Parameter(0, 'int')
        submission = SQLloadSubmission(submission_id)
        if not submission:
                SESSION.DisplayError('Specified submission ID does not exist')

        sub_type = submission[SUB_TYPE]
        sub_user = submission[SUB_SUBMITTER]
        sub_reviewer = submission[SUB_REVIEWER]
        sub_state = submission[SUB_STATE]
        sub_reason = submission[SUB_REASON]
        sub_data = submission[SUB_DATA]
        sub_time = submission[SUB_TIME]
        sub_reviewed = submission[SUB_REVIEWED]
        xml_tag = SUBMAP[sub_type][1]
        displayPage = SUBMAP[sub_type][2]

        # Parse the XML record and get the "true" submission type for display purposes
        doc2 = ISFDBSubmissionDoc(sub_data, xml_tag)
        display_tag = ISFDBSubmissionType(xml_tag, sub_type, doc2)
        displayType = ISFDBSubmissionDisplayType(display_tag, xml_tag, sub_type)

        # Compose the header, which will depend on the submission type and its approval status
        if sub_state == 'N':
                header = 'Pending'
        elif sub_state == 'I':
                header = 'Approved'
        elif sub_state == 'R':
                header = 'Canceled/Rejected'
        elif sub_state == 'P':
                header = 'In Progress or Errored Out'
        else:
                header = 'INVALID SUBMISSION STATUS!!!'
        header += ' %s Submission' % displayType
        PrintHeader(header)
        PrintNavbar('recent', 0, 0, 'view_submission.cgi', 0)
        
        if sub_state == 'R':
                print('<b>Cancellation/Rejection Reason</b>: %s<p>' % sub_reason)

        print('<b>Note</b>: For "Edit" submissions, the "Current" column shows the data as it currently exists in the database,')
        print('not as it existed when the submission was created.<p>')

        function_name = SUBMAP[sub_type][5]
        if SUBMAP[sub_type][0] == 0:
                function_to_call = getattr(viewers, function_name)
                submitter = function_to_call(submission_id)
        else:
                submission_viewer = viewers.SubmissionViewer(function_name, submission_id)
                submitter = submission_viewer.submitter

        if sub_state == 'I':
                (subjectLink, new_record) = getSubjectLink(submission, doc2, sub_type)
                if new_record:
                        print('<p><b>New record:</b> %s' % subjectLink)

        print('<p>%s' % ISFDBLink('dumpxml.cgi', submission_id, 'View the submission as raw XML'))
        
        print('<p><b>Submitted by</b> %s on %s' % (WikiLink(submitter), sub_time))

        (userID, username, usertoken) = GetUserData()
        # If the viewing user is the submitter and the submission is "N"ew, allow the user to cancel
        if int(userID) == int(sub_user) and sub_state == 'N':
                print(' %s' % ISFDBLink('cancelsubmission.cgi', submission_id, 'Cancel submission', True))
        # If the submission has been reviewed, display the reviewer's name
        elif sub_reviewer:
                moderator_name = SQLgetUserName(sub_reviewer)
                if sub_state == 'R':
                        status = 'Rejected'
                else:
                        status = 'Approved'
                print('<p><b>%s by</b> %s on %s' % (status, WikiLink(moderator_name), sub_reviewed))

        if SQLisUserModerator(userID):
                if sub_state == 'R':
                        print('<p>%s' % ISFDBLink('mod/unreject.cgi', submission_id, 'Unreject Submission'))
                elif sub_state == 'N':
                        print('<p>%s' % ISFDBLink('mod/submission_review.cgi', submission_id, 'Moderator View'))
        elif SQLisUserSelfApprover(userID) and sub_state == 'N':
                print('<p>%s' % ISFDBLink('mod/submission_review.cgi', submission_id, 'Self-Approver View'))

        PrintTrailer('recent', 0, 0)

