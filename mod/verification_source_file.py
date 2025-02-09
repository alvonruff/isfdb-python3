#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 696 $
#     Date: $Date: 2021-08-13 16:03:00 -0400 (Fri, 13 Aug 2021) $

from isfdb import *
from SQLparsing import *
from library import GetElementValue, ISFDBLink, XMLunescape2, TagPresent
from isfdblib import PrintPreMod, PrintNavBar, PrintPostMod, NotApprovable, markIntegrated
from xml.dom import minidom


submission    = 0
submitter     = 0
reviewer      = 0

def UpdateColumn(doc, tag, column, record_id):
	if TagPresent(doc, tag):
		query = "select %s from reference where reference_id = %d" % (column, record_id)
       		db.query(query)
		result = db.store_result()
		record = result.fetch_row()

		value = GetElementValue(doc, tag)
        	if value:
			update = "update reference set %s = '%s' where reference_id = %d" % (column, db.escape_string(value), record_id)
		else:
			update = "update reference set %s = NULL where reference_id = %d" % (column, record_id)
		print "<li> ", update
       		db.query(update)

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

	PrintPreMod('Verification Source Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

	print "<h1>SQL Updates:</h1>"
	print "<hr>"
	print "<ul>"

	xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('VerificationSource'):
		merge = doc.getElementsByTagName('VerificationSource')
        	Record = int(GetElementValue(merge, 'Record'))
		subname = GetElementValue(merge, 'Submitter')
		submitter = SQLgetSubmitterID(subname)

		UpdateColumn(merge, 'SourceLabel', 'reference_label',  Record)
		UpdateColumn(merge, 'SourceName',  'reference_fullname',  Record)
		UpdateColumn(merge, 'SourceURL',   'reference_url',  Record)

		markIntegrated(db, submission, Record)

	print ISFDBLink('edit/edit_verification_source.cgi', Record, 'Edit This Verification Source', 1)
	print ISFDBLink('mod/list_verification_sources.cgi', '', 'View Verification Sources', 1)

	PrintPostMod(0)
