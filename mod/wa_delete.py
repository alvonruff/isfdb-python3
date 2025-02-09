#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2021   Al von Ruff nad Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 674 $
#     Date: $Date: 2021-07-04 15:59:13 -0400 (Sun, 04 Jul 2021) $


from isfdb import *
from isfdblib import *
from common import *
from pubClass import *
from SQLparsing import *
from library import *
from awardClass import *


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Award Delete - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

	print "<h1>SQL Updates:</h1>"
	print "<hr>"
	print "<ul>"

	xml = SQLloadXML(submission)
	doc = minidom.parseString(XMLunescape2(xml))

        if doc.getElementsByTagName('AwardDelete'):
		merge = doc.getElementsByTagName('AwardDelete')
        	Record = GetElementValue(merge, 'Record')

                current = awards(db)
                current.load(int(Record))

		##########################################################
		# Delete award/title map
		##########################################################
		query = "delete from title_awards where award_id=%d" % current.award_id
		print "<li> ", query
		db.query(query)

                ##############################################################
                # Delete note
                ##############################################################
                if current.award_note_id:
                        delete = "delete from notes where note_id=%d" % int(current.award_note_id)
                        print "<li> ", delete
                        db.query(delete)

		##########################################################
		# Delete the award itself
		##########################################################
		query = "delete from awards where award_id=%d" % current.award_id
		print "<li> ", query
		db.query(query)

		submitter = GetElementValue(merge, 'Submitter')
		markIntegrated(db, submission, Record)

	print '<p>'

	PrintPostMod(0)
