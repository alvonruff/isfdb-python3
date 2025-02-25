#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 972 $
#     Date: $Date: 2022-08-23 16:44:48 -0400 (Tue, 23 Aug 2022) $

        
import cgi
import sys
import MySQLdb
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

        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <AwardTypeDelete>\n"
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(awardType.award_type_name)))
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <AwardTypeId>%d</AwardTypeId>\n" % int(awardType.award_type_id)
        update_string += "    <Reason>%s</Reason>\n" % db.escape_string(XMLescape(reason))
        update_string += "  </AwardTypeDelete>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
