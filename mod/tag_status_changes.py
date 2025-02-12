#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 17 $
#     Date: $Date: 2017-10-31 18:57:31 -0400 (Tue, 31 Oct 2017) $


from SQLparsing import *
from isfdblib import PrintPreMod, PrintNavBar, PrintPostMod
from library import ISFDBTable, ISFDBLink, WikiLink

def PrintTable(tags):
        table = ISFDBTable()
        table.row_align = 'left'
        table.headers.extend(['Tag', 'Moderator', 'New Status', 'Date/Time'])
        for tag in tags:
                tag_id = tag[0]
                tag_name = tag[1]
                numeric_status = tag[2]
                if numeric_status:
                        updated_status = 'Private'
                else:
                        updated_status = 'Public'
                timestamp = tag[3]
                user_name = tag[4]
                table.rows.append((ISFDBLink('tag.cgi', tag_id, tag_name), WikiLink(user_name), updated_status, timestamp))
        table.PrintTable()

if __name__ == '__main__':

        PrintPreMod('Tag Status Changes')
        PrintNavBar()

        tags = SQLLoadTagStatusChanges()
        if tags:
                PrintTable(tags)
        else:
                print '<h3>There are no tag status changes on file.</h3>'
        PrintPostMod(0)


