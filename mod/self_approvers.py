#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 419 $
#     Date: $Date: 2019-05-15 10:54:53 -0400 (Wed, 15 May 2019) $


from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from login import *

class SelfApprovers:
        def __init__(self):
                self.user = User()
                self.user.load()
        
        def display_current_self_approvers(self):
                PrintPreMod('Manage Self-Approvers')
                PrintNavBar()

                current_self_approvers = SQLGetSelfApprovers()
                print('Users who can currently approve their own submissions:')
                print('<ul>')
                if not current_self_approvers:
                        print('<li>None')
                else:
                        for self_approver in current_self_approvers:
                                print('<li>%s' % WikiLink(self_approver[1]))
                print('</ul>')
                print('<hr>')

        def display_entry_form(self):
                print('<form METHOD="GET" action="/cgi-bin/mod/self_approver_file.cgi">')
                print('<p>')
                print('User Name (case sensitive): <input NAME="user_name" SIZE="50">')
                print('<select NAME="self_approver">')
                print('<option SELECTED VALUE="0">not self-approver')
                print('<option VALUE="1">self-approver')
                print('</select>')
                print('<p>')
                print('<input TYPE="SUBMIT" VALUE="Submit">')
                print('</form>')
                print('<p>')

        
if __name__ == '__main__':
        self_approvers = SelfApprovers()
        self_approvers.display_current_self_approvers()
        self_approvers.display_entry_form()
        PrintPostMod(0)
