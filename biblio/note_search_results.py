#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2018-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 917 $
#     Date: $Date: 2022-05-15 17:54:21 -0400 (Sun, 15 May 2022) $


import cgi
import sys
import string
import os
from isfdb import *
from library import AutoVivification, ISFDBLink
from SQLparsing import *
from common import *
from login import User

class NoteSearch:
        def __init__(self):
                self.operator = ''
                self.operators = ('exact', 'contains', 'starts_with', 'ends_with')
                self.note_value = ''
                self.clause = ''
                self.records = AutoVivification()
                self.record_types = {
                        'Authors': ('author_id', 'author_canonical', 'author_note', 'ea', 'authors', 'author_lastname'),
                        'Titles': ('title_id', 'title_title', 'note_id', 'title', 'titles', 'title_title'),
                        'Synopses': ('title_id', 'title_title', 'title_synopsis', 'title', 'titles', 'title_title'),
                        'Series': ('series_id', 'series_title', 'series_note_id', 'pe', 'series', 'series_title'),
                        'Publications': ('pub_id', 'pub_title', 'note_id', 'pl', 'pubs', 'pub_title'),
                        'Publishers': ('publisher_id', 'publisher_name', 'note_id', 'publisher', 'publishers', 'publisher_name'),
                        'Publication Series': ('pub_series_id', 'pub_series_name', 'pub_series_note_id', 'pubseries', 'pub_series', 'pub_series_name'),
                        'Awards': ('award_id', 'award_title', 'award_note_id', 'award_details', 'awards', 'award_title'),
                        'Award Categories': ('award_cat_id', 'award_cat_name', 'award_cat_note_id', 'award_category', 'award_cats', 'award_cat_name'),
                        'Award Types': ('award_type_id', 'award_type_name', 'award_type_note_id', 'awardtype', 'award_types', 'award_type_name')
                        }
                self.user = User()
                self.user.load()

        def get_search_parameters(self):
                form = cgi.FieldStorage()
                try:
                        self.operator = form['OPERATOR'].value
                        if self.operator not in self.operators:
                                raise
                except:
                        self.display_error('Invalid operator specified')

                try:
                        self.note_value = form['NOTE_VALUE'].value
                        self.note_value = string.strip(self.note_value)
                        self.note_value = self.note_value.replace('*', '%')
                except:
                        self.display_error('No note value specified')

        def build_query_clause(self):
                escaped_value = db.escape_string(self.note_value)
                if self.operator == 'exact':
                        self.clause = "like '%s'" % escaped_value
                elif self.operator == 'contains':
                        self.clause = "like '%%%s%%'" % escaped_value
                elif self.operator == 'starts_with':
                        self.clause = "like '%s%%'" % escaped_value
                elif self.operator == 'ends_with':
                        self.clause = "like '%%%s'" % escaped_value
                
        def display_error(self, message):
                print('<h2>%s</h2>' % message)
                PrintTrailer('search', '', 0)
                sys.exit(0)

        def get_author_notes(self):
                query = """select author_id, author_canonical, author_note, author_lastname
                                from authors where author_note %s limit 1000""" % self.clause
                db.query(query)
                result = db.store_result()
                self.num = result.num_rows()
                record = result.fetch_row()
                while record:
                        author_id = record[0][0]
                        author_name = record[0][1]
                        note_text = record[0][2]
                        author_lastname = record[0][3]
                        self.records['Authors'][author_lastname][author_name][author_id] = note_text
                        record = result.fetch_row()

        def get_other_notes(self):
                notes = {}
                query = """select note_id, note_note from notes where note_note %s order by note_id desc limit 1000""" % self.clause
                db.query(query)
                result = db.store_result()
                self.num = result.num_rows()
                record = result.fetch_row()
                while record:
                        note_id = record[0][0]
                        note_text = record[0][1]
                        notes[note_id] = note_text
                        record = result.fetch_row()
                if not notes:
                        return
                in_clause = dict_to_in_clause(notes)

                for record_type in self.record_types:
                        if record_type == 'Authors':
                                continue
                        table = self.record_types[record_type][4]
                        id_field = self.record_types[record_type][0]
                        name_field = self.record_types[record_type][1]
                        note_field = self.record_types[record_type][2]
                        ordering_field = self.record_types[record_type][5]
                        query = """select %s, %s, %s, %s from %s where %s in (%s)""" % (id_field, name_field, note_field, ordering_field, table, note_field, in_clause)
                        db.query(query)
                        result = db.store_result()
                        self.num = result.num_rows()
                        record = result.fetch_row()
                        while record:
                                record_id = record[0][0]
                                record_name = record[0][1]
                                note_id = record[0][2]
                                note_text = notes[note_id]
                                ordering_name = record[0][3]
                                self.records[record_type][ordering_name][record_name][record_id] = note_text
                                record = result.fetch_row()

        def print_notes(self):
                if not self.records:
                        print('<b>No matching records found.</b>')
                        return
                print('<b>Note Search is currently limited to the first 1000 author matches plus up to 1000 other matches.</b>')
                print('<p><b>Jump to record type:</b>')
                print('<ul>')
                for record_type in sorted(self.record_types):
                        if record_type not in self.records:
                                continue
                        count = 0
                        for ordering_field in self.records[record_type]:
                                for record_name in self.records[record_type][ordering_field]:
                                        count += len(self.records[record_type][ordering_field][record_name])
                        print('<li><a href="#%s">%s</a> (%d)' % (record_type.replace(' ',''), record_type, count))
                print('</ul>')
                for record_type in sorted(self.record_types):
                        if record_type not in self.records:
                                continue
                        print('<h3 id="%s" class="centered">%s</h3>' % (record_type.replace(' ',''), record_type))
                        print('<table>')
                        print('<tr class="table1">')
                        print('<th>#</th>')
                        print('<th>Record Name</th>')
                        print('<th>Note</th>')
                        print('</tr>')
                        cgi_script = self.record_types[record_type][3]
                        bgcolor = 1
                        count = 1
                        for ordering_field in sorted(self.records[record_type]):
                                for record_name in sorted(self.records[record_type][ordering_field]):
                                        for record_id in self.records[record_type][ordering_field][record_name]:
                                                print('<tr class="table%d">' % (bgcolor+1))
                                                print('<td>%d</td>' % count)
                                                print('<td>%s</td>' % ISFDBLink('%s.cgi' % cgi_script, record_id, record_name))
                                                note = self.records[record_type][ordering_field][record_name][record_id]
                                                print('<td>%s</td>' % FormatNote(note,'','full'))
                                                print('</tr>')
                                                bgcolor ^= 1
                                                count += 1
                        print('</table>')

if __name__ == '__main__':

        PrintHeader('ISFDB Note Search')
        PrintNavbar('search', 0, 0, 0, 0)

        search = NoteSearch()
        if not search.user.id:
                print('<h3>For performance reasons, Advanced Searches are currently restricted to registered users.</h3>')
        else:
                search.get_search_parameters()
                search.build_query_clause()
                # Authors are a special case because their notes are kept in the main 'authors' table
                search.get_author_notes()
                search.get_other_notes()
                search.print_notes()
        PrintTrailer('note_search_results', 0, 0)
