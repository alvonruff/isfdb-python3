#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1212 $
#     Date: $Date: 2025-01-22 16:00:18 -0500 (Wed, 22 Jan 2025) $


import sys
import os
import string
from SQLparsing import *
from common import *
from login import *


if __name__ == '__main__':

        publisher_id = SESSION.Parameter(0, 'int')
        publisher = SQLGetPublisher(publisher_id)
        if not publisher:
                SESSION.DisplayError('Specified Publisher Does Not Exist')

        user = User()
        user.load()
        
        title = 'Publisher: %s' % publisher[PUBLISHER_NAME]
        PrintHeader(title)
        PrintNavbar('publisher', publisher_id, publisher_id, 'publisher.cgi', publisher_id)

        print '<div class="ContentBox">'
        other_publishers = SQLGetDisambiguatedRecords(publisher_id, publisher[PUBLISHER_NAME], 'publishers', 'publisher_id', 'publisher_name')
        if other_publishers:
                print '<h3>Note: There are other publishers with the same name:'
                displayRecordList('publisher', other_publishers)
                print '</h3>'
        print '<ul>'
        # Transliterated name(s)
        trans_names = SQLloadTransPublisherNames(publisher_id)
        print '<li><b>Publisher: </b>%s' % ISFDBMouseover(trans_names, publisher[PUBLISHER_NAME], '')
        printRecordID('Publisher', publisher_id, user.id)

        # Webpages
        webpages = SQLloadPublisherWebpages(publisher_id)
        PrintWebPages(webpages)

        # Local Wiki Link
        if SQLwikiLinkExists('Publisher', publisher[PUBLISHER_NAME]):
                print "<li><b>Publisher Comments:</b>"
                publisher_name = 'Publisher:%s' % publisher[PUBLISHER_NAME]
                print '<a href="%s://%s/index.php/%s">%s</a>' % (PROTOCOL, WIKILOC, publisher_name, publisher_name)

        # Publisher Note
        if publisher[PUBLISHER_NOTE]:
                print '<li>'
                notes = SQLgetNotes(publisher[PUBLISHER_NOTE])
                print FormatNote(notes, 'Note', 'short', publisher_id, 'Publisher')

        print '</ul>'
        print '</div>'

        print '<div class="ContentBox">'
        print '<h3 class="contentheader">Publication series data</h3>'
        print '<ul class="unindent">'
        # Retrieve the count of this publisher's publications not in a publication series
        pubs_not_in_series = SQLCountPubsNotInPubSeries(publisher_id)
        if pubs_not_in_series:
                plural = ''
                if pubs_not_in_series > 1:
                        plural = 's'
                display = '%d publication%s not in a publication series' % (pubs_not_in_series, plural)
                if pubs_not_in_series > SESSION.max_displayable_pubs_without_pub_series:
                        display += ' (too many to display on one page)'
                else:
                        display = ISFDBLink('pubs_not_in_series.cgi', publisher_id, display)
                print '<li><b>%s</b>' % display

        # Retrieve all Publication Series IDs used by this publisher
        all_pub_series = SQLFindPubSeriesForPublisher(publisher_id)
        if all_pub_series:
                # Convert the list of series IDs into a comma-delimited string suitable for the SQL IN clause
                list_of_series = []
                for pub_series_id in all_pub_series:
                        list_of_series.append(str(pub_series_id[0]))
                list_of_series_as_string = ",".join(list_of_series)
                all_pub_series = SQLLoadPubSeries(list_of_series_as_string)
                for pub_series in all_pub_series:
                        print '<li>%s</li>' % ISFDBLink('pubseries.cgi', pub_series[PUB_SERIES_ID], pub_series[PUB_SERIES_NAME])
        print '</ul>'
        print '</div>'

        print '<div class="ContentBox">'
        print '<h3 class="contentheader">Years When Books Were Published</h3>'
        years = SQLGetPublisherYears(publisher_id)

        print '<table class="yearblock">'

        low_decade = 10000
        hi_decade  = 0
        for year in years:
                exception = ''
                if year == 0:
                        exception = 'unknown'

                if year == 8888:
                        exception = ISFDBunpublishedDate()

                if year == 9999:
                        exception = 'forthcoming'

                if exception:
                        print '<tr>'
                        print '<td colspan="10">%s</td>' % ISFDBLink("publisheryear.cgi", "%d+%s" % (publisher_id, year), exception)
                        print '</tr>'

                if (year != 0) and (year < 2100):
                        decade = 10*(int(year)/10)
                        if decade < low_decade:
                                low_decade = decade
                        if decade > hi_decade:
                                hi_decade = decade

        decade = low_decade
        while decade <= hi_decade:
                year = decade
                print '<tr>'
                while year < decade+10:
                        if year in years:
                                print '<td>%s</td>' % ISFDBLink("publisheryear.cgi", "%d+%s" % (publisher_id, year), year)
                        else:
                                print "<td>------</td>"
                        year += 1
                print "</tr>"
                decade += 10
        print '</table>'
        print '</div>'

        print '<div class="ContentBox">'
        print '<b>Publication Breakdown by Author:</b>'
        print '<ul>'
        print '<li>%s' % ISFDBLink('publisher_authors.cgi', '%d+name' % publisher_id, 'Sort by Author Name')
        print '<li>%s' % ISFDBLink('publisher_authors.cgi', '%d+count' % publisher_id, 'Sort by Publication Count')
        print '</ul>'
        print '</div>'

        PrintTrailer('publisher', publisher_id, publisher_id)
