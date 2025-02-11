#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 730 $
#     Date: $Date: 2021-09-02 13:09:43 -0400 (Thu, 02 Sep 2021) $


from isfdb import *
from isfdblib import *
from isfdblib_help import *
from SQLparsing import *
from library import *
from isfdblib_print import printAwardName


if __name__ == '__main__':
        
        title_id = SESSION.Parameter(0, 'int')
        if title_id:
                title = SQLloadTitle(title_id)
                if not title:
                        SESSION.DisplayError('Record Does Not Exist')

        PrintPreSearch('Award Type Selector')
        PrintNavBar('edit/select_award_type.cgi', title_id)

        help = HelpAward(0)

        print '<div id="HelpBox">'
        print '<b>Help on adding an award: </b>'
        print '<a href="%s://%s/index.php/Help:Screen:AddAward">Help:Screen:AddAward</a><p>' % (PROTOCOL, WIKILOC)
        print '</div>'

        print '<form method="POST" action="/cgi-bin/edit/submit_select_award_type.cgi">'
        print '<table border="0">'
        print '<tbody id="titleBody">'

        printAwardName('award_type_id', 'Award Name', help)

        print '</tbody>'
        print '</table>'
        print '<p>'

        print '<input name="title_id" value="%d" type="HIDDEN">' % title_id
        print '<input type="SUBMIT" value="Proceed to the Next Page" tabindex="1">'
        print '</form>'

        PrintPostSearch(0, 0, 0, 0, 0, 0)
