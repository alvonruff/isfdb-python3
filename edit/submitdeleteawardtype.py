#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
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
from login import *
from library import *
from awardtypeClass import *
from SQLparsing import *
from navbar import *
        
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Award Type Delete Submission'
        submission.cgi_script = 'deleteawardtype'
        submission.type = MOD_AWARD_TYPE_DELETE

        form = IsfdbFieldStorage()

        try:
                record = int(form['award_type_id'].value)
                awardType = award_type()
                awardType.award_type_id = record
                awardType.load()
                if not awardType.award_type_name:
                        raise
        except:
                submission.error('Invalid award type')
        
        if 'reason' in form:
                reason = form['reason'].value
        else:
                reason = 'No reason given.'

        if not submission.user.id:
                submission.error('', awardType.award_type_id)

        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <AwardTypeDelete>\n"
        update_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(awardType.award_type_name)))
        update_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))
        update_string += "    <AwardTypeId>%d</AwardTypeId>\n" % int(awardType.award_type_id)
        update_string += "    <Reason>%s</Reason>\n" % CNX.DB_ESCAPE_STRING(XMLescape(reason))
        update_string += "  </AwardTypeDelete>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
