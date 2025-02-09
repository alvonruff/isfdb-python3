#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2022  Al von Ruff, Bill Longley and Ahasuerus
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
from seriesClass import *
from SQLparsing import *
from login import *
from library import *
from navbar import *


def CheckSeriesField(newUsed, oldUsed, newField, oldField, tag, multi):
	update = 0
	changes = 0
	update_string = ''

	######################################################################
	# If a field is and was being used, update it only if it's different
	######################################################################
	if newUsed and oldUsed:
                if multi:
                        update = compare_lists(newField, oldField)
                else:
                        if newField != XMLescape(oldField):
                                update = 1

	######################################################################
	# If a field is being used, but wasn't before, update it
	######################################################################
	elif newUsed and (oldUsed == 0):
		update = 1

	######################################################################
	# If a field is not being used, but it was before, update it
	######################################################################
	elif (newUsed == 0) and oldUsed:
		newField = ""
		update = 1

	if update:
		if multi:
			update_string = "    <%ss>\n" % (tag)
			for field in newField:
				update_string += "      <%s>%s</%s>\n" % (tag, db.escape_string(field), tag)
			update_string += "    </%ss>\n" % (tag)
		else:
			update_string = "    <%s>%s</%s>\n" % (tag, db.escape_string(newField), tag)

		changes = 1
	return (changes, update_string)


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Series Change Submission'
        submission.cgi_script = 'editseries'
        submission.type = MOD_SERIES_UPDATE

	new = series(db)
	new.cgi2obj()
	if new.error:
                submission.error(new.error)

	if not submission.user.id:
                submission.error('', new.series_id)

	old = series(db)
	old.loadXML(int(new.series_id))

	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <SeriesUpdate>\n"
	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(old.series_name)))
	update_string += "    <Record>%d</Record>\n" % (int(new.series_id))

	(changes, update) = CheckSeriesField(new.used_name, old.used_name, new.series_name, old.series_name, 'Name', 0)
	if changes:
                update_string += update

	(changes, update) = CheckSeriesField(new.used_trans_names, old.used_trans_names, new.series_trans_names, old.series_trans_names, 'SeriesTransName', 1)
	if changes:
		update_string += update

	(changes, update) = CheckSeriesField(new.used_parent, old.used_parent, new.series_parent, old.series_parent, 'Parent', 0)
	if changes:
                update_string += update

	(changes, update) = CheckSeriesField(new.used_parentposition, old.used_parentposition, new.series_parentposition, old.series_parentposition, 'Parentposition', 0)
	if changes:
                update_string += update

	(changes, update) = CheckSeriesField(new.used_note, old.used_note, new.series_note, old.series_note, 'Note', 0)
	if changes:
		update_string += update

	(changes, update) = CheckSeriesField(new.used_webpages, old.used_webpages, new.series_webpages, old.series_webpages, 'Webpage', 1)
	if changes:
		update_string += update

	if new.form.has_key('mod_note'):
		update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))
	
	update_string += "  </SeriesUpdate>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
