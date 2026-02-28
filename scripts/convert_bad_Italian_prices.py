#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2021-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 418 $
#         Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


import cgi
import sys
import os
import string
from SQLparsing import *
from library import *

debug = 0

if __name__ == '__main__':

        # Find all duplicate tags
        query = """select pub_id, pub_price from pubs where pub_price like '% Lit'"""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        while record:
                pub_id = record[0][0]
                pub_price = record[0][1]
                numeric_price = pub_price.split(' Lit')[0]
                new_price = 'Lit %s' % numeric_price
                print('ID: ', pub_id)
                print('Old: ', numeric_price)
                print('New: ', new_price)
                update = "update pubs set pub_price = '%s' where pub_id = %d" % (CNX.DB_ESCAPE_STRING(new_price), int(pub_id))
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
                record = CNX.DB_FETCHMANY()
        print("Total processed: %d" % int(CNX.DB_NUMROWS()))

