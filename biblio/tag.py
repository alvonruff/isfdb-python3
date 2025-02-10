#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2025   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 715 $
#     Date: $Date: 2021-08-27 18:27:37 -0400 (Fri, 27 Aug 2021) $

from SQLparsing import *
from common import *
from library import *


if __name__ == '__main__':

        tag_id = SESSION.Parameter(0, 'int')
        start = SESSION.Parameter(1, 'int', 0)

        tag = SQLGetTagById(tag_id)
        if not tag:
                SESSION.DisplayError('Tag Does Not Exist')

        PrintHeader('Titles marked with tag %s' % (tag[TAG_NAME]))
        PrintNavbar('tag', 0, 0, 'tag.cgi', tag_id)

        current_user = User()
        current_user.load()
        current_user.load_moderator_flag()

        if tag[TAG_STATUS]:
                current_status = 'Private'
        else:
                current_status = 'Public'
        print "This tag is currently marked <b>%s</b>" % current_status
        if current_user.moderator:
                logging_added = '2021-08-12'
                print '<p>'
                changes = SQLgetTagStatusHistory(tag_id)
                if changes:
                        print '<b>Log of Tag Status Changes Since %s</b>' % logging_added
                        table = ISFDBTable()
                        table.headers.extend(['Moderator', 'New Status', 'Date/Time'])
                        for change in changes:
                                user_link = WikiLink(change[0])
                                numeric_status = change[1]
                                if numeric_status:
                                        updated_status = 'Private'
                                else:
                                        updated_status = 'Public'
                                timestamp = change[2]
                                table.rows.append((user_link, updated_status, timestamp))
                        table.PrintTable()
                        print '<br>'
                else:
                        print 'No Tag Status Changes Since %s' % logging_added
                if current_status == 'Private':
                        new_status = 'Public'
                else:
                        new_status = 'Private'
                print '<form METHOD="POST" ACTION="/cgi-bin/mod/change_tag_status.cgi">'
                print '<div>'
                print '<input name="new_status" value="%s" type="HIDDEN">' % new_status
                print '<input name="tag_id" value="%s" type="HIDDEN">' % tag_id
                print '<input type="SUBMIT" value="Change the status to %s">' % new_status
                print '</div>'
                print '</form>'

        print '<h3>Users of this Tag:</h3>'
        tag_users = SQLgetUsersForTag(tag_id)
        need_comma = 0
        for tag_user in tag_users:
                output = ''
                if need_comma:
                        output += ', '
                else:
                        need_comma = 1
                output += ISFDBLink('usertag.cgi', tag_user[0], tag_user[2])
                output += ' (%s)' % ISFDBLink('usertitles.cgi', '%d+%d' % (tag_user[0], tag_id), tag_user[1])
                print output

        print '<h3>Titles Marked With This Tag:</h3>'
        titles = SQLgetTitlesForTag(tag_id, start)
        PrintTitleTable(titles, 0, 100, current_user)

        if len(titles) > 100:
                print ISFDBLink('tag.cgi', '%d+%d' % (tag_id, start+100), 'Next page (%d - %d)' % (start+101, start+200))

        PrintTrailer('tag', tag_id, tag_id)
