#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 717 $
#     Date: $Date: 2021-08-28 11:04:26 -0400 (Sat, 28 Aug 2021) $


from SQLparsing import *
from common import *
from login import *
from seriesClass import *


#########################################################
# printSeries is a recursive function that outputs the
# titles attached to the given series, then finds all
# of its children and calls itself with each child.
#########################################################
def printSeries(seriesData, seriesTitles, seriesTree, parentAuthors,
                variantTitles, variantSerials, parentsWithPubs,
                variantAuthors, translit_titles, translit_authors, ser, user):
        output = '<li>'
        if ser.series_parentposition > 0:
                output += '%s ' % ser.series_parentposition
        output += ISFDBLink('pe.cgi', ser.series_id, ser.series_name)
        print(output)
        magazine_found = 0
        for ser_id in seriesTitles:
                # If any of the Titles in this series or its sub-series is
                # an EDITOR title, display a link to the magazine's issue grid
                for title in seriesTitles[ser_id]:
                        if title[TITLE_TTYPE] == 'EDITOR':
                                print(ISFDBLink('seriesgrid.cgi', ser.series_id, ' (View Issue Grid)'))
                                magazine_found = 1
                                break
                if magazine_found:
                        break
        print("<ul>")
        if ser.series_id in seriesTitles:
                for title in seriesTitles[ser.series_id]:
                        # Display the series number
                        output = '<li>'
                        if title[TITLE_SERIESNUM] is not None:
                                output += '%s' % title[TITLE_SERIESNUM]
                        if title[TITLE_SERIESNUM_2] is not None:
                                output += '.%s' % title[TITLE_SERIESNUM_2]
                        print(output)
                        # The "non-genre" parameter is set to 0 because for series biblios the
                        # non-genre flag is always displayed
                        displayTitle(title, 0, parentAuthors, SERIES_TYPE_UNKNOWN, variantTitles,
                                     variantSerials, parentsWithPubs, variantAuthors, translit_titles,
                                     translit_authors, user)
        print("</ul>")

        children = seriesTree[ser.series_id]
        if children:
                print("<ul>")
                for child_id in children:
                        ser1 = seriesData[child_id]
                        printSeries(seriesData, seriesTitles, seriesTree, parentAuthors,
                                    variantTitles, variantSerials, parentsWithPubs,
                                    variantAuthors, translit_titles, translit_authors,
                                    ser1, user)
                print("</ul>")

if __name__ == '__main__':

        # Get the series parameter. May be a series name or a series record number.
        parameter = SESSION.Parameter(0, 'unescape')

        # Translate the series name to its series number if necessary
        try:
                series_id = int(parameter)
        except:
                series_id = 0
        
        if series_id:
                if not SQLFindSeriesName(series_id):
                        if SQLDeletedSeries(series_id):
                                SESSION.DisplayError('This series has been deleted. See %s for details' % ISFDBLink('series_history.cgi', series_id, 'Edit History'))
                        else:
                                SESSION.DisplayError('Specified Series Does Not Exist')
        else:
                series_id = SQLFindSeriesId(parameter)

        if not series_id:
                SESSION.DisplayError('Specified Series Does Not Exist')

        ser = series(db)
        ser.load(series_id)

        user = User()
        user.load()

        # Check if the user is not logged in and trying to change the default settings for translations
        if not user.id:
                default_value = user.display_all_languages
                translations = SESSION.Parameter(1, 'str', default_value, ('All', 'None'))
                if translations:
                        user.translation_cookies(translations)

        PrintHeader('Series: %s' % ser.series_name)
        PrintNavbar('series', series_id, 0, 'pe.cgi', ser.series_id)

        (seriesData, seriesTitles, seriesTree, parentAuthors,
         seriesTags, variantTitles, variantSerials, parentsWithPubs,
         variantAuthors, translit_titles, translit_authors) = ser.BuildTreeData(user)

        ser.PrintMetaData(user, 'brief', seriesTags, 'series')

        print('<div class="ContentBox">')
        if seriesData:
                print(user.translation_message('series', ser))
                # Traverse and print series tree
                print("<ul>")
                printSeries(seriesData, seriesTitles, seriesTree, parentAuthors,
                            variantTitles, variantSerials, parentsWithPubs,
                            variantAuthors, translit_titles, translit_authors,
                            ser, user)
                print("</ul>")
        else:
                print('<p><b>This series is empty and will be deleted.</b>')

        print('</div>')

        PrintTrailer('series', 0, 0)
