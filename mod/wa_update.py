#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Ahasuerus and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 744 $
#     Date: $Date: 2021-09-14 19:17:46 -0400 (Tue, 14 Sep 2021) $


from isfdb import *
from isfdblib import *
from common import *
from awardClass import *
from awardtypeClass import *
from SQLparsing import *
from common import *
from library import *

debug = 0

def UpdateColumn(doc, tag, column, id):
        if TagPresent(doc, tag):
                value = GetElementValue(doc, tag)
                if value:
                        value = XMLunescape(value)
                        value = db.escape_string(value)
                        update = "update awards set %s='%s' where award_id=%s" % (column, value, id)
                else:
                        update = "update awards set %s=NULL where award_id=%s" % (column, id)
                print "<li> ", update
                if debug == 0:
                        db.query(update)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Award Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print "<h1>SQL Updates:</h1>"
        print "<hr>"
        print "<ul>"

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('AwardUpdate'):
                merge = doc.getElementsByTagName('AwardUpdate')
                Record = GetElementValue(merge, 'Record')

                UpdateColumn(merge, 'AwardTitle',    'award_title', Record)
                UpdateColumn(merge, 'AwardYear',     'award_year',  Record)
                UpdateColumn(merge, 'AwardType',     'award_type_id', Record)
                UpdateColumn(merge, 'AwardCategory', 'award_cat_id', Record)
                UpdateColumn(merge, 'AwardLevel',    'award_level', Record)
                UpdateColumn(merge, 'AwardMovie',    'award_movie', Record)

                ##########################################################
                # AUTHORS
                ##########################################################
                value = GetElementValue(merge, 'AwardAuthors')
                NewAuthors = []
                if value:
                        counter = 0
                        austring = ""
                        authors = doc.getElementsByTagName('AwardAuthor')
                        for author in authors:
                                data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                if counter:
                                        austring += "+"
                                austring += data
                                counter += 1
                        update = "update awards set award_author='%s' where award_id=%s" % (db.escape_string(austring), Record)
                        print "<li> ", update
                        if debug == 0:
                                db.query(update)

                if TagPresent(merge, 'AwardNote'):
                        value = GetElementValue(merge, 'AwardNote')
                        if value:
                                ############################################################
                                # Check to see if this award already has a note
                                ############################################################
                                query = "select award_note_id from awards where award_id=%d and award_note_id is not null and award_note_id<>'0';" % int(Record)
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
                                        print "<li> ", insert
                                        db.query(insert)
                                        retval = db.insert_id()
                                        update = "update awards set award_note_id='%d' where award_id=%d" % (retval, int(Record))
                                        print "<li> ", update
                                        db.query(update)
                        else:
                                ##############################################################
                                # An empty note submission was made - delete the previous note
                                ##############################################################
                                query = "select award_note_id from awards where award_id=%d and award_note_id is not null and award_note_id<>'0';" % int(Record)
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        rec = res.fetch_row()
                                        note_id = rec[0][0]
                                        delete = "delete from notes where note_id=%d" % (note_id)
                                        print "<li> ", delete
                                        db.query(delete)
                                        update = "update awards set award_note_id=NULL where award_id=%d" % int(Record)
                                        print "<li> ", update
                                        db.query(update)

                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission, Record)

        # Load the award data
        award = awards(db)
        award.load(int(Record))

        # Only display title links if this award was entered for a Title record
        if award.title_id:
                print ISFDBLinkNoName('edit/edittitle.cgi', award.title_id, 'Edit This Title', True)
                print ISFDBLinkNoName('title.cgi', award.title_id, 'View This Title', True)
        print ISFDBLinkNoName('award_details.cgi', award.award_id, 'View This Award', True)
        print ISFDBLinkNoName('edit/editaward.cgi', award.award_id, 'Edit This Award', True)
        print ISFDBLinkNoName('ay.cgi', '%s+%s' % (award.award_type_id, award.award_year[:4]), 'View Award Year', True)
        print '<p>'

        PrintPostMod(0)
