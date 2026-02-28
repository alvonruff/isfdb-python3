#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2011-2026   Bill Longley, Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


from common import *

if __name__ == '__main__':

        PrintHeader('Authors By Debut Year')
        PrintNavbar('authors_by_debut_year', 0, 0, 'authors_by_debut_year.cgi', 0)

        print(ISFDBLink('authors_by_debut_year.cgi', '0', 'Prior to 1900'))
        print('<table class="seriesgrid">')
        print('<tr>')
        print('<th colspan="10">Years</th>')
        print('</tr>')
        PrintAnnualGrid(1900, 'authors_by_debut_year', '', 0, '')
        PrintTrailer('frontpage', 0, 0)
