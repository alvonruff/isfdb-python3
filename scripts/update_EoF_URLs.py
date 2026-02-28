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
        query = """select webpage_id, url from webpages where url like 'http://sf-encyclopedia.uk/fe.php?nm=%'"""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        while record:
                webpage_id = record[0][0]
                url = record[0][1]
                new_url = 'https://sf-encyclopedia.com/fe/%s' % url.split('fe.php?nm=')[1]
                update = """update webpages set url = '%s' where webpage_id = %d""" % (CNX.DB_ESCAPE_STRING(new_url), webpage_id)
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
                record = CNX.DB_FETCHMANY()
