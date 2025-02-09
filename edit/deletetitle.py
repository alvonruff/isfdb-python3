#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2021   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 666 $
#     Date: $Date: 2021-06-27 20:05:59 -0400 (Sun, 27 Jun 2021) $

	
from isfdb import *
from isfdblib import *
from SQLparsing import *
	
if __name__ == '__main__':

        title_id = SESSION.Parameter(0, 'int')
	
	titleRecord = SQLloadTitle(title_id)
	if not titleRecord:
                SESSION.DisplayError('Record Does Not Exist')

	PrintPreSearch('Delete Title Submission')
	PrintNavBar('edit/deletetitle.cgi', title_id)

	# Find pubs that refer to this title
	pubs = SQLGetPubsByTitle(title_id)

	# Find any variants that refer to this title
	variants = SQLgetTitleVariants(title_id)

	# Find any awards that refer to this title
	awards = SQLTitleAwards(title_id)

	if pubs:
		print '<h2>Error: %d publications still refer to this title:</h2>' % len(pubs)
		print '<ul>'
		for pub in pubs:
			print '<li>'
                        print '%s (%s)' % (ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE]), pub[PUB_YEAR])
		print '</ul>'

        if variants:
		print '<h2>Error: %d variant titles still refer to this parent title:</h2>' % len(variants)
		print '<ul>'
		for variant in variants:
			print '<li>'
                        print '%s (%s)' % (ISFDBLink('title.cgi', variant[TITLE_PUBID], variant[TITLE_TITLE]), variant[TITLE_YEAR])
		print '</ul>'

        if awards:
		print '<h2>Error: %d awards still refer to this title</h2>' % len(awards)

	if not pubs and not variants and not awards:
		titlename = SQLgetTitle(title_id)
		print '<b>Request to Delete:</b> <i>%s</i>' % titlename
		print '<form METHOD="POST" ACTION="/cgi-bin/edit/submitdeltitle.cgi">'
		print '<p>'
		print '<b>Deletion Reason</b><br>'
		print '<textarea name="reason" rows="4" cols="45"></textarea>'
		print '<p>'
		print '<input name="title_id" value="%d" type="HIDDEN">' % title_id
		print '<input type="SUBMIT" value="Delete">'
		print '</form>'
	
	PrintPostSearch(0, 0, 0, 0, 0, 0)
