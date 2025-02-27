#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1062 $
#     Date: $Date: 2022-12-27 19:27:57 -0500 (Tue, 27 Dec 2022) $


import cgi
import sys
import string
import os
from isfdb import *
from SQLparsing import *
from common import *
from biblio import *
from library import normalizeInput, ISFDBLink, ISFDBText, ISFDBLocalRedirect
from isbn import *

##########################################################################################
# GENERAL SECTION
##########################################################################################

def validateYear(string):
        if PYTHONVER == 'python2':
                now = datetime.datetime.now()
        else:
                now = datetime.now()
        # Validate that the passed string is in the YYYY format
        error = "Year must be specified using the YYYY format"
        if len(string ) != 4:
                return (0, error)
        try:
                year=int(string)
                if (year < 1) or (year > (now.year +1)):
                        return (0, "Year must be YYYY between 0001 and one year in the future")
                return (year, '')

        except:
                return (0, error)

def PrintSummary(arg, count, limit, search_type, search_abbreviation):
        print("<p><b>A search for '%s' found %d matches. " % (ISFDBText(arg), count))
        if count >= limit:
                print("<br>The first %d matches are displayed below. Use " % (limit))
                print(ISFDBLink('adv_search_selection.cgi', search_abbreviation, 'Advanced %s Search' % search_type, False, 'class="inverted"'))
                print(" to see more matches.")
        print('</b>')
        print('<p>')

def PrintWholeWordNote():
        print("""Note that All Titles and Fiction Titles searches are now limited to
                complete words for performance reasons. If you want to search for a
                substring, e.g. 'kenstein' in 'Frankenstein', you will need to use
                %s.""" % ISFDBLink('adv_search_selection.cgi', 'title', 'Advanced Title Search', False, 'class="inverted"'))

def PrintGoogleSearch(arg, search_type):
        print('You can also try:')
        print('<form METHOD="GET" action="%s:/%s/google_search_redirect.cgi" accept-charset="utf-8">' % (PROTOCOL, HTFAKE))
        print('<p>')
        print('<select NAME="OPERATOR">')
        print('<option VALUE="exact">exact %s search' % search_type)
        print('<option SELECTED VALUE="approximate">approximate %s search' % search_type)
        print('</select>')
        print(' on <input NAME="SEARCH_VALUE" SIZE="50" VALUE="%s">' % ISFDBText(arg))
        print('<input NAME="PAGE_TYPE" VALUE="%s" TYPE="HIDDEN">' % search_type)
        print('<input TYPE="SUBMIT" VALUE="using Google">')
        print('</form>')

def PrintReplaceScript(script, value):
        ISFDBLocalRedirect('%s.cgi?%s' % (script, value))

def DoError(error, search_value, search_type):
        PrintHeader('ISFDB Search Error')
        PrintNavbar('search', '', 0, 'se.cgi', '', search_value, search_type)
        print('<h2>%s</h2>' % ISFDBText(error))
        PrintTrailer('search', '', 0)
        sys.exit(0)


##########################################################################################
# MAGAZINE SECTION
##########################################################################################

def PrintMagazineResults(results, arg):
        print("""<h3>Note: The search results displayed below include all series
                 AND magazine title records that match the entered value.
                 Matching magazines whose series titles do not match the
                 entered value have asterisks next to their titles.</h3>""")
        print('<table class="generic_table">')
        print('<tr class="generic_table_header">')
        print('<th>Magazine Series</th>')
        print('<th>Parent Series</th>')
        print('</tr>')

        bgcolor = 1
        counter = 0
        for title in sorted(results.keys(), key=lambda x: x.lower()):
                for series_id in results[title]:
                        parent_id = results[title][series_id][0]
                        series_title = results[title][series_id][1]
                        PrintMagazineRecord(title, series_id, parent_id, series_title, bgcolor, arg)
                        bgcolor ^= 1
                        counter += 1
                        if counter > 299:
                                break
                if counter > 299:
                        break
        print('</table>')

