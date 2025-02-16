#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley, Ahasuerus and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended serieslication of such source code.
#
#     Version: $Revision: 750 $
#     Date: $Date: 2021-09-16 16:51:32 -0400 (Thu, 16 Sep 2021) $


from isfdb import *
from isfdblib import *
from common import *
from seriesClass import *
from SQLparsing import *
from library import *

debug = 0

def UpdateColumn(doc, tag, column, id):
        value = GetElementValue(doc, tag)
        if TagPresent(doc, tag):
                value = XMLunescape(value)
                value = db.escape_string(value)
                update = "update series set %s='%s' where series_id=%s" % (column, value, id)
                print("<li> ", update)
                if debug == 0:
                        db.query(update)



if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Series Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('SeriesUpdate'):
                merge = doc.getElementsByTagName('SeriesUpdate')
                Record = GetElementValue(merge, 'Record')

                UpdateColumn(merge, 'Name', 'series_title', Record)

                value = GetElementValue(merge, 'SeriesTransNames')
                if value:
                        # Delete the old transliterated names
                        delete = "delete from trans_series where series_id=%d" % int(Record)
                        print("<li> ", delete)
                        db.query(delete)

                        # Insert the new transliterated names
                        trans_names = doc.getElementsByTagName('SeriesTransName')
                        for trans_name in trans_names:
                                name = XMLunescape(trans_name.firstChild.data.encode('iso-8859-1'))
                                update = """insert into trans_series(series_id, trans_series_name)
                                            values(%d, '%s')""" % (int(Record), db.escape_string(name))
                                print("<li> ", update)
                                db.query(update)

                parent = GetElementValue(merge, 'Parent')
                #If the Parent element is present and the value is NULL, set the MySQL value to NULL
                if len(doc.getElementsByTagName('Parent')):
                        if not parent:
                                update = "update series set series_parent=NULL where series_id=%d" % (int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                               db.query(update)
                if parent:
                        # STEP 1 - Look to see if parent exists
                        query = "select series_id from series where series_title='%s'" % (db.escape_string(parent))
                        db.query(query)
                        res = db.store_result()
                        if res.num_rows():
                                record = res.fetch_row()
                                series_id = record[0][0]
                                update = "update series set series_parent='%d' where series_id=%d" % (series_id, int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)
                        else:
                                query = "insert into series(series_title) values('%s');" % (db.escape_string(parent))
                                print("<li> ", query)
                                if debug == 0:
                                        db.query(query)
                                series_id = db.insert_id()
                                update = "update series set series_parent='%d' where series_id=%d" % (series_id, int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)

                parentposition = GetElementValue(merge, 'Parentposition')
                #If the ParentPosition element is present and the value is NULL, set the MySQL value to NULL
                if len(doc.getElementsByTagName('Parentposition')):
                        if not parentposition:
                                update = "update series set series_parent_position=NULL where series_id=%d" % (int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                               db.query(update)
                        else:
                                update = "update series set series_parent_position=%s where series_id=%d" % (int(parentposition), int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                               db.query(update)

                value = GetElementValue(merge, 'Webpages')
                if value:
                        ##########################################################
                        # Construct the string of old webpage values
                        ##########################################################
                        webpages = SQLloadSeriesWebpages(int(Record))

                        ##########################################################
                        # Delete the old webpages
                        ##########################################################
                        delete = "delete from webpages where series_id=%s" % (Record)
                        print("<li> ", delete)
                        db.query(delete)

                        ##########################################################
                        # Insert the new webpages
                        ##########################################################
                        webpages = doc.getElementsByTagName('Webpage')
                        for webpage in webpages:
                                address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                                update = "insert into webpages(series_id, url) values(%s, '%s')" % (Record, db.escape_string(address))
                                print("<li> ", update)
                                db.query(update)
                if TagPresent(merge, 'Note'):
                        value = GetElementValue(merge, 'Note')
                        if value:
                                ############################################################
                                # Check to see if this publication series already has a note
                                ############################################################
                                query = "select series_note_id from series where series_id='%s' and series_note_id is not null and series_note_id<>'0';" % (Record)
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
                                        update = "update series set series_note_id='%d' where series_id='%s'" % (retval, Record)
                                        print("<li> ", update)
                                        db.query(update)
                        else:
                                ##############################################################
                                # An empty note submission was made - delete the previous note
                                ##############################################################
                                query = "select series_note_id from series where series_id=%s and series_note_id is not null and series_note_id<>'0';" % (Record)
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        rec = res.fetch_row()
                                        note_id = rec[0][0]
                                        delete = "delete from notes where note_id=%d" % (note_id)
                                        print("<li> ", delete)
                                        db.query(delete)
                                        update = "update series set series_note_id=NULL where series_id=%s" % (Record)
                                        print("<li> ", update)
                                        db.query(update)

                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission, Record)

        print(ISFDBLinkNoName('edit/editseries.cgi', Record, 'Edit This Series', True))
        print(ISFDBLinkNoName('pe.cgi', Record, 'View This Series', True))

        print('<p>')

        PrintPostMod(0)
