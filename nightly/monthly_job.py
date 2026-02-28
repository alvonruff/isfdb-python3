#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2026   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1261 $
#     Date: $Date: 2026-02-18 15:47:04 -0500 (Wed, 18 Feb 2026) $

from SQLparsing import *
from library import *
from dup_authors import *
from shared_cleanup_lib import *

if __name__ == '__main__':
        # Delete unresolved records for the duplicate authors report from the cleanup table
        query = 'delete from cleanup where resolved IS NULL and report_type = 9999'
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        dup_authors()
