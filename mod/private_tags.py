#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 17 $
#     Date: $Date: 2017-10-31 18:57:31 -0400 (Tue, 31 Oct 2017) $


from SQLparsing import *
from isfdblib import *
from library import *
from login import *

def PrintTable(tags):
        table = ISFDBTable()
        table.row_align = 'left'
        table.headers.extend(['Tag',])
        for tag in tags:
                tag_id = tag[0]
                tag_name = tag[1]
                table.rows.append((ISFDBLink('tag.cgi', tag_id, tag_name), ))
        table.PrintTable()

if __name__ == '__main__':

        PrintPreMod('Private Tags')
        PrintNavBar()

        tags = SQLLoadPrivateTags()
        if tags:
                print """<h3>If you notice a misspelled or otherwise malformed tag,
                             please post on the Moderator Noticeboard and a bureaucrat will remove it.</h3>"""
                PrintTable(tags)
        else:
                print '<h3>There are no private tags on file.</h3>'
	PrintPostMod(0)
