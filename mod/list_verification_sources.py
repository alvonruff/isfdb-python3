#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 91 $
#     Date: $Date: 2018-03-21 15:28:47 -0400 (Wed, 21 Mar 2018) $


from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *


if __name__ == '__main__':

        PrintPreMod('Secondary Verification Sources')
        PrintNavBar()

        table = ISFDBTable()
        table.headers.extend(('Verification Source', ))
        table.row_align = 'left'

        sources = SQLGetRefDetails()
        for source in sources:
                source_id = source[REFERENCE_ID]
                source_label = source[REFERENCE_LABEL]
                table.rows.append((ISFDBLink('edit/edit_verification_source.cgi', source_id, source_label), ))

        table.PrintTable()

        PrintPostMod(0)

