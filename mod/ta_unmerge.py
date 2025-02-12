#!_PYTHONLOC
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
import string
from isfdb import *
from isfdblib import *
from common import *
from pubClass import *
from SQLparsing import *
from library import *


def UpdateTitle(TitleRecord, column, value):
        if value:
                update = "update titles set %s='%s' where title_id=%d" % (column, db.escape_string(value), int(TitleRecord))
                print "<li> ", update
                db.query(update)

def doUnmerge(doc):
        # Perform the actual unmerge
        if not doc.getElementsByTagName('TitleUnmerge'):
                return ('','')
        
        merge = doc.getElementsByTagName('TitleUnmerge')
        # Check that the Record (i.e. Title) number and at least one PubRecord (i.e. pub) number are present
        Record = GetElementValue(merge, 'Record')
        if not Record:
                return (merge,'')
        if not doc.getElementsByTagName('PubRecord'):
                return (merge,Record)
        
        title = SQLloadTitle(int(Record))
        # Get all pubs for this Title record and put them in "pubs"
        pubs = SQLGetPubsByTitle(int(Record))

        # Get all pubs that are to be unmerged and put them in "unmergeList"
        unmergeList = []
        children = doc.getElementsByTagName('PubRecord')
        if len(children):
                for child in children:
                        record = int(child.firstChild.data)
                        unmergeList.append(record)

        unmergedTitles = []
        for pub in pubs:
                if pub[PUB_PUBID] not in unmergeList:
                        continue
                #################################################
                # STEP 1 - Save Content details
                #################################################
                query = "select pubc_page from pub_content where title_id=%s and pub_id=%s" % (Record, pub[PUB_PUBID])
                print "<li> ", query
                db.query(query)
                pcresult = db.store_result()
                pcrecord = pcresult.fetch_row()
                try:
                        pagenum = pcrecord[0][0]
                except:
                        pagenum = None
                
                #################################################
                # STEP 2 - Delete Content
                #################################################
                query = "delete from pub_content where title_id=%s and pub_id=%s" % (Record, pub[PUB_PUBID])
                print "<li> ", query
                db.query(query)

                #################################################
                # STEP 3 - Create a new title record
                #################################################
                if title[TITLE_TTYPE] in ('COVERART','INTERIORART','ESSAY','INTERVIEW','POEM','REVIEW','SERIAL','SHORTFICTION'):
                        newTitle = title[TITLE_TITLE]
                else:
                        newTitle = pub[PUB_TITLE]
                query = "insert into titles(title_title, title_copyright, title_ttype) values('%s', '%s', '%s');" % (db.escape_string(newTitle), pub[PUB_YEAR], title[TITLE_TTYPE])
                print "<li> ", query
                db.query(query)
                TitleRecord = db.insert_id()

                UpdateTitle(TitleRecord, 'title_storylen', title[TITLE_STORYLEN])
                UpdateTitle(TitleRecord, 'title_content', title[TITLE_CONTENT])
                UpdateTitle(TitleRecord, 'title_jvn', title[TITLE_JVN])
                UpdateTitle(TitleRecord, 'title_nvz', title[TITLE_NVZ])
                UpdateTitle(TitleRecord, 'title_non_genre', title[TITLE_NON_GENRE])
                UpdateTitle(TitleRecord, 'title_graphic', title[TITLE_GRAPHIC])

                # Append the newly created title record to the list of unmerged titles - will be used for display purposes later
                unmergedTitles.append(TitleRecord)
                if title[TITLE_LANGUAGE]:
                        query = "update titles set title_language=%d where title_id=%d" % (title[TITLE_LANGUAGE], TitleRecord)
                        print "<li> ", query
                        db.query(query)
                
                # If this is a REVIEW and it was linked to its reviewed Title, then link the new Review record to the same reviewed Title
                if title[TITLE_TTYPE] == 'REVIEW':
                        reviewed_title_id = SQLfindReviewedTitle(int(Record))
                        if reviewed_title_id:
                                update = "insert into title_relationships(title_id, review_id) values(%d, %d);" % (int(reviewed_title_id), int(TitleRecord))
                                print "<li> ", update
                                db.query(update)

                #################################################
                # STEP 4 - Add author entries to canonical_author
                #################################################
                # Content titles use same authors: Container titles will use Publication Authors
                if title[TITLE_TTYPE] in ('COVERART','INTERIORART','ESSAY','INTERVIEW','POEM','REVIEW','SERIAL','SHORTFICTION'):
                        query =  "insert into canonical_author(title_id, author_id, ca_status) " 
                        query += "select %d, author_id, ca_status from canonical_author " % (int(TitleRecord))
                        query += "where title_id = %d "  % (int(Record))
                        print "<li> ", query
                        db.query(query)
                else:
                        query = "insert into canonical_author(title_id, author_id, ca_status) select %d, author_id, 1 from pub_authors pa where pa.pub_id = %d" % (int(TitleRecord), int(pub[PUB_PUBID]))
                        print "<li> ", query
                        db.query(query)
        
                #################################################
                # STEP 5 - Add mapping to pub_content
                #################################################
                if pagenum is None:
                        query = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (pub[PUB_PUBID], int(TitleRecord)) 
                else:
                        query = "insert into pub_content(pub_id, title_id, pubc_page) values(%d, %d, '%s');" % (pub[PUB_PUBID], int(TitleRecord), pagenum) 
                print "<li> ", query
                db.query(query)
                print "<li> ##########################################################"
        return (merge, Record, unmergedTitles)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Title Unmerge - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print "<h1>SQL Updates:</h1>"
        print "<hr>"
        print "<ul>"

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        PubidList = []

        (merge, Record, unmergedTitles) = doUnmerge(doc)

        submitter = GetElementValue(merge, 'Submitter')
        markIntegrated(db, submission, Record)

        if Record:
                print ISFDBLinkNoName('title.cgi', Record, 'View Original Title', True)
        count_unmerged = 1
        duplicates_check = []
        for unmergedTitle in unmergedTitles:
                # Display the number of the new title if more than 1 was unmerged
                if len(unmergedTitles) > 1:
                        title_display = 'Title %d' % count_unmerged
                else:
                        title_display = 'Title'
                print ISFDBLinkNoName('title.cgi', unmergedTitle, 'View New %s' % title_display, True)
                count_unmerged += 1
                duplicates_check.append(str(unmergedTitle))
        duplicates_check_string = "+".join(duplicates_check)
        print ISFDBLinkNoName('edit/find_title_dups.cgi', duplicates_check_string, 'Check for Duplicate Titles', True)
        print '<p>'

        PrintPostMod(0)
