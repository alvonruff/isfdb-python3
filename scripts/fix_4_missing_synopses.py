#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2019-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 15 $
#     Date: $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

def list_to_in_clause(id_list):
        in_clause = ''
        for id_value in id_list:
                id_string = str(id_value)
                if not in_clause:
                        in_clause = "'%s'" % id_string
                else:
                        in_clause += ",'%s'" % id_string
        return in_clause


if __name__ == '__main__':

        update = """update titles set title_synopsis=NULL
                where title_id in (85496,87408,119072,1670052)"""
        print(update)
        if debug == 0:
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(update)
        print("Title records updated")
