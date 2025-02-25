#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended serieslication of such source code.
#
#     Version: $Revision: 713 $
#     Date: $Date: 2021-08-27 10:38:44 -0400 (Fri, 27 Aug 2021) $

        
import cgi
import sys
from isfdb import *
from isfdblib import *
from seriesClass import *
from SQLparsing import SQLaddTagToTitle, SQLDeteleOrphanTags
from login import *
from library import ISFDBLocalRedirect


if __name__ == '__main__':

        user = User()
        user.load()
        if not user.id:
                SESSION.DisplayError('You must be logged in to add tags')

        sys.stderr = sys.stdout
        form = IsfdbFieldStorage()

        try:
                title_id = int(form['title_id'].value)
        except:
                SESSION.DisplayError('Title ID not specified')

        tags = []
        counter = 1
        while counter < 100:
                key = "tag_name%d" % counter
                if key in form:
                        tag = form[key].value
                        # Strip off leading and trailing spaces. Normally it happens
                        # in XMLescape when a submission is created. However, title tags
                        # are filed into the database directly and do not go through the
                        # standard submission process, so we need to strip spaces directly.
                        tag = str.strip(tag)
                        tag = str.rstrip(tag)
                        # Replace multiple adjacent spaces with single spaces
                        tag = ' '.join(tag.split())
                        # Only add the new tag to the list of tags if it's not already in the list
                        if tag not in tags:
                                tags.append(tag)
                counter += 1

        # Delete the old tags
        update = 'delete from tag_mapping where title_id=%d and user_id=%d' % (int(title_id), int(user.id))
        db.query(update)

        # Insert the new tags
        for tag in tags:
                result = SQLaddTagToTitle(tag, title_id, user.id)

        # Delete all old tags that are now without an associated entry in the tag_mapping table
        SQLDeteleOrphanTags()

        ISFDBLocalRedirect('title.cgi?%d' % int(title_id))
