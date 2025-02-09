#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023   Ahasuerus
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

class WebAPIUsers:
        def __init__(self):
                self.user = User()
                self.user.load()
        
        def display_current_web_api_users(self):
        	PrintPreMod('Manage Web API Users')
                PrintNavBar()

                web_api_users = SQLGetWebAPIUsers()
                print('Users who can currently create Web API submissions:')
                print('<ul>')
                if not web_api_users:
                        print('<li>None')
                else:
                        for web_api_user in web_api_users:
                                print('<li>%s' % WikiLink(web_api_user[1]))
                print('</ul>')
                print('<hr>')

        def display_entry_form(self):
                print('<form METHOD="GET" action="/cgi-bin/mod/web_api_users_file.cgi">')
                print('<p>')
                print('User Name (case sensitive): <input NAME="user_name" SIZE="50">')
                print('<select NAME="web_api_user">')
                print('<option SELECTED VALUE="0">not an authorized Web API user')
                print('<option VALUE="1">an authorized Web API user')
                print('</select>')
                print('<p>')
                print('<input TYPE="SUBMIT" VALUE="Submit">')
                print('</form>')
                print('<p>')

        
if __name__ == '__main__':
        web_api_users = WebAPIUsers()
        web_api_users.display_current_web_api_users()
        web_api_users.display_entry_form()
        PrintPostMod(0)
