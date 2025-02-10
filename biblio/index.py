#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Ahasuerus, Uzume and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1172 $
#     Date: $Date: 2024-04-03 20:46:06 -0400 (Wed, 03 Apr 2024) $


from SQLparsing import *
from library import ISFDBLink, ISFDBText, ISFDBPubFormat, ISFDBDate, ISFDBPrice, ISFDBHostCorrection
import datetime
from common import displayAuthorList, PrintHeader, PrintNavbar, PrintTrailer
from calendarClass import CalendarDay
from isbn import convertISBN


def displayLinks():
        print '<p class="bottomlinks">\n%s\n%s Note: Information based on pre-publication data and subject to change' % (
                ISFDBLink("fc.cgi", "", "View All Forthcoming Books", argument='class="inverted"'),
                ISFDBLink("stats.cgi?24", "", "View Top Forthcoming", argument='class="inverted"')
                )
        return

if __name__ == '__main__':

        PrintHeader('The Internet Speculative Fiction Database')
        PrintNavbar('frontpage', 0, 0, 'index.cgi', 0)

        print 'The <i><b>ISFDB</b></i> is a community effort to catalog works of science '
        print 'fiction, fantasy, and horror. '
        print 'It links together various types of bibliographic data: author bibliographies, '
        print 'publication bibliographies, award listings, magazine content listings, anthology '
        print 'and collection content listings, and forthcoming books.'

        # Authors who were born and died on this day
        calendar_day = CalendarDay()
        calendar_day.padded_day = ISFDBDate()
        calendar_day.print_authors_section()
        # Forthcoming Books
        displayLinks()
        print '<div class="divider">'
        print '<b>Selected Forthcoming Books:</b>'
        print '</div>'

        print '<div id="Intro">'
        print '<table>'

        leftcolumn = 1
        # Retrieve publication list from front_page_pubs which is built by the nightly job
        pubs = SQLGetFrontPagePubs(1)
        # If the nightly job hasn't run recently, retrieve publication list directly from the database
        if len(pubs) < SESSION.front_page_pubs:
                pubs = SQLGetNextMonthPubs()
        for pub in pubs:
                if leftcolumn:
                        print '<tr>'

                image_source = ISFDBHostCorrection(pub[PUB_IMAGE])
                image_source = image_source.split("|")[0]
                alt_name = 'Book Image'
                print '<td><img src="%s" class="covermainpage" alt="%s"></td>' % (image_source, alt_name)
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

                print '<td>%s' % outstr
                authors = SQLPubBriefAuthorRecords(pub[PUB_PUBID])
                displayAuthorList(authors)
                print '</td>'
                if leftcolumn:
                        leftcolumn = 0
                else:
                        print '</tr>'
                        leftcolumn = 1

        if leftcolumn == 0:
                print '</tr>'
                print '<tr>'
                print '<td></td>'
                print '<td></td>'
                print '</tr>'
        print '</table>'
        print '</div>'
        displayLinks()

        PrintTrailer('frontpage', 0, 0)
