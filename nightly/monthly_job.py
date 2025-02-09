#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2022   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 879 $
#     Date: $Date: 2022-03-12 18:49:56 -0500 (Sat, 12 Mar 2022) $

from SQLparsing import *
from library import *
from dup_authors import *
from shared_cleanup_lib import *

if __name__ == '__main__':
        # Delete unresolved records for the duplicate authors report from the cleanup table
        query = 'delete from cleanup where resolved IS NULL and report_type = 9999'
        db.query(query)
        dup_authors()
