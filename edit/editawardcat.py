#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1247 $
#     Date: $Date: 2026-02-09 10:25:26 -0500 (Mon, 09 Feb 2026) $


from awardcatClass import *
from isfdblib import *
from isfdblib_help import *
from isfdb import *
from SQLparsing import *
from isfdblib_print import *


if __name__ == '__main__':

        awardCat = award_cat()
        awardCat.award_cat_id = SESSION.Parameter(0, 'int')
        awardCat.load()
        if not awardCat.award_cat_name:
                SESSION.DisplayError('Record Does Not Exist')
                
        PrintPreSearch('Award Category Editor')
        PrintNavBar('edit/editawardcat.cgi', awardCat.award_cat_id)

        help = HelpAwardCat()

        printHelpBox('Award Category', 'AwardCat')

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitawardcat.cgi">')

        print('<table border="0">')
        print('<tbody id="tagBody">')

        printfield('Award Category',      'award_cat_name',     help, awardCat.award_cat_name)

        printfield('Display Order',       'award_cat_order',    help, awardCat.award_cat_order)

        printWebPages(awardCat.award_cat_webpages, 'award_cat', help)

        printtextarea('Note', 'award_cat_note', help, awardCat.award_cat_note)

        print('</table>')

        print('<p>')
        print('<input NAME="award_cat_type_id" VALUE="%d" TYPE="HIDDEN">' % awardCat.award_cat_type_id)
        print('<input NAME="award_cat_id" VALUE="%d" TYPE="HIDDEN">' % awardCat.award_cat_id)
        print('<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">')
        print('</form>')
        print('<p>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)

