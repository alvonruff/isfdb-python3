#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1.2 $
#         Date: $Date: 2014/09/10 20:20:28 $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        # First delete all old images that are associated with pubs that no longer exist
        delete = " delete from bad_images where not exists (select 1 from pubs where bad_images.pub_id=pubs.pub_id)"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(delete)
        
        # Open the flat file with bad image URLs and read in its content
        fd = open('BadImages')
        lines = fd.readlines()
        fd.close();
        for line in lines:
                oneline = line.strip()
                onelist = oneline.split(',')
                pubid = onelist[0]
                url = onelist[1]
                print(pubid, url)
                update = "insert into bad_images (pub_id, image_url) values(%d,'%s')" % (int(pubid), CNX.DB_ESCAPE_STRING(url))
                print(update)
                if debug == 0:
                        CNX.DB_QUERY(update)
        sys.exit(0)
