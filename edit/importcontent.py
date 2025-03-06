#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2008-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 735 $
#     Date: $Date: 2021-09-06 16:25:55 -0400 (Mon, 06 Sep 2021) $


from isfdb import *
from isfdblib import *
from isfdblib_print import *
from library import *


if __name__ == '__main__':

        pub_id = SESSION.Parameter(0, 'int')
        pub_data = SQLGetPubById(pub_id)
        if not pub_data:
                SESSION.DisplayError('Record Does Not Exist')

        PrintPreSearch('Import Content - %s' % pub_data[PUB_TITLE])
        PrintNavBar('edit/importcontent.cgi', pub_id)

        print('<div id="HelpBox">')
        print('<a href="%s://%s/index.php/Help:Screen:ImportContent">Help on importing content</a><p>' % (PROTOCOL, WIKILOC))
        print('</div>')

        print('<hr class="divider">')
        print('<p>')
        print('<h2>Option 1</h2>')
        print('<p>')

        print("Enter the publication ID/record number you would like to import from:")

        print('<form class="topspace" id="data" METHOD="POST" ACTION="/cgi-bin/edit/clonecontent.cgi">')
        print('<table>')
        
        printfield('Import From', 'ExportFrom')

        print('<tr>')
        print('<td><b>Include COVERART title(s)?</b></td>')
        print('<td><input type="checkbox" NAME="IncludeCoverArt" value="on" checked></td>')
        print('</tr>')
        
        print('<tr>')
        print('<td><b>Include INTERIORART titles?</b></td>')
        print('<td><input type="checkbox" NAME="IncludeInteriorArt" value="on" checked></td>')
        print('</tr>')

        print('<tr>')
        print('<td><b>Include page numbers?</b></td>')
        print('<td><input type="checkbox" NAME="IncludePages" value="on" checked></td>')
        print('</tr>')
        print('</table>')
        print('<p>')
        
        print('<input NAME="ExportTo" VALUE="%d" TYPE="HIDDEN">' % pub_id)
        print('<input TYPE="SUBMIT" VALUE="Import Content">')
        print('</form>')

        print('<hr class="divider">')
        print('<p>')
        print('<h2>Option 2</h2>')
        print('<p>')

        print('<p>Enter the title ID(s) you would like to import:')

        print('<form class="topspace" id="singledata" METHOD="POST" ACTION="/cgi-bin/edit/clonecontent.cgi">')
        print('<table>')
        printmultiple([], "Title", "ImportTitles")
        print('</table>')
        print('<p>')
        print('<input NAME="ExportTo" VALUE="%d" TYPE="HIDDEN">' % pub_id)
        print('<input TYPE="SUBMIT" VALUE="Import Titles">')
        print('</form>')

        PrintPostSearch(tableclose=False)
