#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended titlelication of such source code.
#
#     Version: $Revision: 972 $
#     Date: $Date: 2022-08-23 16:44:48 -0400 (Tue, 23 Aug 2022) $

        
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from titleClass import *
from SQLparsing import *
from login import *
from library import *
        
def DoField(Label, NewUsed, NewValue):
        if Label == 'Synopsis':
                CheckValue = XMLunescape(NewValue)
        else:
                CheckValue = NewValue
        if NewUsed:
                retval = "    <%s>%s</%s>\n" % (Label, db.escape_string(NewValue), Label)
                return(retval, 1)
        else:
                return("", 0)

        
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Add Variant Title Submission'
        submission.cgi_script = 'addvariant'
        submission.type = MOD_VARIANT_TITLE

        new = titles(db)
        new.cgi2obj()
        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error("", new.title_id)
        
        parent_data = SQLloadTitle(new.title_id)
        if parent_data[TITLE_PARENT]:
                submission.error('Parent title is currently a variant of another title. Variants of variants are not allowed')

        titlename = SQLgetTitle(new.title_id)
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <VariantTitle>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(titlename)))
        update_string += "    <Parent>%d</Parent>\n" % (int(new.title_id))
        
        (val, changed) = DoField('Title', new.used_title, new.title_title)
        update_string += val

        if new.used_trans_titles:
                update_string += "    <TransTitles>\n"
                for trans_title in new.title_trans_titles:
                        update_string += "      <TransTitle>%s</TransTitle>\n" % (db.escape_string(trans_title))
                update_string += "    </TransTitles>\n"

        (val, changed) = DoField('Year', new.used_year, new.title_year)
        update_string += val
        (val, changed) = DoField('Translator', new.used_xlate, new.title_xlate)
        update_string += val
        (val, changed) = DoField('Storylen', new.used_storylen, new.title_storylen)
        update_string += val
        (val, changed) = DoField('TitleType', new.used_ttype, new.title_ttype)
        update_string += val
        (val, changed) = DoField('Language', new.used_language, new.title_language)
        update_string += val
        (val, changed) = DoField('Note', new.used_note, new.title_note)
        update_string += val

        if 'mod_note' in new.form:
                update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))

        #############################################################
        update_string += "    <Authors>\n"
        counter = 0
        while counter < new.num_authors:
                update_string += "      <Author>%s</Author>\n" % (db.escape_string(new.title_authors[counter]))
                counter += 1
        update_string += "    </Authors>\n"

        update_string += "  </VariantTitle>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
