#!_PYTHONLOC
#
#     (C) COPYRIGHT 2015   Ahasuerus
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


if __name__ == '__main__':

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    # Retrieve all user preferences for "display all languages"
    query = """select user_pref_id, display_all_languages
            from user_preferences
            where display_all_languages is not null"""
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    user_preferences = []
    while record:
        user_preferences.append(record[0])
        record = result.fetch_row()
    print user_preferences

    query = 'update user_preferences set display_all_languages = null'
    db.query(query)
    result = db.store_result()

    query = 'ALTER TABLE user_preferences MODIFY display_all_languages ENUM("All","None","Selected")'
    db.query(query)
    result = db.store_result()

    for user_preference in user_preferences:
        user_pref_id = user_preference[0]
        display_all_languages = user_preference[1]
        if display_all_languages:
            value = 'All'
        else:
            value = 'Selected'
        query = "update user_preferences set display_all_languages = '%s' where user_pref_id = %d" % (value, user_pref_id)
        db.query(query)
        result = db.store_result()

    query = "select distinct user_id from user_languages union select user_id from user_preferences"
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    user_ids = []
    while record:
        user_ids.append(record[0][0])
        record = result.fetch_row()

    # Add "English" to the list of "Selected" languages for all users who have user preferences defined
    for user_id in user_ids:
        update = "insert into user_languages (user_id, lang_id, user_choice) values(%d, 17, 1)" % user_id
        db.query(update)
        print user_id
