#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2020-2026   Ahasuerus, Al von Ruff
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

        query = """select sub_id, sub_data from submissions
                where sub_type=6
                and sub_state='I'
                and affected_record_id is null"""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        while record:
                sub_id = record[0][0]
                sub_data = record[0][1]
                doc = minidom.parseString(XMLunescape2(sub_data))
                merge = doc.getElementsByTagName('PubDelete')
                record_id = GetElementValue(merge, 'Record')
                print(sub_id, record_id)
                update = "update submissions set affected_record_id = %d where sub_id = %d" % (int(record_id), int(sub_id))
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
                record = CNX.DB_FETCHMANY()
        print("Total processed: %d" % int(CNX.DB_NUMROWS()))

