#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Ahasuerus, Uzume and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1172 $
#     Date: $Date: 2024-04-03 20:46:06 -0400 (Wed, 03 Apr 2024) $

##############################################################################
#  Pylint disable list. These checks are too gratuitous for our purposes
##############################################################################
# pylint: disable=C0103, C0209, C0116, W0311, R1705, C0301, R0902, C0413, R0903, C0413
#
# C0103 = Not using snake_case naming conventions
# C0209 = Lack of f-string usage
# C0116 = Lack of docstrings
# W0311 = Lack of using 4 spaces for indention
# R1705 = Unnecessary else after return
# C0301 = Line too long (> 80 characters)
# R0902 = Too many instance attributes
# R0903 = Too few public methods
# C0413 = Wrong import position

from SQLparsing import *
from library import ISFDBLink, ISFDBText, ISFDBPubFormat, ISFDBDate, ISFDBPrice, ISFDBHostCorrection
import datetime
from common import displayAuthorList, PrintHeader, PrintNavbar, PrintTrailer
from calendarClass import CalendarDay
from isbn import convertISBN

def displayNotices():
        #if (HTMLLOC == "www.isfdb.org") or (HTMLLOC == "isfdb.org"):
        if HTMLLOC in ('www.isfdb.org', 'isfdb.org'):
                print('The <i><b>ISFDB</b></i> is a community effort to catalog works of science ')
                print('fiction, fantasy, and horror. ')
                print('It links together various types of bibliographic data: author bibliographies, ')
                print('publication bibliographies, award listings, magazine content listings, anthology ')
                print('and collection content listings, and forthcoming books.')
        elif (HTMLLOC == "www.isfdb2.org") or (HTMLLOC == "isfdb2.org"):
                print('This is the staging server for the ISFDB. This server runs features that are broad in scope, and generally')
                print('too risky to run on the main server, or impossible for multiple people to test on a home server. The kinds')
                print('of projects that could be running here include updating LAMP stack components, moving to Python3, mobile support,')
                print('moving charsets to unicode, and UI redesign. This server may be unstable, and <b>data entered here will be lost</b>.')
                print('<p>')
                print('<br><b>Last Database Sync:</b> 9 March 2024')
                print('<br><b>Source Revision:</b> r1026 (+ isfdb2 differentiation)')
                print('<br><b>Current Project:</b> Python3 Conversion. Biblio/Edit/Mod work under Python2. Biblio/Edit work under Python3. All else is suspect.')
                print('This system oftens switches between python2 and python3.')
                print('<br><b>Current Python version:</b> %s' % PYTHONVER)
        else:
                print('This is a private server instance of the ISFDB.')

def displayLinks():
        print('<p class="bottomlinks">\n%s\n%s Note: Information based on pre-publication data and subject to change' % (
                ISFDBLink("fc.cgi", "", "View All Forthcoming Books", argument='class="inverted"'),
                ISFDBLink("stats.cgi?24", "", "View Top Forthcoming", argument='class="inverted"')
                ))
        return

def ConvertMonth(integer_month):
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

def doDates(captions):
        print('<tr>')
        for caption in captions:
                if caption != '':
                        print('<td>')
                        print('<span class="covermainpage">')
                        capmonth = ConvertMonth(int(caption[PUB_YEAR][5:7]))
                        label = '%s %s' % (capmonth, caption[PUB_YEAR][8:10])
                        outstr = ISFDBLink("pl.cgi", caption[PUB_PUBID], "%s" % label)
                        print(outstr)
                        #print label
                        print('</span>')
                        print('</td>')
        print('</tr>')

def ConvertFormat(format):
        format_map = {
        'pb'  : 'Mass Market Paperback',
        'tp'  : 'Trade Paperback',
        'hc'  : 'Hardcover',
        'ebook'  : 'E-book',
        'digest'  : 'Digest',
        'digital audio download'  : 'Digital Audio',
        }
        return format_map[format]

def doPubTypes(captions):
        print('<tr>')
        for caption in captions:
                if caption != '':
                        print('<td>')
                        print('<span class="covermainpage">')
                        try:
                                format = ConvertFormat(caption[PUB_PTYPE])
                        except:
                                format = caption[PUB_PTYPE]
                        label = '(%s)' % (format)
                        #outstr = ISFDBLink("pl.cgi", caption[PUB_PUBID], "%s" % label)
                        #print outstr
                        print(label)
                        print('</span>')
                        print('</td>')
        print('</tr>')

def displayForthcoming():
        # Forthcoming Books
        displayLinks()
        print('<div class="divider">')
        print('<b>Selected Forthcoming Books:</b>')
        print('</div>')

        print('<div id="Intro">')
        print('<table class="mainpage">')

        # Retrieve publication list from front_page_pubs which is built by the nightly job
        pubs = SQLGetFrontPagePubs(1)
        # If the nightly job hasn't run recently, retrieve publication list directly from the database
        if len(pubs) < SESSION.front_page_pubs:
                pubs = SQLGetNextMonthPubs()

        booksPrinted    = 0
        columnNumber    = 1
        maxColumns      = 5
        maxRows         = 4
        maxBooks        = maxColumns * maxRows

        titles = []
        captions = ['', '', '', '', '', '', '']
        CaptionIndex = 0

        for pub in pubs:

                image_source = ISFDBHostCorrection(pub[PUB_IMAGE])
                image_source = image_source.split("|")[0]
                alt_name = 'Book Image'
                captions[CaptionIndex] = pub
                CaptionIndex += 1

                if columnNumber == 1:
                        print('<tr>')
                print('<td class="forthbook"><img src="%s" class="covermainpage" alt="%s"></td>' % (image_source, alt_name))
                booksPrinted += 1

                if columnNumber == maxColumns:
                        columnNumber = 1
                        print('</tr>')
                        doDates(captions)
                        doPubTypes(captions)
                        captions = ['', '', '', '', '', '', '']
                        CaptionIndex = 0
                else:
                        columnNumber += 1

                if booksPrinted >= maxBooks:
                        break

        print('</table>')
        print('</div>')
        displayLinks()

def displayAuthors():
        # Authors who were born and died on this day
        calendar_day = CalendarDay()
        calendar_day.padded_day = ISFDBDate()
        calendar_day.print_authors_section()

if __name__ == '__main__':

        PrintHeader('The Internet Speculative Fiction Database')
        PrintNavbar('frontpage', 0, 0, 'index.cgi', 0)

        displayNotices()
        displayForthcoming()
        displayAuthors()

        PrintTrailer('frontpage', 0, 0)
