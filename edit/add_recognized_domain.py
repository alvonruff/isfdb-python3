#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 91 $
#     Date: $Date: 2018-03-21 15:28:47 -0400 (Wed, 21 Mar 2018) $


from isfdb import *
from isfdblib import PrintPreSearch, PrintNavBar, PrintPostSearch
from isfdblib_help import HelpRecognizedDomain
from isfdblib_print import printfield, printdropdown
from login import User


if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('The ability to add recognized domains is limited to ISFDB Bureaucrats')

        PrintPreSearch('Add New Recognized Domain')
        PrintNavBar('edit/add_recognized_domain.cgi', 0)

        help = HelpRecognizedDomain()

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submit_add_recognized_domain.cgi">')
        print('<table border="0">')
        print('<tbody id="tagBody">')

        printfield('Domain Name', 'domain_name', help)

        printfield('Web Site Name', 'site_name', help)

        printfield('Web Site URL', 'site_url', help)

        values = {}
        values['Yes'] = 0
        values['No'] = 1
        printdropdown('Linking Allowed', 'linking_allowed', values, help)

        printfield('Required URL Segment', 'required_segment', help)

        values = {}
        values['Yes'] = 0
        values['No'] = 1
        printdropdown('Explicit Credit Page Link Required', 'explicit_link_required', values, help)

        print('</table>')
        print('<p>')
        print('<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">')
        print('</form>')
        print('<p>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)

