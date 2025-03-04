#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1166 $
#     Date: $Date: 2024-02-08 14:50:44 -0500 (Thu, 08 Feb 2024) $


import cgi
import sys
import string
import random
from isfdb import *
from isfdblib import *
from pubClass import *
from SQLparsing import *
from common import *
from library import *

debug = 0

def Unique(db, tag):
        query = "select pub_tag from pubs where pub_tag='%s'" % (tag)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS():
                return 0
        else:
                return 1

charmap = ['B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Z']

def CreateTag(db, title, year):

        ########################################################
        # STEP 1 - Convert the entire title string to upper case
        ########################################################
        newtitle = str.upper(title)

        ########################################################
        # STEP 2 - Extract the consonants. Max length = 10
        ########################################################
        counter = 0
        chars   = 0
        base = ''
        while counter < len(newtitle):
                if newtitle[counter] in charmap:
                        base += newtitle[counter]
                        chars += 1
                if chars > 9:
                        break
                counter += 1

        ########################################################
        # STEP 3 - If length < 10, pad with random consonants
        ########################################################
        while chars < 10:
                # create random characters until there are 10
                char = random.choice(charmap)
                base += char
                chars += 1
        
        ########################################################
        # STEP 4 - Test uniqueness of tag. If already exists
        #          generate extra last characters until good
        ########################################################
        tag = base + year
        tries = 0
        while Unique(db, tag) == 0:
                base = base[:len(base)-1]
                try:
                        char = charmap[tries]
                except:
                        char = str(tries)
                        # Reset tries so we go back to letters rather than
                        # adding '20' then '221' then '2222' then '22223' etc
                        tries = -1
                base += char
                tag = base + year
                tries += 1
        return tag


def UpdatePubColumn(doc, tag, column, id):
        CNX = MYSQL_CONNECTOR()
        value = GetElementValue(doc, tag)
        if TagPresent(doc, tag):
                value = XMLunescape(value)
                value = CNX.DB_ESCAPE_STRING(value)
                update = "update pubs set %s='%s' where pub_id=%s" % (column, value, id)
                print("<li> ", update)
                if debug == 0:
                        CNX.DB_QUERY(update)
        if tag == 'Tag':
                title = GetElementValue(doc, 'Title')
                title = XMLunescape(title)
                title = CNX.DB_ESCAPE_STRING(title)
                year = GetElementValue(doc, 'Year')
                year = year[:4]
                tag = CreateTag(db, title, year)
                update = "update pubs set %s='%s' where pub_id=%s" % (column, tag, id)
                print("<li> ", update)
                if debug == 0:
                        CNX.DB_QUERY(update)

def UpdateTitleColumn(doc, tag, column, id):
        CNX = MYSQL_CONNECTOR()
        value = GetElementValue(doc, tag)
        if TagPresent(doc, tag):
                value = XMLunescape(value)
                value = CNX.DB_ESCAPE_STRING(value)
                if column == 'title_ttype' and value == 'CHAPBOOK':
                        update = "update titles set title_storylen=NULL where title_id=%s" % (id)
                        print("<li> ", update)
                        if debug == 0:
                                CNX.DB_QUERY(update)
                        update = "update titles set title_ttype='SHORTFICTION' where title_id=%s" % (id)
                if column == 'title_ttype' and value == 'MAGAZINE':
                        update = "update titles set title_ttype='EDITOR' where title_id=%s" % (id)
                elif column == 'title_ttype' and value == 'FANZINE':
                        update = "update titles set title_ttype='EDITOR' where title_id=%s" % (id)
                else:
                        update = "update titles set %s='%s' where title_id=%s" % (column, value, id)
                print("<li> ", update)
                if debug == 0:
                        CNX.DB_QUERY(update)

def addPubAuthor(author, pub_id):
        ##############################################
        # STEP 1 - Get the author_id for this name,
        #          or else create one
        ##############################################
        CNX = MYSQL_CONNECTOR()
        query = "select author_id from authors where author_canonical='%s'" % (CNX.DB_ESCAPE_STRING(author))
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS():
                record = CNX.DB_FETCHONE()
                author_id = record[0][0]
        else:
                author_id = insertAuthorCanonical(author)

        ##############################################
        # STEP 2 - Insert author mapping into 
        #          pub_authors
        ##############################################
        insert = "insert into pub_authors(pub_id, author_id) values('%d', '%d');" % (int(pub_id), author_id)
        print("<li> ", insert)
        if debug == 0:
                CNX.DB_QUERY(insert)

