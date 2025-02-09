#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2022   Al von Ruff, Bill Longley and Ahasuerus
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
	
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'New Award Submission'
        submission.cgi_script = 'addaward'
        submission.type = MOD_AWARD_NEW

	new = awards(db)
	new.cgi2obj()
	if new.error:
                submission.error(new.error)

	if not submission.user.id:
                submission.error()

        # For title-based awards, load the associated title record
        if int(new.title_id):
                title = SQLloadTitle(new.title_id)
                subject = XMLescape(title[TITLE_TITLE])
        else:
                subject = new.award_title

	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <NewAward>\n"
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(subject))
	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))

	if int(new.title_id):
		update_string += "    <Record>%d</Record>\n" % (int(new.title_id))
	else:
                update_string += "    <AwardTitle>%s</AwardTitle>\n" % (db.escape_string(new.award_title))

        if new.num_authors:
                update_string += "    <AwardAuthors>\n"
                counter = 0
                while counter < new.num_authors:
                        update_string += "      <AwardAuthor>%s</AwardAuthor>\n" % (db.escape_string(new.award_authors[counter]))
                        counter += 1
                update_string += "    </AwardAuthors>\n"

	if new.used_type_id:
		update_string += "    <AwardType>%d</AwardType>\n" % (int(new.award_type_id))

	if new.used_year:
		update_string += "    <AwardYear>%s</AwardYear>\n" % (db.escape_string(new.award_year))

	if new.used_cat_id:
		update_string += "    <AwardCategory>%d</AwardCategory>\n" % (int(new.award_cat_id))

	if new.used_level:
		update_string += "    <AwardLevel>%s</AwardLevel>\n" % (db.escape_string(new.award_level))

	if new.used_movie:
		update_string += "    <AwardMovie>%s</AwardMovie>\n" % (db.escape_string(new.award_movie))

	if new.used_note:
		update_string += "    <AwardNote>%s</AwardNote>\n" % (db.escape_string(new.award_note))

	if new.form.has_key('mod_note'):
		update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))

	update_string += "  </NewAward>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
