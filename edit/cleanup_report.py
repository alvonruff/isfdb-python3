#!_PYTHONLOC
#
#     (C) COPYRIGHT 2011-2025   Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1217 $
#     Date: $Date: 2025-01-29 17:08:02 -0500 (Wed, 29 Jan 2025) $

import string
import sys
import MySQLdb
import cgi
from cleanup_lib import *
from isfdb import *
from isfdblib import *
from SQLparsing import *
from library import *
from login import User

class Cleanup():
        def __init__(self):
                self.query = ''
                self.none = ''
                self.ignore = 0
                self.report_id = 0
                self.note = ''
                self.print_record_function = None
                self.record_name = ''

        def print_generic_table(self):
                db.query(self.query)
                result = db.store_result()
                num = result.num_rows()

                if num > 0:
                        if self.note:
                                print '<div class="bold">%s</div>' % self.note
                        record = result.fetch_row()
                        bgcolor = 1
                        if self.ignore:
                                PrintTableColumns(('#', self.record_name, 'Ignore'))
                        else:
                                PrintTableColumns(('#', self.record_name))
                        count = 1
                        while record:
                                record_id = record[0][0]
                                record_title = record[0][1]
                                if self.ignore:
                                        cleanup_id = record[0][2]
                                        self.print_record_function(record_id, record_title, bgcolor, count, cleanup_id, self.report_id)
                                else:
                                        self.print_record_function(record_id, record_title, bgcolor, count)
                                bgcolor ^= 1
                                count += 1
                                record = result.fetch_row()
                        print '</table>'
                else:
                        print '<h2>%s.</h2>' % self.none

        def print_pub_table(self):
                self.print_record_function = PrintPublicationRecord
                self.record_name = 'Publication'
                self.print_generic_table()

        def print_title_table(self):
                self.print_record_function = PrintTitleRecord
                self.record_name = 'Title'
                self.print_generic_table()

        def print_author_table(self):
                self.print_record_function = self.PrintAuthorRecord
                self.record_name = 'Author'
                self.print_generic_table()

        def print_award_table(self):
                self.print_record_function = PrintAwardRecord
                self.record_name = 'Award'
                self.print_generic_table()

        def print_publisher_table(self):
                self.print_record_function = PrintPublisherRecord
                self.record_name = 'Publisher'
                self.print_generic_table()

        def print_pub_series_table(self):
                self.print_record_function = PrintPubSeriesRecord
                self.record_name = 'Publication Series'
                self.print_generic_table()

        def print_series_table(self):
                self.print_record_function = PrintSeriesRecord
                self.record_name = 'Series'
                self.print_generic_table()

        def invalid_title_types(self, pub_type, excluded_title_types):
                excluded = ExcludedTitleTypes()
                excluded.report_id = self.report_id
                excluded.pub_type = pub_type
                excluded.excluded_title_types = excluded_title_types
                excluded.retrieve_data()
                excluded.print_data()

        def print_pub_with_date_table(self):
                db.query(self.query)
                result = db.store_result()
                num = result.num_rows()
                if num > 0:
                        if self.note:
                                print '<h3>%s</h3>' % self.note
                        record = result.fetch_row()
                        bgcolor = 1
                        count = 1
                        PrintTableColumns(('', 'Publication', 'Date'))
                        while record:
                                pub_id = record[0][0]
                                pub_title = record[0][1]
                                pub_date = record[0][2]
                                if bgcolor:
                                        print '<tr align=left class="table1">'
                                else:
                                        print '<tr align=left class="table2">'

                                print '<td>%d</td>' % int(count)
                                print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                                print '<td>%s</td>' % pub_date
                                print '</tr>'
                                bgcolor ^= 1
                                count += 1
                                record = result.fetch_row()
                        print '</table>'
                else:
                        print '<h2>%s</h2>' % self.none

        def PrintAuthorRecord(self, author_id, author_name, bgcolor, count, cleanup_id = 0, report_id = 0, mode = 1):
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%d</td>' % int(count)
                print '<td>%s</td>' % ISFDBLink('ea.cgi', author_id, author_name)
                if cleanup_id and user.moderator:
                        message = {0: 'Resolve', 1: 'Ignore'}
                        print '<td>%s</td>' % ISFDBLinkNoName('mod/resolve_cleanup.cgi',
                                                              '%d+%d+%d' % (int(cleanup_id), int(mode), int(report_id)),
                                                              '%s this author' % message[mode])
                print '</tr>'

        def books_with_trans_and_no_pubs(self, lang_name, length = 'long'):
                if length == 'short':
                        in_clause = 'not in'
                else:
                        in_clause = 'in'
                self.query = """select t1.title_id, t1.title_title
                        from titles t1, languages l, cleanup c
                        where t1.title_id = c.record_id
                        and c.report_type = %d
                        and exists
                                (select 1 from titles t2
                                where t2.title_parent = t1.title_id
                                and t2.title_language != t1.title_language)
                        and not exists
                                (select 1 from pub_content pc
                                where pc.title_id = t1.title_id)
                        and not exists
                                (select 1 from titles t3
                                where t3.title_parent = t1.title_id
                                and t3.title_language = t1.title_language)
                        and t1.title_language = l.lang_id
                        and l.lang_name = '%s'
                        and t1.title_copyright not in ('8888-00-00', '0000-00-00')
                        and t1.title_ttype %s ('NOVEL', 'COLLECTION', 'ANTHOLOGY', 'NONFICTION', 'OMNIBUS')
                        order by t1.title_title""" % (self.report_id, lang_name, in_clause)
                self.none = 'No %s %s titles with no publications, no same-language VT and with a translation' % (lang_name, length)
                self.note = """For the purposes of this report, "book" or "long" title types are defined as
                               NOVEL, COLLECTION, ANTHOLOGY, NONFICTION, and OMNIBUS. All other title types
                               are considered "short". Titles with 0000-00-00 and 8888-00-00 dates are not
                               included."""
                self.print_title_table()

        def other_books_with_trans_and_no_pubs(self, length = 'long'):
                if length == 'short':
                        in_clause = 'not in'
                else:
                        in_clause = 'in'
                self.query = """select t1.title_id, t1.title_title, l.lang_name, t1.title_ttype
                        from titles t1, languages l, cleanup c
                        where t1.title_id = c.record_id
                        and c.report_type = %d
                        and exists
                                (select 1 from titles t2
                                where t2.title_parent = t1.title_id
                                and t2.title_language != t1.title_language)
                        and not exists
                                (select 1 from pub_content pc
                                where pc.title_id = t1.title_id)
                        and not exists
                                (select 1 from titles t3
                                where t3.title_parent = t1.title_id
                                and t3.title_language = t1.title_language)
                        and t1.title_language = l.lang_id
                        and l.lang_name not in ('English', 'French', 'German', 'Italian', 'Japanese', 'Russian', 'Spanish')
                        and t1.title_copyright not in ('8888-00-00', '0000-00-00')
                        and t1.title_ttype %s ('NOVEL', 'COLLECTION', 'ANTHOLOGY', 'NONFICTION', 'OMNIBUS')
                        order by l.lang_name, t1.title_title""" % (self.report_id, in_clause)
                self.none = 'No %s titles with no publications and with a translation in other languages' % length
                self.note = """For the purposes of this report, "book" or "long" title types are defined as
                               NOVEL, COLLECTION, ANTHOLOGY, NONFICTION, and OMNIBUS. All other title types
                               are considered "short". Titles with 0000-00-00 and 8888-00-00 dates are not
                               included."""

                db.query(self.query)
                result = db.store_result()
                num = result.num_rows()

                if num > 0:
                        if self.note:
                                print '<div class="bold">%s</div>' % self.note
                        record = result.fetch_row()
                        bgcolor = 1
                        PrintTableColumns(('#', 'Language', 'Title', 'Type'))
                        count = 1
                        while record:
                                record_id = record[0][0]
                                record_title = record[0][1]
                                record_language = record[0][2]
                                record_type = record[0][3]
                                if bgcolor:
                                        print '<tr align=left class="table1">'
                                else:
                                        print '<tr align=left class="table2">'

                                print '<td>%d</td>' % count
                                print '<td>%s</td>' % record_language
                                print '<td>%s</td>' % ISFDBLink('title.cgi', record_id, record_title)
                                print '<td>%s</td>' % record_type
                                print '</tr>'
                                bgcolor ^= 1
                                count += 1
                                record = result.fetch_row()
                        print '</table>'
                else:
                        print '<h2>%s.</h2>' % self.none

class ExcludedTitleTypes():
        def __init__(self):
                self.query = ''
                self.ignore = 0
                self.note = ''
                self.pub_type = ''
                self.excluded_title_types = ()
                self.report_id = 0
                self.pub_id = 0
                self.pub_title = ''
                self.mode = 1

        def retrieve_data(self):
                self.query = """select p.pub_id, p.pub_title, c.cleanup_id
                        from pubs p, cleanup c
                        where p.pub_ctype='%s'
                        and exists
                        (select 1 from pub_content pc, titles t
                        where pc.pub_id=p.pub_id
                        and t.title_id=pc.title_id
                        and t.title_ttype in (%s)
                        )
                        and c.report_type = %d
                        and p.pub_id = c.record_id
                        order by p.pub_title""" % (self.pub_type, list_to_in_clause(self.excluded_title_types), self.report_id)
                self.none = 'No %s Publications with Invalid Title Types' % self.pub_type.lower().capitalize()
                self.note = 'Invalid title types for %s publications: %s' % (self.pub_type.capitalize(), ', '.join(self.excluded_title_types))
                db.query(self.query)
                self.result = db.store_result()
                self.num = self.result.num_rows()

        def print_data(self):
                if self.num > 0:
                        if self.note:
                                print '<h3>%s</h3>' % self.note
                        record = self.result.fetch_row()
                        if self.ignore:
                                PrintTableColumns(('#', 'Publication', 'Invalid Titles', 'Ignore'))
                        else:
                                PrintTableColumns(('#', 'Publication', 'Invalid Titles'))
                        self.bgcolor = 1
                        self.count = 1
                        while record:
                                self.pub_id = record[0][0]
                                self.pub_title = record[0][1]
                                self.cleanup_id = record[0][2]
                                self.print_row()
                                self.bgcolor ^= 1
                                self.count += 1
                                record = self.result.fetch_row()
                        print '</table>'
                else:
                        print '<h2>%s.</h2>' % self.none

        def print_row(self):
                if self.bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%d</td>' % self.count
                print '<td>%s</td>' % ISFDBLink('pl.cgi', self.pub_id, self.pub_title)
                invalid_titles = SQLloadTitlesXBT(self.pub_id)
                print '<td>'
                first_title = True
                for title in invalid_titles:
                        if title[TITLE_TTYPE] in self.excluded_title_types:
                                if not first_title:
                                        print '<br>'
                                print '%s - ' % title[TITLE_TTYPE]
                                print ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE])
                                first_title = False
                print '</td>'
                if self.ignore and user.moderator:
                        message = {0: 'Resolve', 1: 'Ignore'}
                        print '<td>%s</td>' % ISFDBLinkNoName('mod/resolve_cleanup.cgi',
                                                              '%d+%d+%d' % (int(self.cleanup_id), self.mode, self.report_id),
                                                              '%s this publication' % message[self.mode])
                print '</tr>'

def PrintTableColumns(columns):
        print '<table class="generic_table">'
        print '<tr class="table2">'
        for column in columns:
                if not column:
                        data = '&nbsp;'
                else:
                        data = column
                # Skip 'Ignore' and 'Resolve' columns if the user is not a moderator
                if ('Ignore' in column or 'Resolve' in column) and not user.moderator:
                        continue
                print '<td><b>%s</b></td>' % data
        print '</tr>'

def nonModeratorMessage():
        if not user.moderator:
                print """<h2>If you find a record that is listed erroneously,
                please post on the Moderator Noticeboard and a moderator will
                remove it from this report.</h2>"""

def function1():
        query = """select c.cleanup_id, c.record_id, t.title_title  
                from cleanup c, titles t
                where c.record_id = t.title_id
                and not exists
                 (select ca.title_id from canonical_author ca where ca.title_id = t.title_id)
                and c.report_type=1 
                order by t.title_title"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()

        if num:
                PrintTableColumns(('', 'Title',))
                bgcolor = 1
                count = 1
                while record:
                        title_id = record[0][1]
                        title_title = record[0][2]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table><p>'
        else:
                print "<h2>No titles without authors found</h2>"

def function2():
        nonModeratorMessage()
        query = """select c.cleanup_id, c.record_id, t.title_title
                from cleanup c, titles t
                where c.record_id=t.title_id and c.report_type=2 and c.resolved IS NULL
                and t.title_parent is not null and t.title_parent <> 0
                and not exists ( 
                  select * from canonical_author vca, canonical_author pca 
                  where vca.title_id = t.title_id and pca.title_id = t.title_parent 
                  and vca.author_id = pca.author_id 
                ) 
                and not exists ( 
                  select * from canonical_author vca, canonical_author pca, pseudonyms p 
                  where vca.title_id = t.title_id and pca.title_id = t.title_parent 
                  and p.pseudonym = vca.author_id and p.author_id = pca.author_id 
                ) 
                and not exists ( 
                  select * from canonical_author vca, canonical_author pca 
                  where vca.title_id = t.title_id and pca.title_id = t.title_parent 
                  and (pca.author_id = 20754 or pca.author_id = 2862 or pca.author_id = 38721 
                  or vca.author_id = 20754 or vca.author_id = 2862 or vca.author_id = 38721 
                  or vca.author_id = 7977 or vca.author_id = 1449 or vca.author_id = 1414 
                  or vca.author_id = 3781 or vca.author_id = 6358 or vca.author_id = 38941 
                  or pca.author_id = 6677 or vca.author_id = 6677)
                  )
                 order by t.title_title"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()

        if num:
                PrintTableColumns(('Count', 'Title','Ignore'))
                bgcolor = 1
                count = 1
                while record:
                        cleanup_id = record[0][0]
                        title_id = record[0][1]
                        title_title = record[0][2]
                        PrintTitleRecord(title_id, title_title, bgcolor, count, cleanup_id, 2)
                        bgcolor = bgcolor ^ 1
                        count += 1
                        record = result.fetch_row()
                print '</table><p>'
        else:
                print "<h2>No VT-alternate name mismatches found</h2>"

def function3():
        nonModeratorMessage()

        query = """select c.cleanup_id, c.record_id, t1.title_title, t1.title_ttype 
                from cleanup c, titles t1 where 
                not exists (select 1 from pub_content p where t1.title_id=p.title_id) 
                and not exists (select 1 from titles t2 where t1.title_id=t2.title_parent) 
                and c.report_type=3
                and c.record_id=t1.title_id 
                and c.resolved IS NULL
                order by t1.title_ttype, t1.title_title"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if not num:
                print "<h2>No eligible titles without publications.</h2>"
                return

        record = result.fetch_row()
        titles = {}
        while record:
                cleanup_id = record[0][0]
                title_id = record[0][1]
                title_title = record[0][2]
                title_type = record[0][3]
                if title_type not in titles:
                        titles[title_type] = []
                titles[title_type].append((cleanup_id, title_id, title_title))
                record = result.fetch_row()

        for title_type in titles.keys():
                if not titles[title_type]:
                        print "<h3>No %s titles without publications.</h3>" % title_type
                        continue
                PrintTableColumns(('', '%s titles' % title_type, 'Ignore'))
                bgcolor = 1
                count = 1
                for title in titles[title_type]:
                        cleanup_id = title[0]
                        title_id = title[1]
                        title_title = title[2]
                        PrintTitleRecord(title_id, title_title, bgcolor, count, cleanup_id, 3)
                        bgcolor ^= 1
                        count += 1
                print '</table><p>'

def function5():
        query = """select cleanup.record_id, notes.note_id,
                LENGTH(notes.note_note) - LENGTH(REPLACE(notes.note_note, '<', '')) openquote, 
                LENGTH(notes.note_note) - LENGTH(REPLACE(notes.note_note, '>', '')) closequote 
                from cleanup, notes where cleanup.record_id=notes.note_id
                and cleanup.report_type=5 having openquote != closequote"""
        MismatchesInNotes(query, 'Mismatched Angle Brackets')

def MismatchesInNotes(query, header):
        db.query(query)
        result = db.store_result()
        num = result.num_rows()
        if not num:
                print '<h2>No %s in Notes/Synopses</h2>' % header
                return

        record = result.fetch_row()
        note_ids = []
        while record:
                note_id = str(record[0][0])
                if not note_ids:
                        note_ids = note_id
                else:
                        note_ids += ",%s" % note_id
                record = result.fetch_row()

        OneType('pub_id', 'pub_title', 'pubs', 'Publications', 'pl', 'note_id', 'Notes', note_ids, header)
        OneType('title_id', 'title_title', 'titles', 'Title Notes', 'title', 'note_id', 'Notes', note_ids, header)
        OneType('title_id', 'title_title', 'titles', 'Title Synopses', 'title', 'title_synopsis', 'Synopses', note_ids, header)
        OneType('series_id', 'series_title', 'series', 'Series', 'pe', 'series_note_id', 'Notes', note_ids, header)
        OneType('publisher_id', 'publisher_name', 'publishers', 'Publishers', 'publisher', 'note_id', 'Notes', note_ids, header)
        OneType('pub_series_id', 'pub_series_name', 'pub_series', 'Publication Series', 'pubseries', 'pub_series_note_id', 'Notes', note_ids, header)
        OneType('award_id', 'award_title', 'awards', 'Awards', 'award_details', 'award_note_id', 'Notes', note_ids, header)
        OneType('award_type_id', 'award_type_short_name', 'award_types', 'Award Types', 'awardtype', 'award_type_note_id', 'Notes', note_ids, header)
        OneType('award_cat_id', 'award_cat_name', 'award_cats', 'Award Categories', 'award_category', 'award_cat_note_id', 'Notes', note_ids, header)

def OneType(record_id, record_title, table, record_name, cgi_script, note_id, term, note_ids, header):
        query = "select %s, %s from %s where %s in (%s) order by %s" % (record_id, record_title, table, note_id, note_ids, record_title)
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                PrintTableColumns(('', record_name))
                bgcolor = 1
                count = 1
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('%s.cgi' % cgi_script, record[0][0], record[0][1])
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h3>No %s with %s in %s</h3>' % (record_name, header, term)
        print '<p>'

def function6():
        query = """select a.author_id, a.author_canonical, a.author_lastname, a.author_language
                from cleanup c, authors a
                where (a.author_lastname like '%&#%'
                or not hex(a.author_lastname) regexp '^([0-7][0-9A-F])*$')
                and c.record_id = a.author_id
                and c.report_type = 6
                order by a.author_lastname"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Directory Entry', 'Author', 'Working Language'))
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        author_id = record[0][0]
                        author_canonical = record[0][1]
                        author_lastname = record[0][2]
                        author_language = record[0][3]
                        if not author_language:
                                author_language = 0
                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % author_lastname
                        print '<td>%s</td>' % ISFDBLink('ea.cgi', author_id, author_canonical)
                        print '<td>%s</td>' % LANGUAGES[author_language]
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No invalid directory names found</h2>'

def function7():
        suffixes = []
        for suffix in SESSION.recognized_suffixes:
                if suffix.count('.') < 2:
                        continue
                period_letter = 0
                for fragment in suffix.split('.'):
                        if not fragment.startswith(' '):
                                period_letter = 1
                                break
                if period_letter:
                        suffixes.append(suffix)

        cleanup.note = """This report identifies author names with:
                <ul>
                <li>Double spaces, leading spaces or trailing spaces
                <li>Double quotes (should be changed to single quotes)
                <li>Names with a period before a letter except for .com, .co.uk and
                recognized suffixes which include a period
                </ul>"""
        
        cleanup.query = """select a.author_id, a.author_canonical, c.cleanup_id
                   from cleanup c, authors a
                   where c.record_id = a.author_id
                   and c.report_type = 7
                   and c.resolved IS NULL
                   and a.author_id in (
                   select author_id from authors where author_canonical like ' %'
                   or author_canonical like '% '
                   or author_canonical like '%  %'
                   or author_canonical like '%\"%'
                   or (
                   author_canonical NOT LIKE '%.com'
                   and author_canonical NOT LIKE '%.co.uk'
                   and """

        subquery = ''
        for suffix in suffixes:
                if not subquery:
                        subquery = """replace(author_canonical, ', %s', '')""" % suffix
                else:
                        subquery = """replace(%s, ', %s', '')""" % (subquery, suffix)

        cleanup.query += subquery
        cleanup.query += """ REGEXP '\\\\.[a-z]' = 1))"""

        cleanup.ignore = 1
        cleanup.none = 'No records found'
        cleanup.print_author_table()

def function8():
        query = """select t.title_id, t.title_title
                from canonical_author ca, authors a, titles t, cleanup c
                where ca.ca_status = 3
                and ca.author_id = a.author_id
                and ca.title_id = t.title_id
                and not exists
                 (SELECT 1 from canonical_author ca2, titles t
                  where ca.author_id = ca2.author_id and ca2.title_id = t.title_id
                  and t.title_ttype != 'REVIEW' and ca2.ca_status = 1)
                and c.report_type=8
                and c.record_id=t.title_id
                and c.resolved IS NULL
                order by t.title_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if not num:
                print "<h2>No records found</h2>"
                return
        record = result.fetch_row()
        bgcolor = 1
        PrintTableColumns(('Title', 'Author(s)', 'Reviewer(s)'))
        while record:
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%s</td>' % ISFDBLink('title.cgi', record[0][0], record[0][1])
                
                reviewees = SQLReviewBriefAuthorRecords(record[0][0])
                print '<td>'
                for reviewee in reviewees:
                        print ISFDBLink('ea.cgi', reviewee[0], reviewee[1])
                print '</td>'
                
                authors = SQLTitleBriefAuthorRecords(record[0][0])
                print '<td>'
                for author in authors:
                        print ISFDBLink('ea.cgi', author[0], author[1])
                print '</td>'
                print '</tr>'
                bgcolor ^= 1
                record = result.fetch_row()
        print '</table>'

def function9():
        query = """select titles.title_id, titles.title_title
                from cleanup, titles
                where cleanup.record_id=titles.title_id 
                and titles.series_id IS NOT NULL
                and titles.series_id !=0
                and titles.title_parent !=0"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title',))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function10():
        query = """select a.author_id, a.author_canonical 
                from cleanup, authors a where a.author_id=cleanup.record_id and cleanup.report_type=10 
                and exists (select 1 from canonical_author c, titles t where a.author_id=c.author_id 
                and c.ca_status=1 and c.title_id=t.title_id and t.title_parent=0) 
                order by a.author_lastname"""
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No alternate names with canonical titles found</h2>'
                return

        # Print table headers
        PrintTableColumns(('Alternate Name', 'Count'))
        record = result.fetch_row()
        bgcolor = 1
        while record:
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print "<td>%s</td>" % ISFDBLink("ea.cgi", record[0][0], record[0][1])
                # Retrieve the number of canonical titles for this alternate name
                query2 = """select count(t.title_id) from canonical_author c, titles t
                        where c.author_id=%d and c.ca_status=1 and c.title_id=t.title_id
                        and t.title_parent=0""" % int(record[0][0])
                db.query(query2)
                result2 = db.store_result()
                record2 = result2.fetch_row()
                print "<td>%s</td>" % record2[0][0]
                print "</tr>"
                bgcolor ^= 1
                record = result.fetch_row()
        print "</table>"

def function11():
        # Ignore the following authors: unknown, Anonymous, various, uncredited, The Readers, The Editors
        query = """select c.author_id, a.author_canonical, count(c.author_id)
                from canonical_author as c, authors as a, cleanup 
                where c.author_id=a.author_id
                and a.author_language IS NULL 
                and cleanup.report_type=11
                and cleanup.record_id=a.author_id 
                group by c.author_id
                order by count(c.author_id) desc"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num:
                PrintTableColumns(('', 'Author', '# of Titles'))
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('ea.cgi', record[0][0], record[0][1])
                        print '<td>%s</td>' % record[0][2]
                        print '</tr>'
                        record = result.fetch_row()
                        bgcolor ^= 1
                        count += 1
                print '</table>'
        else:
                print '<h2>No authors without a defined language found</h2>'

def function12():
        query = """select titles.* from titles, cleanup
                where titles.title_ttype = 'EDITOR'
                and titles.series_id IS NULL 
                and titles.title_parent = 0
                and titles.title_id=cleanup.record_id
                and cleanup.report_type=12"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                PrintTableColumns(('Year', 'Title', 'Editors'))
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%s</td>' % record[0][TITLE_YEAR][:4]
                        print '<td>%s</td>' % ISFDBLink('title.cgi', record[0][TITLE_PUBID], record[0][TITLE_TITLE])
                        authors = SQLTitleBriefAuthorRecords(record[0][TITLE_PUBID])
                        print '<td>'
                        for author in authors:
                                print ISFDBLink('ea.cgi', author[0], author[1])
                        print '</td>'
                        print '</tr>'
                        bgcolor ^= 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No records found</h2>'

