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
                print('<br><b>Last Database Sync:</b> 5 February 2024')
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

if __name__ == '__main__':

        PrintHeader('The Internet Speculative Fiction Database')
        PrintNavbar('frontpage', 0, 0, 'index.cgi', 0)

        displayNotices()

        # Authors who were born and died on this day
        calendar_day = CalendarDay()
        calendar_day.padded_day = ISFDBDate()
        calendar_day.print_authors_section()
        # Forthcoming Books
        displayLinks()
        print('<div class="divider">')
        print('<b>Selected Forthcoming Books:</b>')
        print('</div>')

        print('<div id="Intro">')
        print('<table>')

        leftcolumn = 1
        # Retrieve publication list from front_page_pubs which is built by the nightly job
        pubs = SQLGetFrontPagePubs(1)
        # If the nightly job hasn't run recently, retrieve publication list directly from the database
        if len(pubs) < SESSION.front_page_pubs:
                pubs = SQLGetNextMonthPubs()
        for pub in pubs:
                if leftcolumn:
                        print('<tr>')

                image_source = ISFDBHostCorrection(pub[PUB_IMAGE])
                image_source = image_source.split("|")[0]
                alt_name = 'Book Image'
                print('<td><img src="%s" class="covermainpage" alt="%s"></td>' % (image_source, alt_name))
                outstr = pub[PUB_YEAR][5:7] +'/'+ pub[PUB_YEAR][8:10] + ' - '
                outstr += ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE], False, 'class="forthcoming"') + " ("
                if pub[PUB_PUBLISHER]:
                        publisher = SQLGetPublisher(pub[PUB_PUBLISHER])
                        outstr += ISFDBLink('publisher.cgi', publisher[PUBLISHER_ID], publisher[PUBLISHER_NAME])

                if pub[PUB_ISBN]:
                        outstr += ", " + convertISBN(pub[PUB_ISBN])

                if pub[PUB_PRICE]:
                        outstr += ", " + ISFDBPrice(pub[PUB_PRICE], 'left')

                if pub[PUB_PAGES]:
                        outstr += ", %spp" % pub[PUB_PAGES]

                if pub[PUB_PTYPE]:
                        outstr += ", " + ISFDBPubFormat(pub[PUB_PTYPE], 'left')

                if pub[PUB_CTYPE]:
                                outstr += ', %s' % pub[PUB_CTYPE].lower()
                outstr += ') by '

                print('<td>%s' % outstr)
                authors = SQLPubBriefAuthorRecords(pub[PUB_PUBID])
                displayAuthorList(authors)
                print('</td>')
                if leftcolumn:
                        leftcolumn = 0
                else:
                        print('</tr>')
                        leftcolumn = 1

        if leftcolumn == 0:
                print('</tr>')
                print('<tr>')
                print('<td></td>')
                print('<td></td>')
                print('</tr>')
        print('</table>')
        print('</div>')
        displayLinks()

        PrintTrailer('frontpage', 0, 0)
