#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Bill Longley, Ahasuerus and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 910 $
#     Date: $Date: 2022-05-01 13:28:59 -0400 (Sun, 01 May 2022) $


from isfdb import *
from isfdblib import *
from titleClass import *
from SQLparsing import *
from common import *
from library import *

debug = 0


def UpdateTitleColumn(doc, tag, column, id):
        value = GetElementValue(doc, tag)
        if TagPresent(doc, tag):
                CNX = MYSQL_CONNECTOR()
                value = XMLunescape(value)
                # For languages, get the language ID from its display name
                if tag == 'Language':
                        value = str(SQLGetLangIdByName(value))
                update = "update titles set %s='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(column), CNX.DB_ESCAPE_STRING(value), int(id))
                print("<li> ", update)
                if debug == 0:
                        CNX.DB_QUERY(update)

def UpdateSeries(ChildRecord, child_data, ParentRecord):
        update = "update titles set series_id=%d where title_id=%d" % (int(child_data[TITLE_SERIES]), int(ParentRecord))
        print("<li> ", update)
        if debug == 0:
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(update)
        DeleteSeries(ChildRecord)

def DeleteSeries(ChildRecord):
        #Clear the series name in the child title record
        update = "update titles set series_id=NULL where title_id=%d" % int(ChildRecord)
        print("<li> ", update)
        if debug == 0:
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(update)

def UpdateSeriesNum(ChildRecord, child_data, ParentRecord):
        if child_data[TITLE_SERIESNUM] is None:
                update = "update titles set title_seriesnum=NULL where title_id=%d" % int(ParentRecord)
        else:
                update = "update titles set title_seriesnum=%d where title_id=%d" % (int(child_data[TITLE_SERIESNUM]), int(ParentRecord))
        print("<li> ", update)
        CNX = MYSQL_CONNECTOR()
        if debug == 0:
                CNX.DB_QUERY(update)

        if child_data[TITLE_SERIESNUM_2] is None:
                update = "update titles set title_seriesnum_2=NULL where title_id=%d" % int(ParentRecord)
        else:
                update = "update titles set title_seriesnum_2='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(child_data[TITLE_SERIESNUM_2]), int(ParentRecord))
        print("<li> ", update)
        if debug == 0:
                CNX.DB_QUERY(update)
        DeleteSeriesNumber(ChildRecord)

def DeleteSeriesNumber(ChildRecord):
        #Clear the series number fields in the child title record
        update = "update titles set title_seriesnum=NULL where title_id=%d" % int(ChildRecord)
        print("<li> ", update)
        CNX = MYSQL_CONNECTOR()
        if debug == 0:
                CNX.DB_QUERY(update)

        update = "update titles set title_seriesnum_2=NULL where title_id=%d" % int(ChildRecord)
        print("<li> ", update)
        if debug == 0:
                CNX.DB_QUERY(update)

def UpdateTags(ChildRecord, ParentRecord):
        update = "update tag_mapping set title_id=%d where title_id=%d" % (int(ParentRecord), int(ChildRecord))
        print("<li> ", update)
        CNX = MYSQL_CONNECTOR()
        if debug == 0:
                CNX.DB_QUERY(update)

def MoveSynopsis(child_data, ParentRecord, ChildRecord):
        update = "update titles set title_synopsis = %d where title_id = %d" % (child_data[TITLE_SYNOP], int(ParentRecord))
        print("<li> ", update)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)
        update = "update titles set title_synopsis = NULL where title_id = %d" % int(ChildRecord)
        print("<li> ", update)
        CNX.DB_QUERY(update)

