#!/usr/bin/python
from __future__ import print_function
#    (C) COPYRIGHT 2008-2026   Al von Ruff
#        ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#

import cgi
import sys
import os
import string
from SQLparsing import *


def doTable(db, table):
        query = "show create table %s" % table

        CNX2 = MYSQL_CONNECTOR()
        CNX2.DB_QUERY(query)
        rec2 = CNX2.DB_FETCHMANY()
        print("%s;\n" % str(rec2[0][1]))
        if table == 'metadata':
                print("INSERT INTO `metadata` VALUES ('0.02',1,1,1);\n")
        elif table == 'directory':
                print("INSERT INTO `directory` VALUES (1,0,'A'),(2,0,'B'),(3,0,'C'),(4,0,'D'),(5,0,'E'),(6,0,'F'), (7,0,'G'),(8,0,'H'),(9,0,'I'),(10,0,'J'),(11,0,'K'),(12,0,'L'),(13,0,'M'),(14,0,'N'),(15,0,'O'),(16,0,'P'),(17,0,'Q'),(18,0,'R'),(19,0,'S'),(20,0,'T'),(21,0,'U'),(22,0,'V'),(23,0,'W'),(24,0,'X'),(25,0,'Y'),(26,0,'Z');\n")


if __name__ == '__main__':

        query = "show tables"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        while record:
                doTable(db, record[0][0])
                record = CNX.DB_FETCHMANY()

        db.close()
