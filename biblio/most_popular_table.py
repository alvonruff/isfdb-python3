#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus, Al von Ruff
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

        code = SESSION.Parameter(0, 'int', None, (0, 1, 2, 3, 4, 5, 6))
        if code == 0:
                title_type = 'Titles'
        elif code == 1:
                title_type = 'Novels'
        elif code == 2:
                title_type = 'Short Fiction'
        elif code == 3:
                title_type = 'Collections'
        elif code == 4:
                title_type = 'Anthologies'
        elif code == 5:
                title_type = 'Non-Fiction'
        elif code == 6:
                title_type = 'Other Title Types'

        PrintHeader('%s Ranked by Awards and Nominations' % title_type)
        PrintNavbar('top', 0, 0, 'most_reviewed.cgi', 0)

        print('<h3>%s</h3>' % ISFDBLinkNoName('most_popular.cgi', '%d+all' % code, 'Highest Ranked %s of All Time' % title_type))
        print('<h3>%s</h3>' % ISFDBLinkNoName('most_popular.cgi', '%d+pre1950' % code, 'Highest Ranked %s Prior to 1950' % title_type))

        print('<h3>Highest Ranked %s Since 1950 by Decade and Year</h3>' % title_type)
        print('<table class="seriesgrid">')
        print('<tr>')
        print('<th>Decade</th>')
        print('<th colspan="10">Years</th>')
        print('</tr>')
        # Get the current year based on system time
        current_year = localtime()[0]
        # Determine the current decade - Python division returns integers by default
        current_decade = current_year/10*10
        bgcolor = 0
        # Display all decades since 1950 in reverse chronological order
        for decade in range(current_decade, 1940, -10):
                print('<tr class="table%d">' % (bgcolor+1))
                print('<td>%s</td>' % ISFDBLinkNoName('most_popular.cgi', '%d+decade+%d' % (code, decade), '%ds' % decade))
                for year in range(decade, decade+10):
                        # Skip future years
                        if year > current_year:
                                print('<td>&nbsp;</td>')
                                continue
                        print('<td>%s</td>' % ISFDBLinkNoName('most_popular.cgi', '%d+year+%d' % (code, year), year))
                print('</tr>')
                bgcolor ^= 1
        print('</table>')
        
        PrintTrailer('top', 0, 0)

