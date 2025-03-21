from __future__ import print_function
#
#     (C) COPYRIGHT 2013-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 943 $
#     Date: $Date: 2022-06-29 19:59:53 -0400 (Wed, 29 Jun 2022) $

##############################################################################
#  Pylint disable list. These checks are too gratuitous for our purposes
##############################################################################
# pylint: disable=bad-indentation
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=consider-using-f-string
# pylint: disable=too-many-statements
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
##############################################################################
# Look at these later
##############################################################################
# pylint: disable=unused-wildcard-import
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

import sys
import re
from isfdb import *
from library import *
from awardClass import awardShared
from awardtypeClass import award_type
from common import PrintWebPages
from login import User


class award_cat(awardShared):
        def __init__(self):
                self.used_cat_id = 0
                self.used_cat_name = 0
                self.used_cat_type_id = 0
                self.used_cat_order = 0
                self.used_note = 0
                self.used_note_id = 0
                self.used_webpages = 0

                self.award_cat_id = 0
                self.award_cat_type_id = 0
                self.award_cat_order = 0
                self.award_cat_note_id = 0
                self.award_cat_name = ''
                self.award_cat_note = ''
                self.award_cat_webpages = []

                self.error = ''
                self.form = 0

        def load(self):
                if not self.award_cat_id:
                        return
                awardCat = SQLGetAwardCatById(self.award_cat_id)
                if not awardCat:
                        self.error = "Award Category doesn't exist"
                        return
                if awardCat[AWARD_CAT_ID]:
                        self.award_cat_id = awardCat[AWARD_CAT_ID]
                        self.used_cat_id = 1
                if awardCat[AWARD_CAT_NAME]:
                        self.award_cat_name = awardCat[AWARD_CAT_NAME]
                        self.used_cat_name = 1
                if awardCat[AWARD_CAT_TYPE_ID]:
                        self.award_cat_type_id = awardCat[AWARD_CAT_TYPE_ID]
                        self.used_cat_type_id = 1
                if awardCat[AWARD_CAT_ORDER]:
                        self.award_cat_order = awardCat[AWARD_CAT_ORDER]
                        self.used_cat_order = 1
                if awardCat[AWARD_CAT_NOTE]:
                        note = SQLgetNotes(awardCat[AWARD_CAT_NOTE])
                        if note:
                                self.award_cat_note_id = awardCat[AWARD_CAT_NOTE]
                                self.used_note_id = 1
                                self.award_cat_note = note
                                self.used_note = 1

                self.award_cat_webpages = SQLloadAwardCatWebpages(awardCat[AWARD_CAT_ID])
                if self.award_cat_webpages:
                        self.used_webpages = 1

        def cgi2obj(self, form=0):
                if form:
                        self.form = form
                else:
                        self.form = IsfdbFieldStorage()
                sys.stderr = sys.stdout
                if 'award_cat_id' in self.form:
                        self.award_cat_id = int(self.form['award_cat_id'].value)
                        self.used_cat_id = 1

                try:
                        self.award_cat_type_id = int(self.form['award_cat_type_id'].value)
                        self.used_cat_type_id = 1
                        awardType = SQLGetAwardTypeById(self.award_cat_type_id)
                        if not awardType:
                                raise
                except:
                        self.error = 'Valid award type is required for award categories'
                        return

                try:
                        self.award_cat_name = XMLescape(self.form['award_cat_name'].value)
                        self.used_cat_name = 1
                        if not self.award_cat_name:
                                raise
                        # Unescape the award category name to ensure that the lookup finds it in the database
                        current_award_cat = SQLGetAwardCatByName(XMLunescape(self.award_cat_name), self.award_cat_type_id)
                        if current_award_cat:
                                if (self.award_cat_type_id == int(current_award_cat[AWARD_CAT_TYPE_ID])) and (self.award_cat_id != int(current_award_cat[AWARD_CAT_ID])):
                                        self.error = "Entered award category name is aready associated with category '%s' for this award type" % current_award_cat[AWARD_CAT_NAME]
                                        return
                except:
                        self.error = 'Award category name is required'
                        return

                if 'award_cat_order' in self.form:
                        self.award_cat_order = XMLescape(self.form['award_cat_order'].value)
                        self.used_cat_order = 1
                        if not re.match(r'^[1-9]{1}[0-9]{0,8}$', self.award_cat_order):
                                self.error = 'Display Order must be an integer greater than 0 and must contain 1-9 digits'
                                return

                if 'award_cat_note' in self.form:
                        value = XMLescape(self.form['award_cat_note'].value)
                        if value:
                                self.award_cat_note = value
                                self.used_note = 1

                for key in self.form:
                        if key[:18] == 'award_cat_webpages':
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.award_cat_webpages:
                                                continue
                                        self.error = invalidURL(value)
                                        if self.error:
                                                return
                                        self.award_cat_webpages.append(value)
                                        self.used_webpages = 1


        def PrintAwardCatYear(self, year):
                self.PrintAwardCatPageHeader()
                print('Displaying awards and nominations for this category for %d.' % year)
                print('You can also %s for this category for all years.' % ISFDBLink('award_category.cgi',
                                                                                     '%d+1' % self.award_cat_id,
                                                                                     'view all awards and nominations'))
                years = {}
                padded_year = '%d-00-00' % year
                years[padded_year] = SQLloadAwardsForCatYear(self.award_cat_id, year)
                self.PrintAwardCatTable(years)

        def PrintAwardCatTable(self, years):
                print('<table>')
                for year in sorted(years.keys()):
                        print('<tr>')
                        print('<td colspan=3> </td>')
                        print('</tr>')
                        print('<tr>')
                        print('<th colspan=3>%s</th>' % ISFDBLink('award_category_year.cgi', '%d+%s' % (self.award_cat_id, year[:4]), year[:4]))
                        print('</tr>')
                        self.PrintOneAwardList(years[year])
                print('</table>')

        def PrintAwardCatSummary(self, win_nom):
                self.PrintAwardCatPageHeader()
                years = SQLloadAwardsForCat(self.award_cat_id, win_nom)
                if win_nom == 0:
                        if years:
                                print('Displaying the')
                        else:
                                print('No')
                        print(' wins for this category. ')
                        print('You can also %s in this category.' % ISFDBLink('award_category.cgi', '%d+1' % self.award_cat_id, 'view all awards and nominations'))
                else:
                        if not years:
                                print('No wins or nominations for this category.')
                                return
                        print('Displaying all wins and nominations for this category. ')
                        print('You can also limit the list to the %s in this category.' % ISFDBLink('award_category.cgi', '%d+0' % self.award_cat_id, 'wins'))
                print('<p>')
                self.PrintAwardCatTable(years)

        def PrintAwardCatPageHeader(self):
                awardType = award_type()
                awardType.award_type_id = self.award_cat_type_id
                awardType.load()
                print('<ul>')
                print('<li><b>Award Category: </b> %s' % ISFDBText(self.award_cat_name))

                #Retrieve this user's data
                user = User()
                user.load()
                printRecordID('Award Category', self.award_cat_id, user.id, user)

                print('<li><b>Award Type: </b> %s' % ISFDBLink('awardtype.cgi', awardType.award_type_id, awardType.award_type_name))
                if self.award_cat_order:
                        print('<li><b>Display Order: </b> %s' % ISFDBText(self.award_cat_order))

                # Webpages
                if self.award_cat_webpages:
                        PrintWebPages(self.award_cat_webpages)

                # Note
                if self.award_cat_note:
                        print('<li>')
                        print(FormatNote(self.award_cat_note, 'Note', 'short', self.award_cat_id, 'AwardCat'))
                print('</ul>')
