#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 419 $
#     Date: $Date: 2019-05-15 10:54:53 -0400 (Wed, 15 May 2019) $


import sys
import string
from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from login import *

class Bureaucrat:
        def __init__(self):
                pass
        
        def display_options(self):
                PrintPreMod('Bureaucrat Menu')
                PrintNavBar()
                print('<ul>')
                print('<li>User Management')
                print('<ul>')
                print('<li>%s' % ISFDBLink('mod/self_approvers.cgi', '', 'Manage Self-Approvers'))
                print('<li>%s' % ISFDBLink('mod/web_api_users.cgi', '', 'Manage Web API Users'))
                print('</ul>')
                print('<li>Table Management')
                print('<ul>')
                print('<li>%s' % ISFDBLink('edit/new_language.cgi', '', 'Add a New Language'))
                print('<li>%s' % ISFDBLink('edit/newawardtype.cgi', '', 'Add a New Award Type'))
                print('</ul>')
                print('<li>Recognized Domains')
                print('<ul>')
                print('<li>%s' % ISFDBLink('mod/list_recognized_domains.cgi', '', 'List/Edit/Delete Recognized Domains'))
                print('<li>%s' % ISFDBLink('edit/add_recognized_domain.cgi', '', 'Add a New Recognized Domain'))
                print('</ul>')
                print('<li>Secondary Verification Sources')
                print('<ul>')
                print('<li>%s' % ISFDBLink('mod/list_verification_sources.cgi', '', 'List/Edit Verification Sources'))
                print('<li>%s' % ISFDBLink('edit/add_verification_source.cgi', '', 'Add a New Verification Source'))
                print('</ul>')
                print('<li>ISFDB Templates')
                print('<ul>')
                print('<li>%s' % ISFDBLink('mod/list_templates.cgi', '', 'List/Edit ISFDB Templates'))
                print('<li>%s' % ISFDBLink('edit/add_template.cgi', '', 'Add a New ISFDB Template'))
                print('</ul>')
                print('<li>%s' % ISFDBLink('mod/marque.cgi', '', 'Re-Calculate Marque (most viewed) Authors'))
                print('<li>%s' % ISFDBLink('mod/cpanel.cgi', '', 'Control Panel'))
                print('</ul>')
                print('<p>')

        
if __name__ == '__main__':
        bureaucrat = Bureaucrat()
        bureaucrat.display_options()
        PrintPostMod(0)
