#!/usr/bin/python
from __future__ import print_function
#    (C) COPYRIGHT 2008-2026   Al von Ruff, MaryD, RobertGl and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1264 $
#     Date: $Date: 2026-02-21 11:58:41 -0500 (Sat, 21 Feb 2026) $

import sys
if sys.version_info.major == 3:
        PYTHONVER = "python3"
elif sys.version_info.major == 2:
        PYTHONVER = "python2"

import cgi
import os
from SQLparsing import *
from struct import *

if PYTHONVER == 'python3':
        from hashlib import md5
else:
        import md5

debug = 0

if __name__ == '__main__':


        try:
                username = sys.argv[1]
                password = sys.argv[2]
        except:
                print('usage: create_user.py username password')
                print('       The third parameter, if specified, should be 1 for moderator/bureaucrat users')
                print('       and 0 for non-privileged users. The default is 1, i.e. moderator AND bureaucrat.')
                sys.exit(1)

        # By default, the new user is a moderator AND bureaucrat. The third parameter passed to this script (if '0')
        # overrides the default behavior and makes the new user a non-privileged user.
        privileged = 1
        try:
                privileged = int(sys.argv[3])
        except:
                pass

        ###############################################################
        # Insert a username and password into mw_user
        # 'try' for MediWiki 1.5-1.34, 'except' for 1.35+
        ###############################################################
        CNX = MYSQL_CONNECTOR()
        try:
                query = """insert into mw_user(user_name,user_real_name,user_password,user_newpassword,user_email,user_options,user_token,user_touched)
                        values('%s','','','','','','','')""" % CNX.DB_ESCAPE_STRING(username)
                if debug == 0:
                        CNX.DB_QUERY(query)
                        user_id = CNX.DB_INSERT_ID()
                else:
                        user_id = 1
        except:
                query = """insert into mw_user(user_name,user_real_name,user_password,user_newpassword,user_email,user_token,user_touched)
                        values('%s','','','','','','')""" % CNX.DB_ESCAPE_STRING(username)
                if debug == 0:
                        CNX.DB_QUERY(query)
                        user_id = CNX.DB_INSERT_ID()
                else:
                        user_id = 1

        ###############################################################
        # Construct and store the password
        ###############################################################
        hash = md5()

        if PYTHONVER == 'python3':
                password = password.encode('utf-8')

        hash.update(password)
        password = str(hash.hexdigest())
        newstr = "%d-%s" % (user_id, password)

        if PYTHONVER == 'python3':
                newstr = newstr.encode('utf-8')

        hash2 = md5()
        hash2.update(newstr)
        submitted_password = hash2.hexdigest()
        query = "update mw_user set user_password='%s' where user_id=%d" % (CNX.DB_ESCAPE_STRING(submitted_password), user_id)

        if debug == 0:
                CNX.DB_QUERY(query)
        else:
                print(query)

        ###############################################################
        # Update privileges
        ###############################################################
        if privileged:
                # Insert moderator/bureaucrat rights into mw_user_groups
                query = "insert into mw_user_groups(ug_user, ug_group) values(%d, '%s')" % (user_id, 'sysop')
                if debug == 0:
                        CNX.DB_QUERY(query)
                else:
                        print(query)
                query = "insert into mw_user_groups(ug_user, ug_group) values(%d, '%s')" % (user_id, 'bureaucrat')
                if debug == 0:
                        CNX.DB_QUERY(query)
                else:
                        print(query)
        
        ###############################################################
        # mw_user_groups is an InnoDB table. We have to commit changes,
        # otherwise this insertion does nothing.
        ###############################################################
        if debug == 0:
                db.commit()
        db.close()