def integrateCover(title, artists, date, pub_id, cover_id, referral_lang):
        CNX = MYSQL_CONNECTOR()
        if int(cover_id) == 0:
                ####################################################
                # Handle new covers
                ####################################################
                if referral_lang:
                        query = "insert into titles(title_title, title_copyright, title_ttype, title_language) values('%s', '%s', 'COVERART', %d)" % (CNX.DB_ESCAPE_STRING(title), CNX.DB_ESCAPE_STRING(date), int(referral_lang))
                else:
                        query = "insert into titles(title_title, title_copyright, title_ttype) values('%s', '%s', 'COVERART')" % (CNX.DB_ESCAPE_STRING(title), CNX.DB_ESCAPE_STRING(date))
                print("<li> ", query)
                if debug == 0:
                        CNX.DB_QUERY(query)
                cover_id = CNX.DB_INSERT_ID()
                # Take care of the artists
                artist_list = str.split(artists, "+")
                for artist in artist_list:
                        addTitleAuthor(artist, cover_id, 'CANONICAL')
                
        # Create publication-title linkage
        query = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(pub_id), int(cover_id))
        print("<li> ", query)
        if debug == 0:
                CNX.DB_QUERY(query)

def integrateTitle(title, authors, date, page, type, length, pub_id, title_id, referral_lang):

        CNX = MYSQL_CONNECTOR()
        if int(title_id) == 0:

                ####################################################
                # Handle any new titles
                ####################################################
                if type == 'SHORTFICTION' and length:
                        if referral_lang:
                                query = "insert into titles(title_title, title_copyright, title_ttype, title_storylen, title_language) values('%s', '%s', '%s', '%s', '%s');" % (CNX.DB_ESCAPE_STRING(title), date, type, length, str(referral_lang))
                        else:
                                query = "insert into titles(title_title, title_copyright, title_ttype, title_storylen) values('%s', '%s', '%s', '%s');" % (CNX.DB_ESCAPE_STRING(title), date, type, length)
                else:
                        if referral_lang:
                                query = "insert into titles(title_title, title_copyright, title_ttype, title_language) values('%s', '%s', '%s', '%s');" % (CNX.DB_ESCAPE_STRING(title), date, type, str(referral_lang))
                        else:
                                query = "insert into titles(title_title, title_copyright, title_ttype) values('%s', '%s', '%s');" % (CNX.DB_ESCAPE_STRING(title), date, type)
                print("<li> ", query)
                if debug == 0:
                        CNX.DB_QUERY(query)
                title_id = CNX.DB_INSERT_ID()

                ####################################################
                # STEP 2 - Take care of the authors
                ####################################################
                authorlist = str.split(authors, "+")
                for author in authorlist:
                        addTitleAuthor(author, title_id, 'CANONICAL')
                
        ####################################################
        # STEP 3 - Take care of pub linkage and page number
        ####################################################
        if page == '':
                query = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(pub_id), int(title_id))
        else:
                query = "insert into pub_content(pub_id, title_id, pubc_page) values(%d, %d, '%s');" % (int(pub_id), int(title_id), CNX.DB_ESCAPE_STRING(page))
        print("<li> ", query)
        if debug == 0:
                CNX.DB_QUERY(query)


