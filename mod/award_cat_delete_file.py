#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 676 $
#     Date: $Date: 2021-07-05 12:14:45 -0400 (Mon, 05 Jul 2021) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from awardcatClass import *


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Award Category Delete - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('AwardCategoryDelete')
        if not merge:
                print '<div id="ErrorBox">'
                print '<h3>Error: Bad argument</h3>'
                print '</div>'
                PrintPostMod()
                sys.exit(0)

        print "<h1>SQL Updates:</h1>"
        print "<hr>"
        print "<ul>"

        current = award_cat()
        current.award_cat_id = int(GetElementValue(merge, 'AwardCategoryId'))
        current.load()

        ##############################################################
        # Delete webpages
        ##############################################################
        delete = "delete from webpages where award_cat_id=%d" % current.award_cat_id
        print "<li> ", delete
        db.query(delete)

        ##############################################################
        # Delete note
        ##############################################################
        if current.award_cat_note_id:
                delete = "delete from notes where note_id=%d" % current.award_cat_note_id
                print "<li> ", delete
                db.query(delete)

        ##############################################################
        # Delete award category record
        ##############################################################
        delete = "delete from award_cats where award_cat_id=%d" % current.award_cat_id
        print "<li> ", delete
        db.query(delete)

        markIntegrated(db, submission, current.award_cat_id)

        PrintPostMod(0)
