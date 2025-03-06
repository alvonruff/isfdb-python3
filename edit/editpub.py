#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Bill Longley, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 984 $
#     Date: $Date: 2022-08-29 18:26:44 -0400 (Mon, 29 Aug 2022) $


from SQLparsing import *
from pubClass import pubs
from isfdb import *
from library import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *


def printpubrecord(pub):
        help = HelpPub()
        print('<h2>Publication Metadata</h2>')
        print('<table id="metadata">')
        print('<tbody id="pubBody">')
        printfield("Title", "pub_title", help, pub.pub_title)
        trans_titles = SQLloadTransPubTitles(pub.pub_id)
        printmultiple(trans_titles, "Transliterated Title", "trans_titles", help)

        authors = SQLPubAuthors(pub.pub_id)
        printmultiple(authors, "Author", "pub_author", help)

        printfield("Date", "pub_year", help, pub.pub_year)
        printfield("Publisher", "pub_publisher", help, pub.pub_publisher)
        printfield("Pages", "pub_pages", help, pub.pub_pages)
        printformat("pub_ptype", "Format", help, pub.pub_ptype)

        print('<tr>')
        printContentHeader('Pub Type:', help)
        print('<td><select tabindex="1" name="pub_ctype" class="metainputselect">')
        print('<option value="%s" selected="selected">%s</option>' % (pub.pub_ctype, pub.pub_ctype))
        for ctype in SESSION.db.pub_types:
                if ctype != pub.pub_ctype:
                        print('<option value="%s">%s</option>' % (ctype, ctype))
        print('</select>')
        print('</tr>')

        printISBN(help, pub.pub_isbn)
        printfield("Catalog ID", "pub_catalog", help, pub.pub_catalog)
        printfield("Price", "pub_price", help, pub.pub_price)
        printfield("Image URL", "pub_image", help, pub.pub_image)
        printfield("Pub Series", "pub_series", help, pub.pub_series)
        printfield("Pub Series #", "pub_series_num", help, pub.pub_series_num)
        printWebPages(pub.pub_webpages, 'pub', help)
        printtextarea('Pub Note', 'pub_note', help, pub.pub_note)
        printExternalIDs(pub.identifiers, "External ID", "external_id", help)
        printtextarea('Note to Moderator', 'mod_note', help)

        print('</tbody>')
        print('</table>')

