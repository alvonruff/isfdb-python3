#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Ahasuerus and Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 917 $
#     Date: $Date: 2022-05-15 17:54:21 -0400 (Sun, 15 May 2022) $


import sys
import string
from isfdb import *
from SQLparsing import *
from common import *
from login import User

class AdvancedUserSearch():
        
        def display_selection(self):
                PrintHeader('User Search')
                PrintNavbar('adv_user_search', 0, 0, 0, 0)
                user = User()
                user.load()
                if not user.id:
                        print('<h3>For performance reasons, Advanced Searches are currently restricted to registered users.</h3>')
                else:
                        self.print_user_search()
                PrintTrailer('adv_user_search', 0, 0)

        def print_user_search(self):
                print('<form METHOD="GET" action="%s:/%s/user_search_results.cgi">' % (PROTOCOL, HTFAKE))
                print('<p>')
                print('User Name: <input NAME="USER_NAME" SIZE="50">')
                print('<p>')
                print('<input TYPE="SUBMIT" VALUE="Submit Query">')
                print('</form>')

        
if __name__ == '__main__':
        search = AdvancedUserSearch()
        search.display_selection()
