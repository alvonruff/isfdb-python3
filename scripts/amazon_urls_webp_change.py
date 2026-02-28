#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2023-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 418 $
#         Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

from SQLparsing import *

debug = 0

if __name__ == "__main__":

        domains = {}
        query = """select pub_id, pub_frontimage from pubs where pub_frontimage like '%amazon\.%\/W\/WEBP_402378-T%'"""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        count = 0
        while record:
                pub_id = record[0][0]
                pub_frontimage = record[0][1]
                url_segments = pub_frontimage.split('https://')[1]

                new_url_list = url_segments.split('/images/W/WEBP_402378-T1/')
                new_url = '/'.join(new_url_list)
                new_url_list = new_url.split('/images/W/WEBP_402378-T2/')
                new_url = 'https://%s'% '/'.join(new_url_list)

                update = """update pubs set pub_frontimage = '%s' where pub_id = %d""" % (CNX.DB_ESCAPE_STRING(new_url), pub_id)
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
                record = CNX.DB_FETCHMANY()
                count += 1
        print(count)
