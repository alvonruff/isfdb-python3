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

import cgi
import sys
import re
from isfdb import *
from library import *
from xml.dom import minidom
from xml.dom import Node
from awardClass import awardShared


class award_cat(awardShared):
        def __init__(self):
                self.used_cat_id = 0
                self.used_cat_name = 0
                self.used_cat_type_id = 0
                self.used_cat_order = 0
                self.used_note = 0
                self.used_note_id = 0
                self.used_webpages = 0

                self.award_cat_id = ''
                self.award_cat_name = ''
                self.award_cat_type_id = ''
                self.award_cat_order = ''
                self.award_cat_note_id = ''
                self.award_cat_note = ''
                self.award_cat_webpages = []

                self.error = ''

        def load(self):
                if not self.award_cat_id:
                        return
                award_cat = SQLGetAwardCatById(self.award_cat_id)
                if not award_cat:
                        self.error = "Award Category doesn't exist"
                        return
                if award_cat[AWARD_CAT_ID]:
                        self.award_cat_id = award_cat[AWARD_CAT_ID]
                        self.used_cat_id = 1
                if award_cat[AWARD_CAT_NAME]:
                        self.award_cat_name = award_cat[AWARD_CAT_NAME]
                        self.used_cat_name = 1
                if award_cat[AWARD_CAT_TYPE_ID]:
                        self.award_cat_type_id = award_cat[AWARD_CAT_TYPE_ID]
                        self.used_cat_type_id = 1
                if award_cat[AWARD_CAT_ORDER]:
                        self.award_cat_order = award_cat[AWARD_CAT_ORDER]
                        self.used_cat_order = 1
                if award_cat[AWARD_CAT_NOTE]:
                        note = SQLgetNotes(award_cat[AWARD_CAT_NOTE])
                        if note:
                                self.award_cat_note_id = award_cat[AWARD_CAT_NOTE]
                                self.used_note_id = 1
                                self.award_cat_note = note
                                self.used_note = 1

                self.award_cat_webpages = SQLloadAwardCatWebpages(award_cat[AWARD_CAT_ID])
                if self.award_cat_webpages:
                        self.used_webpages = 1

        def cgi2obj(self):
                sys.stderr = sys.stdout
                self.form = cgi.FieldStorage()
                if self.form.has_key('award_cat_id'):
                        self.award_cat_id = int(self.form['award_cat_id'].value)
                        self.used_cat_id = 1

                try:
                        self.award_cat_type_id = int(self.form['award_cat_type_id'].value)
                        self.used_cat_type_id = 1
                        award_type = SQLGetAwardTypeById(self.award_cat_type_id)
                        if not award_type:
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

                if self.form.has_key('award_cat_order'):
                        self.award_cat_order = XMLescape(self.form['award_cat_order'].value)
                        self.used_cat_order = 1
                        if not re.match(r'^[1-9]{1}[0-9]{0,8}$', self.award_cat_order):
                                self.error = 'Display Order must be an integer greater than 0 and must contain 1-9 digits'
                                return

                if self.form.has_key('award_cat_note'):
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
                from awardtypeClass import award_type
                from common import PrintWebPages
                from login import User
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
