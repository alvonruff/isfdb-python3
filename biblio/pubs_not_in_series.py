#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2016-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


from SQLparsing import *
from common import *


if __name__ == '__main__':
        publisher_id = SESSION.Parameter(0, 'int')
        publisher = SQLGetPublisher(publisher_id)
        if not publisher:
                SESSION.DisplayError('Publisher not found')
        display_mode = SESSION.Parameter(1, 'int', 0, (0, 1, 2))

        title = 'Publications not in a Publication Series for Publisher: %s' % publisher[PUBLISHER_NAME]
        PrintHeader(title)
        PrintNavbar('pubs_not_in_series', publisher_id, publisher_id, 'pubs_not_in_series.cgi', publisher_id)

        print(('Publications not in a Publication Series for Publisher: %s<p>' % ISFDBLink('publisher.cgi', publisher_id, publisher[PUBLISHER_NAME])))
        sort_order = 'ASC'
        if display_mode == 1:
                sort_order = 'DESC'
        pubs = SQLGetPubsNotInSeries(publisher_id, sort_order)
        if len(pubs) > SESSION.max_displayable_pubs_without_pub_series:
                print(('%d publications not in a publication series - too many to display on one page' % len(pubs)))
        elif display_mode == 0:
                print((ISFDBLinkNoName('pubs_not_in_series.cgi', '%d+1' % publisher_id, 'Show last year first')))
                print((SESSION.ui.bullet))
                print((ISFDBLinkNoName('pubs_not_in_series.cgi', '%d+2' % publisher_id, 'Show Covers')))
                print('<p>')
                PrintPubsTable(pubs, 'pubs_not_in_series')
        elif display_mode == 1:
                print((ISFDBLinkNoName('pubs_not_in_series.cgi', '%d+0' % publisher_id, 'Show earliest year first')))
                print((SESSION.ui.bullet))
                print((ISFDBLinkNoName('pubs_not_in_series.cgi', '%d+2' % publisher_id, 'Show Covers')))
                print('<p>')
                PrintPubsTable(pubs, 'pubs_not_in_series')
        elif display_mode == 2:
                print((ISFDBLinkNoName('pubs_not_in_series.cgi', '%d+0' % publisher_id, 'Show earliest year first')))
                print((SESSION.ui.bullet))
                print((ISFDBLinkNoName('pubs_not_in_series.cgi', '%d+1' % publisher_id, 'Show last year first')))
                print('<p>')
                count = 0
                for pub in pubs:
                        if pub[PUB_IMAGE]:
                                print((ISFDBScan(pub[PUB_PUBID], pub[PUB_IMAGE])))
                                count += 1
                if not count:
                        print('<h3>No covers to display</h3>')

        PrintTrailer('pubs_not_in_series', publisher_id, publisher_id)
