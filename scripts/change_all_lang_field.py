#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2015-2026   Ahasuerus, Al von Ruff
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

        # Retrieve all user preferences for "display all languages"
        query = """select user_pref_id, display_all_languages
                from user_preferences
                where display_all_languages is not null"""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        user_preferences = []
        while record:
                user_preferences.append(record[0])
                record = CNX.DB_FETCHMANY()
        print(user_preferences)

        query = 'update user_preferences set display_all_languages = null'
        if debug == 0:
                CNX.DB_QUERY(query)
        else:
                print(query)

        query = 'ALTER TABLE user_preferences MODIFY display_all_languages ENUM("All","None","Selected")'
        if debug == 0:
                CNX.DB_QUERY(query)
        else:
                print(query)

        for user_preference in user_preferences:
                user_pref_id = user_preference[0]
                display_all_languages = user_preference[1]
                if display_all_languages:
                        value = 'All'
                else:
                        value = 'Selected'
                query = "update user_preferences set display_all_languages = '%s' where user_pref_id = %d" % (value, user_pref_id)
                if debug == 0:
                        CNX.DB_QUERY(query)
                else:
                        print(query)

        query = "select distinct user_id from user_languages union select user_id from user_preferences"
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        user_ids = []
        while record:
                user_ids.append(record[0][0])
                record = CNX.DB_FETCHMANY()

        # Add "English" to the list of "Selected" languages for all users who have user preferences defined
        for user_id in user_ids:
                update = "insert into user_languages (user_id, lang_id, user_choice) values(%d, 17, 1)" % user_id
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(query)
                print(user_id)
