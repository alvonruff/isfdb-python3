#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 91 $
#     Date: $Date: 2018-03-21 15:28:47 -0400 (Wed, 21 Mar 2018) $


from isfdb import *
from isfdblib import PrintPreSearch, PrintNavBar, PrintPostSearch
from isfdblib_help import HelpVerificationSource
from isfdblib_print import printfield
from SQLparsing import SQLisUserBureaucrat, SQLGetVerificationSource
from login import User


if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('The ability to edit verification sources is limited to ISFDB Bureaucrats')

        source_id = SESSION.Parameter(0, 'int')
        source = SQLGetVerificationSource(source_id)
        if not source:
                SESSION.DisplayError('Specified Verification Source does not exist')

        PrintPreSearch('Edit Verification Source')
        PrintNavBar('edit/edit_verification_source.cgi', 0)

        help = HelpVerificationSource()

        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submit_edit_verification_source.cgi">'
        print '<table border="0">'
        print '<tbody id="tagBody">'

        printfield('Source Label', 'source_label', help, source[REFERENCE_LABEL])

        printfield('Source Name', 'source_name', help, source[REFERENCE_NAME])

        printfield('Source URL', 'source_url', help, source[REFERENCE_URL])

        print '</table>'
        print '<p>'
        print '<input NAME="source_id" VALUE="%d" TYPE="HIDDEN">' % source_id
        print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
        print '</form>'
        print '<p>'

        PrintPostSearch(0, 0, 0, 0, 0, 0)

