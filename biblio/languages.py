#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 474 $
#     Date: $Date: 2019-10-26 17:34:10 -0400 (Sat, 26 Oct 2019) $


from isfdb import *
from common import PrintHeader, PrintNavbar, PrintTrailer
from library import ISFDBTable, ISFDBText
from SQLparsing import SQLLoadFullLanguages

PrintHeader('ISFDB-Supported Languages')
PrintNavbar('languages', 0, 0, 'languages.cgi', 0)

print('<h4>ISFDB supports the following subset of <a href="https://www.loc.gov/standards/iso639-2/php/code_list.php">ISO 639-2-recognized</a> languages</h4>')

table = ISFDBTable()
table.headers.extend(['Name', 'ISO 639-2 Code', 'Supports Latin-Derived Script'])
table.row_align = 'left'
languages = SQLLoadFullLanguages()
for language in languages:
        if language[LANGUAGE_LATIN_SCRIPT] == 'No':
                script = 'No'
        else:
                script = 'Yes'
        table.rows.append((ISFDBText(language[LANGUAGE_NAME]), ISFDBText(language[LANGUAGE_CODE]), ISFDBText(script)), )
table.PrintTable()

PrintTrailer('languages', 0, 0)
