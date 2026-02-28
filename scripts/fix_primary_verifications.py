#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2018-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 15 $
#         Date: $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        query = """select distinct pv1.pub_id, pv1.user_id,
                        pv1.verification_id, pv1.ver_time, pv1.ver_transient,
                        pv2.verification_id, pv2.ver_time, pv2.ver_transient
                        from primary_verifications pv1, primary_verifications pv2
                        where pv1.verification_id != pv2.verification_id
                        and pv1.pub_id = pv2.pub_id
                        and pv1.user_id = pv2.user_id
                """

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        count = 0
        delete_vers = {}
        while record:
                pub_id = record[0][0]
                user_id = record[0][1]
                ver_id1 = record[0][2]
                ver_time1 = record[0][3]
                ver_trans1 = record[0][4]
                ver_id2 = record[0][5]
                ver_time2 = record[0][6]
                ver_trans2 = record[0][7]
                record = CNX.DB_FETCHMANY()

                # If this pub/user combination has already been processed, skip the verification record
                if pub_id in delete_vers and user_id in delete_vers[pub_id]:
                        continue

                count += 1
                drop = 1
                # If one verification is transient and the other one is permanent, then keep the permanent one
                if ver_trans1 and not ver_trans2:
                        drop = 1
                elif ver_trans2 and not ver_trans1:
                        drop = 2
                else:
                        # If the transient flags are the same, then drop the more recent verification
                        if ver_time1 < ver_time2:
                                drop = 2
                        else:
                                drop = 1
                #print count, ver_trans1, ver_trans2, ver_time1, ver_time2, drop

                if pub_id not in delete_vers:
                        delete_vers[pub_id] = {}

                if drop == 1:
                        delete_vers[pub_id][user_id] = ver_id1
                else:
                        delete_vers[pub_id][user_id] = ver_id2

        count = 0
        for pub_id in delete_vers:
                for user_id in delete_vers[pub_id]:
                        ver_id = delete_vers[pub_id][user_id]
                        count += 1
                        print(count, pub_id, user_id, ver_id, 'http://www.isfdb.org/cgi-bin/pl.cgi?%d' % pub_id)
                        delete = "delete from primary_verifications where verification_id = %d" % ver_id
                        if debug == 0:
                                CNX.DB_QUERY(delete)
                        else:
                                print(delete)
