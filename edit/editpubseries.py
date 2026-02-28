#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2010-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1247 $
#     Date: $Date: 2026-02-09 10:25:26 -0500 (Mon, 09 Feb 2026) $


from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *
from isfdb import *
from SQLparsing import *


if __name__ == '__main__':

        pub_series_id = SESSION.Parameter(0, 'int')
        record = SQLGetPubSeries(pub_series_id)
        if not record:
                SESSION.DisplayError('Record Does Not Exist')

        PrintPreSearch('Publication Series Editor')
        PrintNavBar('edit/editpubseries.cgi', pub_series_id)

        help = HelpPubSeries()

        printHelpBox('publication series', 'PublicationSeries')

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitpubseries.cgi">')

        print('<table border="0">')
        print('<tbody id="tagBody">')
        printfield("Pub. Series Name",  "pub_series_name",       help, record[PUB_SERIES_NAME])
        
        trans_pub_series_names = SQLloadTransPubSeriesNames(record[PUB_SERIES_ID])
        printmultiple(trans_pub_series_names, "Transliterated Name", "trans_pub_series_names", help)

        webpages = SQLloadPubSeriesWebpages(pub_series_id)
        printWebPages(webpages, 'pub_series', help)
        
        printtextarea('Note', 'pub_series_note', help, SQLgetNotes(record[PUB_SERIES_NOTE]))

        printtextarea('Note to Moderator', 'mod_note', help, '')

        print('</table>')

        print('<p>')
        print('<input NAME="pub_series_id" VALUE="%d" TYPE="HIDDEN">' % pub_series_id)
        print('<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">')
        print('</form>')
        print('<p>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)

