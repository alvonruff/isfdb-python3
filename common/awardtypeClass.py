from __future__ import print_function
#
#     (C) COPYRIGHT 2013-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 796 $
#     Date: $Date: 2021-11-02 19:08:22 -0400 (Tue, 02 Nov 2021) $

import cgi
from SQLparsing import SQLGetAwardTypeById, SQLgetNotes, SQLloadAwardTypeWebpages
from awardClass import awardShared
from isfdb import *
from library import *


class award_type(awardShared):
        def __init__(self):
                self.used_id = 0
                self.used_code = 0
                self.used_by = 0
                self.used_for = 0
                self.used_name = 0
                self.used_short_name = 0
                self.used_note = 0
                self.used_note_id = 0
                self.used_poll = 0
                self.used_webpages = 0
                self.used_non_genre = 0

                self.award_type_id = ''
                self.award_type_code = ''
                self.award_type_by = ''
                self.award_type_for = ''
                self.award_type_name = ''
                self.award_type_short_name = ''
                self.award_type_poll = ''
                self.award_type_note_id = ''
                self.award_type_note = ''
                self.award_type_webpages = []
                self.award_type_non_genre = ''

                self.error = ''

        def load(self):
                if not self.award_type_id and not self.award_type_code:
                        self.error = "Award type not specified"
                        return
                if self.award_type_id:
                        award_type = SQLGetAwardTypeById(self.award_type_id)
                        if not award_type:
                                self.error = "Award type not found: %s" % self.award_type_id
                                return
                if self.award_type_code:
                        award_type = SQLGetAwardTypeByCode(self.award_type_code)
                        if not award_type:
                                self.error = "Award type not found: %s" % self.award_type_code
                                return

                if award_type[AWARD_TYPE_ID]:
                        self.award_type_id = award_type[AWARD_TYPE_ID]
                        self.used_id = 1
                if award_type[AWARD_TYPE_CODE]:
                        self.award_type_code = award_type[AWARD_TYPE_CODE]
                        self.used_code = 1
                if award_type[AWARD_TYPE_NAME]:
                        self.award_type_name = award_type[AWARD_TYPE_NAME]
                        self.used_name = 1
                if award_type[AWARD_TYPE_SHORT_NAME]:
                        self.award_type_short_name = award_type[AWARD_TYPE_SHORT_NAME]
                        self.used_short_name = 1
                if award_type[AWARD_TYPE_BY]:
                        self.award_type_by = award_type[AWARD_TYPE_BY]
                        self.used_by = 1
                if award_type[AWARD_TYPE_FOR]:
                        self.award_type_for = award_type[AWARD_TYPE_FOR]
                        self.used_for = 1
                if award_type[AWARD_TYPE_POLL]:
                        self.award_type_poll = award_type[AWARD_TYPE_POLL]
                        self.used_poll = 1
                if award_type[AWARD_TYPE_NOTE]:
                        note = SQLgetNotes(award_type[AWARD_TYPE_NOTE])
                        if note:
                                self.award_type_note_id = award_type[AWARD_TYPE_NOTE]
                                self.used_note_id = 1
                                self.award_type_note = note
                                self.used_note = 1
                if award_type[AWARD_TYPE_NONGENRE]:
                        self.award_type_non_genre = award_type[AWARD_TYPE_NONGENRE]
                        self.used_non_genre = 1

                self.award_type_webpages = SQLloadAwardTypeWebpages(award_type[AWARD_TYPE_ID])
                if self.award_type_webpages:
                        self.used_webpages = 1

        def cgi2obj(self):
                self.form = IsfdbFieldStorage()
                if 'award_type_id' in self.form:
                        self.award_type_id = int(self.form['award_type_id'].value)
                        self.used_id = 1

                try:
                        self.award_type_name = XMLescape(self.form['award_type_name'].value)
                        self.used_name = 1
                        if not self.award_type_name:
                                raise
                        # Unescape the award type name to ensure that the lookup finds it in the database
                        current_award_type = SQLGetAwardTypeByName(XMLunescape(self.award_type_name))
                        if current_award_type:
                                if self.award_type_id != int(current_award_type[AWARD_TYPE_ID]):
                                        self.error = "Award type with full name '%s' already exists" % current_award_type[AWARD_TYPE_NAME]
                                        return
                except:
                        self.error = "Full name is required for Award types"
                        return

                try:
                        self.award_type_short_name = XMLescape(self.form['award_type_short_name'].value)
                        self.used_short_name = 1
                        if not self.award_type_short_name:
                                raise
                        # Unescape the award type name to ensure that the lookup finds it in the database
                        current_award_type = SQLGetAwardTypeByShortName(XMLunescape(self.award_type_short_name))
                        if current_award_type:
                                if self.award_type_id != int(current_award_type[AWARD_TYPE_ID]):
                                        self.error = "Award type with short name '%s' already exists" % current_award_type[AWARD_TYPE_SHORT_NAME]
                                        return
                except:
                        self.error = "Short name is required for Award types"
                        return

                if 'award_type_by' in self.form:
                        value = XMLescape(self.form['award_type_by'].value)
                        if value:
                                self.award_type_by = value
                                self.used_by = 1
                
                if 'award_type_for' in self.form:
                        value = XMLescape(self.form['award_type_for'].value)
                        if value:
                                self.award_type_for = value
                                self.used_for = 1

                if 'award_type_poll' in self.form:
                        value = XMLescape(self.form['award_type_poll'].value)
                        if value:
                                self.award_type_poll = value
                                self.used_poll = 1

                if 'award_type_note' in self.form:
                        value = XMLescape(self.form['award_type_note'].value)
                        if value:
                                self.award_type_note = value
                                self.used_note = 1

                for key in self.form:
                        if key[:19] == 'award_type_webpages':
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.award_type_webpages:
                                                continue
                                        self.error = invalidURL(value)
                                        if self.error:
                                                return
                                        self.award_type_webpages.append(value)
                                        self.used_webpages = 1

                if 'award_type_non_genre' in self.form:
                        value = XMLescape(self.form['award_type_non_genre'].value)
                        if value:
                                self.award_type_non_genre = value
                                self.used_non_genre = 1


        def display_table_grid(self, current_year = 0):
                # Display a grid of years when this award was given. The parameter, "current_year",
                # indicates the year that the grid is being displayed for, so that year is not hyperlinked.
                # If current_year is 0, then we are displaying a complete grid and will hyperlink all years
                award_years = SQLGetAwardYears(self.award_type_id)
                if award_years:
                        print('<div class="generic_centered_div">')
                        if current_year:
                                print('<h3>Award Years for %s</h3>' % ISFDBLink('awardtype.cgi', self.award_type_id, self.award_type_name))
                        else:
                                print('<h3>Award Years</h3>')
                        print('<table class="generic_centered_table">')
                        decades = {}
                        for award_year in award_years:
                                decade = award_year[:3]
                                if decade not in decades:
                                        decades[decade] = []
                                decades[decade].append(award_year[:4])
                        for decade in sorted(decades.keys()):
                                print('<tr align="center" class="generic_table_header">')
                                print('<td>%s0\'s:</td>' % (decade))
                                for i in range(0,10):
                                        award_year = decade+str(i)
                                        print('<td>')
                                        if award_year in decades[decade]:
                                                if int(award_year) == int(current_year):
                                                        # If this is the year being displayed, don't hyperlink it
                                                        print('<b>%s</b>' % award_year)
                                                else:
                                                        print(ISFDBLink('ay.cgi', '%s+%s' % (self.award_type_id, award_year), award_year))
                                        else:
                                                print('&nbsp;-&nbsp;')
                                        print('</td>')
                                print('</tr>')
                        print('</table>')
                        print('</div>')

        def display_categories(self):
                categories = SQLGetAwardCatBreakdown(self.award_type_id)
                if categories:
                        print('<div class="generic_centered_div">')
                        print('<h3>Categories</h3>')
                        print('<table class="generic_centered_table">')
                        print('<tr class="generic_table_header">')
                        print('<th>Display Order</th>')
                        print('<th>Category</th>')
                        print('<th>Wins</th>')
                        print('<th>All awards and nominations</th>')
                        print('</tr>')
                        for category in categories:
                                print('<tr class="generic_table_header">')
                                if category[2]:
                                        display_order = category[2]
                                else:
                                        display_order = ''
                                print('<td>%s</td>' % display_order)
                                print('<td>%s</td>' % ISFDBLink('award_category.cgi', '%s+0' % category[1], category[0]))
                                print('<td>%s</td>' % ISFDBLink('award_category.cgi', '%s+0' % category[1], category[3]))
                                print('<td>%s</td>' % ISFDBLink('award_category.cgi', '%s+1' % category[1], category[4]))
                                print('</tr>')
                        print('</table>')
                        print('</div>')
                
                empty_categories = SQLGetEmptyAwardCategories(self.award_type_id)
                if empty_categories:
                        print('<div class="generic_centered_div">')
                        print('<h3>Empty Categories</h3>')
                        print('<table class="generic_centered_table">')
                        print('<tr class="generic_table_header">')
                        print('<th>Display Order</th>')
                        print('<th>Category</th>')
                        print('</tr>')
                        for category in empty_categories:
                                print('<tr class="generic_table_header">')
                                print('<td>%s</td>' % category[AWARD_CAT_ORDER])
                                print('<td>%s</td>' % ISFDBLink('award_category.cgi', '%s+1' % category[AWARD_CAT_ID], category[AWARD_CAT_NAME]))
                                print('</tr>')
                        print('</table>')
                        print('</div>')

        def display_awards_for_year(self, year):
                # Display a grid of all years when the award was given
                self.display_table_grid(year)

                all_awards = SQLloadAwardsForYearType(self.award_type_id, year)

                if not all_awards:
                        print("<h2>No awards available for %s</h2>" % year)
                        return

                print('<table>')
                while all_awards:
                        # Get the name of the category of the first award in the list;
                        # it will be the category that we will be processing in this iteration of the while loop
                        name = all_awards[0][AWARD_NOTEID+1]
                        counter = 0
                        # Create a list of awards for the current category only
                        awards_for_category = []
                        while counter < len(all_awards):
                                if all_awards[counter][AWARD_NOTEID+1] == name:
                                        awards_for_category.append(all_awards[counter])
                                        del all_awards[counter]
                                else:
                                        counter += 1
                        if awards_for_category:
                                # Print awards for one category
                                print('<tr>')
                                print('<td colspan=3> </td>')
                                print('</tr>')
                                print('<tr>')
                                print('<td colspan=3><b>%s</b></td>' % ISFDBLink('award_category.cgi',
                                                                               '%s+0' % awards_for_category[0][AWARD_CATID],
                                                                               awards_for_category[0][AWARD_NOTEID+1]))
                                print('</tr>')
                                self.PrintOneAwardList(awards_for_category)
                print('</table>')
