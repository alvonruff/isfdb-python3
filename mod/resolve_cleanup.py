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

        user = User()
        user.load()
        user.load_moderator_flag()
        if not user.moderator:
                SESSION.DisplayError('Only Moderators Can Resolve Cleanup Report Records')

        cleanup_id = SESSION.Parameter(0, 'int')
        # Mode 0 is "delete from the table"; mode 1 is "set the resolve flag"
        mode = SESSION.Parameter(1, 'int', None, (0, 1))
        report_number = SESSION.Parameter(2, 'int')
        return_location = 'cleanup_report.cgi?%d' % report_number

        if mode == 0:
                update = 'delete from cleanup where cleanup_id=%d' % cleanup_id
        else:
                update = 'update cleanup set resolved=1 where cleanup_id=%d' % cleanup_id
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)
        ISFDBLocalRedirect('edit/%s' % return_location)