if __name__ == '__main__':

        pub_id = SESSION.Parameter(0, 'int')
        pub = pubs(db)
        pub.load(pub_id)
        if pub.error:
                SESSION.DisplayError('Record Does Not Exist')

        PrintPreSearch('Publication Editor')
        PrintNavBar('edit/editpub.cgi', pub_id)

        titles = getSortedTitlesInPub(pub_id)
        covers = SQLPubCovers(pub_id)

        printHelpBox('publication', 'EditPub')

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitpub.cgi">')
        printpubrecord(pub)

        print('<hr class="topspace">')
        print('<h2 class="editheadline">Content</h2>')
        print("""<ul>
                <li>To change the order of records in the Content section, use "pipe" characters in the "Page" field --
                see the "Sorting" paragraph in <a href="%s://%s/index.php/Template:PubContentFields:Page">Template:PubContentFields:Page</a> for details.
                <li>White: non-container titles appearing only in this publication; can be edited
                <li>Yellow: container titles appearing only in this publication; can be edited except for page numbers and OMNIBUS length
                <li>Gray: titles appearing in multiple publications; cannot be edited here
                <li>See <a href="%s://%s/index.php/Help:How to change a story in a collection">Help:How
                to change a story in a collection</a> for details.
                </ul>"""  % (PROTOCOL, WIKILOC, PROTOCOL, WIKILOC))
        print('<p>')

        print('<hr class="topspace">')
        # Retrieve the Help text for covers
        help = HelpCoverArt()
        print('<h2>Cover Art</h2>')
        print('<table class="coveredit">')
        print('<tbody id="coverBody">')

        if not covers:
                index = 1
                printbriefblankcoverart(index, help)
                index += 1
                printNewBriefCoverButton()
        else:
                print('<tr>')
                print('<td>&nbsp;</td>')
                printContentHeader('Title', help)
                printContentHeader('Date', help)
                print('</tr>')
                index = 1
                for cover in covers:
                        # Find out if this cover is in more than 1 publication
                        manypubs = SQLCountPubsForTitle(cover[TITLE_PUBID])
                        if manypubs:
                                printfullcoverart(cover, index, help, 1)
                        else:
                                printfullcoverart(cover, index, help, 0)
                        index += 1
                printNewFullCoverButton()
        print('</tbody>')
        print('</table>')

        # Retrieve the Help text for publication content
        help = HelpTitleContent()
        print('<hr class="topspace">')
        print('<h2 class="editheadline">Regular Titles</h2>')
        print('<table class="titleedit">')
        print('<tbody id="titleBody">')

        print('<tr>')
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        printContentHeader('Title Type', help)
        printContentHeader('Length', help)
        print('</tr>')

        normal_titles = []
        container_titles = []
        review_titles = []
        interview_titles = []

        for title in titles:
                if title[TITLE_TTYPE] == 'COVERART':
                        continue
                elif title[TITLE_TTYPE] == 'EDITOR':
                        container_titles.append(title)
                elif (title[TITLE_TTYPE] == 'OMNIBUS') and (pub.pub_ctype == 'OMNIBUS'):
                        container_titles.append(title)
                elif (title[TITLE_TTYPE] == 'COLLECTION') and (pub.pub_ctype == 'COLLECTION'):
                        container_titles.append(title)
                elif (title[TITLE_TTYPE] == 'ANTHOLOGY') and (pub.pub_ctype == 'ANTHOLOGY'):
                        container_titles.append(title)
                elif (title[TITLE_TTYPE] == 'CHAPBOOK') and (pub.pub_ctype == 'CHAPBOOK'):
                        container_titles.append(title)
                elif (title[TITLE_TTYPE] == 'REVIEW'):
                        review_titles.append(title)
                elif (title[TITLE_TTYPE] == 'INTERVIEW'):
                        interview_titles.append(title)
                else:
                        normal_titles.append(title)

        index = 1
        if container_titles:
                for title in container_titles:
                        printeditabletitlerecord(title, index, 1, help, pub_id)
                        index += 1

        if normal_titles:
                for title in normal_titles:
                        printeditabletitlerecord(title, index, 0, help, pub_id)
                        index += 1
        
        if index == 1:
                printblanktitlerecord(index, help, pub.pub_ctype)
                index += 1
        printNewTitleButton()
        print('</tbody>')
        print('</table>')

        print('<hr class="topspace">')
        # Retrieve the Help text for reviews
        help = HelpReviewContent()
        print('<h2 class="editheadline">Reviews</h2>')
        print('<table class="reviewedit">')
        print('<tbody id="reviewBody">')
        print('<tr>')
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        print('</tr>')
        index = 1
        if review_titles:
                for title in review_titles:
                        printeditablereviewrecord(title, index, help, pub_id)
                        index += 1
        else:
                printblankreviewrecord(index, help)
                index += 1
        printNewReviewButton()
        print('</tbody>')
        print('</table>')

        print('<hr class="topspace">')
        # Retrieve the Help text for interviews
        help = HelpInterviewContent()
        print('<h2 class="editheadline">Interviews</h2>')
        print('<table class="interviewedit">')
        print('<tbody id="interviewBody">')
        print('<tr>')
        printContentHeader('Page', help)
        printContentHeader('Interview Title', help)
        printContentHeader('Date', help)
        print('</tr>')
        index = 1
        if interview_titles:
                for title in interview_titles:
                        printeditableinterviewrecord(title, index, help, pub_id)
                        index += 1
        else:
                printblankinterviewrecord(index, help)
                index += 1
        printNewInterviewButton()
        print('</tbody>')
        print('</table>')

        print('<hr class="topspace">')
        print('<p>')
        print('<input name="pub_id" value="%d" type="HIDDEN">' % pub_id)
        print('<input name="editor" value="editpub" type="HIDDEN">')
        print('<input type="SUBMIT" value="Submit Changed Data" tabindex="1">')
        pub.printModNoteRequired()
        print('</form>')
        print('<hr class="topspace">')
        print(ISFDBLink("edit/deletepub.cgi", pub_id, "Delete record"))

        PrintPostSearch(tableclose=False)
