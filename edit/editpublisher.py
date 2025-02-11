#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 667 $
#     Date: $Date: 2021-06-28 18:30:46 -0400 (Mon, 28 Jun 2021) $


from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *
from isfdb import *
from SQLparsing import *
from login import User


if __name__ == '__main__':

        publisherID = SESSION.Parameter(0, 'int')
        record = SQLGetPublisher(publisherID)
        if not record:
                SESSION.DisplayError('Record Does Not Exist')
                
        PrintPreSearch('Publisher Editor')
        PrintNavBar('edit/editpublisher.cgi', publisherID)

        help = HelpPublisher()

        printHelpBox('publisher', 'EditPublisher')

        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitpublisher.cgi">'

        print '<table border="0">'
        print '<tbody id="tagBody">'

        # Limit the ability to edit publisher names to moderators
        user = User()
        user.load()
        display_only = 1
        if SQLisUserModerator(user.id):
                display_only = 0
        printfield("Publisher Name", "publisher_name", help, record[PUBLISHER_NAME], display_only)

        trans_publisher_names = SQLloadTransPublisherNames(record[PUBLISHER_ID])
        printmultiple(trans_publisher_names, "Transliterated Name", "trans_publisher_names", help)

        webpages = SQLloadPublisherWebpages(record[PUBLISHER_ID])
        printWebPages(webpages, 'publisher', help)

        printtextarea('Note', 'publisher_note', help, SQLgetNotes(record[PUBLISHER_NOTE]))

        printtextarea('Note to Moderator', 'mod_note', help, '')

        print '</tbody>'
        print '</table>'

        print '<p>'
        print '<input NAME="publisher_id" VALUE="%d" TYPE="HIDDEN">' % publisherID
        print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
        print '</form>'
        print '<p>'

        PrintPostSearch(0, 0, 0, 0, 0, 0)

