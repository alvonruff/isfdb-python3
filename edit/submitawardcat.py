#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 972 $
#     Date: $Date: 2022-08-23 16:44:48 -0400 (Tue, 23 Aug 2022) $

        
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from library import *
from awardcatClass import *
from SQLparsing import *
        
def CheckAwardCatField(newUsed, oldUsed, newField, oldField, tag, multi):
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

        if update:
                if multi:
                        update_string = "    <%ss>\n" % (tag)
                        for field in newField:
                                update_string += "      <%s>%s</%s>\n" % (tag, db.escape_string(field), tag)
                        update_string += "    </%ss>\n" % (tag)
                else:
                        update_string = "    <%s>%s</%s>\n" % (tag, db.escape_string(newField), tag)

                changes = 1
        return (changes, update_string)


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Award Category Change Submission'
        submission.cgi_script = 'editawardcat'
        submission.type = MOD_AWARD_CAT_UPDATE

        new = award_cat()
        new.cgi2obj()
        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error('', new.award_cat_id)

        old = award_cat()
        old.award_cat_id = new.award_cat_id
        old.load()
        
        changes = 0
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <AwardCategoryUpdate>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <AwardCategoryId>%d</AwardCategoryId>\n" % (int(new.award_cat_id))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(old.award_cat_name)))
        
        (changes, update) = CheckAwardCatField(new.used_cat_name, old.used_cat_name, new.award_cat_name, old.award_cat_name, 'CategoryName', 0)
        if changes:
                update_string += update
        
        (changes, update) = CheckAwardCatField(new.used_cat_order, old.used_cat_order, new.award_cat_order, old.award_cat_order, 'DisplayOrder', 0)
        if changes:
                update_string += update

        (changes, update) = CheckAwardCatField(new.used_note, old.used_note, new.award_cat_note, old.award_cat_note, 'Note', 0)
        if changes:
                update_string += update
        
        (changes, update) = CheckAwardCatField(new.used_webpages, old.used_webpages, new.award_cat_webpages, old.award_cat_webpages, 'Webpage', 1)
        if changes:
                update_string += update

        update_string += "  </AwardCategoryUpdate>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
