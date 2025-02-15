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
from library import ISFDBLink
from SQLparsing import SQLisUserBureaucrat, SQLGetRecognizedDomainByID
from recognizeddomainClass import RecognizedDomain
from login import User


if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('The ability to edit/delete recognized domains is limited to ISFDB Bureaucrats')

        domain_id = SESSION.Parameter(0, 'int')
        domain = RecognizedDomain()
        domain.load(domain_id)
        if domain.error:
                SESSION.DisplayError(domain.error)

        PrintPreSearch('Edit/Delete Recognized Domain')
        PrintNavBar('edit/edit_delete_recognized_domain.cgi', 0)

        help = HelpRecognizedDomain()

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submit_edit_recognized_domain.cgi">')
        print('<table border="0">')
        print('<tbody id="tagBody">')

        printfield('Domain Name', 'domain_name', help, domain.domain_name)

        printfield('Web Site Name', 'site_name', help, domain.site_name)

        printfield('Web Site URL', 'site_url', help, domain.site_url)

        values = {}
        if domain.linking_allowed:
                values['Yes'] = 1
                values['No'] = 0
        else:
                values['Yes'] = 0
                values['No'] = 1
        printdropdown('Linking Allowed', 'linking_allowed', values, help)

        printfield('Required URL Segment', 'required_segment', help, domain.required_segment)

        values = {}
        if domain.explicit_link_required:
                values['Yes'] = 1
                values['No'] = 0
        else:
                values['Yes'] = 0
                values['No'] = 1
        printdropdown('Explicit Credit Page Link Required', 'explicit_link_required', values, help)

        print('</table>')
        print('<p>')
        print(('<input NAME="domain_id" VALUE="%d" TYPE="HIDDEN">' % domain_id))
        print('<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">')
        print('</form>')
        print('<p>')
        print((ISFDBLink('edit/submit_delete_recognized_domain.cgi', domain_id, 'Delete This Recognized Domain')))

        PrintPostSearch(0, 0, 0, 0, 0, 0)

