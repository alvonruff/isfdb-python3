#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2013-2025   Ahasuerus, Klaus Elsbernd, Al von Ruff
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
from awardtypeClass import *

submission    = 0
submitter     = 0
reviewer      = 0

def UpdateColumn(doc, tag, column, id):
        if TagPresent(doc, tag):

                ###########################################
                # Get the old value
                ###########################################
                query = "select %s from award_types where award_type_id=%s" % (column, id)
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                from_value = record[0][0]

                value = GetElementValue(doc, tag)
                if value:
                        update = "update award_types set %s='%s' where award_type_id=%s" % (column, db.escape_string(value), id)
                else:
                        update = "update award_types set %s = NULL where award_type_id=%s" % (column, id)
                print("<li> ", update)
                db.query(update)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Award Type Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if not doc.getElementsByTagName('AwardTypeUpdate'):
                print('<div id="ErrorBox">')
                print('<h3>Invalid Submission</h3>')
                print('</div>')
                PrintPostMod()
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")
        merge = doc.getElementsByTagName('AwardTypeUpdate')
        subname = GetElementValue(merge, 'Submitter')
        submitter = SQLgetSubmitterID(subname)

        current = award_type()
        current.award_type_id = GetElementValue(merge, 'AwardTypeId')
        current.load()

        UpdateColumn(merge, 'ShortName',  'award_type_short_name',  current.award_type_id)

        UpdateColumn(merge, 'FullName',   'award_type_name',        current.award_type_id)

        UpdateColumn(merge, 'AwardedBy',  'award_type_by',          current.award_type_id)

        UpdateColumn(merge, 'AwardedFor', 'award_type_for',         current.award_type_id)

        UpdateColumn(merge, 'Poll',       'award_type_poll',        current.award_type_id)

        UpdateColumn(merge, 'NonGenre',   'award_type_non_genre',   current.award_type_id)

        value = GetElementValue(merge, 'Webpages')
        if value:
                ##########################################################
                # Construct the string of old webpage values
                ##########################################################
                webpages = SQLloadAwardTypeWebpages(current.award_type_id)
                from_value = ''
                for webpage in webpages:
                        if from_value == '':
                                from_value += webpage
                        else:
                                from_value += "," + webpage

                ##########################################################
                # Delete the old webpages
                ##########################################################
                delete = "delete from webpages where award_type_id=%s" % (current.award_type_id)
                print("<li> ", delete)
                db.query(delete)

                ##########################################################
                # Insert the new webpages
                ##########################################################
                to_value = ''
                webpages = doc.getElementsByTagName('Webpage')
                for webpage in webpages:
                        address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                        update = "insert into webpages(award_type_id, url) values(%s, '%s')" % (current.award_type_id, db.escape_string(address))
                        print("<li> ", update)
                        db.query(update)

                        # Construct the new list of webpages
                        if to_value == '':
                                to_value += address
                        else:
                                to_value += ","+address

        if TagPresent(merge, 'Note'):
                value = GetElementValue(merge, 'Note')
                if value:
                        ############################################################
                        # Check to see if this award type already has a note
                        ############################################################
                        query = "select award_type_note_id from award_types where award_type_id='%s' and award_type_note_id is not null and award_type_note_id<>'0';" % (current.award_type_id)
                        db.query(query)
                        res = db.store_result()
                        if res.num_rows():
                                rec = res.fetch_row()
                                note_id = rec[0][0]
                                print('<li> note_id:', note_id)
                                update = "update notes set note_note='%s' where note_id='%d'" % (db.escape_string(value), int(note_id))
                                print("<li> ", update)
                                db.query(update)
                        else:
                                insert = "insert into notes(note_note) values('%s');" % (db.escape_string(value))
                                db.query(insert)
                                retval = db.insert_id()
                                update = "update award_types set award_type_note_id='%d' where award_type_id='%s'" % (retval, current.award_type_id)
                                print("<li> ", update)
                                db.query(update)
                else:
                        ##############################################################
                        # An empty note submission was made - delete the previous note
                        ##############################################################
                        query = "select award_type_note_id from award_types where award_type_id=%s and award_type_note_id is not null and award_type_note_id<>'0';" % (current.award_type_id)
                        db.query(query)
                        res = db.store_result()
                        if res.num_rows():
                                rec = res.fetch_row()
                                note_id = rec[0][0]
                                delete = "delete from notes where note_id=%d" % (note_id)
                                print("<li> ", delete)
                                db.query(delete)
                                update = "update award_types set award_type_note_id=NULL where award_type_id=%s" % (current.award_type_id)
                                print("<li> ", update)
                                db.query(update)

        markIntegrated(db, submission, current.award_type_id)

        print(ISFDBLinkNoName('edit/editawardtype.cgi', current.award_type_id, 'Edit This Award Type', True))
        print(ISFDBLinkNoName('awardtype.cgi', current.award_type_id, 'View This Award Type', True))

        PrintPostMod(0)

