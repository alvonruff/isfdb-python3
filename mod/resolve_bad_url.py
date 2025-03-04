#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 713 $
#     Date: $Date: 2021-08-27 10:38:44 -0400 (Fri, 27 Aug 2021) $

from isfdb import *
from SQLparsing import *
from library import ISFDBLocalRedirect
from login import User

        
if __name__ == '__main__':

        pub_id = SESSION.Parameter(0, 'int')

        user = User()
        user.load()
        user.load_moderator_flag()
        if not user.moderator:
                SESSION.DisplayError('Only Moderators Can Resolve Bad URLs')

        update = 'delete from bad_images where pub_id=%d' % pub_id
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)
        ISFDBLocalRedirect('mod/bad_images.cgi')
