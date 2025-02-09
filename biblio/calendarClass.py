#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2022   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 873 $
#     Date: $Date: 2022-03-10 21:47:35 -0500 (Thu, 10 Mar 2022) $

from isfdb import *
import datetime
from common import *
from SQLparsing import *
from library import *
import calendar

class CalendarMenu:
        def __init__(self):
                self.month = 0
                self.num_days = 0
                today = datetime.date.today()
                self.current_month = today.month
                self.current_day = today.day

        def display(self):
                PrintHeader('SF Calendar')
                PrintNavbar('calendar_menu', 0, 0, 'calendar_menu.cgi', 0)
                print '<table class="calendar_table">'
                for month_row in (1,2,3,4):
                        print '<tr>'
                        for month_column in (1,2,3):
                                self.month += 1
                                self.num_days = calendar.monthrange(2000, self.month)[1]
                                print '<td>'
                                self.print_month()
                                print '</td>'
                        print '</tr>'
                print '</table>'
                PrintTrailer('calendar_menu', 0, 0)
        
        def print_month(self):
                print '<table class="calendar_row">'
                self.print_month_header()
                self.print_decades()
                print '</table>'

        def print_decades(self):
                day = 0
                for decade_row in (1,2,3):
                        print '<tr>'
                        for day_cell in range(1,11):
                                day += 1
                                print '<td>'
                                if decade_row == 3 and day == 30 and self.num_days < 30:
                                        print '&nbsp;'
                                else:
                                        self.print_day(day)
                                print '</td>'

                        print '<td>'
                        if day == 30 and self.num_days == 31:
                                self.print_day(31)
                        else:
                                print '&nbsp;'
                        print '</td>'
                        print '</tr>'

        def print_day(self, day):
                inverted = ''
                # Highlight the current day
                if self.month == self.current_month and self.current_day == day:
                        inverted = 'class="inverted"'
                print ISFDBLink('calendar_day.cgi', '%s+%s' % (self.month, day), day, argument = inverted)

        def print_month_header(self):
                print '<tr>'
                print '<th colspan="10" class="calendar">'
                print calendar.month_name[self.month]
                print '</th>'
                print '</tr>'

class CalendarDay:
        def __init__(self):
                self.month = 0
                self.day = 0

        def display(self):
                self.parse_parameters()
                PrintHeader('On This Day in SF - %s %s' % (calendar.month_name[self.month], self.day))
                PrintNavbar('calendar_day', 0, 0, 'calendar_day.cgi', 0)
                self.padded_day = '2000-%02d-%02d' % (self.month, self.day)
                self.print_authors_section()
                PrintTrailer('calendar_day', 0, 0)

        def parse_parameters(self):
                self.month = SESSION.Parameter(0, 'int', None, range(1, 13))
                self.day = SESSION.Parameter(1, 'int')
                if self.day < 1 or self.day > calendar.monthrange(2000, self.month)[1]:
                        SESSION.DisplayError('Invalid day for this month')

        def print_authors_section(self):
                print '<table class="mainauthors">'
                print '<tr>'
                print '<th class="dividerrow">Authors Born On This Day:</th>'
                print '<th class="dividerrow">Authors Who Died On This Day:</th>'
                print '</tr>'
                # Authors born on this day
                print '<tr>'
                self.authors = SQLAuthorsBorn(self.padded_day)
                self.printAuthorList()
                # Authors who died on this day
                self.authors = SQLAuthorsDied(self.padded_day)
                self.printAuthorList()
                print '</tr>'
                print '</table>'

        def printAuthorList(self):
                print '<td>'
                if self.authors:
                        print '<ul>'
                        for self.author in self.authors:
                                print '<li>%s %s' % (ISFDBLink('ea.cgi', self.author[AUTHOR_ID], self.author[AUTHOR_CANONICAL]), self.lifeSpan())
                        print '</ul>'
                print '</td>'

        def lifeSpan(self):
                birthyear = self.author[AUTHOR_BIRTHDATE]
                if birthyear:
                        birthyear = birthyear[:4]
                if birthyear == '0000':
                        birthyear = 'unknown'

                deathyear = self.author[AUTHOR_DEATHDATE]
                if deathyear:
                        deathyear = deathyear[:4]
                if deathyear == '0000':
                        deathyear = 'unknown'

                if deathyear:
                        lifespan = " (%s-%s)" % (birthyear, deathyear)
                else:
                        lifespan = " (%s)" % birthyear
                return lifespan
