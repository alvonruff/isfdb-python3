#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Ahasuerus, Bill Longley and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1166 $
#     Date: $Date: 2024-02-08 14:50:44 -0500 (Thu, 08 Feb 2024) $


from isfdb import *
from isfdblib import *
from common import *
from pubClass import *
from pubseriesClass import pub_series
from publisherClass import publishers
from titleClass import *
from SQLparsing import *
from common import *
from library import *

debug = 0
pub_id = 0


def UpdateColumn(doc, tag, column, id):
        value = GetElementValue(doc, tag)
        if TagPresent(doc, tag):
                value = XMLunescape(value)
                value = db.escape_string(value)
                update = "update pubs set %s='%s' where pub_id=%s" % (column, value, id)
                print("<li> ", update)
                if debug == 0:
                        db.query(update)

def addAuthor(author, pub_id):

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
        #          pub_authors
        ##############################################
        insert = "insert into pub_authors(pub_id, author_id) values('%d', '%d');" % (int(pub_id), author_id)
        print("<li> ", insert)
        if debug == 0:
                db.query(insert)

def deleteAuthor(author, pub_id):
        ##############################################
        # STEP 1 - Get the author_id for this name
        ##############################################
        query = "select author_id from authors where author_canonical='%s'" % (db.escape_string(author))
        db.query(query)
        result = db.store_result()
        if result.num_rows():
                record = result.fetch_row()
                author_id = record[0][0]
        else:
                return

        ##############################################
        # STEP 2 - Delete the author entry for this
        #          publication from pub_authors
        ##############################################
        query = "delete from pub_authors where author_id='%s' and pub_id='%s'" % (author_id, pub_id)
        print("<li> ", query)
        if debug == 0:
                db.query(query)

        ##############################################
        # STEP 3 - If the author still has an entry
        #          in any of the mapping tables, done.
        ##############################################
        for i in ['canonical_author', 'pub_authors']:
                query = 'select COUNT(author_id) from %s where author_id=%d' % (i, author_id)
                print("<li> ", query)
                db.query(query)
                res = db.store_result()
                record = res.fetch_row()
                if record[0][0]:
                        return

        ##############################################
        # STEP 4 - If no one references the author,
        #          delete it.
        ##############################################
        deleteFromAuthorTable(author_id)


def insertCover(title, artists, date, referral_lang):
        record = createNewTitle(title)
        update = "insert into pub_content(pub_id, title_id) values(%d, %d)" % (int(pub_id), int(record))
        print("<li>", update)
        if debug == 0:
                db.query(update)

        if date:
                setTitleDate(record, date)
        setTitleType(record, 'COVERART')
        if referral_lang:
                setTitleLang(record, referral_lang)

        artistlist = str.split(artists, '+')
        NewArtists = []
        for artist in artistlist:
                NewArtists.append(artist)
        setTitleAuthors(record, NewArtists)

def mergeCover(record, title, artists, date, doArtists):
        if title:
                setTitleName(record, title)
        if date:
                setTitleDate(record, date)
        setTitleType(record, 'COVERART')

        if doArtists:
                artistlist = str.split(artists, '+')
                NewArtists = []
                for artist in artistlist:
                        NewArtists.append(artist)
                setTitleAuthors(record, NewArtists)

def insertTitle(title, authors, date, page, type, length, referral_lang):
        record = createNewTitle(title)
        update = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(pub_id), int(record))
        print("<li>", update)
        if debug == 0:
                db.query(update)

        if date:
                setTitleDate(record, date)
        if type:
                setTitleType(record, type)
        if length:
                setTitleLength(record, length)
        if page:
                setTitlePage(record, page, pub_id)
        if referral_lang:
                setTitleLang(record, referral_lang)

        authorlist = str.split(authors, '+')
        NewAuthors = []
        for author in authorlist:
                NewAuthors.append(author)
        setTitleAuthors(record, NewAuthors)

