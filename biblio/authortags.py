#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus
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

        author_id = SESSION.Parameter(0, 'int')
        author_data = SQLloadAuthorData(author_id)
        if not author_data:
                SESSION.DisplayError('Author Does Not Exist')
        author_name = author_data[AUTHOR_CANONICAL]

        PrintHeader('All Tags for %s' % author_name)
        PrintNavbar('authortags', 0, 0, 'authortags.cgi', author_id)

        # Determine the current user
        (userid, username, usertoken) = GetUserData()

        tags = SQLgetAuthorTags(author_id, int(userid))
        if not tags:
                print('<h3>No tags for author %s</h3>' % author_name)
        else:
                print_string = ''
                count = 0
                for tag in tags:
                        if count:
                                print_string += ', '
                        print_string += '%s (%d)' % (ISFDBLink('tag_author.cgi', '%d+%d' % (tag[0], author_id), tag[1]), tag[2])
                        count += 1
                print(print_string)

        print('<p><b>Back to the Summary Bibliography page for %s</b>' % ISFDBLink('ea.cgi', author_id, author_name))

        PrintTrailer('authortags', author_id, author_id)
