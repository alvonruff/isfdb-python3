#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 730 $
#     Date: $Date: 2021-09-02 13:09:43 -0400 (Thu, 02 Sep 2021) $


import cgi
import sys
from SQLparsing import *
from isfdb import *
from isfdblib import *
from library import ISFDBLinkNoName, ISFDBLocalRedirect


def DoError(error, title_id):
        PrintPreSearch('Add Quick Tag')
        PrintNavBar('edit/addquicktag.cgi', 0)
        print('<h2>ERROR: %s</h2>' % error)
        if title_id:
                print('<br>%s' % ISFDBLinkNoName('title.cgi', title_id, 'View This Title', True))
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)


if __name__ == '__main__':

        (user_id, username, usertoken) = GetUserData()

        if not user_id:
                DoError('You must be logged in to tag titles', 0)

        sys.stderr = sys.stdout
        form = IsfdbFieldStorage()

        if 'title_id' in form:
                title_id = form['title_id'].value
        else:
                DoError('Specified title ID does not exit', 0)

        if 'tag' in form:
                new_tag = form['tag'].value
        else:
                DoError('No tag specified', 0)

        ##################################################################
        # Retrieve all tags for this user/Title ID combination
        ##################################################################
        tags = SQLgetUserTags(title_id, user_id)
        for tag in tags:
                if tag.lower() == new_tag.lower():
                        DoError('You have already added this Tag to this Title', title_id)

        result = SQLaddTagToTitle(new_tag, title_id, user_id)

        # Redirect the user back to the Title page
        ISFDBLocalRedirect('title.cgi?%d' % int(title_id))
