#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Klaus Elsbernd, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1263 $
#     Date: $Date: 2026-02-19 16:39:39 -0500 (Thu, 19 Feb 2026) $

import sys
if sys.version_info.major == 3:
        PYTHONVER = "python3"
elif sys.version_info.major == 2:
        PYTHONVER = "python2"

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
                print('<div id="ErrorBox">')
                print('<h3>Error: Bad argument</h3>')
                print('</div>')
                PrintPostMod()
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")
        subname = GetElementValue(merge, 'Submitter')
        submitter = SQLgetSubmitterID(subname)
        AwardCatName = GetElementValue(merge, 'AwardCatName')
        AwardTypeId = GetElementValue(merge, 'AwardTypeId')
        DisplayOrder = GetElementValue(merge, 'DisplayOrder')

        #######################################
        # Insert into the award category  table
        #######################################
        CNX = MYSQL_CONNECTOR()
        if not DisplayOrder:
                insert = "insert into award_cats(award_cat_name, award_cat_type_id, award_cat_order) values('%s', %d, NULL)" % (CNX.DB_ESCAPE_STRING(AwardCatName), int(AwardTypeId))
        else:
                insert = "insert into award_cats(award_cat_name, award_cat_type_id, award_cat_order) values('%s', %d, %d)" % (CNX.DB_ESCAPE_STRING(AwardCatName), int(AwardTypeId), int(DisplayOrder))
        print("<li> ", insert)
        CNX.DB_QUERY(insert)
        award_cat_id = int(CNX.DB_INSERT_ID())

        #####################################
        # NOTE
        #####################################
        note_id = ''
        note = GetElementValue(merge, 'Note')
        if note:
                insert = "insert into notes(note_note) values('%s');" % CNX.DB_ESCAPE_STRING(note)
                print("<li> ", insert)
                CNX.DB_QUERY(insert)
                note_id = int(CNX.DB_INSERT_ID())
                update = "update award_cats set award_cat_note_id = %d where award_cat_id=%d" % (note_id, award_cat_id)
                print("<li> ", update)
                CNX.DB_QUERY(update)

        ##########################################################
        # Insert the new webpages
        ##########################################################

        value = GetElementValue(merge, 'Webpages')
        if value:
                webpages = doc.getElementsByTagName('Webpage')
                for webpage in webpages:
                        if PYTHONVER == 'python2':
                                address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                        else:
                                address = XMLunescape(webpage.firstChild.data)
                        update = "insert into webpages(award_cat_id, url) values(%d, '%s')" % (award_cat_id, CNX.DB_ESCAPE_STRING(address))
                        print("<li> ", update)
                        CNX.DB_QUERY(update)

        markIntegrated(db, submission, award_cat_id)

        print(ISFDBLinkNoName('award_category.cgi', '%d+1' % award_cat_id, 'View This Category', True))
        print(ISFDBLinkNoName('awardtype.cgi', AwardTypeId, 'View This Category\'s Award Type', True))

        PrintPostMod(0)
