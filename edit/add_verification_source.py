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
from login import User


if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('The ability to add verification sources is limited to ISFDB Bureaucrats')

        PrintPreSearch('Add New Verification Source')
        PrintNavBar('edit/add_verification_source.cgi', 0)

        help = HelpVerificationSource()

        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submit_add_verification_source.cgi">'
        print '<table border="0">'
        print '<tbody id="tagBody">'

        printfield('Source Label', 'source_label', help)

        printfield('Source Name', 'source_name', help)

        printfield('Source URL', 'source_url', help)

        print '</table>'
        print '<p>'
        print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
        print '</form>'
        print '<p>'

        PrintPostSearch(0, 0, 0, 0, 0, 0)

