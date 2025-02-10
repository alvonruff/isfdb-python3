#!_PYTHONLOC
#
#     (C) COPYRIGHT 2010-2025   Ahasuerus, Bill Longley and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1212 $
#     Date: $Date: 2025-01-22 16:00:18 -0500 (Wed, 22 Jan 2025) $


from SQLparsing import *
from common import *
from login import *


if __name__ == '__main__':

        pub_series_id = SESSION.Parameter(0, 'int')
        pub_series = SQLGetPubSeries(pub_series_id)
        if not pub_series:
                SESSION.DisplayError('Publication series not found')

        messages = {0: 'Show earliest year first',
                    1: 'Show last year first',
                    2: 'Sort by series number',
                    3: 'Show covers'
                    }
        display_order = SESSION.Parameter(1, 'int', 0, (0, 1, 2, 3))

        user = User()
        user.load()

        title = 'Publication Series: %s' % pub_series[PUB_SERIES_NAME]
        PrintHeader(title)
        PrintNavbar('pub_series', pub_series_id, pub_series_id, 'pubseries.cgi', pub_series_id)

        print '<div class="ContentBox">'
        other_series = SQLGetDisambiguatedRecords(pub_series_id, pub_series[PUB_SERIES_NAME], 'pub_series', 'pub_series_id', 'pub_series_name')
        if other_series:
                print '<h3>Note: There are other publication series with the same name:'
                displayRecordList('pub_series', other_series)
                print '</h3>'
        print '<ul>'
        # Transliterated name(s)
        trans_names = SQLloadTransPubSeriesNames(pub_series_id)
        print '<li><b>Publication Series: </b>%s' % ISFDBMouseover(trans_names, pub_series[PUB_SERIES_NAME], '')
        printRecordID('Pub. Series', pub_series_id, user.id)

        # Webpages
        webpages = SQLloadPubSeriesWebpages(int(pub_series_id))
        PrintWebPages(webpages)

        # Note
        if pub_series[PUB_SERIES_NOTE]:
                print '<li>'
                notes = SQLgetNotes(pub_series[PUB_SERIES_NOTE])
                print FormatNote(notes, 'Note', 'short', pub_series_id, 'Pubseries')

        print '</ul>'
        print '</div>'

        print '<div class="ContentBox">'
        output = ''
        for message_number in sorted(messages.keys()):
                if message_number != display_order:
                        if output:
                                output += ' %s ' % SESSION.ui.bullet
                        output += ISFDBLinkNoName('pubseries.cgi', '%d+%d' % (int(pub_series_id), message_number), messages[message_number])
        print output,'<p>'
        if display_order == 3:
                pubs = SQLGetPubSeriesPubs(pub_series_id, 2)
                count = 0
                for pub in pubs:
                        if pub[PUB_IMAGE]:
                                print ISFDBScan(pub[PUB_PUBID], pub[PUB_IMAGE])
                                count += 1
                if not count:
                        print '<h3>No covers for %s</h3>' % pub_series[PUB_SERIES_NAME]
        else:
                pubs = SQLGetPubSeriesPubs(pub_series_id, display_order)
                PrintPubsTable(pubs, 'pubseries')
        print '</div>'

        PrintTrailer('pub_series', pub_series_id, pub_series_id)
