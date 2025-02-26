from __future__ import print_function
#
#     (C) COPYRIGHT 2010-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 796 $
#     Date: $Date: 2021-11-02 19:08:22 -0400 (Tue, 02 Nov 2021) $

import cgi
import sys
import os
from isfdb import *
from isfdblib import *
from library import *
from xml.dom import minidom
from xml.dom import Node


class pub_series:
        def __init__(self, db):
                self.db = db
                self.used_id = 0
                self.used_name = 0
                self.used_trans_names = 0
                self.used_webpages = 0
                self.used_note = 0

                self.pub_series_id = ''
                self.pub_series_name = ''
                self.pub_series_trans_names = []
                self.pub_series_note = ''
                self.pub_series_note_id = ''
                self.pub_series_webpages = []

                self.error = ''

        def load(self, id):
                record = SQLGetPubSeries(id)
                if record:
                        if record[PUB_SERIES_ID]:
                                self.pub_series_id = record[PUB_SERIES_ID]
                                self.used_id = 1

                        if record[PUB_SERIES_NAME]:
                                self.pub_series_name = record[PUB_SERIES_NAME]
                                self.used_name = 1

                        res2 = SQLloadTransPubSeriesNames(record[PUB_SERIES_ID])
                        if res2:
                                self.pub_series_trans_names = res2
                                self.used_trans_names = 1

                        if record[PUB_SERIES_NOTE]:
                                note = SQLgetNotes(record[PUB_SERIES_NOTE])
                                if note:
                                        self.pub_series_note_id = record[PUB_SERIES_NOTE]
                                        self.pub_series_note = note
                                        self.used_note = 1

                        self.pub_series_webpages = SQLloadPubSeriesWebpages(record[PUB_SERIES_ID])
                        if self.pub_series_webpages:
                                self.used_webpages = 1
                else:
                        print("ERROR: publication series record not found: ", id)
                        self.error = 'Publication series record not found'
                        return

        # Currently unused
        def obj2xml(self):
                if self.used_id:
                        container = "<UpdatePubSeries>\n"
                        container += "  <PubSeriesId>%s</PubSeriesId>\n" % (self.pub_series_id)
                        if self.used_name:
                                container += "  <PubSeriesName>%s</PubSeriesName>\n" % \
                                                (self.pub_series_name)
                        if self.used_webpages:
                                container += "  <PubSeriesWebpages>%s</PubSeriesWebpages>\n" % \
                                                (self.pub_series_webpages)
                        container += "</UpdatePubSeries>\n"
                else:
                        print("XML: pass")
                        container = ""
                return container


        def xml2obj(self, xml):
                doc = minidom.parseString(xml)
                metadata = doc.getElementsByTagName('UpdatePubSeries')
                if metadata == 0:
                        metadata = doc.getElementsByTagName('NewPubSeries')
                if metadata == 0:
                        return

                elem = GetElementValue(metadata, 'PubSeriesName')
                if elem:
                        self.used_name = 1
                        self.pub_series_name = elem

                elem = GetElementValue(metadata, 'PubSeriesWebpages')
                if elem:
                        self.used_webpages = 1
                        self.pub_series_webpages = elem


        def cgi2obj(self):
                self.form = IsfdbFieldStorage()
                try:
                        self.pub_series_id = str(int(self.form['pub_series_id'].value))
                        self.used_id = 1
                except:
                        self.error = 'Publication Series ID must be an integer number'
                        return
                try:
                        self.pub_series_name = XMLescape(self.form['pub_series_name'].value)
                        self.used_name = 1
                        if not self.pub_series_name:
                                raise
                except:
                        self.error = 'Publication Series name is required'
                        return

                # Unescape the pub series name to ensure that the lookup finds it in the database
                current_pub_series = SQLGetPubSeriesByName(XMLunescape(self.pub_series_name))
                if current_pub_series:
                        if int(self.pub_series_id) != int(current_pub_series[PUB_SERIES_ID]):
                                self.error = "Publication series '%s' already exists" % current_pub_series[PUB_SERIES_NAME]
                                return

                for key in self.form:
                        if 'trans_pub_series_names' in key:
                                value = XMLescape(self.form[key].value)
                                if value:
                                        self.pub_series_trans_names.append(value)
                                        self.used_trans_names = 1

                if 'pub_series_note' in self.form:
                        self.pub_series_note = XMLescape(self.form['pub_series_note'].value)
                        self.used_note = 1

                counter = 1
                for key in self.form:
                        if key[:19] == 'pub_series_webpages':
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.pub_series_webpages:
                                                continue
                                        self.error = invalidURL(value)
                                        if self.error:
                                                return
                                        self.pub_series_webpages.append(value)
                                        self.used_webpages = 1

        def delete(self):
                if not self.pub_series_id:
                        return

                CNX = MYSQL_CONNECTOR()
                query = 'select COUNT(pub_series_id) from pubs where pub_series_id=%d' % (int(self.pub_series_id))
                print("<li> ", query)
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHONE()
                # Do not delete the publication series if there are pubs associated with it
                if record[0][0] != 0:
                        return

                query = 'delete from pub_series where pub_series_id=%d' % (int(self.pub_series_id))
                print("<li> ", query)
                CNX.DB_QUERY(query)

                query = 'delete from trans_pub_series where pub_series_id=%d' % (int(self.pub_series_id))
                print("<li> ", query)
                CNX.DB_QUERY(query)

                delete = "delete from webpages where pub_series_id=%d" % (int(self.pub_series_id))
                print("<li> ", delete)
                CNX.DB_QUERY(delete)

                if self.pub_series_note:
                        delete = "delete from notes where note_id=%d" % int(self.pub_series_note_id)
                        print("<li> ", delete)
                        CNX.DB_QUERY(delete)