def function13():
        query = """select t.* from titles as t, cleanup where t.title_ttype = 'EDITOR' 
                and t.series_id IS NOT NULL and t.title_parent != 0 
                and t.title_id=cleanup.record_id and cleanup.report_type=13"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                PrintTableColumns(('Year', 'Title', 'Editors'))
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print "<td>%s</td>" % record[0][TITLE_YEAR][:4]
                        print '<td>%s</td>' % ISFDBLink('title.cgi', record[0][TITLE_PUBID], record[0][TITLE_TITLE])

                        authors = SQLTitleBriefAuthorRecords(record[0][TITLE_PUBID])
                        print "<td>"
                        for author in authors:
                                print ISFDBLink('ea.cgi', author[0], author[1])
                        print "</td>"

                        print "</tr>"
                        bgcolor ^= 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function14():
        query = """select pubs.pub_id, pubs.pub_title
                from pubs, cleanup
                where pubs.pub_id = cleanup.record_id
                and cleanup.report_type=14"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication',))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function15():
        query =  """select p.pub_id, p.pub_title
                from pubs p, cleanup, titles t, pub_content pc
                where p.pub_id = cleanup.record_id
                and cleanup.report_type=15
                and pc.title_id = t.title_id
                and pc.pub_id = p.pub_id
                and t.title_ttype = 'EDITOR'
                group by pc.pub_id, p.pub_title
                HAVING COUNT(*) > 1
                order by p.pub_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication',))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Publications with Extra EDITOR Records found</h2>"

def function16():
        query = """select s1.series_id, s1.series_title from series s1, cleanup 
                where s1.series_id=cleanup.record_id and cleanup.report_type=16 and not exists 
                (select 1 from titles t where t.series_id = s1.series_id) and not exists 
                (select 1 from series s2 where s2.series_parent = s1.series_id)"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Series Name',))
                while record:
                        series_id = record[0][0]
                        series_name = record[0][1]
                        PrintSeriesRecord(series_id, series_name, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No records found</h2>'

def function17():
        query = """select titles.series_id, titles.title_seriesnum, titles.title_seriesnum_2, count(*) cnt 
                from titles, cleanup where series_id IS NOT NULL and title_seriesnum IS NOT NULL 
                and titles.series_id = cleanup.record_id and cleanup.report_type=17 
                group by series_id, title_seriesnum, title_seriesnum_2 having cnt >1"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Series', 'Series Number'))
                while record:
                        series_id = record[0][0]
                        series_number = record[0][1]
                        series_number_2 = record[0][2]
                        series_data = SQLget1Series(series_id)
                        series_name = series_data[SERIES_NAME]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('pe.cgi', series_id, series_name)
                        display_series_num = str(series_number)
                        if series_number_2 is not None:
                                display_series_num += '.%s' % series_number_2
                        print '<td>%s</td>' % (display_series_num)
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No series with duplicate series numbers found</h2>"

def function18():
        query = """select t.title_id, t.title_title from titles t, cleanup c 
                where t.title_title like '%. . .%' and c.report_type=18 
                and t.title_id=c.record_id order by t.title_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()
        if not num:
                print "<h2>No titles with bad ellipses found.</h2>"
                return
        PrintTableColumns(('', 'Title'))
        bgcolor = 1
        count = 1
        record = result.fetch_row()
        while record:
                title_id = record[0][0]
                title_title = record[0][1]
                PrintTitleRecord(title_id, title_title, bgcolor, count)
                record = result.fetch_row()
                bgcolor ^= 1
                count += 1
        print "</table>"

def function19():
        query = """select ca.title_id, t.title_title from 
                titles t, canonical_author ca, authors a, cleanup 
                where t.title_ttype = 'INTERVIEW' and ca.title_id = t.title_id 
                and ca.author_id = a.author_id and ca.ca_status = 2 
                and a.author_canonical != 'uncredited' and exists 
                (select 1 from pseudonyms p where a.author_id = p.pseudonym) 
                and t.title_id=cleanup.record_id and cleanup.report_type=19"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title',))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function20():
        query = """select t.title_id, t.title_title from titles t, titles tp, cleanup 
                where tp.title_id = t.title_parent and tp.title_parent != 0 
                and t.title_id=cleanup.record_id and cleanup.report_type=20"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title',))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function21():
        query = """select t.title_id, t.title_title from titles t, cleanup where t.title_parent<>0 
                and not exists (select 1 from titles pt where t.title_parent=pt.title_id) 
                and t.title_id=cleanup.record_id and cleanup.report_type=21"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title',))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function22():
        query = """select t.title_id,t.title_title from titles t, cleanup where 
                t.title_ttype='SERIAL' and title_parent=0 and 
                t.title_id=cleanup.record_id and cleanup.report_type=22 
                order by t.title_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num:
                PrintTableColumns(('', 'Serial'))
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        record = result.fetch_row()
                        bgcolor ^= 1
                        count += 1
                print "</table>"
        else:
                print "<h2>No SERIALs without a Parent Title found</h2>"

def function23():
        from awardClass import awards
        records = []
        query = """select awards.*
                from awards, title_awards, cleanup where 
                awards.award_id = title_awards.award_id
                and not exists
                        (select 1 from titles
                        where titles.title_id = title_awards.title_id) 
                and cleanup.record_id = awards.award_id
                and cleanup.report_type = 23 
                order by award_type_id, award_year, award_level"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()
        if not num:
                print "<h2>No records found</h2>"
                return

        PrintTableColumns(('Award Title', 'Award Name', 'Award Year', 'Award Category', 'Award Level'))
        record = result.fetch_row()
        bgcolor = 1
        while record:
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                award = awards(db)
                award.load(record[0][AWARD_ID])

                print '<td>%s</td>' % ISFDBLink('award_details.cgi', award.award_id, award.award_title)
                print '<td>%s</td>' % ISFDBLink('awardtype.cgi', award.award_type_id, award.award_type_name)
                print '<td>%s</td>' % ISFDBLink('ay.cgi', '%s+%s' % (award.award_type_id, award.award_year[:4]), award.award_year[:4])
                print '<td>%s</td>' % award.award_cat_name
                print '<td>%s</td>' % award.award_displayed_level
                print '</tr>'
                bgcolor ^= 1
                record = result.fetch_row()
        print "</table>"

def function24():
        from awardClass import awards
        records = []
        query = """select cleanup.cleanup_id, a.award_id
                from awards a, cleanup
                where a.award_id = cleanup.record_id
                and cleanup.report_type = 24
                and cleanup.resolved IS NULL 
                order by a.award_type_id, a.award_year, a.award_level"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()
        if not result.num_rows():
                print "<h2>No records found</h2>"
                return

        PrintTableColumns(('Award Title', 'Award Name', 'Award Year', 'Award Category', 'Award Level', ''))
        record = result.fetch_row()
        bgcolor = 1
        while record:
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                award = awards(db)
                award.load(record[0][1])

                print '<td>%s</td>' % ISFDBLink('award_details.cgi', award.award_id, award.award_title)
                print '<td>%s</td>' % ISFDBLink('awardtype.cgi', award.award_type_id, award.award_type_short_name)
                print '<td>%s</td>' % ISFDBLink('ay.cgi', '%s+%s' % (award.award_type_id, award.award_year[:4]), award.award_year[:4])
                print '<td>%s</td>' % ISFDBLink('award_category.cgi', '%s+0' % award.award_cat_id, award.award_cat_name)
                print '<td>%s</td>' % award.award_displayed_level
                print '<td>%s</td>' % ISFDBLinkNoName('mod/resolve_cleanup.cgi', '%s+1+24' % record[0][0], 'Ignore this award')
                print '</tr>'
                bgcolor ^= 1
                record = result.fetch_row()
        print "</table>"

def function25():
        query = """select * from award_types, cleanup
                where NOT EXISTS 
                (select 1 from awards
                where awards.award_type_id=award_types.award_type_id) 
                and cleanup.record_id=award_types.award_type_id
                and cleanup.report_type=25"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num:
                PrintTableColumns(('Award Type',))
                record = result.fetch_row()
                bgcolor = 1
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        award_type_id = record[0][AWARD_TYPE_ID]
                        award_type_name = record[0][AWARD_TYPE_NAME]
                        print '<td>%s</td>' % ISFDBLink('awardtype.cgi', award_type_id, award_type_name)
                        print '</tr>'
                        record = result.fetch_row()
                        bgcolor ^= 1

                print '</table>'
        else:
                print '<h3>No empty Award Types found</h3>'

def function26():
        query = """select award_cats.*
                from award_cats, cleanup
                where NOT EXISTS 
                (select 1 from awards
                where awards.award_cat_id=award_cats.award_cat_id) 
                and cleanup.record_id=award_cats.award_cat_id
                and cleanup.report_type=26"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num:
                PrintTableColumns(('Award Category',))
                record = result.fetch_row()
                bgcolor = 1
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        award_cat_id = record[0][AWARD_CAT_ID]
                        award_cat_name = record[0][AWARD_CAT_NAME]
                        print '<td>%s</td>' % ISFDBLink('award_category.cgi', award_cat_id, award_cat_name)
                        print '</tr>'
                        record = result.fetch_row()
                        bgcolor ^= 1
                print '</table>'
        else:
                print '<h3>No empty Award Categories found</h3>'

def function27():
        query = """select s.series_id, s.series_title from series s, cleanup c where 
                c.record_id=s.series_id and c.report_type=27 and exists 
                (select 1 from titles t where t.title_ttype='CHAPBOOK'
                and t.series_id = s.series_id) 
                order by s.series_title"""
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print "<h2>No records found</h2>"
                return

        record = result.fetch_row()
        bgcolor = 1
        count = 1
        PrintTableColumns(('', 'Series',))
        while record:
                series_id = record[0][0]
                series_name = record[0][1]
                PrintSeriesRecord(series_id, series_name, bgcolor, count)
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print "</table>"

def function28():
        query = """select t.title_id, t.title_title from titles t, cleanup c 
                where t.title_ttype='CHAPBOOK' and t.title_synopsis !=0 
                and c.record_id=t.title_id and c.report_type=28 order by t.title_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title',))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function29():
        query = """select pub_id, pub_title from pubs, cleanup 
                   where pub_ctype='CHAPBOOK' and NOT EXISTS 
                   (select 1 from pub_content,titles where pubs.pub_id=pub_content.pub_id 
                   and pub_content.title_id=titles.title_id and (titles.title_ttype='SHORTFICTION' 
                   or titles.title_ttype='POEM' or titles.title_ttype='SERIAL')) 
                   and pubs.pub_id=cleanup.record_id and cleanup.report_type=29 
                   order by pub_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                PrintTableColumns(('', 'Publication Title'))
                bgcolor = 1
                count = 1
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function30():
        query = """select t1.title_id, t1.title_title from titles t1, titles t2, cleanup c where 
                t1.title_ttype='CHAPBOOK' and t2.title_parent=t1.title_id and t2.title_ttype!='CHAPBOOK' 
                and (t1.title_id=c.record_id or t2.title_id=c.record_id) and c.report_type=30 
                UNION select t1.title_id,t1.title_title from titles t1, titles t2, cleanup c where 
                t1.title_ttype!='CHAPBOOK' and t2.title_parent=t1.title_id and t2.title_ttype='CHAPBOOK' 
                and (t1.title_id=c.record_id or t2.title_id=c.record_id) and c.report_type=30"""
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print "<h2>No records found</h2>"
                return

        record = result.fetch_row()
        bgcolor = 1
        count = 1
        PrintTableColumns(('', 'Title',))
        while record:
                title_id = record[0][0]
                title_title = record[0][1]
                PrintTitleRecord(title_id, title_title, bgcolor, count)
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print "</table>"

def function31():
        query = """select c.cleanup_id, p.pub_id, p.pub_isbn, p.pub_year from pubs p, cleanup c 
                where ((p.pub_isbn like '97%' and length(replace(p.pub_isbn,'-',''))=13 
                and p.pub_year <'2005-00-00' and p.pub_year !='0000-00-00') or 
                (p.pub_isbn not like '#%' and length(replace(p.pub_isbn,'-',''))=10 
                and p.pub_year>'2008-00-00' and p.pub_year !='8888-00-00' and 
                p.pub_year !='9999-00-00')) and p.pub_id=c.record_id and 
                c.report_type=31 and c.resolved IS NULL order by pub_year, pub_isbn"""
                
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('Count', 'Date', 'ISBN', ''))
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % record[0][3]
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', record[0][1], record[0][2])
                        print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                        '%s+1+31' % record[0][0],
                                                        'Ignore this ISBN')
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No records found</h2>'

def function32():
        query = """select p1.pub_id, p1.pub_tag, p1.pub_title from pubs p1, 
                (select pub_tag, count(*) from pubs, cleanup c where pubs.pub_id=c.record_id 
                and c.report_type=32 group by pub_tag having count(*) > 1) p2 
                where p1.pub_tag = p2.pub_tag order BY 2,1,3"""
        
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                PrintTableColumns(('Publication Title', 'Publication Tag'))
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%s</td>' % ISFDBLink('pl.cgi', record[0][0], record[0][2])
                        print '<td>%s</td>' % record[0][1]
                        print '</tr>'
                        bgcolor ^= 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function33():
        query = """select p.pub_id, p.pub_title as order_title, pa.author_id, a.author_canonical
                from pub_authors pa, pubs p, pub_content pc, titles t, authors a, cleanup 
                where pa.pub_id = p.pub_id 
                and pc.title_id = t.title_id 
                and pc.pub_id = p.pub_id 
                and pa.author_id = a.author_id 
                and p.pub_ctype in ('ANTHOLOGY','NOVEL','COLLECTION','NONFICTION','OMNIBUS','CHAPBOOK') 
                and t.title_ttype in ('ANTHOLOGY','NOVEL','COLLECTION','OMNIBUS','NONFICTION','CHAPBOOK') 
                and t.title_ttype = p.pub_ctype 
                and not exists
                  (select 1 from canonical_author ca
                  where ca.title_id = t.title_id and pa.author_id = ca.author_id) 
                and p.pub_id=cleanup.record_id and cleanup.report_type=33
                UNION
                select p.pub_id, p.pub_title as order_title, pa.author_id, a.author_canonical
                from pub_authors pa, pubs p, pub_content pc, titles t, authors a, cleanup 
                where pa.pub_id = p.pub_id 
                and pc.title_id = t.title_id 
                and pc.pub_id = p.pub_id 
                and pa.author_id = a.author_id 
                and p.pub_ctype in ('FANZINE','MAGAZINE')
                and t.title_ttype = 'EDITOR'
                and t.title_language != 26
                and not exists
                  (select 1 from canonical_author ca
                  where ca.title_id = t.title_id and pa.author_id = ca.author_id) 
                and p.pub_id=cleanup.record_id and cleanup.report_type=33
                order by order_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title', 'Author'))
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', record[0][0], record[0][1])
                        print '<td>%s</td>' % ISFDBLink('ea.cgi', record[0][2], record[0][3])
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No records found</h2>'

def function34():
        query =  """select pub_id, pub_title from pubs, cleanup
                where not exists
                (select 1 from pub_content pc, titles t
                where pubs.pub_id = pc.pub_id
                and pc.title_id = t.title_id
                and t.title_ttype != 'COVERART')
                and pubs.pub_id=cleanup.record_id
                and cleanup.report_type=34
                order by pubs.pub_title"""
                
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication Title',))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function35():
        formats = "'" + "','".join(SESSION.db.formats) + "'"
        query = """select pubs.pub_ptype, pubs.pub_id, pubs.pub_title from pubs, cleanup where 
                pubs.pub_ptype not in (%s) and pubs.pub_ptype IS NOT NULL and pubs.pub_ptype !='' 
                and pubs.pub_id=cleanup.record_id and cleanup.report_type=35 
                order by pubs.pub_ptype, pubs.pub_title""" % (formats)

        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No matching records</h2>'
                return
        
        PrintTableColumns(('Format', 'Publication'))
        bgcolor = 1
        record = result.fetch_row()
        while record:
                format = record[0][0]
                pub_id = record[0][1]
                pub_title = record[0][2]
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%s</td>' % format
                print '<td>'
                print ISFDBLink('pl.cgi', pub_id, pub_title)
                print '</td>'
                print '</tr>'
                bgcolor ^= 1
                record = result.fetch_row()
        print '</table>'

def function36():
        query = """select pub_id, pub_title, pub_frontimage
                from pubs, cleanup 
                where pubs.pub_frontimage != ''
                and pubs.pub_frontimage is not null 
                and pubs.pub_id = cleanup.record_id
                and cleanup.report_type = 36"""
        domains = SQLLoadRecognizedDomains()
        for domain in domains:
                # Skip domains that are "recognized", but we don't have permission to link to
                if not domain[DOMAIN_LINKING_ALLOWED]:
                        continue
                query += " and SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(pub_frontimage,'//',2),'//',-1),'/',1) not like '%%%s'" % domain[DOMAIN_NAME]
        # Check for URL segments which must be present in the URL
        subquery = ''
        for domain in domains:
                if not domain[DOMAIN_REQUIRED_SEGMENT]:
                        continue
                if subquery:
                        subquery += ' or'
                subquery += """ (SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(pub_frontimage,'//',2),'//',-1),'/',1)
                                  like '%%%s' and pub_frontimage not like '%%%s%%')""" % (domain[DOMAIN_NAME], domain[DOMAIN_REQUIRED_SEGMENT])
        query += """ UNION select pub_id, pub_title, pub_frontimage
                from pubs, cleanup
                where pubs.pub_frontimage != ''
                and pubs.pub_frontimage is not null
                and pubs.pub_id = cleanup.record_id
                and cleanup.report_type = 36
                and SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(pub_frontimage,'//',2),'//',-1),'/',1) not like '%%sf-encyclopedia.uk'
                and SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(pub_frontimage,'//',2),'//',-1),'/',1) not like '%%sf-encyclopedia.com'
                and (%s)""" % subquery
        query += ' order by pub_title'
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        if not record:
                print '<h2>No records found</h2>'
                return

        bgcolor = 1
        PrintTableColumns(('Publication', 'URL'))
        while record:
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%s</td>' % ISFDBLink('pl.cgi', record[0][0], record[0][1])
                print '<td><a href="%s">%s</a></td>' % (ISFDBText(record[0][2]), ISFDBText(record[0][2]))
                print '</tr>'
                bgcolor ^= 1
                record = result.fetch_row()
        print '</table>'

def function37():
        nonModeratorMessage()
        query = """select p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, cleanup c
                where p.pub_ctype='OMNIBUS'
                and p.pub_id=c.record_id
                and c.report_type=37
                and c.resolved is NULL
                and NOT EXISTS 
                (select 1 from pub_content pc, titles t
                 where p.pub_id=pc.pub_id 
                 and pc.title_id=t.title_id
                 and t.title_ttype in ('NOVEL', 'COLLECTION', 'ANTHOLOGY', 'NONFICTION')
                ) 
                order by p.pub_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                PrintTableColumns(('', 'Publication Title', 'Ignore'))
                bgcolor = 1
                count = 1
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count, cleanup_id, 37)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No records found</h2>'

def function38():
        query = 'select pc.pub_id, pc.title_id, count(*) as cnt \
                from pub_content pc, cleanup c \
                where pc.pub_id=c.record_id and c.report_type=38 \
                group by pc.pub_id, pc.title_id having cnt>1'

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        pubs = {}
        titles = {}
        pub_data = {}
        title_data = {}
        record = result.fetch_row()
        while record:
                pub_id = record[0][0]
                # Skip records where pub_id is NULL -- they will have to be cleaned up manually
                if not pub_id:
                        record = result.fetch_row()
                        continue
                title_id = record[0][1]
                count = record[0][2]
                pub_data[pub_id] = SQLGetPubById(pub_id)
                title_data[title_id] = SQLloadTitle(title_id)
                if pub_id not in pubs:
                        pubs[pub_id] = [(title_id, count), ]
                else:
                        pubs[pub_id].append((title_id, count), )
                record = result.fetch_row()

        if not pubs:
                print "<h2>No publications with duplicate titles found</h2>"
                return
        bgcolor = 1
        PrintTableColumns(('Publication', 'Duplicate Titles (count)'))
        for pub_id in pubs:
                titles = pubs[pub_id]
                pub_title = pub_data[pub_id][PUB_TITLE]
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                print '<td>'
                first = 1
                for title in titles:
                        title_id = title[0]
                        count = title[1]
                        title_title = title_data[title_id][TITLE_TITLE]
                        if first:
                                first = 0
                        else:
                                print '<br>'
                        print '%s (%s)' % (ISFDBLink('title.cgi', title_id, title_title), count)
                print '</td>'
                print '</tr>'
                bgcolor ^= 1
        print '</table>'

def function39():
        query = """select p.pub_id, p.pub_title from pubs p, cleanup c 
                where p.pub_title like '%. . .%' and c.report_type=39 
                and p.pub_id=c.record_id order by p.pub_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()
        if not num:
                print "<h2>No publications with bad ellipses found.</h2>"
                return
        PrintTableColumns(('', 'Publication'))
        bgcolor = 1
        count = 1
        record = result.fetch_row()
        while record:
                pub_id = record[0][0]
                pub_title = record[0][1]
                PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                record = result.fetch_row()
                bgcolor ^= 1
                count += 1
        print "</table>"

def function40():
        query = """select t.* from titles t, cleanup c where title_ttype='REVIEW' and not exists 
                (select 1 from canonical_author ca where ca.title_id=t.title_id and ca.ca_status=3) 
                and t.title_id=c.record_id and c.report_type=40 order by t.title_title"""

        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No Reviews without Reviewed Authors</h2>'
                return

        # Print table headers
        PrintTableColumns(('', 'Review',))
        record = result.fetch_row()
        bgcolor = 1
        count = 1
        while record:
                title_id = record[0][0]
                title_title = record[0][1]
                PrintTitleRecord(title_id, title_title, bgcolor, count)
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print "</table>"

def function41():
        query = """select t1.title_id, t1.title_title, c.cleanup_id from titles t1, cleanup c
                where title_ttype='REVIEW' and not exists 
                (select 1 from title_relationships tr where tr.review_id=t1.title_id) 
                and not exists (select 1 from titles t2 where t2.title_parent=t1.title_id) 
                and t1.title_id=c.record_id and c.report_type=41
                order by t1.title_title"""

        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No Reviews not Linked to Titles</h2>'
                return

        # Print table headers
        PrintTableColumns(('', 'Review'))
        record = result.fetch_row()
        bgcolor = 1
        count = 1
        while record:
                title_id = record[0][0]
                title_title = record[0][1]
                PrintTitleRecord(title_id, title_title, bgcolor, count)
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print '</table>'

def function42():
        print '<h3>This report finds reviews of CHAPBOOK, COVERART, INTERIORART, INTERVIEW and REVIEW records.</h3>'

        query = """select c.cleanup_id, t1.title_id, t1.title_title, t2.title_ttype 
                from titles t1, titles t2, cleanup c, title_relationships tr 
                where t1.title_ttype='REVIEW'
                and t1.title_id=tr.review_id 
                and t2.title_id=tr.title_id
                and t2.title_ttype in ('CHAPBOOK', 'COVERART', 'INTERIORART', 'INTERVIEW', 'REVIEW') 
                and c.report_type=42
                and c.record_id=t1.title_id 
                and c.resolved IS NULL
                order by t2.title_ttype, t2.title_title"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if not num:
                print '<h2>No Reviews of Uncommon Title Types.</h2>'
                return

        record = result.fetch_row()
        titles = {}
        while record:
                cleanup_id = record[0][0]
                title_id = record[0][1]
                title_title = record[0][2]
                title_type = record[0][3]
                if title_type not in titles:
                        titles[title_type] = []
                titles[title_type].append((cleanup_id, title_id, title_title))
                record = result.fetch_row()

        for title_type in titles.keys():
                if not titles[title_type]:
                        print '<h3>No reviews of %ss.</h3>' % title_type
                        continue
                PrintTableColumns(('', 'Reviews of %s records' % title_type, ''))
                color = 0
                count = 1
                for title in titles[title_type]:
                        if color:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        cleanup_id = title[0]
                        title_id = title[1]
                        title_title = title[2]
                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title)
                        print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%s+1+42' % cleanup_id, 'Ignore this title')
                        print '</tr>'
                        color = color ^ 1
                        count += 1
                print '</table><p>'

def function43():
        query = """select p1.publisher_name from publishers p1, publishers p2, cleanup c where 
                p1.publisher_id!=p2.publisher_id and p1.publisher_name=p2.publisher_name 
                and p1.publisher_id=c.record_id and c.report_type=43 order by p1.publisher_name"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                while record:
                        PrintTableColumns(('', 'Publisher', ))
                        publisher_name = record[0][0]
                        query2 = "select publisher_id from publishers where publisher_name = '%s'" % db.escape_string(publisher_name)
                        db.query(query2)
                        result2 = db.store_result()
                        record2 = result2.fetch_row()
                        bgcolor = 1
                        count = 1
                        while record2:
                                publisher_id = record2[0][0]
                                PrintPublisherRecord(publisher_id, publisher_name, bgcolor, count)
                                bgcolor ^= 1
                                count += 1
                                record2 = result2.fetch_row()
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function44():
        query = """select c.record_id, p1.publisher_name,
                c.record_id_2, p2.publisher_name, c.cleanup_id
                from cleanup c, publishers p1, publishers p2
                where c.report_type=44 and c.resolved IS NULL
                and c.record_id = p1.publisher_id
                and c.record_id_2 = p2.publisher_id
                order by p1.publisher_name"""
        db.query(query)
        result = db.store_result()

        if not result.num_rows():
                print '<h2>No similar publisher records found</h2>'
                return

        PrintTableColumns(('', 'Publisher 1', 'Publisher 2', 'Ignore'))
        bgcolor = 1
        count = 1
        record = result.fetch_row()
        while record:
                publisher_id_1 = record[0][0]
                publisher_name_1 = record[0][1]
                publisher_id_2 = record[0][2]
                publisher_name_2 = record[0][3]
                cleanup_id = record[0][4]
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'
                print '<td>%d</td>' % count
                print '<td>%s</td>' % ISFDBLink('publisher.cgi', publisher_id_1, publisher_name_1)
                print '<td>%s</td>' % ISFDBLink('publisher.cgi', publisher_id_2, publisher_name_2)
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%d+1+44' % int(cleanup_id), 'Ignore')
                print '</tr>'
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print '</table>'

def function45():
        query = """select v.title_id, v.title_title, v.title_ttype, p.title_ttype
                from titles v, titles p, cleanup c
                where v.title_parent > 0 
                and v.title_parent=p.title_id
                and v.title_ttype!=p.title_ttype 
                and not (v.title_ttype='SERIAL' and p.title_ttype in ('NOVEL', 'SHORTFICTION', 'COLLECTION')) 
                and not (v.title_ttype='INTERIORART' and p.title_ttype='COVERART')
                and not (v.title_ttype='COVERART' and p.title_ttype='INTERIORART')
                and v.title_id=c.record_id
                and c.report_type=45
                order by v.title_title"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if not num:
                print "<h2>No variant title type mismatches</h2>"
                return

        record = result.fetch_row()
        titles = {}
        while record:
                variant_type = record[0][2]
                if variant_type not in titles:
                        titles[variant_type] = []
                titles[variant_type].append(record[0])
                record = result.fetch_row()

        for variant_type in titles.keys():
                if not titles[variant_type]:
                        print "<h3>No %s title type mismatches</h3>" % variant_type
                        continue
                PrintTableColumns(('', '%s titles' % variant_type, 'Parent type'))
                color = 0
                count = 1
                for title in titles[variant_type]:
                        if color:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        variant_id = title[0]
                        variant_title = title[1]
                        parent_type = title[3]
                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('title.cgi', variant_id, variant_title)
                        print '<td>%s</td>' % parent_type
                        print '</tr>'
                        color = color ^ 1
                        count += 1
                print '</table><p>'

