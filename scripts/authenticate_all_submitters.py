#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2016-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


import cgi
import sys
import os
import string
import MySQLdb
from localdefs import *

def Date_or_None(s):
    return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)

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

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    # Retrieve all unauthenticated users with submissions
    query = """select distinct s.sub_submitter
            from submissions s, mw_user u
            where s.sub_submitter = u.user_id
            and u.user_email !=''
            and u.user_email IS NOT NULL
            and u.user_email_authenticated IS NULL
            order by s.sub_submitter"""
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    users = []
    while record:
        users.append(record[0][0])
        record = result.fetch_row()
    if not users:
        print("No unauthenticated users with submissions. Exiting.")
        sys.exit(0)
    users_in_clause = list_to_in_clause(users)

    query = """update mw_user set user_email_authenticated=20160128010101
                where user_id in (%s)""" % users_in_clause
    print(query)
    db.query(query)
    print("User records updated")