def DoSubmission(db, submission):
        ParentRecord = 0
        ChildRecord = 0
        CNX = MYSQL_CONNECTOR()
        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('MakeVariant'):
                merge = doc.getElementsByTagName('MakeVariant')
                ChildRecord = GetElementValue(merge, 'Record')
                child_data = SQLloadTitle(ChildRecord)

                print("<ul>")
                if TagPresent(merge, 'Parent'):
                        ParentRecord = int(GetElementValue(merge, 'Parent'))
                        parent_data = SQLloadTitle(ParentRecord)
                        
                        if parent_data:
                                if child_data[TITLE_SERIES]:
                                        # If the parent title is already in a Series, DELETE 
                                        # the child's series AND the child's series number
                                        if parent_data[TITLE_SERIES]:
                                                DeleteSeries(ChildRecord)
                                                DeleteSeriesNumber(ChildRecord)
                                        # If the parent title is not in a Series, then MOVE the Series name
                                        # AND the Series number from the child record to the parent record
                                        else:
                                                UpdateSeries(ChildRecord, child_data, ParentRecord)
                                                UpdateSeriesNum(ChildRecord, child_data, ParentRecord)
                        # If the parent record exists
                        if ParentRecord > 0:
                                # Move any Tags to the parent record
                                UpdateTags(ChildRecord, ParentRecord)
                                # If the child record has synopsis data AND the parent record doesn't,
                                # move the sysnopsis data to the parent record
                                if child_data[TITLE_SYNOP] and not parent_data[TITLE_SYNOP]:
                                        MoveSynopsis(child_data, ParentRecord, ChildRecord)
                else:
                        # Create a new Title record
                        query = "insert into titles(title_title) values('xxx');"
                        print("<li> ", query)
                        if debug == 0:
                                CNX.DB_QUERY(query)
                        ParentRecord = CNX.DB_INSERT_ID()
                        UpdateTitleColumn(merge, 'Title',     'title_title',     ParentRecord)
                        
                        value = GetElementValue(merge, 'TransTitles')
                        if value:
                                trans_titles = doc.getElementsByTagName('TransTitle')
                                for trans_title in trans_titles:
                                        if PYTHONVER == 'python2':
                                                title_value = XMLunescape(trans_title.firstChild.data.encode('iso-8859-1'))
                                        else:
                                                title_value = XMLunescape(trans_title.firstChild.data)
                                        update = """insert into trans_titles(title_id, trans_title_title)
                                                    values(%d, '%s')""" % (int(ParentRecord), CNX.DB_ESCAPE_STRING(title_value))
                                        print("<li> ", update)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)
                        UpdateTitleColumn(merge, 'Year',      'title_copyright', ParentRecord)
                        UpdateTitleColumn(merge, 'TitleType', 'title_ttype',     ParentRecord)
                        UpdateTitleColumn(merge, 'Language',  'title_language',  ParentRecord)

                        #Copy the "storylen" value from the child record to the new parent record
                        storylen = child_data[TITLE_STORYLEN]
                        if storylen:
                                update = "update titles set title_storylen='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(storylen), int(ParentRecord))
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)

                        #Copy the "content" value from the child record to the new parent record
                        content = child_data[TITLE_CONTENT]
                        if content:
                                update = "update titles set title_content='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(content), int(ParentRecord))
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)

                        #Copy the "juvenile" value from the child record to the new parent record
                        juvenile = child_data[TITLE_JVN]
                        if juvenile:
                                update = "update titles set title_jvn='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(juvenile), int(ParentRecord))
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)

                        #Copy the "novelization" value from the child record to the new parent record
                        novelization = child_data[TITLE_NVZ]
                        if novelization:
                                update = "update titles set title_nvz='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(novelization), int(ParentRecord))
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)

                        #Copy the "Non-Genre" value from the child record to the new parent record
                        nongenre = child_data[TITLE_NON_GENRE]
                        if nongenre:
                                update = "update titles set title_non_genre='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(nongenre), int(ParentRecord))
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)
                        
                        #Copy the "Graphic" value from the child record to the new parent record
                        graphic = child_data[TITLE_GRAPHIC]
                        if graphic:
                                update = "update titles set title_graphic='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(graphic), int(ParentRecord))
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)

                        # Series name:
                        #  If the child record has a series value, move it to the new parent record
                        if child_data[TITLE_SERIES]:
                                UpdateSeries(ChildRecord, child_data, ParentRecord)
                        #  Otherwise, if the submission has a series name, process it
                        elif TagPresent(merge, 'Series'):
                                series_name = GetElementValue(merge, 'Series')
                                series_data = SQLFindSeries(series_name, 'exact')
                                if series_data:
                                        update = "update titles set series_id=%d where title_id=%d" % (int(series_data[0][SERIES_PUBID]), int(ParentRecord))
                                        print("<li> ", update)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)
                                else:
                                        insert = "insert into series(series_title) values('%s')" % (CNX.DB_ESCAPE_STRING(series_name))
                                        print("<li> ", insert)
                                        if debug == 0:
                                                CNX.DB_QUERY(insert)
                                        new_series_id = CNX.DB_INSERT_ID()
                                        update = "update titles set series_id=%d where title_id=%d" % (int(new_series_id), int(ParentRecord))
                                        print("<li> ", update)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)
                        
                        # Series number:
                        #  If the child record has a series number, move it to the new parent record
                        if child_data[TITLE_SERIESNUM] is not None:
                                UpdateSeriesNum(ChildRecord, child_data, ParentRecord)
                        #  Otherwise, if the submission has a series number, process it
                        elif TagPresent(merge, 'Seriesnum'):
                                series_num = GetElementValue(merge, 'Seriesnum')
                                series_list = series_num.split('.')
                                if len(series_list):
                                        update = "update titles set title_seriesnum=%d where title_id=%d" % (int(series_list[0]), int(ParentRecord))
                                else:
                                        update = "update titles set title_seriesnum=NULL where title_id=%d" % int(ParentRecord)
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)
                                        
                                if len(series_list) >1:
                                        # The secondary series number is not necessarily an integer, e.g. "05" is allowed
                                        update = "update titles set title_seriesnum_2='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(series_list[1]), int(ParentRecord))
                                else:
                                        update = "update titles set title_seriesnum_2=NULL where title_id=%d" % int(ParentRecord)
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)

                        value = GetElementValue(merge, 'Webpages')
                        if value:
                                web_pages = doc.getElementsByTagName('Webpage')
                                for web_page in web_pages:
                                        if PYTHONVER == 'python2':
                                                url = XMLunescape(web_page.firstChild.data.encode('iso-8859-1'))
                                        else:
                                                url = XMLunescape(web_page.firstChild.data)
                                        update = """insert into webpages(title_id, url)
                                                    values(%d, '%s')""" % (int(ParentRecord), CNX.DB_ESCAPE_STRING(url))
                                        print("<li> ", update)
                                        CNX.DB_QUERY(update)

                        # Move any Tags to Parent
                        UpdateTags(ChildRecord, ParentRecord)

                        # If the child record has synopsis data, move it to the new parent record
                        if child_data[TITLE_SYNOP]:
                                MoveSynopsis(child_data, ParentRecord, ChildRecord)

                        ##########################################################
                        # TITLE AUTHORS
                        ##########################################################
                        value = GetElementValue(merge, 'Authors')
                        if value:
                                authors = doc.getElementsByTagName('Author')
                                for author in authors:
                                        if PYTHONVER == 'python2':
                                                data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                        else:
                                                data = XMLunescape(author.firstChild.data)
                                        addTitleAuthor(data, ParentRecord, 'CANONICAL')

                if TagPresent(merge, 'Note'):
                        value = GetElementValue(merge, 'Note')
                        insert = "insert into notes(note_note) values('%s')" % CNX.DB_ESCAPE_STRING(value)
                        insert2 = "insert into notes(note_note) values('%s')" % value
                        print("<li> ", insert2)
                        if debug == 0:
                                CNX.DB_QUERY(insert)
                        note_id = CNX.DB_INSERT_ID()
                        update = "update titles set note_id=%d where title_id=%d" % (note_id, ParentRecord)
                        print("<li> ", update)
                        if debug == 0:
                                CNX.DB_QUERY(update)

                update = "update titles set title_parent=%d where title_id=%d" % (int(ParentRecord), int(ChildRecord))
                print("<li> ", update)
                if debug == 0:
                        CNX.DB_QUERY(update)

                ##########################################################          
                #  REVIEWED TITLE AUTHORS AND INTERVIEWEES          
                ##########################################################          
                value = GetElementValue(merge, 'TitleType')
                if value == 'REVIEW':
                        insert = "insert into canonical_author (title_id, author_id, ca_status) \
                                select %d, author_id, 3 from canonical_author where title_id = %d \
                                and ca_status = 3" % (int(ParentRecord), int(ChildRecord))
                        print("<li> ", insert)
                        if debug == 0:
                                CNX.DB_QUERY(insert)
                elif value == 'INTERVIEW':
                        insert = "insert into canonical_author (title_id, author_id, ca_status) \
                                select %d, author_id, 2 from canonical_author where title_id = %d \
                                and ca_status = 2" % (int(ParentRecord), int(ChildRecord))
                        print("<li> ", insert)
                        if debug == 0:
                                CNX.DB_QUERY(insert)

                # If the new parent is a valid title ID and not 0
                if int(ParentRecord):
                        # Relink any grandchildren variants from the child to the parent
                        query = "select title_id from titles where title_parent=%d" % int(ChildRecord)
                        CNX2 = MYSQL_CONNECTOR()
                        CNX2.DB_QUERY(query)
                        rec2 = CNX2.DB_FETCHMANY()
                        while rec2:
                                grandchild_id = int(rec2[0][0])
                                update = "update titles set title_parent=%d where title_id=%d" % (int(ParentRecord), grandchild_id)
                                print("<li> ", update)
                                if debug == 0:
                                        CNX3 = MYSQL_CONNECTOR()
                                        CNX3.DB_QUERY(update)
                                rec2 = CNX2.DB_FETCHMANY()

                submitter = GetElementValue(merge, 'Submitter')
                if debug == 0:
                        markIntegrated(db, submission, ChildRecord)
        return (ParentRecord, ChildRecord)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Make Variant - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")

        (ParentRecord, ChildRecord) = DoSubmission(db, submission)

        if ParentRecord:
                print(ISFDBLinkNoName('edit/edittitle.cgi', ParentRecord, 'Edit Parent Title', True))
                print(ISFDBLinkNoName('title.cgi', ParentRecord, 'View Parent Title', True))
                print(ISFDBLinkNoName('edit/find_title_dups.cgi', ParentRecord, 'Check Parent Title for Duplicates', True))
        if ChildRecord:
                print(ISFDBLinkNoName('edit/edittitle.cgi', ChildRecord,'Edit Variant Title', True))
                print(ISFDBLinkNoName('title.cgi', ChildRecord, 'View Variant Title', True))
        print('<p>')

        PrintPostMod(0)
