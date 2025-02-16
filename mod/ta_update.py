#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 778 $
#     Date: $Date: 2021-10-11 22:42:01 -0400 (Mon, 11 Oct 2021) $


import cgi
import sys
import MySQLdb
import traceback
from isfdb import *
from isfdblib import *
from common import *
from titleClass import *
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
                        update = "update titles set %s='%s' where title_id=%s" % (column, value, id)
                else:
                        update = "update titles set %s=NULL where title_id=%s" % (column, id)
                print("<li> ", update)
                if debug == 0:
                        db.query(update)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Title Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('TitleUpdate'):
                merge = doc.getElementsByTagName('TitleUpdate')
                Record = GetElementValue(merge, 'Record')

                UpdateColumn(merge, 'Title',      'title_title',      Record)
                UpdateColumn(merge, 'Year',       'title_copyright',  Record)
                UpdateColumn(merge, 'Storylen',   'title_storylen',   Record)
                UpdateColumn(merge, 'TitleType',  'title_ttype',      Record)
                UpdateColumn(merge, 'ContentIndicator', 'title_content', Record)
                UpdateColumn(merge, 'Juvenile',   'title_jvn',        Record)
                UpdateColumn(merge, 'Novelization', 'title_nvz',      Record)
                UpdateColumn(merge, 'NonGenre',   'title_non_genre',  Record)
                UpdateColumn(merge, 'Graphic',    'title_graphic',    Record)

                ##########################################################
                # Series numbers 1 and 2
                ##########################################################
                if TagPresent(merge, 'Seriesnum'):
                        value = GetElementValue(merge, 'Seriesnum')
                        if value:
                                series_list = value.split('.')
                                if len(series_list):
                                        update = "update titles set title_seriesnum='%d' where title_id=%d" % (int(series_list[0]), int(Record))
                                else:
                                        update = "update titles set title_seriesnum=NULL where title_id=%d" % (int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)
                                        
                                if len(series_list) >1:
                                        # The secondary series number is not necessarily an integer, e.g. "05" is allowed
                                        update = "update titles set title_seriesnum_2='%s' where title_id=%d" % (db.escape_string(series_list[1]), int(Record))
                                else:
                                        update = "update titles set title_seriesnum_2=NULL where title_id=%d" % (int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)

                        else:
                                update = "update titles set title_seriesnum=NULL where title_id=%d" % (int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)
                                update = "update titles set title_seriesnum_2=NULL where title_id=%d" % (int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)


                ##########################################################
                # Language
                ##########################################################
                if TagPresent(merge, 'Language'):
                        value = GetElementValue(merge, 'Language')
                        if value:
                                lang_id = SQLGetLangIdByName(XMLunescape(value))
                                if lang_id:
                                        update = "update titles set title_language='%d' where title_id=%s" % (int(lang_id), Record)
                                        print("<li> ", update)
                                        if debug == 0:
                                                db.query(update)

                ##########################################################
                # Webpages
                ##########################################################
                value = GetElementValue(merge, 'Webpages')
                if value:
                        ##########################################################
                        # Delete the old webpages
                        ##########################################################
                        delete = "delete from webpages where title_id=%d" % int(Record)
                        print("<li> ", delete)
                        db.query(delete)

                        ##########################################################
                        # Insert the new webpages
                        ##########################################################
                        webpages = doc.getElementsByTagName('Webpage')
                        for webpage in webpages:
                                address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                                update = "insert into webpages(title_id, url) values(%d, '%s')" % (int(Record), db.escape_string(address))
                                print("<li> ", update)
                                db.query(update)

                ##########################################################
                # Transliterated Titles
                ##########################################################
                value = GetElementValue(merge, 'TranslitTitles')
                if value:
                        ##########################################################
                        # Delete the old transliterated titles
                        ##########################################################
                        delete = "delete from trans_titles where title_id=%d" % int(Record)
                        print("<li> ", delete)
                        db.query(delete)

                        ##########################################################
                        # Insert the new transliterated titles
                        ##########################################################
                        trans_titles = doc.getElementsByTagName('TranslitTitle')
                        for trans_title in trans_titles:
                                title_value = XMLunescape(trans_title.firstChild.data.encode('iso-8859-1'))
                                update = """insert into trans_titles(title_id, trans_title_title)
                                            values(%d, '%s')""" % (int(Record), db.escape_string(title_value))
                                print("<li> ", update)
                                db.query(update)

                ##########################################################
                # NOTE
                ##########################################################
                if TagPresent(merge, 'Note'):
                        value = GetElementValue(merge, 'Note')
                        if value:
                                #################################################
                                # Check to see if this title already has a note
                                #################################################
                                query = "select note_id from titles where title_id=%s and note_id is not null and note_id<>'0';" % Record
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        rec = res.fetch_row()
                                        note_id = rec[0][0]
                                        update = "update notes set note_note='%s' where note_id=%d" % (db.escape_string(value), note_id)
                                        update2 = "update notes set note_note='%s' where note_id=%d" % (value, note_id)
                                        print("<li> ", update2)
                                        if debug == 0:
                                                db.query(update)
                                else:
                                        insert = "insert into notes(note_note) values('%s');" % db.escape_string(value)
                                        insert2 = "insert into notes(note_note) values('%s');" % value
                                        print("<li> ", insert2)
                                        if debug == 0:
                                                db.query(insert)
                                        retval = db.insert_id()
                                        update = "update titles set note_id='%d' where title_id=%s" % (retval, Record)
                                        print("<li> ", update)
                                        if debug == 0:
                                                db.query(update)
                        else:
                                #################################################
                                # An empty note submission was made
                                #################################################
                                query = 'select note_id from titles where title_id=%s and note_id is not null;' % Record
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        rec = res.fetch_row()
                                        note_id = rec[0][0]
                                        delete = "delete from notes where note_id=%d" % (note_id)
                                        print("<li> ", delete)
                                        if debug == 0:
                                                db.query(delete)
                                        update = "update titles set note_id=NULL where title_id=%s" % (Record)
                                        print("<li> ", update)
                                        if debug == 0:
                                                db.query(update)

                ##########################################################
                # SYNOPSIS
                ##########################################################
                if TagPresent(merge, 'Synopsis'):
                        value = GetElementValue(merge, 'Synopsis')
                        if value:
                                query = 'select title_synopsis from titles where title_id=%s and title_synopsis is not null;' % Record
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        rec = res.fetch_row()
                                        note_id = rec[0][0]
                                        update = "update notes set note_note='%s' where note_id=%d" % (db.escape_string(value), note_id)
                                        update2 = "update notes set note_note='%s' where note_id=%d" % (value, note_id)
                                        print("<li> ", update2)
                                        if debug == 0:
                                                db.query(update)
                                else:
                                        insert = "insert into notes(note_note) values('%s');" % db.escape_string(value)
                                        insert2 = "insert into notes(note_note) values('%s');" % value
                                        print("<li> ", insert2)
                                        if debug == 0:
                                                db.query(insert)

                                        retval = db.insert_id()
                                        update = "update titles set title_synopsis='%d' where title_id=%s" % (retval, Record)
                                        print("<li> ", update)
                                        if debug == 0:
                                                db.query(update)
                        else:
                                #################################################
                                # An empty synopsis submission was made
                                #################################################
                                query = 'select title_synopsis from titles where title_id=%s and title_synopsis is not null;' % Record
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        rec = res.fetch_row()
                                        note_id = rec[0][0]
                                        delete = "delete from notes where note_id=%d" % (note_id)
                                        print("<li> ", delete)
                                        if debug == 0:
                                               db.query(delete)
                                               update = "update titles set title_synopsis=NULL where title_id=%s" % (Record)
                                               print("<li> ", update)
                                        if debug == 0:
                                               db.query(update)

                ##########################################################
                # SERIES
                ##########################################################
                if TagPresent(merge, 'Series'):
                        value = GetElementValue(merge, 'Series')
                        if value:
                                ################################################
                                # STEP 1 - Get the old series_id from the record
                                ################################################
                                query = 'select series_id from titles where title_id=%s and series_id is not null' % (Record)
                                db.query(query)
                                res = db.store_result()
                                OldSeries = -1
                                if res.num_rows():
                                        record = res.fetch_row()
                                        OldSeries = record[0][0]

                                ################################################
                                # STEP 2 - Get the ID for the new series
                                ################################################
                                query = "select series_id from series where series_title='%s';" % (db.escape_string(value))
                                print("<li> ", query)
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        record = res.fetch_row()
                                        NewSeries = record[0][0]
                                else:
                                        query = "insert into series(series_title) values('%s');" % (db.escape_string(value))
                                        print("<li> ", query)
                                        if debug == 0:
                                                try:
                                                        db.query(query)
                                                except Exception, e:
                                                        print("db.query FAILED")
                                                        traceback.print_exc()
                                        NewSeries = db.insert_id()

                                ################################################
                                # STEP 3 - Update the title record
                                ################################################
                                update = "update titles set series_id='%d' where title_id=%s" % (NewSeries, Record)
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)

                                ################################################
                                # STEP 4 - Check to see if old series_id is still referenced
                                ################################################
                                #if OldSeries > -1:
                                #        query = 'select COUNT(series_id) from titles where series_id=%d' % (int(OldSeries))
                                #        db.query(query)
                                #        res = db.store_result()
                                #        record = res.fetch_row()
                                #        if record[0][0] == 0:
                                #                # STEP 5 - Delete old series if no longer referenced
                                #                query = 'delete from series where series_id=%d' % (int(OldSeries))
                                #                print "<li> ", query
                                #                if debug == 0:
                                #                        db.query(query)
                        else:
                                ################################################
                                # Otherwise, wipe out the series_id and 
                                # the two seriesnum fields
                                ################################################
                                update = "update titles set series_id=NULL where title_id=%s" % (Record)
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)
                                update = "update titles set title_seriesnum=NULL where title_id=%s" % (Record)
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)
                                update = "update titles set title_seriesnum_2=NULL where title_id=%s" % (Record)
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)

                ##########################################################
                # AUTHORS
                ##########################################################
                value = GetElementValue(merge, 'Authors')
                NewAuthors = []
                if value:
                        authors = doc.getElementsByTagName('Author')
                        for author in authors:
                                data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                NewAuthors.append(data)
                        setTitleAuthors(Record, NewAuthors)

                ##########################################################
                # SUBJECT AUTHORS
                ##########################################################
                value = GetElementValue(merge, 'BookAuthors')
                NewAuthors = []
                if value:
                        authors = doc.getElementsByTagName('BookAuthor')
                        for author in authors:
                                data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                NewAuthors.append(data)
                        setReviewees(Record, NewAuthors)
                value = GetElementValue(merge, 'Interviewees')
                NewAuthors = []
                if value:
                        authors = doc.getElementsByTagName('Interviewee')
                        for author in authors:
                                data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                NewAuthors.append(data)
                        setInterviewees(Record, NewAuthors)

                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission, Record)

        print(ISFDBLinkNoName('edit/edittitle.cgi', Record, 'Edit This Title', True))
        print(ISFDBLinkNoName('title.cgi', Record, 'View This Title', True))
        print(ISFDBLinkNoName('edit/find_title_dups.cgi', Record, 'Check for Duplicate Titles', True))

        print('<p>')

        PrintPostMod(0)
