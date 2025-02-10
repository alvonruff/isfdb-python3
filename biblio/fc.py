#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1172 $
#     Date: $Date: 2024-04-03 20:46:06 -0400 (Wed, 03 Apr 2024) $


import sys
import string

from isfdb import *
from SQLparsing import *
from common import *
from library import *
from login import User


class PublicationMonth:
        def __init__(self):
                # List of publication IDs
                self.pub_ids = []
                # Dictionary of publications indexed by pub_id
                self.pubs = {}
                # List of publication bodies
                self.pub_list = []
                # Dictionary of pub title transliterations indexed by publication ID
                self.pub_trans = {}

                self.publisher_ids = []
                self.publishers = {}
                # Dictionary of publisher name transliterations indexed by publisher ID
                self.publisher_trans = {}

                self.pub_series_ids = []
                self.pub_series = {}
                # Dictionary of publication series name transliterations indexed by pub series ID
                self.pub_series_trans = {}

                self.pub_authors = {}
                self.referral_titles = {}
                self.series = {}
                self.tags = {}
                
                self.pub_id = ''
                self.first_author_id = ''
                self.title_id = ''
                self.title_data = []
                self.title_genre = 'Adult'

                date = localtime()
                self.current_year = str(date[0])
                self.current_month = date[1]
                self.current_day = date[2]
                self.target_year = self.current_year
                self.target_month = self.current_month
                self.target_day = self.current_day
                
                self.sorting = 'date'
                
                self.adult = []
                self.ya = []
                self.romance = []

                self.bgcolor = 1

                self.user = User()
                self.user.load()

        def parseArguments(self):
                self.sorting = SESSION.Parameter(0, 'str', 'date', ('date','author'))
                self.target_month = SESSION.Parameter(1, 'int', self.target_month)
                self.target_year  = SESSION.Parameter(2, 'int', self.target_year)
                if len(SESSION.parameters) > 1:
                        default_start_day = 0
                else:
                        default_start_day = self.target_day
                self.target_day   = SESSION.Parameter(3, 'int', default_start_day)

        def load_data(self):
                self.loadPubs()
                if not self.pub_list:
                        return
                self.loadPublishers()
                self.loadPubSeries()
                self.loadPubAuthors()
                self.loadTitles()
                self.loadSeries()
                self.loadTags()

        def loadPubs(self):
                # Retrieve a list of all pubs published during the requested time period
                self.pub_list = SQLGetForthcoming(self.target_month, self.target_year, self.target_day, 1)
                if not self.pub_list:
                        return

                for pub in self.pub_list:
                        pub_id = pub[PUB_PUBID]
                        # Populate a dictionary of pubs indexed by pub_id
                        self.pubs[pub_id] = pub
                        # Populate a list of pub IDs
                        self.pub_ids.append(pub_id)

                # Populate a dictionary of pub title transliterations indexed by publication ID
                self.pub_trans = SQLLoadTransPubTitlesList(self.pub_ids)

        def loadPublishers(self):
                for pub in self.pub_list:
                        if pub[PUB_PUBLISHER]:
                                publisher_id = pub[PUB_PUBLISHER]
                                if publisher_id not in self.publisher_ids:
                                        self.publisher_ids.append(publisher_id)
                self.publishers = SQLGetPublisherList(self.publisher_ids)

                # Populate a dictionary of publisher name transliterations indexed by publisher ID
                self.publisher_trans = SQLLoadTransPublisherList(self.publisher_ids)

        def loadPubSeries(self):
                for pub in self.pub_list:
                        if pub[PUB_SERIES]:
                                pub_series_id = pub[PUB_SERIES]
                                if pub_series_id not in self.pub_series_ids:
                                        self.pub_series_ids.append(pub_series_id)
                self.pub_series = SQLGetPubSeriesList(self.pub_series_ids)

                # Populate a dictionary of pub series name transliterations indexed by pub series ID
                self.pub_series_trans = SQLLoadTransPubSeriesList(self.pub_series_ids)

        def loadPubAuthors(self):
                self.pub_authors = SQLPubListBriefAuthorRecords(self.pub_ids)

        def loadTitles(self):
                self.referral_titles = SQLgetTitleReferralList(self.pub_list, 1)
                # Retrieve all parent titles
                parent_ids = []
                for pub_id in self.referral_titles:
                        title_data = self.referral_titles[pub_id]
                        parent_id = title_data[TITLE_PARENT]
                        if parent_id not in parent_ids:
                                parent_ids.append(parent_id)

                # Replace variant titles with their parents
                if parent_ids:
                        parent_titles = SQLloadTitleList(parent_ids)
                        for pub_id in self.referral_titles:
                                title_data = self.referral_titles[pub_id]
                                parent_id = title_data[TITLE_PARENT]
                                if parent_id in parent_titles:
                                        parent_data = parent_titles[parent_id]
                                        self.referral_titles[pub_id] = parent_data

        def loadSeries(self):
                # Load series data for referral titles
                series_ids = []
                for pub_id in self.referral_titles:
                        title_data = self.referral_titles[pub_id]
                        series_id = title_data[TITLE_SERIES]
                        if series_id and series_id not in series_ids:
                                series_ids.append(series_id)
                if series_ids:
                        self.series = SQLLoadSeriesFromList(series_ids)

        def loadTags(self):
                # Retrieve user_specific tags for referral titles
                title_ids = []
                for pub_id in self.referral_titles:
                        title_data = self.referral_titles[pub_id]
                        title_id = title_data[TITLE_PUBID]
                        if title_id not in title_ids:
                                title_ids.append(title_id)
                if title_ids:
                        self.tags = SQLgetTagsByTitleForTitleList(title_ids, self.user.id)

        def PrintPage(self):
                print '<hr>'
                print '<h2 class="centered">Upcoming Months</h2>'
                self.PrintMonthLine()
                print '<hr>'

                if not self.pubs:
                        print '<h1 class="centered">No books available for %s %s</h1>' % (ISFDBmonthmap[self.target_month], self.target_year)
                else:
                        if self.sorting == 'date':
                                self.SortByDateAndGenre()
                        else:
                                self.SortByAuthor()

                print '<hr>'
                self.PrintMonthLine()
                PrintTrailer('forthcoming', 0, 0)

        def PrintMonthLine(self):
                count = 0
                print '<table class="generic_centered_table">'
                print '<tr class="generic_centered_header">'
                TmpMonth = self.current_month
                TmpYear = int(self.current_year)
                while count < 12:
                        if self.current_month == TmpMonth:
                                full = ' (Full)'
                        else:
                                full = ''
                        print '<td>%s</td>' % ISFDBLinkNoName('fc.cgi',
                                                              'date+%s+%d' % (TmpMonth, TmpYear),
                                                              '%s %d%s' % (ISFDBmonthmap[TmpMonth], TmpYear, full),
                                                              False, 'class = "bold"')
                        TmpMonth += 1
                        if TmpMonth > 12:
                                TmpMonth = 1
                                TmpYear += 1
                        count += 1
                print '</tr>'
                print '</table>'

        def SortByAuthor(self):
                self.sorting = 'author'
                # Create a three level dictionary of pubs sorted by pub author's last name, full name and pub ID
                pub_dict = AutoVivification()

                # Iterate over the list of publications for this month
                for pub_record in self.pub_list:
                        pub_id = pub_record[PUB_PUBID]
                        publisher_name = self.publishers.get(pub_record[PUB_PUBLISHER], '')
                        pub_series_name = self.pub_series.get(pub_record[PUB_SERIES], '')
                        referral_title = self.referral_titles.get(pub_id, None)

                        # Get all authors for this publication
                        authors = self.pub_authors[pub_id]
                        # Iterate over all authors for this pub and save the ID of one of the pub's authors
                        for author in authors:
                                author_id = author[0]
                                canonical_name = author[1]
                                last_name = author[2]
                                pub_dict[last_name][canonical_name][pub_id] = author_id

                if self.target_day == 0:
                        print '<h1 class="centered"> All Books for %s %s by Author</h1>' % (ISFDBmonthmap[self.target_month], self.target_year)
                        print ISFDBLinkNoName('fc.cgi', 'date+%d+%s' % (self.target_month, self.target_year), 'Sort by Genre and Date')
                else:
                        print '<h1 class="centered"> Future Books for %s %s by Author (Information based on pre-publication data and subject to change)</h1>' % (ISFDBmonthmap[self.target_month], self.target_year)
                        print ISFDBLinkNoName('fc.cgi', 'date', 'Sort by Genre and Date')
                print '<br>'
                self.PrintTableHeader()

                # Now that the dictionary has been populated, traverse it alphabetically
                for last_name in sorted(pub_dict, key=lambda s: s.lower()):
                        for canonical_name in sorted(pub_dict[last_name], key=lambda s: s.lower()):
                                for pub_id in pub_dict[last_name][canonical_name]:
                                        self.first_author_id = pub_dict[last_name][canonical_name][pub_id]
                                        self.pub_id = pub_id
                                        self.PrintOneRecord()
                print '</table>'
                return

        def SortByDateAndGenre(self):
                self.sorting = 'date'
                for pub_record in self.pub_list:
                        self.pub_id = pub_record[PUB_PUBID]

                        self.GetTitleGenre()
                        
                        if self.title_genre == 'Adult':
                                self.adult.append(self.pub_id)
                        elif self.title_genre == 'YA':
                                self.ya.append(self.pub_id)
                        else:
                                self.romance.append(self.pub_id)

                # Print out the target month
                if self.target_day == 0:
                        print '<h1 class="centered"> All Books for %s %s by Genre and Date</h1>' % (ISFDBmonthmap[self.target_month], self.target_year)
                        print ISFDBLinkNoName('fc.cgi', 'author+%d+%s' % (self.target_month, self.target_year), 'Sort by Author')
                else:
                        print '<h1 class="centered"> Future Books for %s %s by Genre and Date (Information based on pre-publication data and subject to change)</h1>' % (ISFDBmonthmap[self.target_month], self.target_year)
                        print ISFDBLinkNoName('fc.cgi', 'author', 'Sort by Author')
                print '<br>Or jump to:'
                print '<ul>'
                if self.adult:
                        print '<li><a href="#adult">Adult</a>'
                if self.ya:
                        print '<li><a href="#ya">Young Adult and Juvenile</a>'
                if self.romance:
                        print '<li><a href="#romance">Romance</a>'
                print '</ul>'

                if self.adult:
                        self.PrintGenre("adult", "Adult", self.adult)
                if self.ya:
                        self.PrintGenre("ya", "Young Adult and Juvenile", self.ya)
                if self.romance:
                        self.PrintGenre("romance", "Romance", self.romance)

        def PrintGenre(self, html_id, displayed_genre, pub_ids):
                print '<h2 id = "%s" class="centered">%s</h2>' % (html_id, displayed_genre)
                self.PrintTableHeader()
                
                for pub_id in pub_ids:
                        self.pub_id = pub_id
                        self.PrintOneRecord()
                print '</table>'

        def PrintTableHeader(self):
                print '<table class="generic_table">'
                print '<tr class="generic_centered_header">'
                if self.sorting == 'author':
                        print "<td><b>Author(s)</b></td>"
                        print "<td><b>Title %s Series</b></td>" % SESSION.ui.bullet
                print "<td><b>Date</b></td>"
                if self.sorting == 'date':
                        print "<td><b>Author(s)</b></td>"
                        print "<td><b>Title %s Series</b></td>" % SESSION.ui.bullet
                print "<td><b>Reprint?</b></td>"
                print "<td><b>Genre/Tags</b></td>"
                print "<td><b>Type</b></td>"
                print "<td><b>Publisher</b></td>"
                print "<td><b>ISBN/Catalog ID</b></td>"
                print "<td><b>Price</b></td>"
                print "<td><b>Pages</b></td>"
                print "<td><b>Format</b></td>"
                print "</tr>"

        def PrintOneRecord(self):
                from isbn import convertISBN
                pub = self.pubs[self.pub_id]
                publisher_id = pub[PUB_PUBLISHER]
                publisher_data = ''
                publisher_name = ''
                if publisher_id:
                        publisher_name = self.publishers[publisher_id]
                pub_series_id = pub[PUB_SERIES]
                pub_series_number = pub[PUB_SERIES_NUM]
                pub_series_data = ''
                pub_series_name = ''
                if pub_series_id:
                        pub_series_name = self.pub_series[pub_series_id]
                self.title_data = self.referral_titles.get(self.pub_id, None)

                if self.bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'
                self.bgcolor ^= 1

                # If sorting by author, print the authors and title first
                if self.sorting == 'author':
                        self.PrintAuthorAndTitle()

                print '<td>'
                print pub[PUB_YEAR]
                print '</td>'

                if self.sorting == 'date':
                        self.PrintAuthorAndTitle()

                # Determine if the book is a reprint
                reprint = '&nbsp;'
                # Magazine (EDITOR) do not allow reprints
                title = self.title_data
                if title and (title[TITLE_TTYPE] != 'EDITOR'):
                        if int(title[TITLE_YEAR][0:4]) < int(pub[PUB_YEAR][0:4]):
                                reprint = 'REPRINT'
                        elif int(title[TITLE_YEAR][0:4]) == int(pub[PUB_YEAR][0:4]):
                                if title[TITLE_YEAR][5:7] != '00':
                                        if pub[PUB_YEAR][5:7] != '00':
                                                if int(title[TITLE_YEAR][5:7]) < int(pub[PUB_YEAR][5:7]):
                                                        reprint = 'REPRINT'

                print '<td>'
                print reprint
                print '</td>'

                print '<td>'
                output = ''
                if self.title_data:
                        self.title_id = self.title_data[TITLE_PUBID]
                        if self.title_id in self.tags:
                                for tag in self.tags[self.title_id]:
                                        if output:
                                                output += ', '
                                        output += ISFDBLink('tag.cgi', tag[TAG_ID], tag[TAG_NAME])
                if output:
                        print output
                else:
                        print "&nbsp;"
                print '</td>'

                print '<td>'
                if pub[PUB_CTYPE]:
                        print pub[PUB_CTYPE].capitalize()
                else:
                        print "&nbsp;"
                print '</td>'
                
                print '<td>'
                if publisher_id:
                        output = ISFDBLink('publisher.cgi', publisher_id, publisher_name, False, '', self.publisher_trans)
                        if pub_series_id:
                                output += ' (%s' % ISFDBLink('pubseries.cgi', pub_series_id, pub_series_name, False, '', self.pub_series_trans)
                                if pub_series_number:
                                        output += ' #%s' % pub_series_number
                                output += ')'
                        print output
                else:
                        print "&nbsp;"
                print '</td>'

                printISBNCatalog(pub)

                print '<td>'
                if pub[PUB_PRICE]:
                        print ISFDBPrice(pub[PUB_PRICE], 'left')
                else:
                        print "&nbsp;"
                print '</td>'

                print '<td>'
                if pub[PUB_PAGES]:
                        print pub[PUB_PAGES]
                else:
                        print "&nbsp;"
                print '</td>'

                print '<td>'
                if pub[PUB_PTYPE]:
                        print ISFDBPubFormat(pub[PUB_PTYPE], 'left')
                else:
                        print "&nbsp;"
                print '</td>'
                print '</tr>'
                return

        def PrintAuthorAndTitle(self):
                # Print the book's authors
                authors = self.pub_authors[self.pub_id]
                if self.sorting == 'author':
                        # Display the "primary" author name first
                        new_authors = []
                        for author in authors:
                                if author[0] != self.first_author_id:
                                        new_authors.append(author)
                                else:
                                        first_author = author
                        authors = []
                        authors.append(first_author)
                        authors = authors + new_authors
                print '<td>'
                displayAuthorList(authors)
                print '</td>'

                # Print the title and series for the book
                pub = self.pubs[self.pub_id]
                print '<td>'
                output = ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE], False, '', self.pub_trans)
                title = self.title_data
                if title:
                        series_id = title[TITLE_SERIES]
                        if series_id:
                                series = self.series[series_id]
                                output += ' %s %s' % (SESSION.ui.bullet, ISFDBLink('pe.cgi',
                                                                                   series[SERIES_PUBID],
                                                                                   series[SERIES_NAME],
                                                                                   False, 'class = "italic"'))
                                if title[TITLE_SERIESNUM] is not None:
                                        output += ' #%s' % (title[TITLE_SERIESNUM])
                                        if title[TITLE_SERIESNUM_2] is not None:
                                                output += '.%s' % (title[TITLE_SERIESNUM_2])
                                elif title[TITLE_CONTENT]:
                                        output += ' /%s' % (title[TITLE_CONTENT])
                print output
                print '</td>'

        def GetTitleGenre(self):
                self.title_genre = 'Adult'
                pub = self.pubs[self.pub_id]
                publisher_name = self.publishers.get(pub[PUB_PUBLISHER], '')
                
                # First use publisher name to determine whether the book is adult, YA or romance
                if publisher_name:
                        # Define substrings within publisher names that inicate YA/romance publishers
                        partial_ya = ('young', 'children', 'teen', 'scholastic', 'atheneum',
                                         'stone arch', 'greenwillow', 'aladdin', 'yearling',
                                         'david fickling', 'lerner','balzer +', 'simon pulse',
                                         'chicken house', 'amulet books', 'mcelderry', 'katherine tegen',
                                         'square fish', 'candlewick', 'feiwel', 'philomel', 'razorbill')
                        exact_ya = ('point', 'starscape', 'flux')
                        partial_romance = ('love spell', 'silhouette', 'hqn', 'harlequin', 'm&b')
                        exact_romance = ('mira', 'mira ink', 'mira uk')
                        check = publisher_name.lower()
                        for substring in partial_ya:
                                if substring in check:
                                        self.title_genre = 'YA'
                                        return
                        for substring in exact_ya:
                                if substring == check:
                                        self.title_genre = 'YA'
                                        return

                        for substring in partial_romance:
                                if substring in check:
                                        self.title_genre = 'romance'
                                        return
                        for substring in exact_romance:
                                if substring == check:
                                        self.title_genre = 'romance'
                                        return

                self.title_data = self.referral_titles.get(self.pub_id, None)
                # If the pub doesn't have a referral title, then we are done
                if not self.title_data:
                        return
                self.title_id = self.title_data[TITLE_PUBID]

                # If there are no tags for this title, then we are done
                if self.title_id not in self.tags:
                        return

                # Use this title's tags to determine whether the book is YA or romance
                tags = self.tags[self.title_id]

                for tag in tags:
                        ya_tags = ('young', 'juvenile', 'children')
                        romance_tags = ('romance', 'erotica')
                        tag_text = tag[TAG_NAME].lower()
                        for ya_tag in ya_tags:
                                if ya_tag in tag_text:
                                        self.title_genre = 'YA'
                                        return
                        for romance_tag in romance_tags:
                                if romance_tag in tag_text:
                                        self.title_genre = 'romance'
                                        return


#==========================================================
#                       M A I N
#==========================================================

if __name__ == '__main__':

        pub_month = PublicationMonth()
        pub_month.parseArguments()
        PrintHeader('Monthly Bibliography')
        PrintNavbar('forthcoming', 0, 0, 0, 0)
        pub_month.load_data()
        pub_month.PrintPage()
