#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 474 $
#     Date: $Date: 2019-10-26 17:34:10 -0400 (Sat, 26 Oct 2019) $


from isfdb import *
from common import PrintHeader, PrintNavbar, PrintTrailer
from library import ISFDBLink, ISFDBTable
from SQLparsing import SQLGetRefDetails

if __name__ == '__main__':
        PrintHeader('ISFDB-Supported Secondary Verification Sources')
        PrintNavbar('verification_sources', 0, 0, 'verification_sources.cgi', 0)

        table = ISFDBTable()
        table.headers.extend(['Label', 'Name', 'URL'])
        table.row_align = 'left'
        sources = SQLGetRefDetails()
        for source in sources:
                link = '<a href="%s">%s</a>' % (source[REFERENCE_URL], source[REFERENCE_URL])
                table.rows.append((source[REFERENCE_LABEL], source[REFERENCE_NAME], link), )
        table.PrintTable()

        PrintTrailer('verification_sources', 0, 0)