def function46():
        query = """select DISTINCT t.*
                from titles t, pubs p, pub_content pc, cleanup c 
                where t.title_ttype='EDITOR'
                and t.title_id=pc.title_id
                and p.pub_id=pc.pub_id
                and p.pub_ctype not in ('MAGAZINE','FANZINE') 
                and t.title_id=c.record_id
                and c.report_type=46"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                PrintTableColumns(('Year', 'Title', 'Editors'))
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%s</td>' % record[0][TITLE_YEAR][:4]
                        print '<td>%s</td>' % ISFDBLink('title.cgi', record[0][TITLE_PUBID], record[0][TITLE_TITLE])

                        authors = SQLTitleBriefAuthorRecords(record[0][TITLE_PUBID])
                        print '<td>'
                        for author in authors:
                                print ISFDBLink('ea.cgi', author[0], author[1])
                        print '</td>'
                        print '</tr>'
                        bgcolor ^= 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No records found</h2>'

def function47():
        query = """select distinct t.title_id, t.title_title, t.title_ttype 
                from titles t, pub_content pc, pubs p, cleanup c
                where pc.title_id = t.title_id
                and pc.pub_id = p.pub_id
                and p.pub_year != '0000-00-00'
                and p.pub_year != '8888-00-00'
                and t.title_copyright != '0000-00-00'
                and t.title_copyright != '0000-00-00'
                and
                (
                        YEAR(t.title_copyright) > YEAR(p.pub_year)
                or
                        (
                                YEAR(p.pub_year) = YEAR(t.title_copyright)
                                and MONTH(p.pub_year) != '00'
                                and MONTH(t.title_copyright) > MONTH(p.pub_year)
                        )
                or
                        (
                                YEAR(p.pub_year) = YEAR(t.title_copyright)
                                and MONTH(p.pub_year) = MONTH(t.title_copyright)
                                and MONTH(p.pub_year) != '00'
                                and DAY(p.pub_year) != '00'
                                and DAY(t.title_copyright) > DAY(p.pub_year)
                        )
                )
                and t.title_id = c.record_id
                and c.report_type = 47"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if not num:
                print "<h2>No Title Dates after Publication Dates.</h2>"
                return

        record = result.fetch_row()
        titles = {}
        while record:
                title_id = record[0][0]
                title_title = record[0][1]
                title_type = record[0][2]
                if title_type not in titles:
                        titles[title_type] = []
                titles[title_type].append((title_title, title_id))
                record = result.fetch_row()

        for title_type in sorted(titles.keys()):
                if not titles[title_type]:
                        print "<h3>No %s with Title Dates after Publication Dates.</h3>" % title_type
                        continue
                PrintTableColumns(('', '%s titles' % title_type))
                bgcolor = 1
                count = 1
                for title in sorted(titles[title_type]):
                        title_title = title[0]
                        title_id = title[1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        bgcolor = bgcolor ^ 1
                        count += 1
                print '</table><p>'

def function48():
        if user.moderator:
                print """<h3>If a series can't be fixed, please document the details
                        in the series' Note field before marking it "Ignored".</h3>"""

        nonModeratorMessage()
        
        # First retrieve all series IDs found by the nightly cleanup report
        query = "select record_id from cleanup where report_type=48 and resolved IS NULL"
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No Series with Numbering Gaps</h2>'
                return

        series_ids = []
        record = result.fetch_row()
        while record:
                series_ids.append(str(record[0][0]))
                record = result.fetch_row()
        # Convert the resulting list to a comma-delimited string
        series_string = ",".join(series_ids)

        # Next retrieve the series/cleanup data - the logic may not be optimal, needs to be reviewed
        query = """select tmp2.series_id, tmp2.series_title, c.cleanup_id from 
                        (select tmp.series_id, s.series_title from 
                                (select t.series_id from titles t where t.series_id IS NOT NULL 
                                and t.title_seriesnum IS NOT NULL and t.title_seriesnum!=8888 
                                and t.series_id in (%s) 
                                group by t.series_id having count(t.title_seriesnum) < 
                                (max(t.title_seriesnum)-min(t.title_seriesnum)+1) 
                                union 
                                select s.series_id from series s where not exists 
                                        (select 1 from titles t where t.series_id=s.series_id 
                                         and t.title_seriesnum=1) 
                                 and exists 
                                         (select 1 from titles t where t.series_id=s.series_id 
                                         and t.title_seriesnum>1 and t.title_seriesnum<1800) 
                                and s.series_id in (%s)) 
                        tmp, series s where tmp.series_id=s.series_id order by s.series_title) 
                tmp2, cleanup c where c.record_id=tmp2.series_id and c.report_type=48 
                order by tmp2.series_title""" % (series_string, series_string)

        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No Series with Numbering Gaps</h2>'
                return

        # Print table headers
        PrintTableColumns(('', 'Series', 'Ignore'))
        record = result.fetch_row()
        bgcolor = 1
        count = 1
        while record:
                series_id = record[0][0]
                series_name = record[0][1]
                cleanup_id = record[0][2]
                PrintSeriesRecord(series_id, series_name, bgcolor, count, cleanup_id, 48)
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print "</table>"


def function49():
        query = """select p.pub_isbn, p.pub_id, p.pub_title
                from pubs p, cleanup c
                where p.pub_isbn is not NULL
                and p.pub_isbn != ''
                and
                (
                     (
                     REPLACE(p.pub_isbn,'-','') not REGEXP '^[[:digit:]]{9}[Xx]{1}$'
                     and REPLACE(p.pub_isbn,'-','') not REGEXP '^[[:digit:]]{10}$'
                     and REPLACE(p.pub_isbn,'-','') not REGEXP '^[[:digit:]]{13}$'
                     )
                     or
                     (
                     REPLACE(p.pub_isbn,'-','') REGEXP '^[[:digit:]]{13}$'
                     and LEFT(REPLACE(p.pub_isbn,'-',''), 3) != '978'
                     and LEFT(REPLACE(p.pub_isbn,'-',''), 3) != '979'
                     )
                )
                and p.pub_id=c.record_id
                and c.report_type=49 
                order by p.pub_title"""

        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No Publications with Invalid ISBN Formats</h2>'
                return
        PrintTableColumns(('', 'ISBN', 'Publication'))
        bgcolor = 1
        count = 1
        record = result.fetch_row()
        while record:
                pub_isbn = record[0][0]
                pub_id = record[0][1]
                pub_title = record[0][2]
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%d</td>' % count
                print '<td>%s</td>' % pub_isbn
                print '<td>'
                print ISFDBLink('pl.cgi', pub_id, pub_title)
                print '</td>'
                print '</tr>'
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print '</table>'

def function50():
        query = """(select tmp.pub_id, tmp.isbn, tmp.pub_title as pub_title, tmp.cleanup_id from
                 (select p.pub_id, REPLACE(p.pub_isbn,'-','') AS isbn, p.pub_title, c.cleanup_id
                 from pubs p, cleanup c
                 where LENGTH(REPLACE(p.pub_isbn,'-',''))=10
                 and p.pub_id=c.record_id and c.report_type=50 and c.resolved IS NULL) tmp
                 where CONVERT((11-MOD( 
                 (substr(isbn,1,1)*10) 
                +(substr(isbn,2,1)*9) 
                +(substr(isbn,3,1)*8) 
                +(substr(isbn,4,1)*7) 
                +(substr(isbn,5,1)*6) 
                +(substr(isbn,6,1)*5) 
                +(substr(isbn,7,1)*4) 
                +(substr(isbn,8,1)*3) 
                +(substr(isbn,9,1)*2) 
                , 11)),CHAR) 
                 != REPLACE(REPLACE(SUBSTR(tmp.isbn,10,1),0,11),'X',10)) 
                union 
                (select tmp.pub_id, tmp.isbn, tmp.pub_title as pub_title, tmp.cleanup_id from 
                 (select p.pub_id, REPLACE(p.pub_isbn,'-','') AS isbn, p.pub_title, c.cleanup_id 
                 from pubs p, cleanup c 
                 where LENGTH(REPLACE(p.pub_isbn,'-',''))=13 
                 and p.pub_id=c.record_id and c.report_type=50 and c.resolved IS NULL) tmp 
                 where MOD(10-MOD( 
                 (substr(isbn,1,1)*1) 
                +(substr(isbn,2,1)*3) 
                +(substr(isbn,3,1)*1) 
                +(substr(isbn,4,1)*3) 
                +(substr(isbn,5,1)*1) 
                +(substr(isbn,6,1)*3) 
                +(substr(isbn,7,1)*1) 
                +(substr(isbn,8,1)*3) 
                +(substr(isbn,9,1)*1) 
                +(substr(isbn,10,1)*3) 
                +(substr(isbn,11,1)*1) 
                +(substr(isbn,12,1)*3) 
                ,10),10) 
                 != SUBSTR(isbn,13,1)) 
                 order by pub_title"""

        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No Publications with Invalid ISBN Checksums</h2>'
                return

        PrintTableColumns(('', 'ISBN', 'Publication', ''))
        record = result.fetch_row()
        bgcolor = 1
        count = 1
        while record:
                pub_id = record[0][0]
                pub_isbn = record[0][1]
                pub_title = record[0][2]
                cleanup_id = record[0][3]
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%d</td>' % count
                print '<td>%s</td>' % pub_isbn
                print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                '%s+1+50' % cleanup_id,
                                                'Ignore this pub')
                print '</tr>'
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print '</table>'

def function51():
        query = """select p.pub_id, p.pub_title, p.pub_isbn, p.pub_year, c.cleanup_id 
                from pubs p, cleanup c where p.pub_isbn!='' and p.pub_isbn IS NOT NULL 
                and p.pub_id=c.record_id and c.report_type=51 and c.resolved IS NULL"""
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No Publications with Identical ISBNs and Different Titles</h2>'
                return

        isbns = {}
        record = result.fetch_row()
        while record:
                normalized_isbn = string.replace(record[0][2],"-",'')
                if normalized_isbn not in isbns:
                        isbns[normalized_isbn] = []
                isbns[normalized_isbn].append(record[0])
                record = result.fetch_row()

        # Blank out ISBNs whose titles have been made identical since the report last ran
        for isbn in isbns:
                title_set = set()
                for pub in isbns[isbn]:
                        pub_title = pub[1]
                        title_set.add(pub_title)
                if len(title_set) == 1:
                        isbns[isbn] = ''
        
        PrintTableColumns(('#', 'ISBN', 'Publications'))
        bgcolor = 1
        count = 1
        for isbn in sorted(isbns):
                if not isbns[isbn]:
                        continue
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%d</td>' % count
                print '<td>%s</td>' % isbn
                print '<td>'
                print '<table class="review">'
                for pub in isbns[isbn]:
                        print '<tr>'
                        print '<td>'
                        print ISFDBLink('pl.cgi', pub[0], pub[1])
                        print '</td>'
                        print '<td>%s</td>' % pub[3]
                        print '<td>'
                        print ISFDBLink('mod/resolve_cleanup.cgi', '%s+1+51' % pub[4], 'Ignore this pub')
                        print '</td>'
                        print '</tr>'
                print '</table>'
                print '</td>'
                print '</tr>'
                bgcolor ^= 1
                count += 1
        print '</table>'

def function52():
        print """<h3>This report finds publication with 0 or 2+ reference titles.</h3>"""

        only_one = {'ANTHOLOGY': ['ANTHOLOGY'],
                    'COLLECTION': ['COLLECTION'],
                    'CHAPBOOK': ['CHAPBOOK'],
                    'MAGAZINE': ['EDITOR'],
                    'FANZINE': ['EDITOR'],
                    'NONFICTION': ['NONFICTION'],
                    'NOVEL': ['NOVEL'],
                    'OMNIBUS': ['OMNIBUS']
                    }

        query = ""
        for pub_type in only_one:
                if query:
                        query += " UNION "
                query += "(select p.pub_id, p.pub_ctype, p.pub_title, c.cleanup_id"
                query += " from pubs p, cleanup c where p.pub_ctype='%s'" % pub_type
                query += " and p.pub_id=c.record_id and c.report_type=52 and c.resolved is NULL"
                query += " and (select count(*) from pub_content pc, titles t"
                query += " where pc.pub_id=p.pub_id and t.title_id=pc.title_id"
                query += " and "
                subquery = ""
                for title_type in only_one[pub_type]:
                        if subquery:
                                subquery += " or "
                        subquery += "(t.title_ttype='%s')" % title_type
                query += "(" + subquery + "))!=1)"

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if not num:
                print "<h2>No Publications with 0 or 2+ Reference Titles.</h2>"
                return

        record = result.fetch_row()
        pubs = {}
        while record:
                pub_id = record[0][0]
                pub_type = record[0][1]
                pub_title = record[0][2]
                if pub_type not in pubs:
                        pubs[pub_type] = []
                pubs[pub_type].append(record[0])
                record = result.fetch_row()

        for pub_type in sorted(pubs.keys()):
                if not pubs[pub_type]:
                        print "<h3>No %s Publications with 0 or 2+ Reference Titles.</h3>" % pub_type
                        continue
                PrintTableColumns(('', '%s publications' % pub_type, ''))
                bgcolor = 1
                count = 1
                for pub in pubs[pub_type]:
                        pub_id = pub[0]
                        pub_title = pub[2]
                        cleanup_id = pub[3]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count, cleanup_id, 52)
                        bgcolor ^= bgcolor
                        count += 1
                print '</table><p>'

def function53():
        query = "select a1.author_id, a1.author_canonical, a2.author_id, a2.author_canonical, count(*) \
                from pseudonyms p, authors a1, authors a2, cleanup c \
                where p.pseudonym = a1.author_id \
                and p.author_id = a2.author_id \
                and p.author_id = c.record_id and c.report_type = 53 \
                group by p.author_id, p.pseudonym \
                having count(*) > 1"
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No Authors with Duplicate Alternate Names Found</h2>'
                return

        # Print table headers
        PrintTableColumns(('','Altrenate Name', 'Author', 'Count'))
        record = result.fetch_row()
        bgcolor = 1
        count = 1
        while record:
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%d</td>' % count
                print '<td>%s</td>' % ISFDBLink("ea.cgi", record[0][0], record[0][1])
                print '<td>%s</td>' % ISFDBLink("ea.cgi", record[0][2], record[0][3])
                print '<td>%s</td>' % record[0][4]
                print '</tr>'
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print "</table>"

def function54():
        print """<h3>This report is currently limited to COLLECTION and ANTHOLOGY
                titles which have at least one publication with fiction contents
                and one publication without fiction contents. The displayed list
                is limited to 1000 publications for performance reasons.</h3>"""

        query ="""select t.title_id, t.title_title, p.pub_id, p.pub_title, p.pub_year
                from titles t, pubs p, pub_content pc, cleanup c where
                t.title_id=c.record_id and c.report_type=54 and
                t.title_id=pc.title_id and pc.pub_id=p.pub_id limit 1000"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()
        if not num:
                print "<h2>No Collections/Anthologies without Contents Whose Other Editions Have Contents</h2>"
                return
        titles = {}
        pubs_set = set()
        count = 1
        while record:
                count += 1
                title_id = record[0][0]
                title_title = record[0][1]
                pub_id = record[0][2]
                pub_title = record[0][3]
                pub_year = record[0][4]
                if title_title not in titles:
                        titles[title_title] = {}
                if title_id not in titles[title_title]:
                        titles[title_title][title_id] = []
                titles[title_title][title_id].append((pub_id, pub_title, pub_year))
                pubs_set.add(str(pub_id))
                record = result.fetch_row()

        pubs_string = ",".join(pubs_set)
        query = """select p.pub_id from pubs p
                 where p.pub_id in (%s) and
                 not exists (select 1 from pub_content pc, titles t
                        where pc.pub_id=p.pub_id and
                        t.title_id=pc.title_id and
                        t.title_ttype in ('SHORTFICTION','POEM','SERIAL'))""" % pubs_string
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        empty_pubs = []
        while record:
                empty_pubs.append(record[0][0])
                record = result.fetch_row()

        PrintTableColumns(('#', 'Title', 'Publications'))
        count = 0
        color = 0
        for title_title in sorted(titles.keys()):
                for title_id in titles[title_title]:
                        # First check if there are any empty pubs for this titles --
                        # if we have already fixed all of them, then do not display this title
                        empty_count = 0
                        for pub in titles[title_title][title_id]:
                                if pub[0] in empty_pubs:
                                        empty_count += 1
                        if not empty_count:
                                break
                        count += 1
                        if color:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title)
                        print '<td>'
                        for pub in titles[title_title][title_id]:
                                if pub[0] in empty_pubs:
                                        suffix = ' [EMPTY]'
                                else:
                                        suffix = ''
                                print '%s (%s)%s<br>' % (ISFDBLink('pl.cgi', pub[0], pub[1]), pub[2], suffix)
                        print '</td>'
                        print '</tr>'
                        color = color ^ 1
                        record = result.fetch_row()
        print '</table><p>'

def function55():
        ui = isfdbUI()
        query = """select title_id, title_title from titles t, cleanup c
                where t.title_id=c.record_id and c.report_type=55
                and %s""" % ui.goodHtmlClause('t', 'title_title')

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num:
                PrintTableColumns(('', 'Title'))
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        record = result.fetch_row()
                        bgcolor ^= 1
                        count += 1

                print "</table>"
        else:
                print "<h2>No Title records with HTML in Titles.</h2>"

def function56():
        ui = isfdbUI()
        query = """select pub_id, pub_title from pubs p, cleanup c
        where p.pub_id=c.record_id and c.report_type=56
        and %s""" % ui.goodHtmlClause('p', 'pub_title')

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num:
                PrintTableColumns(('', 'Publication'))
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        record = result.fetch_row()
                        bgcolor ^= 1
                        count += 1

                print "</table>"
        else:
                print "<h2>No Publications with HTML in Titles.</h2>"

def function57():
        print '<h3>For SFE-hosted images, only links to /clute/, /clute_uk/, /langford/ and /robinson/ sub-directories are allowed.</h3>'
        
        query = """select pub_id, pub_title from pubs, cleanup c
                   where c.report_type = 57
                   and pubs.pub_id = c.record_id
                   and (pub_frontimage like '%sf-encyclopedia.uk%' or pub_frontimage like '%sf-encyclopedia.com%')
                   and pub_frontimage not like '%/clute/%'
                   and pub_frontimage not like '%/clute_uk/%'
                   and pub_frontimage not like '%/langford/%'
                   and pub_frontimage not like '%/robinson/%'
                   order by pub_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                PrintTableColumns(('', 'Publication'))
                count = 1
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No invalid SFE image links found</h2>'

def function58():
        cleanup.query = """select a.author_id, a.author_canonical
                from authors a, cleanup c
                where a.author_language is null
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and t.title_language is not null
                 and t.title_language = 16
                 )>0
                and c.record_id=a.author_id
                and c.report_type=58
                order by a.author_lastname"""

        cleanup.none = 'No matching records found'
        cleanup.print_author_table()

def function59():
        cleanup.query = """select a.author_id, a.author_canonical
                from authors a, cleanup c
                where a.author_language is null
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and t.title_language is not null
                 and t.title_language = 22
                 )>0
                and c.record_id=a.author_id
                and c.report_type=59
                order by a.author_lastname"""

        cleanup.none = 'No matching records found'
        cleanup.print_author_table()

def function60():
        cleanup.query = """select a.author_id, a.author_canonical
                from authors a, cleanup c
                where a.author_language is null
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and t.title_language is not null
                 and t.title_language = 26
                 )>0
                and c.record_id=a.author_id
                and c.report_type=60
                order by a.author_lastname"""

        cleanup.none = 'No matching records found'
        cleanup.print_author_table()

def function61():
        cleanup.query = """select a.author_id, a.author_canonical
                from authors a, cleanup c
                where a.author_language is null
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and t.title_language is not null
                 and t.title_language not in (16,17,22,26)
                 )>0
                and c.record_id=a.author_id
                and c.report_type=61
                order by a.author_lastname"""

        cleanup.none = 'No matching records found'
        cleanup.print_author_table()

def function62():
        query = """select t.title_id,t.title_title
                from cleanup c, titles t
                where (
                (t.title_storylen is not null
                and t.title_storylen not in ('ss','nt','nv'))
                or (t.title_storylen in ('ss','nt','nv')
                and t.title_ttype!='SHORTFICTION')
                )
                and c.record_id=t.title_id and c.report_type=62
                order by t.title_title"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()

        if num:
                PrintTableColumns(('', 'Title'))
                bgcolor = 1
                count = 1
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        bgcolor = bgcolor ^ 1
                        count += 1
                        record = result.fetch_row()
                print '</table><p>'
        else:
                print "<h2>No Titles with Invalid Length Values found</h2>"

def function63():
        query = """select distinct t1.title_id, t1.title_title
                from titles t1, titles t2, cleanup c
                where t1.title_parent = t2.title_id
                and t1.title_non_genre != t2.title_non_genre
                and t1.title_id = c.record_id
                and c.report_type = 63
                order by t1.title_title"""
        
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if not num:
                print "<h2>No Genre/Non-Genre Mismatches.</h2>"
                return

        PrintTableColumns(('', 'Title'))
        bgcolor = 1
        count = 1
        record = result.fetch_row()
        while record:
                title_id = record[0][0]
                title_title = record[0][1]
                PrintTitleRecord(title_id, title_title, bgcolor, count)
                bgcolor = bgcolor ^ 1
                count += 1
                record = result.fetch_row()
        print '</table>'

def function64():
        print """<h3>If a series legitimately contains EDITOR and non-EDITOR titles,
                please mention this fact in the series' Note field before marking it "Ignored".</h3>"""

        query = """select s.series_id, s.series_title, c.cleanup_id from series s, cleanup c
                 where s.series_id = c.record_id and c.report_type = 64 and c.resolved IS NULL
                 and exists(select 1 from titles t where t.series_id = s.series_id and t.title_ttype = 'EDITOR')
                 and exists(select 1 from titles t where t.series_id = s.series_id and t.title_ttype != 'EDITOR')
                 order by s.series_title"""
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h2>No Series with EDITOR and non-EDITOR Titles</h2>'
                return

        # Print table headers
        PrintTableColumns(('', 'Series', 'Ignore'))
        record = result.fetch_row()
        bgcolor = 1
        count = 1
        while record:
                series_id = record[0][0]
                series_name = record[0][1]
                cleanup_id = record[0][2]
                PrintSeriesRecord(series_id, series_name, bgcolor, count, cleanup_id, 64)
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print "</table>"

def function65():
        pattern_match = ISFDBBadUnicodePatternMatch('publisher_name')
        cleanup.query = """select publisher_id, publisher_name
                from publishers p, cleanup c where (%s)
                and p.publisher_id=c.record_id
                and c.report_type=65
                order by p.publisher_name""" % pattern_match

        cleanup.none = 'No Publishers with Invalid Unicode Characters Found'
        cleanup.print_publisher_table()

def function66():
        pattern_match = ISFDBBadUnicodePatternMatch('pub_series_name')
        cleanup.query = """select pub_series_id, pub_series_name
                from pub_series p, cleanup c where (%s)
                and p.pub_series_id=c.record_id
                and c.report_type=66
                order by p.pub_series_name""" % pattern_match
        cleanup.none = 'No Publication Series with Invalid Unicode Characters Found'
        cleanup.print_pub_series_table()

def function67():
        pattern_match = ISFDBBadUnicodePatternMatch('series_title')
        cleanup.query = """select series_id, series_title
                from series s, cleanup c where (%s)
                and s.series_id=c.record_id
                and c.report_type=67
                order by s.series_title""" % pattern_match
        cleanup.none = 'No Series with Invalid Unicode Characters Found'
        cleanup.print_series_table()

def function68():
        pattern_match = ISFDBBadUnicodePatternMatch('author_canonical')
        cleanup.query = """select author_id, author_canonical
                from authors a, cleanup c where (%s)
                and a.author_id=c.record_id
                and c.report_type=68
                order by a.author_lastname""" % pattern_match
        cleanup.none = 'No Authors with Invalid Unicode Characters Found'
        cleanup.print_author_table()

def function69():
        pattern_match = ISFDBBadUnicodePatternMatch('title_title')
        cleanup.query = """select title_id, title_title
                from titles t, cleanup c where (%s)
                and t.title_id=c.record_id
                and c.report_type=69
                order by t.title_title""" % pattern_match
        cleanup.none = 'No Titles with Invalid Unicode Characters Found'
        cleanup.print_title_table()

def function70():
        pattern_match = ISFDBBadUnicodePatternMatch('pub_title')
        cleanup.query = """select pub_id, pub_title
                from pubs p, cleanup c where (%s)
                and p.pub_id=c.record_id
                and c.report_type=70
                order by p.pub_title""" % pattern_match
        cleanup.none = 'No Publications with Invalid Unicode Characters Found'
        cleanup.print_pub_table()

def function71():
        print """<h3>This report lists all 9999-00-00 titles and titles expected
                     to be published more than 3 months in the future.</h3>"""
        query = """select t.title_id, t.title_title, t.title_copyright
                from titles t, cleanup c
                where t.title_copyright > DATE_ADD(NOW(), INTERVAL 3 MONTH)
                and t.title_copyright != '8888-00-00'
                and t.title_id=c.record_id and c.report_type=71
                order by t.title_title"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title', 'Date'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        title_date = record[0][2]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title)
                        print '<td>%s</td>' % title_date
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Forthcoming Titles Found</h2>'
        return

def function72():
        cleanup.note = """This report lists all 9999-00-00 publications and publications
                     expected to be published more than 3 months in the future."""
        cleanup.query = """select pub_id, pub_title, p.pub_year
                from pubs p, cleanup c
                where p.pub_year > DATE_ADD(NOW(), INTERVAL 3 MONTH)
                and p.pub_year != '8888-00-00'
                and p.pub_id=c.record_id and c.report_type=72
                order by p.pub_title"""
        cleanup.none = 'No Forthcoming Publications Found'
        cleanup.print_pub_with_date_table()

def function73():
        pattern_match = suspectUnicodePatternMatch('publisher_name')
        query = """select publisher_id, publisher_name, c.cleanup_id
                from publishers p, cleanup c where (%s)
                and p.publisher_id=c.record_id and c.report_type=73
                and c.resolved IS NULL
                order by p.publisher_name""" % pattern_match
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publisher', 'Ignore'))
                while record:
                        id = record[0][0]
                        name = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPublisherRecord(id, name, bgcolor, count, cleanup_id, 73)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Publishers with Suspect Unicode Characters Found</h2>"
        return

def function74():
        pattern_match = suspectUnicodePatternMatch('title_title')
        query = """select title_id, title_title, c.cleanup_id
                from titles t, cleanup c where (%s)
                and t.title_id=c.record_id and c.report_type=74
                and c.resolved IS NULL
                order by t.title_title""" % pattern_match
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title', 'Ignore'))
                while record:
                        id = record[0][0]
                        title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintTitleRecord(id, title, bgcolor, count, cleanup_id, 74)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Titles with Suspect Unicode Characters Found</h2>"
        return

def function75():
        pattern_match = suspectUnicodePatternMatch('pub_title')
        query = """select pub_id, pub_title, c.cleanup_id
                from pubs p, cleanup c where (%s)
                and p.pub_id=c.record_id and c.report_type=75
                and c.resolved IS NULL
                order by p.pub_title""" % pattern_match
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication', 'Ignore'))
                while record:
                        id = record[0][0]
                        name = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPublicationRecord(id, name, bgcolor, count, cleanup_id, 75)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Publications with Suspect Unicode Characters Found</h2>"
        return

def function76():
        pattern_match = suspectUnicodePatternMatch('series_title')
        query = """select series_id, series_title, c.cleanup_id
                from series s, cleanup c where (%s)
                and s.series_id=c.record_id and c.report_type=76
                and c.resolved IS NULL
                order by s.series_title""" % pattern_match
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Series', 'Ignore'))
                while record:
                        id = record[0][0]
                        name = record[0][1]
                        cleanup_id = record[0][2]
                        PrintSeriesRecord(id, name, bgcolor, count, cleanup_id, 76)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Series with Suspect Unicode Characters Found</h2>"
        return

def function77():
        pattern_match = suspectUnicodePatternMatch('pub_series_name')
        query = """select pub_series_id, pub_series_name, c.cleanup_id
                from pub_series p, cleanup c where (%s)
                and p.pub_series_id=c.record_id and c.report_type=77
                and c.resolved IS NULL
                order by p.pub_series_name""" % pattern_match
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication Series', 'Ignore'))
                while record:
                        id = record[0][0]
                        name = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPubSeriesRecord(id, name, bgcolor, count, cleanup_id, 77)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Publication Series with Suspect Unicode Characters Found</h2>"
        return

def function78():
        pattern_match = suspectUnicodePatternMatch('author_canonical')
        cleanup.query = """select author_id, author_canonical, c.cleanup_id
                from authors a, cleanup c where (%s)
                and a.author_id=c.record_id and c.report_type=78
                and c.resolved IS NULL
                order by a.author_canonical""" % pattern_match
        cleanup.ignore = 1
        cleanup.none = 'No Authors with Suspect Unicode Characters Found'
        cleanup.print_author_table()


def function79():
        query = """select p.pub_id, p.pub_title, c.cleanup_id from pubs p, cleanup c
                where
                (
                  (REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(pub_pages,'[',''),']',''),'+',''),'v',''),'i',''),'x','') < 80
                  and pub_pages!='' and pub_pages!='0'
                  and pub_pages not like '%+%')
                or
                  (pub_pages like '%+%' and pub_pages not REGEXP '[[:digit:]]{3}')
                )
                and p.pub_ctype='NOVEL'
                and p.pub_id=c.record_id and c.report_type=79
                and c.resolved IS NULL
                order by p.pub_title"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication', ''))
                while record:
                        id = record[0][0]
                        name = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPublicationRecord(id, name, bgcolor, count, cleanup_id, 79)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No NOVEL publications with fewer than 80 pages</h2>"
        return

