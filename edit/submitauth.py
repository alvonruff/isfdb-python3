#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Bill Longley and Ahasuerus
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
from SQLparsing import *
from authorClass import *
from navbar import *
        
def CheckAuthField(newUsed, oldUsed, newField, oldField, tag, multi):
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
        submission.header = 'Author Change Submission'
        submission.cgi_script = 'editauth'
        submission.type = MOD_AUTHOR_UPDATE
        
        new = authors(db)
        new.cgi2obj()
        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error('', new.author_id)
        
        old = authors(db)
        old.load(int(new.author_id))
        
        changes = 0
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <AuthorUpdate>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <Record>%d</Record>\n" % (int(new.author_id))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(old.author_canonical)))
        
        (changes, update) = CheckAuthField(new.used_canonical, old.used_canonical, new.author_canonical, old.author_canonical, 'Canonical', 0)
        if changes:
                update_string += update

        (changes, update) = CheckAuthField(new.used_trans_names, old.used_trans_names,
                                           new.author_trans_names, old.author_trans_names, 'AuthorTransName', 1)
        if changes:
                update_string += update

        (changes, update) = CheckAuthField(new.used_legalname, old.used_legalname, new.author_legalname, old.author_legalname, 'Legalname', 0)
        if changes:
                update_string += update

        (changes, update) = CheckAuthField(new.used_trans_legal_names, old.used_trans_legal_names,
                                           new.author_trans_legal_names, old.author_trans_legal_names, 'AuthorTransLegalName', 1)
        if changes:
                update_string += update
        (changes, update) = CheckAuthField(new.used_lastname, old.used_lastname, new.author_lastname, old.author_lastname, 'Familyname', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAuthField(new.used_image, old.used_image, new.author_image, old.author_image, 'Image', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAuthField(new.used_birthplace, old.used_birthplace, new.author_birthplace, old.author_birthplace, 'Birthplace', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAuthField(new.used_birthdate, old.used_birthdate, new.author_birthdate, old.author_birthdate, 'Birthdate', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAuthField(new.used_deathdate, old.used_deathdate, new.author_deathdate, old.author_deathdate, 'Deathdate', 0)
        if changes:
                update_string += update
        (changes, update) = CheckAuthField(new.used_language, old.used_language, new.author_language, old.author_language, 'Language', 0)
        if changes:
                update_string += update

        (changes, update) = CheckAuthField(new.used_emails, old.used_emails, new.author_emails, old.author_emails, 'Email', 1)
        if changes:
                update_string += update
        (changes, update) = CheckAuthField(new.used_webpages, old.used_webpages, new.author_webpages, old.author_webpages, 'Webpage', 1)
        if changes:
                update_string += update

        (changes, update) = CheckAuthField(new.used_note, old.used_note, new.author_note, old.author_note, 'Note', 0)
        if changes:
                update_string += update

        if new.form.has_key('mod_note'):
                update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))
        
        update_string += "  </AuthorUpdate>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
