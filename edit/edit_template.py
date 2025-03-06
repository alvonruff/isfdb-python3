#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2022-2025   Ahasuerus, Al von Ruff
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
from SQLparsing import SQLisUserBureaucrat, SQLGetTemplate
from login import User


if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('The ability to edit templates is limited to ISFDB Bureaucrats')

        template_id = SESSION.Parameter(0, 'int')
        template = SQLGetTemplate(template_id)
        if not template_id:
                SESSION.DisplayError('Specified Template does not exist')

        PrintPreSearch('Edit ISFDB Template')
        PrintNavBar('edit/edit_template.cgi', 0)

        print("""Note that HTML entity references like "&amp;amp;" are curently automatically
                converted to their ASCII equivalents. See SVN Bug 514 for details.""")
        help = HelpTemplate()

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submit_edit_template.cgi">')
        print('<table border="0">')
        print('<tbody id="tagBody">')

        printfield('Name', 'template_name', help, template[TEMPLATE_NAME])

        printfield('Displayed Name', 'template_displayed_name', help, template[TEMPLATE_DISPLAYED_NAME])

        values = {}
        for template_type in ('External URL', 'Internal URL', 'Substitute String'):
                if template_type == template[TEMPLATE_TYPE]:
                        values[template_type] = 1
                else:
                        values[template_type] = 0
        printdropdown('Template Type', 'template_type', values, help)

        printfield('Link URL', 'template_url', help, template[TEMPLATE_URL])

        printfield('Mouseover Help', 'template_mouseover', help, template[TEMPLATE_MOUSEOVER])

        print('</table>')
        print('<p>')
        print('<input NAME="template_id" VALUE="%d" TYPE="HIDDEN">' % template_id)
        print('<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">')
        print('</form>')
        print('<p>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)