def PrintMagazineRecord(title, series_id, parent_id, series_title, bgcolor, arg):
        if bgcolor:
                print('<tr align=left class="table1">')
        else:
                print('<tr align=left class="table2">')

        print('<td>')
        print(ISFDBLink('pe.cgi', series_id, title))
        if title != series_title:
                print('*')
        print(ISFDBLink('seriesgrid.cgi', series_id, ' (issue grid)'))
        print('</td>')
        if parent_id:
                parent_title = SQLgetSeriesName(int(parent_id))
                print('<td>')
                print(ISFDBLink('pe.cgi', parent_id, parent_title))
                print(ISFDBLink('seriesgrid.cgi', parent_id, ' (issue grid)'))
                print('</td>')
        else:
                print('<td>-</td>')
        print('</tr>')

##########################################################################################
# PUBLISHER SECTION
##########################################################################################

def PrintPublisherResults(results,moderator):
        print('<table class="generic_table">')
        print('<tr class="generic_table_header">')
        if moderator:
                print('<th>Merge</th>')
        print('<th>Publisher</th>')
        print('</tr>')

        bgcolor = 1
        counter = 0
        for result in results:
                PrintPublisherRecord(result, bgcolor, moderator)
                bgcolor ^= 1
                counter += 1
                if counter > 299:
                        break
        print('</table>')

def PrintPublisherRecord(record, bgcolor, moderator):
        if bgcolor:
                print('<tr align=left class="table1">')
        else:
                print('<tr align=left class="table2">')

        if moderator:
                print('<td><INPUT TYPE="checkbox" NAME="merge" VALUE="%d"></td>' % (record[PUBLISHER_ID]))

        print('<td>%s</td>' % ISFDBLink('publisher.cgi', record[PUBLISHER_ID], record[PUBLISHER_NAME]))
        print('</tr>')


##########################################################################################
# PUBLICATION SERIES SECTION
##########################################################################################

def PrintPubSeriesResults(results):
        print('<table class="generic_table">')
        print('<tr class="generic_table_header">')
        print('<th>Publication Series</th>')
        print('</tr>')

        bgcolor = 1
        counter = 0
        for result in results:
                PrintPubSeriesRecord(result, bgcolor)
                bgcolor ^= 1
                counter += 1
                if counter > 299:
                        break
        print('</table>')

def PrintPubSeriesRecord(record, bgcolor):
        if bgcolor:
                print('<tr align=left class="table1">')
        else:
                print('<tr align=left class="table2">')

        print('<td>%s</td>' % ISFDBLink('pubseries.cgi', record[PUB_SERIES_ID], record[PUB_SERIES_NAME]))
        print('</tr>')


##########################################################################################
# TAG SECTION
##########################################################################################

def PrintTagResults(results):
        print('<table class="generic_table">')
        print('<tr class="generic_table_header">')
        print('<th>Tag Name</th>')
        print('<th>Private?</th>')
        print('</tr>')

        bgcolor = 1
        counter = 0
        for tag in results:
                PrintTagRecord(tag, bgcolor)
                bgcolor ^= 1
                counter += 1
                if counter > 299:
                        break
        print('</table>')

def PrintTagRecord(tag, bgcolor):
        if bgcolor:
                print('<tr align=left class="table1">')
        else:
                print('<tr align=left class="table2">')

        if tag[TAG_STATUS]:
                status = '<b>Private</b>'
        else:
                status = ''
        print('<td>%s</td>' % ISFDBLink('tag.cgi', tag[TAG_ID], tag[TAG_NAME]))
        print('<td>%s</td>' % (status))
        print('</tr>')

def LengthCheck(arg, record_name, search_type):
        # Check that the search string contains at least 2 non-wildcard characters
        if len(arg.replace('_','').replace('*','').replace('%','')) < 2:
                DoError('Regular search doesn\'t support single character searches for %s. Use Advanced Search instead.' % record_name, arg, search_type)


