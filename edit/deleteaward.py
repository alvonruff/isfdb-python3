#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 664 $
#     Date: $Date: 2021-06-27 14:13:38 -0400 (Sun, 27 Jun 2021) $


from isfdb import *
from isfdblib import *
from awardClass import *
from SQLparsing import *
        

if __name__ == '__main__':

        award_id = SESSION.Parameter(0, 'int')
        award = SQLloadAwards(award_id)
        if not award:
                SESSION.DisplayError('Record Does Not Exist')

        PrintPreSearch('Delete Award Submission')
        PrintNavBar('edit/deleteaward.cgi', award_id)

        print '<b>Request to Delete:</b> <i>%s</i>' % award[0][AWARD_TITLE]
        print '<form METHOD="POST" ACTION="/cgi-bin/edit/submitdelaward.cgi">'
        print '<p>'
        print '<b>Deletion Reason</b><br>'
        print '<textarea name="reason" rows="4" cols="45"></textarea>'
        print '<p>'
        print '<input name="award_id" value="%d" type="HIDDEN">' % award_id
        print '<input type="SUBMIT" value="Delete">'
        print '</form>'

        PrintPostSearch(0, 0, 0, 0, 0, 0)
