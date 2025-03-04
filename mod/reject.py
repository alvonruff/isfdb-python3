#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 614 $
#     Date: $Date: 2021-04-06 15:42:09 -0400 (Tue, 06 Apr 2021) $


import string
import sys
import cgi
from isfdb import *
from common import *
from isfdblib import *
from library import *
from SQLparsing import *


def PrintError(message):
        print(message)
        PrintPostMod(0)
        sys.exit(1)

if __name__ == '__main__':

        PrintPreMod('Reject Submission')
        PrintNavBar()

        sys.stderr = sys.stdout
        form = IsfdbFieldStorage()

        try:
                sub_id = int(form["sub_id"].value)
        except:
                PrintError("ERROR: Can't get submission ID.")

        if NotApprovable(sub_id):
                sys.exit(0)

        if "reason" in form:
                # Run the rejection reason through XML escaping and
                # unescaping in order to normalize input
                reason = XMLunescape(XMLescape(form["reason"].value))
        else:
                reason = ''

        print("<ul>")

        (reviewerid, username, usertoken) = GetUserData()
        reviewer_is_moderator = SQLisUserModerator(reviewerid)
        if not reviewer_is_moderator and not SelfCreated(sub_id, reviewerid):
                PrintError("This submission wasn't created by you. Self-approvers can only reject their own submissions.")

        CNX = MYSQL_CONNECTOR()
        update = """update submissions set sub_state='R', sub_reason='%s',
                    sub_reviewer='%d', sub_reviewed=NOW(), sub_holdid=0
                    where sub_id=%d""" % (CNX.DB_ESCAPE_STRING(reason), int(reviewerid), sub_id)
        print("<li> ", update)
        CNX.DB_QUERY(update)

        print("</ul><p><hr>")
        
        print("Record %d has been moved to the Rejected state.<br>" % sub_id)
        print("<b>Reason:</b> ", reason)

        print('<p>')
        print('<hr>')
        print('<p>')
        PrintSubmissionLinks(sub_id, reviewerid)

        PrintPostMod(0)
