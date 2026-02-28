#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2022-2026   Ahasuerus, Al von Ruff
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
        query = """select pub_id, pub_frontimage from pubs where pub_frontimage like 'http://sf-encyclopedia.uk/%'"""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        while record:
                pub_id = record[0][0]
                old_url = record[0][1]
                new_url = old_url.replace('http://sf-encyclopedia.uk/', 'https://x.sf-encyclopedia.com/')
                update = """update pubs set pub_frontimage = '%s' where pub_id = %d""" % (CNX.DB_ESCAPE_STRING(new_url), pub_id)
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
                record = CNX.DB_FETCHMANY()
