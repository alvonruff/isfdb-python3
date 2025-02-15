#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 664 $
#     Date: $Date: 2021-06-27 14:13:38 -0400 (Sun, 27 Jun 2021) $

        
from isfdb import *
from isfdblib import *
from awardtypeClass import *
from SQLparsing import *
        
if __name__ == '__main__':

        (userid, username, usertoken) = GetUserData()
        if not SQLisUserModerator(userid):
                SESSION.DisplayError('Award Type Deletion Is Limited to Moderators')

        awardType = award_type()
        awardType.award_type_id = SESSION.Parameter(0, 'int')
        awardType.load()
        if not awardType.award_type_name:
                SESSION.DisplayError('Record Does Not Exist')
        
        PrintPreSearch('Delete Award Type')
        PrintNavBar('edit/deleteawardtype.cgi', awardType.award_type_id)

        # Check if there are any awards or award categories for this award type
        awards = SQLGetAwardYears(awardType.award_type_id)
        award_cats = SQLGetAwardCategories(awardType.award_type_id)
        if awards or award_cats:
                if awards:
                        print('<h2>Error: Award records for %d years still on file for this award type</h2>' % (len(awards)))
                if award_cats:
                        print('<h2>Error: %d award categories still on file for this award type</h2>' % (len(award_cats)))
                print('<h2>*** Cannot delete this award type</h2>')
        else:
                print('<b>Request to Delete:</b> <i>%s</i>' % awardType.award_type_name)

                print('<form METHOD="POST" ACTION="/cgi-bin/edit/submitdeleteawardtype.cgi">')
                print('<p>')
                print('<b>Deletion Reason</b><br>')
                print('<textarea name="reason" rows="4" cols="45"></textarea>')
                print('<p>')
                print('<input name="award_type_id" value="%d" type="HIDDEN">' % awardType.award_type_id)
                print('<input type="SUBMIT" value="Delete">')
                print('</form>')
        
        PrintPostSearch(0, 0, 0, 0, 0, 0)
