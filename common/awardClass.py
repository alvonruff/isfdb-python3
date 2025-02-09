#
#     (C) COPYRIGHT 2005-2025   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1220 $
#     Date: $Date: 2025-02-03 16:47:16 -0500 (Mon, 03 Feb 2025) $

import cgi
import sys
import os
import MySQLdb
import urllib
from isfdb import *
from library import *
from xml.dom import minidom
from xml.dom import Node
from SQLparsing import *

class awardShared:
        def __init__(self):
                pass

        @staticmethod
        def SpecialAwards():
                return {
                        '71' : 'No Winner -- Insufficient Votes',
                        '72' : 'Not on ballot -- Insufficient Nominations',
                        '73' : 'No Award Given This Year',
                        '81' : 'Withdrawn',
                        '82' : 'Withdrawn -- Nomination Declined',
                        '83' : 'Withdrawn -- Conflict of Interest',
                        '84' : 'Withdrawn -- Official Publication in a Previous Year',
                        '85' : 'Withdrawn -- Ineligible',
                        '90' : 'Finalists',
                        '91' : 'Made First Ballot',
                        '92' : "Preliminary Nominees",
                        '93' : 'Honorable Mentions',
                        '98' : 'Early Submissions',
                        '99' : 'Nominations Below Cutoff',
                }
        
        def PrintOneAwardList(self, awards):
                # Print all awards for one list of awards. The awards may be for one award type/year, one category or one category/year.
                special_awards = self.SpecialAwards()
                last_level = 1
                for level in range(1,100):
                        for award in awards:
                                if int(award[AWARD_LEVEL]) == level:
                                        # Skip any records whose level is over 70 and is not a recognized "special" level
                                        if level > 70 and str(level) not in special_awards:
                                                pass
                                        else:
                                                # If this is the first occurrence of a new "special" level, display its special message
                                                if str(level) in special_awards and level != last_level:
                                                        print '<tr>'
                                                        print '<td colspan=3><i>--- ' + special_awards[str(level)] + ' -------</i></td>'
                                                        print '</tr>'
                                                self.PrintOneAward(award)
                                        last_level = level

        def PrintOneAward(self, record):
                from awardClass import awards
                award = awards(db)
                award.load(record[AWARD_ID])

                print '<tr>'
                css_class = ''
                # Do not display the award level of "special" levels; they are displayed separately as headers
                if int(award.award_level) > 70:
                        award_link = '*'
                elif award.award_type_poll == 'Yes':
                        award_link = award.award_level
                else:
                        if award.award_level == '1':
                                award_link = 'Win'
                                css_class = 'class="bold"'
                        else:
                                award_link = 'Nomination'

                print('<td>%s</td>' % award.BuildDisplayLevel(award_link, css_class))
                
                print '<td>'

                if award.award_title == 'untitled':
                        print '----'
                else:
                        if award.title_id:
                                # Retrieve the title data associated with this award
                                title = SQLloadTitle(award.title_id)
                                print ISFDBLink('title.cgi', award.title_id, title[TITLE_TITLE], False, css_class)
                                if title[TITLE_PARENT]:
                                        parent = SQLloadTitle(title[TITLE_PARENT])
                                        if title[TITLE_LANGUAGE] and parent[TITLE_LANGUAGE] and title[TITLE_LANGUAGE] != parent[TITLE_LANGUAGE]:
                                                print ' (translation of %s)' % ISFDBLink('title.cgi', parent[TITLE_PUBID], parent[TITLE_TITLE], False, css_class)
                                        elif parent[TITLE_TITLE] != title[TITLE_TITLE]:
                                                print ' (variant of %s)' % ISFDBLink('title.cgi', parent[TITLE_PUBID], parent[TITLE_TITLE], False, css_class)
                        else:
                                print ISFDBText(award.award_title)

                if award.award_movie:
                        print '(%s)' %IMDBLink(award.award_movie)
                print '</td>'

                print '<td>'
                award.PrintAwardAuthors()
                print '</td>'
                print '</tr>'


