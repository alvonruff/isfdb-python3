#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2015-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 893 $
#     Date: $Date: 2022-03-25 14:03:59 -0400 (Fri, 25 Mar 2022) $


from isfdb import *
from isfdblib import *
from library import *


if __name__ == '__main__':

        pub_id = SESSION.Parameter(0, 'int')
        pub_data = SQLGetPubById(pub_id)
        if not pub_data:
                SESSION.DisplayError('Record Does Not Exist')

        PrintPreSearch('Clone Publication - %s' % pub_data[PUB_TITLE])
        PrintNavBar('edit/clonecover.cgi', pub_id)

        print('<div id="HelpBox">')
        print('<a href="%s://%s/index.php/Help:Screen:ClonePub">Help on cloning publications</a><p>' % (PROTOCOL, WIKILOC))
        print('</div>')

        print('<form class="topspace" id="data" METHOD="POST" ACTION="/cgi-bin/edit/clonepub.cgi">')
        print('<table>')
        pub_image = ISFDBHostCorrection(pub_data[PUB_IMAGE])
        if pub_image:
                print('<tr class="scan">')
                print('<td><b>Current image:</b></td>')
                if "|" in pub_image:
                        image = pub_image.split("|")[0]
                        link = pub_image.split("|")[1]
                else:
                        image = pub_image
                        link = pub_image
                print('<td><a href="%s"><img src="%s" alt="picture" class="scan"></a></td>' % (link, image))
                print('</tr>')

        print('<tr>')
        print('<td><b>Reuse COVERART title(s) and image URL?</b></td>')
        print('<td><input type="checkbox" NAME="ReuseCoverArt" value="on" checked></td>')
        print('</tr>')
        
        print('<tr>')
        print('<td><b>Reuse INTERIORART titles?</b></td>')
        print('<td><input type="checkbox" NAME="ReuseInteriorArt" value="on" checked></td>')
        print('</tr>')
        
        print('<tr>')
        print('<td><b>Reuse page numbers?</b></td>')
        print('<td><input type="checkbox" NAME="ReusePageNumbers" value="on" checked></td>')
        print('</tr>')

        print('<tr>')
        print('<td><b>Reuse external IDs?</b></td>')
        print('<td><input type="checkbox" NAME="ReuseExternalIDs" value="on"></td>')
        print('</tr>')

        print('</table>')
        print('<p>')
        print('<input NAME="CloneTo" VALUE="%d" TYPE="HIDDEN">' % pub_id)
        print('<input TYPE="SUBMIT" VALUE="Clone Publication">')
        print('</form>')

        PrintPostSearch(tableclose=False)
