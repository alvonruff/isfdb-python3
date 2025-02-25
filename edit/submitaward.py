#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2025   Al von Ruff and Ahasuerus
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
from awardClass import *
from isfdb import *
from isfdblib import *
from SQLparsing import *
from login import *
from library import *
        
def EvalField(Label, NewUsed, OldUsed, NewValue, OldValue):
        OldValue = XMLescape(OldValue)
        update = 0
        if NewUsed and OldUsed:
                if NewValue != OldValue:
                        update = 1
        elif NewUsed and (OldUsed == 0):
                update = 1
        elif (NewUsed == 0) and OldUsed:
                NewValue = ""
                update = 1
        if update:
                retval = "    <%s>%s</%s>\n" % (Label, db.escape_string(NewValue), Label)
                return(retval, 1)
        else:
                return("", 0)

if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Award Update Submission'
        submission.cgi_script = 'editaward'
        submission.type = MOD_AWARD_UPDATE

        new = awards(db)
        new.cgi2obj()
        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error("", new.award_id)

        old = awards(db)
        old.loadXML(int(new.award_id))

        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <AwardUpdate>\n"
        update_string += "    <Record>%d</Record>\n" % (int(new.award_id))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(old.award_title)))
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))

        changes = 0

        (val, changed) = EvalField('AwardTitle', new.used_title, old.used_title, new.award_title, old.award_title)
        update_string += val
        changes += changed

        (val, changed) = EvalField('AwardType', new.used_type_id, old.used_type_id, new.award_type_id, old.award_type_id)
        update_string += val
        changes += changed

        (val, changed) = EvalField('AwardYear', new.used_year, old.used_year, new.award_year, old.award_year)
        update_string += val
        changes += changed

        (val, changed) = EvalField('AwardCategory', new.used_cat_id, old.used_cat_id, new.award_cat_id, old.award_cat_id)
        update_string += val
        changes += changed

        (val, changed) = EvalField('AwardLevel', new.used_level, old.used_level, new.award_level, old.award_level)
        update_string += val
        changes += changed

        (val, changed) = EvalField('AwardMovie', new.used_movie, old.used_movie, new.award_movie, old.award_movie)
        update_string += val
        changes += changed

        #############################################################
        #       AUTHORS
        #############################################################
        update = 0
        if new.num_authors != old.num_authors:
                update = 1
        else:
                counter = 0
                while counter < new.num_authors:
                        if new.award_authors[counter] != XMLescape(old.award_authors[counter]):
                                update = 1
                                break
                        counter += 1

        if update:
                update_string += "    <AwardAuthors>\n"
                counter = 0
                while counter < new.num_authors:
                        update_string += "      <AwardAuthor>%s</AwardAuthor>\n" % (db.escape_string(new.award_authors[counter]))
                        counter += 1
                update_string += "    </AwardAuthors>\n"

        (val, changed) = EvalField('AwardNote', new.used_note, old.used_note, new.award_note, old.award_note)
        update_string += val
        changes += changed

        if 'mod_note' in new.form:
                update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))

        update_string += "  </AwardUpdate>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
