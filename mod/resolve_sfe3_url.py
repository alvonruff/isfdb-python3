#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1260 $
#     Date: $Date: 2026-02-18 08:27:14 -0500 (Wed, 18 Feb 2026) $

from isfdb import *
from SQLparsing import *
from library import ISFDBLocalRedirect
from login import User


if __name__ == '__main__':

        url = SESSION.Parameter(0, 'str')

        user = User()
        user.load()
        user.load_moderator_flag()
        if not user.moderator:
                SESSION.DisplayError('Only Moderators Can Resolve SFE URLs')

        update = "update sfe3_authors set resolved=1 where url='%s'" % CNX.DB_ESCAPE_STRING(url)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)
        ISFDBLocalRedirect('edit/sfe3_authors.cgi')
