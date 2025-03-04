from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley nad Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1212 $
#     Date: $Date: 2025-01-22 16:00:18 -0500 (Wed, 22 Jan 2025) $

import cgi
import sys
import re
import os
from SQLparsing import SQLgetNotes, SQLloadSeriesWebpages
from isfdb import *
from isfdblib import *
from library import *
from xml.dom import minidom
from xml.dom import Node


class series:
        def __init__(self, db):
                self.db = db
                self.used_id         = 0
                self.used_name       = 0
                self.used_trans_names = 0
                self.used_parent_id  = 0
                self.used_parent     = 0
                self.used_type       = 0
                self.used_parentposition = 0
                self.used_webpages = 0
                self.used_note_id = 0
                self.used_note = 0

                self.series_id         = ''
                self.series_name       = ''
                self.series_trans_names = []
                self.series_parent_id  = ''
                self.series_parent     = ''
                self.series_type       = ''
                self.series_parentposition = ''
                self.series_note_id = ''
                self.series_note = ''
                self.series_webpages = []

                self.error = ''

        def load(self, id, fullLoad = 1):
                self.loadCommon(id, 0, fullLoad)

        def loadXML(self, id, fullLoad = 1):
                self.loadCommon(id, 1, fullLoad)

        def loadCommon(self, id, doXML = 0, fullLoad = 1):
                if id == 0:
                        return
                record = SQLget1Series(id)
                if record:
                        if record[SERIES_PUBID]:
                                self.series_id = record[SERIES_PUBID]
                                self.used_id = 1
                        if record[SERIES_NAME]:
                                self.series_name = record[SERIES_NAME]
                                self.used_name = 1

                        res2 = SQLloadTransSeriesNames(record[PUB_SERIES_ID])
                        if res2:
                                self.series_trans_names = res2
                                self.used_trans_names = 1

                        if record[SERIES_PARENT]:
                                self.series_parent_id = record[SERIES_PARENT]
                                self.used_parent_id = 1
                                if fullLoad:
                                        self.series_parent = SQLgetSeriesName(record[SERIES_PARENT])
                                        self.used_parent = 1
                        if record[SERIES_TYPE]:
                                self.series_type = record[SERIES_TYPE]
                                self.used_type = 1
                        if record[SERIES_PARENT_POSITION]:
                                self.series_parentposition = record[SERIES_PARENT_POSITION]
                                self.used_parentposition = 1
                        if fullLoad and record[SERIES_NOTE]:
                                self.series_note_id = record[SERIES_NOTE]
                                self.used_note_id = 1
                                self.series_note = SQLgetNotes(self.series_note_id)
                                if self.series_note:
                                        self.used_note = 1

                        if fullLoad:
                                self.series_webpages = SQLloadSeriesWebpages(record[SERIES_PUBID])
                                if self.series_webpages:
                                        self.used_webpages = 1

                else:
                        print("ERROR: series record not found: ", id)
                        self.error = 'Series record not found'
                        return

        def cgi2obj(self):
                self.form = IsfdbFieldStorage()
                try:
                        self.series_id = str(int(self.form['series_id'].value))
                        self.used_id = 1
                except:
                        self.error = "Series ID must be a valid integer number"
                        return
                
                try:
                        self.series_name = XMLescape(self.form['series_name'].value)
                        self.used_name = 1
                        if not self.series_name:
                                raise
                        # Unescape the series name to ensure that the lookup finds it in the database
                        current_series = SQLGetSeriesByName(XMLunescape(self.series_name))
                        if current_series:
                                if int(self.series_id) != int(current_series[SERIES_PUBID]):
                                        self.error = "Series '%s' already exists" % current_series[SERIES_NAME]
                                        return
                except:
                        self.error = "Series name is required"
                        return

                for key in self.form:
                        if 'trans_series_names' in key:
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.series_trans_names:
                                                continue
                                        self.series_trans_names.append(value)
                                        self.used_trans_names = 1

                if 'series_parent' in self.form:
                        self.series_parent = XMLescape(self.form['series_parent'].value)
                        if self.series_parent:
                                self.used_parent = 1
                                # Check that the entered parent series is not the same as the current series
                                current_parent = SQLget1Series(self.series_id)
                                if XMLunescape(self.series_parent) == current_parent[SERIES_NAME]:
                                        self.error = 'Parent series name cannot be the same as the series name'
                                        return
                
                if 'series_type' in self.form:
                        self.series_type = XMLescape(self.form['series_type'].value)
                        if self.series_type:
                                self.used_type = 1
                
                if 'series_parentposition' in self.form:
                        self.series_parentposition = XMLescape(self.form['series_parentposition'].value)
                        if self.series_parentposition:
                                self.used_parentposition = 1
                                # Check that the entered position within the superseries is 1-9 digits
                                if not re.match(r'^[1-9]{1}[0-9]{0,8}$', self.series_parentposition):
                                        self.error = "Series Parent Position must be an integer greater than 0 and contain 1-9 digits"
                                        return
                
                if 'series_note' in self.form:
                        self.series_note = XMLescape(self.form['series_note'].value)
                        if self.series_note:
                                self.used_note = 1

                counter = 1
                for key in self.form:
                        if key[:15] == 'series_webpages':
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.series_webpages:
                                                continue
                                        self.error = invalidURL(value)
                                        if self.error:
                                                return
                                        self.series_webpages.append(value)
                                        self.used_webpages = 1

        def PrintMetaData(self, user, tags_type, seriesTags, display_type):
                from common import PrintWebPages, displayRecordList
                print('<div class="ContentBox">')
                other_series = SQLGetDisambiguatedRecords(self.series_id, self.series_name, 'series', 'series_id', 'series_title')
                if other_series:
                        print('<h3>Note: There are other series with the same name:')
                        displayRecordList('series', other_series)
                        print('</h3>')
                print('<ul>')
                trans_names = SQLloadTransSeriesNames(self.series_id)
                print('<li><b>Series: </b>%s' % ISFDBMouseover(trans_names, self.series_name, ''))
                printRecordID('Series', self.series_id, user.id)
                if self.series_parent:
                        print('<li><b>Sub-series of:</b> %s' % ISFDBLink("pe.cgi", self.series_parent_id, self.series_parent))
                        if display_type == 'grid':
                                print(ISFDBLink('seriesgrid.cgi', self.series_parent_id, '(View Issue Grid)'))

                PrintWebPages(self.series_webpages, '<li>')

                # Series Note
                if self.series_note:
                        print('<li>')
                        print(FormatNote(self.series_note, 'Note', 'short', self.series_id, 'Series'))
                
                if tags_type == 'brief':
                        self.PrintSeriesTagsBrief(seriesTags)
                else:
                        self.PrintSeriesTagsFull(seriesTags)

                print('</ul>')
                print('</div>')

        def PrintSeriesTagsBrief(self, seriesTags):
                if not seriesTags:
                        return
                print('<li><b>Series Tags:</b>')
                print_string = ''
                count = 0
                total_tags = len(seriesTags)
                for tag in seriesTags:
                        if count:
                                print_string += ', '
                        print_string += '%s (%d)' % (ISFDBLink('tag.cgi', tag[0], tag[1]), tag[2])
                        count += 1
                        if count == 20 and total_tags > 20:
                                print_string += ' and %d additional tags. ' % (total_tags-20)
                                print_string += ISFDBLink('seriestags.cgi', self.series_id,
                                                          'View all tags for %s' % self.series_name,
                                                          False, 'class="inverted bold"')
                                break
                print(print_string)

        def PrintSeriesTagsFull(self, seriesTags):
                if not seriesTags:
                        print('<h3>No tags for series %s</h3>' % self.series_name)
                else:
                        print('<li><b>Series Tags:</b>')
                        print_string = ''
                        count = 0
                        for tag in seriesTags:
                                if count:
                                        print_string += ', '
                                print_string += '%s (%d)' % (ISFDBLink('tag.cgi', tag[0], tag[1]), tag[2])
                                count += 1
                        print(print_string)
                print('<p>%s' % ISFDBLink("pe.cgi", self.series_id,
                                          'Back to the series page for %s' % self.series_name,
                                          False, 'class="bold"'))

        def BuildTreeData(self, user):
                from common import buildVariants, buildVTAuthors, builtTranslitTitles, builtTranslitAuthors
                seriesData = {}
                # Dictionary of ALL canonical titles in this series
                # and its sub-series indexed by series ID
                seriesCanonicalTitles = {}
                seriesTree = {}
                self.BuildSeriesTree(seriesData, seriesTree)

                # Now that we have all series IDs for all sub-series, retrieve
                # all of their canonical titles and put them in seriesCanonicalTitles
                series_list = []
                for series_id in seriesData:
                        series_list.append(str(series_id))
                series_string = ", ".join(series_list)
                (seriesCanonicalTitles, seriesTitlesList) = SQLLoadSeriesListTitles(series_string)
                if not seriesCanonicalTitles:
                        return (None, None, None, None, None, None, None, None, None, None, None)

                # Now that we have all the titles for this series and its subseries,
                # retrieve related authors and VTs
                title_list = []
                for series_id in seriesCanonicalTitles:
                        for title in seriesCanonicalTitles[series_id]:
                                title_list.append(str(title[TITLE_PUBID]))
                title_string = ", ".join(title_list)
                # Retrieve the canonical titles' authors
                parentAuthors = SQLTitleListBriefAuthorRecords(title_string)
                # Retrieve the canonical titles' VTs
                variants = SQLloadVTsForTitleList(title_string)
                # Retrieve distionaries of variant titles and variant serials for this series
                (variantTitles, variantSerials) = buildVariants(seriesTitlesList, variants, user)
                # Retrieve all user tags for this series
                seriesTags = SQLgetTitleListTags(title_string, user.id)
                
                # Build a list of parent title IDs that have pubs associated DIRECTLY with them
                parent_string = dict_to_in_clause(variantTitles, variantSerials)
                parentsWithPubs = SQLTitlesWithPubs(parent_string)

                # Load all variants' (including serials') authors
                variantAuthors = buildVTAuthors(variantTitles, variantSerials)

                # Load all transliterated titles
                translit_titles = builtTranslitTitles(seriesTitlesList, variantTitles, variantSerials)

                # Load all transliterated authors
                translit_authors = builtTranslitAuthors(parentAuthors, variantAuthors)

                return (seriesData, seriesCanonicalTitles, seriesTree, parentAuthors,
                        seriesTags, variantTitles, variantSerials, parentsWithPubs, variantAuthors,
                        translit_titles, translit_authors)

        def BuildSeriesTree(self, seriesData, seriesTree):
                seriesData[self.series_id] = self
                seriesTree[self.series_id] = SQLFindSeriesChildren(self.series_id)
                for child_id in seriesTree[self.series_id]:
                        series1 = series(db)
                        # Do a barebones load of the child series to improve performance
                        series1.load(child_id, 0)
                        series1.BuildSeriesTree(seriesData, seriesTree)