def integrateReview(title, authors, reviewers, date, page, pub_id, title_id, referral_lang):

        CNX = MYSQL_CONNECTOR()
        if int(title_id) == 0:

                ####################################################
                # STEP 1 - Update the title table
                ####################################################
                if referral_lang:
                        query = "insert into titles(title_title, title_copyright, title_ttype, title_language) values('%s', '%s', 'REVIEW', '%s');" % (CNX.DB_ESCAPE_STRING(title), date, str(referral_lang))
                else:
                        query = "insert into titles(title_title, title_copyright, title_ttype) values('%s', '%s', 'REVIEW');" % (CNX.DB_ESCAPE_STRING(title), date)
                print("<li> ", query)
                if debug == 0:
                        CNX.DB_QUERY(query)
                title_id = CNX.DB_INSERT_ID()

                ####################################################
                # STEP 2 - Take care of the reviewers
                ####################################################
                authorlist = str.split(reviewers, "+")
                for author in authorlist:
                        addTitleAuthor(author, title_id, 'CANONICAL')
                
                ####################################################
                # STEP 3 - Take care of the reviewees
                ####################################################
                authorlist = str.split(authors, "+")
                for author in authorlist:
                        addTitleAuthor(author, title_id, 'REVIEWEE')

                ####################################################
                # STEP 4 - Generate title relationship entries
                ####################################################
                for author in authorlist:
                        parent = SQLFindReviewParent(title, author, referral_lang)
                        if parent:
                                update = "insert into title_relationships(title_id, review_id) values(%d, %d);" % (parent, title_id)
                                print("<li>", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)
                                break
                
        ####################################################
        # STEP 3 - Take care of pub linkage and page number
        ####################################################
        if page == '':
                query = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(pub_id), int(title_id))
        else:
                query = "insert into pub_content(pub_id, title_id, pubc_page) values(%d, %d, '%s');" % (int(pub_id), int(title_id), CNX.DB_ESCAPE_STRING(page))
        print("<li> ", query)
        if debug == 0:
                CNX.DB_QUERY(query)


def integrateInterview(title, interviewees, interviewers, date, page, pub_id, title_id, referral_lang):

        CNX = MYSQL_CONNECTOR()
        if int(title_id) == 0:

                ####################################################
                # STEP 1 - Update the title table
                ####################################################
                if referral_lang:
                        query = "insert into titles(title_title, title_copyright, title_ttype, title_language) values('%s', '%s', 'INTERVIEW', '%s');" % (CNX.DB_ESCAPE_STRING(title), date, str(referral_lang))
                else:
                        query = "insert into titles(title_title, title_copyright, title_ttype) values('%s', '%s', 'INTERVIEW');" % (CNX.DB_ESCAPE_STRING(title), date)
                print("<li> ", query)
                if debug == 0:
                        CNX.DB_QUERY(query)
                title_id = CNX.DB_INSERT_ID()

                ####################################################
                # STEP 2 - Take care of the interviewers
                ####################################################
                authorlist = str.split(interviewers, "+")
                for author in authorlist:
                        addTitleAuthor(author, title_id, 'CANONICAL')
                        
                ####################################################
                # STEP 3 - Take care of the interviewees
                ####################################################
                authorlist = str.split(interviewees, "+")
                for author in authorlist:
                        addTitleAuthor(author, title_id, 'INTERVIEWEE')
                
        ####################################################
        # STEP 3 - Take care of pub linkage and page number
        ####################################################
        if page == '':
                query = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(pub_id), int(title_id))
        else:
                query = "insert into pub_content(pub_id, title_id, pubc_page) values(%d, %d, '%s');" % (int(pub_id), int(title_id), CNX.DB_ESCAPE_STRING(page))
        print("<li> ", query)
        if debug == 0:
                CNX.DB_QUERY(query)



