#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1165 $
#     Date: $Date: 2024-02-06 13:18:28 -0500 (Tue, 06 Feb 2024) $


from isfdb import *
from common import *
from isfdblib import *
from library import *
from SQLparsing import *
from xml.dom import minidom
from xml.dom import Node


def moveAuthorColumn(db, column, keep, drop):
        query = "select %s from authors where author_id='%d'" % (column, int(drop))
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        value = str(record[0][0])
        if value == 'None':
                update = "update authors set %s=NULL where author_id='%d'" % (column, int(keep))
        else:
                update = "update authors set %s='%s' where author_id='%d'" % (column, db.escape_string(value), int(keep))
        print("<li> ", update)
        db.query(update)

def MergeMultiple(keep_values, drop_values, table_name, author_column, value_column, KeepId):
        for value in drop_values:
                # If this value is not already associated with the author that we will keep,
                # then insert it into the table for the kept author
                if value not in keep_values:
                        update = "insert into %s(%s, %s) values(%d, '%s')" % (table_name, author_column, value_column, int(KeepId), db.escape_string(value))
                        db.query(update)
                        print("<li> ", update)

########################################################################

def AuthorMerge(db, recno, doc):
        merge = doc.getElementsByTagName('AuthorMerge')
        KeepId = GetElementValue(merge, 'KeepId')
        DropId = GetElementValue(merge, 'DropId')

        id = GetElementValue(merge, 'Canonical')
        if id and id != KeepId:
                moveAuthorColumn(db, 'author_canonical', KeepId, DropId)

        # Merge the two authors' transliterated canonical names
        keep_names = SQLloadTransAuthorNames(int(KeepId))
        drop_names = SQLloadTransAuthorNames(int(DropId))
        MergeMultiple(keep_names, drop_names, 'trans_authors', 'author_id', 'trans_author_name', KeepId)

        id = GetElementValue(merge, 'Legalname')
        if id and id != KeepId:
                moveAuthorColumn(db, 'author_legalname', KeepId, DropId)

        # Merge the two authors' transliterated legal names
        keep_legal_names = SQLloadTransLegalNames(int(KeepId))
        drop_legal_names = SQLloadTransLegalNames(int(DropId))
        MergeMultiple(keep_legal_names, drop_legal_names, 'trans_legal_names', 'author_id', 'trans_legal_name', KeepId)

        id = GetElementValue(merge, 'Familyname')
        if id and id != KeepId:
                moveAuthorColumn(db, 'author_lastname', KeepId, DropId)

        id = GetElementValue(merge, 'Birthplace')
        if id and id != KeepId:
                moveAuthorColumn(db, 'author_birthplace', KeepId, DropId)

        id = GetElementValue(merge, 'Birthdate')
        if id and id != KeepId:
                moveAuthorColumn(db, 'author_birthdate', KeepId, DropId)

        id = GetElementValue(merge, 'Deathdate')
        if id and id != KeepId:
                moveAuthorColumn(db, 'author_deathdate', KeepId, DropId)

        id = GetElementValue(merge, 'Image')
        if id and id != KeepId:
                moveAuthorColumn(db, 'author_image', KeepId, DropId)

        id = GetElementValue(merge, 'Language')
        if id and id != KeepId:
                moveAuthorColumn(db, 'author_language', KeepId, DropId)

        id = GetElementValue(merge, 'Note')
        if id and id != KeepId:
                moveAuthorColumn(db, 'author_note', KeepId, DropId)

        # Merge the two authors' e-mail addresses
        keep_emails = SQLloadEmails(int(KeepId))
        drop_emails = SQLloadEmails(int(DropId))
        MergeMultiple(keep_emails, drop_emails, 'emails', 'author_id', 'email_address', KeepId)

        # Merge the two authors' Web pages
        keep_webpages = SQLloadWebpages(int(KeepId))
        drop_webpages = SQLloadWebpages(int(DropId))
        MergeMultiple(keep_webpages, drop_webpages, 'webpages', 'author_id', 'url', KeepId)

        update = "update canonical_author set author_id='%d' where author_id='%d'" % (int(KeepId), int(DropId))
        print("<li> ", update)
        db.query(update)

        update = "update pub_authors set author_id='%d' where author_id='%d'" % (int(KeepId), int(DropId))
        print("<li> ", update)
        db.query(update)

        # Re-point the deleted author's alternate names to the kept author ID
        update = "update pseudonyms set author_id = %d where author_id = %d" % (int(KeepId), int(DropId))
        print("<li> ", update)
        db.query(update)

        # Check if there are any references left to the dropped author
        for i in ['canonical_author', 'pub_authors']:
                query = 'select COUNT(author_id) from %s where author_id=%d' % (i, int(DropId))
                db.query(query)
                res = db.store_result()
                record = res.fetch_row()
                if record[0][0]:
                        return KeepId

        deleteFromAuthorTable(DropId)
        return KeepId

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Author Merge Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('AuthorMerge')
        if merge:
                KeepId = AuthorMerge(db, submission, doc)
                markIntegrated(db, submission, KeepId)
                print(ISFDBLinkNoName('ea.cgi', KeepId, 'View This Author', True))
        PrintPostMod(0)
