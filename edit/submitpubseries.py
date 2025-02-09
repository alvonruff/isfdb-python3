#!_PYTHONLOC
#
#     (C) COPYRIGHT 2010-2022   Ahasuerus
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
from pubseriesClass import *
from SQLparsing import *


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Publication Series Change Submission'
        submission.cgi_script = 'editpubseries'
        submission.type = MOD_PUB_SERIES_UPDATE

	new = pub_series(db)
	new.cgi2obj()
	if new.error:
                submission.error(new.error)

	if not submission.user.id:
                submission.error('', new.pub_series_id)
	
	old = pub_series(db)
	old.load(int(new.pub_series_id))
	
	changes = 0
	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <PubSeriesUpdate>\n"
	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
	update_string += "    <Record>%d</Record>\n" % (int(new.pub_series_id))
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(old.pub_series_name)))
	
	(changes, update) = submission.CheckField(new.used_name, old.used_name, new.pub_series_name, old.pub_series_name, 'Name', 0)
	if changes:
		update_string += update

	(changes, update) = submission.CheckField(new.used_trans_names, old.used_trans_names,
                                                  new.pub_series_trans_names, old.pub_series_trans_names, 'PubSeriesTransName', 1)
	if changes:
		update_string += update

	(changes, update) = submission.CheckField(new.used_note, old.used_note, new.pub_series_note, old.pub_series_note, 'Note', 0)
	if changes:
		update_string += update
	(changes, update) = submission.CheckField(new.used_webpages, old.used_webpages, new.pub_series_webpages, old.pub_series_webpages, 'Webpage', 1)
	if changes:
		update_string += update

	if new.form.has_key('mod_note'):
		update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))
	
	update_string += "  </PubSeriesUpdate>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
