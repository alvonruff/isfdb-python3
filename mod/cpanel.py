#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 693 $
#     Date: $Date: 2021-08-09 17:10:16 -0400 (Mon, 09 Aug 2021) $


from isfdb import *
from isfdblib import PrintPreMod, PrintNavBar, PrintPostMod
from SQLparsing import *


if __name__ == '__main__':

        PrintPreMod('ISFDB Control Panel')
        PrintNavBar()

        query = "select * from metadata"
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        isfdb_version = record[0][0]
        DbOnline = record[0][2]
        EditOnline = record[0][3]

        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/mod/submitcpanel.cgi">'
        print '<p>'

        ###############################################################
        # VALUE 1 - ISFDB Version
        ###############################################################
        print '<b>ISFDB Version:</b>'
        print '<INPUT NAME="VERSION" SIZE=15 VALUE="%s">' % isfdb_version
        print '<hr>'

        ###############################################################
        # VALUE 2 - ISFDB Online/Offline
        ###############################################################
        print '<p><b>ISFDB Status:</b><br>'
        if DbOnline:
                print '<INPUT TYPE="radio" NAME="ONLINE" VALUE="1" CHECKED>'
                print '<b>Online</b><br>'
                print '<INPUT TYPE="radio" NAME="ONLINE" VALUE="0">'
                print '<b>Offline</b><br>'
        else:
                print '<INPUT TYPE="radio" NAME="ONLINE" VALUE="1">'
                print '<b>Online</b><br>'
                print '<INPUT TYPE="radio" NAME="ONLINE" VALUE="0" CHECKED>'
                print '<b>Offline</b><br>'
        print '<hr>'

        ###############################################################
        # VALUE 3 - Editing Online/Offline/Moderator
        ###############################################################
        print '<p><b>Editing Status:</b><br>'
        if EditOnline == 0:
                print '<INPUT TYPE="radio" NAME="EDITING" VALUE="0" CHECKED>'
                print '<b>Editing Offline</b><br>'
                print '<INPUT TYPE="radio" NAME="EDITING" VALUE="1">'
                print '<b>Public Editing</b><br>'
                print '<INPUT TYPE="radio" NAME="EDITING" VALUE="2">'
                print '<b>Moderator Editing Only</b><br>'
        elif EditOnline == 1:
                print '<INPUT TYPE="radio" NAME="EDITING" VALUE="0">'
                print '<b>Editing Offline</b><br>'
                print '<INPUT TYPE="radio" NAME="EDITING" VALUE="1" CHECKED>'
                print '<b>Public Editing</b><br>'
                print '<INPUT TYPE="radio" NAME="EDITING" VALUE="2">'
                print '<b>Moderator Editing Only</b><br>'
        elif EditOnline == 2:
                print '<INPUT TYPE="radio" NAME="EDITING" VALUE="0">'
                print '<b>Editing Offline</b><br>'
                print '<INPUT TYPE="radio" NAME="EDITING" VALUE="1">'
                print '<b>Public Editing</b><br>'
                print '<INPUT TYPE="radio" NAME="EDITING" VALUE="2" CHECKED>'
                print '<b>Moderator Editing Only</b><br>'

        print '<hr>'
        print '<p>'
        print '<input TYPE="SUBMIT" VALUE="Submit Data">'
        print '</form>'

        PrintPostMod(0)

