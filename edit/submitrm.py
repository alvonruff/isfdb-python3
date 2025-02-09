#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2022   Al von Ruff, Bill Longley and Ahasuerus
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
from SQLparsing import *
from login import *
from library import *
from navbar import *
	

if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Remove Titles Submission'
        submission.cgi_script = 'rmtitles'
        submission.type = MOD_RMTITLE

        form = cgi.FieldStorage()

	try:
		pubid = int(form['pub_id'].value)
                pub = SQLGetPubById(pubid)
                pub_title = pub[PUB_TITLE]
	except:
                submission.error("Valid publication ID must be provided")

	if not submission.user.id:
                submission.error("", pubid)

	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <TitleRemove>\n"
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(pub_title)))
	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
	update_string += "    <Record>%d</Record>\n" % (pubid)

        try:
                entry = 1
                while entry < 2000:
                        name = 'cover%d' % entry
                        if form.has_key(name):
                                val = form[name].value
                                update_string += "    <CoverRecord>%d</CoverRecord>\n" % (int(val))
                        else:
                                pass
                        entry += 1

                entry = 1
                while entry < 2000:
                        name = 'title%d' % entry
                        if form.has_key(name):
                                val = form[name].value
                                update_string += "    <TitleRecord>%d</TitleRecord>\n" % (int(val))
                        else:
                                pass
                        entry += 1

                entry = 1
                while entry < 2000:
                        name = 'review%d' % entry
                        if form.has_key(name):
                                val = form[name].value
                                update_string += "    <ReviewRecord>%d</ReviewRecord>\n" % (int(val))
                        else:
                                pass
                        entry += 1

                entry = 1
                while entry < 2000:
                        name = 'interview%d' % entry
                        if form.has_key(name):
                                val = form[name].value
                                update_string += "    <InterviewRecord>%d</InterviewRecord>\n" % (int(val))
                        else:
                                pass
                        entry += 1
        except:
                submission.error("Selected title IDs must be integer numbers")

	try:
                if val:
                        pass
        except:
                submission.error("At least one title must be selected")

	if form.has_key('mod_note'):
		update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(form['mod_note'].value)))

	update_string += "  </TitleRemove>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