class awards(awardShared):
        def __init__(self, db):
                self.db = db
                self.used_id         = 0
                self.used_title      = 0
                self.used_year       = 0
                self.used_cat_id     = 0
                self.used_cat_name   = 0
                self.used_level             = 0
                self.used_movie             = 0
                self.used_title_id   = 1
                self.num_authors     = 0
                self.used_type_name  = 0
                self.used_type_short_name = 0
                self.used_type_id    = 0
                self.used_type_poll  = 0
                self.used_note_id    = 0
                self.used_note       = 0
                
                self.award_authors    = []
                self.award_id         = ''
                self.title_id         = ''
                self.award_title      = ''
                self.award_year       = ''
                self.award_cat_id     = ''
                self.award_cat_name   = ''
                self.award_level      = ''
                self.award_displayed_level = ''
                self.award_movie      = ''
                self.award_type_name  = ''
                self.award_type_short_name = ''
                self.award_type_id    = ''
                self.award_type_poll  = ''
                self.award_note_id    = ''
                self.award_note       = ''
                self.special_awards   = self.SpecialAwards()

                self.error = ''

        def authors(self):
                counter = 0
                retval = ''
                while counter < self.num_authors:
                        if counter == 0:
                                retval = self.award_authors[counter]
                        else:
                                retval += "+" + self.award_authors[counter]
                        counter += 1
                return retval

        def load(self, id):
                self.loadCommon(id, 0)

        def loadXML(self, id):
                self.loadCommon(id, 1)

        def loadCommon(self, id, doXML):
                if id == 0:
                        return
                award = SQLloadAwards(id)
                if award:
                        award = award[0]
                        if award[AWARD_ID]:
                                self.award_id = award[AWARD_ID]
                                self.used_id = 1
                                title = SQLloadTitleFromAward(self.award_id)
                                if title:
                                        self.title_id = title[0][TITLE_PUBID]
                                        self.used_title_id = 1
                        if award[AWARD_TITLE]:
                                self.award_title = award[AWARD_TITLE]
                                self.used_title = 1
                        if award[AWARD_YEAR]:
                                self.award_year = award[AWARD_YEAR]
                                self.used_year = 1
                        if award[AWARD_TYPEID]:
                                self.award_type_id = award[AWARD_TYPEID]
                                self.used_type_id = 1
                                award_type = SQLGetAwardTypeById(self.award_type_id)
                                self.award_type_name = award_type[AWARD_TYPE_NAME]
                                self.award_type_short_name = award_type[AWARD_TYPE_SHORT_NAME]
                                self.used_type_name = 1
                                self.award_type_poll = award_type[AWARD_TYPE_POLL]
                                self.used_type_poll = 1
                        if award[AWARD_LEVEL]:
                                self.award_level = award[AWARD_LEVEL]
                                self.used_level = 1
                                self.award_displayed_level = ''
                                if int(self.award_level) > 70:
                                        self.award_displayed_level = self.special_awards[self.award_level]
                                elif self.award_type_poll == 'Yes':
                                                self.award_displayed_level = self.award_level
                                else:
                                        if int(self.award_level) == 1:
                                                self.award_displayed_level = 'Win'
                                        else:
                                                self.award_displayed_level = 'Nomination'
                        if award[AWARD_CATID]:
                                self.award_cat_id = award[AWARD_CATID]
                                self.used_cat_id = 1
                                self.award_cat_name = SQLGetAwardCatById(self.award_cat_id)[AWARD_CAT_NAME]
                                self.used_cat_name = 1
                        if award[AWARD_MOVIE]:
                                self.award_movie = award[AWARD_MOVIE]
                                self.used_movie = 1
                        if award[AWARD_AUTHOR]:
                                authors = string.split(award[AWARD_AUTHOR], '+')
                                self.num_authors = 0
                                for author in authors:
                                        self.award_authors.append(author)
                                        self.num_authors += 1
                        if award[AWARD_NOTEID]:
                                note = SQLgetNotes(award[AWARD_NOTEID])
                                if note:
                                        self.award_note_id = award[AWARD_NOTEID]
                                        self.used_note_id = 1
                                        self.award_note = note
                                        self.used_note = 1

                else:
                        print "ERROR: award record not found: ", id
                        self.error = 'Award record not found'
                        return

        def cgi2obj(self):
                self.form = cgi.FieldStorage()
                if self.form.has_key('award_id'):
                        self.award_id = self.form['award_id'].value
                        self.used_id = 1

                # title_id is only present for Add (as opposed to Edit) Award submissions
                if self.form.has_key('title_id'):
                        self.title_id = self.form['title_id'].value
                        self.used_title_id = 1
                
                if self.form.has_key('award_title'):
                        self.award_title = XMLescape(self.form['award_title'].value)
                        self.used_title = 1
                else:
                        self.award_title = 'untitled'
                        self.used_title = 1

                self.num_authors = 0
                self.award_authors = []
                counter = 0
                while counter < 100:
                        if self.form.has_key('title_author'+str(counter+1)):
                                value = XMLescape(ISFDBnormalizeAuthor(self.form['title_author'+str(counter+1)].value))
                                self.error = ISFDBAuthorError(value)
                                if self.error:
                                        return
                                if value and (value not in self.award_authors):
                                        self.award_authors.append(value)
                                        self.num_authors += 1
                        counter += 1

                if self.form.has_key('award_year'):
                        year = self.form['award_year'].value
                        # Take the submitted value and convert it to the standard YYYY-MM-DD format
                        self.award_year = ISFDBnormalizeDate(year)
                        if self.award_year == '0000-00-00':
                                self.error = "For awards, 0000 years are not allowed."
                                return
                        if self.award_year[5:] != '00-00':
                                self.error = "Bad YEAR value. Only YYYY and YYYY-00-00 values are valid for awards."
                                return
                        self.used_year = 1
                else:
                        self.error = "Missing YEAR value"
                        return

                if self.form.has_key('award_type_id'):
                        self.award_type_id = self.form['award_type_id'].value
                        self.used_type_id = 1
                else:
                        self.error = "Missing Award Type ID"
                        return

                if self.form.has_key('award_cat_id'):
                        self.award_cat_id = self.form['award_cat_id'].value
                        self.used_cat_id = 1
                else:
                        self.error = "Missing Award Category ID"
                        return

                if self.form.has_key('LEVEL'):
                        if self.form['LEVEL'].value == 'WIN':
                                self.award_level = '1'
                                self.used_level = 1
                        elif self.form['LEVEL'].value == 'NOM':
                                self.award_level = '9'
                                self.used_level = 1
                        elif self.form['LEVEL'].value == 'LEVEL':
                                if self.form.has_key('award_level'):
                                        try:
                                                self.award_level = self.form['award_level'].value
                                                self.used_level = 1
                                                # Check that the entered value is between 1 and 70
                                                if int(self.award_level) > 70 or int(self.award_level) < 1:
                                                        raise
                                        except:
                                                self.error = "Award level must be an integer number between 1 and 70"
                                                return
                                else:
                                        self.error = "Missing award level value"
                                        return
                        elif self.form['LEVEL'].value == 'SPECIAL':
                                if self.form.has_key('award_special'):
                                        try:
                                                self.award_level = self.form['award_special'].value
                                                self.used_level = 1
                                                # Check that the entered value is a recognized "special" value
                                                if self.award_level not in self.special_awards:
                                                        raise
                                        except:
                                                self.error = "Only displayed special award levels are supported"
                                                return
                                else:
                                        self.error = "Missing special award level value"
                                        return

                if self.form.has_key('award_movie'):
                        self.award_movie = XMLescape(self.form['award_movie'].value)
                        if self.award_movie[:2] != 'tt':
                                self.error = "IMDB title codes must start with 'tt'. See mouseover Help for details"
                                return
                        self.used_movie = 1

                if self.form.has_key('award_note'):
                        self.award_note = XMLescape(self.form['award_note'].value)
                        self.used_note = 1

        def PrintAwardTable(self, award_list, print_title = 1, print_authors = 0, limit = 10000):
                print '<table>'
                print '<tr class="table2">'
                print '<th>Place</th>'
                print '<th>Year and Award</th>'
                if print_title:
                        print '<th>Title</th>'
                if print_authors:
                        print '<th>Author(s)</th>'
                print '<th>Category</th>'
                print '</tr>'
                counter = 1
                bgcolor = 0
                for fullaward in award_list:
                        award = awards(db)
                        award.load(fullaward[AWARD_ID])
                        award.PrintAwardRow(print_title, print_authors, bgcolor)
                        counter += 1
                        if counter > limit:
                                break
                        bgcolor ^= 1
                print '</table>'

        def PrintAwardRow(self, print_title, print_authors, bgcolor):
                print '<tr class="table%d">' % (bgcolor+1)
                # Display the award level/place
                print '<td>'
                self.PrintLevel(print_title)
                print '</td>'
                # Display the award year and link it to the annual award page for that year/award
                self.PrintYear()
                if print_title:
                        print '<td>'
                        self.PrintTitle()
                        print '</td>'
                if print_authors:
                        print '<td>'
                        self.PrintAwardAuthors()
                        print '</td>'
                # Link to all awards for this category for this year
                print '<td>%s</td>' % ISFDBLink('award_category_year.cgi', '%s+%s' % (self.award_cat_id, self.award_year[:4]), self.award_cat_name)
                print '</tr>'

        def PrintYear(self):
                print '<td>'
                year = self.award_year[:4]
                print ISFDBLink('ay.cgi', '%s+%s' % (self.award_type_id, year), '%s %s' % (year, self.award_type_short_name))
                print '</td>'

        def PrintLevel(self, print_title):
                css_class = ''
                if int(self.award_level) > 70:
                        level = self.special_awards[self.award_level]
                        css_class = 'italic'
                elif self.award_type_poll == 'Yes':
                        if int(self.award_level) == 1:
                                level = '1'
                                css_class = 'bold'
                        else:
                                level = self.award_level
                else:
                        if int(self.award_level) == 1:
                                level = 'Win'
                                css_class = 'bold'
                        else:
                                level = 'Nomination'
                if css_class:
                        argument = 'class="%s"' % css_class
                else:
                        argument = ''
                print self.BuildDisplayLevel(level, argument)
                # For title-based awards given to VTs, display the VT
                if not print_title and self.title_id:
                        title = SQLloadTitle(self.title_id)
                        if title[TITLE_PARENT]:
                                parent = SQLloadTitle(title[TITLE_PARENT])
                                if parent[TITLE_TITLE] != title[TITLE_TITLE]:
                                        print '(as %s)' % ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE])

        def BuildDisplayLevel(self, level, css_class):
                level_link = ISFDBLink('award_details.cgi', self.award_id, level, False, css_class)
                if self.award_note:
                        formatted_note = FormatNote(self.award_note, '', 'full', 0, '', 0)
                        level_link += ISFDBMouseover([formatted_note], '', '', SESSION.ui.info_sign, note = 1)
                return level_link

        def PrintTitle(self):
                # For title-based awards, display and hyperlink the work's title
                if self.title_id:
                        title = SQLloadTitle(self.title_id)
                        print ISFDBLink('title.cgi', self.title_id, title[TITLE_TITLE])
                        if title[TITLE_PARENT]:
                                parent = SQLloadTitle(title[TITLE_PARENT])
                                if title[TITLE_LANGUAGE] and parent[TITLE_LANGUAGE] and title[TITLE_LANGUAGE] != parent[TITLE_LANGUAGE]:
                                        print ' (%s translation of %s)' % (LANGUAGES[title[TITLE_LANGUAGE]],
                                                                           ISFDBLink('title.cgi', parent[TITLE_PUBID], parent[TITLE_TITLE]))
                                elif parent[TITLE_TITLE] != title[TITLE_TITLE]:
                                        print ' (variant of %s)' % ISFDBLink('title.cgi', parent[TITLE_PUBID], parent[TITLE_TITLE])
                else:
                        if self.award_title and (self.award_title != "untitled"):
                                print self.award_title

        def PrintAwardSummary(self):
                from login import User

                print '<ul>'
                print '<li><b>Title: </b>'
                title_data = ''
                if self.title_id:
                        title_data = SQLloadTitle(self.title_id)
                        print ISFDBLink("title.cgi", self.title_id, title_data[TITLE_TITLE])
                else:
                        print '%s (<i>no ISFDB title record</i>)' % ISFDBText(self.award_title)
                
                #Retrieve this user's data
                user = User()
                user.load()
                printRecordID('Award', self.award_id, user.id)

                if self.award_authors:
                        if len(self.award_authors) > 1:
                                print '<li><b>Authors: </b> '
                        else:
                                print '<li><b>Author: </b> '
                        self.PrintAwardAuthors()

                print '<li><b>Award Name: </b> %s' % ISFDBLink('awardtype.cgi', self.award_type_id, self.award_type_name)
                print '<li><b>Year: </b> %s' % ISFDBLink('ay.cgi', '%s+%s' % (self.award_type_id, self.award_year[:4]), self.award_year[:4])
                print '<li><b>Category: </b> %s' % ISFDBLink('award_category.cgi', '%s+0' % self.award_cat_id, self.award_cat_name)

                print '<li><b>Award Level: </b> '
                if int(self.award_level) > 70:
                        print '<i>%s</i>' % self.special_awards[self.award_level]
                elif self.award_type_poll == 'Yes':
                                print "<i>Poll Place</i>: %s" % self.award_level
                else:
                        if int(self.award_level) == 1:
                                print " Win"
                        else:
                                print " Nomination"

                if self.award_movie:
                        print '<li><b>IMDB record: </b> %s' % IMDBLink(self.award_movie, self.award_movie)

                if self.award_note:
                        print '<li>'
                        print FormatNote(self.award_note, 'Note', 'short', self.award_id, 'Award')
                print '</ul>'
                
        def PrintAwardAuthors(self):
                counter = 0
                # If the award is title-based, then display that title's authors
                if self.title_id:
                        authors = SQLTitleBriefAuthorRecords(self.title_id)
                        for author in authors:
                                if counter:
                                        print " <b>and</b> "
                                print ISFDBLink("ea.cgi", author[0], author[1])
                                counter += 1
                else:
                        for author in self.award_authors:
                                if counter:
                                        print " <b>and</b> "
                                actual = string.split(author, '^')
                                if string.find(actual[0], '***') > -1:
                                        print '-'
                                elif actual[0] == 'No Award':
                                        print 'No Award'
                                else:
                                        self.displayAuthor(actual[0])
                                counter += 1

        def displayAuthor(self, author):
                author_data = SQLgetAuthorData(author)
                if author_data:
                        print ISFDBLink('ea.cgi', author_data[AUTHOR_ID], author)
                else:
                        print ISFDBText(author)
