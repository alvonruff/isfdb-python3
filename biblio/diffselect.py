#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2022   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 901 $
#     Date: $Date: 2022-04-04 15:24:03 -0400 (Mon, 04 Apr 2022) $


from SQLparsing import *
from common import *
from library import *


if __name__ == '__main__':

        title_id = SESSION.Parameter(0, 'int')

	########################################
	# STEP 1 - Get the title record
	########################################
	title = SQLloadTitle(title_id)
	if not title:
        	SESSION.DisplayError('Title Record Does Not Exist')

	SQLupdateTitleViews(title_id)

        PrintHeader('Compare Publications for %s' % title[TITLE_TITLE])
	PrintNavbar('title', 0, title_id, 'title.cgi', title_id)
	if title[TITLE_TTYPE] == 'REVIEW':
		print "<b>Review of:</b>", title[TITLE_TITLE]
		authors = SQLReviewBriefAuthorRecords(title_id)
		if len(authors) > 1:
			print "<br><b>Book Authors:</b>"
		else:
			print "<br><b>Book Author:</b>"
		counter = 0
		for author in authors:
			if counter:
				print " <b>and</b> "
			displayAuthorById(author[0], author[1])
			counter += 1
	else:
		print "<b>Title:</b>", title[TITLE_TITLE]
	print "<br>"

	########################################
	# STEP 2 - Get the title's authors
	########################################
	authors = SQLTitleBriefAuthorRecords(title_id)
	if title[TITLE_TTYPE] == 'ANTHOLOGY':
		if len(authors) > 1:
			print "<b>Editors:</b>"
		else:
			print "<b>Editor:</b>"
	elif title[TITLE_TTYPE] == 'REVIEW':
		if len(authors) > 1:
			print "<b>Reviewers:</b>"
		else:
			print "<b>Reviewer:</b>"
	else:
		if len(authors) > 1:
			print "<b>Authors:</b>"
		else:
			print "<b>Author:</b>"
	counter = 0
	for author in authors:
		if counter:
			print " <b>and</b> "
		displayAuthorById(author[0], author[1])
		counter += 1
	print "<br>"

	print "<b>Date:</b>", ISFDBconvertDate(title[TITLE_YEAR], 1)

	if title[TITLE_TTYPE]:
		print "<br>"
		print "<b>Type:</b>", title[TITLE_TTYPE]


        print '<p><b>Select publications to compare:</b>'
        print '<p>'

	print '<form METHOD="POST" ACTION="/cgi-bin/submitdiff.cgi">'

	########################################
	# STEP 3 - Get the title's pub data
	########################################
	pubs = SQLGetPubsByTitle(title_id)
	PrintPubsTable(pubs, 'diffselect')

	print '<p>'
        print '<input type="SUBMIT" value="Submit Query">'
	print '<input name="title_id" value="%d" type="HIDDEN">' % (title_id)
	print '</form>'

	print '<p><hr><p>'
	PrintTrailer('title', title_id, title_id)
