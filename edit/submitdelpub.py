#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025  Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 972 $
#     Date: $Date: 2022-08-23 16:44:48 -0400 (Tue, 23 Aug 2022) $

        
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
        submission.header = 'Publication Delete Submission'
        submission.cgi_script = 'deletepub'
        submission.type = MOD_PUB_DELETE

        form = IsfdbFieldStorage()
        try:
                pub_id = int(form['pub_id'].value)
                pubname = SQLgetPubTitle(pub_id)
                if not pubname:
                        raise
        except:
                submission.error('Publication does not exist any more')

        if not submission.user.id:
                submission.error('', pub_id)
        
        if 'mod_note' in form:
                reason = form['mod_note'].value
        else:
                reason = 'No reason given.'

        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <PubDelete>\n"
        update_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(pubname)))
        update_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))
        update_string += "    <Record>%d</Record>\n" % (pub_id)
        update_string += "    <Reason>%s</Reason>\n" % CNX.DB_ESCAPE_STRING(XMLescape(reason))
        update_string += "  </PubDelete>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
