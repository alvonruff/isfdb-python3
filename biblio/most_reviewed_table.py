#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2013-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


from SQLparsing import *
from common import *


if __name__ == '__main__':
        PrintHeader('Most-Reviewed Titles')
        PrintNavbar('top', 0, 0, 'most_reviewed_table.cgi', 0)

        print('<h3>%s</h3>' % ISFDBLinkNoName('most_reviewed.cgi', 'all', 'Most-Reviewed Titles of All Time'))
        print('<h3>%s</h3>' % ISFDBLinkNoName('most_reviewed.cgi', 'pre1900', 'Most-Reviewed Titles Prior to 1900'))

        print('<h3>Most-Reviewed Titles Since 1900 by Decade and Year</h3>')
        print('<table class="seriesgrid">')
        print('<tr>')
        print('<th>Decade</th>')
        print('<th colspan="10">Years</th>')
        print('</tr>')
        PrintAnnualGrid(1900, 'most_reviewed', 'year+', 1, 'decade+')

        PrintTrailer('top', 0, 0)
