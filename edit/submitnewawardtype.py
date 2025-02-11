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
from awardtypeClass import *
from SQLparsing import *


if __name__ == '__main__':
        
        submission = Submission()
        submission.header = 'New Award Type Submission'
        submission.cgi_script = 'newawardtype'
        submission.type = MOD_AWARD_TYPE_NEW

        new = award_type()
        new.cgi2obj()
        if new.error:
                submission.error(new.error)
        
        if not submission.user.id:
                submission.error()

        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <NewAwardType>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(new.award_type_name))
        
        if new.used_short_name:
                update_string += "    <ShortName>%s</ShortName>\n" % (db.escape_string(new.award_type_short_name))

        if new.used_name:
                update_string += "    <FullName>%s</FullName>\n" % (db.escape_string(new.award_type_name))
        
        if new.used_by:
                update_string += "    <AwardedBy>%s</AwardedBy>\n" % (db.escape_string(new.award_type_by))

        if new.used_for:
                update_string += "    <AwardedFor>%s</AwardedFor>\n" % (db.escape_string(new.award_type_for))

        if new.used_poll:
                update_string += "    <Poll>%s</Poll>\n" % (db.escape_string(new.award_type_poll))

        if new.used_note:
                update_string += "    <Note>%s</Note>\n" % (db.escape_string(new.award_type_note))

        if new.used_webpages:
                update_string += "    <Webpages>\n"
                for webpages in new.award_type_webpages:
                        update_string += "         <Webpage>%s</Webpage>\n" % (db.escape_string(webpages))
                update_string += "    </Webpages>\n"

        if new.used_non_genre:
                update_string += "    <NonGenre>%s</NonGenre>\n" % (db.escape_string(new.award_type_non_genre))


        update_string += "  </NewAwardType>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