def DoSubmission(db, submission):
        CNX = MYSQL_CONNECTOR()
        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('NewPub'):

                print("<ul>")
                merge = doc.getElementsByTagName('NewPub')
                Record = GetElementValue(merge, 'ClonedTo')
                referral_lang = None
                if Record:
                        doingExport = 1
                        # Try to find the language of the "referral" title for this pub
                        referral_lang = findReferralLang(int(Record))
                        # Build a list of titles in the publication that we are importing new titles into
                        # so that we could avoid creating duplicate entries later
                        current_contents = SQLGetPubContentList(int(Record))
                        content_titles = []
                        for content_item in current_contents:
                                if content_item[PUB_CONTENTS_TITLE]:
                                        content_titles.append(content_item[PUB_CONTENTS_TITLE])
                else:
                        doingExport = 0
                        query = "insert into pubs(pub_title) values('xxx');"
                        print("<li> ", query)
                        if debug == 0:
                                CNX.DB_QUERY(query)
                        Record = CNX.DB_INSERT_ID()

                        UpdatePubColumn(merge, 'Title',   'pub_title',      Record)

                        # Transliterated Titles
                        value = GetElementValue(merge, 'TransTitles')
                        if value:
                                trans_titles = doc.getElementsByTagName('TransTitle')
                                for trans_title in trans_titles:
                                        title_value = XMLunescape(trans_title.firstChild.data.encode('iso-8859-1'))
                                        update = """insert into trans_pubs(pub_id, trans_pub_title)
                                                    values(%d, '%s')""" % (int(Record), CNX.DB_ESCAPE_STRING(title_value))
                                        print("<li> ", update)
                                        CNX.DB_QUERY(update)

                        # Web Pages
                        value = GetElementValue(merge, 'Webpages')
                        if value:
                                webpages = doc.getElementsByTagName('Webpage')
                                for webpage in webpages:
                                        address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                                        update = "insert into webpages(pub_id, url) values(%d, '%s')" % (int(Record), CNX.DB_ESCAPE_STRING(address))
                                        print("<li> ", update)
                                        CNX.DB_QUERY(update)

                        UpdatePubColumn(merge, 'Tag',     'pub_tag',        Record)
                        UpdatePubColumn(merge, 'Year',    'pub_year',       Record)
                        UpdatePubColumn(merge, 'Pages',   'pub_pages',      Record)
                        UpdatePubColumn(merge, 'PubSeriesNum', 'pub_series_num', Record)
                        UpdatePubColumn(merge, 'Binding', 'pub_ptype',      Record)
                        UpdatePubColumn(merge, 'PubType', 'pub_ctype',      Record)
                        UpdatePubColumn(merge, 'Isbn',    'pub_isbn',       Record)
                        UpdatePubColumn(merge, 'Catalog', 'pub_catalog',    Record)
                        UpdatePubColumn(merge, 'Price',   'pub_price',      Record)
                        UpdatePubColumn(merge, 'Image',   'pub_frontimage', Record)

                        ##########################################################
                        # Auto-verifications
                        ##########################################################
                        submitter = GetElementValue(merge, 'Submitter')
                        submitterid = SQLgetSubmitterID(submitter)
                        source = GetElementValue(merge, 'Source')
                        if source == 'Primary':
                                insert = SQLInsertPrimaryVerification(Record, 0, submitterid)
                                print('<li>%s' % (insert))
                        elif source == 'Transient':
                                insert = SQLInsertPrimaryVerification(Record, 1, submitterid)
                                print('<li>%s' % (insert))

                        #################################################################
                        # NOTE, auto-updated with the Source information for some sources
                        #################################################################
                        note = GetElementValue(merge, 'Note')
                        if source == 'PublisherWebsite':
                                note = 'Data from publisher\'s website. %s' % (note)
                        elif source == 'AuthorWebsite':
                                note = 'Data from author\'s website. %s' % (note)
                        if note:
                                query = 'select note_id from pubs where pub_id=%s and note_id is not null;' % Record
                                CNX.DB_QUERY(query)
                                if CNX.DB_NUMROWS():
                                        rec = CNX.DB_FETCHONE()
                                        note_id = rec[0][0]
                                        update = "update notes set note_note='%s' where note_id=%d" % (CNX.DB_ESCAPE_STRING(note), note_id)
                                        print("<li> ", update)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)
                                else:
                                        insert = "insert into notes(note_note) values('%s');" % CNX.DB_ESCAPE_STRING(note)
                                        print("<li> ", insert)
                                        if debug == 0:
                                                CNX.DB_QUERY(insert)
                                        retval = CNX.DB_INSERT_ID()
                                        update = "update pubs set note_id='%d' where pub_id=%s" % (retval, Record)
                                        print("<li> ", update)
                                        if debug == 0:
                                                CNX.DB_QUERY(update)

                        ##########################################################
                        # PUBLISHER
                        ##########################################################
                        value = GetElementValue(merge, 'Publisher')
                        if value:

                                # STEP 1 - Get the ID for the new publisher
                                query = "select publisher_id from publishers where publisher_name='%s';" % (CNX.DB_ESCAPE_STRING(value))
                                print("<li> ", query)
                                CNX.DB_QUERY(query)
                                if CNX.DB_NUMROWS():
                                        record = CNX.DB_FETCHONE()
                                        NewPublisher = record[0][0]
                                else:
                                        query = "insert into publishers(publisher_name) values('%s');" % (CNX.DB_ESCAPE_STRING(value))
                                        print("<li> ", query)
                                        if debug == 0:
                                                CNX.DB_QUERY(query)
                                        NewPublisher = CNX.DB_INSERT_ID()

                                # STEP 2 - Update the publication record
                                update = "update pubs set publisher_id='%d' where pub_id=%s" % (NewPublisher, Record)
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)

                        ##########################################################
                        # PUBLICATION SERIES
                        ##########################################################
                        value = GetElementValue(merge, 'PubSeries')
                        if value:

                                # STEP 1 - Get the ID for the new publication series
                                query = "select pub_series_id from pub_series where pub_series_name='%s';" % (CNX.DB_ESCAPE_STRING(value))
                                print("<li> ", query)
                                CNX.DB_QUERY(query)
                                if CNX.DB_NUMROWS():
                                        record = CNX.DB_FETCHONE()
                                        NewPubSeries = record[0][0]
                                else:
                                        query = "insert into pub_series(pub_series_name) values('%s');" % (CNX.DB_ESCAPE_STRING(value))
                                        print("<li> ", query)
                                        if debug == 0:
                                                CNX.DB_QUERY(query)
                                        NewPubSeries = CNX.DB_INSERT_ID()

                                # STEP 2 - Update the publication record
                                update = "update pubs set pub_series_id='%d' where pub_id=%s" % (NewPubSeries, Record)
                                print("<li> ", update)
                                if debug == 0:
                                        CNX.DB_QUERY(update)
                        
                        ##########################################################
                        # PUBLICATION AUTHORS
                        ##########################################################
                        value = GetElementValue(merge, 'Authors')
                        if value:
                                authors = doc.getElementsByTagName('Author')
                                for author in authors:
                                        data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                        addPubAuthor(data, Record)

                        if TagPresent(merge, 'Parent'):
                                TitleRecord = GetElementValue(merge, 'Parent')
                        else:
                                ##########################################################
                                # TITLE
                                ##########################################################
                                query = "insert into titles(title_title) values('xxx');"
                                print("<li> ", query)
                                if debug == 0:
                                        CNX.DB_QUERY(query)
                                TitleRecord = CNX.DB_INSERT_ID()
                                UpdateTitleColumn(merge, 'Title',   'title_title',     TitleRecord)
                                UpdateTitleColumn(merge, 'Year',    'title_copyright', TitleRecord)
                                UpdateTitleColumn(merge, 'PubType', 'title_ttype',     TitleRecord)

                                ##########################################################
                                # TITLE AUTHORS
                                ##########################################################
                                value = GetElementValue(merge, 'Authors')
                                if value:
                                        authors = doc.getElementsByTagName('Author')
                                        for author in authors:
                                                data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                                addTitleAuthor(data, TitleRecord, 'CANONICAL')

                        query = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(Record), int(TitleRecord))
                        print("<li> ", query)
                        if debug == 0:
                                CNX.DB_QUERY(query)
                        PubcRecord = CNX.DB_INSERT_ID()

                        ##########################################################
                        # EXTERNAL IDENTIFIERS
                        ##########################################################
                        if GetElementValue(merge, 'External_IDs'):
                                external_id_elements = doc.getElementsByTagName('External_ID')
                                for external_id_element in external_id_elements:
                                        type_id = GetChildValue(external_id_element, 'IDtype')
                                        id_value = GetChildValue(external_id_element, 'IDvalue')
                                        insert = """insert into identifiers(identifier_type_id, identifier_value,
                                                    pub_id) values(%d, '%s', %d)
                                                    """ % (int(type_id), CNX.DB_ESCAPE_STRING(id_value), Record)
                                        print("<li> ", insert)
                                        CNX.DB_QUERY(insert)

                if doc.getElementsByTagName('Content'):
                        # If the language of the "referral" title was unknown when we started
                        # processing this submission, try finding it again in case the referral
                        # title is now different
                        if not referral_lang:
                                referral_lang = findReferralLang(int(Record))
                        
                        ##########################################################
                        # Cover Art
                        ##########################################################
                        children = doc.getElementsByTagName('Cover')
                        if len(children):
                                for child in children:
                                        tRecord = GetChildValue(child, 'Record')
                                        title   = GetChildValue(child, 'cTitle')
                                        artists = GetChildValue(child, 'cArtists')
                                        date    = GetChildValue(child, 'cDate')
                                        if doingExport:
                                                if int(tRecord) not in content_titles:
                                                        integrateCover(title, artists, date, Record, tRecord, referral_lang)
                                        else:
                                                # Don't insert a second record
                                                if int(tRecord) != int(TitleRecord):
                                                        integrateCover(title, artists, date, Record, tRecord, referral_lang)

                        ##########################################################
                        # Regular Titles
                        ##########################################################
                        children = doc.getElementsByTagName('ContentTitle')
                        if len(children):
                                for child in children:
                                        tRecord = GetChildValue(child, 'Record')
                                        title   = GetChildValue(child, 'cTitle')
                                        authors = GetChildValue(child, 'cAuthors')
                                        date    = GetChildValue(child, 'cDate')
                                        page    = GetChildValue(child, 'cPage')
                                        type    = GetChildValue(child, 'cType')
                                        length  = GetChildValue(child, 'cLength')
                                        if doingExport:
                                                if int(tRecord) not in content_titles:
                                                        integrateTitle(title, authors, date, page, type, length, Record, tRecord, referral_lang)
                                        else:
                                                # Don't insert a second record
                                                if int(tRecord) != int(TitleRecord):
                                                        integrateTitle(title, authors, date, page, type, length, Record, tRecord, referral_lang)
                                                elif page != '':
                                                        query = "update pub_content set pubc_page='%s' where pubc_id=%d;" % (CNX.DB_ESCAPE_STRING(page), PubcRecord)
                                                        print("<li> ", query)
                                                        if debug == 0:
                                                                CNX.DB_QUERY(query)
                                
                        ##########################################################
                        # Reviews
                        ##########################################################
                        children = doc.getElementsByTagName('ContentReview')
                        if len(children):
                                for child in children:
                                        tRecord = GetChildValue(child, 'Record')
                                        title     = GetChildValue(child, 'cTitle')
                                        authors   = GetChildValue(child, 'cBookAuthors')
                                        reviewers = GetChildValue(child, 'cReviewers')
                                        date      = GetChildValue(child, 'cDate')
                                        page      = GetChildValue(child, 'cPage')
                                        integrateReview(title, authors, reviewers, date, page, Record, tRecord, referral_lang)

                        ##########################################################
                        # Interviews
                        ##########################################################
                        children = doc.getElementsByTagName('ContentInterview')
                        if len(children):
                                for child in children:
                                        tRecord = GetChildValue(child, 'Record')
                                        title        = GetChildValue(child, 'cTitle')
                                        interviewees = GetChildValue(child, 'cInterviewees')
                                        interviewers = GetChildValue(child, 'cInterviewers')
                                        date         = GetChildValue(child, 'cDate')
                                        page         = GetChildValue(child, 'cPage')
                                        integrateInterview(title, interviewees, interviewers, date, page, Record, tRecord, referral_lang)

                submitter = GetElementValue(merge, 'Submitter')
                if debug == 0:
                        if doingExport:
                                # Pass the ID of the pub that the data was imported into
                                markIntegrated(db, submission, Record, Record)
                        else:
                                # Pass the ID of the newly created pub
                                markIntegrated(db, submission, Record, None)
        return(Record)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Publication Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        if debug:
                print('<div id="ErrorBox">')
                print('<h3>Warning: This app is in debug mode. No writes actually occured to the database.</h3>')
                print('</div>')

        print('<h1>SQL Updates:</h1>')
        print('<hr>')

        Record = DoSubmission(db, submission)

        print(ISFDBLinkNoName('edit/editpub.cgi', Record, 'Edit This Pub', True))
        print(ISFDBLinkNoName('pl.cgi', Record, 'View This Pub', True))
        print(ISFDBLinkNoName('edit/verify.cgi', Record, 'Verify This Pub', True))
        print(ISFDBLinkNoName('edit/find_pub_dups.cgi', Record, 'Check for Duplicate Titles', True))
        print('<p>')
        LIBPrintDuplicateWarning(Record)

        PrintPostMod(0)
