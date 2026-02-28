#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2024-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

import sys
from SQLparsing import *

debug = 0

if __name__ == "__main__":

        domains = {}
        query = """select pub_id, pub_frontimage from pubs where pub_frontimage like '%amazon%/images/W/MEDIAX%/images/I/%'"""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        count = 0
        while record:
                pub_id = record[0][0]
                pub_frontimage = record[0][1]
                new_url_list = pub_frontimage.split('/images/W/MEDIAX')
                first_segment = new_url_list[0]
                second_segment = new_url_list[1].split('/images/')[1]
                new_url = first_segment + '/images/' + second_segment
                print(new_url)
                update = """update pubs set pub_frontimage = '%s' where pub_id = %d""" % (CNX.DB_ESCAPE_STRING(new_url), pub_id)
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                       print(update)
                record = CNX.DB_FETCHMANY()
                count += 1
        print(count)
