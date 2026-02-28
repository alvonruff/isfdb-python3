#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2026   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended titlelication of such source code.
#
#     Version: $Revision: 1259 $
#     Date: $Date: 2026-02-15 16:59:31 -0500 (Sun, 15 Feb 2026) $

        
import cgi
import sys
from isfdb import *
from isfdblib import *
from titleClass import *
from SQLparsing import *
from login import *
from library import *
from navbar import *
        
        
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Make Variant Submission'
        submission.cgi_script = 'mkvariant'
        submission.type = MOD_TITLE_MKVARIANT

        new = titles(db)
        new.cgi2obj()

        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error("", new.title_id)

        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <MakeVariant>\n"
        update_string += "    <Record>%d</Record>\n" % (int(new.title_id))
        update_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(new.title_title))
        update_string += "    <Title>%s</Title>\n" % (CNX.DB_ESCAPE_STRING(new.title_title))
        if new.title_trans_titles:
                update_string += "    <TransTitles>\n"
                for trans_title in new.title_trans_titles:
                        update_string += "      <TransTitle>%s</TransTitle>\n" % (CNX.DB_ESCAPE_STRING(trans_title))
                update_string += "    </TransTitles>\n"
        update_string += "    <Year>%s</Year>\n" % (CNX.DB_ESCAPE_STRING(new.title_year))
        if new.title_series:
                update_string += "    <Series>%s</Series>\n" % (CNX.DB_ESCAPE_STRING(new.title_series))
        if new.title_seriesnum:
                update_string += "    <Seriesnum>%s</Seriesnum>\n" % (CNX.DB_ESCAPE_STRING(new.title_seriesnum))
        if new.title_webpages:
                update_string += "    <Webpages>\n"
                for title_webpage in new.title_webpages:
                        update_string += "      <Webpage>%s</Webpage>\n" % (CNX.DB_ESCAPE_STRING(title_webpage))
                update_string += "    </Webpages>\n"
        update_string += "    <Language>%s</Language>\n" % (CNX.DB_ESCAPE_STRING(new.title_language))
        update_string += "    <TitleType>%s</TitleType>\n" % (CNX.DB_ESCAPE_STRING(new.title_ttype))
        if new.title_note:
                update_string += "    <Note>%s</Note>\n" % CNX.DB_ESCAPE_STRING(new.title_note)
        if 'mod_note' in new.form:
                # Unlike the attributes of the new object, the form data is not XML-escaped, so we need to escape it here
                update_string += "    <ModNote>%s</ModNote>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(new.form['mod_note'].value)))
        
        #############################################################

        update_string += "    <Authors>\n"
        counter = 0
        while counter < new.num_authors:
                update_string += "      <Author>%s</Author>\n" % (CNX.DB_ESCAPE_STRING(new.title_authors[counter]))
                counter += 1
        update_string += "    </Authors>\n"
        update_string += "  </MakeVariant>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
