#
#     (C) COPYRIGHT 2005-2024   Al von Ruff, Kevin Pulliam (kevin.pulliam@gmail.com), Bill Longley, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1166 $
#     Date: $Date: 2024-02-08 14:50:44 -0500 (Thu, 08 Feb 2024) $


from isfdb import *
from login import *
from library import *
from navbar import *
from SQLparsing import *


##################################################################
# These routines start and end the HTML page
##################################################################
def PrintPreMod(title):
        PrintHTMLHeaders(title)
        print '</div>'

##################################################
#
#	Function appears in three different locations
#	See /edit/isfdblib.py for Edit PrintUserInfo function
#	see /biblio/common.py for Regular PrintUserInfo function
#
##################################################
def PrintUserInfo():
	(userid, username, usertoken) = GetUserData()
	if username:
                PrintLoggedIn(userid, username)
	else:
                PrintNotLoggedIn(0,0)
	return username
#######################################################
#
#	Function appears in three different locations
#	Moderator NavBar function.
#	See /edit/isfdblib.py for Edit NavBar function
#	see /biblio/common.py for Regular NavBar function
#
#######################################################
def PrintNavBar():
	print '<div id="nav">'

        # Print the search box from module navbar
        PrintSearchBox('')
	
        (userid, username, usertoken) = GetUserData()
        moderator = SQLisUserModerator(userid)
        bureaucrat = SQLisUserBureaucrat(userid)
        self_approver = SQLisUserSelfApprover(userid)

	username = PrintUserInfo()

        # Print the Other Pages section from module navbar
	PrintOtherPages('')

	if moderator:
                print '<div class="divider">'
                print 'Moderator Links:'
                print '</div>'
                print '<ul class="navbar">'
                print '<li>%s' % ISFDBLink('mod/list.cgi', 'N', 'Moderator')
                if bureaucrat:
                        print '<li>%s' % ISFDBLink('mod/bureaucrat.cgi', 'N', 'Bureaucrat')
                print '<li>%s' % ISFDBLink('mod/recent.cgi', '0+R', 'Recent Rejections')
                print '<li>%s' % ISFDBLink('mod/recent.cgi', '0+I', 'Recent Approvals')
                print '<li>%s' % ISFDBLink('mod/recent.cgi', '0+P', 'Errored Out Submissions')
                print '<li>%s' % ISFDBLink('mod/tag_status_changes.cgi', '', 'Tag Status Changes')
                print '<li>%s' % ISFDBLink('mod/private_tags.cgi', '', 'Private Tags')
                print '<li>%s' % ISFDBLink('mod/submission_search.cgi', '', 'Submission Search')
                print '</ul>'
        print '</div>'
        print '<div id="main2">'
        onlineVersion = SQLgetSchemaVersion()
        if onlineVersion != SCHEMA_VER:
                print "<h3>Warning: database schema mismatch (%s vs %s)</h3>" % (onlineVersion, SCHEMA_VER)
        if username == 0:
                SESSION.DisplayError('%s required to perform moderator tasks.' % ISFDBLink('dologin.cgi', 'mod/list.cgi+N', 'Login'), 0)

	if not moderator:
                if self_approver and SelfApprovalAllowed(userid):
                        pass
                else:
                        SESSION.DisplayError('Moderator privileges are required for this option', 0)

        bureaucrat_only = ('bureaucrat', 'cpanel', 'list_verification_sources', 'marque'
                           'self_approvers', 'self_approver_file', 'submitcpanel',
                           'verification_source_file', 'verification_source_add_file',
                           'web_api_users', 'web_api_users_file')
        if SESSION.cgi_script in bureaucrat_only and not bureaucrat:
                SESSION.DisplayError('Bureaucrat privileges are required for this option', 0)

def SelfApprovalAllowed(userid):
        # Special case -- rejection permissions are handled by reject.cgi because the submission ID is in the form
        if SESSION.cgi_script == 'reject':
                return 1

        self_approval_supported = 0
        # Only submission review and submission approval scripts can be accessed by self-approvers
        if SESSION.cgi_script == 'submission_review':
                self_approval_supported = 1
        else:
                for option_number in SUBMAP:
                        option_tuple = SUBMAP[option_number]
                        if len(option_tuple) > 6 and option_tuple[6] == SESSION.cgi_script:
                                self_approval_supported = 1
                                break
        if not self_approval_supported:
                return 0

        try:
                submission_id = int(SESSION.parameters[0])
        except:
                return 0

        if SelfCreated(submission_id, userid):
                return 1
        else:
                return 0


