#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2023   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1070 $
#     Date: $Date: 2023-01-05 17:56:54 -0500 (Thu, 05 Jan 2023) $


from isfdb import *
from SQLparsing import *
from isfdblib import *
from publisherClass import publishers

debug        = 0
MaxRecords   = 0
RecordNumber = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Records      = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def Compare2(fieldname, values, note = 0):

	checked_entry = 1
	recno = 1
	while recno < MaxRecords:
        	if values[0] != values[recno]:
			print '<tr align="left">'
			print '<td class="drop">'
			print "<b>" +fieldname+ " Conflict:</b><br>"
			index = 1
			for value in values:
				if index == checked_entry:
					print '<INPUT TYPE="radio" NAME="' +fieldname+ '" VALUE="%s" checked="checked">' % (index)
				else:
					print '<INPUT TYPE="radio" NAME="' +fieldname+ '" VALUE="%s">' % (index)
				index += 1
				if note:
                                        print value
                                else:
                                        print ISFDBText(value)
				print '<br>'
			print '</td>'
			print '</tr>'
			return
		recno += 1
	print '<tr align="left">'
	print '<td class="keep">'
	print "<b>Merged " +fieldname+ ": </b>", values[0]
	print '</td>'
	print '</tr>'

def Merge2(fieldname, values):

	print '<tr align=left>'
	print '<td class="keep">'
	print "<b>Merged " +fieldname+ " </b><br>"
	for value in values:
		if value:
			print ISFDBText(value)
			print "<br>"
	print '</td>'
	print '</tr>'

def SelectionError():
	print "<h1>Error: You need to select at least two records to merge.</h1>"
	print "</body>\n"
	print "</html>\n"
	PrintPostSearch(0, 0, 0, 0, 0)
	sys.exit(1)


if __name__ == '__main__':
	PrintPreSearch("Publisher Merge Results")
	PrintNavBar(0, 0)

	##################################################################
	# Gather the form input
	##################################################################
	sys.stderr = sys.stdout
	form = cgi.FieldStorage()
	if form.has_key('merge'):
		while 1:
			try:
				RecordNumber[MaxRecords] = form['merge'][MaxRecords].value
			except:
				break
			MaxRecords += 1
		rec = 0
		print '<h2>Merging Records: '
		while rec < MaxRecords:
			print RecordNumber[rec]
			rec += 1
		print '</h2>'
		print '<hr>'
	else:
		SelectionError()

	if MaxRecords < 1:
		SelectionError()

	##################################################
	# Load in all of the data records
	##################################################
	recno = 0
	while recno < MaxRecords:
        	Records[recno] = publishers(db)
        	Records[recno].load(int(RecordNumber[recno]))
		recno += 1

	print '<form METHOD="POST" ACTION="/cgi-bin/edit/ps_merge.cgi">'
	print '<table class="generic_table">'

	##################################################
	# publisher_name
	##################################################
	record_list = []
	recno = 0
	while recno < MaxRecords:
		record_list.append(Records[recno].publisher_name)
		recno += 1
	Compare2("publisher_name", record_list)

	##################################################
	# publisher_webpages 	 
	################################################## 	 
	record_list = [] 	 
	recno = 0 	 
	while recno < MaxRecords: 	 
		for webpage in Records[recno].publisher_webpages:
                        if webpage not in record_list:
                                record_list.append(webpage)
		recno += 1 	 
	Merge2("publisher_webpages", record_list)

	##################################################
	# publisher_trans_names 	 
	################################################## 	 
	record_list = [] 	 
	recno = 0 	 
	while recno < MaxRecords: 	 
		for publisher_trans_name in Records[recno].publisher_trans_names:
                        if publisher_trans_name not in record_list:
                                record_list.append(publisher_trans_name)
		recno += 1 	 
	Merge2("publisher_trans_names", record_list)

	##################################################
	# publisher_note
	##################################################
	record_list = []
	recno = 0
	while recno < MaxRecords:
		record_list.append(Records[recno].publisher_note)
		recno += 1
	Compare2("publisher_note", record_list, 1)

	print '</table>'
	print '<p>'

	recno = 0
	while recno < MaxRecords:
		print '<input NAME="record%s" VALUE="%s" TYPE="HIDDEN">' % ((recno+1), RecordNumber[recno])
		recno += 1

	print '<input TYPE="SUBMIT" VALUE="Complete Merge">'
	print '</form>'

	PrintPostSearch(0, 0, 0, 0, 0, 0)
