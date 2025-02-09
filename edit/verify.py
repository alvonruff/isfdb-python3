#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2022   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1003 $
#     Date: $Date: 2022-09-15 14:36:33 -0400 (Thu, 15 Sep 2022) $


from isfdb import *
from isfdblib import *
from SQLparsing import *
from login import *

pub_id = SESSION.Parameter(0, 'int')
publication = SQLGetPubById(pub_id)
if not publication:
        SESSION.DisplayError('Record Does Not Exist')

PrintPreSearch('Verify Publication')
PrintNavBar(0, 0)

print '<div id="HelpBox">'
print '<b>Help on verifying publications: </b>'
print '<a href="%s://%s/index.php/Help:Screen:Verify">Help:Screen:Verify</a><p>' % (PROTOCOL, WIKILOC)
print '</div>'

# Get the current user's information
(user_id, username, usertoken) = GetUserData()
print '<h2>Primary Verification Status of %s</h2>' % ISFDBLink('pl.cgi', pub_id, publication[PUB_TITLE])
ver_status = SQLPrimaryVerStatus(pub_id, user_id)
if not ver_status:
        message = 'Currently not verified by you. You can add one of the following'
        choices = (('Permanent', ' CHECKED'), ('Transient', ''))
elif ver_status == 'permanent':
        message = 'Permanently verified by you. You can change it as follows'
        choices = (('No', ' CHECKED'), ('Transient', ''))
elif ver_status == 'transient':
        message = 'Transient-verified by you. You can change it as follows'
        choices = (('Permanent', ' CHECKED'), ('No', ''))
else:
        print 'An error has occurred. Please report it on the Community Portal.'
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)
print '<h3>%s:</h3>' % message
print '<form METHOD="POST" ACTION="/cgi-bin/edit/submit_primary_verification.cgi">'
print '<p>'
print '<input NAME="pubid" VALUE="%d" TYPE="HIDDEN">' % int(pub_id)
print '<table>'
for choice in choices:
        print '<tr>'
        ver_type = choice[0]
        checked = choice[1]
        print '<td>%s verification:</td>' % ver_type
        print '<td><input type="radio" value="%s" name="ver_status"%s></td>' % (ver_type, checked)
        print '</tr>'
print '</table>'
print '<p>'
print '<input type="SUBMIT" VALUE="Verify">'
print '</form>'
print '<p>'

print '<hr class="divider">'
print '<p>'
# Retrieve secondary verifications for the current publication
secondary_verifications = SQLSecondaryVerifications(pub_id)
# Retrieve the reference/source list for secondary verifications
references = SQLGetRefDetails()

print '<h2>Secondary Verifications</h2>'
print '<form METHOD="POST" ACTION="/cgi-bin/edit/submitver.cgi">'
print '<p>'
print '<input NAME="pubid" VALUE="%s" TYPE="HIDDEN">' % pub_id
print '<table>'
print '<tr>'
print '<th>Reference</th>'
print '<th>Not Verified</th>'
print '<th>Verified</th>'
print '<th>Marked N/A</th>'
print '</tr>'
for reference in references:
        ref_id = reference[REFERENCE_ID]
        print '<tr class="generic_table_header">'
        if not reference[REFERENCE_URL]:
                print '<td class="label">%s</td>' % (reference[REFERENCE_LABEL])
        else:
                print '<td class="label"><a href="%s">%s</a></td>' % (reference[REFERENCE_URL], reference[REFERENCE_LABEL])

        ver_status = 0
        for verification in secondary_verifications:
                if verification[VERIF_REF_ID] == ref_id:
                        ver_status = verification[VERIF_STATUS]
                        break
        if ver_status == 0:
                print '<td><input type="radio" value="NOTVER" name="xx%d" CHECKED></td>' % ref_id
                print '<td><input type="radio" value="VER" name="xx%d"></td>' % ref_id
                print '<td><input type="radio" value="NA" name="xx%d"></td>' % ref_id
        elif ver_status == 1:
                # Retrieve the name of the user who verified this pub/source combination
                verifier_name = SQLgetUserName(verification[VERIF_USER_ID])
                # Only allow checking "Not verified" if the current user is the verifier for this source
                if verifier_name == username:
                        print '<td><input type="radio" value="NOTVER" name="xx%d"></td>' % ref_id
                else:
                        print '<td><input type="radio" value="NOTVER" name="xx%d" class="nodisplay"></td>'  % ref_id
                print '<td><input type="radio" value="VER" name="xx%d" class="nodisplay">%s</td>' % (ref_id, WikiLink(verifier_name))
                # Only allow checking "N/A" if the current user is the verifier for this source
                if verifier_name == username:
                        print '<td><input type="radio" value="NA" name="xx%d"></td>' % ref_id
                else:
                        print '<td><input type="radio" value="NA" name="xx%d" class="nodisplay"></td>'  % ref_id
        elif ver_status == 2:
                # Retrieve the name of the user who marked this pub/source combination "N/A"
                verifier_name = SQLgetUserName(verification[VERIF_USER_ID])
                print '<td><input type="radio" value="NOTVER" name="xx%d"></td>' % ref_id
                print '<td><input type="radio" value="VER" name="xx%d"></td>' % ref_id
                print '<td><input type="radio" value="NA" name="xx%d" class="nodisplay">%s</td>' % (ref_id, WikiLink(verifier_name))
        print '</tr>'
print '</table>'
print '<p>'
print '<input type="SUBMIT" VALUE="Update Secondary Verifications">'
print '</form>'

if SQLisUserModerator(user_id):
        print '<hr class="divider">'
        print ISFDBLink('mod/select_secondary_verification.cgi', pub_id, 'Select a Secondary Verification to Remove (Moderator Only)')

PrintPostSearch(tableclose=False)
