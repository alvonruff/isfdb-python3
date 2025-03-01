#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended titlelication of such source code.
#
#     Version: $Revision: 972 $
#     Date: $Date: 2022-08-23 16:44:48 -0400 (Tue, 23 Aug 2022) $

        
import cgi
import sys
from isfdb import *
from isfdblib import *
from SQLparsing import *
from login import *
from library import *
        
        
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Remove Alternate Name Submission'
        submission.cgi_script = 'mkpseudo'
        submission.type = MOD_REMOVE_PSEUDO

        form = IsfdbFieldStorage()

        try:
                parent_id = int(form['parent_id'].value)
        except:
                submission.error('Valid parent record must be specified')

        try:
                author_id = int(form['author_id'].value)
        except:
                submission.error('Valid author record must be specified')

        author_data = SQLloadAuthorData(author_id)
        if not author_data:
                submission.error('Unknown author record')

        parent_data = SQLloadAuthorData(parent_id)
        if not parent_data:
                submission.error('Unknown parent author')

        if not submission.user.id:
                submission.error('', author_id)

        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <RemovePseud>\n"

        CNX = MYSQL_CONNECTOR()
        update_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(author_data[AUTHOR_CANONICAL])))
        update_string += "    <Record>%d</Record>\n" % (author_id)
        update_string += "    <Parent>%d</Parent>\n" % (parent_id)
        if 'mod_note' in form:
                update_string += "    <ModNote>%s</ModNote>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(form['mod_note'].value)))
        update_string += "  </RemovePseud>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
