#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2009-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended serieslication of such source code.
#
#     Version: $Revision: 713 $
#     Date: $Date: 2021-08-27 10:38:44 -0400 (Fri, 27 Aug 2021) $


import cgi
import sys
from login import *
from SQLparsing import *
from common import *
        
debug = 0

def DoError(message):
        PrintHeader("My Translation Preferences Update")
        PrintNavbar("languages", 0, 0, 0, 0)
        print('<h3>%s.</h3>' % message)
        PrintTrailer('mylanguages', 0, 0)
        sys.exit(0)

        
if __name__ == '__main__':

        sys.stderr = sys.stdout
        form = cgi.FieldStorage()

        user = User()
        user.load()

        if not user.id:
                DoError('You must be logged in to modify your language preferences')

        user_id = int(user.id)
        langs = []
        choices = []
        try:
                for key in form.keys():
                        if '.' not in key:
                                continue
                        key_type = key.split('.')[0]
                        key_number = int(key.split('.')[1])
                        if key_type == 'lang_id':
                                # Check that the submitted language code exists
                                if key_number > (len(LANGUAGES)-1) or key_number < 1:
                                        raise
                                langs.append(key_number)
                        if key_type == 'lang_choice':
                                choice = form[key].value
                                choices.append((key_number,choice))
        except:
                DoError('Invalid language code')

        updates = []
        for lang_id in langs:
                status = 0
                for choice in choices:
                        if lang_id == choice[0]:
                                if choice[1] == 'on':
                                        status = 1
                                break
                updates.append((lang_id,status))

        for update in updates:
                lang_id = update[0]
                status = update[1]
                query = "select user_lang_id,user_choice from user_languages where lang_id=%d and user_id=%d" % (lang_id, user_id)
                db.query(query)
                result = db.store_result()

                #If this user/language combination is not already on file:
                if result.num_rows() < 1:
                        # If the language is not selected and not on file, skip it
                        if status == 0:
                                continue
                        # If the languages is selected and not on file, add a new row
                        update = "insert into user_languages(lang_id,user_id,user_choice) values(%d,%d,%d)" % (lang_id, user_id, status)

                #If this user/language combination is already on file, retrieve the row ID and current value
                else:
                        record = result.fetch_row()
                        user_lang_id = int(record[0][0])
                        current_choice = record[0][1]
                        # If the user choice is on file and the entered user choice is the same, don't change anything
                        if current_choice == status:
                                continue
                        # If the user choice on file is ON and the entered user choice is OFF for this language,
                        #   then delete the row with this language choice from the table
                        if (current_choice == 1) and (status == 0):
                                update = "delete from user_languages where user_lang_id = %d" % (user_lang_id)
                        elif (current_choice == 0) and (status == 1):
                                update = "update user_languages set user_choice = %d where user_lang_id = %d" % (status, user_lang_id)
                if debug == 0:
                        db.query(update)

        ISFDBLocalRedirect('mypreferences.cgi')

