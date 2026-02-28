#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2009-2026   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1247 $
#     Date: $Date: 2026-02-09 10:25:26 -0500 (Mon, 09 Feb 2026) $


import cgi
import sys
from isfdb import *
from isfdblib import *

if __name__ == '__main__':

        author_id = SESSION.Parameter(0, 'int')
        author = SQLloadAuthorData(author_id)
        if not author:
                SESSION.DisplayError('Record Does Not Exist')

        PrintPreSearch('Make/Remove Alternate Name - %s' % author[AUTHOR_CANONICAL])
        PrintNavBar('edit/mkpseudo.cgi', author_id)

        print('<div id="HelpBox">')
        print('<b>Help on creating alternate names: </b>')
        print('<a href="%s://%s/index.php/Help:Screen:MakeAlternateName">Help:Screen:MakeAlternateName</a><p>' % (PROTOCOL, WIKILOC))
        print('</div>')

        print('Making/removing alternate name for <b>%s</b>' % author[AUTHOR_CANONICAL])
        print('<br>')

        #Retrieve a list of current canonical authors for this alternate name
        parents = SQLgetActualFromPseudo(author_id)
        if parents:
                print('This name is currently labeled as an alternate name for the following author(s):')
                for count, parent in enumerate(parents):
                        parent_data = SQLgetAuthorData(parent[0])
                        print('<form id="data%d" METHOD="POST" ACTION="/cgi-bin/edit/submitrempseudo.cgi">' % count)
                        print('<table border="1">')
                        print('<tr>')
                        print('<td>')
                        print(ISFDBLink('ea.cgi', parent_data[AUTHOR_ID], parent[0]))
                        print('</td>')
                        print('<td>')
                        print('<input NAME="author_id" VALUE="%d" TYPE="HIDDEN">' % (author_id))
                        print('<input NAME="parent_id" VALUE="%s" TYPE="HIDDEN">' % (parent_data[AUTHOR_ID]))
                        print('<input TYPE="SUBMIT" VALUE="Remove">')
                        print('</td>')
                        print('</tr>')
                        print('<tr>')
                        print('<td>')
                        print('<b>Note to Moderator: </b>')
                        print('<br><TEXTAREA name="mod_note" ROWS=1 COLS=45></TEXTAREA>')
                        print('</td>')
                        print('</tr>')
                        print('</table>')
                        print('</form>')

        print('<p><hr class="divider">')

        ##################################################################
        # Section 1
        ##################################################################
        print('Enter the name or the record number of the new parent author below.')
        print('The author must already exist in the database.')

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitmkpseudo.cgi">')
        print('<p>')
        print('<b>Parent Record #:</b>  <INPUT NAME="ParentRec" SIZE=16>')
        print('<br><b>Parent Name:</b>  <INPUT NAME="ParentName" id="ParentName" SIZE=20>')
        print('<br><b>Note to Moderator: </b>')
        print('<br><TEXTAREA name="mod_note" ROWS=4 COLS=45></TEXTAREA>')
        print('<p>')
        print('<input NAME="author_id" VALUE="%d" TYPE="HIDDEN">' % author_id)
        print('<input TYPE="SUBMIT" VALUE="Submit Data">')
        print('</form>')

        print('<p>')
        print('<hr>')
        print('<p>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)