##########################################################################################
# MAIN SECTION
##########################################################################################

if __name__ == '__main__':

        form = IsfdbFieldStorage()
        try:
                mode = form['mode'].value
                if mode not in ('exact', 'contains'):
                        raise
        except:
                mode = 'contains'
        try:
                type = form['type'].value
                # Save the double-quote-escaped version of the original search value
                # to be re-displayed in the search box
                search_value = form['arg'].value.replace('"','&quot;')
                # Replace asterisks with % to facilitate wild cards
                arg = str.replace(normalizeInput(form['arg'].value), '*', '%')
                # Double escape backslashes, which is required by the SQL syntax
                arg = str.replace(arg, '\\', '\\\\')
                user = User()
                user.load()
                if not user.keep_spaces_in_searches:
                        arg = str.strip(arg)
                if not arg:
                        raise
        except:
                PrintHeader("ISFDB Search Error")
                PrintNavbar('search', '', 0, 'se.cgi', '')
                print("<h2>No search value specified</h2>")
                PrintTrailer('search', '', 0)
                sys.exit(0)

        if type[:4] == 'Name':
                LengthCheck(arg, 'names', type)
                results = SQLFindAuthors(arg, mode)
                if len(results) == 1:
                        PrintReplaceScript("ea", str(results[0][AUTHOR_ID]))
                else:
                        PrintHeader("ISFDB Name search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, len(results), 300, 'Author', 'author')
                        if results:
                                PrintAuthorTable(results, 0, 300)
                        else:
                                PrintGoogleSearch(arg, 'name')

        elif type[:14] == 'Fiction Titles':
                LengthCheck(arg, 'titles', type)
                results = SQLFindFictionTitles(arg)
                if len(results) == 1:
                        PrintReplaceScript("title", str(results[0][TITLE_PUBID]))
                else:
                        PrintHeader("ISFDB Fiction Title search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, len(results), 300, 'Title', 'title')
                        PrintWholeWordNote()
                        if results:
                                PrintTitleTable(results, 0, 300, user)
                        else:
                                PrintGoogleSearch(arg, 'title')

        elif type[:10] == 'All Titles':
                LengthCheck(arg, 'titles', type)
                results = SQLFindTitles(arg)
                if len(results) == 1:
                        PrintReplaceScript("title", str(results[0][TITLE_PUBID]))
                else:
                        PrintHeader("ISFDB Title search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, len(results), 300, 'Title', 'title')
                        PrintWholeWordNote()
                        if results:
                                PrintTitleTable(results, 0, 300, user)
                        else:
                                PrintGoogleSearch(arg, 'title')
        
        elif type[:13] == 'Year of Title':
                # Validate the passed in string and get the normalized year string
                (year, error) = validateYear(arg)
                if error:
                        DoError(error, search_value, type)
                results = SQLFindYear(year)
                if len(results) == 1:
                        PrintReplaceScript("title", str(results[0][TITLE_PUBID]))
                else:
                        PrintHeader("ISFDB Year of Title search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, len(results), 300, 'Title', 'title')
                        if results:
                                PrintTitleTable(results, 0, 300, user)

        elif type[:14] == 'Month of Title':
                # Validate the passed in string and get the normalized year and month data
                (year, month, error) = validateMonth(arg)
                if error:
                        DoError(error, search_value, type)
                if month < 10:
                        month = "0" + str(month)
                search_string = str(year) + '-' + str(month)
                results = SQLFindMonth(search_string)
                if len(results) == 1:
                        PrintReplaceScript("title", str(results[0][TITLE_PUBID]))
                else:
                        PrintHeader("ISFDB Month of Title search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, len(results), 300, 'Title', 'title')
                        if results:
                                PrintTitleTable(results, 0, 300, user)

        elif type[:20] == 'Month of Publication':
                # Validate the passed in string and get the normalized year and month data
                (year, month, error) = validateMonth(arg)
                if error:
                        DoError(error, search_value, type)
                # Redirect to the Forthcoming Book script
                PrintReplaceScript("fc", "date" + "+" + str(month) + "+" + str(year))

                        
        elif type[:6] == 'Series':
                results = SQLFindSeries(arg, mode)
                if len(results) == 1:
                        PrintReplaceScript("pe", str(results[0][SERIES_PUBID]))
                else:
                        PrintHeader("ISFDB Series search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, len(results), 300, 'Series', 'series')
                        if results:
                                PrintSeriesTable(results, 300)
                        else:
                                PrintGoogleSearch(arg, 'series')

        elif type[:8] == 'Magazine':
                (results, count) = SQLFindMagazine(arg)
                if count == 1:
                        for title in results:
                                for series_id in results[title]:
                                        PrintReplaceScript("pe", str(series_id))
                else:
                        PrintHeader("ISFDB Magazine search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, count, 300, 'Title', 'title')
                        if results:
                                PrintMagazineResults(results, arg)

        elif type[:9] == 'Publisher':
                LengthCheck(arg, 'publishers', type)
                (userid, username, usertoken) = GetUserData()
                moderator = 0
                results = SQLFindPublisher(arg, mode)

                if len(results) == 1:
                        PrintReplaceScript("publisher", str(results[0][PUBLISHER_ID]))
                else:
                        PrintHeader("ISFDB Publisher search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        if SQLisUserModerator(userid):
                                moderator = 1
                                print('<form METHOD="POST" ACTION="/cgi-bin/edit/pv_merge.cgi">')
                        PrintSummary(arg, len(results), 300, 'Publisher', 'publisher')
                        if results:
                                PrintPublisherResults(results, moderator)
                        else:
                                print('</form>')
                                PrintGoogleSearch(arg, 'publisher')

                if moderator and (len(results) > 1):
                        print('<p>')
                        print('<input TYPE="SUBMIT" VALUE="Merge Selected Records">')
                        print('</form>')

        elif type[:18] == 'Publication Series':
                results = SQLFindPubSeries(arg, mode)

                if len(results) == 1:
                        PrintReplaceScript("pubseries",str(results[0][PUB_SERIES_ID]))
                else:
                        PrintHeader("ISFDB Publication Series search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, len(results), 300, 'Publication Series', 'pub_series')
                        if results:
                                PrintPubSeriesResults(results)
                        else:
                                PrintGoogleSearch(arg, 'pubseries')

        elif type[:4] == 'ISBN':
                LengthCheck(arg, 'ISBNs', type)
                # Search for possible ISBN variations
                targets = isbnVariations(arg)
                results = SQLFindPubsByIsbn(targets)

                if len(results) == 1:
                        PrintReplaceScript("pl", str(results[0][PUB_PUBID]))
                else:
                        PrintHeader("ISFDB ISBN search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, len(results), 300, 'Publication', 'pub')
                        PrintPubsTable(results, "isbn_search")

        elif type[:3] == 'Tag':
                results = SQLsearchTags(arg)

                if len(results) == 1:
                        PrintReplaceScript("tag", str(results[0][TAG_ID]))
                else:
                        PrintHeader("ISFDB Tag search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, len(results), 300, 'Title', 'title')
                        if results:
                                PrintTagResults(results)

        elif type[:5] == 'Award':
                results = SQLSearchAwards(arg)
                if len(results) == 1:
                        PrintReplaceScript("awardtype", str(results[0][AWARD_TYPE_ID]))
                else:
                        PrintHeader("ISFDB Award search")
                        PrintNavbar('search', 0, 0, 0, 0, search_value, type)
                        PrintSummary(arg, len(results), 300, 'Award Type', 'award_type')
                        if results:
                                PrintAwardResults(results, 300)

        else:
                DoError('No search value specified', search_value, type)

        PrintTrailer('search', 0, 0)

