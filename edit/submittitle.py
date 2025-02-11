#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended titlelication of such source code.
#
#     Version: $Revision: 1099 $
#     Date: $Date: 2023-02-07 18:29:53 -0500 (Tue, 07 Feb 2023) $

        
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from titleClass import *
from SQLparsing import *
from login import *
from library import *
from navbar import *
        
def EvalField(Label, NewUsed, OldUsed, newField, oldField, multi):
        update = 0

        ######################################################################
        # If a field is and was being used, update it only if it's different
        #####################################################################
        if NewUsed and OldUsed:
                if multi:
                        update = compare_lists(newField, oldField)
                else:
                        if newField != XMLescape(oldField):
                                update = 1
                        
        ######################################################################
        # If a field is being used, but wasn't before, update it
        #####################################################################
        elif NewUsed and (OldUsed == 0):
                update = 1
                
        ######################################################################
        # If a field is not being used, but it was before, update it
        #####################################################################
        elif (NewUsed == 0) and OldUsed:
                newField = ""
                update = 1

        if update:
                if multi:
                        update_string = "    <%ss>\n" % (Label)
                        for field in newField:
                                update_string += "      <%s>%s</%s>\n" % (Label, db.escape_string(field), Label)
                        update_string += "    </%ss>\n" % (Label)
                else:
                        update_string = "    <%s>%s</%s>\n" % (Label, db.escape_string(newField), Label)

                return(update_string, 1)
        else:
                return("", 0)

        
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Title Change Submission'
        submission.cgi_script = 'edittitle'
        submission.type = MOD_TITLE_UPDATE

        new = titles(db)
        new.cgi2obj()
        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error('', new.title_id)
        
        old = titles(db)
        old.loadXML(int(new.title_id))

        changes = 0
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        if new.title_id == '0':
                update_string += "  <NewTitle>\n"
        else:
                update_string += "  <TitleUpdate>\n"
                update_string += "    <Record>%d</Record>\n" % (int(new.title_id))

        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(old.title_title)))
        
        (val, changed) = EvalField('Title', new.used_title, old.used_title, new.title_title, old.title_title,0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('TranslitTitle', new.used_trans_titles, old.used_trans_titles, new.title_trans_titles, old.title_trans_titles,1)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Year', new.used_year, old.used_year, new.title_year, old.title_year,0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Series', new.used_series, old.used_series, new.title_series, old.title_series,0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Seriesnum', new.used_seriesnum, old.used_seriesnum, new.title_seriesnum, old.title_seriesnum,0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Translator', new.used_xlate, old.used_xlate, new.title_xlate, old.title_xlate,0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Storylen', new.used_storylen, old.used_storylen, new.title_storylen, old.title_storylen,0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Webpage', new.used_webpages, old.used_webpages, new.title_webpages, old.title_webpages,1)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Language', new.used_language, old.used_language, new.title_language, old.title_language,0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('TitleType', new.used_ttype, old.used_ttype, new.title_ttype, old.title_ttype,0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Synopsis', new.used_synop, old.used_synop, new.title_synop, old.title_synop,0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Note', new.used_note, old.used_note, new.title_note, old.title_note,0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('NonGenre', new.used_non_genre, old.used_non_genre, new.title_non_genre, old.title_non_genre, 0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Graphic', new.used_graphic, old.used_graphic, new.title_graphic, old.title_graphic, 0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Juvenile', new.used_jvn, old.used_jvn, new.title_jvn, old.title_jvn, 0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Novelization', new.used_nvz, old.used_nvz, new.title_nvz, old.title_nvz, 0)
        update_string += val
        changes += changed

        (val, changed) = EvalField('ContentIndicator', new.used_content, old.used_content, new.title_content, old.title_content, 0)
        update_string += val
        changes += changed

        if new.form.has_key('mod_note'):
                update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))

        if ISFDBDifferentAuthorLists(new.title_authors, old.title_authors):
                update_string += "    <Authors>\n"
                for new_author in new.title_authors:
                        update_string += "      <Author>%s</Author>\n" % db.escape_string(new_author)
                update_string += "    </Authors>\n"

        if old.title_ttype == 'REVIEW':
                if ISFDBDifferentAuthorLists(new.title_subjauthors, old.title_subjauthors):
                        update_string += "    <BookAuthors>\n"
                        for new_author in new.title_subjauthors:
                                update_string += "      <BookAuthor>%s</BookAuthor>\n" % db.escape_string(new_author)
                        update_string += "    </BookAuthors>\n"
        elif old.title_ttype == 'INTERVIEW':
                if ISFDBDifferentAuthorLists(new.title_subjauthors, old.title_subjauthors):
                        update_string += "    <Interviewees>\n"
                        for new_author in new.title_subjauthors:
                                update_string += "      <Interviewee>%s</Interviewee>\n" % db.escape_string(new_author)
                        update_string += "    </Interviewees>\n"


        if new.title_id == '0':
                update_string += "  </NewTitle>\n"
        else:
                update_string += "  </TitleUpdate>\n"

        update_string += "</IsfdbSubmission>\n"
        
        submission.file(update_string)
