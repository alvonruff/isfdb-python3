#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2020-2026   Ahasuerus, Al von Ruff
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

def PrintTable(tags, user):
        print('<table>')
        print('<tr>')
        print('<th>Tag</th>')
        print('<th>User</th>')
        print('<th>User Tags</th>')
        if user.bureaucrat:
                print('<th>Remove</th>')
        print('</tr>')
        bgcolor = 1
        for tag_data in tags:
                tag_id = tag_data[0]
                tag_name = tag_data[1]
                user_id = tag_data[2]
                tagmapping_id = tag_data[3]
                if bgcolor:
                        print('<tr align=left class="table1">')
                else:
                        print('<tr align=left class="table2">')
                print('<td>%s</td>' % ISFDBLink('tag.cgi', tag_id, tag_name))
                print('<td>%s</td>' % WikiLink(SQLgetUserName(user_id)))
                print('<td>%s</td>' % ISFDBLink('usertag.cgi', user_id, 'User Tags'))
                if user.bureaucrat:
                        print('<td>%s</td>' % ISFDBLink('/mod/remove_tag.cgi', tagmapping_id, 'Remove'))
                print('</tr>')
                bgcolor ^= 1
        print('</table>')

if __name__ == '__main__':

        title_id = SESSION.Parameter(0, 'int')
        title = SQLloadTitle(title_id)
        if not title:
                SESSION.DisplayError('Invalid Title Specified')

        PrintPreMod('Tag Breakdown by User')
        PrintNavBar()

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                print('Note that ISFDB bureaucrats can remove invalid tags. Requests should be posted on the Moderator Noticeboard.<p>')
        tags = SQLgetTitleTagsByUser(title[TITLE_PUBID])
        print('<b>Tags Associated with</b> %s:<p>' % ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE]))
        if tags:
                PrintTable(tags, user)
        else:
                print('<h3>There are no tags for the specified title. If this is a variant title, its parent may have tags associated with it.</h3>')
        PrintPostMod(0)


