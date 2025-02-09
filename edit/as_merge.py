#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2022   Al von Ruff, Bill Longley and Ahasuerus
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
from library import *
from isfdblib import *
from authorClass import *
from login import *
from SQLparsing import *

def DoColumn(column, tag, recno1, recno2):
	if form.has_key(column):
		value = form[column].value
		if value == '1':
			retval = "    <%s>%d</%s>\n" % (tag, int(recno1), tag)
		else:
			retval = "    <%s>%d</%s>\n" % (tag, int(recno2), tag)
		return retval
	else:
		return ""

if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Author Merge Submission'
        submission.cgi_script = 0
        submission.type = MOD_AUTHOR_MERGE

	form = cgi.FieldStorage()
	if form.has_key('record1'):
		recno1 = form['record1'].value
	else:
                submission.error('Could not extract record1 ID')

	if form.has_key('record2'):
		recno2 = form['record2'].value
	else:
                submission.error('Could not extract record2 ID')

	if not submission.user.id:
                submission.error()

        submission.user.load_moderator_flag()
        if not submission.user.moderator:
                submission.error('Only moderators can merge authors')

	if int(recno1) < int(recno2):
		targetID = int(recno1)
		deleteID = int(recno2)
	else:
		targetID = int(recno2)
		deleteID = int(recno1)

	author1 = authors(db)
	author1.load(int(recno1))
	author2 = authors(db)
	author2.load(int(recno2))

	merge_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	merge_string += "<IsfdbSubmission>\n"
	merge_string += "  <AuthorMerge>\n"
	merge_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
	merge_string += "    <Subject>%s/%s</Subject>\n" % (db.escape_string(XMLescape(author1.author_canonical)),db.escape_string(XMLescape(author2.author_canonical)))
	merge_string += "    <KeepId>%d</KeepId>\n" % (targetID)
	merge_string += "    <DropId>%d</DropId>\n" % (deleteID)

	merge_string += DoColumn('author_canonical',  'Canonical',  recno1, recno2)
	merge_string += DoColumn('author_legalname',  'Legalname',  recno1, recno2)
	merge_string += DoColumn('author_lastname',   'Familyname', recno1, recno2)
	merge_string += DoColumn('author_birthplace', 'Birthplace', recno1, recno2)
	merge_string += DoColumn('author_birthdate',  'Birthdate',  recno1, recno2)
	merge_string += DoColumn('author_deathdate',  'Deathdate',  recno1, recno2)
	merge_string += DoColumn('author_pseudos',    'Pseudos',    recno1, recno2)
	merge_string += DoColumn('author_image',      'Image',      recno1, recno2)
	merge_string += DoColumn('author_language',   'Language',   recno1, recno2)
	merge_string += DoColumn('author_note',       'Note',       recno1, recno2)

	merge_string += "  </AuthorMerge>\n"
	merge_string +=  "</IsfdbSubmission>\n"

	submission.file(merge_string)
