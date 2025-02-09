#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 664 $
#     Date: $Date: 2021-06-27 14:13:38 -0400 (Sun, 27 Jun 2021) $

from isfdb import *
from isfdblib import *
from awardcatClass import *
from SQLparsing import *

if __name__ == '__main__':

        (userid, username, usertoken) = GetUserData()
        if not SQLisUserModerator(userid):
                SESSION.DisplayError('Award Category Deletion Is Limited to Moderators')
	awardCat = award_cat()
	awardCat.award_cat_id = SESSION.Parameter(0, 'int')
	awardCat.load()
	if not awardCat.award_cat_name:
		SESSION.DisplayError('Record Does Not Exist')

	PrintPreSearch('Delete Award Category')
	PrintNavBar('edit/deleteawardcat.cgi', awardCat.award_cat_id)

	# Check if there are any awards for this award category
	awards = SQLloadAwardsForCat(awardCat.award_cat_id, 1)
        if awards:
                print '<h2>Error: Award records for %d years still on file for this award category</h2>' % (len(awards))
                print '<h2>*** Cannot delete this award category</h2>'
        else:
		print '<b>Request to Delete:</b> <i>%s</i>' % awardCat.award_cat_name
		print '<form METHOD="POST" ACTION="/cgi-bin/edit/submitdeleteawardcat.cgi">'
		print '<p>'
		print '<b>Deletion Reason</b><br>'
		print '<textarea name="reason" rows="4" cols="45"></textarea>'
		print '<p>'
		print '<input name="award_cat_id" value="%d" type="HIDDEN">' % awardCat.award_cat_id
		print '<input type="SUBMIT" value="Delete">'
		print '</form>'
	
	PrintPostSearch(0, 0, 0, 0, 0, 0)
