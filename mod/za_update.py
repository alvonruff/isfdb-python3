#!_PYTHONLOC
#
#     (C) COPYRIGHT 2010-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 729 $
#     Date: $Date: 2021-09-02 12:08:46 -0400 (Thu, 02 Sep 2021) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from pubseriesClass import *

submission    = 0
submitter     = 0
reviewer      = 0

def UpdateColumn(doc, tag, column, id):
	if TagPresent(doc, tag):

		###########################################
		# Get the old value
		###########################################
		query = "select %s from pub_series where pub_series_id=%s" % (column, id)
       		db.query(query)
		result = db.store_result()
		record = result.fetch_row()

		value = GetElementValue(doc, tag)
        	if value:
			update = "update pub_series set %s='%s' where pub_series_id=%s" % (column, db.escape_string(value), id)
		else:
			update = "update pub_series set %s = NULL where pub_series_id=%s" % (column, id)
		print "<li> ", update
       		db.query(update)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

	PrintPreMod('Publication Series Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

	print "<h1>SQL Updates:</h1>"
	print "<hr>"
	print "<ul>"

	xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('PubSeriesUpdate'):
		merge = doc.getElementsByTagName('PubSeriesUpdate')
        	Record = GetElementValue(merge, 'Record')
		subname = GetElementValue(merge, 'Submitter')
		submitter = SQLgetSubmitterID(subname)

		current = pub_series(db)
		current.load(int(Record))

		UpdateColumn(merge, 'Name',  'pub_series_name',  Record)

		value = GetElementValue(merge, 'PubSeriesTransNames')
        	if value:
			##########################################################
			# Delete the old transliterated names
			##########################################################
			delete = "delete from trans_pub_series where pub_series_id=%s" % (Record)
			print "<li> ", delete
        		db.query(delete)

			##########################################################
			# Insert the new transliterated names
			##########################################################
			trans_names = doc.getElementsByTagName('PubSeriesTransName')
			for trans_name in trans_names:
                                name = XMLunescape(trans_name.firstChild.data.encode('iso-8859-1'))
                                update = """insert into trans_pub_series(pub_series_id, trans_pub_series_name)
                                            values(%d, '%s')""" % (int(Record), db.escape_string(name))
                                print "<li> ", update
                                db.query(update)

		value = GetElementValue(merge, 'Webpages')
        	if value:
			##########################################################
			# Delete the old webpages
			##########################################################
			delete = "delete from webpages where pub_series_id=%s" % (Record)
			print "<li> ", delete
        		db.query(delete)

			##########################################################
			# Insert the new webpages
			##########################################################
			webpages = doc.getElementsByTagName('Webpage')
			for webpage in webpages:
                                address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                                update = "insert into webpages(pub_series_id, url) values(%s, '%s')" % (Record, db.escape_string(address))
                                print "<li> ", update
                                db.query(update)

		if TagPresent(merge, 'Note'):
                        value = GetElementValue(merge, 'Note')
                        if value:
				############################################################
				# Check to see if this publication series already has a note
				############################################################
                                query = "select pub_series_note_id from pub_series where pub_series_id='%s' and pub_series_note_id is not null and pub_series_note_id<>'0';" % (Record)
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        rec = res.fetch_row()
                                        note_id = rec[0][0]
                                        print '<li> note_id:', note_id
                                        update = "update notes set note_note='%s' where note_id='%d'" % (db.escape_string(value), int(note_id))
                                        print "<li> ", update
                                        db.query(update)
                                else:
                                        insert = "insert into notes(note_note) values('%s');" % (db.escape_string(value))
                                        db.query(insert)
                                        retval = db.insert_id()
                                        update = "update pub_series set pub_series_note_id='%d' where pub_series_id='%s'" % (retval, Record)
                                        print "<li> ", update
                                        db.query(update)
			else:
				##############################################################
				# An empty note submission was made - delete the previous note
				##############################################################
				query = "select pub_series_note_id from pub_series where pub_series_id=%s and pub_series_note_id is not null and pub_series_note_id<>'0';" % (Record)
				db.query(query)
				res = db.store_result()
				if res.num_rows():
					rec = res.fetch_row()
					note_id = rec[0][0]
					delete = "delete from notes where note_id=%d" % (note_id)
					print "<li> ", delete
					db.query(delete)
					update = "update pub_series set pub_series_note_id=NULL where pub_series_id=%s" % (Record)
					print "<li> ", update
					db.query(update)

		markIntegrated(db, submission, Record)

	print ISFDBLinkNoName('edit/editpubseries.cgi', Record, 'Edit This Publication Series', True)
	print ISFDBLinkNoName('pubseries.cgi', Record, 'View This Publication Series', True)

	PrintPostMod(0)

