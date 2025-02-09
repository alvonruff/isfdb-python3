#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 723 $
#     Date: $Date: 2021-08-30 12:47:45 -0400 (Mon, 30 Aug 2021) $


from SQLparsing import *
from biblio import *


if __name__ == '__main__':

        report_type = SESSION.Parameter(0, 'int', None, (0, 1, 2, 3, 4, 5, 6))
        if report_type == 0:
                author_type = 'Authors and Editors'
        elif report_type == 1:
                author_type = 'Novel Authors'
        elif report_type == 2:
                author_type = 'Short Fiction Authors'
        elif report_type == 3:
                author_type = 'Collection Authors'
        elif report_type == 4:
                author_type = 'Anthology Editors'
        elif report_type == 5:
                author_type = 'Non-Fiction Authors'
        elif report_type == 6:
                author_type = 'Other Title Types Authors'

	PrintHeader('%s Ranked by Awards and Nominations' % author_type)
	PrintNavbar('top', 0, 0, 'popular_authors_table.cgi', 0)

        print '<h3>%s</h3>' % ISFDBLinkNoName('popular_authors.cgi', '%d+all' % report_type, 'Highest Ranked %s of All Time' % author_type)
        print '<h3>%s</h3>' % ISFDBLinkNoName('popular_authors.cgi', '%d+pre1950' % report_type, 'Highest Ranked %s Prior to 1950' % author_type)

        print '<h3>Highest Ranked %s Since 1950 by Decade:</h3>' % author_type
        # Set the end decade to the decade of the current year
        endyear = localtime()[0]
        enddecade = endyear/10
        print '<ul>'
        for decade in range(195, enddecade+1):
                print '<li>%s' % ISFDBLinkNoName('popular_authors.cgi', '%d+decade+%d0' % (report_type, decade), '%d0s' % decade)
        print '</ul>'
	
	PrintTrailer('top', 0, 0)