def function80():
        query = """select p.pub_id, p.pub_title, t.title_id, t.title_title, c.cleanup_id
                from pubs p, pub_content pc, titles t, cleanup c
                where pc.pub_id = p.pub_id
                and (p.pub_ctype = 'MAGAZINE' or p.pub_ctype = 'FANZINE')
                and pc.title_id = t.title_id
                and t.title_ttype = 'SHORTFICTION'
                and p.pub_id=c.record_id
                and c.report_type=80
                and c.resolved is NULL
                GROUP BY p.pub_id, p.pub_title, t.title_title
                HAVING count(*) > 1"""

        db.query(query)
        result = db.store_result()

        if not result.num_rows():
                print "<h2>No Duplicate SHORTFICTION in Magazines/Fanzines</h2>"
                return

        record = result.fetch_row()
        data = {}
        while record:
                pub_id = record[0][0]
                if pub_id not in data:
                        data[pub_id] = []
                data[pub_id].append(record[0])
                record = result.fetch_row()

        PrintTableColumns(('', 'Publication', 'Title(s)', 'Ignore'))
        bgcolor = 1
        count = 1
        for pub_id in data:
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'
                print '<td>%d</td>' % count
                pub_title = data[pub_id][0][1]
                print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                print '<td>'
                for pub_data in data[pub_id]:
                        title_id = pub_data[2]
                        title_title = pub_data[3]
                        print ISFDBLink('title.cgi', title_id, title_title)
                        print '<br>'
                print '</td>'
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%d+1+80' % int(data[pub_id][0][4]), 'Ignore')
                print '</tr>'
                bgcolor ^= 1
                count += 1
        print '</table>'

def function81():
        query = """select s.series_id, s.series_title, c.cleanup_id
                from series s, cleanup c
                where s.series_title like '%/%'
                and s.series_title not like '% / %'
                and s.series_id=c.record_id
                and c.report_type=81
                and c.resolved IS NULL"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Series', ''))
                while record:
                        series_id = record[0][0]
                        series_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintSeriesRecord(series_id, series_title, bgcolor, count, cleanup_id, 81)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Series with Slashes and No Spaces</h2>"
        return

def function82():
        query = """select a.award_type_id, a.award_type_name, c.cleanup_id
                from award_types a, cleanup c
                where c.record_id=a.award_type_note_id
                and c.report_type=82"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                print '<h2>Award Types</h2>'
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Award Type', 'Resolve'))
                while record:
                        award_type_id = record[0][0]
                        award_type_name = record[0][1]
                        cleanup_id = record[0][2]
                        PrintAwardTypeRecord(award_type_id, award_type_name, bgcolor, count, cleanup_id, 82, 0)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Invalid Record URLs in Award Type Notes</h2>"

        query = """select a.award_cat_id, a.award_cat_name, c.cleanup_id
                from award_cats a, cleanup c
                where c.record_id=a.award_cat_note_id
                and c.report_type=82"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                print '<h2>Award Categories</h2>'
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Award Category', 'Resolve'))
                while record:
                        award_cat_id = record[0][0]
                        award_cat_name = record[0][1]
                        cleanup_id = record[0][2]
                        PrintAwardCatRecord(award_cat_id, award_cat_name, bgcolor, count, cleanup_id, 82, 0)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Invalid Record URLs in Award Category Notes</h2>"

        query = """select a.award_id, a.award_title, c.cleanup_id
                from awards a, cleanup c
                where c.record_id=a.award_note_id
                and c.report_type=82"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                print '<h2>Awards</h2>'
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Award', 'Resolve'))
                while record:
                        award_id = record[0][0]
                        award_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintAwardRecord(award_id, award_title, bgcolor, count, cleanup_id, 82, 0)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Invalid Record URLs in Award Notes</h2>"

        query = """select s.series_id, s.series_title, c.cleanup_id
                from series s, cleanup c
                where c.record_id=s.series_note_id
                and c.report_type=82"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                print '<h2>Series</h2>'
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Series', 'Resolve'))
                while record:
                        series_id = record[0][0]
                        series_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintSeriesRecord(series_id, series_title, bgcolor, count, cleanup_id, 82, 0)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Invalid Record URLs in Series Notes</h2>"

        query = """select p.publisher_id, p.publisher_name, c.cleanup_id
                from publishers p, cleanup c
                where c.record_id=p.note_id
                and c.report_type=82"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                print '<h2>Publishers</h2>'
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publisher', 'Resolve'))
                while record:
                        publisher_id = record[0][0]
                        publisher_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPublisherRecord(publisher_id, publisher_title, bgcolor, count, cleanup_id, 82, 0)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Invalid Record URLs in Publisher Notes</h2>"

        query = """select p.pub_series_id, p.pub_series_name, c.cleanup_id
                from pub_series p, cleanup c
                where c.record_id=p.pub_series_note_id
                and c.report_type=82"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                print '<h2>Publication Series</h2>'
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication Series', 'Resolve'))
                while record:
                        pub_series_id = record[0][0]
                        pub_series_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPubSeriesRecord(pub_series_id, pub_series_title, bgcolor, count, cleanup_id, 82, 0)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Invalid Record URLs in Publication Series Notes</h2>"

        query = """select t.title_id, t.title_title, c.cleanup_id
                from titles t, cleanup c
                where c.record_id=t.note_id
                and c.report_type=82"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                print '<h2>Title Notes</h2>'
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title', 'Resolve'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintTitleRecord(title_id, title_title, bgcolor, count, cleanup_id, 82, 0)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Invalid Record URLs in Title Notes</h2>"

        query = """select t.title_id, t.title_title, c.cleanup_id
                from titles t, cleanup c
                where c.record_id=t.title_synopsis
                and c.report_type=82"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                print '<h2>Synopses</h2>'
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title', 'Resolve'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintTitleRecord(title_id, title_title, bgcolor, count, cleanup_id, 82, 0)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Invalid Record URLs in Synopses</h2>"

        query = """select p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, cleanup c
                where c.record_id=p.note_id
                and c.report_type=82"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                print '<h2>Publications</h2>'
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication', 'Resolve'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count, cleanup_id, 82, 0)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Invalid Record URLs in Publication Notes</h2>"

def function83():
        nonModeratorMessage()
        # Serials without parenthetical disambiguation
        query = """select t.title_id, t.title_title, c.cleanup_id
                from titles t, cleanup c where
                (title_title not like '%(Complete Novel)')
                and (title_title not like '%(Part % of %)')
                and title_ttype='SERIAL'
                and c.report_type=83
                and c.record_id=t.title_id
                and c.resolved is NULL
                order by t.title_title"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title', 'Ignore'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintTitleRecord(title_id, title_title, bgcolor, count, cleanup_id, 83)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Serials without Standard Parenthetical Disambiguators Found</h2>"

def function84():
        nonModeratorMessage()
        # Serials with Potentially Unnecessary Disambiguation
        query = """select x.title_id, x.title_title, c.cleanup_id
                from (
                select min(t.title_id) as "title_id",
                t.title_title,
                substring(t.title_title,1,LOCATE("(", t.title_title)) y,
                count(*)
                from titles t
                where t.title_ttype = 'SERIAL'
                and t.title_title like '%(Part % of %)'
                group by y
                having count(*) = 1
                ) x, cleanup c
                where x.title_id = c.record_id
                and c.report_type = 84
                and c.resolved IS NULL
                order by x.title_title"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title', 'Ignore'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintTitleRecord(title_id, title_title, bgcolor, count, cleanup_id, 84)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Serials with Potentially Unnecessary Disambiguation Found</h2>"

def function85():
        query = """select a.author_id, a.author_canonical, a.author_legalname, l.lang_name
                from authors a, languages l, cleanup c
                where a.author_language = l.lang_id
                and l.latin_script='No'
                and a.author_legalname regexp'[[:alpha:]]'
                and a.author_id = c.record_id
                and c.report_type = 85
                order by a.author_lastname"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Canonical Name', 'Legal Name', 'Language'))
                while record:
                        author_id = record[0][0]
                        author_name = record[0][1]
                        author_legalname = record[0][2]
                        if not author_legalname:
                                author_legalname = '-'
                        lang_name = record[0][3]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('ea.cgi', author_id, author_name)
                        print '<td>%s</td>' % author_legalname
                        print '<td>%s</td>' % lang_name
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No records found</h2>'

def function86():
        query = """select distinct p.pub_id, p.pub_title
                from pubs p, primary_verifications pv, cleanup c, mw_user u
                where p.pub_id = pv.pub_id
                and p.pub_ptype = 'unknown'
                and p.pub_id=c.record_id and c.report_type=86
                and pv.user_id = u.user_id
                order by u.user_name, p.pub_title"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Verifiers', 'Publication'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % int(count)
                        verifiers = SQLPrimaryVerifiers(pub_id)
                        print '<td>'
                        verifier_count = 0
                        for verifier in verifiers:
                                user_name = verifier[1]
                                if verifier_count > 0:
                                        print ', '
                                print WikiLink(user_name)
                                verifier_count += 1
                        if not verifier_count:
                                print '&nbsp;'
                        print '</td>'
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Primary-Verified Publications with Unknown Format</h2>'
        return

def function87():
        # Author/title language mismatches
        nonModeratorMessage()

        print """<h3>Note: This report is currently limited to EDITOR, NOVEL, NONFICTION
                and SHORTFICTION titles.</h3>"""
        query = """select distinct t.title_id, t.title_title, t.title_ttype, c.cleanup_id
                from titles t, canonical_author ca, authors a, cleanup c
                where t.title_id=ca.title_id
                and ca.author_id=a.author_id
                and ca.ca_status=1
                and t.title_parent=0
                and t.title_language IS NOT NULL
                and a.author_language IS NOT NULL
                and t.title_language != a.author_language
                and c.report_type=87
                and c.resolved IS NULL
                and c.record_id=t.title_id
                order by t.title_ttype, a.author_lastname, a.author_canonical, t.title_title
                 """
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title Type', 'Author', 'Title', 'Ignore'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        title_ttype = record[0][2]
                        cleanup_id = record[0][3]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % title_ttype
                        authors = SQLTitleBriefAuthorRecords(title_id)
                        print '<td>'
                        author_counter = 0
                        for author in authors:
                                if author_counter:
                                        print ' <b>and</b> '
                                print ISFDBLink('ea.cgi', author[0], author[1])
                                author_counter += 1
                        print '</td>'
                        print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title)
                        if user.moderator:
                                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%d+1+87' % int(cleanup_id), 'Ignore this title')
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Author/Title Language Mismatches Found.</h2>'

def function88():
        # Pubs with multiple COVERART titles
        nonModeratorMessage()

        query = """select p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, cleanup c
                where (select count(t.title_id)
                      from titles t, pub_content pc
                      where p.pub_id = pc.pub_id
                      and t.title_id = pc.title_id
                      and t.title_ttype='COVERART')
                > 1
                and p.pub_id=c.record_id
                and c.report_type=88
                and c.resolved IS NULL
                order by p.pub_title"""
        db.query(query)
        result = db.store_result()

        if not result.num_rows():
                print "<h2>No publications with multiple COVERART titles</h2>"

        record = result.fetch_row()
        bgcolor = 1
        count = 1
        PrintTableColumns(('', 'Publication', 'Authors', 'Primary Verifiers', 'Ignore'))
        while record:
                pub_id = record[0][0]
                pub_title = record[0][1]
                cleanup_id = record[0][2]
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%s</td>' % count

                print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                
                authors = SQLPubBriefAuthorRecords(pub_id)
                print '<td>'
                for author in authors:
                        print ISFDBLink('ea.cgi', author[0], author[1])
                print '</td>'
                
                verifiers = SQLPrimaryVerifiers(pub_id)
                ver_count = 0
                print '<td>'
                for verifier in verifiers:
                        user_id = verifier[0]
                        user_name = verifier[1]
                        if ver_count > 0:
                                print '<br>'
                        print WikiLink(user_name)
                        ver_count += 1
                if not verifiers:
                        print '&nbsp;'
                print '</td>'
                                
                if user.moderator:
                        print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%s+1+88"' % cleanup_id, 'Ignore this pub')
                print '</tr>'

                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print '</table>'
        return

def function89():
        # Authors with Invalid Birthplaces
        query = """select author_id, author_canonical, author_birthplace, author_birthdate
                from authors, cleanup c
                where (
                (author_birthplace like '%, US')
                or
                  (author_birthplace like "%England%"
                  and author_birthplace not like "%Kingdom of England"
                  and author_birthplace not like "%England, Kingdom of Great Britain"
                  and author_birthplace not like "%England, UK")
                or
                  (author_birthplace like "%Scotland%"
                  and author_birthplace not like "%Kingdom of Scotland"
                  and author_birthplace not like "%Scotland, Kingdom of Great Britain"
                  and author_birthplace not like "%Scotland, UK")
                or
                  (YEAR(author_birthdate) <1801 and YEAR(author_birthdate) != '0000'
                  and author_birthplace like '%, UK')
                or (author_birthplace like '%United Kingdom')
                or
                  (YEAR(author_birthdate) < 1917 and YEAR(author_birthdate) != '0000'
                  and
                    (author_birthplace like '%, Russia%'
                    or
                    author_birthplace like '%, Ukraine%')
                  and author_birthplace not like '%Russian Empire')
                or
                  (YEAR(author_birthdate) > 1922 and YEAR(author_birthdate) < 1992
                  and YEAR(author_birthdate) != '0000'
                  and author_birthplace like '%, Russia%'
                  and author_birthplace not like '%, USSR')
                or
                  (YEAR(author_birthdate) < 1923 and YEAR(author_birthdate) != '0000'
                  and author_birthplace like '%, USSR')
                or
                  (YEAR(author_birthdate) > 1991 and author_birthplace like '%, USSR')
                or
                  (author_birthplace like '%Russian Federation%')
                """
        british_provinces = ('Connecticut',
                             'Delaware',
                             'Maryland',
                             'Massachusetts',
                             'New Hampshire',
                             'New Jersey',
                             'New York',
                             'North Carolina',
                             'Pennsylvania',
                             'Rhode Island',
                             'South Carolina',
                             'Virginia')
        for province in british_provinces:
                query += """ or (author_birthplace like '%%%s%%'
                                and author_birthplace not like '%%, USA'
                                and author_birthplace not like '%%, British Empire')
                         """ % province
        # 'Georgia' can be either:
        # 1. a British province which later became a US state, or
        # 2. a country that was a part of the Russian Empire in 1801-1971 and the USSR in 1922-1991
        query += """ or (author_birthplace like '%Georgia%'
                         and author_birthplace not like '%, USA'
                         and author_birthplace not like '%, British Empire'
                         and author_birthplace not like '%, USSR'
                         and author_birthplace not like '%, Russian Empire'
                         and author_birthplace not like '%, Georgia')"""

        # 'California' can be either a US state or 'Baja California', a Mexican state
        query += """ or (author_birthplace like '%California%'
                         and author_birthplace not like '%, USA'
                         and author_birthplace not like '%Baja California%')"""

        # 'Maine' can be either a US state or a French town or a French province or an Australian city
        query += """ or (author_birthplace like '%Maine%'
                    and author_birthplace not like '%, USA'
                    and author_birthplace not like '%Maine-et-Loire%'
                    and author_birthplace not like '%Domaine de la Devi%'
                    and author_birthplace not like '%Castlemaine%'
                    and author_birthplace not like '%Chalons-du-Maine%')"""

        # 'Hawaii' can be a US state or an independent kingdom or an independent republic
        query += """ or (author_birthplace like '%Hawaii%'
                    and author_birthplace not like '%, USA'
                    and author_birthplace not like '%Kingdom of Hawaii'
                    and author_birthplace not like '%Republic of Hawaii')"""

        # 'Montana' can be a US state or a town in Bulgaria
        query += """ or (author_birthplace like '%Montana%'
                    and author_birthplace not like '%, USA'
                    and author_birthplace not like '%Bulgaria')"""

        # 'Florida' can be a US state, a town in the state of Missouri (USA) or a municipality in Brazil
        query += """ or (author_birthplace like '%Florida%'
                    and author_birthplace not like '%, USA'
                    and author_birthplace not like '%, Brazil')"""

        other_us_states = ('Alabama',
                           'Alaska',
                           'Arizona',
                           'Arkansas',
                           'Colorado',
                           'Idaho',
                           'Illinois',
                           'Indiana',
                           'Iowa',
                           'Kansas',
                           'Kentucky',
                           'Louisiana',
                           'Michigan',
                           'Minnesota',
                           'Mississippi',
                           'Missouri',
                           'Nebraska',
                           'Nevada',
                           'New Mexico',
                           'North Dakota',
                           'Ohio',
                           'Oklahoma',
                           'Oregon',
                           'South Dakota',
                           'Tennessee',
                           'Texas',
                           'Utah',
                           'Vermont',
                           'Washington',
                           'West Virginia',
                           'Wisconsin',
                           'Wyoming')

        for us_state in other_us_states:
                query += """ or (author_birthplace like '%%%s%%'
                                and author_birthplace not like '%%, USA')""" % us_state

        query += """) and c.report_type = 89
                     and c.record_id = authors.author_id
                     order by authors.author_lastname"""

        db.query(query)
        result = db.store_result()

        print """<h3>See <a href="%s://%s/index.php?title=Template:AuthorFields:BirthPlace">
                        this template</a> for formatting information.</h3>""" % (PROTOCOL, WIKILOC)
        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Name', 'Birthplace', 'Birthdate'))
                while record:
                        author_id = record[0][0]
                        name = record[0][1]
                        birthplace = record[0][2]
                        birthdate = record[0][3]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('ea.cgi', author_id, name)
                        print '<td>%s</td>' % birthplace
                        print '<td>%s</td>' % birthdate
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No authors with invalid birthplaces</h2>'
        return

def function90():
        # Duplicate sub-series numbers within a series
        query = """select series_id from series
                where series_parent_position is not null
                group by series_parent, series_parent_position
                having count(*) >1
                """
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Parent Series', 'Position', 'Sub-series'))
                while record:
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        series_id = record[0][0]
                        print '<td>%d</td>' % count
                        
                        # Retrieve the parent series information
                        query1 = """select s2.series_id, s2.series_title
                                        from series s1, series s2
                                        where s1.series_parent = s2.series_id
                                        and s1.series_id = %s""" % series_id
                        db.query(query1)
                        result1 = db.store_result()
                        record1 = result1.fetch_row()
                        parent_series_id = record1[0][0]
                        parent_series_name = record1[0][1]
                        print '<td>%s</td>' % ISFDBLink('pe.cgi', parent_series_id, parent_series_name)
                        
                        # Retrieve the sub-series position
                        query2 = """select series_parent_position from series where
                                        series_id = %s""" % series_id
                        db.query(query2)
                        result2 = db.store_result()
                        record2 = result2.fetch_row()
                        parent_position = record2[0][0]
                        print '<td>%d</td>' % parent_position
                        
                        # Retrieve duplicate sub_series for this parent position
                        query3 = """select series_id, series_title from series where
                                        series_parent = %s and series_parent_position
                                        = %s""" % (parent_series_id, parent_position)
                        db.query(query3)
                        result3 = db.store_result()
                        record3 = result3.fetch_row()
                        print '<td>'
                        while record3:
                                subseries_id = record3[0][0]
                                subseries_name = record3[0][1]
                                print '%s<br>' % ISFDBLink('pe.cgi', subseries_id, subseries_name)
                                record3 = result3.fetch_row()
                        print '</td>'
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No duplicate sub-series numbers within a series found</h2>"

def function91():
        # Non-Art Titles by Non-English Authors without a Language
        query = """select distinct t.title_ttype, t.title_id, t.title_title
                   from authors a, titles t, canonical_author ca, cleanup c
                   where a.author_language != 17
                   and a.author_language is not null
                   and a.author_id = ca.author_id
                   and ca.title_id = t.title_id
                   and ca.ca_status = 1
                   and t.title_ttype not in ('COVERART', 'INTERIORART')
                   and t.title_language is null
                   and c.report_type = 91 and c.record_id = t.title_id
                   order by t.title_ttype, a.author_lastname, t.title_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num:
                PrintTitlesWithoutLanguage(result)
        else:
                print "<h2>No non-art titles by non-English authors without a language found</h2>"

def function92():
        # Primary-Verified Anthologies/Collections without Contents Titles
        query = """select distinct p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, primary_verifications pv, cleanup c,
                authors a, pub_authors pa, mw_user u
                where p.pub_ctype in ('ANTHOLOGY', 'COLLECTION')
                and c.report_type = 92 and c.record_id = p.pub_id
                and c.resolved is NULL
                and p.pub_id = pv.pub_id
                and NOT EXISTS
                  (select 1 from pub_content pc, titles t
                  where p.pub_id=pc.pub_id 
                  and pc.title_id=t.title_id
                  and (t.title_ttype in ('NOVEL', 'SHORTFICTION', 'POEM', 'SERIAL'))
                  )
                and p.pub_id = pa.pub_id
                and pa.author_id = a.author_id
                and pv.user_id = u.user_id
                order by u.user_name, a.author_lastname, p.pub_title"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                if not user.moderator:
                        print """<h2>If you find a legitimate Contents-less publication,
                        please post on the Moderator Noticeboard and a moderator will
                        remove it from this report.</h2>"""
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Verifier', 'Authors', 'Publication', 'Ignore'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        cleanup_id = record[0][2]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%s</td>' % count
                        verifiers = SQLPrimaryVerifiers(pub_id)
                        print '<td>'
                        verifier_count = 0
                        for verifier in verifiers:
                                if verifier_count > 0:
                                        print ', '
                                user_name = verifier[1]
                                print WikiLink(user_name)
                                verifier_count += 1
                        if not verifier_count:
                                print '&nbsp;'
                        print '</td>'
                        authors = SQLPubBriefAuthorRecords(pub_id)
                        print '<td>'
                        for author in authors:
                                print ISFDBLink('ea.cgi', author[0], author[1])
                        print '</td>'
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                        if user.moderator:
                                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%s+1+92' % cleanup_id, 'Ignore this pub')
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Primary-Verified Anthologies/Collections without Contents Titles found</h2>'
        return

def function93():
        # Publication Title-Reference Title Mismatches
        cleanup.query = """select distinct p.pub_id, p.pub_title
          from pubs p, cleanup c
          where p.pub_ctype in ('CHAPBOOK', 'OMNIBUS', 'ANTHOLOGY', 'COLLECTION', 'NONFICTION', 'NOVEL')
          and not exists
           (select 1 from titles t, pub_content pc
           where p.pub_id = pc.pub_id
           and pc.title_id = t.title_id
           and t.title_ttype = p.pub_ctype
           and p.pub_title = t.title_title
           )
          and c.report_type = 93
          and c.record_id = p.pub_id
          order by p.pub_title"""
        cleanup.note = 'The displayed list is limited to 1000 publications for performance reasons'
        cleanup.none = 'No Publication Title-Reference Title Mismatches found'
        cleanup.print_pub_table()

def function94():
        cleanup.query = """select a.author_id, a.author_canonical
                 from authors a, cleanup c
                 where
                 not exists (select 1 from canonical_author ca
                    where ca.author_id = a.author_id)
                 and not exists (select 1 from pub_authors pa
                    where pa.author_id = a.author_id)
                 and a.author_id = c.record_id
                 and c.report_type=94
                 order by a.author_lastname"""
        cleanup.none = 'No records found'
        cleanup.print_author_table()

def function95():
        cleanup.query = """select a.author_id, a.author_canonical
                 from authors a, cleanup c
                 where
                 not exists (select 1 from canonical_author ca
                    where ca.author_id = a.author_id)
                 and exists (select 1 from pub_authors pa
                    where pa.author_id = a.author_id)
                 and a.author_id = c.record_id
                 and c.report_type=95
                 order by a.author_lastname"""
        cleanup.none = 'No records found'
        cleanup.print_author_table()

def function96():
        query = """select t.title_id, t.title_title
                   from titles t, trans_titles tt, cleanup c
                   where t.title_ttype = 'COVERART'
                   and (t.title_title like 'Cover:%'
                   or (tt.trans_title_title like 'Cover:%' and tt.title_id = t.title_id)
                   )
                   and t.title_id = c.record_id and c.report_type=96
                   order by t.title_title"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title'))
                while record:
                        id = record[0][0]
                        title = record[0][1]
                        PrintTitleRecord(id, title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No COVERART Titles with a 'Cover: ' Prefix</h2>"
        return

def function97():
        nonModeratorMessage()

        query = """select distinct ps.pub_series_id, ps.pub_series_name, c.cleanup_id
                from pub_series ps, cleanup c
                where ps.pub_series_name regexp'[[:alpha:]]'
                and ps.pub_series_id = c.record_id
                and c.report_type=97 and c.resolved IS NULL
                order by ps.pub_series_name"""

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication Series', 'Ignore'))
                while record:
                        pub_series_id = record[0][0]
                        pub_series_name = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPubSeriesRecord(pub_series_id, pub_series_name, bgcolor, count, cleanup_id, 97)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Publication Series with Latin Characters in the Pub. Series Name and non-Latin Title Records Found</h2>"
        return

def function98():
        query = """select ps1.pub_series_name
                from pub_series ps1, pub_series ps2, cleanup c
                where ps1.pub_series_id != ps2.pub_series_id
                and ps1.pub_series_name=ps2.pub_series_name
                and ps1.pub_series_id=c.record_id and c.report_type=98
                order by ps1.pub_series_name"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                while record:
                        PrintTableColumns(('', 'Publication Series', ))
                        pub_series_name = record[0][0]
                        query2 = "select pub_series_id from pub_series where pub_series_name = '%s'" % db.escape_string(pub_series_name)
                        db.query(query2)
                        result2 = db.store_result()
                        record2 = result2.fetch_row()
                        bgcolor = 1
                        count = 1
                        while record2:
                                pub_series_id = record2[0][0]
                                PrintPubSeriesRecord(pub_series_id, pub_series_name, bgcolor, count)
                                bgcolor ^= 1
                                count += 1
                                record2 = result2.fetch_row()
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function99():
        nonModeratorMessage()

        query = """select distinct p.publisher_id, p.publisher_name, c.cleanup_id
                from publishers p, cleanup c
                where p.publisher_name regexp'[[:alpha:]]'
                and p.publisher_id = c.record_id
                and c.report_type=99
                and c.resolved IS NULL
                order by p.publisher_name"""

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publisher', 'Problem Pubs', 'Ignore'))
                while record:
                        publisher_id = record[0][0]
                        publisher_name = record[0][1]
                        cleanup_id = record[0][2]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('publisher.cgi', publisher_id, publisher_name)
                        print '<td>%s</td>' % ISFDBLink('edit/publisher_exceptions.cgi', publisher_id, 'Link')
                        if user.moderator:
                                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%d+1+99' % int(cleanup_id), 'Ignore this publisher')
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Publishers with Latin Characters and non-Latin Title Records Found</h2>'
        return

