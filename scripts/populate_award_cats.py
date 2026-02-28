#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1.1 $
#         Date: $Date: 2014/06/09 02:26:28 $


# import cgi
# import sys
# import os
# import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        # Retrieve all award categories for each award type IDs
        query = "select distinct award_type_id, award_atype from awards order by award_type_id"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        pairs = []
        while record:
                pairs.append(record[0])
                record = CNX.DB_FETCHMANY()

        for pair in pairs:
                award_cat_type_id = int(pair[0])
                award_cat_name = pair[1]
                if award_cat_name == None:
                        continue

                insert = "insert into award_cats (award_cat_name, award_cat_type_id) values('%s',%d)" % (CNX.DB_ESCAPE_STRING(award_cat_name), award_cat_type_id)
                if debug == 0:
                        CNX.DB_QUERY(insert)
                else:
                        print(insert)
                award_cat_id = CNX.DB_INSERT_ID()
                update = "update awards set award_cat_id=%d where award_type_id=%d and award_atype='%s'" % (award_cat_id, award_cat_type_id, CNX.DB_ESCAPE_STRING(award_cat_name))
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)

        query = "update awards set award_atype=NULL"
        if debug == 0:
                CNX.DB_QUERY(query)
        else:
                print(query)
