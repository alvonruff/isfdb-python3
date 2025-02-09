#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 723 $
#     Date: $Date: 2021-08-30 12:47:45 -0400 (Mon, 30 Aug 2021) $


from SQLparsing import *
from common import *


PrintHeader('Most-Reviewed Titles')
PrintNavbar('top', 0, 0, 'most_reviewed_table.cgi', 0)

print '<h3>%s</h3>' % ISFDBLinkNoName('most_reviewed.cgi', 'all', 'Most-Reviewed Titles of All Time')
print '<h3>%s</h3>' % ISFDBLinkNoName('most_reviewed.cgi', 'pre1900', 'Most-Reviewed Titles Prior to 1900')

print '<h3>Most-Reviewed Titles Since 1900 by Decade and Year</h3>'
print '<table class="seriesgrid">'
print '<tr>'
print '<th>Decade</th>'
print '<th colspan="10">Years</th>'
print '</tr>'
PrintAnnualGrid(1900, 'most_reviewed', 'year+', 1, 'decade+')

PrintTrailer('top', 0, 0)
