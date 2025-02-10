#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 939 $
#     Date: $Date: 2022-06-21 17:16:35 -0400 (Tue, 21 Jun 2022) $


from SQLparsing import *
from common import *
from library import *
from login import *


if __name__ == '__main__':

        publisher_id = SESSION.Parameter(0, 'int')
        publisher = SQLgetPublisherName(publisher_id)
        if not publisher:
                SESSION.DisplayError('Specified Publisher Does Not Exist')
        year = SESSION.Parameter(1, 'int')
        show_covers = SESSION.Parameter(2, 'int', 0, (0, 1))

        display_year = year
        if year == 0:
                display_year = '0000'

        title = "Publisher %s: Books Published in %s" % (publisher, ISFDBconvertYear(display_year))

        PrintHeader(title)
        PrintNavbar('publisheryear', publisher_id, publisher_id, 'publisheryear.cgi', 0)
        pubs = SQLGetPubsByPublisherYear(publisher_id, year)
        if show_covers:
                print ISFDBLinkNoName('publisheryear.cgi', '%d+%d' % (publisher_id, year), 'View publication list for this year')
                print SESSION.ui.bullet
                print ISFDBLinkNoName('publisher.cgi', publisher_id, 'Return to the publisher page')
                print '<p>'
                count = 0
                for pub in pubs:
                        if pub[PUB_IMAGE]:
                                print ISFDBScan(pub[PUB_PUBID], pub[PUB_IMAGE])
                                count += 1
                if not count:
                        print '<h3>No covers for %s</h3>' % year
                PrintTrailer('publisheryear', publisher_id, publisher_id)
                sys.exit(0)
        if len(pubs):
                print '<p>'
                print ISFDBLinkNoName('publisheryear.cgi', '%d+%d+1' % (publisher_id, year), 'View covers for this year')
                print SESSION.ui.bullet
                print ISFDBLinkNoName('publisher.cgi', publisher_id, 'Return to the publisher page')
                print '<p>'
                PrintPubsTable(pubs, 'publisher')

        PrintTrailer('publisheryear', publisher_id, publisher_id)
