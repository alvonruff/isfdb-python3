#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 667 $
#     Date: $Date: 2021-06-28 18:30:46 -0400 (Mon, 28 Jun 2021) $


from isfdb import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *
from library import *
from SQLparsing import *


if __name__ == '__main__':


        series_number = SESSION.Parameter(0, 'int')
        series = SQLget1Series(series_number)
        if not series:
                SESSION.DisplayError('Record Does Not Exist')
        
        PrintPreSearch('Series Editor')
        PrintNavBar('edit/editseries.cgi', series_number)

        help = HelpSeries()

        printHelpBox('series', 'SeriesData')

        print("Note:")
        print("<ul>")
        print("<li>Changing the Name field changes the name of the series for all books currently in this series.")
        print("<li>Changing the Parent field does NOT change the name of the parent series.")
        print("<li>If the Parent exists, changing the Parent field relinks the Named series to that parent.")
        print("<li>If the Parent does not exist, a new Parent series will be created and the Named series will be linked to that parent.")
        print("</ul>")
        print("<hr>")
        print("<p>")

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitseries.cgi">')
        print('<table border="0">')
        print('<tbody id="tagBody">')

        # Display the series name
        printfield("Name", "series_name", help, series[SERIES_NAME])

        trans_series_names = SQLloadTransSeriesNames(series[SERIES_PUBID])
        printmultiple(trans_series_names, "Transliterated Name", "trans_series_names", help)

        # Display the name of this series' parent (if one exists)
        parent_series_name = ''
        if series[SERIES_PARENT]:
                parent_series = SQLget1Series(series[SERIES_PARENT])
                parent_series_name = parent_series[SERIES_NAME]
        printfield("Parent", "series_parent", help, parent_series_name)

        # Display this series' ordering position within its superseries
        printfield("Series Parent Position", "series_parentposition", help, series[SERIES_PARENT_POSITION])

        webpages = SQLloadSeriesWebpages(series[SERIES_PUBID])
        printWebPages(webpages, 'series', help)

        printtextarea('Note', 'series_note', help, SQLgetNotes(series[SERIES_NOTE]))

        printtextarea('Note to Moderator', 'mod_note', help, '')

        print('</tbody>')
        print('</table>')

        print('<p>')
        print('<hr>')
        print('<p>')
        print('<input NAME="series_id" VALUE="%d" TYPE="HIDDEN">' % series_number)
        print('<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">')
        print('</form>')
        print('<p>')
        print('<hr>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)
