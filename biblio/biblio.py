from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1212 $
#     Date: $Date: 2025-01-22 16:00:18 -0500 (Wed, 22 Jan 2025) $


import sys
import os
import string
import traceback
from SQLparsing import *
from common import *
from login import *
from awardClass import awards

class Bibliography:
        def __init__(self):
                # Last time we printed a message indicating how long
                # a certain part of the page generation process took
                # (development server only)
                self.last_checkpoint = time()

                ##############################################
                # AUTHOR properties
                ##############################################
                # Author name
                self.author_name = ''
                # Author ID
                self.au_id = -1
                # Full author record
                self.au_data = []
                # 0/1 flag indicating whether this author is an alternate name
                self.au_is_pseudonym = 0
                # 0/1 flag indicating whether this author has alternate names
                self.au_has_pseudonyms = 0
                # List of this author's tags
                self.au_tags = []
                # List of this author's transliterated canonical names
                self.au_trans_names = []
                # List of this author's transliterated legal names
                self.au_trans_legal_names = []

                ##############################################
                # WEB PAGE TYPE properties
                ##############################################
                # Author page type; can be reset by CGI scripts
                self.page_type = 'Summary'
                # Dictionary of CGI script names indexed by displayed Web page name
                self.page_types = {'Summary': 'ea',
                                 'Alphabetical': 'ae',
                                 'Chronological': 'ch',
                                 'Award': 'eaw'
                                 }
                self.cgi_script = ''

                ##############################################
                # SERIES and TITLE TYPE properties
                ##############################################
                # Dictionary of displayed title types indexed by title type
                # names stored in the database
                self.title_types = {'NOVEL': 'Novels',
                               'COLLECTION': 'Collections',
                               'ANTHOLOGY': 'Anthologies',
                               'OMNIBUS': 'Omnibus',
                               'SERIAL': 'Serials',
                               'SHORTFICTION': 'Short Fiction',
                               'ESSAY': 'Essays',
                               'REVIEW': 'Reviews',
                               'POEM': 'Poems',
                               'EDITOR': 'Magazine Editor',
                               'INTERVIEW': 'Interviews by This Author',
                               'NONFICTION': 'Nonfiction',
                               'INTERIORART': 'Interior Art',
                               'COVERART': 'Cover Art',
                               'CHAPBOOK': 'Chapbooks'
                               }
                # List of series types and title types in the
                # order in which the page will display them
                self.ordered_title_types = (SERIES_TYPE_FICTION,
                                            'NOVEL',
                                            'COLLECTION',
                                            'OMNIBUS',
                                            'SERIAL',
                                            SERIES_TYPE_EDIT, 'EDITOR',
                                            SERIES_TYPE_ANTH, 'ANTHOLOGY',
                                            'CHAPBOOK',
                                            SERIES_TYPE_NONFIC, 'NONFICTION',
                                            SERIES_TYPE_SF, 'SHORTFICTION',
                                            SERIES_TYPE_POEM, 'POEM',
                                            SERIES_TYPE_ESSAY, 'ESSAY',
                                            SERIES_TYPE_COVERART, 'COVERART',
                                            SERIES_TYPE_INTERIORART, 'INTERIORART',
                                            SERIES_TYPE_REVIEW, 'REVIEW',
                                            SERIES_TYPE_INTERVIEW, 'INTERVIEW'
                                            )

                ##############################################
                # TITLE and CO-AUTHOR properties
                ##############################################
                # List of canonical titles for this author. The sorting depends on
                # the type of author page. For alphabetical and award
                # biblios, the list also contains variant title records.
                self.canonical_titles = []
                # List of interviews WITH this author
                self.interviews = []
                # Dictionary of variant titles, excluding Serials, indexed by parent title ID
                self.variant_titles = {}
                # Dictionary of variant serials indexed by parent title ID
                self.variant_serials = {}
                # Dictionary of parent author IDs indexed by parent title ID
                self.parent_authors = {}
                # Dictionary of variant author IDs indexed by variant title ID
                self.variant_authors = {}
                # List of parent title IDs that have pubs associated DIRECTLY with them
                self.parent_titles_with_pubs = []
                # Dictionary of transliterated titles
                self.translit_titles = {}
                # Dictionary of transliterated authors
                self.translit_authors = {}

                ##############################################
                # AWARD properties
                ##############################################
                # List of awards for this author
                self.au_awards = []

                ##############################################
                # USER properties
                ##############################################
                self.user = User()
                # Load user data
                self.user.load()

                ##############################################
                # SERIES TREE properties
                ##############################################
                # Dict of all (bottom, top and intermediate) series by series ID: {series_id : series_data}
                self.series_tree = {}
                # Dict of ALL series by parent ID: {parent_series_id : [child_id_1, child_id_2, ...]}
                self.series_parent = {}
                # Dict of ALL parents by child ID: {child_series_id : parent_series_id}
                self.series_child = {}
                # Dict of TOP series: {series_id : series_type}. Series type mapping is defined in self.type_order
                self.series_priority = {}
                self.series_type = {}
                # Series type display order; lower numbers are displayed first
                self.type_order = {
                        'NOVEL': SERIES_TYPE_FICTION,
                        'COLLECTION': SERIES_TYPE_FICTION,
                        'SERIAL': SERIES_TYPE_FICTION,
                        'OMNIBUS': SERIES_TYPE_FICTION,
                        'EDITOR': SERIES_TYPE_EDIT,
                        'ANTHOLOGY': SERIES_TYPE_ANTH,
                        'NONFICTION': SERIES_TYPE_NONFIC,
                        'SHORTFICTION': SERIES_TYPE_SF,
                        'POEM': SERIES_TYPE_POEM,
                        'ESSAY': SERIES_TYPE_ESSAY,
                        'COVERART': SERIES_TYPE_COVERART,
                        'INTERIORART': SERIES_TYPE_INTERIORART,
                        'REVIEW': SERIES_TYPE_REVIEW,
                        'INTERVIEW': SERIES_TYPE_INTERVIEW
                        }
                # Mapping between series display order and displayed section headers
                self.type_reverse = {
                        SERIES_TYPE_FICTION: 'Fiction',
                        SERIES_TYPE_EDIT: 'Magazine Editor',
                        SERIES_TYPE_ANTH: 'Anthology',
                        SERIES_TYPE_NONFIC: 'Nonfiction',
                        SERIES_TYPE_SF: 'Short Fiction',
                        SERIES_TYPE_POEM: 'Poem',
                        SERIES_TYPE_ESSAY: 'Essay',
                        SERIES_TYPE_COVERART: 'Cover Art',
                        SERIES_TYPE_INTERIORART: 'Interior Art',
                        SERIES_TYPE_REVIEW: 'Review',
                        SERIES_TYPE_INTERVIEW: 'Interview'
                        }
                # Dictionary of TOP series showing each top series' genre status
                self.series_genre = {}

                ##############################################
                # OTHER properties
                ##############################################
                # Flag indicating whether we are displaying the genre section
                # or the non-genre section
                self.nongenre = 0
                # 1/0 flag indicating whether the current title is the first within its
                # category/title type; used to decide whether to display the category line
                self.first = 1
                
        ####################################################
        #         MAIN DISPLAY METHOD
        ####################################################
        def displayBiblio(self):
                self.printHeaders()
                self.printAuthorData()
                self.loadAllAuthorTitles()
                print('<div class="ContentBox">')
                if self.canonical_titles or self.interviews:
                        self.loadParentAuthors()
                        # Load author variants for all but Alphabetical bibliographies
                        if self.page_type != 'Alphabetical':
                                self.loadVariantTitles()
                        # Load transliterated titles
                        self.loadTransliterations()
                        # Load series data for Summary pages only
                        if self.page_type == 'Summary':
                                self.loadSeriesData()
                        self.displayBiblioLinks()
                        self.printTime('Loading biblio')
                        # For all but award biblios:
                        if self.page_type != 'Award':
                                # Display genre works
                                self.displaySummary()
                                # Print interviews WITH this author
                                self.printInterviews()
                                # Display non-genre works
                                self.nongenre = 1
                                self.displaySummary()
                                self.printTime('Printing biblio')
                # If this is an alternate name, display the name of the parent author
                elif self.au_is_pseudonym and not self.selfPseudo():
                        self.printAuthorPseudo()
                # If this is not an Award page and there are stray pubs, display them
                elif self.page_type != 'Award':
                        self.printStrayPubs()

                if self.page_type == 'Award':
                        self.loadAuthorAwards()
                        self.printAwards()
                print('</div>')

                PrintTrailer('author', self.author_name, self.au_id)

        def printTime(self, message):
                # Currently disabled
                return
                # If we are on the development server, print how long it takes
                # to load and print different parts of the page
                if HTMLHOST == '127.0.0.1':
                        start = self.last_checkpoint
                        self.last_checkpoint = time()
                        print('%s %f<br>' % (message, self.last_checkpoint - start))

        ####################################################
        #         LOAD METHODS
        ####################################################
        def loadAuthorData(self):
                self.au_id = self.au_data[AUTHOR_ID]
                SQLupdateAuthorViews(self.au_id)
                self.au_trans_names = SQLloadTransAuthorNames(self.au_id)
                self.au_trans_legal_names = SQLloadTransLegalNames(self.au_id)
                self.au_emails = SQLloadEmails(self.au_id)
                self.au_webpages = SQLloadWebpages(self.au_id)
                self.au_is_pseudonym = SQLauthorIsPseudo(self.au_id)
                self.au_has_pseudonyms = SQLauthorHasPseudo(self.au_id)
                self.au_tags = SQLgetAuthorTags(self.au_id, int(self.user.id))

        def loadAllAuthorTitles(self):
                self.canonical_titles = SQLloadAllAuthorTitles(self.au_id, self.page_type, self.user.display_all_languages, self.user.languages)
                self.interviews = SQLGetInterviews(self.au_id, self.page_type)

        def selfPseudo(self):
                authors = SQLgetActualFromPseudo(self.au_id)
                for author in authors:
                        if self.author_name == author[0]:
                                return 1
                return 0

        def loadAuthorAwards(self):
                pseudonyms = SQLgetBriefPseudoFromActual(self.au_id)
                self.au_awards = SQLloadAwardsXBA(self.author_name, self.canonical_titles, pseudonyms)

        def loadParentAuthors(self):
                title_list = []
                for title in self.canonical_titles:
                        title_id = str(title[TITLE_PUBID])
                        title_list.append(title_id)
                title_string = ", ".join(title_list)
                self.parent_authors = SQLTitleListBriefAuthorRecords(title_string, self.au_id)

        def loadVariantTitles(self):
                # Retrieve all variants associated with this author, including Serials
                variants = SQLloadVTsForAuthor(self.au_id)
                
                # Create a dictionary of variant titles and a separate dictionary of
                # variant serials, both indexed by parent title ID. The logic is
                # shared with the series display code.
                (self.variant_titles, self.variant_serials) = buildVariants(self.canonical_titles, variants, self.user)

                # Build a list of parent title IDs that have pubs associated DIRECTLY with them
                parent_string = dict_to_in_clause(self.variant_titles, self.variant_serials)
                self.parent_titles_with_pubs = SQLTitlesWithPubs(parent_string)

                # Load all variants' (including serials') authors
                self.variant_authors = buildVTAuthors(self.variant_titles, self.variant_serials)

        def loadTransliterations(self):
                self.translit_titles = builtTranslitTitles(self.canonical_titles, self.variant_titles,
                                                           self.variant_serials, self.interviews)
                self.translit_authors = builtTranslitAuthors(self.parent_authors, self.variant_authors)
                
        def loadSeriesData(self):
                series_list = SQLgetSeriesData(self.au_id)
                # Retrieve all higher level super-series and put them in self.series_tree
                for series in series_list:
                        self.buildSuperSeries(series)

                # For every title with a series designation, find the type
                # and the "non-genre" status of its top level series
                for title in self.canonical_titles:
                        series_id = title[TITLE_SERIES]
                        if not series_id:
                                continue
                        # Retrieve the top parent for this title
                        top_parent = self.findTopSeries(series_id)
                        
                        # Indicate that this top series has at least one title of this type
                        if top_parent not in self.series_type:
                                self.series_type[top_parent] = {}
                        self.series_type[top_parent][title[TITLE_TTYPE]] = 1
                        
                        # If at least one title in a series tree is NOT "non-genre", then the
                        # whole series tree will be displayed in the genre section of the Summary page
                        if title[TITLE_NON_GENRE] != 'Yes':
                                self.series_genre[top_parent] = 1

                # For every top series, check which title types it contains and assign
                # appropriate display priority. The "if-elif-else" logic creates a
                # hierarchy of title types.
                for top_parent in self.series_type:
                        if 'NOVEL' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_FICTION
                        elif 'COLLECTION' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_FICTION
                        elif 'SERIAL' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_FICTION
                        elif 'EDITOR' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_EDIT
                        elif 'ANTHOLOGY' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_ANTH
                        elif 'NONFICTION' in self.series_type[top_parent]:
                                if ('SHORTFICTION' not in self.series_type[top_parent]
                                and 'POEM' not in self.series_type[top_parent]):
                                        self.series_priority[top_parent] = SERIES_TYPE_NONFIC
                                else:
                                        self.series_priority[top_parent] = SERIES_TYPE_FICTION
                        # For omnibuses, display the series in the "Fiction Series" section if
                        # there are no NOVEL, COLLECTION, EDITOR, ANTHOLOGY or NONFICTION titles
                        # in this series tree
                        elif 'OMNIBUS' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_FICTION
                        elif 'SHORTFICTION' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_SF
                        elif 'POEM' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_POEM
                        elif 'ESSAY' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_ESSAY
                        elif 'COVERART' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_COVERART
                        elif 'INTERIORART' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_INTERIORART
                        elif 'REVIEW' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_REVIEW
                        elif 'INTERVIEW' in self.series_type[top_parent]:
                                self.series_priority[top_parent] = SERIES_TYPE_INTERVIEW
                        else:
                                self.series_priority[top_parent] = SERIES_TYPE_OTHER

        def buildSuperSeries(self, series):
                series_id = series[SERIES_PUBID]
                parent_id = series[SERIES_PARENT]
                # If this series is already in the series tree, stop
                if series_id in self.series_tree:
                        return
                # Add this series to the series tree
                self.series_tree[series_id] = series
                # If this series has no super-series, we have reached the top of the tree
                if not parent_id:
                        return
                # Add this parent-child relationship to series_parents and series_children
                if parent_id not in self.series_parent:
                        self.series_parent[parent_id] = []
                self.series_parent[parent_id].append(series_id)
                self.series_child[series_id] = parent_id
                # Retrieve the super-series record for this series
                super_series = SQLget1Series(parent_id)
                # Call this method recursively for the identified super-series
                self.buildSuperSeries(super_series)

        def findTopSeries(self, series_id):
                # For a given series ID, return its top parent
                if series_id not in self.series_child:
                        return series_id
                parent_id = self.series_child[series_id]
                return self.findTopSeries(parent_id)

        ####################################################
        #         PRINT METHODS
        ####################################################

        def displaySummary(self):
                if self.nongenre and not self.displaySeparator():
                        return
                for title_type in self.ordered_title_types:
                        # Display one series type
                        if isinstance(title_type, int):
                                # Skip series display for non-Summary author pages
                                if self.page_type != 'Summary':
                                        continue
                                self.printSeriesType(title_type)
                        # Display one title type
                        else:
                                self.displayWorks(title_type)

        def displaySeparator(self):
                # Display separator only if there are non-genre
                # works that still need to be displayed
                for title in self.canonical_titles:
                        if title[TITLE_NON_GENRE] == 'Yes':
                                print('<hr>')
                                print('<div class="nongenre"><b>Non-Genre Titles</b></div><br>')
                                return 1
                return 0

        def printSeriesType(self, series_type):
                if series_type not in self.series_priority.values():
                        return
                series_type_list = []
                for series_id in self.series_priority:
                        # If we are displaying genre works and this is a non-genre
                        # series, then skip it
                        if self.nongenre == 0 and self.series_genre.get(series_id) != 1:
                                continue
                        # If we are displaying non-genre works and this is a genre
                        # series, then skip it
                        elif self.nongenre == 1 and self.series_genre.get(series_id) == 1:
                                continue
                        if self.series_priority[series_id] == series_type:
                                series_type_list.append(self.series_tree[series_id])
                
                # If there are no titles to display for this series type/genre, return
                if not series_type_list:
                        return
                # Sort the list of series of this type by name
                sorted_series_list = sorted(series_type_list, key=lambda x: x[SERIES_NAME])

                # Print series type
                print('<b>%s Series</b>' % self.type_reverse[series_type])
                print('<ul>')
                # For all but the last series, display the series and a blank line at the end
                for series_data in sorted_series_list[:-1]:
                        self.printSeries(series_data, series_type)
                        print('<br>')
                # For the last series, display the series, but no blank line
                self.printSeries(sorted_series_list[-1], series_type)
                print('</ul>')
                return

        def printSeries(self, series_data, series_type):
                series_id = series_data[SERIES_PUBID]
                if series_data[SERIES_PARENT_POSITION] == None:
                        position = ''
                else:
                        position = int(series_data[SERIES_PARENT_POSITION])
                print('<li> %s %s' % (position, ISFDBLink('pe.cgi', series_id, series_data[SERIES_NAME])))
                print('<ul>')
                counter = 0
                delete_list = []
                for title in self.canonical_titles:
                        if title[TITLE_SERIES] == series_id:
                                output = '<li>'
                                if title[TITLE_SERIESNUM] is not None:
                                        output += ' %d' % title[TITLE_SERIESNUM]
                                if title[TITLE_SERIESNUM_2] is not None:
                                        output += '.%s' % title[TITLE_SERIESNUM_2]
                                print(output)
                                displayTitle(title, self.au_id, self.parent_authors, series_type,
                                             self.variant_titles, self.variant_serials,
                                             self.parent_titles_with_pubs, self.variant_authors,
                                             self.translit_titles, self.translit_authors, self.user,
                                             self.au_data[AUTHOR_LANGUAGE], self.nongenre)
                                delete_list.insert(0, counter)
                        counter += 1
                # Remove the displayed titles from the list of titles so that they wouldn't be displayed again
                for i in delete_list:
                        del self.canonical_titles[i]

                # Check if this series is a parent of any series
                if series_id in self.series_parent:
                        # Process this series' subseries
                        sub_series_list = []
                        for sub_series in self.series_parent[series_id]:
                                sub_series_list.append(self.series_tree[sub_series])
                        if not sub_series_list:
                                return
                        # Sort sub-series by the "position" attribute, with None sorting last;
                        # then sort by series name
                        for sub_series_data in sorted(sub_series_list,
                                                      key=lambda x: (int(x[SERIES_PARENT_POSITION] or 999999), x[SERIES_NAME]),
                                                      reverse=False):
                                self.printSeries(sub_series_data, series_type)
                print('</ul>')

        def printIsPseudo(self):
                authors = SQLgetBriefActualFromPseudo(self.au_id)
                print('<li><b>Used As Alternate Name By:</b>')
                displayAuthorList(authors)

        def printHasPseudo(self):
                authors = SQLgetBriefPseudoFromActual(self.au_id)
                print('<li><b>Used These Alternate Names:</b>')
                displayAuthorList(authors)

        def printAuthorData(self):
                print('<div class="ContentBox">')
                other_authors = SQLGetDisambiguatedRecords(self.au_id, self.au_data[AUTHOR_CANONICAL], 'authors', 'author_id', 'author_canonical')
                if other_authors:
                        print('<h3>Note: There are other authors with the same name:')
                        displayAuthorList(other_authors)
                        print('</h3>')

                if self.au_data[AUTHOR_IMAGE]:
                        print('<table>')
                        print('<tr align="left">')
                        print('<td>')
                        print('<img src="%s" width="150" alt="Author Picture">' % ISFDBHostCorrection(self.au_data[AUTHOR_IMAGE].split('|')[0]))
                        print('</td>')
                        print('<td class="authorimage">')

                print('<ul>')
                print('<li><b>Author:</b> %s' % ISFDBMouseover(self.au_trans_names, self.au_data[AUTHOR_CANONICAL], ''))
                printRecordID('Author', self.au_id, self.user.id)

                if self.au_data[AUTHOR_LEGALNAME]:
                        print('<li><b>Legal Name:</b> %s' % ISFDBMouseover(self.au_trans_legal_names, self.au_data[AUTHOR_LEGALNAME], ''))

                if self.au_data[AUTHOR_BIRTHPLACE]:
                        print('<li><b>Birthplace:</b>',  ISFDBText(self.au_data[AUTHOR_BIRTHPLACE]))

                if self.au_data[AUTHOR_BIRTHDATE]:
                        print('<li><b>Birthdate:</b>', self.ConvertDate(self.au_data[AUTHOR_BIRTHDATE]))

                if self.au_data[AUTHOR_DEATHDATE]:
                        print('<li><b>Deathdate:</b>', self.ConvertDate(self.au_data[AUTHOR_DEATHDATE]))

                if self.au_data[AUTHOR_LANGUAGE]:
                        displayed_language = LANGUAGES[int(self.au_data[AUTHOR_LANGUAGE])]
                        print('<li><b>Language:</b>', displayed_language)

                if self.au_emails:
                        for email in self.au_emails:
                                print("<li><b>Email:</b>")
                                print('<a href="mailto:' +email+ '">' +email+ '</a>')

                PrintWebPages(self.au_webpages)

                if self.au_is_pseudonym and not self.selfPseudo():
                        self.printIsPseudo()

                if self.au_has_pseudonyms:
                        self.printHasPseudo()

                if self.au_data[AUTHOR_NOTE]:
                        print("<li>",FormatNote(self.au_data[AUTHOR_NOTE], 'Note', 'short', self.au_id, 'Author'))

                has_bio = SQLwikiLinkExists('Bio', self.au_data[AUTHOR_CANONICAL])
                if has_bio:
                        print("<li><b>Additional Biographical Data:</b>")
                        bio_title = 'Bio:%s' % self.au_data[AUTHOR_CANONICAL]
                        print('<a href="%s://%s/index.php/%s">%s</a>' % (PROTOCOL, WIKILOC, bio_title, bio_title))

                has_biblio = SQLwikiLinkExists('Author', self.au_data[AUTHOR_CANONICAL])
                if has_biblio:
                        print("<li><b>Additional Bibliographic Comments:</b>")
                        biblio_title = 'Author:%s' % self.au_data[AUTHOR_CANONICAL]
                        print('<a href="%s://%s/index.php/%s">%s</a>' % (PROTOCOL, WIKILOC, biblio_title, biblio_title))

                if self.au_tags:
                        print("<li><b>Author Tags:</b>")
                        print_string = ''
                        count = 0
                        total_tags = len(self.au_tags)
                        for tag in self.au_tags:
                                if count:
                                        print_string += ', '
                                print_string += ISFDBLinkNoName('tag_author.cgi', '%d+%d' % (tag[0], self.au_id), tag[1])
                                print_string += ' (%d)' % tag[2]
                                count += 1
                                if count == 20 and total_tags > 20:
                                        print_string += ' and %d additional tags. ' % (total_tags-20)
                                        print_string += ISFDBLinkNoName('authortags.cgi',
                                                                        self.au_id,
                                                                        'View all tags for %s' % self.au_data[AUTHOR_CANONICAL],
                                                                        False,
                                                                        'class="bold inverted"')
                                        break
                        print(print_string)
                
                print('</ul>')

                if self.au_data[AUTHOR_IMAGE]:
                        print('</td>')
                        print('</table>')
                        (webpage, credit, home_page, linked_page) = BuildDisplayedURL(self.au_data[AUTHOR_IMAGE])
                        print('Image supplied by <a href="%s" target="_blank">%s</a>' % (home_page, credit))
                        if linked_page:
                                print(' on <a href="%s" target="_blank">this Web page</a>' % linked_page)

                print('</div>')

        def printAuthorPseudo(self):
                authors = SQLgetBriefActualFromPseudo(self.au_id)
                if len(authors) > 0:
                        print('<b>Alternate Name. See: ')
                        displayAuthorList(authors)
                        print(AuthorSearchLink(self.author_name))
                        print('(or view all titles published using this alternate name)</a></b>')

        def printInterviews(self):
                if not self.interviews:
                        return
                print('<b>Interviews with This Author</b>')
                print('<ul>')
                for interview in self.interviews:
                        print('<li> %s ' % buildCoreTitleLine(interview, self.au_data[AUTHOR_LANGUAGE], self.translit_titles))
                        self.displayAuthorsforInterview(interview)
                print('</ul>')

        def displayAuthorsforInterview(self, title):
                interviewed_collaborators = SQLIntervieweeAuthors(title[TITLE_PUBID], self.au_id)
                interviewer_collaborators = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])
                print(" <b>by</b> ")
               
                counter = 0
                for author in interviewer_collaborators:
                        if counter:
                                print(" <b>and</b> ")
                        displayAuthorById(author[0], author[1])
                        counter += 1

                counter = 0
                output = ''
                for author in interviewed_collaborators:
                        if not counter:
                                output += "(co-interviewed with "
                        else:
                                output += " <b>and</b> "
                        output += buildAuthorById(author[0], author[1])
                        counter += 1
                if counter:
                        output +=  ")"
                print(output)

        def displayWorks(self, title_type):
                self.first = 1
                for title in self.canonical_titles:
                        if title[TITLE_TTYPE] == title_type:
                                # If we are displaying genre works and this title is non-genre, skip it
                                if self.nongenre == 0 and title[TITLE_NON_GENRE] == 'Yes':
                                        continue
                                # If we are displaying non-genre works and this title is genre, skip it
                                if self.nongenre == 1 and title[TITLE_NON_GENRE] != 'Yes':
                                        continue
                                # If this is Summary bibliography and this title is in a series and
                                # that series type is yet to be printed, then skip it
                                if self.page_type == 'Summary' and title[TITLE_SERIES] and (title[TITLE_TTYPE] in self.type_order):
                                        continue
                                if self.first:
                                        print('<b>%s</b>' % self.title_types.get(title_type))
                                        print("<ul>")
                                        self.first = 0
                                print("<li>")
                                displayTitle(title, self.au_id, self.parent_authors, SERIES_TYPE_OTHER,
                                             self.variant_titles, self.variant_serials,
                                             self.parent_titles_with_pubs, self.variant_authors,
                                             self.translit_titles, self.translit_authors, self.user,
                                             self.au_data[AUTHOR_LANGUAGE], self.nongenre)
                
                if not self.first:
                        print("</ul>")

        def printStrayPubs(self):
                pubs = SQLGetPubsByAuthor(self.au_id)
                if len(pubs):
                        print('<b>Stray Publications:</b>')
                        print('<ul>')
                        for pub in pubs:
                                print('<li>')
                                print(ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE], False, 'class = "italic"'))
                        print('</ul>')

        def displayBiblioLinks(self):
                print(self.user.translation_message(self.page_type, self))
                print('<table class=bibliolinks>')
                print('<tr>')
                print('<td><b>Other views:</b></td>')
                print_string = '<td class="authorbiblios"><b>'
                if self.page_type != 'Summary':
                        print_string += ' %s' % ISFDBLinkNoName('ea.cgi', self.au_id, 'Summary')
                if self.page_type != 'Award':
                        print_string += ' %s' % ISFDBLinkNoName('eaw.cgi', self.au_id, 'Awards')
                if self.page_type != 'Alphabetical':
                        print_string += ' %s' % ISFDBLinkNoName('ae.cgi', self.au_id, 'Alphabetical')
                if self.page_type != 'Chronological':
                        print_string += ' %s' % ISFDBLinkNoName('ch.cgi', self.au_id, 'Chronological')
                print('%s</b></td>' % print_string)
                print('</tr>')
                print('</table>')
                print('<br>')
                return

        def printHeaders(self):
                self.cgi_script = '%s.cgi' % self.page_types[self.page_type]

                author = SESSION.Parameter(0, 'unescape')

                # if the first parameter is an author ID
                if author.isdigit():
                        self.au_data = SQLloadAuthorData(int(author))
                # Otherwise use the author name to retrieve the author record
                else:
                        self.au_data = SQLgetAuthorData(author)

                if not self.au_data:
                        SESSION.DisplayError('Author not found: %s' % author)

                # Check if the user not logged in and is trying to change the default settings for translations
                if not self.user.id and len(SESSION.parameters) > 1:
                        translations = SESSION.Parameter(1, 'str', None, ('All', 'None'))
                        self.user.translation_cookies(translations)

                self.author_name = self.au_data[AUTHOR_CANONICAL]
                PrintHeader("%s Bibliography: %s" % (self.page_type, self.author_name))

                if self.author_name == 'uncredited' and self.page_type != 'Award':
                        PrintNavbar('author', author, 0, self.cgi_script, author)
                        print('<h2>%s</h2>' % 'Only %s is available for "uncredited"' % ISFDBLink('eaw.cgi', 'uncredited', 'Award Bibliography'))
                        PrintTrailer('author', author, 0)
                        sys.exit(0)

                self.loadAuthorData()

                PrintNavbar('author', self.author_name, self.au_id, self.cgi_script, self.au_id)

        def printAwards(self):
                print('<p>')
                if not self.au_awards:
                        print('<h2>No awards found for %s</h2>' % self.author_name)
                        PrintTrailer('author', self.author_name, 0)
                        sys.exit(0)
                award = awards(db)
                award.PrintAwardTable(self.au_awards)

        def ConvertDate(self, date):
                decompose = str.split(date, '-')
                ##################################
                # Day
                ##################################
                if decompose[2] == '00':
                        retval = ''
                elif decompose[2][0] == '0':
                        retval = decompose[2][1] + ' '
                else:
                        retval = decompose[2] + ' '

                ##################################
                # Month
                ##################################
                if decompose[1] == '00':
                        pass
                else:
                        retval += self.ConvertMonth(int(decompose[1])) + ' '

                if decompose[0] == '0000':
                        retval += 'unknown'
                else:
                        retval += decompose[0]
                return retval

        def ConvertMonth(self, integer_month):
                full_month_map = {
                        1  : 'January',
                        2  : 'February',
                        3  : 'March',
                        4  : 'April',
                        5  : 'May',
                        6  : 'June',
                        7  : 'July',
                        8  : 'August',
                        9  : 'September',
                        10 : 'October',
                        11 : 'November',
                        12 : 'December',
                        }
                return full_month_map[integer_month]