def function100():
        query = """select distinct p.pub_id, p.pub_title, p.pub_price
                from pubs p, cleanup c
                where p.pub_id = c.record_id
                and c.report_type = 100
                and (p.pub_price like '%$ %'
                or p.pub_price like concat('%',CHAR(0xA3),' ','%')
                or p.pub_price like concat('%',CHAR(0xA5),' ','%')
                or p.pub_price like concat('%',CHAR(0x80),'%',' ','%')
                or p.pub_price like concat('%','_',CHAR(0x80),'%')
                or p.pub_price like concat('%',CHAR(0x80),'%',',','%')
                or p.pub_price like '%CDN%'
                or p.pub_price like '%EUR%'
                or (p.pub_price like '$%,%'
                        and p.pub_price not like '$%.%')
                or (p.pub_price like 'C$%,%'
                        and p.pub_price not like 'C$%.%')
                or (p.pub_price like concat(CHAR(0xA3),'%',',','%')
                        and p.pub_price not like concat(CHAR(0xA3),'%',".",'%'))
                or p.pub_price regexp '^[[:digit:]]{1,}[,.]{0,}[[:digit:]]{0,}$'
                or (p.pub_price regexp '[.]{1}[[:digit:]]{3,}'
                        and p.pub_price not like 'BD %'
                        and p.pub_price not like '$0.__5'
                        and p.pub_price not like concat(CHAR(0xA3),'0.__5'))
                or (p.pub_price regexp '^[[:digit:]]{1,}'
                        and p.pub_price not like '%/%')
                or p.pub_price regexp '[[:digit:]]{4,}$'
                or p.pub_price like 'http%'
                or p.pub_price like '%&#20870;%'
                or p.pub_price like '%JP%'
                or p.pub_price like '% % %'
                or p.pub_price like '% $%'
                or p.pub_price like '%+%'
                or p.pub_price regexp '[[:digit:]]{1,} '
            )
                order by p.pub_title
                """

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                print """<h2>See <a href="%s">this Help template</a> and
                         <a href="%s">this Help page</a> for valid price
                         formats</h2>""" % (ISFDBWikiTemplate('PublicationFields:Price'),
                                            ISFDBWikiPage('Help:List of currency symbols'))
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication', 'Price'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        pub_price = record[0][2]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                        print '<td>%s</td>' % pub_price
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Publication Records with Invalid Prices Found</h2>'
        return

def function101():
        WikiPages(101, 108, 'Publication', 'Publication', 'pubs', 'pub_id', 'pub_title', 'pub_tag', 'pl')

def function102():
        WikiPages(102, 109, 'Publication_Talk', 'Publication', 'pubs', 'pub_id', 'pub_title', 'pub_tag', 'pl')

def function103():
        StrandedWikiPages(103, 108, 'Publication')

def function104():
        StrandedWikiPages(104, 109, 'Publication_Talk')

def function105():
        WikiPages(105, 112, 'Series', 'Series', 'series', 'series_id', 'series_title', 'series_title', 'pe')

def function106():
        WikiPages(106, 113, 'Series_Talk', 'Series', 'series', 'series_id', 'series_title', 'series_title', 'pe')

def function107():
        StrandedWikiPages(107, 112, 'Series')

def function108():
        StrandedWikiPages(108, 113, 'Series_Talk')

def function109():
        WikiPages(109, 110, 'Publisher', 'Publisher', 'publishers', 'publisher_id', 'publisher_name', 'publisher_name', 'publisher')

def function110():
        WikiPages(110, 111, 'Publisher_Talk', 'Publisher', 'publishers', 'publisher_id', 'publisher_name', 'publisher_name', 'publisher')

def function111():
        StrandedWikiPages(111, 110, 'Publisher')

def function112():
        StrandedWikiPages(112, 111, 'Publisher_Talk')

def function113():
        WikiPages(113, 106, 'Magazine', 'Magazine', 'series', 'series_id', 'series_title', 'series_title', 'pe')

def function114():
        WikiPages(114, 107, 'Magazine_Talk', 'Magazine', 'series', 'series_id', 'series_title', 'series_title', 'pe')

def function115():
        StrandedWikiPages(115, 106, 'Magazine')

def function116():
        StrandedWikiPages(116, 107, 'Magazine_Talk')

def function117():
        WikiPages(117, 104, 'Fanzine', 'Fanzine', 'series', 'series_id', 'series_title', 'series_title', 'pe')

def function118():
        WikiPages(118, 105, 'Fanzine_Talk', 'Fanzine', 'series', 'series_id', 'series_title', 'series_title', 'pe')

def function119():
        StrandedWikiPages(119, 104, 'Fanzine')

def function120():
        StrandedWikiPages(120, 105, 'Fanzine_Talk')

def WikiPages(report_number, namespace_number, namespace_name, record_name,
              table, record_id_field, record_title_field, linking_field,
              script, sort_name = ''):
        import urllib
        if not sort_name:
                sort_name = record_title_field
        # First check that Wiki tables exist in this instance of ISFDB
        if not WikiExists():
                print '<h2>Wiki data does not exist in this instance of ISFDB, so this report is not available.</h2>'
                return

        # Step 1: Find all record IDs with a matching Wiki page
        query = """select %s.%s, mw.page_title from mw_page mw, %s, cleanup c
                where c.record_id=%s.%s and c.report_type=%d
                and mw.page_namespace=%d and mw.page_title=REPLACE(%s.%s,' ','_')
                order by %s.%s
                """ % (table, record_id_field, table, table, record_id_field, int(report_number),
                       int(namespace_number), table, linking_field, table, sort_name)

        db.query(query)
        result = db.store_result()

        if not result.num_rows():
                print "<h2>No records found</h2>"
                return

        record = result.fetch_row()
        records = {}
        while record:
                record_id = record[0][0]
                page_title = record[0][1]
                records[record_id] = page_title
                record = result.fetch_row()

        # Step 2:
        query = """select distinct %s from webpages
                   where %s is not null
                   and url like '%%www.isfdb.org%%'""" % (record_id_field, record_id_field)

        # Step 3:
        #  Retrieve records and delete them from the record ID list built in Step 1
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
                record_id = record[0][0]
                if record_id in records:
                        del records[record_id]
                record = result.fetch_row()

        if not records:
                print "<h2>No records found</h2>"
                return

        # Step 4:
        # Convert the trimmed list of record IDs to a list and then to a SQL "in" clause.
        # Retrieve the final list of records from the database
        records_list = []
        for record_id in records:
                records_list.append(record_id)
        records_in_clause = list_to_in_clause(records_list)

        query = """select %s, %s from %s where %s in (%s) order by %s
                """ % (record_id_field, record_title_field, table, record_id_field, records_in_clause, sort_name)
        db.query(query)
        result = db.store_result()

        if not result.num_rows():
                print "<h2>No records found</h2>"
                return

        record = result.fetch_row()
        bgcolor = 1
        count = 1
        PrintTableColumns(('', record_name, 'Wiki Link'))
        while record:
                record_id = record[0][0]
                record_title = record[0][1]
                wiki_title = records[record_id]
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%d</td>' % int(count)
                print '<td>%s</td>' % ISFDBLink('%s.cgi' % script, record_id, record_title)
                print '<td><a href="%s://%s/index.php/%s:%s">%s</a></td>' % (PROTOCOL, WIKILOC, namespace_name, urllib.quote(wiki_title), wiki_title)
                print '</tr>'
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print '</table>'

def StrandedWikiPages(report_number, namespace_number, namespace_name):
        import urllib
        # First check that Wiki tables exist in this instance of ISFDB
        if not WikiExists():
                print '<h2>Wiki data does not exist in this instance of ISFDB, so this report is not available.</h2>'
                return

        query = """select mw.page_title from mw_page mw, cleanup c
                        where mw.page_namespace=%d
                        and c.record_id=mw.page_id
                        and c.report_type=%d order by mw.page_title
                        """ % (int(namespace_number), int(report_number))

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Wiki Link'))
                while record:
                        page_title = record[0][0]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td><a href="%s://%s/index.php/%s:%s">%s</a></td>' % (PROTOCOL, WIKILOC, namespace_name, urllib.quote(page_title), page_title)
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No records found</h2>'

