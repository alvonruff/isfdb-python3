#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2026   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1259 $
#     Date: $Date: 2026-02-15 16:59:31 -0500 (Sun, 15 Feb 2026) $

        
import cgi
import sys
from isfdb import *
from isfdblib import *
from pubClass import *
from login import *
from library import *
from SQLparsing import *
from navbar import *
        
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Title Delete Submission'
        submission.cgi_script = 'deletetitle'
        submission.type = MOD_TITLE_DELETE

        form = IsfdbFieldStorage()

        try:
                title_id = int(form['title_id'].value)
        except:
                submission.error('Invalid title number')
        
        if 'reason' in form:
                reason = form['reason'].value
        else:
                reason = 'No reason given.'

        if not submission.user.id:
                submission.error("", title_id)

        titlename = SQLgetTitle(title_id)

        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <TitleDelete>\n"
        update_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(titlename)))
        update_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))
        update_string += "    <Record>%d</Record>\n" % int(title_id)
        update_string += "    <Reason>%s</Reason>\n" % CNX.DB_ESCAPE_STRING(XMLescape(reason))
        update_string += "  </TitleDelete>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
