#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2026   Al von Ruff, Bill Longley and Ahasuerus
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

import cgi
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
        CNX = MYSQL_CONNECTOR()
        if TagPresent(doc, tag):
                value = GetElementValue(doc, tag)
                if value:
                        value = XMLunescape(value)
                        value = CNX.DB_ESCAPE_STRING(value)
                        update = "update titles set %s='%s' where title_id=%s" % (column, value, id)
                else:
                        update = "update titles set %s=NULL where title_id=%s" % (column, id)
                print("<li> ", update)
                if debug == 0:
                        CNX.DB_QUERY(update)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Title Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")

        CNX = MYSQL_CONNECTOR()
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
                                        CNX.DB_QUERY(update)
                                        
                                if len(series_list) >1:
                                        # The secondary series number is not necessarily an integer, e.g. "05" is allowed
                                        update = "update titles set title_seriesnum_2='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(series_list[1]), int(Record))
                                else:
                                        update = "update titles set title_seriesnum_2=NULL where title_id=%d" % (int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)

                        else:
                                update = "update titles set title_seriesnum=NULL where title_id=%d" % (int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)
                                update = "update titles set title_seriesnum_2=NULL where title_id=%d" % (int(Record))
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)


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
                                                CNX.DB_QUERY(update)

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
                        CNX.DB_QUERY(delete)

                        ##########################################################
                        # Insert the new webpages
                        ##########################################################
                        webpages = doc.getElementsByTagName('Webpage')
                        for webpage in webpages:
                                if PYTHONVER == 'python2':
                                        address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                                else:
                                        address = XMLunescape(webpage.firstChild.data)
                                update = "insert into webpages(title_id, url) values(%d, '%s')" % (int(Record), CNX.DB_ESCAPE_STRING(address))
                                print("<li> ", update)
                                CNX.DB_QUERY(update)

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
                        CNX.DB_QUERY(delete)

                        ##########################################################
                        # Insert the new transliterated titles
                        ##########################################################
                        trans_titles = doc.getElementsByTagName('TranslitTitle')
                        for trans_title in trans_titles:
                                if PYTHONVER == 'python2':
                                        title_value = XMLunescape(trans_title.firstChild.data.encode('iso-8859-1'))
                                else:
                                        title_value = XMLunescape(trans_title.firstChild.data)
                                update = """insert into trans_titles(title_id, trans_title_title)
                                            values(%d, '%s')""" % (int(Record), CNX.DB_ESCAPE_STRING(title_value))
                                print("<li> ", update)
                                CNX.DB_QUERY(update)

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
                                CNX.DB_QUERY(query)
                                if CNX.DB_NUMROWS():
                                        rec = CNX.DB_FETCHONE()
                                        note_id = rec[0][0]
                                        update = "update notes set note_note='%s' where note_id=%d" % (CNX.DB_ESCAPE_STRING(value), note_id)
                                        update2 = "update notes set note_note='%s' where note_id=%d" % (value, note_id)
                                        print("<li> ", update2)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)
                                else:
                                        insert = "insert into notes(note_note) values('%s');" % CNX.DB_ESCAPE_STRING(value)
                                        insert2 = "insert into notes(note_note) values('%s');" % value
                                        print("<li> ", insert2)
                                        if debug == 0:
                                                CNX.DB_QUERY(insert)
                                        retval = CNX.DB_INSERT_ID()
                                        update = "update titles set note_id='%d' where title_id=%s" % (retval, Record)
                                        print("<li> ", update)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)
                        else:
                                #################################################
                                # An empty note submission was made
                                #################################################
                                query = 'select note_id from titles where title_id=%s and note_id is not null;' % Record
                                CNX.DB_QUERY(query)
                                if CNX.DB_NUMROWS():
                                        rec = CNX.DB_FETCHONE()
                                        note_id = rec[0][0]
                                        delete = "delete from notes where note_id=%d" % (note_id)
                                        print("<li> ", delete)
                                        if debug == 0:
                                                CNX.DB_QUERY(delete)
                                        update = "update titles set note_id=NULL where title_id=%s" % (Record)
                                        print("<li> ", update)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)

                ##########################################################
                # SYNOPSIS
                ##########################################################
                if TagPresent(merge, 'Synopsis'):
                        value = GetElementValue(merge, 'Synopsis')
                        if value:
                                query = 'select title_synopsis from titles where title_id=%s and title_synopsis is not null;' % Record
                                CNX.DB_QUERY(query)
                                if CNX.DB_NUMROWS():
                                        rec = CNX.DB_FETCHONE()
                                        note_id = rec[0][0]
                                        update = "update notes set note_note='%s' where note_id=%d" % (CNX.DB_ESCAPE_STRING(value), note_id)
                                        update2 = "update notes set note_note='%s' where note_id=%d" % (value, note_id)
                                        print("<li> ", update2)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)
                                else:
                                        insert = "insert into notes(note_note) values('%s');" % CNX.DB_ESCAPE_STRING(value)
                                        insert2 = "insert into notes(note_note) values('%s');" % value
                                        print("<li> ", insert2)
                                        if debug == 0:
                                                CNX.DB_QUERY(insert)

                                        retval = CNX.DB_INSERT_ID()
                                        update = "update titles set title_synopsis='%d' where title_id=%s" % (retval, Record)
                                        print("<li> ", update)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)
                        else:
                                #################################################
                                # An empty synopsis submission was made
                                #################################################
                                query = 'select title_synopsis from titles where title_id=%s and title_synopsis is not null;' % Record
                                CNX.DB_QUERY(query)
                                if CNX.DB_NUMROWS():
                                        rec = CNX.DB_FETCHONE()
                                        note_id = rec[0][0]
                                        delete = "delete from notes where note_id=%d" % (note_id)
                                        print("<li> ", delete)
                                        if debug == 0:
                                                CNX.DB_QUERY(delete)
                                        update = "update titles set title_synopsis=NULL where title_id=%s" % (Record)
                                        print("<li> ", update)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)

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
                                CNX.DB_QUERY(query)
                                OldSeries = -1
                                if CNX.DB_NUMROWS():
                                        record = CNX.DB_FETCHONE()
                                        OldSeries = record[0][0]

                                ################################################
                                # STEP 2 - Get the ID for the new series
                                ################################################
                                query = "select series_id from series where series_title='%s';" % (CNX.DB_ESCAPE_STRING(value))
                                print("<li> ", query)
                                CNX.DB_QUERY(query)
                                if CNX.DB_NUMROWS():
                                        record = CNX.DB_FETCHONE()
                                        NewSeries = record[0][0]
                                else:
                                        query = "insert into series(series_title) values('%s');" % (CNX.DB_ESCAPE_STRING(value))
                                        print("<li> ", query)
                                        if debug == 0:
                                                try:
                                                        CNX.DB_QUERY(query)
                                                except Exception as e:
                                                        print("CNX.DB_QUERY FAILED")
                                                        traceback.print_exc()
                                        NewSeries = CNX.DB_INSERT_ID()

                                ################################################
                                # STEP 3 - Update the title record
                                ################################################
                                update = "update titles set series_id='%d' where title_id=%s" % (NewSeries, Record)
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)

                                ################################################
                                # STEP 4 - Check to see if old series_id is still referenced
                                ################################################
                                #if OldSeries > -1:
                                #        query = 'select COUNT(series_id) from titles where series_id=%d' % (int(OldSeries))
                                #        CNX.DB_QUERY(query)
                                #        record = CNX.DB_FETCHONE()
                                #        if record[0][0] == 0:
                                #                # STEP 5 - Delete old series if no longer referenced
                                #                query = 'delete from series where series_id=%d' % (int(OldSeries))
                                #                print "<li> ", query
                                #                if debug == 0:
                                #                        CNX.DB_QUERY(query)
                        else:
                                ################################################
                                # Otherwise, wipe out the series_id and 
                                # the two seriesnum fields
                                ################################################
                                update = "update titles set series_id=NULL where title_id=%s" % (Record)
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)
                                update = "update titles set title_seriesnum=NULL where title_id=%s" % (Record)
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)
                                update = "update titles set title_seriesnum_2=NULL where title_id=%s" % (Record)
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)

                ##########################################################
                # AUTHORS
                ##########################################################
                value = GetElementValue(merge, 'Authors')
                NewAuthors = []
                if value:
                        authors = doc.getElementsByTagName('Author')
                        for author in authors:
                                if PYTHONVER == 'python2':
                                        data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                else:
                                        data = XMLunescape(author.firstChild.data)
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
                                if PYTHONVER == 'python2':
                                        data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                else:
                                        data = XMLunescape(author.firstChild.data)
                                NewAuthors.append(data)
                        setReviewees(Record, NewAuthors)
                value = GetElementValue(merge, 'Interviewees')
                NewAuthors = []
                if value:
                        authors = doc.getElementsByTagName('Interviewee')
                        for author in authors:
                                if PYTHONVER == 'python2':
                                        data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                else:
                                        data = XMLunescape(author.firstChild.data)
                                NewAuthors.append(data)
                        setInterviewees(Record, NewAuthors)

                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission, Record)

        print(ISFDBLinkNoName('edit/edittitle.cgi', Record, 'Edit This Title', True))
        print(ISFDBLinkNoName('title.cgi', Record, 'View This Title', True))
        print(ISFDBLinkNoName('edit/find_title_dups.cgi', Record, 'Check for Duplicate Titles', True))

        print('<p>')

        PrintPostMod(0)
