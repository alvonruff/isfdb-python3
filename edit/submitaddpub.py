#!_PYTHONLOC
#
#     (C) COPYRIGHT 2017-2022   Ahasuerus
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
        submission.header = 'Publication Add Submission'
        submission.type = MOD_PUB_NEW
        submission.cgi_script = 'addpub'

	new = pubs(db)
	new.cgi2obj('implied')
	if new.error:
                submission.error(new.error)

	if not submission.user.id:
                submission.error('', new.title_id)
	
	old = pubs(db)
	old.load(int(new.pub_id))

	changes = 0
	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
        update_string += "  <NewPub>\n"
	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(new.pub_title))
        update_string += "    <Parent>%d</Parent>\n" % (int(new.title_id))

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

        if new.identifiers:
		update_string += new.xmlIdentifiers()

	(val, changed) = EvalField('Price', new.used_price, old.used_price, new.pub_price, old.pub_price)
	update_string += val
	changes += changed

	(val, changed) = EvalField('Image', new.used_image, old.used_image, new.pub_image, old.pub_image)
	update_string += val
	changes += changed

	(val, changed) = EvalField('Note', new.used_note, old.used_note, new.pub_note, old.pub_note)
	update_string += val
	changes += changed

	if new.form.has_key('mod_note'):
		update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))

	if new.form.has_key('Source'):
		update_string += "    <Source>%s</Source>\n" % (db.escape_string(XMLescape(new.form['Source'].value)))

			
	#############################################################
	# Authors
	#############################################################
	update = 0
	if new.num_authors != old.num_authors:
		update = 1
	else:
		counter = 0
		while counter < new.num_authors:
			if new.pub_authors[counter] != XMLescape(old.pub_authors[counter]):
					update = 1
					break
			counter += 1
	if update:
		update_string += "    <Authors>\n"
		counter = 0
		while counter < new.num_authors:
			update_string += "      <Author>%s</Author>\n" % (db.escape_string(new.pub_authors[counter]))
			counter += 1
		update_string += "    </Authors>\n"

        # Transliterated titles
	(changed, val) = submission.CheckField(new.used_trans_titles, old.used_trans_titles,
                                                  new.pub_trans_titles, old.pub_trans_titles, 'TransTitle', 1)
	changes += changed
	if changed:
		update_string += val

        # Web pages
	(changed, val) = submission.CheckField(new.used_webpages, old.used_webpages,
                                                  new.pub_webpages, old.pub_webpages, 'PubWebpage', 1)
	changes += changed
	if changed:
		update_string += val

	# Build the XML payload for the Content section
	update_string += db.escape_string(new.xmlContent())
        update_string += "  </NewPub>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
