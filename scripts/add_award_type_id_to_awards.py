#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1264 $
#         Date: $Date: 2026-02-21 11:58:41 -0500 (Sat, 21 Feb 2026) $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        # Retrieve all award types and create a dictionary of award type IDs by award code
        query = "select award_type_id, award_type_code from award_types"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        codes = {}
        while record:
                award_type_id = record[0][0]
                code = record[0][1]
                codes[code] = award_type_id
                record = CNX.DB_FETCHMANY()
        print(codes)

        for code in codes:
                award_type_id = codes[code]
                update = "update awards set award_type_id=%d where award_ttype='%s'" % (award_type_id, code)
                print(update)
                if debug == 0:
                        CNX.DB_QUERY(update)
