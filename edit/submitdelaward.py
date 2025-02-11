#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff and Ahasuerus
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
from awardClass import *
from login import *
from library import *
from SQLparsing import *


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Award Delete Submission'
        submission.cgi_script = 'deleteaward'
        submission.type = MOD_AWARD_DELETE

        form = cgi.FieldStorage()

        try:
                award_id = int(form['award_id'].value)
                award_data = SQLloadAwards(award_id)
                award_title = award_data[0][AWARD_TITLE]
        except:
                submission.error('Invalid award number')

        if form.has_key('reason'):
                reason = form['reason'].value
        else:
                reason = 'No reason given.'

        if not submission.user.id:
                submission.error("", award_id)

        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <AwardDelete>\n"
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(award_title)))
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <Record>%d</Record>\n" % int(award_id)
        update_string += "    <Reason>%s</Reason>\n" % (db.escape_string(XMLescape(reason)))
        update_string += "  </AwardDelete>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
