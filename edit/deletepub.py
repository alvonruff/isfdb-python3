#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 666 $
#     Date: $Date: 2021-06-27 20:05:59 -0400 (Sun, 27 Jun 2021) $

        
from isfdb import *
from isfdblib import *
from pubClass import *
from SQLparsing import *


if __name__ == '__main__':

        pub = pubs(db)
        pub.load(SESSION.Parameter(0, 'int'))
        if not pub.pub_title:
                SESSION.DisplayError('Record Does Not Exist')
        
        PrintPreSearch('Delete Publication')
        PrintNavBar('edit/deletepub.cgi', pub.pub_id)
        
        print '<b>Publication to Delete:</b> <i>%s</i>' % pub.pub_title
        print '<p>'
        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitdelpub.cgi">'
        print '<p>'
        print '<b>Note to Moderator:</b><br>'
        print '<textarea tabindex="1" name="mod_note" rows="4" cols="60"></textarea>'
        print '<p>'
        print '<input name="pub_id" value="%d" type="HIDDEN">' % pub.pub_id
        print '<input type="SUBMIT" value="Delete">'
        pub.printModNoteRequired()
        print '</form>'

        PrintPostSearch(tableclose=False)