def function121():
        query = """select distinct ps.pub_series_id, ps.pub_series_name, c.cleanup_id
                from pub_series ps, cleanup c
                where not exists
                  (select 1 from trans_pub_series tps where tps.pub_series_id = ps.pub_series_id)
                and ps.pub_series_id = c.record_id and c.report_type=121
                order by ps.pub_series_name"""

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication Series'))
                while record:
                        pub_series_id = record[0][0]
                        pub_series_name = record[0][1]
                        PrintPubSeriesRecord(pub_series_id, pub_series_name, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Publication Series with Latin Characters in the Pub. Series Name and no Transliterated Names.</h2>"
        return

def function122():
        query = """select distinct p.publisher_id, p.publisher_name, c.cleanup_id
                from publishers p, cleanup c
                where not exists
                  (select 1 from trans_publisher tp where tp.publisher_id = p.publisher_id)
                and p.publisher_id = c.record_id and c.report_type=122
                order by p.publisher_name"""

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publisher'))
                while record:
                        publisher_id = record[0][0]
                        publisher_name = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPublisherRecord(publisher_id, publisher_name, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Publishers with Latin Characters and no Transliterated Names.</h2>'
        return

def function123():
        query = """select a.author_id, a.author_canonical, a.author_legalname, l.lang_name
                from authors a, languages l, cleanup c
                where a.author_language = l.lang_id
                and (a.author_legalname = '' or a.author_legalname IS NULL)
                and exists
                        (select 1 from trans_legal_names tr
                        where tr.author_id = a.author_id)
                and a.author_id = c.record_id
                and c.report_type = 123
                order by a.author_lastname"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Canonical Name', 'Legal Name', 'Language'))
                while record:
                        author_id = record[0][0]
                        author_name = record[0][1]
                        author_legalname = record[0][2]
                        if not author_legalname:
                                author_legalname = '-'
                        lang_name = record[0][3]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('ea.cgi', author_id, author_name)
                        print '<td>%s</td>' % author_legalname
                        print '<td>%s</td>' % lang_name
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No records found</h2>'

def function124():
        transliteratedTitles(124)

def function125():
        transliteratedTitles(125)

def function126():
        transliteratedTitles(126)

def function127():
        transliteratedTitles(127)

def function128():
        transliteratedTitles(128)

def function129():
        transliteratedTitles(129)

def function130():
        transliteratedTitles(130)

def function131():
        transliteratedTitles(131)

def function132():
        transliteratedTitles(132)

def function133():
        transliteratedTitles(133)

def function134():
        transliteratedTitles(134)

def function135():
        transliteratedTitles(135)

def function136():
        transliteratedTitles(136)

def function137():
        reports = transliteratedReports('titles')
        languages = []
        for report in reports:
                language_name = report[0]
                languages.append(language_name)
        languages_in_clause = list_to_in_clause(languages)
        query = """select distinct t.title_id, t.title_title
                        from titles t, languages l, cleanup c
                        where t.title_title regexp '&#'
                        and ((t.title_language = l.lang_id and l.lang_name not in (%s))
                              or t.title_language is null)
                        and not exists
                          (select 1 from trans_titles tt where tt.title_id = t.title_id)
                        and t.title_id = c.record_id and c.report_type=137
                        order by t.title_title
                        """ % languages_in_clause
        transliteratedTitlesDisplay(query, 'Other')

def transliteratedTitles(report_id):
        reports = transliteratedReports('titles')
        for report in reports:
                if report_id == report[1]:
                        language = report[0]
                        break
        
        query = """select distinct t.title_id, t.title_title
                        from titles t, languages l, cleanup c
                        where t.title_title regexp '&#'
                        and t.title_language = l.lang_id
                        and l.lang_name = '%s'
                        and not exists
                          (select 1 from trans_titles tt where tt.title_id = t.title_id)
                        and t.title_id = c.record_id and c.report_type=%d
                        order by t.title_title
                        """ % (language, report_id)
        transliteratedTitlesDisplay(query, language)

def transliteratedTitlesDisplay(query, language):
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title', 'Authors'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        authors = SQLTitleBriefAuthorRecords(title_id)
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title)
                        print '<td>'
                        for author in authors:
                                print ISFDBLink('ea.cgi', author[0], author[1])
                        print '</td>'
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No %s Titles with no Transliterated Names.</h2>' % language
        return

def function138():
        nonLatinTitles(138)

def function139():
        nonLatinTitles(139)

def function140():
        nonLatinTitles(140)

def function141():
        nonLatinTitles(141)

def function142():
        nonLatinTitles(142)

def function143():
        reports = popularNonLatinLanguages('titles')
        languages = []
        for report in reports:
                languages.append(report[0])
        languages_in_clause = list_to_in_clause(languages)

        query = """select distinct t.title_id, t.title_title, c.cleanup_id
                   from titles t, languages l, cleanup c
                   where t.title_language = l.lang_id
                   and l.lang_name not in (%s)
                   and l.latin_script = 'No'
                   and t.title_title regexp'[[:alpha:]]'
                   and t.title_id = c.record_id and c.report_type=143
                   and c.resolved is NULL
                   order by t.title_title
                   """ % languages_in_clause
        nonLatinTitlesDisplay(143, query, 'Other')

def nonLatinTitles(report_id):
        reports = popularNonLatinLanguages('titles')
        for report in reports:
                if report_id == report[1]:
                        language = report[0]
                        break

        query = """select distinct t.title_id, t.title_title, c.cleanup_id
                   from titles t, languages l, cleanup c
                   where t.title_language = l.lang_id
                   and l.lang_name = '%s'
                   and t.title_title regexp'[[:alpha:]]'
                   and t.title_id = c.record_id and c.report_type=%d
                   and c.resolved is NULL
                   order by t.title_title
                   """ % (language, report_id)
        nonLatinTitlesDisplay(report_id, query, language)

def nonLatinTitlesDisplay(report_id, query, language):
        nonModeratorMessage()
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title', 'Ignore'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintTitleRecord(title_id, title_title, bgcolor, count, cleanup_id, report_id)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No %s Titles with Latin characters.</h2>" % language
        return

def function144():
        nonModeratorMessage()

        query = """select x.series_id, x.series_title, c.cleanup_id
                   from cleanup c,
                    (select distinct s1.series_id, s1.series_title
                    from series s1, series s2
                    where s1.series_id != s2.series_id
                    and s1.series_title = substring(s2.series_title, 1, LOCATE(' (', s2.series_title)-1)
                    and (
                           (s1.series_parent is not null and s1.series_parent != s2.series_id)
                           or (s2.series_parent is not null and s2.series_parent != s1.series_id)
                           or (s1.series_parent is null and s2.series_parent is null)
                        )
                    ) as x
                   where c.report_type=144
                   and c.resolved IS NULL
                   and c.record_id = x.series_id
                   order by x.series_title"""

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Series Title', 'Other Series Titles', 'Ignore'))
                while record:
                        series_id = record[0][0]
                        series_title = record[0][1]
                        cleanup_id = record[0][2]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('pe.cgi', series_id, series_title)

                        print '<td>'
                        query2 = """select series_id, series_title
                                    from series
                                    where series_title like '%s (%%'""" % db.escape_string(series_title)
                        db.query(query2)
                        result2 = db.store_result()
                        record2 = result2.fetch_row()
                        count2 = 1
                        while record2:
                                parenthetical_id = record2[0][0]
                                parenthetical_title = record2[0][1]
                                if count2 > 1:
                                        print '<br>'
                                print ISFDBLink('pe.cgi', parenthetical_id, parenthetical_title)
                                count2 += 1
                                record2 = result2.fetch_row()
                        
                        if user.moderator:
                                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                                '%d+%d+%d' % (int(cleanup_id), 1, 144),
                                                                'Ignore this series')
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Series Names That May Need Disambiguation Found</h2>'
        return

def function145():
        query = """select t.title_id, t.title_title from titles t, cleanup c
                   where t.title_id = c.record_id and c.report_type=145
                   and t.title_language = 54
                   and (
                           title_title like '%&#350%'
                           or title_title like '%&#351%'
                           or title_title like '%&#354%'
                           or title_title like '%&#355%'
                        )
                order by t.title_title"""

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No Romanian titles with s-cedilla or t-cedilla in the title.</h2>"
        return

def function146():
        query = """select distinct p.pub_id, p.pub_title
                   from pubs p, pub_content pc, titles t, cleanup c
                   where p.pub_id = pc.pub_id
                   and pc.title_id = t.title_id
                   and t.title_language = 54
                   and p.pub_id = c.record_id and c.report_type=146
                   and (
                           p.pub_title like '%&#350%'
                           or p.pub_title like '%&#351%'
                           or p.pub_title like '%&#354%'
                           or p.pub_title like '%&#355%'
                        )
                order by p.pub_title"""

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No pubs with Romanian titles with s-cedilla or t-cedilla.</h2>"
        return

def function147():
        query = """select distinct p.pub_id, p.pub_title
                   from pubs p, cleanup c
                   where p.pub_price like '%&#65509;%'
                   and p.pub_id = c.record_id and c.report_type=147
                   order by p.pub_title"""

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No pubs with fullwidth yen signs.</h2>"
        return

def function148():
        transliteratedPubs(148)

def function149():
        transliteratedPubs(149)

def function150():
        transliteratedPubs(150)

def function151():
        transliteratedPubs(151)

def function152():
        transliteratedPubs(152)

def function153():
        transliteratedPubs(153)

def function154():
        transliteratedPubs(154)

def function155():
        transliteratedPubs(155)

def function156():
        transliteratedPubs(156)

def function157():
        transliteratedPubs(157)

def function158():
        transliteratedPubs(158)

def function159():
        transliteratedPubs(159)

def function160():
        transliteratedPubs(160)

def function161():
        reports = transliteratedReports('pubs')
        languages = []
        for report in reports:
                language_name = report[0]
                languages.append(language_name)
        languages_in_clause = list_to_in_clause(languages)
        query = """select distinct p.pub_id, p.pub_title
                        from pubs p, pub_content pc, titles t, languages l, cleanup c
                        where p.pub_title regexp '&#'
                        and p.pub_id = pc.pub_id
                        and pc.title_id = t.title_id
                        and t.title_language = l.lang_id
                        and l.lang_name not in (%s)
                        and not exists
                          (select 1 from trans_pubs tp where tp.pub_id = p.pub_id)
                        and p.pub_id = c.record_id and c.report_type=161
                        order by t.title_title
                        """ % languages_in_clause
        transliteratedPubsDisplay(query, 'Other')

def transliteratedPubs(report_id):
        reports = transliteratedReports('pubs')
        for report in reports:
                if report_id == report[1]:
                        language = report[0]
                        break
        
        query = """select distinct p.pub_id, p.pub_title
                        from pubs p, pub_content pc, titles t, languages l, cleanup c
                        where p.pub_title regexp '&#'
                        and p.pub_id = pc.pub_id
                        and pc.title_id = t.title_id
                        and t.title_language = l.lang_id
                        and l.lang_name = '%s'
                        and not exists
                          (select 1 from trans_pubs tp where tp.pub_id = p.pub_id)
                        and p.pub_id = c.record_id and c.report_type=%d
                        order by p.pub_title
                        """ % (language, report_id)
        transliteratedPubsDisplay(query, language)

def transliteratedPubsDisplay(query, language):
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No %s Publications without Transliterated Titles.</h2>" % language
        return

def function162():
        nonLatinPubs(162)

def function163():
        nonLatinPubs(163)

def function164():
        nonLatinPubs(164)

def function165():
        nonLatinPubs(165)

def function166():
        nonLatinPubs(166)

def function167():
        reports = popularNonLatinLanguages('pubs')
        languages = []
        for report in reports:
                languages.append(report[0])
        languages_in_clause = list_to_in_clause(languages)

        query = """select distinct p.pub_id, p.pub_title, c.cleanup_id
                   from pubs p, pub_content pc, titles t, languages l, cleanup c
                   where t.title_language = l.lang_id
                   and p.pub_id = pc.pub_id
                   and pc.title_id = t.title_id
                   and l.lang_name not in (%s)
                   and l.latin_script = 'No'
                   and p.pub_title regexp'[[:alpha:]]'
                   and p.pub_id = c.record_id and c.report_type=167
                   and c.resolved is NULL
                   order by p.pub_title
                   """ % languages_in_clause
        nonLatinPubsDisplay(167, query, 'Other')

def nonLatinPubs(report_id):
        reports = popularNonLatinLanguages('pubs')
        for report in reports:
                if report_id == report[1]:
                        language = report[0]
                        break

        query = """select distinct p.pub_id, p.pub_title, c.cleanup_id
                   from pubs p, pub_content pc, titles t, languages l, cleanup c
                   where t.title_language = l.lang_id
                   and p.pub_id = pc.pub_id
                   and pc.title_id = t.title_id
                   and l.lang_name = '%s'
                   and p.pub_title regexp'[[:alpha:]]'
                   and p.pub_id = c.record_id and c.report_type=%d
                   and c.resolved is NULL
                   order by p.pub_title
                   """ % (language, report_id)
        nonLatinPubsDisplay(report_id, query, language)

def nonLatinPubsDisplay(report_id, query, language):
        nonModeratorMessage()
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication', 'Ignore'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count, cleanup_id, report_id)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No %s Publications with Latin characters.</h2>" % language
        return

def function168():
        query = """select a.author_id, a.author_canonical, a.author_lastname, a.author_language
                   from authors a, languages l, canonical_author ca1, titles t, cleanup c
                   where (select count(*) from canonical_author ca2
                        where ca2.author_id = a.author_id) = 1
                   and ca1.author_id = a.author_id
                   and ca1.title_id = t.title_id
                   and t.title_language = l.lang_id
                   and l.latin_script = 'No'
                   and not exists(select 1 from trans_authors ta
                                  where ta.author_id = a.author_id)
                   and a.author_id = c.record_id and c.report_type=168
                   order by a.author_lastname"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Author', 'Language'))
                while record:
                        author_id = record[0][0]
                        author_name = record[0][1]
                        author_language = record[0][3]
                        if not author_language:
                                author_language = 0
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('ea.cgi', author_id, author_name)
                        print '<td>%s</td>' % LANGUAGES[author_language]
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No records found</h2>"

def function169():
        transliteratedAuthors(169)

def function170():
        transliteratedAuthors(170)

def function171():
        transliteratedAuthors(171)

def function172():
        transliteratedAuthors(172)

def function173():
        transliteratedAuthors(173)

def function174():
        transliteratedAuthors(174)

def function175():
        transliteratedAuthors(175)

def function176():
        transliteratedAuthors(176)

def function177():
        transliteratedAuthors(177)

def function178():
        transliteratedAuthors(178)

def function179():
        transliteratedAuthors(179)

def function180():
        transliteratedAuthors(180)

def function181():
        transliteratedAuthors(181)

def function182():
        reports = transliteratedReports('titles')
        languages = []
        for report in reports:
                language_name = report[0]
                languages.append(language_name)
        languages_in_clause = list_to_in_clause(languages)
        query = """select distinct a.author_id, a.author_canonical
                        from authors a, languages l, cleanup c
                        where not exists
                          (select 1 from trans_authors ta
                           where ta.author_id = a.author_id)
                        and a.author_canonical regexp '&#'
                        and a.author_language = l.lang_id
                        and l.lang_name not in (%s)
                        and a.author_id = c.record_id and c.report_type=182
                        order by a.author_canonical
                        """ % languages_in_clause
        transliteratedAuthorsDisplay(query, 'Other')

def transliteratedAuthors(report_id):
        reports = transliteratedReports('authors')
        for report in reports:
                if report_id == report[1]:
                        language = report[0]
                        break
        
        query = """select distinct a.author_id, a.author_canonical
                        from authors a, languages l, cleanup c
                        where not exists
                          (select 1 from trans_authors ta
                           where ta.author_id = a.author_id)
                        and a.author_canonical regexp '&#'
                        and a.author_language = l.lang_id
                        and l.lang_name = '%s'
                        and a.author_id = c.record_id and c.report_type=%d
                        order by a.author_canonical
                        """ % (language, report_id)
        transliteratedAuthorsDisplay(query, language)

def transliteratedAuthorsDisplay(query, language):
        cleanup.query = query
        cleanup.none = 'No %s Authors without Transliterated Names' % language
        cleanup.print_author_table()

def function183():
        nonLatinAuthors(183)

def function184():
        nonLatinAuthors(184)

def function185():
        nonLatinAuthors(185)

def function186():
        nonLatinAuthors(186)

def function187():
        nonLatinAuthors(187)

def function188():
        reports = popularNonLatinLanguages('authors')
        languages = []
        for report in reports:
                languages.append(report[0])
        languages_in_clause = list_to_in_clause(languages)

        query = """select distinct t.title_id, t.title_title, t.title_ttype, c.cleanup_id
                   from titles t, languages l, authors a, canonical_author ca, cleanup c
                   where t.title_language = l.lang_id
                   and l.lang_name not in (%s)
                   and l.latin_script = 'No'
                   and a.author_canonical not regexp '&#'
                   and a.author_canonical not in ('unknown', 'uncredited')
                   and ca.title_id = t.title_id
                   and ca.author_id = a.author_id
                   and ca.ca_status = 1
                   and t.title_id = c.record_id and c.report_type=188
                   and c.resolved is NULL
                   order by t.title_title
                   """ % languages_in_clause
        nonLatinAuthorsDisplay(188, query, 'Other')

def nonLatinAuthorsDisplay(report_id, query, language):
        nonModeratorMessage()
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title', 'Title Type', 'Authors', 'Ignore'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        title_ttype = record[0][2]
                        cleanup_id = record[0][3]
                        authors = SQLTitleBriefAuthorRecords(title_id)
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title)
                        print '<td>%s</td>' % title_ttype
                        print '<td>'
                        for author in authors:
                                print ISFDBLink('ea.cgi', author[0], author[1])
                        print '</td>'
                        if cleanup_id and user.moderator:
                                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%d+1+%d' % (int(cleanup_id), int(report_id)), 'Ignore this title')
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No %s Titles with a Latin author name.</h2>' % language
        return
                  
def nonLatinAuthors(report_id):
        reports = popularNonLatinLanguages('authors')
        for report in reports:
                if report_id == report[1]:
                        language = report[0]
                        break

        query = """select distinct t.title_id, t.title_title, t.title_ttype, c.cleanup_id
                   from titles t, languages l, authors a, canonical_author ca, cleanup c
                   where t.title_language = l.lang_id
                   and l.lang_name = '%s'
                   and a.author_canonical not regexp '&#'
                   and a.author_canonical not in ('unknown', 'uncredited')
                   and ca.title_id = t.title_id
                   and ca.author_id = a.author_id
                   and ca.ca_status = 1
                   and t.title_id = c.record_id and c.report_type=%d
                   and c.resolved is NULL
                   order by t.title_title
                   """ % (language, report_id)
        nonLatinAuthorsDisplay(report_id, query, language)

def function189():
        nonModeratorMessage()

        query = """select x.pub_series_id, x.pub_series_name, c.cleanup_id
                   from cleanup c,
                    (select distinct ps1.pub_series_id, ps1.pub_series_name
                    from pub_series ps1, pub_series ps2
                    where ps1.pub_series_id != ps2.pub_series_id
                    and ps1.pub_series_name = substring(ps2.pub_series_name, 1, LOCATE(' (', ps2.pub_series_name)-1)
                    ) as x
                   where c.report_type=189
                   and c.resolved IS NULL
                   and c.record_id = x.pub_series_id
                   order by x.pub_series_name"""

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Pub. Series Title', 'Other Pub. Series Titles', 'Ignore'))
                while record:
                        pub_series_id = record[0][0]
                        pub_series_title = record[0][1]
                        cleanup_id = record[0][2]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink("pubseries.cgi", pub_series_id, pub_series_title)

                        print '<td>'
                        query2 = """select pub_series_id, pub_series_name from pub_series
                                where pub_series_name like '%s (%%'""" % db.escape_string(pub_series_title)
                        db.query(query2)
                        result2 = db.store_result()
                        record2 = result2.fetch_row()
                        count2 = 1
                        while record2:
                                parenthetical_id = record2[0][0]
                                parenthetical_title = record2[0][1]
                                if count2 > 1:
                                        print '<br>'
                                print ISFDBLink("pubseries.cgi", parenthetical_id, parenthetical_title)
                                count2 += 1
                                record2 = result2.fetch_row()
                        
                        if user.moderator:
                                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%d+1+189' % int(cleanup_id), 'Ignore this series')
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Publication Series Names That May Need Disambiguation Found</h2>'
        return

def function190():
        query = """select a.award_id, a.award_movie
                   from awards a, cleanup c
                   where a.award_id=c.record_id and c.report_type=190
                   and a.award_movie is not NULL
                   and a.award_movie != ''
                   and SUBSTRING(a.award_movie, 1, 2) != 'tt'
                   order by a.award_movie"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Movie/TV Show'))
                while record:
                        award_id = record[0][0]
                        award_movie = record[0][1]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('award_details.cgi', award_id, award_movie)
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No invalid award records found</h2>"

def function191():
        query = """select c.record_id, n.note_id
                from cleanup c, notes n
                where c.record_id = n.note_id
                and c.report_type=191
                and (
                REPLACE(n.note_note, ' ', '') like '%<ahref=""%'
                or REPLACE(n.note_note, ' ', '') regexp 'ahref=http'
                or REPLACE(n.note_note, ' ', '') regexp 'ahref="http{1}[^\"\>]{1,}>'
                or REPLACE(note_note, ' ', '') regexp 'ahref="http{1}[^\"\>]{1,}"">'
                )"""
        MismatchesInNotes(query, 'Invalid URLs')

def function192():
        # Authors without a Working Language
        cleanup.note = 'This report is currently limited to authors whose names start with the letters W-Z'
        cleanup.query = """select a.author_id, a.author_canonical
                   from authors a, cleanup c
                   where a.author_language is null
                   and c.record_id = a.author_id
                   and c.report_type = 192
                   order by a.author_lastname, a.author_canonical"""
        cleanup.none = 'No eligible authors without a working language'
        cleanup.print_author_table()

def function193():
        # Multilingual Publications
        query = """select pc.pub_id, p.pub_title, p.pub_ctype, c.cleanup_id
                   from titles t, pub_content pc, pubs p, cleanup c
                   where pc.title_id = t.title_id
                   and pc.pub_id = p.pub_id
                   and t.title_language is not null
                   and t.title_language != ''
                   and c.report_type = 193
                   and c.record_id = pc.pub_id
                   and c.resolved is NULL
                   group by pc.pub_id
                   HAVING COUNT(distinct t.title_language) > 1
                   order by p.pub_ctype, p.pub_title
                """

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Pub. Type', 'Publication', 'Ignore'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        pub_ctype = record[0][2]
                        cleanup_id = record[0][3]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % pub_ctype
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                        if cleanup_id and user.moderator:
                                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                                '%d+1+193' % int(cleanup_id),
                                                                'Ignore this publication')
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No outstanding multilingual publications found</h2>'

def function194():
        query = """select title_id, t.title_title, t.title_ttype
                   from titles t, cleanup c
                   where t.title_language is null
                   and t.title_id = c.record_id
                   and c.report_type = 194
                   order by t.title_ttype, t.title_title"""

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Title Type', 'Title', 'Author'))
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        title_type = record[0][2]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%s</td>' % count
                        print '<td>%s</td>' % title_type
                        print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title)
                        authors = SQLTitleBriefAuthorRecords(title_id)
                        print '<td>'
                        for author in authors:
                                print ISFDBLink('ea.cgi', author[0], author[1])
                        print '</td>'
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No titles without a language found.</h2>'
        return

def function195():
        print """<h2>This report identifies non-Omnibus titles with content values.
                   It also identifies Content values starting with a slash, which
                   is no longer necessary.</h2>"""
        query = """select t.title_id, t.title_title
                   from titles t, cleanup c
                   where (
                   (t.title_ttype != 'OMNIBUS' and t.title_content is not null)
                   or SUBSTRING(title_content,1,1) = '/'
                   )
                   and c.record_id = t.title_id and c.report_type = 195
                   order by t.title_title"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()

        if num:
                PrintTableColumns(('', 'Title'))
                bgcolor = 1
                count = 1
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        PrintTitleRecord(title_id, title_title, bgcolor, count)
                        bgcolor = bgcolor ^ 1
                        count += 1
                        record = result.fetch_row()
                print '</table><p>'
        else:
                print "<h2>No Titles with invalid content values found</h2>"

def function196():
        query = """select distinct t1.title_id, t1.title_title
                from titles t1, titles t2, cleanup c
                where t1.title_parent = t2.title_id
                and t1.title_jvn != t2.title_jvn
                and t1.title_id = c.record_id
                and c.report_type = 196
                order by t1.title_title"""
        
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if not num:
                print "<h2>No Juvenile/Non-Juvenile Mismatches.</h2>"
                return

        PrintTableColumns(('', 'Title'))
        bgcolor = 1
        count = 1
        record = result.fetch_row()
        while record:
                title_id = record[0][0]
                title_title = record[0][1]
                PrintTitleRecord(title_id, title_title, bgcolor, count)
                bgcolor = bgcolor ^ 1
                count += 1
                record = result.fetch_row()
        print '</table>'

def function197():
        query = """select distinct t1.title_id, t1.title_title
                from titles t1, titles t2, cleanup c
                where t1.title_parent = t2.title_id
                and t1.title_nvz != t2.title_nvz
                and t1.title_id = c.record_id
                and c.report_type = 197
                order by t1.title_title"""
        
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if not num:
                print "<h2>No Novelization/Non-Novelization Mismatches.</h2>"
                return

        PrintTableColumns(('', 'Title'))
        bgcolor = 1
        count = 1
        record = result.fetch_row()
        while record:
                title_id = record[0][0]
                title_title = record[0][1]
                PrintTitleRecord(title_id, title_title, bgcolor, count)
                bgcolor = bgcolor ^ 1
                count += 1
                record = result.fetch_row()
        print '</table>'

def function198():
        # Author/alternate name language mismatches
        cleanup.query = """select distinct a2.author_id, a2.author_canonical, c.cleanup_id
                from authors a1, authors a2, pseudonyms p, cleanup c
                where a1.author_id = p.author_id
                and p.pseudonym = a2.author_id
                and (
                        (a1.author_language != a2.author_language)
                        or (a1.author_language is NULL and a2.author_language is not null)
                        or (a1.author_language is not NULL and a2.author_language is null)
                )
                and c.record_id = a2.author_id
                and c.report_type = 198
                and c.resolved IS NULL
                order by a2.author_lastname, a2.author_canonical"""
        cleanup.none = 'No author/alternate name language mismatches found'
        cleanup.ignore = 1
        cleanup.print_author_table()

def function199():
        # Author Notes to be Migrated from ISFDB 1.0"
        query = """select a.author_id, a.author_canonical, a.author_note, n.note_note
                   from authors a, notes n
                   where a.note_id is not null
                   and a.note_id=n.note_id
                   order by a.author_lastname"""
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Author', 'Old Note', 'New Note'))
                while record:
                        author_id = record[0][0]
                        author_name = record[0][1]
                        new_note = record[0][2]
                        if not new_note:
                                new_note = '&nbsp;'
                        old_note = record[0][3]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('ea.cgi', author_id, author_name)
                        print '<td>%s</td>' % old_note
                        print '<td>%s</td>' % new_note
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No author/alternate name language mismatches found.</h2>'
        return

def function200():
        WikiPages(200, 100, 'Author', 'Author', 'authors', 'author_id', 'author_canonical', 'author_canonical', 'ea', 'author_lastname')

def function201():
        WikiPages(201, 101, 'Author_talk', 'Author', 'authors', 'author_id', 'author_canonical', 'author_canonical', 'ea', 'author_lastname')

def function202():
        StrandedWikiPages(202, 100, 'Author')

def function203():
        StrandedWikiPages(203, 101, 'Author_talk')

def function204():
        WikiPages(204, 102, 'Bio', 'Author', 'authors', 'author_id', 'author_canonical', 'author_canonical', 'ea', 'author_lastname')

def function205():
        WikiPages(205, 103, 'Bio_talk', 'Author', 'authors', 'author_id', 'author_canonical', 'author_canonical', 'ea', 'author_lastname')

def function206():
        StrandedWikiPages(206, 102, 'Bio')

def function207():
        StrandedWikiPages(207, 103, 'Bio_talk')

def function208():
        Nightly_html(208, 'pubs', 'note_id', 'pub_id', 'pub_title', 'pl')

def function209():
        Nightly_html(209, 'titles', 'note_id', 'title_id', 'title_title', 'title')

def function210():
        Nightly_html(210, 'publishers', 'note_id', 'publisher_id', 'publisher_name', 'publisher')

def function211():
        Nightly_html(211, 'series', 'series_note_id', 'series_id', 'series_title', 'pe')

def function212():
        Nightly_html(212, 'pub_series', 'pub_series_note_id', 'pub_series_id', 'pub_series_name', 'pubseries')

def function213():
        Nightly_html(213, 'awards', 'award_note_id', 'award_id', 'award_title', 'award_details')

def function214():
        Nightly_html(214, 'award_types', 'award_type_note_id', 'award_type_id', 'award_type_name', 'awardtype')

def function215():
        Nightly_html(215, 'award_cats', 'award_cat_note_id', 'award_cat_id', 'award_cat_name', 'award_category')

def function216():
        Nightly_html(216, 'titles', 'title_synopsis', 'title_id', 'title_title', 'title')

def function217():
        Nightly_html(217, 'authors', 'author_note', 'author_id', 'author_canonical', 'ea')

def function218():
        ids_in_notes(218, '%ASIN%', 'ASINs', 1, 'binary')

def function219():
        ids_in_notes(219, '%.bl.%', 'British Library IDs', 1)

def function220():
        ids_in_notes(220, '%.sfbg.us%', 'SFBG IDs')

def function221():
        ids_in_notes(221, '%/d-nb.info/%', 'direct Deutsche Nationalbibliothek links')

def function222():
        ids_in_notes(222, '%fantlab.ru/%', 'FantLab links', 1)

def function223():
        ids_in_notes(223, '%.amazon.%dp%', 'direct Amazon links', 1)

def function224():
        ids_in_notes(224, '%catalogue.bnf.fr%', 'direct BNF links')

def function225():
        ids_in_notes(225, '%lccn.loc%', 'direct Library of Congress links', 1)

def function226():
        ids_in_notes(226, '%worldcat.org/%', 'direct OCLC/WorldCat links', 1)

def ids_in_notes(report_number, pattern_match, display_name, allow_ignore = 0, like_modifier = ''):
        if allow_ignore:
                nonModeratorMessage()
        query = """select p.pub_id, p.pub_title, c.cleanup_id
                 from notes n, pubs p, cleanup c
                 where p.note_id = n.note_id
                 and n.note_note like %s '%s'
                 and p.pub_id = c.record_id
                 and c.report_type=%d
                 and c.resolved is NULL
                 order by p.pub_title""" % (like_modifier, pattern_match, int(report_number))

        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                if allow_ignore:
                        PrintTableColumns(('', 'Publication', 'Ignore'))
                else:
                        PrintTableColumns(('', 'Publication'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        if allow_ignore:
                                cleanup_id = record[0][2]
                                PrintPublicationRecord(pub_id, pub_title, bgcolor, count, cleanup_id, report_number)
                        else:
                                PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print "</table>"
        else:
                print "<h2>No publications with %s in Notes.</h2>" % display_name

def function227():
        nonModeratorMessage()
        query = """select t.title_id, t.title_title, c.cleanup_id,
                LENGTH(REPLACE(t.title_title, ')', '')) - LENGTH(REPLACE(t.title_title, '(', '')) as cnt
                from titles t, cleanup c
                where t.title_id = c.record_id
                and c.report_type = 227
                and c.resolved is NULL
                having cnt != 0
                order by t.title_title"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()

        if num:
                PrintTableColumns(('', 'Title', 'Ignore'))
                bgcolor = 1
                count = 1
                while record:
                        title_id = record[0][0]
                        title_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintTitleRecord(title_id, title_title, bgcolor, count, cleanup_id, 227)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table><p>'
        else:
                print "<h2>No titles with mismatched parentheses found</h2>"

def function228():
        nonModeratorMessage()
        query = """select p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, cleanup c, publishers pb
                where p.pub_isbn is null
                and p.publisher_id = pb.publisher_id
                and pb.publisher_name not like '%Project Gutenberg%'
                and p.pub_ptype = 'ebook'
                and p.pub_ctype not in ('FANZINE','MAGAZINE')
                and not exists(
                         select 1 from identifiers
                         where identifier_type_id = 1 and pub_id = p.pub_id)
                and p.pub_id = c.record_id
                and c.report_type = 228
                and c.resolved is null
                order by p.pub_title"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()

        if num:
                PrintTableColumns(('', 'Publication', 'Ignore'))
                bgcolor = 1
                count = 1
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count, cleanup_id, 228)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table><p>'
        else:
                print "<h2>No ISBN-less e-publications without an ASIN found</h2>"

def function229():
        ui = isfdbUI()
        query = """select p.pub_id, p.pub_title
                from pubs p, notes n, cleanup c
                where p.note_id = n.note_id and ("""
        count = 0
        for tag in ui.required_paired_tags:
                if count:
                        query += " or "
                query += """round((length(lower(n.note_note)) - length(replace(lower(n.note_note),'<%s>','')))/%d) !=
                round((length(lower(n.note_note)) - length(replace(lower(n.note_note),'</%s>','')))/%d)""" % (tag, len(tag)+2, tag, len(tag)+3)
                count += 1
        query += """) and p.pub_id = c.record_id
                and c.report_type = 229
                order by p.pub_title"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()

        if num:
                PrintTableColumns(('', 'Publication'))
                bgcolor = 1
                count = 1
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table><p>'
        else:
                print "<h2>No publications with mismatches HTML tags found.</h2>"

def function230():
        query = """select p.pub_id, n.note_note
                from notes n, pubs p, cleanup c
                where p.note_id = n.note_id
                and n.note_note regexp
                '<a href=\"https:\/\/www.worldcat.org\/oclc\/[[:digit:]]{1,11}"\>[[:digit:]]{1,11}\<\/a>'
                and p.pub_id = c.record_id
                and c.report_type = 230"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        pubs = []
        while record:
                pub_id = int(record[0][0])
                note_note = record[0][1]
                record = result.fetch_row()
                two_numbers = note_note.lower().split('/oclc/')[1].split('</a>')[0]
                number_list = two_numbers.split('">')
                if number_list[0] != number_list[1]:
                        pubs.append(pub_id)

        if pubs:
                in_clause = list_to_in_clause(pubs)
                query = "select pub_id, pub_title from pubs where pub_id in (%s) order by pub_title" % in_clause
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                num = result.num_rows()
                if num:
                        PrintTableColumns(('', 'Publication'))
                        bgcolor = 1
                        count = 1
                        while record:
                                pub_id = record[0][0]
                                pub_title = record[0][1]
                                PrintPublicationRecord(pub_id, pub_title, bgcolor, count)
                                bgcolor ^= 1
                                count += 1
                                record = result.fetch_row()
                        print '</table><p>'
        else:
                print "<h2>No publications with mismatched OCLC URLs in Notes.</h2>"

def function231():
        domains = SQLLoadRecognizedDomains()
        cleanup.note="""The following third party sites require that links to their hosted images
                        include publication-specific Web pages, which must be entered in the Image
                        field after a '|':"""
        required_domains = []
        for domain in domains:
                if domain[DOMAIN_EXPLICIT_LINK_REQUIRED] and (domain[DOMAIN_NAME] not in required_domains):
                        required_domains.append(domain[DOMAIN_NAME])
        for required_domain in required_domains:
                cleanup.note += '<br> %s' % required_domain
        cleanup.query = """select pub_id, pub_title from pubs, cleanup c
                   where c.report_type=231
                   and pubs.pub_id=c.record_id
                   and pub_frontimage not like '%|%' and ("""
        for domain in domains:
                if domain[DOMAIN_EXPLICIT_LINK_REQUIRED]:
                        cleanup.query += "pub_frontimage like '%%%s/%%' or " % domain[DOMAIN_NAME]
        cleanup.query = cleanup.query[:-4]
        cleanup.query += ') order by pub_title'
        cleanup.none = 'No Missing Required Web Pages for Cover Images found'
        cleanup.print_pub_table()

def function232():
        cleanup.query = """select award_id, award_title
                from awards
                where award_year not like '%-00-00'
                order by award_title"""
        cleanup.none = 'No invalid award years found'
        cleanup.print_award_table()

def function233():
        query = """select distinct p1.pub_id, p1.pub_title,
                   p2.pub_id, p2.pub_title, c.cleanup_id
                   from titles t, pub_content pc1, pub_content pc2,
                   pubs p1, pubs p2, cleanup c
                   where t.title_id = pc1.title_id
                   and pc1.pubc_id != pc2.pubc_id
                   and pc1.pub_id = p1.pub_id
                   and p1.pub_ptype = 'ebook'
                   and t.title_id = pc2.title_id
                   and p2.pub_ptype = 'ebook'
                   and pc2.pub_id = p2.pub_id
                   and YEAR(p1.pub_year) = YEAR(p2.pub_year)
                   and MONTH(p1.pub_year) = MONTH(p2.pub_year)
                   and (p1.pub_isbn is null or p2.pub_isbn is null or p1.pub_isbn = p2.pub_isbn)
                   and not (p1.pub_catalog is not null and p2.pub_catalog is not null and p1.pub_catalog != p2.pub_catalog)
                   and p1.pub_ctype = p2.pub_ctype
                   and p1.pub_title = p2.pub_title
                   and c.report_type = 233
                   and p1.pub_id = c.record_id
                   and c.resolved is null
                   group by t.title_id
                   order by p1.pub_title"""

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                PrintTableColumns(('', 'Publication 1', 'Publication 2', 'Ignore'))
                count = 1
                while record:
                        pub_id1 = record[0][0]
                        pub_title1 = record[0][1]
                        pub_id2 = record[0][2]
                        pub_title2 = record[0][3]
                        cleanup_id = record[0][4]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id1, pub_title1)
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id2, pub_title2)
                        if user.moderator:
                                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%d+1+233' % int(cleanup_id), 'Ignore')
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No potential duplicate e-book publications found.</h2>'

def function234():
        cleanup.query = """select p.pub_id, p.pub_title
                   from notes n, pubs p, cleanup c
                   where p.note_id = n.note_id
                   and n.note_note like '%picarta.pica.nl/%'
                   and c.report_type = 234
                   and p.pub_id = c.record_id
                   order by pub_title"""
        cleanup.none = 'No publications with direct De Nederlandse Bibliografie links in Notes'
        cleanup.print_pub_table()

def function235():
        cleanup.query = """select distinct p.pub_id, p.pub_title
                 from pubs p, identifiers i, cleanup c
                 where p.pub_id = i.pub_id
                 and i.identifier_type_id = 4
                 and i.identifier_value not regexp '^cb[[:digit:]]{8}[[:alnum:]]{1}$'
                 and c.report_type = 235
                 and p.pub_id = c.record_id
                 order by p.pub_title"""
        cleanup.none = 'No publications with invalid BNF identifiers'
        cleanup.print_pub_table()

def function236():
        cleanup.query = """select distinct p.pub_id, p.pub_title, c.cleanup_id
                 from pubs p, publishers pu, cleanup c
                 where p.publisher_id = pu.publisher_id
                 and (pu.publisher_name like '%SFBC%'
                      or pu.publisher_name = 'Science Fiction Book Club')
                 and p.pub_isbn is not NULL and p.pub_isbn != ""
                 and p.pub_catalog is NULL
                 and c.report_type = 236
                 and p.pub_id = c.record_id
                 and c.resolved is null
                 order by p.pub_title"""
        cleanup.none = 'No SFBC publications with an ISBN and no Catalog ID'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function237():
        nonModeratorMessage()
        cleanup.query = """select distinct p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, notes n, cleanup c
                where p.note_id = n.note_id
                and (n.note_note like '%LCCN:%' or n.note_note regexp 'LCCN [[:digit:]]{1}')
                and c.report_type = 237
                and p.pub_id = c.record_id
                and c.resolved is null
                order by p.pub_title"""
        cleanup.none = 'No Pubs with non-template Library of Congress numbers in notes'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function238():
        query = """select t1.title_id, t1.title_title, t1.title_language,
                t2.title_id, t2.title_title, t2.title_language
                from titles t1, titles t2, cleanup c
                where t1.title_parent = t2.title_id
                and t1.title_ttype not in ('COVERART','INTERIORART')
                and t1.title_language != t2.title_language
                and t1.title_language not in (17, 36, 22, 26, 16, 53, 59, 37)
                and not exists (select 1 from notes n where t1.note_id = n.note_id)
                and c.report_type = 238
                and t1.title_id = c.record_id
                order by t1.title_title"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                PrintTableColumns(('#', 'Translated Title', 'Tr. Language', 'Original Title', 'Orig. Language'))
                bgcolor = 1
                count = 1
                while record:
                        variant_id = record[0][0]
                        variant_title = record[0][1]
                        variant_language_id = record[0][2]
                        if variant_language_id:
                                variant_language = LANGUAGES[variant_language_id]
                        else:
                                variant_language = '&nbsp;'
                        parent_id = record[0][3]
                        parent_title = record[0][4]
                        parent_language_id = record[0][5]
                        if parent_language_id:
                                parent_language = LANGUAGES[parent_language_id]
                        else:
                                parent_language = '&nbsp;'

                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('title.cgi', variant_id, variant_title)
                        print '<td>%s</td>' % variant_language
                        print '<td>%s</td>' % ISFDBLink('title.cgi', parent_id, parent_title)
                        print '<td>%s</td>' % parent_language
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h3>No translations without notes found for less common languages</h3>'
        print '<p>'

def function239():
        query = """select t1.title_id, t1.title_title, l1.lang_name,
                t2.title_id, t2.title_title, l2.lang_name
                from titles t1, titles t2, notes n, cleanup c,
                languages l1, languages l2
                where t1.title_parent = t2.title_id
                and t1.title_ttype not in ('COVERART','INTERIORART')
                and t1.title_language != t2.title_language
                and t1.title_language = l1.lang_id
                and t2.title_language = l2.lang_id
                and t1.note_id = n.note_id
                and n.note_note not like '%{{Tr|%'
                and c.report_type = 239
                and t1.title_id = c.record_id
                order by l1.lang_name, t1.title_title"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                PrintTableColumns(('#', 'Translated Title', 'Trans. Language', 'Original Title', 'Orig. Language'))
                bgcolor = 1
                count = 1
                while record:
                        variant_id = record[0][0]
                        variant_title = record[0][1]
                        variant_language = record[0][2]
                        parent_id = record[0][3]
                        parent_title = record[0][4]
                        parent_language = record[0][5]

                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('title.cgi', variant_id, variant_title)
                        print '<td>%s</td>' % variant_language
                        print '<td>%s</td>' % ISFDBLink('title.cgi', parent_id, parent_title)
                        print '<td>%s</td>' % parent_language
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h3>No Translations without the Tr Template in Notes found.</h3>'
        print '<p>'

##        cleanup.none = 'No translations without the Tr template in notes found'
##        cleanup.print_title_table()

def function240():
        containers_grid(240)

def function241():
        containers_grid(241)

def function242():
        cleanup.query = """select distinct t1.title_id, t1.title_title
                from titles t1, titles t2, pub_content pc1, pub_content pc2, cleanup c
                where t1.title_id = pc1.title_id
                and pc1.pub_id = pc2.pub_id
                and pc2.title_id = t2.title_id
                and t1.title_ttype = 'CHAPBOOK'
                and t2.title_ttype = 'SHORTFICTION'
                and t1.title_jvn != t2.title_jvn
                and t1.title_id = c.record_id
                and c.report_type = 242
                order by t1.title_title"""
        cleanup.none = 'No CHAPBOOK/SHORTFICTION juvenile flag mismatches found'
        cleanup.print_title_table()

def function243():
        cleanup.query = """select p.pub_id, p.pub_title
                from pubs p, cleanup c
                where c.report_type = 243
                and p.pub_id = c.record_id
                and p.pub_frontimage like '%amazon.com/%'
                and not
                (REPLACE(p.pub_frontimage,'%2B','+') REGEXP '/images/[PIG]/[0-9A-Za-z+-]{10}[LS]?(\._CR[0-9]+,[0-9]+,[0-9]+,[0-9]+)?\.(gif|png|jpg)$'
                or
                p.pub_frontimage REGEXP '\.images(\-|\.)amazon\.com/images/G/0[1-3]/ciu/[0-9a-f]{2}/[0-9a-f]{2}/[0-9a-f]{22,24}\.L\.(gif|png|jpg)$'
                or
                p.pub_frontimage REGEXP '(m\.media-amazon|\.ssl-images-amazon)\.com/images/S/amzn-author-media-prod/[0-9a-z]{26}\.(gif|png|jpg)$')
                order by p.pub_title"""
        cleanup.none = 'No Publications with Images with Extra Formatting in Amazon URLs'
        cleanup.print_pub_table()

