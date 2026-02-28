#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2016-2026   Ahasuerus, Al von Ruff
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

        # Retrieve all unauthenticated users with submissions
        query = """select distinct s.sub_submitter
                from submissions s, mw_user u
                where s.sub_submitter = u.user_id
                and u.user_email !=''
                and u.user_email IS NOT NULL
                and u.user_email_authenticated IS NULL
                order by s.sub_submitter"""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        users = []
        while record:
                users.append(record[0][0])
                record = CNX.DB_FETCHMANY()
        if not users:
                print("No unauthenticated users with submissions. Exiting.")
                sys.exit(0)
        users_in_clause = list_to_in_clause(users)

        query = """update mw_user set user_email_authenticated=20160128010101
                where user_id in (%s)""" % users_in_clause
        print(query)
        if debug == 0:
                CNX.DB_QUERY(query)
        print("User records updated")