def mergeTitle(record, title, authors, date, page, type, length, doAuthors):
        if title:
                setTitleName(record, title)
        if date:
                setTitleDate(record, date)
        if type:
                setTitleType(record, type)

        if length != 'NoXmlTag':
                setTitleLength(record, length)

        if page != 'NoXmlTag':
                setTitlePage(record, page, pub_id)

        if doAuthors:
                authorlist = str.split(authors, '+')
                NewAuthors = []
                for author in authorlist:
                        NewAuthors.append(author)
                setTitleAuthors(record, NewAuthors)


def insertReview(title, reviewees, reviewers, date, page, referral_lang):
        record = createNewTitle(title)
        update = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(pub_id), int(record))
        print("<li>", update)
        if debug == 0:
                db.query(update)

        setTitleType(record, "REVIEW")
        if date:
                setTitleDate(record, date)
        if page:
                setTitlePage(record, page, pub_id)
        if referral_lang:
                setTitleLang(record, referral_lang)

        reviewerlist = str.split(reviewers, '+')
        NewReviewers = []
        for reviewer in reviewerlist:
                NewReviewers.append(reviewer)
        setTitleAuthors(record, NewReviewers)

        revieweelist = str.split(reviewees, '+')
        NewReviewees = []
        for reviewee in revieweelist:
                NewReviewees.append(reviewee)
        setReviewees(record, NewReviewees)

        for reviewee in revieweelist:
                parent = SQLFindReviewParent(title, reviewee, referral_lang)
                if parent:
                        update = "insert into title_relationships(title_id, review_id) values(%d, %d);" % (parent, record)
                        print("<li>", update)
                        if debug == 0:
                                db.query(update)
                        return


def mergeReview(record, title, reviewees, reviewers, date, page, doReviewees, doReviewers):
        if title:
                setTitleName(record, title)
        if date:
                setTitleDate(record, date)
        if page != 'NoXmlTag':
                setTitlePage(record, page, pub_id)

        if doReviewers:
                reviewerlist = str.split(reviewers, '+')
                NewReviewers = []
                for reviewer in reviewerlist:
                        NewReviewers.append(reviewer)
                setTitleAuthors(record, NewReviewers)

        if doReviewees:
                revieweelist = str.split(reviewees, '+')
                NewReviewees = []
                for reviewee in revieweelist:
                        NewReviewees.append(reviewee)
                setReviewees(record, NewReviewees)


def insertInterview(title, interviewees, interviewers, date, page, referral_lang):
        record = createNewTitle(title)
        update = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(pub_id), int(record))
        print("<li>", update)
        if debug == 0:
                db.query(update)

        setTitleType(record, "INTERVIEW")
        if date:
                setTitleDate(record, date)
        if page:
                setTitlePage(record, page, pub_id)
        if referral_lang:
                setTitleLang(record, referral_lang)

        interviewerlist = str.split(interviewers, '+')
        NewInterviewers = []
        for interviewer in interviewerlist:
                NewInterviewers.append(interviewer)
        setTitleAuthors(record, NewInterviewers)

        intervieweelist = str.split(interviewees, '+')
        NewInterviewees = []
        for interviewee in intervieweelist:
                NewInterviewees.append(interviewee)
        setInterviewees(record, NewInterviewees)


