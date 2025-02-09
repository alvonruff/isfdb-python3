#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2022   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended titlelication of such source code.
#
#     Version: $Revision: 968 $
#     Date: $Date: 2022-08-13 16:57:38 -0400 (Sat, 13 Aug 2022) $

	
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
        submission.header = 'Make Variant Title Submission'
        submission.cgi_script = 'mkvariant'
        submission.type = MOD_TITLE_MKVARIANT

	form = cgi.FieldStorage()

	try:
                # Drop everything to the left of the last question mark in case a title URL was entered
		parent_id = int(form['Parent'].value.split('?')[-1])
	except:
                submission.error('An integer parent number must be specified')

	try:
		title_id = int(form['title_id'].value)
	except:
                submission.error('An integer title number must be specified')

        if title_id == parent_id:
                submission.error('Title record can not be a variant of itself')

        if parent_id != 0:
                parent = SQLloadTitle(parent_id)
                if not parent:
                        submission.error('Parent title does not exist')
                if parent[TITLE_PARENT]:
                        submission.error('Proposed parent title is currently a variant of another title. Variants of variants are not allowed')

	if not submission.user.id:
                submission.error("", title_id)
	
	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <MakeVariant>\n"
	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))

	title = SQLloadTitle(title_id)
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(title[TITLE_TITLE])))
	update_string += "    <Record>%d</Record>\n" % (title_id)
	update_string += "    <Parent>%d</Parent>\n" % (parent_id)
	if form.has_key('mod_note'):
		update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(form['mod_note'].value)))
	update_string += "  </MakeVariant>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
