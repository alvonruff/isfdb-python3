#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2017-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1003 $
#     Date: $Date: 2022-09-15 14:36:33 -0400 (Thu, 15 Sep 2022) $


import cgi
from isfdb import *
from SQLparsing import *
from common import *
from login import User


##########################################################################################
# MAIN SECTION
##########################################################################################

if __name__ == '__main__':

        PrintHeader("ISFDB User Search")
        PrintNavbar('search', 0, 0, 0, 0)
        user = User()
        user.load()
        if not user.id:
                print('<h3>For performance reasons, Advanced Searches are currently restricted to registered users.</h3>')
                sys.exit(0)

        form = cgi.FieldStorage()
        try:
                user_name = form['USER_NAME'].value
                user_name = str.strip(user_name)
        except:
                print("<h2>No user name specified</h2>")
                PrintTrailer('search', '', 0)
                sys.exit(0)

        user_id = SQLgetSubmitterID(user_name, 0)
        if not user_id:
                print("<h2>Specified user name does not exist</h2>")
                PrintTrailer('search', '', 0)
                sys.exit(0)
        # Re-retrieve the user name in case the captilization is different
        user_name = SQLgetUserName(user_id)
        privileges = SQLUserPrivileges(user_id)

        print('<table>')
        print('<tr class="table1">')
        print('<th>User Name</th>')
        print('<th>Privileges</th>')
        print('<th>Last User Activity Date</th>')
        print('</tr>')
        print('<tr class="table2">')
        print('<td>%s</td>' % WikiLink(user_name))
        print('<td>%s</td>' % privileges)
        print('<td>%s</td>' % SQLLastUserActivity(user_id))
        print('</tr>')
        print('</table>')

        print('<p>')
        PrintTrailer('search', 0, 0)