def function244():
        cleanup.note = """This cleanup report finds publications with non-numeric
                        External IDs for the following External ID Types:
                        <ul>
                        <li>Biblioman, BL, Bleiler Early Years, Bleiler Gernsback,
                        all COBISSes, COPAC (defunct), FantLab, Goodreads, JNB/JPNO,
                        KBR, Libris, LTF, NDL, NILF, NLA, OCLC/WorldCat, PORBASE, SF-Leihbuch
                        <li>NooSFere (optional leading hyphen allowed)
                        <li>DNB and PPN (optional trailing 'x'/'X' allowed)
                        <li>Reginald-1, Reginald-3 and Bleiler Supernatural (one optional trailing letter allowed)
                        <li>NDL (optional leading 'b' allowed)
                        </ul>"""
        cleanup.query = """select distinct p.pub_id, p.pub_title
                from pubs p, identifiers i, identifier_types it, cleanup c
                where c.report_type = 244
                and p.pub_id = c.record_id
                and p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and (
                (it.identifier_type_name in
                ('Biblioman', 'BL', 'Bleiler Early Years', 'Bleiler Gernsback',
                'COBISS.BG', 'COBISS.SR', 'COPAC (defunct)', 'FantLab',
                'Goodreads', 'JNB/JPNO', 'KBR', 'Libris', 'LTF', 'NILF', 'NLA',
                'OCLC/WorldCat', 'PORBASE', 'SF-Leihbuch')
                and i.identifier_value not regexp '^[[:digit:]]{1,30}$')
                or
                (it.identifier_type_name in ('DNB', 'PPN')
                and i.identifier_value not regexp '^[[:digit:]]{1,30}[Xx]{0,1}$')
                or
                (it.identifier_type_name = 'NDL'
                and i.identifier_value not regexp '^[b]{0,1}[[:digit:]]{1,30}$')
                or
                (it.identifier_type_name in ('Reginald-1', 'Reginald-3', 'Bleiler Supernatural')
                and i.identifier_value not regexp '^[[:digit:]]{1,6}[[:alpha:]]{0,1}$')
                or
                (it.identifier_type_name = 'NooSFere'
                and i.identifier_value not regexp '^[-]{0,1}[[:digit:]]{1,30}$')
                )
                order by p.pub_title"""
        cleanup.none = 'No Publications with Invalid External ID Format'
        cleanup.print_pub_table()

def function245():
        cleanup.note = """This cleanup report finds publications with ASIN IDs which do
                        not start with the letter B. It also finds Audible-ASIN IDs which
                        do not start with the letter B or use an ISBN-10 as the Audible-ASIN.
                        Moderators have the ability to ignore false positives."""
        cleanup.query = """select p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, identifiers i, identifier_types it, cleanup c
                where c.report_type = 245
                and c.resolved is NULL
                and p.pub_id = c.record_id
                and p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and (
                        (
                                it.identifier_type_name = 'ASIN'
                                and i.identifier_value not like 'B%'
                        )
                        or (
                                it.identifier_type_name = 'Audible-ASIN'
                                and i.identifier_value not like 'B%'
                                and i.identifier_value not regexp '^[[:digit:]]{9}[0-9Xx]{1}$'
                        )
                )
                order by p.pub_title"""
        cleanup.none = 'No Publications with Non-Standard ASINs or Audible-ASINs'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function246():
        cleanup.note = """This cleanup report finds publications with Barnes & Noble IDs
                        that do not start with '294'. Moderators
                        have the ability to ignore false positives."""
        cleanup.query = """select p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, identifiers i, identifier_types it, cleanup c
                where c.report_type = 246
                and c.resolved is NULL
                and p.pub_id = c.record_id
                and p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'BN'
                and i.identifier_value not like '294%'
                order by p.pub_title"""
        cleanup.none = 'No Publications with Non-Standard Barnes & Noble IDs'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function247():
        cleanup.note = """This cleanup report finds publications with LCCNs that
                        include anything aside from digits and hyphens.
                        Moderators have the ability to ignore false positives."""
        cleanup.query = """select p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, identifiers i, identifier_types it, cleanup c
                where c.report_type = 247
                and c.resolved is NULL
                and p.pub_id = c.record_id
                and p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'LCCN'
                and replace(i.identifier_value,'-','') not regexp '^[[:digit:]]{1,30}$'
                order by p.pub_title"""
        cleanup.none = 'No Publications with Invalid LCCNs'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function248():
        cleanup.note = """This cleanup report finds publications with Open Library IDs
                        that do not start with the letter 'O'."""
        cleanup.query = """select p.pub_id, p.pub_title
                from pubs p, identifiers i, identifier_types it, cleanup c
                where c.report_type = 248
                and p.pub_id = c.record_id
                and p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'Open Library'
                and i.identifier_value not like 'O%'
                order by p.pub_title"""
        cleanup.none = 'No Publications with Invalid Open Library IDs'
        cleanup.print_pub_table()

def function249():
        cleanup.note = """This cleanup report finds publications with BNB IDs
                        that start with the letters 'BLL'."""
        cleanup.query = """select p.pub_id, p.pub_title
                from pubs p, identifiers i, identifier_types it, cleanup c
                where c.report_type = 249
                and p.pub_id = c.record_id
                and p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'BNB'
                and i.identifier_value like 'BLL%'
                order by p.pub_title"""
        cleanup.none = 'No Publications with Invalid BNB IDs'
        cleanup.print_pub_table()

def function250():
        cleanup.query = """select p.pub_id, p.pub_title
                from pubs p, identifiers i, cleanup c
                where c.report_type = 250
                and p.pub_id = c.record_id
                and p.pub_id = i.pub_id
                and i.identifier_type_id = 12
                and replace(i.identifier_value,'-','') = replace(p.pub_isbn,'-','')
                order by p.pub_title"""
        cleanup.none = 'No Publications with OCLC IDs matching ISBNs'
        cleanup.print_pub_table()

def function251():
        cleanup.query = """select distinct p.pub_id, p.pub_title
            from pubs p, verification v, reference r, cleanup c
            where c.report_type = 251
            and p.pub_id = c.record_id
            and p.pub_id = v.pub_id
            and (p.pub_isbn is null or p.pub_isbn = '')
            and v.reference_id = r.reference_id
            and r.reference_label = 'OCLC/Worldcat'
            and v.ver_status = 1
            and not exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'OCLC/WorldCat')
            order by p.pub_title"""
        cleanup.none = 'No Publications with an OCLC Verification, no ISBN and no OCLC External ID'
        cleanup.print_pub_table()

def function252():
        query = """select distinct p.pub_id, p.pub_title, p.pub_isbn
            from pubs p, verification v, reference r, cleanup c
            where c.report_type = 252
            and p.pub_id = c.record_id
            and p.pub_id = v.pub_id
            and p.pub_isbn is not null
            and p.pub_isbn != ''
            and v.reference_id = r.reference_id
            and r.reference_label = 'OCLC/Worldcat'
            and v.ver_status = 1
            and not exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'OCLC/WorldCat')
            order by p.pub_title"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()
        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                PrintTableColumns(('#', 'Publication', 'ISBN link to OCLC'))
                count = 1
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        pub_isbn = record[0][2]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                        print '<td><a href="https://www.worldcat.org/isbn/%s">%s</a></td>' % (pub_isbn, pub_isbn)
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Publications with an OCLC Verification, an ISBN and no OCLC External ID.</h2>'

def function253():
        cleanup.query = """select distinct p.pub_id, p.pub_title
            from pubs p, notes n, cleanup c
            where c.report_type = 253
            and p.pub_id = c.record_id
            and p.note_id = n.note_id
            and (
                n.note_note like '%{{BREAK}}%Reginald1%'
                or n.note_note like '%{{BREAK}}%Reginald3%'
                or n.note_note like '%{{BREAK}}%Bleiler%Early Years%'
                or n.note_note like '%{{BREAK}}%Bleiler%Gernsback%'
                or n.note_note like '%{{BREAK}}%Bleiler%Guide to Supernatural%'
            )
            order by p.pub_title"""
        cleanup.none = 'No Publications with non-linking External IDs in Notes'
        cleanup.print_pub_table()

def function254():
        ids_in_notes(254, '%www.noosfere.org%', 'direct NooSFere links')

def function255():
        ids_in_notes(255, '%nilf.it/%', 'direct NILF links')

def function256():
        ids_in_notes(256, '%fantascienza.com/catalogo%', 'direct Fantascienza links')

def function257():
        query = """select s.series_id, s.series_title
                 from series s, cleanup c
                 where s.series_title regexp '&#'
                 and s.series_id = c.record_id
                 and c.report_type = 257
                 and not exists
                  (select 1 from trans_series ts
                  where ts.series_id = s.series_id)
                 order by s.series_title"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Series Name',))
                while record:
                        series_id = record[0][0]
                        series_name = record[0][1]
                        PrintSeriesRecord(series_id, series_name, bgcolor, count)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Series with non-Latin Characters in the Series Name without a Transliterated Name found</h2>'

def function258():
        nonLatinSeries(258)

def function259():
        nonLatinSeries(259)

def function260():
        nonLatinSeries(260)

def function261():
        nonLatinSeries(261)

def function262():
        nonLatinSeries(262)

def function263():
        reports = popularNonLatinLanguages('series')
        languages = []
        for report in reports:
                language_name = report[0]
                languages.append(language_name)
        languages_in_clause = list_to_in_clause(languages)
        query = """select distinct s.series_id, s.series_title, c.cleanup_id
                   from series s, titles t, languages l, cleanup c
                   where s.series_title not regexp '&#'
                   and s.series_id = t.series_id
                   and t.title_language = l.lang_id
                   and t.title_ttype != 'COVERART'
                   and t.title_ttype != 'INTERIORART'
                   and l.lang_name not in (%s)
                   and l.latin_script = 'No'
                   and s.series_id = c.record_id
                   and c.report_type = 263
                   and c.resolved is NULL
                   order by s.series_title
                   """ % languages_in_clause

        nonModeratorMessage()
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Series', 'Ignore'))
                while record:
                        series_id = record[0][0]
                        series_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintSeriesRecord(series_id, series_title, bgcolor, count, cleanup_id, 263)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No matching Series with Latin characters.</h2>'
        return

def function264():
        translated_report(264)

def function265():
        translated_report(265)

def function266():
        translated_report(266)

def function267():
        translated_report(267)

def function268():
        translated_report(268)

def function269():
        translated_report(269)

def function270():
        translated_report(270)

def function271():
        translated_report(271)

def function272():
        nonModeratorMessage()
        cleanup.query = """select p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, cleanup c, notes n
                where n.note_note not like '%{{Incomplete}}%'
                and
                (n.note_note like '%not complete%'
                or REPLACE(LOWER(n.note_note), 'incomplete number line', '') like '%incomplete%'
                or n.note_note like '%partial content%'
                or n.note_note like '%partial data%'
                or n.note_note like '%to be entered%'
                or n.note_note like '%to be added%'
                or n.note_note like '%more%added%'
                or n.note_note like '%not entered yet%')
                and p.note_id = n.note_id
                and c.report_type = 272
                and p.pub_id = c.record_id
                and c.resolved is null
                order by p.pub_title"""
        cleanup.none = 'No Publications with incomplete contents and no Incomplete Template'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function273():
        query = """select cleanup.record_id, notes.note_id,
                LENGTH(notes.note_note) - LENGTH(REPLACE(notes.note_note, '{', '')) openquote, 
                LENGTH(notes.note_note) - LENGTH(REPLACE(notes.note_note, '}', '')) closequote 
                from cleanup, notes
                where cleanup.record_id=notes.note_id
                and cleanup.report_type=273
                having openquote != closequote"""
        MismatchesInNotes(query, 'Mismatched Braces')

def function274():
        query = """select cleanup.record_id, notes.note_id
                from cleanup, notes where """
        replace_string = "REPLACE(lower(note_note), '{{break', '')"
        for template in SQLLoadAllTemplates():
                query += "REPLACE("
                replace_string += ", '{{%s', '')" % db.escape_string(template.lower())
        query += "%s like '%%{{%%'" % replace_string
        query += """ and cleanup.record_id=notes.note_id
                and cleanup.report_type=274"""
        MismatchesInNotes(query, 'References to Non-Existent Templates')

def function275():
        cleanup.query = """select t1.title_id, t1.title_title
                from titles t1, cleanup c
                where t1.title_ttype in ('ANTHOLOGY', 'CHAPBOOK', 'COLLECTION', 'COVERART', 'OMNIBUS', 'SERIAL')
                and t1.title_parent > 0
                and YEAR(t1.title_copyright) <
                        (select YEAR(min(p.pub_year))
                        from pubs p, pub_content pc
                        where pc.pub_id = p.pub_id
                        and pc.title_id = t1.title_id)
                and c.report_type = 275
                and t1.title_id = c.record_id
                order by t1.title_title"""
        cleanup.none = 'Title Dates Before First Publication Dates'
        cleanup.note = 'This report is currently limited to ANTHOLOGY, CHAPBOOK, COLLECTION, COVERART, OMNIBUS, and SERIAL <b>variant</b> titles'
        cleanup.print_title_table()

def function276():
        cleanup.query = """select t1.title_id, t1.title_title, c.cleanup_id
                from titles t1, titles t2, cleanup c
                where t1.title_parent = t2.title_id
                and t1.title_copyright < t2.title_copyright
                and t1.title_copyright != '0000-00-00'
                and t2.title_copyright != '0000-00-00'
                and month(t1.title_copyright) != '00'
                and month(t2.title_copyright) != '00'
                and t1.title_ttype != 'SERIAL'
                and c.report_type = 276
                and c.resolved IS NULL
                and t1.title_id = c.record_id
                order by t1.title_title"""
        cleanup.none = 'Variant Title Dates Before Canonical Title Dates'
        cleanup.ignore = 1
        cleanup.print_title_table()

def function277():
        containers_grid(277, 'incomplete_contents')

def function278():
        cleanup.invalid_title_types('ANTHOLOGY', ('CHAPBOOK','NONFICTION','OMNIBUS','EDITOR'))

def function279():
        cleanup.invalid_title_types('COLLECTION', ('ANTHOLOGY','CHAPBOOK','NONFICTION','OMNIBUS','EDITOR'))

def function280():
        cleanup.invalid_title_types('CHAPBOOK', ('ANTHOLOGY','COLLECTION','NONFICTION','OMNIBUS','EDITOR','NOVEL'))

def function281():
        cleanup.invalid_title_types('MAGAZINE', ('CHAPBOOK','NONFICTION','OMNIBUS'))

def function282():
        cleanup.invalid_title_types('FANZINE', ('ANTHOLOGY','CHAPBOOK','NONFICTION','OMNIBUS'))

def function283():
        cleanup.invalid_title_types('NONFICTION', ('ANTHOLOGY','COLLECTION','EDITOR','NOVEL','OMNIBUS','SERIAL','CHAPBOOK'))

def function284():
        cleanup.invalid_title_types('NOVEL', ('ANTHOLOGY','COLLECTION','EDITOR','NONFICTION','OMNIBUS','SERIAL','CHAPBOOK'))

def function285():
        cleanup.invalid_title_types('OMNIBUS', ('EDITOR','SERIAL','CHAPBOOK'))

def function286():
        cleanup.query = """select distinct t1.title_id, t1.title_title
                from titles t1, titles t2, cleanup c
                where t1.title_parent = t2.title_id
                and (
                        (t1.title_storylen != t2.title_storylen)
                        or
                        (t1.title_storylen is not NULL and t2.title_storylen is NULL)
                )
                and t1.title_id = c.record_id
                and c.report_type = 286
                order by t1.title_title"""
        cleanup.none = 'Variant Title Length Mismatches'
        cleanup.print_title_table()

def function287():
        cleanup.note = """This cleanup report finds publications with the following types of invalid Contents page values:
                <ul>
                <li>value contains "del"
                <li>value is a nonstandard special designation like 'fp'
                <li>a non-numeric value after the pipe character
                <li>the HTML pipe character &amp;#448 is used instead of the regular pipe character |
                <li>value contains the backtick (`) character
                </ul>
                """
        cleanup.query = """select distinct p.pub_id, p.pub_title
                from pubs p, pub_content pc, cleanup c
                where  (pc.pubc_page like '%del%'
                        or pc.pubc_page like '%&#448;%'
                        or pubc_page REGEXP '[\|]{1}[^0-9\.]'
                        or pubc_page REGEXP '[\|]{1}$'
                        or pubc_page like 'fp'
                        or pubc_page like 'fp|%'
                        or pubc_page like '%`%')
                and pc.pub_id = p.pub_id
                and c.record_id = p.pub_id
                and c.report_type = 287
                order by p.pub_title"""
        cleanup.none = 'Publications with Invalid Page Numbers'
        cleanup.print_pub_table()

def function288():
        sql_version = SQLMajorVersion()
        if sql_version < 6:
                regexp = """[^\]\[0-9ivxlcdm+ ,]"""
        else:
                regexp = """[^\\\\]\\\\[0-9ivxlcdm+ ,]"""
        query = """select distinct p.pub_id, p.pub_title, p.pub_pages
                from pubs p, pub_content pc, cleanup c
                where p.pub_pages REGEXP '%s'
                and pc.pub_id = p.pub_id
                and c.record_id = p.pub_id
                and c.report_type = 288
                order by p.pub_title""" % regexp

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication', 'Page Count'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        pub_pages = record[0][2]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                        print '<td>%s</td>' % pub_pages
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No Publications with Invalid Page Numbers</h2>'

def function289():
        cleanup.query = """select distinct p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, cleanup c
                where p.pub_ctype='CHAPBOOK'
                and
                        (select count(t.title_id)
                        from pub_content pc, titles t
                        where p.pub_id = pc.pub_id
                        and pc.title_id = t.title_id
                        and t.title_ttype in ('SHORTFICTION', 'POEM', 'SERIAL'))
                > 1
                and c.record_id = p.pub_id
                and c.report_type = 289
                and c.resolved IS NULL
                order by p.pub_title"""
        cleanup.none = 'CHAPBOOKs with Multiple Fiction Titles'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function290():
        cleanup.query = """select distinct t1.title_id, t1.title_title, c.cleanup_id
                from titles t1, title_relationships tr, titles t2, pubs p, pub_content pc, cleanup c
                where t1.title_ttype = 'NONFICTION'
                and t1.title_id = tr.title_id
                and t2.title_id = tr.review_id
                and t2.title_ttype = 'REVIEW'
                and t1.title_id = pc.title_id
                and p.pub_id = pc.pub_id
                and c.record_id = t1.title_id
                and c.report_type = 290
                and c.resolved IS NULL
                order by t1.title_title"""
        cleanup.none = 'NONFICTION Titles Which Exist Only Due to Reviews'
        cleanup.ignore = 1
        cleanup.note = 'Note: Reviews of ineligible non-fiction titles should be entered as ESSAYs.'
        cleanup.print_title_table()

def function291():
        cleanup.note = """This cleanup report finds publications with a non-audio
                format and the Narrator template in the Note field."""
        cleanup.query = """select distinct p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, notes n, cleanup c
                where p.note_id = n.note_id
                and note_note like '%{{narrator%'
                and p.pub_ptype not like '%audio%'
                and c.record_id = p.pub_id
                and c.report_type = 291
                and c.resolved IS NULL
                order by p.pub_title"""
        cleanup.none = 'No suspected invalid uses of the Narrator template'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function292():
        cleanup.query = """select distinct p.pub_id, p.pub_title
                from pubs p, notes n, cleanup c
                where p.pub_ptype like '%audio%'
                and p.note_id = n.note_id
                and n.note_note not like '%{{narrator%'
                and c.record_id = p.pub_id
                and c.report_type = 292
                order by p.pub_title"""
        cleanup.none = 'No audio books without the Narrator template'
        cleanup.print_pub_table()

def function293():
        cleanup.query = """select t.title_id, t.title_title, c.cleanup_id
                from titles t, cleanup c
                where binary t.title_title REGEXP "[^\:\.\!\;\/](%s)"
                and t.title_language = 17
                and c.record_id = t.title_id
                and c.report_type = 293
                and c.resolved IS NULL
                order by t.title_title""" % requiredLowerCase()
        cleanup.note = """This cleanup report finds English language title records with
                        capitalized words which should not be capitalized as per the ISFDB
                        data entry rules. The words are: %s""" % ", ".join(SESSION.english_lower_case)
        cleanup.ignore = 1
        cleanup.print_title_table()

def function294():
        cleanup.query = """select p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, cleanup c
                where binary p.pub_title REGEXP "[^\:\.\!\;\/](%s)"
                and exists (
                        select 1 from titles t, pub_content pc
                        where t.title_id = pc.title_id
                        and p.pub_id = pc.pub_id
                        and t.title_language = 17
                )
                and c.record_id = p.pub_id
                and c.report_type = 294
                and c.resolved IS NULL
                order by p.pub_title""" % requiredLowerCase()
        cleanup.note = """This cleanup report finds publications whose titles include
                        capitalized words which should not be capitalized as per
                        the ISFDB data entry rules. The report is curently limited
                        to publications with English language title records.
                        The words are: %s""" % ", ".join(SESSION.english_lower_case)
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function295():
        query = """select distinct p.pub_id, p.pub_title, p.pub_year, n.note_note
                from pubs p, notes n, cleanup c
                where p.note_id = n.note_id
                and n.note_note like '%{{WatchPrePub|%'
                and c.record_id = p.pub_id
                and c.report_type = 295
                order by p.pub_year, p.pub_title"""
        db.query(query)
        result = db.store_result()
        num = result.num_rows()
        if num > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Publication', 'Date', 'Questionable Field(s)'))
                while record:
                        pub_id = record[0][0]
                        pub_title = record[0][1]
                        pub_date = record[0][2]
                        note_text = record[0][3]
                        field_names = note_text.lower().split('{{watchprepub|')[1].split('}}')[0]
                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % int(count)
                        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
                        print '<td>%s</td>' % pub_date
                        print '<td>%s</td>' % field_names.capitalize()
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No publications with the WatchPrePub template</h2>'

def function296():
        cleanup.query = """select distinct p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, notes n, cleanup c
                where p.note_id = n.note_id
                and n.note_note like '%first printing%'
                and n.note_note not like '%apparent first printing%'
                and n.note_note not like '%assumed first printing%'
                and c.record_id = p.pub_id
                and c.report_type = 296
                and c.resolved IS NULL
                order by p.pub_title"""
        cleanup.none = 'No suspect publications with "First printing" in Notes'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function297():
        cleanup.query = """select distinct t.title_id, t.title_title, c.cleanup_id
                from titles t, cleanup c
                where title_title like '%(Part %'
                and title_ttype = 'SHORTFICTION'
                and c.record_id = t.title_id
                and c.report_type = 297
                and c.resolved IS NULL
                order by t.title_title"""
        cleanup.none = 'No suspect SHORTFICTION title records with "(Part " in the title field'
        cleanup.ignore = 1
        cleanup.print_title_table()

def function298():
        cleanup.note = """Title-based awards capture the title and the name of the title's
                        author(s) when a new award is created. However, the captured information
                        stored in the award record is never used: the software always uses the
                        current title and the current author(s) of the linked title record for
                        display and sorting purposes.<br>
                        In the past, some ISFDB Web pages used the captured title/author(s) data
                        instead, which allowed title-based awards to be adjusted to point to
                        other authors/titles. This cleanup report exists to help make sure that
                        all title-based awards are linked to the intended title."""
        cleanup.query = """select a.award_id, a.award_title, c.cleanup_id
                from awards a, cleanup c
                where exists(select 1 from title_awards ta1 where ta1.award_id = a.award_id) 
                and not exists( 
                select 1 from title_awards ta2, titles t, canonical_author ca, authors au 
                where ta2.award_id = a.award_id 
                and ta2.title_id = t.title_id 
                and t.title_id = ca.title_id 
                and ca.ca_status = 1 
                and ca.author_id = au.author_id 
                and ( 
                (au.author_canonical = a.award_author) 
                or (a.award_author like concat(au.author_canonical, '+%'))
                or (a.award_author like concat('%+', au.author_canonical))
                or (a.award_author like concat('%+', au.author_canonical, '+%'))
                ))
                and c.record_id = a.award_id
                and c.report_type = 298
                and c.resolved IS NULL
                order by a.award_title"""
        cleanup.none = 'No Suspect Title-Based Awards with a Different Stored Author Name'
        cleanup.ignore = 1
        cleanup.print_award_table()

def function299():
        cleanup.query = """select distinct p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, titles t, pub_content pc, languages l, cleanup c
                where p.pub_id = pc.pub_id
                and pc.title_id = t.title_id
                and t.title_language = l.lang_id
                and l.lang_name = 'Swedish'
                and p.pub_ctype not in ('MAGAZINE', 'FANZINE')
                and t.title_ttype not in ('INTERIORART')
                and not exists
                (select 1 from identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'Libris XL')
                and c.record_id = p.pub_id
                and c.report_type = 299
                and c.resolved IS NULL
                order by p.pub_title"""
        cleanup.none = 'No Publications with Swedish Titles with no Libris XL ID'
        cleanup.note = 'This reports excludes INTERIORART titles and MAGAZINE/FANZINE publications'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function300():
        cleanup.query = """select distinct p.pub_id, p.pub_title, c.cleanup_id
                from pubs p, titles t, pub_content pc, languages l, cleanup c
                where p.pub_id = pc.pub_id
                and pc.title_id = t.title_id
                and t.title_language = l.lang_id
                and l.lang_name = 'Swedish'
                and p.pub_ctype not in ('MAGAZINE', 'FANZINE')
                and t.title_ttype not in ('INTERIORART')
                and exists
                (select 1 from identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'Libris')
                and not exists
                (select 1 from identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'Libris XL')
                and c.record_id = p.pub_id
                and c.report_type = 300
                and c.resolved IS NULL
                order by p.pub_title"""
        cleanup.none = 'No Publications with Swedish Titles with a Libris ID and no Libris XL ID'
        cleanup.note = 'This reports excludes INTERIORART titles and MAGAZINE/FANZINE publications'
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function301():
        cleanup.query = """select r.title_id, r.title_title, c.cleanup_id
                from titles r, title_relationships tr, titles t, cleanup c
                where r.title_ttype = 'REVIEW'
                and r.title_id = tr.review_id
                and tr.title_id = t.title_id
                and r.title_language != t.title_language
                and c.record_id = r.title_id
                and c.report_type = 301
                and c.resolved IS NULL
                order by r.title_title"""
        cleanup.note = """REVIEWs are typically written in the same language as the title
                        that they review and should be linked to the correct translated
                        variant title. If a REVIEW title reviews a title written in a
                        different language, a Note should be added to the review record.
                        Moderators should then 'Ignore' the REVIEW in the body of the
                        report below."""
        cleanup.none = "No Reviews Whose Language Doesn't Match the Language of the Reviewed Title"
        cleanup.ignore = 1
        cleanup.print_title_table()

