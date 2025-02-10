#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 930 $
#     Date: $Date: 2022-06-08 15:54:08 -0400 (Wed, 08 Jun 2022) $

import cgi
import sys
import string
import MySQLdb
from isfdb import *
from common import *
from SQLparsing import *
from library import *
from isbn import *
from advSearchClass import AdvancedSearch

class AdvancedSearchResults(AdvancedSearch):
        def __init__(self):
                self.action = 'query'
                self.conjunction = 'AND'
                self.dbases = []
                self.form = {}
                self.id_field = ''
                self.joins = set()
                self.num = 0
                self.query = ''
                self.records = []
                self.search_type = ''
                self.selection_criteria = set()
                self.sort = ''
                self.sort_name = ''
                self.start = 0
                self.term_list = []
                self.terms = ''
                self.wildcards = '%*_'

                user = User()
                user.load()
                user.load_moderator_flag()
                self.user = user
                
                self.define_criteria()

        def results(self):
                self.parse_parameters()
                PrintHeader("Advanced %s Search" % ISFDBText(self.search_type))
                PrintNavbar('adv_search_results', 0, 0, 0, 0)
                if not self.user.id:
                        print '<h3>For performance reasons, Advanced Searches are currently restricted to registered users.</h3>'
                else:
                        self.set_search_type()
                        self.process_terms()
                        self.validate_conjunction()
                        self.validate_sort()
                        self.expand_sort()
                        self.print_selection_criteria()
                        self.print_merge_form()
                        self.make_terms()
                        self.execute_query()
                        self.print_results()
                        self.print_page_buttons()
                PrintTrailer('adv_search_results', 0, 0)

        def display_error(self, message, display_header = 0):
                if display_header:
                        PrintHeader('Advanced Search')
                        PrintNavbar('adv_search_results', 0, 0, 0, 0)
                self.display_message('Error: %s' % message)

        def display_message(self, message):
                print '<h2>%s</h2>' % ISFDBText(message)
                PrintTrailer('adv_search_results', 0, 0)
                sys.exit(0)

        def parse_parameters(self):
                sys.stderr = sys.stdout
                raw_form = cgi.FieldStorage()

                try:
                        # Strip leading and trailing spaces if the user's preferences call for it;
                        # move the parameters to a new dictionary, 'form'
                        for key in raw_form.keys():
                                value = raw_form[key].value
                                if not self.user.keep_spaces_in_searches:
                                        value = string.strip(value)
                                if value:
                                        self.form[key] = value

                        self.start = int(self.form.get('START', 0))
                        if self.start > 30000:
                                self.display_error('Advanced Search Is Currently Limited to 300 pages or 30,000 records', 1)
                        self.search_type = self.form['TYPE']
                        self.sort = self.format_entry(self.form['ORDERBY'])
                        self.action = self.form.get('ACTION', 'query')
                        if self.action not in ('query', 'count'):
                                raise
                        if 'C' in self.form:
                                self.conjunction = self.form.get('C')
                        # Legacy queries send CONJUNCTION_1 instead of C
                        elif 'CONJUNCTION_1' in self.form:
                                self.conjunction = self.form.get('CONJUNCTION_1')
                except:
                        self.display_error('Invalid Advanced Search Parameters', 1)

        def set_search_type(self):
                if self.search_type == 'Author':
                        self.table = 'authors'
                        self.id_field = 'author_id'
                        self.SQLterm = self.make_author_SQL_term
                        self.print_results = self.print_author_results
                elif self.search_type == 'Title':
                        self.table = 'titles'
                        self.id_field = 'title_id'
                        self.SQLterm = self.make_titles_SQL_term
                        self.print_results = self.print_title_results
                elif self.search_type == 'Publication':
                        self.table = 'pubs'
                        self.id_field = 'pub_id'
                        self.SQLterm = self.make_pub_SQL_term
                        self.print_results = self.print_pub_results
                elif self.search_type == 'Publisher':
                        self.table = 'publishers'
                        self.id_field = 'publisher_id'
                        self.SQLterm = self.make_publisher_SQL_term
                        self.print_results = self.print_publisher_results
                elif self.search_type == 'Publication Series':
                        self.table = 'pub_series'
                        self.id_field = 'pub_series_id'
                        self.SQLterm = self.make_pub_series_SQL_term
                        self.print_results = self.print_pub_series_results
                elif self.search_type == 'Series':
                        self.table = 'series'
                        self.id_field = 'series_id'
                        self.SQLterm = self.make_series_SQL_term
                        self.print_results = self.print_series_results
                elif self.search_type == 'Award Type':
                        self.table = 'award_types'
                        self.id_field = 'award_type_id'
                        self.SQLterm = self.make_award_type_SQL_term
                        self.print_results = self.print_award_type_results
                elif self.search_type == 'Award Category':
                        self.table = 'award_cats'
                        self.id_field = 'award_cat_id'
                        self.SQLterm = self.make_award_cat_SQL_term
                        self.print_results = self.print_award_cat_results
                elif self.search_type == 'Award':
                        self.table = 'awards'
                        self.id_field = 'award_id'
                        self.SQLterm = self.make_award_SQL_term
                        self.print_results = self.print_award_results
                else:
                        self.display_error('Non-Existing Record Type')

        def validate_conjunction(self):
                if self.conjunction not in ('AND', 'OR'):
                        self.display_error('Only AND and OR conjunction values are allowed')
                
        def validate_sort(self):
                for sort_tuple in self.sort_values[self.search_type]:
                        if sort_tuple[0] == self.sort:
                                self.sort_name = sort_tuple[1]
                                break
                if not self.sort_name:
                        self.display_error("Unknown sort field: %s" % self.sort)

        def expand_sort(self):
                if self.sort == 'pub_pages':
                        self.sort = 'CAST(pub_pages as SIGNED)'
                elif self.sort == 'pub_price':
                        self.sort = "REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(pub_price,' ',''),'$',''),'C',''),'A',''),'M',''),'D',''),CHAR(0xA3),''),'F',''),CHAR(0x80),''),'z&#322;',''),'NZ',''),'t',''),CHAR(0x83),'')*100"
                if self.search_type == 'Author':
                        if self.sort != 'author_canonical':
                                self.sort += ', author_canonical'
                elif self.search_type == 'Title':
                        if self.sort != 'title_title':
                                self.sort += ', title_title'
                        if self.sort != 'title_copyright':
                                self.sort += ', title_copyright'
                elif self.search_type == 'Publication':
                        if self.sort != 'pub_title':
                                self.sort += ', pub_title'
                        if self.sort != 'pub_year':
                                self.sort += ', pub_year'
                elif self.search_type == 'Award Type':
                        if self.sort != 'award_type_short_name':
                                self.sort += ', award_type_short_name'
                elif self.search_type == 'Award Category':
                        if self.sort != 'award_cat_name':
                                self.sort += ', award_cat_name'
                elif self.search_type == 'Award':
                        if self.sort == 'award_level':
                                self.sort = 'CAST(award_level as SIGNED)'
                        if self.sort != 'award_year':
                                self.sort += ', award_year'

        def process_terms(self):
                for count in range(1, self.max_term + 1):
                        term = 'TERM_%d' % count
                        if self.form.has_key(term):
                                use = self.form.get('USE_%d' % count)
                                operator = self.form.get('O_%d' % count)
                                if not operator:
                                        operator = self.form.get('OPERATOR_%d' % count)
                                term_value = self.form.get(term)
                                self.process_one_term(term_value, use, operator)
                                self.selection_criteria.add((use, operator, term_value))

                if not self.term_list:
                        self.display_error("No search data entered")

        def process_one_term(self, term, use, operator):
                term = normalizeInput(term)
                if not term:
                        return
                raw_entry = term
                entry = self.format_entry(term)
                self.validate_term(use, entry)

                self.check_valid_operator(operator)

                # Process special cases: ISBNs and award levels
                if use == 'pub_isbn':
                        # Search for possible ISBN variations
                        isbn_values = isbnVariations(entry)
                        isbn_count = 0
                        sql_value = '('
                        for isbn_value in isbn_values:
                                padded_entry = self.pad_entry(operator, isbn_value)
                                if isbn_count:
                                        if operator in ('notexact', 'notcontains'):
                                                sql_value += ' and '
                                        else:
                                                sql_value += ' or '
                                sql_value += "pubs.pub_isbn %s" % padded_entry
                                isbn_count += 1
                        sql_value += ")"
                elif use == 'award_level':
                        try:
                                # Remove the trailing description of the award level
                                entry = entry.split(' ')[0]
                                entry = int(entry)
                        except:
                                self.display_error('Invalid Award Level')
                        sql_value = self.pad_entry(operator, entry)
                # Process standard cases which require simply padding the entered values
                else:
                        sql_value = self.pad_entry(operator, entry)

                (new_term, new_dbases) = self.SQLterm(use, entry, sql_value)
                self.term_list.append('(%s)' % new_term)
                self.merge_table_info_lists(self.dbases, new_dbases)

        def check_valid_operator(self, operator):
                found_operator = 0
                for operator_tuple in self.operators:
                        if operator == operator_tuple[0]:
                                found_operator = 1
                                break
                if not found_operator:
                        self.display_error("Invalid operator")

        def pad_entry(self, operator, entry):
                if operator == 'exact':
                        padded_entry = "like '%s'" % entry
                elif operator == 'notexact':
                        padded_entry = "not like '%s'" % entry
                elif operator == 'contains':
                        padded_entry = "like '%%%s%%'" % entry
                elif operator == 'notcontains':
                        padded_entry = "not like '%%%s%%'" % entry
                elif operator == 'starts_with':
                        padded_entry = "like '%s%%'" % entry
                elif operator == 'ends_with':
                        padded_entry = "like '%%%s'" % entry
                else:
                        self.display_error('An unexpected error has occurred. Please post the URL of this Web page on the Moderator noticeboard.')
                return padded_entry

        def validate_empty_term(self, value):
                stripped = value
                for wildcard in self.wildcards:
                        stripped = stripped.replace(wildcard,'')
                        if not stripped:
                                self.display_error('Search values must contain at least one non-wildcard character')

        def validate_term(self, field, value):
                self.validate_empty_term(value)
                
                if field in ('month', 'pub_month'):
                        (year, month, error) = validateMonth(value)
                        if error:
                                self.display_error(error)
                elif field == 'title_ttype':
                        if value.upper() not in SESSION.db.all_title_types:
                                self.display_error('Valid title types are: %s' % ', '.join(SESSION.db.all_title_types))
                elif field in ('title_graphic', 'title_non_genre', 'title_jvn', 'title_nvz', 'award_type_poll', 'award_type_non_genre'):
                        if value.lower() not in ('yes', 'no'):
                                self.display_error('Yes/No value required')
                elif field == 'pub_ctype':
                        if value.upper() not in SESSION.db.pub_types:
                                self.display_error('Valid title types are: %s' % ', '.join(SESSION.db.pub_types))

        def merge_table_info_lists(self, dest, src):
                for sti in src:
                        found = 0
                        for dti in dest:
                                if dti == sti:
                                        found = 1
                                        dti.merge_hints(sti)
                                        break
                        if not found:
                                dest.append(sti)

        def format_entry(self, value):
                # Double escape backslashes, which is required by the SQL syntax
                value = string.replace(value, '\\', '\\\\')
                value = db.escape_string(value)
                # Change asterisks to % because * is also a supported wildcard character
                value = string.replace(value, '*', '%')
                return value

        def make_terms(self):
                # Concatenate terms using the conjunction. Wrap the result in parentheses
                # to avoid unintended interaction with the join clauses.
                self.terms = "("
                count = 1
                for term in self.term_list:
                        if count == 1:
                                self.terms += '%s ' % term
                        else:
                                self.terms += '%s %s ' % (self.conjunction, term)
                        count += 1
                self.terms += ")"

                # Add the join clauses to the end
                for join in self.joins:
                        self.terms += " and " + join

        def execute_query(self):
                if self.action == 'query':
                        self.query = 'select distinct %s.* from ' % self.table
                elif self.action == 'count':
                        self.query = 'select count(distinct %s.%s) from ' % (self.table, self.id_field)
                self.build_full_query()
                self.search()
                if self.action == 'count':
                        self.display_message('Count of matching records: %d' % self.records[0])

        def print_selection_criteria(self):
                print '<b>Selection Criteria (joined using %s):</b>' % ISFDBText(self.conjunction)
                for selection in sorted(self.selection_criteria):
                        print '<br>'
                        for term_tuple in self.selection[self.search_type]:
                                if term_tuple[0] == selection[0]:
                                        print ISFDBText(term_tuple[1])
                                        break
                        for operator_tuple in self.operators:
                                if operator_tuple[0] == selection[1]:
                                        print ISFDBText(operator_tuple[1])
                                        break
                        print ISFDBText(selection[2])
                print '<br>Sort by %s' % ISFDBText(self.sort_name)

        def print_pub_results(self):
                PrintPubsTable(self.records, 'adv_search', self.user, 100)

        def print_publisher_results(self):
                PrintPublisherTable(self.records, 1, 100, self.user)
                if self.user.moderator:
                        self.print_merge_button()

        def print_pub_series_results(self):
                PrintPubSeriesTable(self.records, 100)

        def print_series_results(self):
                PrintSeriesTable(self.records, 100)

        def print_award_type_results(self):
                PrintAwardResults(self.records, 100)

        def print_award_cat_results(self):
                PrintAwardCatResults(self.records, 100)

        def print_award_results(self):
                from awardClass import awards
                award = awards(db)
                award.PrintAwardTable(self.records, 1, 1, 100)

        def print_author_results(self):
                PrintAuthorTable(self.records, 1, 100, self.user)
                if self.user.moderator:
                        self.print_merge_button()

        def print_title_results(self):
                PrintTitleTable(self.records, 1, 100, self.user)
                self.print_merge_button()

        def search(self):
                db.query(self.query)
                result = db.store_result()
                self.num = result.num_rows()

                if not self.num:
                        self.display_message('No records found')

                record = result.fetch_row()
                while record:
                        self.records.append(record[0])
                        record = result.fetch_row()

        def build_full_query(self):
                first = 1
                for dbase in self.dbases:
                        tclause = dbase.tname
                        firstHint = 1
                        for hint in dbase.hints:
                                if firstHint:
                                        tclause += " " + hint
                                        firstHint = 0
                                else :
                                        tclause += ", " + hint
                        if first:
                                self.query += tclause
                                first = 0
                        else:
                                self.query += "," + tclause
                self.query += " where %s order by %s limit %d,%d" % (self.terms, self.sort, self.start, 101)

        def print_merge_form(self):
                if self.user.moderator:
                        if self.search_type == 'Author':
                                self.print_help_merge('authors', 'av_merge')
                        elif self.search_type == 'Publisher':
                                self.print_help_merge('publishers', 'pv_merge')
                if self.search_type == 'Title':
                        self.print_help_merge('titles', 'tv_merge')

        def print_help_merge(self, record_type, script):
                print '<div id="HelpBox">'
                print '<b>Help:How to merge %s: </b>' % record_type
                print '<a href="%s://%s/index.php/Help:How_to_merge_%s">Help:How to merge %s</a><p>' % (PROTOCOL, WIKILOC, record_type, record_type)
                print '</div>'
                print '<form METHOD="POST" ACTION="/cgi-bin/edit/%s.cgi">' % script

        def print_page_buttons(self):
                print '<div class="button-container">'
                if self.start > 99:
                        self.print_page_button('Previous')
                if self.num > 100:
                        self.print_page_button('Next')
                print '</div>'

        def print_page_button(self, direction):
                print '<form METHOD="GET" action="%s:/%s/adv_search_results.cgi">' % (PROTOCOL, HTFAKE)
                print '<div>'
                if direction == 'Previous':
                        new_start = self.start - 100
                else:
                        new_start = self.start + 100
                print '<input NAME="START" value="%s" type="HIDDEN">' % new_start
                for key in self.form.keys():
                        if key != 'START':
                                key_value = ISFDBText(self.form[key], True)
                                print '<input NAME="%s" value="%s" type="HIDDEN">' % (key, key_value)
                if direction == 'Previous':
                        start = self.start-99
                        end = self.start
                else:
                        start = self.start+101
                        end = self.start+200
                print '<input TYPE="SUBMIT" VALUE="%s page (%d - %d)">' % (direction, start, end)
                print '</div>'
                print '</form>'

        def print_merge_button(self):
                print '<p>'
                print '<input TYPE="SUBMIT" VALUE="Merge Selected Records">'
                print '</form>'
                print '<hr>'

        def make_titles_SQL_term(self, field, value, sql_value):
                # Set up default values
                dbases = [tableInfo('titles')]
                if field == 'title_title':
                        clause = "titles.title_title %s" % sql_value
                elif field == 'title_trans_title':
                        clause = "trans_titles.trans_title_title %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('trans_titles')]
                        self.joins.add('trans_titles.title_id=titles.title_id')
                elif field == 'title_copyright':
                        clause = "SUBSTRING(titles.title_copyright,1,4) %s" % sql_value
                elif field == 'month':
                        clause = "SUBSTRING(titles.title_copyright,1,7) %s" % sql_value
                elif field == 'title_ttype':
                        clause = "titles.title_ttype %s" % sql_value
                elif field in ('title_storylen', 'title_content', 'title_graphic', 'title_non_genre', 'title_jvn', 'title_nvz'):
                        clause = "titles.%s %s" % (field, sql_value)
                elif field in ('author_canonical', 'author_birthplace', 'author_birthdate', 'author_deathdate'):
                        clause = "authors.%s %s and canonical_author.ca_status=1" % (field, sql_value)
                        dbases = [tableInfo('titles'), tableInfo('authors'), tableInfo('canonical_author',['USE INDEX(authors)'])]
                        self.joins.add('authors.author_id=canonical_author.author_id')
                        self.joins.add('titles.title_id=canonical_author.title_id')
                elif field == 'author_webpage':
                        clause = "webpages.url %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('canonical_author'), tableInfo('webpages')]
                        self.joins.add('canonical_author.title_id=titles.title_id')
                        self.joins.add('canonical_author.author_id=webpages.author_id')
                elif field == 'series':
                        clause = "series.series_title %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('series')]
                        self.joins.add('series.series_id=titles.series_id')
                elif field == 'reviewee':
                        clause = "titles.title_ttype='REVIEW' AND ca1.ca_status=3"
                        dbases = [tableInfo("titles"),tableInfo("canonical_author ca1"),
                                  tableInfo("(select author_id from authors where author_canonical %s) a1" % sql_value)]
                        self.joins.add('titles.title_id=ca1.title_id')
                        self.joins.add('ca1.author_id=a1.author_id')
                elif field == 'interviewee':
                        clause = "titles.title_ttype='INTERVIEW' AND ca2.ca_status=2"
                        dbases = [tableInfo("titles"),tableInfo("canonical_author ca2"),
                                  tableInfo("(select author_id from authors where author_canonical %s) a2" % sql_value)]
                        self.joins.add('titles.title_id=ca2.title_id')
                        self.joins.add('ca2.author_id=a2.author_id')
                elif field == 'title_note':
                        clause = "n1.note_note %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('notes n1')]
                        self.joins.add('n1.note_id=titles.note_id')
                elif field == 'title_synopsis':
                        clause = "n2.note_note %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('notes n2')]
                        self.joins.add('n2.note_id=titles.title_synopsis')
                elif field == 'single_vote':
                        clause = "votes.rating %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('votes')]
                        self.joins.add('votes.title_id=titles.title_id')
                elif field == 'title_webpage':
                        clause = "webpages.url %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('webpages')]
                        self.joins.add('webpages.title_id=titles.title_id')
                elif field in ('title_language', 'title_language_free'):
                        clause = "languages.lang_name %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('languages')]
                        self.joins.add('languages.lang_id=titles.title_language')
                elif field == 'tag':
                        clause = "tags.tag_name %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('tags'), tableInfo('tag_mapping')]
                        self.joins.add('tag_mapping.title_id=titles.title_id')
                        self.joins.add('tags.tag_id=tag_mapping.tag_id')
                else:
                        self.display_error("Unknown field: %s" % field)
                return (clause, dbases)

        def make_author_SQL_term(self, field, value, sql_value):
                # Set up default values
                dbases = [tableInfo('authors')]
                if field == 'author_canonical':
                        clause = "authors.author_canonical %s" % sql_value
                elif field == 'author_trans_name':
                        clause = "trans_authors.trans_author_name %s" % sql_value
                        dbases = [tableInfo('authors'), tableInfo('trans_authors')]
                        self.joins.add('trans_authors.author_id=authors.author_id')
                elif field == 'author_legalname':
                        clause = "authors.author_legalname %s" % sql_value
                elif field == 'author_trans_legalname':
                        clause = "trans_legal_names.trans_legal_name %s" % sql_value
                        dbases = [tableInfo('authors'), tableInfo('trans_legal_names')]
                        self.joins.add('trans_legal_names.author_id=authors.author_id')
                elif field == 'author_lastname':
                        clause = "authors.author_lastname %s" % sql_value
                elif field == 'author_birthplace':
                        clause = "authors.author_birthplace %s" % sql_value
                elif field == 'author_birthdate':
                        clause = "authors.author_birthdate %s" % sql_value
                elif field == 'author_deathdate':
                        clause = "authors.author_deathdate %s" % sql_value
                elif field in ('author_language', 'author_language_free'):
                        clause = "languages.lang_name %s" % sql_value
                        dbases = [tableInfo('authors'), tableInfo('languages')]
                        self.joins.add('languages.lang_id=authors.author_language')
                elif field == 'author_pseudos':
                        clause = """authors.author_id in (SELECT pseudonyms.author_id from pseudonyms,
                                  authors a1 WHERE pseudonym = a1.author_id AND a1.author_canonical %s)""" % sql_value
                elif field == 'author_image':
                        clause = "authors.author_image %s" % sql_value
                elif field == 'author_webpage':
                        clause = "webpages.url %s" % sql_value
                        dbases = [tableInfo('authors'), tableInfo('webpages')]
                        self.joins.add('webpages.author_id=authors.author_id')
                elif field == 'author_email':
                        clause = "emails.email_address %s" % sql_value
                        dbases = [tableInfo('authors'), tableInfo('emails')]
                        self.joins.add('emails.author_id=authors.author_id')
                elif field == 'author_note':
                        clause = "authors.author_note %s" % sql_value
                else:
                        self.display_error("Unknown field: %s" % field)
                return (clause, dbases)

        def make_pub_SQL_term(self, field, value, sql_value):
                # Set up default values
                dbases = [tableInfo('pubs')]
                if field == 'pub_title':
                        clause = "pubs.pub_title %s" % sql_value
                elif field == 'pub_trans_title':
                        clause = "trans_pubs.trans_pub_title %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('trans_pubs')]
                        self.joins.add('trans_pubs.pub_id=pubs.pub_id')
                elif field == 'pub_year':
                        clause = "SUBSTRING(pubs.pub_year,1,4) %s" % sql_value
                elif field == 'pub_month':
                        clause = "SUBSTRING(pubs.pub_year,1,7) %s" % sql_value
                elif field == 'pub_publisher':
                        clause = "publishers.publisher_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('publishers')]
                        self.joins.add('pubs.publisher_id=publishers.publisher_id')
                elif field == 'trans_publisher':
                        clause = "trans_publisher.trans_publisher_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('trans_publisher')]
                        self.joins.add('trans_publisher.publisher_id=pubs.publisher_id')
                elif field == 'pub_series':
                        clause = "pub_series.pub_series_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('pub_series')]
                        self.joins.add('pubs.pub_series_id=pub_series.pub_series_id')
                elif field == 'trans_pub_series':
                        clause = "trans_pub_series.trans_pub_series_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('trans_pub_series')]
                        self.joins.add('trans_pub_series.pub_series_id=pubs.pub_series_id')
                elif field == 'pub_isbn':
                        # ISBNs are a special case. The whole clause was pre-built in process_one_term
                        clause = sql_value
                elif field == 'pub_catalog':
                        clause = "pubs.pub_catalog %s" % sql_value
                elif field == 'pub_ptype':
                        clause = "pubs.pub_ptype %s" % sql_value
                elif field in ('author_canonical', 'author_birthplace', 'author_birthdate', 'author_deathdate'):
                        clause = "authors.%s %s" % (field, sql_value)
                        dbases = [tableInfo('pubs'), tableInfo('authors'), tableInfo('pub_authors',['USE INDEX(author_id)'])]
                        self.joins.add('authors.author_id=pub_authors.author_id')
                        self.joins.add('pubs.pub_id=pub_authors.pub_id')
                elif field == 'author_webpage':
                        clause = "webpages.url %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('pub_authors'), tableInfo('webpages')]
                        self.joins.add('pub_authors.pub_id=pubs.pub_id')
                        self.joins.add('pub_authors.author_id=webpages.author_id')
                elif field == 'pub_price':
                        clause = "pubs.pub_price %s" % sql_value
                elif field == 'pub_pages':
                        clause = "pubs.pub_pages %s" % sql_value
                elif field == 'pub_coverart':
                        clause = "titles.title_ttype='COVERART' and authors.author_canonical %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('pub_content'), tableInfo('canonical_author'), tableInfo('titles'), tableInfo('authors')]
                        self.joins.add('pubs.pub_id=pub_content.pub_id')
                        self.joins.add('pub_content.title_id=canonical_author.title_id')
                        self.joins.add('canonical_author.title_id=titles.title_id')
                        self.joins.add('canonical_author.author_id=authors.author_id')
                elif field in ('title_language', 'title_language_free'):
                        clause = "languages.lang_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('pub_content'), tableInfo('titles'), tableInfo('languages')]
                        self.joins.add('pubs.pub_id=pub_content.pub_id')
                        self.joins.add('pub_content.title_id=titles.title_id')
                        self.joins.add('languages.lang_id=titles.title_language')
                elif field == 'pub_note':
                        clause = "notes.note_note %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('notes')]
                        self.joins.add('pubs.note_id = notes.note_id')
                elif field == 'pub_verifier':
                        clause = "mw_user.user_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('mw_user'), tableInfo('primary_verifications')]
                        self.joins.add('pubs.pub_id = primary_verifications.pub_id')
                        self.joins.add('primary_verifications.user_id = mw_user.user_id')
                elif field == 'pub_ver_date':
                        clause = "DATE(primary_verifications.ver_time) %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('primary_verifications')]
                        self.joins.add('pubs.pub_id = primary_verifications.pub_id')
                elif field == 'secondary_ver_source':
                        clause = "reference.reference_label %s and verification.ver_status = 1" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('reference'), tableInfo('verification')]
                        self.joins.add('pubs.pub_id = verification.pub_id')
                        self.joins.add('verification.reference_id = reference.reference_id')
                elif field == 'pub_frontimage':
                        clause = "pub_frontimage %s" % sql_value
                elif field == 'pub_ctype':
                        clause = "pubs.pub_ctype %s" % sql_value
                elif field == 'pub_webpage':
                        clause = "webpages.url %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('webpages')]
                        self.joins.add('webpages.pub_id=pubs.pub_id')
                else:
                        self.display_error("Unknown field: %s" % field)
                return (clause, dbases)

        def make_publisher_SQL_term(self, field, value, sql_value):
                # Set up default values
                dbases = [tableInfo('publishers')]
                if field == 'publisher_name':
                        clause = 'publishers.publisher_name %s' % sql_value
                elif field == 'trans_publisher_name':
                        clause = 'trans_publisher.trans_publisher_name %s' % sql_value
                        dbases = [tableInfo('publishers'), tableInfo('trans_publisher')]
                        self.joins.add('trans_publisher.publisher_id=publishers.publisher_id')
                elif field == 'publisher_note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('publishers'), tableInfo('notes')]
                        self.joins.add('publishers.note_id = notes.note_id')
                elif field == 'publisher_webpage':
                        clause = 'webpages.url %s' % sql_value
                        dbases = [tableInfo('publishers'), tableInfo('webpages')]
                        self.joins.add('webpages.publisher_id=publishers.publisher_id')
                else:
                        self.display_error('Unknown field: %s' % field)
                return (clause, dbases)

        def make_pub_series_SQL_term(self, field, value, sql_value):
                # Set up default values
                dbases = [tableInfo('pub_series')]
                if field == 'pub_series_name':
                        clause = 'pub_series.pub_series_name %s' % sql_value
                elif field == 'trans_pub_series_name':
                        clause = 'trans_pub_series.trans_pub_series_name %s' % sql_value
                        dbases = [tableInfo('pub_series'), tableInfo('trans_pub_series')]
                        self.joins.add('trans_pub_series.pub_series_id=pub_series.pub_series_id')
                elif field == 'pub_series_note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('pub_series'), tableInfo('notes')]
                        self.joins.add('pub_series.pub_series_note_id = notes.note_id')
                elif field == 'pub_series_webpage':
                        clause = 'webpages.url %s' % sql_value
                        dbases = [tableInfo('pub_series'), tableInfo('webpages')]
                        self.joins.add('webpages.pub_series_id=pub_series.pub_series_id')
                else:
                        self.display_error('Unknown field: %s' % field)
                return (clause, dbases)

        def make_award_type_SQL_term(self, field, value, sql_value):
                # Set up default values
                dbases = [tableInfo('award_types')]
                if field == 'award_type_short_name':
                        clause = 'award_types.award_type_short_name %s' % sql_value
                elif field == 'award_type_name':
                        clause = 'award_types.award_type_name %s' % sql_value
                elif field == 'award_type_for':
                        clause = 'award_types.award_type_for %s' % sql_value
                elif field == 'award_type_by':
                        clause = 'award_types.award_type_by %s' % sql_value
                elif field == 'award_type_poll':
                        clause = 'award_types.award_type_poll %s' % sql_value
                elif field == 'award_type_non_genre':
                        clause = 'award_types.award_type_non_genre %s' % sql_value
                elif field == 'note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('notes'), tableInfo('award_types')]
                        self.joins.add('award_types.award_type_note_id = notes.note_id')
                elif field == 'webpage':
                        clause = 'webpages.url %s' % sql_value
                        dbases = [tableInfo('award_types'), tableInfo('webpages')]
                        self.joins.add('webpages.award_type_id=award_types.award_type_id')
                else:
                        self.display_error('Unknown field: %s' % field)
                return (clause, dbases)

        def make_award_cat_SQL_term(self, field, value, sql_value):
                # Set up default values
                dbases = [tableInfo('award_cats')]
                if field == 'award_cat_name':
                        clause = 'award_cats.award_cat_name %s' % sql_value
                elif field == 'award_type_short_name':
                        clause = 'award_types.award_type_short_name %s' % sql_value
                        dbases = [tableInfo('award_types'), tableInfo('award_cats')]
                        self.joins.add('award_cats.award_cat_type_id = award_types.award_type_id')
                elif field == 'award_type_full_name':
                        clause = 'award_types.award_type_name %s' % sql_value
                        dbases = [tableInfo('award_types'), tableInfo('award_cats')]
                        self.joins.add('award_cats.award_cat_type_id = award_types.award_type_id')
                elif field == 'award_cat_order':
                        clause = 'award_cats.award_cat_order %s' % sql_value
                elif field == 'note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('notes'), tableInfo('award_cats')]
                        self.joins.add('award_cats.award_cat_note_id = notes.note_id')
                elif field == 'webpage':
                        clause = 'webpages.url %s' % sql_value
                        dbases = [tableInfo('award_cats'), tableInfo('webpages')]
                        self.joins.add('webpages.award_cat_id = award_cats.award_cat_id')
                else:
                        self.display_error('Unknown field: %s' % field)
                return (clause, dbases)

        def make_award_SQL_term(self, field, value, sql_value):
                # Set up default values
                dbases = [tableInfo('awards')]
                if field == 'award_year':
                        clause = 'SUBSTRING(awards.award_year,1,4) %s' % sql_value
                elif field == 'award_level':
                        clause = 'awards.award_level %s' % sql_value
                elif field == 'title_title':
                        clause = 'titles.title_title %s' % sql_value
                        dbases = [tableInfo('awards'), tableInfo('titles'), tableInfo('title_awards')]
                        self.joins.add('awards.award_id = title_awards.award_id')
                        self.joins.add('title_awards.title_id=titles.title_id')
                elif field == 'title_ttype':
                        clause = 'titles.title_ttype %s' % sql_value
                        dbases = [tableInfo('awards'), tableInfo('titles'), tableInfo('title_awards')]
                        self.joins.add('awards.award_id = title_awards.award_id')
                        self.joins.add('title_awards.title_id=titles.title_id')
                elif field == 'award_cat_name':
                        clause = 'award_cats.award_cat_name %s' % sql_value
                        dbases = [tableInfo('award_cats'), tableInfo('awards')]
                        self.joins.add('award_cats.award_cat_id = awards.award_cat_id')
                elif field == 'award_type_short_name':
                        clause = 'award_types.award_type_short_name %s' % sql_value
                        dbases = [tableInfo('award_types'), tableInfo('award_cats'), tableInfo('awards')]
                        self.joins.add('awards.award_cat_id = award_cats.award_cat_id and award_cats.award_cat_type_id = award_types.award_type_id')
                elif field == 'award_type_full_name':
                        clause = 'award_types.award_type_name %s' % sql_value
                        dbases = [tableInfo('award_types'), tableInfo('award_cats'), tableInfo('awards')]
                        self.joins.add('awards.award_cat_id = award_cats.award_cat_id and award_cats.award_cat_type_id = award_types.award_type_id')
                elif field == 'note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('notes'), tableInfo('awards')]
                        self.joins.add('awards.award_note_id = notes.note_id')
                else:
                        self.display_error('Unknown field: %s' % field)
                return (clause, dbases)

        def make_series_SQL_term(self, field, value, sql_value):
                # Set up default values
                dbases = [tableInfo('series')]
                if field == 'series_title':
                        clause = 'series.series_title %s' % sql_value
                elif field == 'trans_series_name':
                        clause = 'trans_series.trans_series_name %s' % sql_value
                        dbases = [tableInfo('series'), tableInfo('trans_series')]
                        self.joins.add('trans_series.series_id=series.series_id')
                elif field == 'parent_series_name':
                        clause = 's2.series_title %s' % sql_value
                        dbases = [tableInfo('series'), tableInfo('series s2')]
                        self.joins.add('s2.series_id = series.series_parent')
                elif field == 'parent_series_position':
                        clause = 'series.series_parent_position %s' % sql_value
                elif field == 'series_note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('series'), tableInfo('notes')]
                        self.joins.add('series.series_note_id = notes.note_id')
                elif field == 'series_webpage':
                        clause = 'webpages.url %s' % sql_value
                        dbases = [tableInfo('series'), tableInfo('webpages')]
                        self.joins.add('webpages.series_id=series.series_id')
                else:
                        self.display_error('Unknown field: %s' % field)
                return (clause, dbases)

class tableInfo:
        def __init__(self, tname='', hints=None):
                self.tname = tname
                if hints == None:
                        self.hints = []
                else:
                        self.hints = hints

        def __cmp__(self, ti):
                if (self.tname == ti.tname):
                        return 0
                if (self.tname < ti.tiname):
                        return -1
                return 1

        def __eq__(self, ti):
                return self.tname == ti.tname

        def merge_hints(self, other):
            for hint in other.hints:
                if not hint in self.hints:
                    self.hints.append(hint)
            return self


if __name__ == '__main__':
        search = AdvancedSearchResults()
        search.results()
