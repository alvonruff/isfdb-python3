#!_PYTHONLOC
from __future__ import print_function
#        (C) COPYRIGHT 2008-2026   Al von Ruff and Ahasuerus
#                 ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1264 $
#         Date: $Date: 2026-02-21 11:58:41 -0500 (Sat, 21 Feb 2026) $

import cgi
import sys
import os
from SQLparsing import *

debug = 0


def trimpages(db, page_id):

        ###############################################################
        # Get every text revision associated with the page, and delete all but the latest 50.
        ###############################################################
        query = "select rev_text_id from mw_revision where rev_page = '%s' order by rev_id desc;" % (page_id)

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        result = REMOVE_THIS_LINE
        counter = 0
        record = CNX.DB_FETCHMANY()
        while record:
                if (counter > 50):
                        delete = "delete from mw_text where old_id='%d'" % (record[0][0])
                        print(delete)
                        if debug == 0:
                                CNX.DB_QUERY(delete)
                record = CNX.DB_FETCHMANY()
                counter += 1



if __name__ == '__main__':

        print("""This script has been disabled. It works for version 1.12 of the
                         MediaWiki software, but does not work for newer versions. It will
                         need to be rewritten before it can be reactivated.""")
        sys.exit(0)

##
##        ###############################################################
##        # Find every page in the wiki, and call trimpages() with its
##        # namespace and title
##        ###############################################################
##        #query = "select * from mw_page where page_namespace = 4 and page_title in ('Community_Portal', 'Help_desk', 'Moderator_noticeboard', 'Verification_requests')"
##        query = "select * from mw_page"
##        CNX = MYSQL_CONNECTOR()
##        CNX.DB_QUERY(query)
##        record = CNX.DB_FETCHMANY()
##        while record:
##                #print("Page ID: %s" % (record[0][0]))
##                trimpages(db, record[0][0])
##                record = CNX.DB_FETCHMANY()
##        db.close()
