#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 752 $
#     Date: $Date: 2021-09-17 18:33:04 -0400 (Fri, 17 Sep 2021) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from awardcatClass import *


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Add New Award Category - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('NewAwardCat')
        if not merge:
                print '<div id="ErrorBox">'
                print '<h3>Error: Bad argument</h3>'
                print '</div>'
                PrintPostMod()
                sys.exit(0)

        print "<h1>SQL Updates:</h1>"
        print "<hr>"
        print "<ul>"
        subname = GetElementValue(merge, 'Submitter')
        submitter = SQLgetSubmitterID(subname)
        AwardCatName = GetElementValue(merge, 'AwardCatName')
        AwardTypeId = GetElementValue(merge, 'AwardTypeId')
        DisplayOrder = GetElementValue(merge, 'DisplayOrder')

        #######################################
        # Insert into the award category  table
        #######################################
        if not DisplayOrder:
                insert = "insert into award_cats(award_cat_name, award_cat_type_id, award_cat_order) values('%s', %d, NULL)" % (db.escape_string(AwardCatName), int(AwardTypeId))
        else:
                insert = "insert into award_cats(award_cat_name, award_cat_type_id, award_cat_order) values('%s', %d, %d)" % (db.escape_string(AwardCatName), int(AwardTypeId), int(DisplayOrder))
        print "<li> ", insert
        db.query(insert)
        award_cat_id = int(db.insert_id())

        #####################################
        # NOTE
        #####################################
        note_id = ''
        note = GetElementValue(merge, 'Note')
        if note:
                insert = "insert into notes(note_note) values('%s');" % db.escape_string(note)
                print "<li> ", insert
                db.query(insert)
                note_id = int(db.insert_id())
                update = "update award_cats set award_cat_note_id = %d where award_cat_id=%d" % (note_id, award_cat_id)
                print "<li> ", update
                db.query(update)

        ##########################################################
        # Insert the new webpages
        ##########################################################

        value = GetElementValue(merge, 'Webpages')
        if value:
                webpages = doc.getElementsByTagName('Webpage')
                for webpage in webpages:
                        address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                        update = "insert into webpages(award_cat_id, url) values(%d, '%s')" % (award_cat_id, db.escape_string(address))
                        print "<li> ", update
                        db.query(update)

        markIntegrated(db, submission, award_cat_id)

        print ISFDBLinkNoName('award_category.cgi', '%d+1' % award_cat_id, 'View This Category', True)
        print ISFDBLinkNoName('awardtype.cgi', AwardTypeId, 'View This Category\'s Award Type', True)

        PrintPostMod(0)
