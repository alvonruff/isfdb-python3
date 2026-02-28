from __future__ import print_function
#
#     (C) COPYRIGHT 2008-2026   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1271 $
#     Date: $Date: 2026-02-27 16:20:27 -0500 (Fri, 27 Feb 2026) $

import cgi
from isfdb import *
from isfdblib import *
from library import *
from xml.dom import minidom


class publishers:
        def __init__(self, db):
                self.db = db
                self.used_id = 0
                self.used_name = 0
                self.used_trans_names = 0
                self.used_webpages = 0
                self.used_note = 0

                self.publisher_id = ''
                self.publisher_name = ''
                self.publisher_trans_names = []
                self.publisher_note = ''
                self.publisher_note_id = ''
                self.publisher_webpages = []

                self.error = ''

        def load(self, id):
                record = SQLGetPublisher(id)
                if record:
                        if record[PUBLISHER_ID]:
                                self.publisher_id = record[PUBLISHER_ID]
                                self.used_id = 1

                        if record[PUBLISHER_NAME]:
                                self.publisher_name = record[PUBLISHER_NAME]
                                self.used_name = 1

                        res2 = SQLloadTransPublisherNames(record[PUBLISHER_ID])
                        if res2:
                                self.publisher_trans_names = res2
                                self.used_trans_names = 1

                        if record[PUBLISHER_NOTE]:
                                note = SQLgetNotes(record[PUBLISHER_NOTE])
                                if note:
                                        self.publisher_note_id = record[PUBLISHER_NOTE]
                                        self.publisher_note = note
                                        self.used_note = 1

                        self.publisher_webpages = SQLloadPublisherWebpages(record[PUBLISHER_ID])
                        if self.publisher_webpages:
                                self.used_webpages = 1
                else:
                        self.error = 'Publisher record not found'
                        return

        def obj2xml(self):
                if self.used_id:
                        container = "<UpdatePublisher>\n"
                        container += "  <PublisherId>%s</PublisherId>\n" % (self.publisher_id)
                        if self.used_name:
                                container += "  <PublisherName>%s</PublisherName>\n" % \
                                                (self.publisher_name)
                        if self.used_webpages:
                                container += "  <PublisherWebpages>%s</PublisherWebpages>\n" % \
                                                (self.publisher_webpages)
                        container += "</UpdatePublisher>\n"
                else:
                        print("XML: pass")
                        container = ""
                return container


        def xml2obj(self, xml):
                doc = minidom.parseString(xml)
                metadata = doc.getElementsByTagName('UpdatePublisher')
                if not metadata:
                        metadata = doc.getElementsByTagName('NewPublisher')
                if not metadata:
                        return

                elem = GetElementValue(metadata, 'PublisherName')
                if elem:
                        self.used_name = 1
                        self.publisher_name = elem

                elem = GetElementValue(metadata, 'PublisherWebpages')
                if elem:
                        self.used_webpages = 1
                        self.publisher_webpages = elem


        def cgi2obj(self):
                from login import User
                self.form = IsfdbFieldStorage()
                try:
                        self.publisher_id = str(int(self.form['publisher_id'].value))
                        self.used_id = 1
                except (KeyError, ValueError):
                        self.error = "Publisher ID must be an integer number"
                        return
                try:
                        self.publisher_name = XMLescape(self.form['publisher_name'].value)
                except KeyError:
                        self.error = 'Publisher name is required'
                        return
                if not self.publisher_name:
                        self.error = 'Publisher name is required'
                        return
                self.used_name = 1
                unescaped_name = XMLunescape(self.publisher_name)

                # Limit the ability to edit publisher names to moderators
                user = User()
                user.load()
                user.load_moderator_flag()
                if not user.moderator:
                        # Retrieve the publisher name that is currently on file for this publisher ID
                        current_publisher = SQLGetPublisher(self.publisher_id)
                        if current_publisher[PUBLISHER_NAME] != unescaped_name:
                                self.error = 'Only moderators can edit publisher names'
                                return

                # If the publisher name has been edited, check if another publisher with the new name
                # already exists in the database
                current_publisher = SQLFindPublisher(unescaped_name, 'exact')
                if current_publisher:
                        if int(self.publisher_id) != int(current_publisher[0][PUBLISHER_ID]):
                                self.error = "Publisher '%s' already exists" % current_publisher[0][PUBLISHER_NAME]
                                return

                for key in self.form:
                        if 'trans_publisher_names' in key:
                                value = XMLescape(self.form[key].value)
                                if value:
                                        self.publisher_trans_names.append(value)
                                        self.used_trans_names = 1

                if 'publisher_note' in self.form:
                        self.publisher_note = XMLescape(self.form['publisher_note'].value)
                        self.used_note = 1

                counter = 1
                for key in self.form:
                        if key[:18] == 'publisher_webpages':
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.publisher_webpages:
                                                continue
                                        self.error = invalidURL(value)
                                        if self.error:
                                                return
                                        self.publisher_webpages.append(value)
                                        self.used_webpages = 1

        def delete(self):
                if not self.publisher_id:
                        return

                query = 'select COUNT(publisher_id) from pubs where publisher_id=%d' % (int(self.publisher_id))
                print("<li> ", query)
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHONE()
                # Do not delete the publisher if there are pubs associated with it
                if record[0][0] != 0:
                        return

                delete = 'delete from publishers where publisher_id=%d' % int(self.publisher_id)
                print("<li> ", delete)
                CNX.DB_QUERY(delete)
                delete = 'delete from trans_publisher where publisher_id=%d' % int(self.publisher_id)
                print("<li> ", delete)
                CNX.DB_QUERY(delete)
                delete = "delete from webpages where publisher_id=%d" % int(self.publisher_id)
                print("<li> ", delete)
                CNX.DB_QUERY(delete)
                if self.publisher_note:
                        delete = "delete from notes where note_id=%d" % int(self.publisher_note_id)
                        print("<li> ", delete)
                        CNX.DB_QUERY(delete)
