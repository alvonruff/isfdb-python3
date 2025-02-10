#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1203 $
#     Date: $Date: 2024-12-23 09:46:14 -0500 (Mon, 23 Dec 2024) $

import cgi
import sys
import string
import MySQLdb
from isfdb import *
from common import *
from SQLparsing import *
from library import *
from isbn import *
from login import User

class AdvancedSearch:
        def __init__ (self):
                self.user = User()
                self.user.load()
                self.define_criteria()

        def define_criteria(self):
                self.max_term = 10
                self.selection = {}
                self.operators = (('exact', 'is exactly'),
                                  ('notexact', 'is not exactly'),
                                  ('contains', 'contains'),
                                  ('notcontains', 'does not contain'),
                                  ('starts_with', 'starts with'),
                                  ('ends_with', 'ends with')
                                  )
                self.sort_values = {}
                self.messages = {}
                self.search_types = {'author': 'Author',
                                     'award': 'Award',
                                     'award_cat': 'Award Category',
                                     'award_type': 'Award Type',
                                     'pub': 'Publication',
                                     'pub_series': 'Publication Series',
                                     'publisher': 'Publisher',
                                     'series': 'Series',
                                     'title': 'Title'}

                self.selection['Award'] = (('award_year', 'Award Year'),
                                           ('award_level', 'Award Level'),
                                           ('title_title', 'Title (for title-based awards)'),
                                           ('title_ttype', 'Title Type'),
                                           ('award_cat_name', 'Award Category'),
                                           ('award_type_short_name', 'Award Type Short Name'),
                                           ('award_type_full_name', 'Award Type Full Name'),
                                           ('note', 'Notes')
                                           )
                self.sort_values['Award'] = (('award_year', 'Award Year'),
                                      ('award_level', 'Award Level')
                                      )

                self.selection['Award Category'] = (('award_cat_name', 'Award Category Name'),
                                           ('award_type_short_name', 'Parent Award Type Short Name'),
                                           ('award_type_full_name', 'Parent Award Type Full Name'),
                                           ('award_cat_order', 'Award Category Order'),
                                           ('note', 'Notes'),
                                           ('webpage', 'Webpage')
                                           )
                self.sort_values['Award Category'] = (('award_cat_name', 'Award Category Name'),
                                      ('award_cat_order', 'Award Category Order')
                                      )

                self.selection['Award Type'] = (('award_type_short_name', 'Award Type Name (Short)'),
                                           ('award_type_name', 'Award Type Name (Full)'),
                                           ('award_type_for', 'Awarded For'),
                                           ('award_type_by', 'Awarded By'),
                                           ('award_type_poll', 'Poll'),
                                           ('award_type_non_genre', 'Non-Genre'),
                                           ('note', 'Notes'),
                                           ('webpage', 'Webpage')
                                           )
                self.sort_values['Award Type'] = (('award_type_short_name', 'Short Award Type Name'),
                                      ('award_type_name', 'Full Award Type Name'),
                                      ('award_type_for', 'Awarded For'),
                                      ('award_type_by', 'Awarded By'),
                                      ('award_type_poll', 'Poll'),
                                      ('award_type_non_genre', 'Non-Genre')
                                      )

                self.selection['Publication Series'] = (('pub_series_name', 'Publication Series Name'),
                                           ('trans_pub_series_name', 'Transliterated Publication Series Name'),
                                           ('pub_series_note', 'Notes'),
                                           ('pub_series_webpage', 'Webpage')
                                           )
                self.sort_values['Publication Series'] = (('pub_series_name', 'Publication Series Name'),
                                      )

                self.selection['Publisher'] = (('publisher_name', 'Publisher Name'),
                                           ('trans_publisher_name', 'Transliterated Publisher Name'),
                                           ('publisher_note', 'Notes'),
                                           ('publisher_webpage', 'Webpage')
                                           )
                self.sort_values['Publisher'] = (('publisher_name', 'Publisher Name'),
                                      )

                self.selection['Series'] = (('series_title', 'Series Name'),
                                           ('trans_series_name', 'Transliterated Series Name'),
                                           ('parent_series_name', 'Parent Series Name'),
                                           ('parent_series_position', 'Position within Parent Series'),
                                           ('series_note', 'Notes'),
                                           ('series_webpage', 'Webpage')
                                           )
                self.sort_values['Series'] = (('series_title', 'Series Name'),
                                      )

                self.selection['Publication'] = (('pub_title', 'Title'),
                                           ('pub_trans_title', 'Transliterated Title'),
                                           ('pub_ctype', 'Publication Type'),
                                           ('author_canonical', 'Author\'s Name'),
                                           ('author_birthplace', 'Author\'s Birth Place'),
                                           ('author_birthdate', 'Author\'s Birthdate'),
                                           ('author_deathdate', 'Author\'s Deathdate'),
                                           ('author_webpage', 'Author\'s Webpage'),
                                           ('pub_year', 'Publication Year'),
                                           ('pub_month', 'Publication Month'),
                                           ('pub_publisher', 'Publisher'),
                                           ('trans_publisher', 'Transliterated Publisher'),
                                           ('pub_series', 'Publication Series'),
                                           ('trans_pub_series', 'Transliterated Publication Series'),
                                           ('title_language', 'Language of an Included Title (list)'),
                                           ('title_language_free', 'Language of an Included Title (free form)'),
                                           ('pub_isbn', 'ISBN'),
                                           ('pub_catalog', 'Catalog ID'),
                                           ('pub_price', 'Price'),
                                           ('pub_pages', 'Page Count'),
                                           ('pub_coverart', 'Cover Artist'),
                                           ('pub_ptype', 'Format'),
                                           ('pub_verifier', 'Primary Verifier'),
                                           ('pub_ver_date', 'Primary Verification Date'),
                                           ('secondary_ver_source', 'Secondary Verification Source'),
                                           ('pub_webpage', 'Publication Webpage'),
                                           ('pub_note', 'Notes'),
                                           ('pub_frontimage', 'Image URL')
                                           )
                self.sort_values['Publication'] = (('pub_title', 'Title'),
                                      ('pub_ctype', 'Publication Type'),
                                      ('pub_year', 'Date'),
                                      ('pub_isbn', 'ISBN'),
                                      ('pub_catalog', 'Catalog ID'),
                                      ('pub_price', 'Price'),
                                      ('pub_pages', 'Page Count'),
                                      ('pub_ptype', 'Format'),
                                      ('pub_frontimage', 'Image URL')
                                      )
                self.messages['Publication'] = ['ISBN searches ignore dashes and search for both ISBN-10 and ISBN-13']
                self.messages['Publication'].append("""When specifying multiple Authors, Cover Artists,
                                                       Publication Webpages, Primary Verifiers or
                                                       Secondary Verification Sources, OR is supported but AND is not""")

                self.selection['Title'] = (('title_title', 'Title'),
                                           ('title_trans_title', 'Transliterated Title'),
                                           ('author_canonical', 'Author\'s Name'),
                                           ('author_birthplace', 'Author\'s Birth Place'),
                                           ('author_birthdate', 'Author\'s Birthdate'),
                                           ('author_deathdate', 'Author\'s Deathdate'),
                                           ('author_webpage', 'Author\'s Webpage'),
                                           ('reviewee', 'Reviewed Author'),
                                           ('interviewee', 'Interviewed Author'),
                                           ('title_copyright', 'Title Year'),
                                           ('month', 'Title Month'),
                                           ('title_storylen', 'Length'),
                                           ('title_content', 'Content (omnibus only)'),
                                           ('title_ttype', 'Title Type'),
                                           ('title_note', 'Notes'),
                                           ('title_synopsis', 'Synopsis'),
                                           ('single_vote', 'Single User Vote'),
                                           ('series', 'Series'),
                                           ('title_language', 'Title Language (list)'),
                                           ('title_language_free', 'Title Language (free form)'),
                                           ('title_webpage', 'Title Webpage'),
                                           ('tag', 'Tag'),
                                           ('title_jvn', 'Juvenile'),
                                           ('title_nvz', 'Novelization'),
                                           ('title_non_genre', 'Non-Genre'),
                                           ('title_graphic', 'Graphic Format')
                                           )
                self.sort_values['Title'] = (('title_title', 'Title'),
                                      ('title_copyright', 'Date'),
                                      ('title_ttype', 'Title Type')
                                      )
                self.messages['Title'] = ['When specifying multiple authors and/or multiple tags, OR is supported but AND is not']

                self.selection['Author'] = (('author_canonical', 'Canonical Name'),
                                           ('author_trans_name', 'Transliterated Name'),
                                           ('author_lastname', 'Directory Entry'),
                                           ('author_legalname', 'Legal Name'),
                                           ('author_trans_legalname', 'Transliterated Legal Name'),
                                           ('author_birthplace', 'Birth Place'),
                                           ('author_birthdate', 'Birthdate'),
                                           ('author_deathdate', 'Deathdate'),
                                           ('author_language', 'Working Language (list)'),
                                           ('author_language_free', 'Working Language (free form)'),
                                           ('author_image', 'Author Image'),
                                           ('author_webpage', 'Webpage'),
                                           ('author_email', 'E-mail'),
                                           ('author_pseudos', 'Alternate Name'),
                                           ('author_note', 'Note')
                                           )
                self.sort_values['Author'] = (('author_canonical', 'Canonical Name'),
                                      ('author_lastname', 'Directory Entry'),
                                      ('author_legalname', 'Legal Name'),
                                      ('author_birthplace', 'Birth Place'),
                                      ('author_birthdate', 'Birthdate'),
                                      ('author_deathdate', 'Deathdate')
                                      )

        def parseArguments(self):
                self.selector_id = SESSION.Parameter(0, 'str', None, self.search_types.keys())
                self.search_type = self.search_types[self.selector_id]

        def display_selection(self):
                self.parseArguments()
                PrintHeader('Advanced %s Search' % self.search_type)
                PrintNavbar('adv_search_selection', 0, 0, 0, 0)
                if not self.user.id:
                        print '<h3>For performance reasons, Advanced Searches are currently restricted to registered users.</h3>'
                else:
                        self.print_invisible_drop_down_values()
                        self.print_full_header()
                        self.print_search_table()
                PrintTrailer('adv_search_selection', 0, 0)

        def print_search_table(self):
                print('<h2>Selection Criteria</h2>')
                print('<form METHOD="GET" action="%s:/%s/adv_search_results.cgi">' % (PROTOCOL, HTFAKE))
                print('<p>')
                if self.search_type in self.messages:
                        print('<ul>')
                        for message in self.messages[self.search_type]:
                                print('<li> %s' % message)
                        print('</ul>')
                for self.number in range(1, self.max_term + 1):
                        self.print_selectors()
                self.print_sort_by()
                self.print_submit_button()

        def print_invisible_drop_down_values(self):
                self.print_one_invisible_drop_down('Formats', SESSION.db.formats)
                self.print_one_invisible_drop_down('PubTypes', SESSION.db.pub_types)
                self.print_one_invisible_drop_down('TitleTypes', SESSION.db.all_title_types)
                self.print_one_invisible_drop_down('StoryLengths', SESSION.db.storylen_codes)
                selectable_languages = sorted(list(LANGUAGES))
                if 'None' in selectable_languages:
                        selectable_languages.remove('None')
                self.print_one_invisible_drop_down('AllLanguages', selectable_languages)
                self.print_invisible_secondary_verifications()
                self.print_invisible_award_levels()

        def print_one_invisible_drop_down(self, name, values):
                print '<select NAME="%s" id="%s" class="nodisplay">' % (name, name)
                for value in values:
                        # Skip empty values, e.g. in SESSION.db.storylen_codes
                        if value:
                                print '<option VALUE="%s">%s' % (value, value)
                print '</select>'

        def print_invisible_secondary_verifications(self):
                sources = SQLGetRefDetails()
                labels = []
                for source in sources:
                        labels.append(source[REFERENCE_LABEL])
                self.print_one_invisible_drop_down('SecondaryVerSources', labels)

        def print_invisible_award_levels(self):
                from awardClass import awardShared
                print '<select NAME="AwardLevels" id="AwardLevels" class="nodisplay">'
                # First display regular award levels in the 1-70 range
                for award_level in range(1,71):
                        if award_level == 1:
                                displayed_value = '1 (Win)'
                        elif award_level == 9:
                                displayed_value = '9 (Nomination)'
                        else:
                                displayed_value = '%d' % award_level
                        print '<option VALUE="%s">%s</option>' % (displayed_value, displayed_value)
                # Next display special award levels in the 71-99 range
                special_levels = awardShared.SpecialAwards()
                for special_level in sorted(special_levels):
                        print '<option VALUE="%s (%s)">%s (%s)</option>' % (special_level, special_levels[special_level], special_level, special_levels[special_level])
                print '</select>'

        def print_full_header(self):
                print '<ul>'
                print '<li>A downloadable version of the ISFDB database is available <a href="%s://%s/index.php/ISFDB_Downloads">here</a>' % (PROTOCOL, WIKILOC)
                print '<li>Supported wildcards: * and % match any number of characters, _ matches one character'
                print '</ul>'
                print '<hr>'

        def print_submit_button(self):
                print '<button TYPE="SUBMIT" NAME="ACTION" VALUE="query">Get Results</button>'
                print '<button TYPE="SUBMIT" NAME="ACTION" VALUE="count">Get Count</button>'
                print '<input NAME="START" VALUE="0" TYPE="HIDDEN">'
                print '<input NAME="TYPE" VALUE="%s" TYPE="HIDDEN">' % self.search_type
                print '</form>'

        def print_radio_selectors(self):
                print '<input TYPE="RADIO" NAME="C" VALUE="AND" CHECKED>AND'
                print '<input TYPE="RADIO" NAME="C" VALUE="OR">OR'

        def print_selectors(self):
                print '<p id="%s_selectors_%d">' % (self.selector_id, self.number)
                print '<select NAME="USE_%d" id="%s_%d">' % (self.number, self.selector_id, self.number)
                for value_display_pair in self.selection[self.search_type]:
                        print '<option VALUE="%s">%s' % (value_display_pair[0], value_display_pair[1])
                print '</select>'

                print '<select NAME="O_%d" id="%s_operator_%d">' % (self.number, self.selector_id, self.number)
                for operator_tuple in self.operators:
                        print '<option VALUE="%s">%s' % (operator_tuple[0], operator_tuple[1])
                print '</select>'

                print '<input id="%sterm_%d" NAME="TERM_%d" TYPE="text" SIZE="50">' % (self.selector_id, self.number, self.number)
                if self.number == 1:
                        self.print_radio_selectors()
                print '<p>'

        def print_sort_by(self):
                if self.search_type not in self.sort_values:
                        return
                # If there is only one way to sort the search results, hide the sort value
                if len(self.sort_values[self.search_type]) == 1:
                        print '<input NAME="ORDERBY" VALUE="%s" TYPE="HIDDEN">' % self.sort_values[self.search_type][0][0]
                        return

                print '<b>Sort Results By:</b>'
                print '<select NAME="ORDERBY">'
                for value_display_pair in self.sort_values[self.search_type]:
                        print '<option VALUE="%s">%s' % (value_display_pair[0], value_display_pair[1])
                print '</select>'
