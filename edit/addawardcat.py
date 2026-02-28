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


from awardtypeClass import *
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from SQLparsing import *
from library import *
from isfdblib_print import printtextarea, printfield, printWebPages


if __name__ == '__main__':
        
        award_type_id = SESSION.Parameter(0, 'int')
        awardType = award_type()
        awardType.award_type_id = award_type_id
        awardType.load()
        if not awardType.award_type_name:
                SESSION.DisplayError('Specified Award Type ID Does Not Exist')

        PrintPreSearch('New Award Category for %s Award' % awardType.award_type_short_name)
        PrintNavBar('edit/addawardcat.cgi', award_type_id)

        print('<div id="HelpBox">')
        print('<b>Help on adding an award category: </b>')
        print('<a href="%s://%s/index.php/Help:Screen:AddAwardCat">Help:Screen:AddAwardCat</a><p>' % (PROTOCOL, WIKILOC))
        print('</div>')

        print('<form id="data" method="POST" action="/cgi-bin/edit/submitnewawardcat.cgi">')
        print('<table border="0">')
        print('<tbody id="tagBody">')

        help = HelpAwardCat()

        printfield("Award Category", "award_cat_name", help)

        printfield("Display Order", "award_cat_order", help)

        printWebPages([], 'award_cat', help)

        printtextarea('Note', 'award_cat_note', help)

        printtextarea('Note to Moderator', 'mod_note', help)

        print('</tbody>')
        print('</table>')
        print('<p>')

        print('<input name="award_cat_type_id" value="%d" type="HIDDEN">' % (award_type_id))
        print('<input type="SUBMIT" value="Submit New Award Category" tabindex="1">')
        print('</form>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)