def function302():
        cleanup.note = """This report identifies author names with unrecognized suffixes.
                          Curently recognized suffixes are: %s If you would like
                          to propose adding another suffix to the list, please post
                          your request on the Community Portal.""" % ', '.join(SESSION.recognized_suffixes)
        
        cleanup.query = """select a.author_id, a.author_canonical, c.cleanup_id
                   from cleanup c, authors a
                   where c.record_id = a.author_id
                   and c.report_type = 302
                   and c.resolved IS NULL
                   and """

        subquery = ''
        for suffix in SESSION.recognized_suffixes:
                if not subquery:
                        subquery = """replace(author_canonical, ', %s', '')""" % suffix
                else:
                        subquery = """replace(%s, ', %s', '')""" % (subquery, suffix)

        cleanup.query += subquery
        cleanup.query += """ like '%,%'"""

        cleanup.ignore = 1
        cleanup.none = 'No Author Names with an Unrecognized Suffix found'
        cleanup.print_author_table()

def function303():
        cleanup.query = """select t.title_id, t.title_title
                        from titles t, authors a, canonical_author ca, cleanup c
                        where t.title_id = ca.title_id
                        and t.title_ttype = 'COVERART'
                        and ca.author_id = a.author_id
                        and ca.ca_status = 1
                        and a.author_canonical = 'uncredited'
                        and c.record_id = t.title_id
                        and c.report_type = 303
                        order by t.title_title"""
        cleanup.none = "No COVERART titles with 'uncredited' Authors"
        cleanup.print_title_table()

def function304():
        cleanup.query = """select p.pub_id, p.pub_title
                        from pubs p, notes n, cleanup c
                        where p.note_id = n.note_id 
                        and n.note_note like '%COBISS%' 
                        and n.note_note not like '%{{COBISS%' 
                        and not exists
                        (select 1 from identifiers i, identifier_types it 
                        where p.pub_id = i.pub_id 
                        and i.identifier_type_id = it.identifier_type_id 
                        and it.identifier_type_name like '%COBISS%')
                        and c.record_id = p.pub_id
                        and c.report_type = 304
                        order by p.pub_title
                        """
        cleanup.none = "No publications with COBISS references in notes without a template/External ID"
        cleanup.print_pub_table()

def function305():
        cleanup.query = """select p.pub_id, p.pub_title
                        from pubs p, notes n, cleanup c
                        where p.note_id = n.note_id 
                        and n.note_note like '%Biblioman%' 
                        and n.note_note not like '%{{Biblioman|%' 
                        and not exists
                        (select 1 from identifiers i, identifier_types it 
                        where p.pub_id = i.pub_id 
                        and i.identifier_type_id = it.identifier_type_id 
                        and it.identifier_type_name = 'Biblioman')
                        and c.record_id = p.pub_id
                        and c.report_type = 305
                        order by p.pub_title
                        """
        cleanup.none = "No publications with Biblioman references in notes without a template/External ID"
        cleanup.print_pub_table()

def function306():
        cleanup.query = """select p.pub_id, p.pub_title
                        from pub_authors pa, pubs p, cleanup c
                        where p.pub_id = pa.pub_id
                        and c.record_id = pa.pub_id
                        and c.report_type = 306
                        group by pa.author_id, pa.pub_id
                        having count(pa.pub_id) > 1
                        order by p.pub_title
                        """
        cleanup.none = "No publications with Duplicate Authors"
        cleanup.print_pub_table()

def function307():
        cleanup.query = """select a.award_id, a.award_title, c.cleanup_id
                        from awards a, titles t, title_awards ta, cleanup c
                        where a.award_id = ta.award_id
                        and ta.title_id = t.title_id
                        and t.title_ttype in ('CHAPBOOK')
                        and c.record_id = a.award_id
                        and c.report_type = 307
                        and c.resolved IS NULL
                        order by a.award_title
                        """
        cleanup.none = 'No Awards Linked to to Uncommon Title Types'
        cleanup.note = 'This report is currently limited to CHAPBOOK titles'
        cleanup.ignore = 1
        cleanup.print_award_table()

def function308():
        cleanup.books_with_trans_and_no_pubs('English')

def function309():
        cleanup.books_with_trans_and_no_pubs('French')

def function310():
        cleanup.books_with_trans_and_no_pubs('German')

def function311():
        cleanup.books_with_trans_and_no_pubs('Italian')

def function312():
        cleanup.books_with_trans_and_no_pubs('Japanese')

def function313():
        cleanup.books_with_trans_and_no_pubs('Russian')

def function314():
        cleanup.books_with_trans_and_no_pubs('Spanish')

def function315():
        cleanup.other_books_with_trans_and_no_pubs('long')

def function316():
        cleanup.books_with_trans_and_no_pubs('English', 'short')

def function317():
        cleanup.books_with_trans_and_no_pubs('French', 'short')

def function318():
        cleanup.books_with_trans_and_no_pubs('German', 'short')

def function319():
        cleanup.books_with_trans_and_no_pubs('Italian', 'short')

def function320():
        cleanup.books_with_trans_and_no_pubs('Japanese', 'short')

def function321():
        cleanup.books_with_trans_and_no_pubs('Russian', 'short')

def function322():
        cleanup.books_with_trans_and_no_pubs('Spanish', 'short')

def function323():
        cleanup.other_books_with_trans_and_no_pubs('short')

def function324():
        cleanup.query = """select p.pub_id, p.pub_title
                from pubs p, cleanup c
                where (p.pub_isbn is NULL or p.pub_isbn = '')
                and c.record_id = p.pub_id
                and c.report_type = 324
                and exists
                        (select 1
                        from identifiers i, identifier_types it
                        where p.pub_id = i.pub_id
                        and i.identifier_type_id = it.identifier_type_id
                        and it.identifier_type_name = 'Audible-ASIN'
                        and i.identifier_value regexp '^[[:digit:]]{9}[0-9Xx]{1}$'
                        )
                order by p.pub_title
                """
        cleanup.none = "No publications without an ISBN and with an Audible ASIN which is an ISBN-10"
        cleanup.print_pub_table()

def function325():
        cleanup.query = """select p.pub_id, p.pub_title
                from pubs p, cleanup c
                where p.pub_ptype = 'digital audio download'
                and (p.pub_price like '$%' or p.pub_price is NULL or p.pub_price = '')
                and c.record_id = p.pub_id
                and c.report_type = 325
                and exists
                        (select 1
                        from identifiers i, identifier_types it
                        where p.pub_id = i.pub_id
                        and i.identifier_type_id = it.identifier_type_id
                        and it.identifier_type_name = 'ASIN'
                        )
                and not exists
                        (select 1
                        from identifiers i, identifier_types it
                        where p.pub_id = i.pub_id
                        and i.identifier_type_id = it.identifier_type_id
                        and it.identifier_type_name = 'Audible-ASIN'
                        )
                order by p.pub_title
                """
        cleanup.none = "No digital audio download pubs with a regular ASIN and no Audible ASIN"
        cleanup.note = "This report is currently limited to publications with a US price or no specified price"
        cleanup.print_pub_table()

def function326():
        cleanup.query = """select p.pub_id, p.pub_title
                from pubs p, identifiers i, identifier_types it, cleanup c
                where p.pub_ptype != 'digital audio download'
                and p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'Audible-ASIN'
                and c.record_id = p.pub_id
                and c.report_type = 326
                order by p.pub_title"""
        cleanup.none = "No pubs with an Audible ASIN and a non-Audible format"
        cleanup.print_pub_table()

def function327():
        query = """select author_id, author_canonical, author_image
                from authors, cleanup 
                where authors.author_image != ''
                and authors.author_image is not null 
                and authors.author_id = cleanup.record_id
                and cleanup.report_type = 327"""
        domains = SQLLoadRecognizedDomains()
        for domain in domains:
                # Skip domains that are "recognized", but we don't have permission to link to
                if not domain[DOMAIN_LINKING_ALLOWED]:
                        continue
                query += " and SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(author_image,'//',2),'//',-1),'/',1) not like '%%%s'" % domain[DOMAIN_NAME]
        # Check for URL segments which must be present in the URL
        subquery = ''
        for domain in domains:
                if not domain[DOMAIN_REQUIRED_SEGMENT]:
                        continue
                if subquery:
                        subquery += ' or'
                subquery += """ (SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(authors.author_image,'//',2),'//',-1),'/',1)
                                like '%%%s' and authors.author_image not like '%%%s%%')""" % (domain[DOMAIN_NAME], domain[DOMAIN_REQUIRED_SEGMENT])
        query += """ UNION select author_id, author_canonical, author_image
                from authors, cleanup
                where authors.author_image != ''
                and authors.author_image is not null
                and authors.author_id = cleanup.record_id
                and cleanup.report_type = 327
                and SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(author_image,'//',2),'//',-1),'/',1) not like '%%sf-encyclopedia.uk'
                and SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(author_image,'//',2),'//',-1),'/',1) not like '%%sf-encyclopedia.com'
                and (%s)""" % subquery
        query += ' order by author_canonical'
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        if not record:
                print '<h2>No records found</h2>'
                return

        bgcolor = 1
        PrintTableColumns(('Author', 'URL'))
        while record:
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%s</td>' % ISFDBLink('ea.cgi', record[0][0], record[0][1])
                print '<td><a href="%s">%s</a></td>' % (ISFDBText(record[0][2]), ISFDBText(record[0][2]))
                print '</tr>'
                bgcolor ^= 1
                record = result.fetch_row()
        print '</table>'

def function328():
        cleanup.query = """select t.title_id, t.title_title
                        from titles t, cleanup c
                        where (title_synopsis is not null and title_synopsis != 0)
                        and title_parent != 0
                        and c.record_id = t.title_id
                        and c.report_type = 328
                        order by t.title_title"""
        cleanup.none = "No variant titles with synopsis data"
        cleanup.print_title_table()

def function329():
        cleanup.query = """select distinct t.title_id, t.title_title
                        from titles t, pubs p, pub_content pc, notes n_t, notes n_p, cleanup c
                        where t.title_id=pc.title_id
                        and p.pub_id=pc.pub_id
                        and t.note_id=n_t.note_id
                        and n_t.note_note not like '%{{Tr|%'
                        and p.note_id=n_p.note_id
                        and n_p.note_note like '%{{Tr|%'
                        and t.title_ttype=p.pub_ctype
                        and c.record_id = t.title_id
                        and c.report_type = 329
                        order by t.title_title"""
        cleanup.none = "No Translations with Tr template in Pub Notes and no Tr template in Title notes"
        cleanup.print_title_table()

def function330():
        cleanup.query = """select pub_id, p.pub_title
                from pubs p, cleanup c
                where p.pub_isbn is not null
                and p.pub_isbn != ''
                and p.pub_year != '0000-00-00'
                and p.pub_year < '1967-00-00'
                and c.record_id = p.pub_id
                and c.report_type = 330
                order by p.pub_title"""
        cleanup.none = "No pre-1967 publications with an ISBN"
        cleanup.print_pub_table()

def function331():
        cleanup.query = """select pub_id, p.pub_title
                from pubs p, cleanup c, notes n
                where c.record_id = p.pub_id
                and c.report_type = 331
                and p.note_id = n.note_id
                and n.note_note regexp 'pv[[:blank:]]{0,}[[:digit:]]{1}'
                order by p.pub_title"""
        cleanup.none = "No publications with PV# in Notes"
        cleanup.print_pub_table()

def function332():
        cleanup.query = """select pub_id, p.pub_title, c.cleanup_id
                from pubs p, cleanup c
                where p.pub_isbn like '979%'
                and p.pub_year != '0000-00-00'
                and p.pub_year < '2020-00-00'
                and c.record_id = p.pub_id
                and c.report_type = 332
                and c.resolved is NULL
                order by p.pub_title"""
        cleanup.none = "No outstanding pre-2020 publications with a 979 ISBN-13"
        cleanup.ignore = 1
        cleanup.print_pub_table()

def function333():
        cleanup.query = """select distinct t.title_id, t.title_title, c.cleanup_id
                from titles t, cleanup c
                where t.title_ttype='INTERIORART'
                and (t.title_title like '%[1]%' or t.title_title like '%(1)%')
                and c.record_id = t.title_id
                and c.report_type = 333
                and c.resolved is NULL
                order by t.title_title"""
        cleanup.none = "Interior art titles with embedded [1] or (1)"
        cleanup.ignore = 1
        cleanup.print_title_table()

def requiredLowerCase():
        clause = ''
        for word in SESSION.english_lower_case:
                clause += ' %s |' % word.capitalize()
        clause = clause[:-1]
        return clause

def translated_report(report_id):
        language_id = ISFDBtranslatedReports()[report_id]
        query = """select t1.title_id, t1.title_title,
                t2.title_id, t2.title_title, t2.title_language
                from titles t1, titles t2, cleanup c
                where t1.title_parent = t2.title_id
                and t1.title_ttype not in ('COVERART','INTERIORART')
                and t1.title_language != t2.title_language
                and t1.title_language = %d
                and not exists (select 1 from notes n where t1.note_id = n.note_id)
                and c.report_type = %d
                and t1.title_id = c.record_id
                order by t1.title_title""" % (language_id, report_id)
        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                record = result.fetch_row()
                PrintTableColumns(('#', 'Translated Title', 'Original Title', 'Orig. Language'))
                bgcolor = 1
                count = 1
                while record:
                        variant_id = record[0][0]
                        variant_title = record[0][1]
                        parent_id = record[0][2]
                        parent_title = record[0][3]
                        parent_language_id = record[0][4]
                        if parent_language_id:
                                parent_language = LANGUAGES[parent_language_id]
                        else:
                                parent_language = '&nbsp;'

                        if bgcolor:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'

                        print '<td>%d</td>' % count
                        print '<td>%s</td>' % ISFDBLink('title.cgi', variant_id, variant_title)
                        print '<td>%s</td>' % ISFDBLink('title.cgi', parent_id, parent_title)
                        print '<td>%s</td>' % parent_language
                        print '</tr>'
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h3>No %s translations without notes found.</h3>' % LANGUAGES[language_id]
        print '<p>'

def nonLatinSeries(report_id):
        reports = popularNonLatinLanguages('series')
        for report in reports:
                if report_id == report[1]:
                        language = report[0]
                        break

        query = """select distinct s.series_id, s.series_title, c.cleanup_id
                   from series s, titles t, languages l, cleanup c
                   where s.series_title not regexp '&#'
                   and s.series_id = t.series_id
                   and t.title_language = l.lang_id
                   and l.lang_name = '%s'
                   and s.series_id = c.record_id
                   and c.report_type = %d
                   and c.resolved is NULL
                   order by s.series_title
                   """ % (language, report_id)
        nonLatinSeriesDisplay(report_id, query, language)

def nonLatinSeriesDisplay(report_id, query, language):
        nonModeratorMessage()
        db.query(query)
        result = db.store_result()

        if result.num_rows() > 0:
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                PrintTableColumns(('', 'Series', 'Ignore'))
                while record:
                        series_id = record[0][0]
                        series_title = record[0][1]
                        cleanup_id = record[0][2]
                        PrintSeriesRecord(series_id, series_title, bgcolor, count, cleanup_id, report_id)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print '</table>'
        else:
                print '<h2>No %s Series with Latin characters.</h2>' % language
        return

def containers_grid(report_id, script = 'empty_containers'):
        anchor = '<a href="%s:/%s/edit/%s.cgi' % (PROTOCOL, HTFAKE, script)
        years = {}
        decades = {}
        months = {}
        unknown = 0
        query = """select count(*), record_id_2
                   from cleanup
                   where report_type = %d
                   and resolved IS NULL
                   group by record_id_2""" % report_id
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
                count = record[0][0]
                month = record[0][1]
                if not month:
                        unknown += count
                else:
                        year = month/100
                        decade = year/10
                        years[year] = years.get(year, 0) + count
                        decades[decade] = decades.get(decade, 0) + count
                        months[month] = months.get(month, 0) + count
                record = result.fetch_row()

        print '<h3 class="centered">Since 2000: By Year and Month</h3>'
        print '<table class="seriesgrid">'
        print '<tr class="table1">'
        print '<th>Year</th>'
        print '<th colspan="13">Month</th>'
        print '</tr>'
        # Get the next year based on system time
        next_year = localtime()[0] + 1
        bgcolor = 1
        for year in range(next_year, 1999, -1):
                if year not in years:
                        continue
                print '<tr class="table%d">' % (bgcolor+1)
                print '<td>%s?year+%d+%d">%d (%d)</a></td>' % (anchor, year, report_id, year, years[year])
                for number in range(0,13):
                        month = year*100+number
                        if number in ISFDBmonthmap:
                                month_name = ISFDBmonthmap[number]
                        else:
                                month_name = 'None'
                        print '<td>'
                        # No links for months with no empty containers
                        if month not in months:
                                print month_name
                        else:
                                print '%s?month+%d+%d">%s (%d)</a>' % (anchor, month, report_id, month_name, months[month])
                        print '</td>'
                print '</tr>'
                bgcolor ^= 1
        print '</table>'
        print '<p>'
        print '<b>Unknown Year:</b> %s?unknown+0+%d">%d</a>' % (anchor, report_id, unknown)
        
        print '<h3 class="centered">Pre-2000: By Year and Decade</h3>'
        print '<table class="seriesgrid">'
        print '<tr class="table1">'
        print '<th>Decade</th>'
        print '<th colspan="10">Years</th>'
        print '</tr>'
        bgcolor = 1
        # Display all pre-21st century decades in reverse chronological order
        for decade in sorted(decades, reverse=1):
                if decade > 199:
                        continue
                print '<tr class="table%d">' % (bgcolor+1)
                print '<td>%s?decade+%d+%d">%d0s (%d)</a></td>' % (anchor, decade, report_id, decade, decades[decade])
                for year in range(decade*10, decade*10+10):
                        print '<td>'
                        # No links for years without empty containers
                        if year not in years:
                                print year
                        else:
                                print '%s?year+%d+%d">%d (%d)</a>' % (anchor, year, report_id, year, years[year])
                        print '</td>'
                print '</tr>'
                bgcolor ^= 1
        print '</table>'

def function9999():
        nonModeratorMessage()
        query = """select c.record_id, a1.author_canonical,
                c.record_id_2, a2.author_canonical, c.cleanup_id
                from cleanup c, authors a1, authors a2
                where report_type=9999 and resolved IS NULL
                and c.record_id = a1.author_id and c.record_id_2 = a2.author_id
                and not exists(select 1 from pseudonyms p
                where c.record_id=p.pseudonym)
                and not exists(select 1 from pseudonyms p
                where c.record_id_2=p.pseudonym)
                order by a1.author_canonical"""
        db.query(query)
        result = db.store_result()

        if not result.num_rows():
                print "<h2>No Suspected Duplicate Authors</h2>"
                return

        record = result.fetch_row()
        bgcolor = 1
        count = 1
        PrintTableColumns(('', 'Author 1', 'Author 2', 'Ignore'))
        while record:
                author_id_1 = record[0][0]
                author_name_1 = record[0][1]
                author_id_2 = record[0][2]
                author_name_2 = record[0][3]
                cleanup_id = record[0][4]
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'
                print '<td>%d</td>' % count
                print '<td>%s</td>' % ISFDBLink('ea.cgi', author_id_1, author_name_1)
                print '<td>%s</td>' % ISFDBLink('ea.cgi', author_id_2, author_name_2)
                if cleanup_id and user.moderator:
                        print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi', '%d+1+9999' % int(cleanup_id), 'Ignore')
                print '</tr>'
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print '</table>'

def Nightly_html(report_id, table, note_field, record_id_field, record_title_field, cgi_script):
        ui = isfdbUI()

        if report_id == 217:
                query = """select t.%s, t.%s, t.%s
                           from %s t, cleanup c where %s
                           and t.%s = c.record_id
                           and c.report_type = %s
                           """ % (record_id_field, record_title_field, note_field, table,
                                  ui.badHtmlClause('t', '%s' % note_field), record_id_field, report_id)
        else:
                query = """select t.%s, t.%s, n.note_note
                           from %s t, notes n, cleanup c where %s
                           and t.%s = n.note_id
                           and t.%s = c.record_id
                           and c.report_type = %s
                        """ % (record_id_field, record_title_field, table, ui.badHtmlClause('n', 'note_note'),
                               note_field, record_id_field, report_id)
        db.query(query)
        result = db.store_result()

        if not result.num_rows():
                print "<h2>No invalid HTML for records of this type.</h2>"
                return

        record = result.fetch_row()
        bgcolor = 1
        count = 1
        PrintTableColumns(('', 'Record', 'Invalid HTML starts close to'))
        while record:
                record_id = record[0][0]
                record_name = record[0][1]
                note = record[0][2]
                for tag in ui.valid_tags:
                        note = string.replace(note, tag.lower(), '')
                        note = string.replace(note, tag.upper(), '')
                problem_part = note
                if '<' in note:
                        problem_part = cgi.escape(note.split('<')[1][:20])
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'
                print '<td>%d</td>' % count
                print '<td>%s</td>' % ISFDBLink('%s.cgi' % cgi_script, record_id, record_name)
                print '<td>&lt;%s</td>' % problem_part
                print '</tr>'
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print '</table>'


def PrintPublicationRecord(pub_id, pub_title, bgcolor, count, cleanup_id = 0, report_id = 0, mode = 1):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%d</td>' % int(count)
        print '<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title)
        if cleanup_id and user.moderator:
                message = {0: 'Resolve', 1: 'Ignore'}
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                '%d+%d+%d' % (int(cleanup_id), int(mode), int(report_id)),
                                                '%s this publication' % message[mode])
        print '</tr>'

def PrintTitleRecord(title_id, title_title, bgcolor, count, cleanup_id = 0, report_id = 0, mode = 1):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%d</td>' % int(count)
        print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title)
        if cleanup_id and user.moderator:
                message = {0: 'Resolve', 1: 'Ignore'}
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                '%d+%d+%d' % (int(cleanup_id), int(mode), int(report_id)),
                                                '%s this title' % message[mode])
        print '</tr>'

def PrintPublisherRecord(pub_id, pub_name, bgcolor, count, cleanup_id = 0, report_id = 0, mode = 1):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%d</td>' % count
        print '<td>%s</td>' % ISFDBLink('publisher.cgi', pub_id, pub_name)
        if cleanup_id and user.moderator:
                message = {0: 'Resolve', 1: 'Ignore'}
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                '%d+%d+%d' % (int(cleanup_id), int(mode), int(report_id)),
                                                '%s this publisher ' % message[mode])
        print '</tr>'
        print '<p>'

def PrintPubSeriesRecord(pub_series_id, pub_series_name, bgcolor, count, cleanup_id = 0, report_id = 0, mode = 1):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%d</td>' % count
        print '<td>%s</td>' % ISFDBLink('pubseries.cgi', pub_series_id, pub_series_name)
        if cleanup_id and user.moderator:
                message = {0: 'Resolve', 1: 'Ignore'}
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                '%d+%d+%d' % (int(cleanup_id), int(mode), int(report_id)),
                                                '%s this publication series' % message[mode])
        print '</tr>'
        print '<p>'

def PrintSeriesRecord(series_id, series_name, bgcolor, count, cleanup_id = 0, report_id = 0, mode = 1):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%d</td>' % count
        print '<td>%s</td>' % ISFDBLink("pe.cgi", series_id, series_name)
        if cleanup_id and user.moderator:
                message = {0: 'Resolve', 1: 'Ignore'}
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                '%d+%d+%d' % (int(cleanup_id), int(mode), int(report_id)),
                                                '%s this series' % message[mode])
        print '</tr>'

def PrintAwardTypeRecord(award_type_id, award_type_name, bgcolor, count, cleanup_id = 0, report_id = 0, mode = 1):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%d</td>' % count
        print '<td>%s</td>' % ISFDBLink('awardtype.cgi', award_type_id, award_type_name)
        if cleanup_id and user.moderator:
                message = {0: 'Resolve', 1: 'Ignore'}
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                '%d+%d+%d' % (int(cleanup_id), int(mode), int(report_id)),
                                                '%s this award type' % message[mode])
        print '</tr>'

def PrintAwardCatRecord(award_cat_id, award_cat_name, bgcolor, count, cleanup_id = 0, report_id = 0, mode = 1):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%d</td>' % count
        print '<td>%s</td>' % ISFDBLink('award_category.cgi', award_cat_id, award_cat_name)
        if cleanup_id and user.moderator:
                message = {0: 'Resolve', 1: 'Ignore'}
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                '%d+%d+%d' % (int(cleanup_id), int(mode), int(report_id)),
                                                '%s this award category' % message[mode])
        print '</tr>'

def PrintAwardRecord(award_id, award_title, bgcolor, count, cleanup_id = 0, report_id = 0, mode = 1):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%d</td>' % count
        print '<td>%s</td>' % ISFDBLink('award_details.cgi', award_id, award_title)
        if cleanup_id and user.moderator:
                message = {0: 'Resolve', 1: 'Ignore'}
                print '<td>%s</td>' % ISFDBLink('mod/resolve_cleanup.cgi',
                                                '%d+%d+%d' % (int(cleanup_id), int(mode), int(report_id)),
                                                '%s this award' % message[mode])
        print '</tr>'

def PrintTitlesWithoutLanguage(result):
        PrintTableColumns(('', 'Title Type', 'Author', 'Title'))
        record = result.fetch_row()
        bgcolor = 1
        count = 1
        while record:
                title_ttype = record[0][0]
                title_id = record[0][1]
                title_name = record[0][2]
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'

                print '<td>%s</td>' % count
                print '<td>%s</td>' % title_ttype
                authors = SQLTitleBriefAuthorRecords(title_id)
                print '<td>'
                for author in authors:
                        print ISFDBLink('ea.cgi', author[0], author[1])
                print '</td>'
                print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_name)
                print '</tr>'
                bgcolor ^= 1
                count += 1
                record = result.fetch_row()
        print '</table>'

        
if __name__ == '__main__':

        # Retrieve all supported reports
        (reports, sections, non_moderator, weeklies, monthlies) = reportsDict()

        type_id = SESSION.Parameter(0, 'int')
        if type_id not in reports:
                SESSION.DisplayError('Cleanup Report Does Not Exist')
        # Determine the name of the function to be called for this report
        function = getattr(sys.modules[__name__], 'function' + str(type_id))

        user = User()
        user.load()
        user.load_moderator_flag()
        if not user.moderator and (type_id not in non_moderator):
                SESSION.DisplayError('Only moderators can access the specified cleanup report')

        PrintPreSearch(reports[type_id])
        PrintNavBar('edit/cleanup_report.cgi', type_id)

        cleanup = Cleanup()
        cleanup.report_id = type_id
        if type_id in weeklies:
                print '<h3>This report is regenerated once a week</h3>'
        elif type_id in monthlies:
                print '<h3>This report is regenerated once a month</h3>'
        else:
                print '<h3>This report is regenerated every night</h3>'
        function()

        PrintPostSearch(0, 0, 0, 0, 0, 0)
        
