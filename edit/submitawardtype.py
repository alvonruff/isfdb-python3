#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 972 $
#     Date: $Date: 2022-08-23 16:44:48 -0400 (Tue, 23 Aug 2022) $

        
import cgi
import sys
from isfdb import *
from isfdblib import *
from library import *
from awardtypeClass import *
from SQLparsing import *
        
def CheckAwardTypeField(newUsed, oldUsed, newField, oldField, tag, multi):
        update = 0
        changes = 0
        update_string = ''

        ######################################################################
        # If a field is and was being used, update it only if it's different
        ######################################################################
        if newUsed and oldUsed:
                if multi:
                        update = compare_lists(newField, oldField)
                else:
                        if newField != XMLescape(oldField):
                                update = 1

        ######################################################################
        # If a field is being used, but wasn't before, update it
        ######################################################################
        elif newUsed and (oldUsed == 0):
                update = 1

        ######################################################################
        # If a field is not being used, but it was before, update it
        ######################################################################
        elif (newUsed == 0) and oldUsed:
                newField = ""
                update = 1

        CNX = MYSQL_CONNECTOR()
        if update:
                if multi:
                        update_string = "    <%ss>\n" % (tag)
                        for field in newField:
                                update_string += "      <%s>%s</%s>\n" % (tag, CNX.DB_ESCAPE_STRING(field), tag)
                        update_string += "    </%ss>\n" % (tag)
                else:
                        update_string = "    <%s>%s</%s>\n" % (tag, CNX.DB_ESCAPE_STRING(newField), tag)

                changes = 1
        return (changes, update_string)


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Award Type Change Submission'
        submission.cgi_script = 'editawardtype'
        submission.type = MOD_AWARD_TYPE_UPDATE

        new = award_type()
        new.cgi2obj()
        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error('', new.award_type_id)
        
        old = award_type()
        old.award_type_id = new.award_type_id
        old.load()
        
        CNX = MYSQL_CONNECTOR()
        changes = 0
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <AwardTypeUpdate>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))
        update_string += "    <AwardTypeId>%d</AwardTypeId>\n" % (int(new.award_type_id))
        update_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(old.award_type_name)))
        
        (changes, update) = CheckAwardTypeField(new.used_short_name, old.used_short_name, new.award_type_short_name, old.award_type_short_name, 'ShortName', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAwardTypeField(new.used_name, old.used_name, new.award_type_name, old.award_type_name, 'FullName', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAwardTypeField(new.used_by, old.used_by, new.award_type_by, old.award_type_by, 'AwardedBy', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAwardTypeField(new.used_for, old.used_for, new.award_type_for, old.award_type_for, 'AwardedFor', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAwardTypeField(new.used_poll, old.used_poll, new.award_type_poll, old.award_type_poll, 'Poll', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAwardTypeField(new.used_note, old.used_note, new.award_type_note, old.award_type_note, 'Note', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAwardTypeField(new.used_webpages, old.used_webpages, new.award_type_webpages, old.award_type_webpages, 'Webpage', 1)
        if changes:
                update_string += update
        (changes, update) = CheckAwardTypeField(new.used_non_genre, old.used_non_genre, new.award_type_non_genre, old.award_type_non_genre, 'NonGenre', 0)
        if changes:
                update_string += update
        
        update_string += "  </AwardTypeUpdate>\n"
        update_string += "</IsfdbSubmission>\n"
        
        submission.file(update_string)
