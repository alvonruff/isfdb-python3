#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Ahasuerus, Bill Longley and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 752 $
#     Date: $Date: 2021-09-17 18:33:04 -0400 (Fri, 17 Sep 2021) $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from authorClass import *

submission    = 0
submitter     = 0
reviewer      = 0

def authorHistory(author_id, field, from_value, to_value):
        if field == 'author_canonical':
                field_index = AUTHOR_CANONICAL
        elif field == 'author_legalname':
                field_index = AUTHOR_LEGALNAME
        elif field == 'author_lastname':
                field_index = AUTHOR_LASTNAME
        elif field == 'author_birthplace':
                field_index = AUTHOR_BIRTHPLACE
        elif field == 'author_birthdate':
                field_index = AUTHOR_BIRTHDATE
        elif field == 'author_deathdate':
                field_index = AUTHOR_DEATHDATE
        elif field == 'author_image':
                field_index = AUTHOR_IMAGE
        elif field == 'author_note_id':
                field_index = AUTHOR_NOTE_ID
        elif field == 'author_emails':
                field_index = AUTHOR_EMAILS
        elif field == 'author_webpages':
                field_index = AUTHOR_WEBPAGES
        elif field == 'author_language':
                field_index = AUTHOR_LANGUAGE
        elif field == 'author_trans_legal_name':
                field_index = AUTHOR_TRANS_LEGALNAME
        elif field == 'author_trans_name':
                field_index = AUTHOR_TRANS_NAME
        elif field == 'author_note':
                field_index = AUTHOR_NOTE
        setHistory(AUTHOR_UPDATE, author_id, field_index, submission, submitter, from_value, to_value)


def UpdateColumn(doc, tag, column, id):
        if TagPresent(doc, tag):

                ###########################################
                # Get the old value
                ###########################################
                query = "select %s from authors where author_id=%s" % (column, id)
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                from_value = record[0][0]
                # If there is a value on file, change it to a string
                if from_value:
                        from_value = str(from_value)
                        print type(from_value)

                to_value = GetElementValue(doc, tag)
                # For languages, retrieve the language code based on the language name
                if tag == 'Language':
                        to_value = str(SQLGetLangIdByName(to_value))
                if to_value:
                        update = "update authors set %s='%s' where author_id=%s" % (column, db.escape_string(to_value), id)
                        authorHistory(id, column, from_value, to_value)
                else:
                        update = "update authors set %s = NULL where author_id=%s" % (column, id)
                        authorHistory(id, column, from_value, 'NULL')
                print "<li> ", update
                db.query(update)

def UpdateMultiple(author_id, field_name, table_name, author_field, tag_name, history_column):
        ##########################################################
        # Construct the string of old values
        ##########################################################
        query = "select %s from %s where %s=%d" % (field_name, table_name, author_field, int(author_id))
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        from_value = ''
        while record:
                if from_value == '':
                        from_value += record[0][0]
                else:
                        from_value += ","+record[0][0]
                record = result.fetch_row()

        ##########################################################
        # Delete the old records
        ##########################################################
        delete = "delete from %s where %s=%d" % (table_name, author_field, int(author_id))
        print "<li> ", delete
        db.query(delete)

        ##########################################################
        # Insert the new records
        ##########################################################
        to_value = ''
        elements = doc.getElementsByTagName(tag_name)
        for element in elements:
                new_value = XMLunescape(element.firstChild.data.encode('iso-8859-1'))
                update = "insert into %s(%s, %s) values(%d, '%s')" % (table_name,
                                                                      author_field, field_name, int(author_id), db.escape_string(new_value))
                print "<li> ", update
                db.query(update)

                # Construct the new list of values
                if to_value == '':
                        to_value += new_value
                else:
                        to_value += ","+new_value

        authorHistory(author_id, history_column, from_value, to_value)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Author Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print "<h1>SQL Updates:</h1>"
        print "<hr>"
        print "<ul>"

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('AuthorUpdate'):
                merge = doc.getElementsByTagName('AuthorUpdate')
                Record = GetElementValue(merge, 'Record')
                subname = GetElementValue(merge, 'Submitter')
                submitter = SQLgetSubmitterID(subname)

                current = authors(db)
                current.load(int(Record))

                UpdateColumn(merge, 'Canonical',  'author_canonical',  Record)

                if GetElementValue(merge, 'AuthorTransNames'):
                        UpdateMultiple(Record, 'trans_author_name', 'trans_authors', 'author_id', 'AuthorTransName', 'author_trans_name')

                UpdateColumn(merge, 'Legalname',  'author_legalname',  Record)

                if GetElementValue(merge, 'AuthorTransLegalNames'):
                        UpdateMultiple(Record, 'trans_legal_name', 'trans_legal_names', 'author_id', 'AuthorTransLegalName', 'author_trans_legal_name')

                UpdateColumn(merge, 'Birthplace', 'author_birthplace', Record)
                UpdateColumn(merge, 'Birthdate',  'author_birthdate',  Record)
                UpdateColumn(merge, 'Deathdate',  'author_deathdate',  Record)
                UpdateColumn(merge, 'Language',   'author_language',   Record)
                UpdateColumn(merge, 'Image',      'author_image',      Record)
                UpdateColumn(merge, 'Note',       'author_note',       Record)

                value = GetElementValue(merge, 'Familyname')
                if value:
                        query = "select author_lastname from authors where author_id=%s" % (Record)
                        db.query(query)
                        result = db.store_result()
                        record = result.fetch_row()
                        oldlastname = record[0][0]
                        newlastname = GetElementValue(merge, 'Familyname')
                        UpdateColumn(merge, 'Familyname',   'author_lastname',   Record)
                        if oldlastname[0:2] != newlastname[0:2]:
                                #update_directory(oldlastname[0:2])
                                #update_directory(newlastname[0:2])
                                update_directory(oldlastname)
                                update_directory(newlastname)

                if GetElementValue(merge, 'Emails'):
                        UpdateMultiple(Record, 'email_address', 'emails', 'author_id', 'Email', 'author_emails')

                if GetElementValue(merge, 'Webpages'):
                        UpdateMultiple(Record, 'url', 'webpages', 'author_id', 'Webpage', 'author_webpages')

                markIntegrated(db, submission, Record)

        print ISFDBLinkNoName('edit/editauth.cgi', Record, 'Edit This Author', True)
        print ISFDBLinkNoName('ea.cgi', Record, 'View This Author', True)
        print '<p>'

        PrintPostMod(0)
