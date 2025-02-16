#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Ahasuerus, Bill Longley and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 745 $
#     Date: $Date: 2021-09-14 21:25:20 -0400 (Tue, 14 Sep 2021) $


from isfdb import *
from isfdblib import *
from common import *
from titleClass import *
from library import *
from SQLparsing import *

debug = 0

def UpdateTitle(TitleRecord, column, value):
        if not value:
                update = "update titles set %s = NULL where title_id = %d" % (column, int(TitleRecord))
        else:
                update = "update titles set %s = '%s' where title_id = %d" % (column, db.escape_string(value), int(TitleRecord))
        print("<li> ", update)
        db.query(update)


def UpdateColumn(doc, tag, column, id):
        value = GetElementValue(doc, tag)
        if TagPresent(doc, tag):
                value = XMLunescape(value)
                value = db.escape_string(value)
                update = "update titles set %s='%s' where title_id=%s" % (column, value, id)
                print("<li> ", update)
                if debug == 0:
                        db.query(update)

def addAuthor(author, title_id):

        ##############################################
        # STEP 1 - Get the author_id for this name,
        #          or else create one
        ##############################################
        query = "select author_id from authors where author_canonical='%s'" % (db.escape_string(author))
        db.query(query)
        result = db.store_result()
        if result.num_rows():
                record = result.fetch_row()
                author_id = record[0][0]
        else:
                author_id = insertAuthorCanonical(author)

        ##############################################
        # STEP 2 - Insert author mapping into 
        #          title_authors
        ##############################################
        insert = "insert into canonical_author(title_id, author_id, ca_status) values('%d', '%d', 1);" % (int(title_id), author_id)
        print("<li> ", insert)
        if debug == 0:
                db.query(insert)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Add Variant Title - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('VariantTitle'):
                merge = doc.getElementsByTagName('VariantTitle')
                Parent = GetElementValue(merge, 'Parent')

                query = "insert into titles(title_title) values('xxx');"
                print("<li> ", query)
                if debug == 0:
                        db.query(query)
                TitleRecord = db.insert_id()

                UpdateColumn(merge, 'Title',      'title_title',      TitleRecord)

                # Transliterated Titles
                value = GetElementValue(merge, 'TransTitles')
                if value:
                        trans_titles = doc.getElementsByTagName('TransTitle')
                        for trans_title in trans_titles:
                                title_value = XMLunescape(trans_title.firstChild.data.encode('iso-8859-1'))
                                update = """insert into trans_titles(title_id, trans_title_title)
                                            values(%d, '%s')""" % (int(TitleRecord), db.escape_string(title_value))
                                print("<li> ", update)
                                db.query(update)

                UpdateColumn(merge, 'Year',       'title_copyright',  TitleRecord)
                UpdateColumn(merge, 'Storylen',   'title_storylen',   TitleRecord)
                UpdateColumn(merge, 'TitleType',  'title_ttype',      TitleRecord)
                UpdateColumn(merge, 'Parent',     'title_parent',     TitleRecord)

                ParentData = SQLloadTitle(Parent)
                # Content Indicator
                UpdateTitle(TitleRecord, 'title_content', ParentData[TITLE_CONTENT])
                # Juvenile flag
                UpdateTitle(TitleRecord, 'title_jvn', ParentData[TITLE_JVN])
                # Novelization flag
                UpdateTitle(TitleRecord, 'title_nvz', ParentData[TITLE_NVZ])
                # Non-genre flag
                UpdateTitle(TitleRecord, 'title_non_genre', ParentData[TITLE_NON_GENRE])
                # Graphic flag
                UpdateTitle(TitleRecord, 'title_graphic', ParentData[TITLE_GRAPHIC])

                ##########################################################
                # Language
                ##########################################################
                if TagPresent(merge, 'Language'):
                        value = GetElementValue(merge, 'Language')
                        if value:
                                lang_id = SQLGetLangIdByName(XMLunescape(value))
                                if lang_id:
                                        update = "update titles set title_language='%d' where title_id=%s" % (int(lang_id), TitleRecord)
                                        print("<li> ", update)
                                        if debug == 0:
                                                db.query(update)

                ##########################################################
                # NOTE
                ##########################################################
                value = GetElementValue(merge, 'Note')
                if value:
                        query = 'select note_id from titles where title_id=%s and note_id is not null;' % TitleRecord
                        db.query(query)
                        res = db.store_result()
                        if res.num_rows():
                                rec = res.fetch_row()
                                note_id = rec[0][0]
                                update = "update notes set note_note='%s' where note_id=%d" % (db.escape_string(value), note_id)
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)
                        else:
                                insert = "insert into notes(note_note) values('%s');" % db.escape_string(value)
                                if debug == 0:
                                        db.query(insert)
                                retval = db.insert_id()
                                update = "update titles set note_id='%d' where title_id=%s" % (retval, TitleRecord)
                                print("<li> ", update)
                                if debug == 0:
                                        db.query(update)

                ##########################################################
                # AUTHORS
                ##########################################################
                value = GetElementValue(merge, 'Authors')
                if value:
                        authors = doc.getElementsByTagName('Author')
                        for author in authors:
                                data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                addAuthor(data, TitleRecord)

                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission, TitleRecord)

        print(ISFDBLinkNoName('title.cgi', Parent, 'View Original Title', True))
        print(ISFDBLinkNoName('title.cgi', TitleRecord, 'View New Title', True))

        print("<p>")

        PrintPostMod(0)
