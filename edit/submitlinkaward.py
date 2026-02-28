#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
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
from SQLparsing import *
from login import *
from library import *
from navbar import *
from awardClass import *


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Link Award Submission'
        submission.cgi_script = 'linkaward'
        submission.type = MOD_AWARD_LINK

        form = IsfdbFieldStorage()

        try:
                title_id = form['title_id'].value
                # Drop everything to the left of the last question mark in case a title URL was entered
                title_id = int(title_id.split('?')[-1])
                if title_id < 0:
                        raise
                if title_id == 0:
                        title_title = 'Unlink award'
                else:
                        title = SQLloadTitle(title_id)
                        if not title:
                                raise
                        title_title = title[TITLE_TITLE]
        except:
                submission.error('Non-existent title record specified')

        try:
                award_id = int(form['award_id'].value)
                award = awards(db)
                award.load(award_id)
                if not award.award_title:
                        raise
        except:
                submission.error('Non-existent award record specified')

        if not submission.user.id:
                submission.error('', award_id)

        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <LinkAward>\n"

        update_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))

        update_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(title_title)))
        update_string += "    <Award>%d</Award>\n" % (award_id)
        update_string += "    <Title>%d</Title>\n" % (title_id)
        if 'mod_note' in form:
                update_string += "    <ModNote>%s</ModNote>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(form['mod_note'].value)))
        update_string += "  </LinkAward>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
