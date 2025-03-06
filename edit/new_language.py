#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


from isfdblib import *
from isfdblib_help import *
from isfdb import *
from SQLparsing import *
from isfdblib_print import *


if __name__ == '__main__':

        (userid, username, usertoken) = GetUserData()
        if SQLisUserBureaucrat(userid) == 0:
                SESSION.DisplayError('The ability to add new languages is limited to ISFDB Bureaucrats')

        PrintPreSearch('Add New Language')
        PrintNavBar('edit/new_language.cgi', 0)

        help = HelpLanguage()

        printHelpBox('Language', 'Language', 1)

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submit_new_language.cgi">')

        print('<table border="0">')
        print('<tbody id="tagBody">')

        printfield('Language Name', 'language_name', help)

        printfield('Language Code', 'language_code', help)

        values = {}
        values['No'] = 1
        values['Yes'] = ''
        printdropdown('Latin-Derived', 'language_latin', values, help)

        print('</table>')
        print('<p>')
        print('<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">')
        print('</form>')
        print('<p>')

        PrintPostSearch(0, 0, 0, 0, 0)

