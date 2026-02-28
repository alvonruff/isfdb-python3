#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1259 $
#     Date: $Date: 2026-02-15 16:59:31 -0500 (Sun, 15 Feb 2026) $

        
import cgi
import sys
from isfdb import *
from isfdblib import *
from library import *
from awardcatClass import *
from SQLparsing import *


if __name__ == '__main__':
        
        submission = Submission()
        submission.header = 'New Award Category Submission'
        submission.cgi_script = 'addawardcat'
        submission.type = MOD_AWARD_CAT_NEW

        new = award_cat()
        new.cgi2obj()
        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error("", new.award_cat_type_id)
        
        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <NewAwardCat>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name))
        update_string += "    <Subject>%s</Subject>\n" % CNX.DB_ESCAPE_STRING(new.award_cat_name)

        if new.used_cat_name:
                update_string += "    <AwardCatName>%s</AwardCatName>\n" % CNX.DB_ESCAPE_STRING(new.award_cat_name)

        if new.used_cat_type_id:
                update_string += "    <AwardTypeId>%d</AwardTypeId>\n" % int(new.award_cat_type_id)

        if new.used_cat_order:
                update_string += "    <DisplayOrder>%d</DisplayOrder>\n" % int(new.award_cat_order)

        if new.used_note:
                update_string += "    <Note>%s</Note>\n" % (CNX.DB_ESCAPE_STRING(new.award_cat_note))

        if new.used_webpages:
                update_string += "    <Webpages>\n"
                for webpages in new.award_cat_webpages:
                        update_string += "         <Webpage>%s</Webpage>\n" % (CNX.DB_ESCAPE_STRING(webpages))
                update_string += "    </Webpages>\n"

        if 'mod_note' in new.form:
                update_string += "    <ModNote>%s</ModNote>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(new.form['mod_note'].value)))

        update_string += "  </NewAwardCat>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
