#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2026   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1247 $
#     Date: $Date: 2026-02-09 10:25:26 -0500 (Mon, 09 Feb 2026) $


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

        print('<b>Request to Delete:</b> <i>%s</i>' % award[0][AWARD_TITLE])
        print('<form METHOD="POST" ACTION="/cgi-bin/edit/submitdelaward.cgi">')
        print('<p>')
        print('<b>Deletion Reason</b><br>')
        print('<textarea name="reason" rows="4" cols="45"></textarea>')
        print('<p>')
        print('<input name="award_id" value="%d" type="HIDDEN">' % award_id)
        print('<input type="SUBMIT" value="Delete">')
        print('</form>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)
