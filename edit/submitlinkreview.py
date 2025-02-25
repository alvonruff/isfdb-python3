#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended titlelication of such source code.
#
#     Version: $Revision: 972 $
#     Date: $Date: 2022-08-23 16:44:48 -0400 (Tue, 23 Aug 2022) $

        
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from SQLparsing import *
from login import *
from library import *
from navbar import *


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Link Review Submission'
        submission.cgi_script = 'linkreview'
        submission.type = MOD_REVIEW_LINK

        form = IsfdbFieldStorage()

        try:
                parent_id = form['Parent'].value
        except:
                submission.error('Valid title record must be specified')

        try:
                title_id = int(form['title_id'].value)
        except:
                submission.error('Valid review record must be specified')

        if not submission.user.id:
                submission.error('', title_id)

        try:
                # Drop everything to the left of the last question mark in case a title URL was entered
                parent_id = int(parent_id.split('?')[-1])
        except:
                submission.error('Title record number must be an integer')

        if title_id == parent_id:
                submission.error('Review record can not be linked to itself')

        if parent_id != 0:
                parent = SQLloadTitle(parent_id)
                if not parent:
                        submission.error('Title record does not exist')
        
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <LinkReview>\n"

        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))

        title = SQLloadTitle(int(title_id))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(title[TITLE_TITLE])))
        update_string += "    <Record>%d</Record>\n" % int(title_id)
        update_string += "    <Parent>%d</Parent>\n" % int(parent_id)
        if 'mod_note' in form:
                update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(form['mod_note'].value)))
        update_string += "  </LinkReview>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
