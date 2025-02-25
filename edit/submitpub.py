#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1099 $
#     Date: $Date: 2023-02-07 18:29:53 -0500 (Tue, 07 Feb 2023) $

        
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from pubClass import *
from SQLparsing import *
from login import *
from library import *
from navbar import *
        

def EvalField(Label, NewUsed, OldUsed, NewValue, OldValue):

        ###################################################
        # Data values are XML escaped when loaded via 
        # cgi2obj(), but not when using load()
        ###################################################
        if Label == 'Title':
                CheckValue = XMLunescape(NewValue)
        else:
                CheckValue = NewValue
                OldValue   = XMLescape(OldValue)

        update = 0
        if NewUsed and OldUsed:
                if CheckValue != OldValue:
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
        submission.header = 'Publication Edit Submission'
        submission.cgi_script = 'editpub'
        submission.type = MOD_PUB_UPDATE

        new = pubs(db)
        new.cgi2obj('explicit')
        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error('', new.pub_id)
        
        old = pubs(db)
        old.load(int(new.pub_id))
        if old.error:
                submission.error(old.error)

        changes = 0
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <PubUpdate>\n"
        update_string += "    <Record>%d</Record>\n" % (int(new.pub_id))
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(new.pub_title))

        (val, changed) = EvalField('Title', new.used_title, old.used_title, new.pub_title, old.pub_title)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Year', new.used_year, old.used_year, new.pub_year, old.pub_year)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Publisher', new.used_publisher, old.used_publisher, new.pub_publisher, old.pub_publisher)
        update_string += val
        changes += changed

        (val, changed) = EvalField('PubSeries', new.used_series, old.used_series, new.pub_series, old.pub_series)
        update_string += val
        changes += changed

        (val, changed) = EvalField('PubSeriesNum', new.used_series_num, old.used_series_num, new.pub_series_num, old.pub_series_num)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Pages', new.used_pages, old.used_pages, new.pub_pages, old.pub_pages)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Binding', new.used_ptype, old.used_ptype, new.pub_ptype, old.pub_ptype)
        update_string += val
        changes += changed

        (val, changed) = EvalField('PubType', new.used_ctype, old.used_ctype, new.pub_ctype, old.pub_ctype)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Isbn', new.used_isbn, old.used_isbn, new.pub_isbn, old.pub_isbn)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Catalog', new.used_catalog, old.used_catalog, new.pub_catalog, old.pub_catalog)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Price', new.used_price, old.used_price, new.pub_price, old.pub_price)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Image', new.used_image, old.used_image, new.pub_image, old.pub_image)
        update_string += val
        changes += changed

        (val, changed) = EvalField('Note', new.used_note, old.used_note, new.pub_note, old.pub_note)
        update_string += val
        changes += changed

        try:
                mod_note = XMLescape(new.form['mod_note'].value)
        except:
                mod_note = ''
        if mod_note:
                update_string += "    <ModNote>%s</ModNote>\n" % db.escape_string(mod_note)
        else:
                if new.requiresModeratorNote(submission.user.id):
                        submission.error("""This publication has been primary verified by at least one editor other than you.
                                         Please enter a moderator note to document the submitted changes""")

        if 'Source' in new.form:
                update_string += "    <Source>%s</Source>\n" % (db.escape_string(XMLescape(new.form['Source'].value)))

        # Only add the submitted identifiers to the submission if they are
        # different from the identifiers that are currently on file
        if old.identifiers != new.identifiers:
                update_string += new.xmlIdentifiers()
        
        if ISFDBDifferentAuthorLists(new.pub_authors, old.pub_authors):
                update_string += "    <Authors>\n"
                for new_author in new.pub_authors:
                        update_string += "      <Author>%s</Author>\n" % db.escape_string(new_author)
                update_string += "    </Authors>\n"

        # Transliterated titles
        (changed, val) = submission.CheckField(new.used_trans_titles, old.used_trans_titles,
                                                  new.pub_trans_titles, old.pub_trans_titles, 'TransTitle', 1)
        changes += changed
        if changed:
                update_string += val

        # Web pages
        (changed, val) = submission.CheckField(new.used_webpages, old.used_webpages,
                                                  new.pub_webpages, old.pub_webpages, 'Webpage', 1)
        changes += changed
        if changed:
                update_string += val

        # Build the XML payload for the Content section
        update_string += db.escape_string(new.xmlContent())
        update_string += "  </PubUpdate>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
