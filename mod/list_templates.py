#!_PYTHONLOC
#
#     (C) COPYRIGHT 2022-2025   Ahasuerus
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

        PrintPreMod('ISFDB Templates')
        PrintNavBar()

        table = ISFDBTable()
        table.headers.extend(('Template', ))
        table.row_align = 'left'

        templates = SQLLoadRawTemplates()
        for template in templates:
                template_id = template[TEMPLATE_ID]
                template_name = template[TEMPLATE_NAME]
                table.rows.append((ISFDBLink('edit/edit_template.cgi', template_id, template_name), ))

        table.PrintTable()

        PrintPostMod(0)

