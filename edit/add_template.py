#!_PYTHONLOC
#
#     (C) COPYRIGHT 2022-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 91 $
#     Date: $Date: 2018-03-21 15:28:47 -0400 (Wed, 21 Mar 2018) $


from isfdb import *
from isfdblib import PrintPreSearch, PrintNavBar, PrintPostSearch
from isfdblib_help import HelpTemplate
from isfdblib_print import printfield, printdropdown
from login import User


if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('The ability to add ISFDB templates is limited to ISFDB Bureaucrats')

        PrintPreSearch('Add New ISFDB Template')
        PrintNavBar('edit/add_template.cgi', 0)

        help = HelpTemplate()

        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submit_add_template.cgi">'
        print '<table border="0">'
        print '<tbody id="tagBody">'

        printfield('Name', 'template_name', help)

        printfield('Displayed Name', 'template_displayed_name', help)

        values = {}
        values['External URL'] = 1
        values['Internal URL'] = 0
        values['Substitute String'] = 0
        printdropdown('Template Type', 'template_type', values, help)

        printfield('Link URL', 'template_url', help)

        printfield('Mouseover Help', 'template_mouseover', help)

        print '</table>'
        print '<p>'
        print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
        print '</form>'
        print '<p>'

        PrintPostSearch(0, 0, 0, 0, 0, 0)

