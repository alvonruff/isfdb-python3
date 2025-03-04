#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus, Klaus Elsbernd, Al von Ruff
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

submission    = 0
submitter     = 0
reviewer      = 0

def UpdateColumn(doc, tag, column, id):
        if TagPresent(doc, tag):

                ###########################################
                # Get the old value
                ###########################################
                query = "select %s from award_cats where award_cat_id=%d" % (column, int(id))
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHONE()
                from_value = record[0][0]

                value = GetElementValue(doc, tag)
                if value:
                        update = "update award_cats set %s='%s' where award_cat_id=%d" % (column, CNX.DB_ESCAPE_STRING(value), int(id))
                else:
                        update = "update award_cats set %s = NULL where award_cat_id=%d" % (column, int(id))
                print("<li> ", update)
                CNX.DB_QUERY(update)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Award Category Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if not doc.getElementsByTagName('AwardCategoryUpdate'):
                print('<div id="ErrorBox">')
                print('<h3>Error: Bad argument</h3>')
                print('</div>')
                PrintPostMod()
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")
        merge = doc.getElementsByTagName('AwardCategoryUpdate')
        subname = GetElementValue(merge, 'Submitter')
        submitter = SQLgetSubmitterID(subname)

        current = award_cat()
        current.award_cat_id = GetElementValue(merge, 'AwardCategoryId')
        current.load()

        UpdateColumn(merge, 'CategoryName',   'award_cat_name',        current.award_cat_id)

        UpdateColumn(merge, 'DisplayOrder',   'award_cat_order',       current.award_cat_id)

        CNX = MYSQL_CONNECTOR()
        value = GetElementValue(merge, 'Webpages')
        if value:
                ##########################################################
                # Construct the string of old webpage values
                ##########################################################
                webpages = SQLloadAwardCatWebpages(current.award_cat_id)
                from_value = ''
                for webpage in webpages:
                        if from_value == '':
                                from_value += webpage
                        else:
                                from_value += "," + webpage

                ##########################################################
                # Delete the old webpages
                ##########################################################
                delete = "delete from webpages where award_cat_id=%d" % int(current.award_cat_id)
                print("<li> ", delete)
                CNX.DB_QUERY(delete)

                ##########################################################
                # Insert the new webpages
                ##########################################################
                to_value = ''
                webpages = doc.getElementsByTagName('Webpage')
                for webpage in webpages:
                        address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                        update = "insert into webpages(award_cat_id, url) values(%d, '%s')" % (int(current.award_cat_id), CNX.DB_ESCAPE_STRING(address))
                        print("<li> ", update)
                        CNX.DB_QUERY(update)

                        # Construct the new list of webpages
                        if to_value == '':
                                to_value += address
                        else:
                                to_value += ","+address

        if TagPresent(merge, 'Note'):
                value = GetElementValue(merge, 'Note')
                if value:
                        ############################################################
                        # Check to see if this award category already has a note
                        ############################################################
                        query = "select award_cat_note_id from award_cats where award_cat_id=%d and \
                                 award_cat_note_id is not null and award_cat_note_id<>'0'" % int(current.award_cat_id)
                        CNX.DB_QUERY(query)
                        if CNX.DB_NUMROWS():
                                rec = CNX.DB_FETCHONE()
                                note_id = rec[0][0]
                                print('<li> note_id:', note_id)
                                update = "update notes set note_note='%s' where note_id='%d'" % (CNX.DB_ESCAPE_STRING(value), int(note_id))
                                print("<li> ", update)
                                CNX.DB_QUERY(update)
                        else:
                                insert = "insert into notes(note_note) values('%s')" % (CNX.DB_ESCAPE_STRING(value))
                                CNX.DB_QUERY(insert)
                                retval = CNX.DB_INSERT_ID()
                                update = "update award_cats set award_cat_note_id=%d where award_cat_id=%d" % (int(retval), int(current.award_cat_id))
                                print("<li> ", update)
                                CNX.DB_QUERY(update)
                else:
                        ##############################################################
                        # An empty note submission was made - delete the previous note
                        ##############################################################
                        query = "select award_cat_note_id from award_cats where award_cat_id=%d and award_cat_note_id \
                                 is not null and award_cat_note_id<>'0'" % int(current.award_cat_id)
                        CNX.DB_QUERY(query)
                        if CNX.DB_NUMROWS():
                                rec = CNX.DB_FETCHONE()
                                note_id = rec[0][0]
                                delete = "delete from notes where note_id=%d" % (note_id)
                                print("<li> ", delete)
                                CNX.DB_QUERY(delete)
                                update = "update award_cats set award_cat_note_id=NULL where award_cat_id=%d" % int(current.award_cat_id)
                                print("<li> ", update)
                                CNX.DB_QUERY(update)

        markIntegrated(db, submission, current.award_cat_id)

        print(ISFDBLinkNoName('edit/editawardcat.cgi', current.award_cat_id, 'Edit This Award Category', True))
        print(ISFDBLinkNoName('award_category.cgi', current.award_cat_id, 'View This Award Category', True))

        PrintPostMod(0)