def mergeInterview(record, title, interviewees, interviewers, date, page, doInterviewees, doInterviewers):
        if title:
                setTitleName(record, title)
        if date:
                setTitleDate(record, date)
        if page != 'NoXmlTag':
                setTitlePage(record, page, pub_id)

        if doInterviewers:
                interviewerlist = str.split(interviewers, '+')
                NewInterviewers = []
                for interviewer in interviewerlist:
                        NewInterviewers.append(interviewer)
                setTitleAuthors(record, NewInterviewers)

        if doInterviewees:
                intervieweelist = str.split(interviewees, '+')
                NewInterviewees = []
                for interviewee in intervieweelist:
                        NewInterviewees.append(interviewee)
                setInterviewees(record, NewInterviewees)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Publication Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('PubUpdate'):
                merge = doc.getElementsByTagName('PubUpdate')
                Record = GetElementValue(merge, 'Record')
                pub_id = int(Record)
                # Try to find the language of the "referral" title for this pub
                referral_lang = findReferralLang(pub_id)

                UpdateColumn(merge, 'Title',   'pub_title',      Record)
                UpdateColumn(merge, 'Year',    'pub_year',       Record)
                UpdateColumn(merge, 'Pages',   'pub_pages',      Record)
                UpdateColumn(merge, 'Binding', 'pub_ptype',      Record)
                UpdateColumn(merge, 'PubType', 'pub_ctype',      Record)
                UpdateColumn(merge, 'Isbn',    'pub_isbn',       Record)
                UpdateColumn(merge, 'Catalog', 'pub_catalog',    Record)
                UpdateColumn(merge, 'Price',   'pub_price',      Record)
                UpdateColumn(merge, 'Image',   'pub_frontimage', Record)
                UpdateColumn(merge, 'PubSeriesNum',   'pub_series_num',      Record)

                ##########################################################
                # Transliterated Titles
                ##########################################################
                value = GetElementValue(merge, 'TransTitles')
                if value:
                        ##########################################################
                        # Delete the old transliterated titles
                        ##########################################################
                        delete = "delete from trans_pubs where pub_id=%d" % int(Record)
                        print("<li> ", delete)
                        db.query(delete)

                        ##########################################################
                        # Insert the new transliterated titles
                        ##########################################################
                        trans_titles = doc.getElementsByTagName('TransTitle')
                        for trans_title in trans_titles:
                                title_value = XMLunescape(trans_title.firstChild.data.encode('iso-8859-1'))
                                update = """insert into trans_pubs(pub_id, trans_pub_title)
                                            values(%d, '%s')""" % (int(Record), db.escape_string(title_value))
                                print("<li> ", update)
                                db.query(update)

                ##########################################################
                # EXTERNAL IDENTIFIERS
                ##########################################################
                if GetElementValue(merge, 'External_IDs'):
                        ##########################################################
                        # Delete the old external identifiers
                        ##########################################################
                        delete = "delete from identifiers where pub_id=%d" % int(Record)
                        print("<li> ", delete)
                        db.query(delete)
                        ##########################################################
                        # Insert the new external identifiers
                        ##########################################################
                        external_id_elements = doc.getElementsByTagName('External_ID')
                        for external_id_element in external_id_elements:
                                type_id = GetChildValue(external_id_element, 'IDtype')
                                id_value = XMLunescape(GetChildValue(external_id_element, 'IDvalue'))
                                insert = """insert into identifiers(identifier_type_id, identifier_value,
                                            pub_id) values(%d, '%s', %d)
                                            """ % (int(type_id), db.escape_string(id_value), int(Record))
                                print("<li> ", insert)
                                db.query(insert)

                ##########################################################
                # NOTE
                ##########################################################
                if TagPresent(merge, 'Note'):
                        value = GetElementValue(merge, 'Note')
                        if value:
                                query = 'select note_id from pubs where pub_id=%s and note_id is not null;' % Record
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        ###########################################
                                        # Update the existing note
                                        ###########################################
                                        rec = res.fetch_row()
                                        note_id = rec[0][0]
                                        update = "update notes set note_note='%s' where note_id=%d" % (db.escape_string(value), note_id)
                                        print("<li> ", update)
                                        db.query(update)
                                else:
                                        ###########################################
                                        # Add a new note
                                        ###########################################
                                        insert = "insert into notes(note_note) values('%s');" % db.escape_string(value)
                                        print("<li> ", insert)
                                        db.query(insert)
                                        retval = db.insert_id()
                                        update = "update pubs set note_id='%d' where pub_id=%s" % (retval, Record)
                                        print("<li> ", update)
                                        db.query(update)
                        else:
                                query = 'select note_id from pubs where pub_id=%s and note_id is not null;' % Record
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        ###########################################
                                        # Delete the current note
                                        ###########################################
                                        rec = res.fetch_row()
                                        note_id = rec[0][0]
                                        update = "delete from notes where note_id=%d" % (note_id)
                                        print("<li> ", update)
                                        db.query(update)
                                        update = "update pubs set note_id=NULL where pub_id=%s" % Record
                                        print("<li> ", update)
                                        db.query(update)

                ##########################################################
                # PUBLISHER
                ##########################################################
                if TagPresent(merge, 'Publisher'):
                        value = GetElementValue(merge, 'Publisher')
                        if value:
                                # STEP 1 - Get the old publisher_id from the record
                                query = 'select publisher_id from pubs where pub_id=%s and publisher_id is not null' % (Record)
                                db.query(query)
                                res = db.store_result()
                                OldPublisher = -1
                                if res.num_rows():
                                        record = res.fetch_row()
                                        OldPublisher = record[0][0]

                                # STEP 2 - Get the ID for the new publisher
                                query = "select publisher_id from publishers where publisher_name='%s';" % (db.escape_string(value))
                                print("<li> ", query)
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        record = res.fetch_row()
                                        NewPublisher = record[0][0]
                                else:
                                        query = "insert into publishers(publisher_name) values('%s');" % (db.escape_string(value))
                                        print("<li> ", query)
                                        db.query(query)
                                        NewPublisher = db.insert_id()

                                # STEP 3 - Update the publication record
                                update = "update pubs set publisher_id='%d' where pub_id=%s" % (NewPublisher, Record)
                                print("<li> ", update)
                                db.query(update)

                                # STEP 4 - Delete the old publisher if there are no other pubs referencing it
                                if OldPublisher > -1:
                                        publisher = publishers(db)
                                        publisher.load(OldPublisher)
                                        publisher.delete()

                        else:
                                # STEP 1 - Get the old publisher_id from the record
                                query = 'select publisher_id from pubs where pub_id=%s and publisher_id is not null' % (Record)
                                db.query(query)
                                res = db.store_result()
                                OldPublisher = -1
                                if res.num_rows():
                                        record = res.fetch_row()
                                        OldPublisher = record[0][0]

                                # STEP 2 - Update the publication record
                                update = "update pubs set publisher_id=%s where pub_id=%s" % ('NULL', Record)
                                print("<li> ", update)
                                db.query(update)

                                # STEP 3 - Delete the old publisher if there are no other pubs referencing it
                                if OldPublisher > -1:
                                        publisher = publishers(db)
                                        publisher.load(OldPublisher)
                                        publisher.delete()

                ##########################################################
                # PUBLICATION SERIES
                ##########################################################
                if TagPresent(merge, 'PubSeries'):
                        value = GetElementValue(merge, 'PubSeries')
                        if value:
                                # STEP 1 - Get the old pub_series_id from the record
                                query = 'select pub_series_id from pubs where pub_id=%s and pub_series_id is not null' % (Record)
                                db.query(query)
                                res = db.store_result()
                                OldPubSeries = ''
                                if res.num_rows():
                                        record = res.fetch_row()
                                        OldPubSeries = record[0][0]

                                # STEP 2 - Get the ID for the new publication series
                                query = "select pub_series_id from pub_series where pub_series_name='%s';" % (db.escape_string(value))
                                print("<li> ", query)
                                db.query(query)
                                res = db.store_result()
                                if res.num_rows():
                                        record = res.fetch_row()
                                        NewPubSeries = record[0][0]
                                else:
                                        query = "insert into pub_series(pub_series_name) values('%s');" % (db.escape_string(value))
                                        print("<li> ", query)
                                        db.query(query)
                                        NewPubSeries = db.insert_id()

                                # STEP 3 - Update the publication record
                                update = "update pubs set pub_series_id='%d' where pub_id=%s" % (NewPubSeries, Record)
                                print("<li> ", update)
                                db.query(update)

                                # STEP 4 - Delete the old publication series if it's now empty
                                if OldPubSeries:
                                        pubseries = pub_series(db)
                                        pubseries.load(OldPubSeries)
                                        pubseries.delete()
                        else:
                                # STEP 1 - Get the old pub_series_id from the record
                                query = 'select pub_series_id from pubs where pub_id=%s and pub_series_id is not null' % (Record)
                                db.query(query)
                                res = db.store_result()
                                OldPubSeries = ''
                                if res.num_rows():
                                        record = res.fetch_row()
                                        OldPubSeries = record[0][0]

                                # STEP 2 - Update the publication record
                                update = "update pubs set pub_series_id=%s where pub_id=%s" % ('NULL', Record)
                                print("<li> ", update)
                                db.query(update)

                                # STEP 3 - Delete the old publication series if it's now empty
                                if OldPubSeries:
                                        pubseries = pub_series(db)
                                        pubseries.load(OldPubSeries)
                                        pubseries.delete()

                ##########################################################
                # Webpages
                ##########################################################
                value = GetElementValue(merge, 'Webpages')
                if value:
                        ##########################################################
                        # Delete the old webpages
                        ##########################################################
                        delete = 'delete from webpages where pub_id=%d' % int(Record)
                        print('<li> ', delete)
                        db.query(delete)

                        ##########################################################
                        # Insert the new webpages
                        ##########################################################
                        webpages = doc.getElementsByTagName('Webpage')
                        for webpage in webpages:
                                address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                                update = "insert into webpages(pub_id, url) values(%d, '%s')" % (int(Record), db.escape_string(address))
                                print('<li> ', update)
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

                        query = "select authors.author_canonical from authors,pub_authors where authors.author_id=pub_authors.author_id and pub_authors.pub_id='%d';" % (int(Record))
                        db.query(query)
                        res = db.store_result()
                        author = res.fetch_row()
                        OldAuthors = []
                        while author:
                                OldAuthors.append(author[0][0])
                                author = res.fetch_row()
                        for author in OldAuthors:
                                deleteAuthor(author, Record)
                        for author in NewAuthors:
                                addAuthor(author, Record)


                ##########################################################################
                #                 C O N T E N T   S E C T I O N
                ##########################################################################
                if doc.getElementsByTagName('Content'):

                        # If the language of the "referral" title was unknown when we started
                        # updating this pub, try finding it again in case the referral title
                        # is now different
                        if not referral_lang:
                                referral_lang = findReferralLang(pub_id)

                        ###############################################
                        # Content Cover Art
                        ###############################################
                        children = doc.getElementsByTagName('Cover')
                        if len(children):
                                for child in children:
                                        record  = GetChildValue(child, 'Record')
                                        title   = GetChildValue(child, 'cTitle')
                                        if TagPresent(child, 'cArtists'):
                                                artists = GetChildValue(child, 'cArtists')
                                                doArtists = 1
                                        else:
                                                artists = ''
                                                doArtists = 0
                                        date    = GetChildValue(child, 'cDate')
                                        if record:
                                                mergeCover(record, title, artists, date, doArtists)
                                        else:
                                                insertCover(title, artists, date, referral_lang)

                        ###############################################
                        # Content Regular Titles
                        ###############################################
                        children = doc.getElementsByTagName('ContentTitle')
                        if len(children):
                                for child in children:
                                        record  = GetChildValue(child, 'Record')
                                        title   = GetChildValue(child, 'cTitle')
                                        if TagPresent(child, 'cAuthors'):
                                                authors = GetChildValue(child, 'cAuthors')
                                                doAuthors = 1
                                        else:
                                                authors = ''
                                                doAuthors = 0
                                        date    = GetChildValue(child, 'cDate')
                                        if TagPresent(child, 'cPage'):
                                                page = GetChildValue(child, 'cPage')
                                        elif record:
                                                page = 'NoXmlTag'
                                        else:
                                                page = ''
                                        
                                        type    = GetChildValue(child, 'cType')
                                        
                                        if TagPresent(child, 'cLength'):
                                                length = GetChildValue(child, 'cLength')
                                        elif record:
                                                length = 'NoXmlTag'
                                        else:
                                                length = ''
                                                
                                        if record:
                                                mergeTitle(record, title, authors, date, page, type, length, doAuthors)
                                        else:
                                                insertTitle(title, authors, date, page, type, length, referral_lang)

                        ###############################################
                        # Content Review
                        ###############################################
                        children = doc.getElementsByTagName('ContentReview')
                        if len(children):
                                for child in children:
                                        record  = GetChildValue(child, 'Record')
                                        title     = GetChildValue(child, 'cTitle')
                                        if TagPresent(child, 'cBookAuthors'):
                                                authors = GetChildValue(child, 'cBookAuthors')
                                                doBookAuthors = 1
                                        else:
                                                authors = ''
                                                doBookAuthors = 0
                                        if TagPresent(child, 'cReviewers'):
                                                reviewers = GetChildValue(child, 'cReviewers')
                                                doReviewers = 1
                                        else:
                                                reviewers = ''
                                                doReviewers = 0
                                        date      = GetChildValue(child, 'cDate')
                                        if TagPresent(child, 'cPage'):
                                                page = GetChildValue(child, 'cPage')
                                        elif record:
                                                page = 'NoXmlTag'
                                        else:
                                                page = ''
                                        if record:
                                                mergeReview(record, title, authors, reviewers, date, page, doBookAuthors, doReviewers)
                                        else:
                                                insertReview(title, authors, reviewers, date, page, referral_lang)

                        ###############################################
                        # Content Interview
                        ###############################################
                        children = doc.getElementsByTagName('ContentInterview')
                        if len(children):
                                for child in children:
                                        record  = GetChildValue(child, 'Record')
                                        title        = GetChildValue(child, 'cTitle')
                                        if TagPresent(child, 'cInterviewees'):
                                                interviewees = GetChildValue(child, 'cInterviewees')
                                                doInterviewees = 1
                                        else:
                                                interviewees = ''
                                                doInterviewees = 0
                                        if TagPresent(child, 'cInterviewers'):
                                                interviewers = GetChildValue(child, 'cInterviewers')
                                                doInterviewers = 1
                                        else:
                                                interviewers = ''
                                                doInterviewers = 0
                                        date         = GetChildValue(child, 'cDate')
                                        if TagPresent(child, 'cPage'):
                                                page = GetChildValue(child, 'cPage')
                                        elif record:
                                                page = 'NoXmlTag'
                                        else:
                                                page = ''
                                        if record:
                                                mergeInterview(record, title, interviewees, interviewers, date, page, doInterviewees, doInterviewers)
                                        else:
                                                insertInterview(title, interviewees, interviewers, date, page, referral_lang)

                submitter = GetElementValue(merge, 'Submitter')
                if debug == 0:
                        markIntegrated(db, submission, Record, pub_id)

        print(ISFDBLinkNoName('edit/editpub.cgi', Record, 'Edit This Pub', True))
        print(ISFDBLinkNoName('pl.cgi', Record,'View This Pub', True))
        print(ISFDBLinkNoName('edit/verify.cgi', Record, 'Verify This Pub', True))
        print(ISFDBLinkNoName('edit/find_pub_dups.cgi', Record, 'Check for Duplicate Titles', True))
        print('<p>')
        LIBPrintDuplicateWarning(Record)

        PrintPostMod(0)