def SelfCreated(submission_id, reviewer_id):
        # Check if this submission was created by this reviewer
        sub_data = SQLloadSubmission(submission_id)
        if not sub_data:
                return 0
        submitter_id = sub_data[SUB_SUBMITTER]
        if int(submitter_id) == int(reviewer_id):
                return 1
        return 0

def PrintPostMod(closetable = 1):
        if closetable:
                print '</table>'
        print '</div>'
        print '<div id="bottom">'
        print COPYRIGHT
        print '<br>'
        print ENGINE
        print '</div>'
        print '</div>'
        print '</body>'
        print '</html>'
        db.close()

def markIntegrated(db, sub_id, affected_record_id = None, pub_id = None):
        from common import PrintSubmissionLinks
        (reviewerid, username, usertoken) = GetUserData()
        update = """update submissions
                    set sub_state='I', sub_reviewer=%d, sub_reviewed=NOW(), sub_holdid=0
                    where sub_id=%d""" %  (int(reviewerid), int(sub_id))
        print '<li> ', update
        db.query(update)

        # For submissions that created a new record or affected an existing record
        # of a supported type, update the "affected record ID" field in the submission record
        if affected_record_id:
                update = "update submissions set affected_record_id=%d where sub_id=%d" %  (int(affected_record_id), int(sub_id))
                print "<li> ", update
                db.query(update)

        # For changed publications, update the Changed Verified Pubs table and the user_status table
        if pub_id:
                # Get the ID of the submitter
                user_id = SQLGetSubmitterId(sub_id)
                # Retrieve the list of primary verifiers for this publication
                VerificationList = SQLPrimaryVerifiers(pub_id)
                for verifier in VerificationList:
                        verifier_id = verifier[0]
                        # If this primary verifier is the user who created the submission,
                        # do not update the "changed verified pubs" table
                        if verifier_id == user_id:
                                continue
                        update = """insert into changed_verified_pubs(pub_id, sub_id, verifier_id, change_time)
                               values(%d, %d, %d, NOW())""" % (int(pub_id), int(sub_id), int(verifier_id))
                        print "<li> ", update
                        db.query(update)
                        SQLUpdate_last_changed_verified_pubs_DTS(verifier_id)

        print '</ul>'
        print '<hr><br>'
        PrintSubmissionLinks(sub_id, reviewerid)
        print '<p>'

def NotApprovable(submission):
    if SQLloadState(submission) != 'N':
            print '<div id="ErrorBox">'
            print '<h3>Submission %d not in NEW state</h3>' % (int(submission))
            print '</div>'
            PrintPostMod(0)
            return 1
    (reviewerid, username, usertoken) = GetUserData()
    hold_id = SQLGetSubmissionHoldId(submission)
    if hold_id:
            if int(hold_id) != int(reviewerid):
                    holding_user = SQLgetUserName(hold_id)
                    print '<div id="ErrorBox">'
                    print "<h3>Submission can't be moderated because it is on hold by %s</h3>" % WikiLink(holding_user)
                    print '</div>'
                    PrintPostMod(0)
                    return 1
    # If we are here, then this submission is approvable. Temporarily set its status to "inProgress".
    SQLmarkInProgress(submission)
    return 0

def LIBPrintDuplicateWarning(pub_id):
        titles = SQLloadTitlesXBT(pub_id)
        duplicate_count = 0
        for title in titles:
                if title[TITLE_TTYPE] != 'REVIEW':
                        if ISFDBPossibleDuplicates(title):
                                duplicate_count += 1
        if duplicate_count:
                print('<p><div id="WarningBox"><b>')
                duplicate_finder_link = 'See %s for details.' % ISFDBLinkNoName('edit/find_pub_dups.cgi', pub_id, 'Duplicate Finder')
                if duplicate_count == 1:
                        print('There is 1 possible duplicate title in the new pub. %s' % duplicate_finder_link)
                else:
                        print('There are %d possible duplicate titles in the new pub. %s' % (duplicate_count, duplicate_finder_link))
                print('</b></div><p>')
