#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2008-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 989 $
#     Date: $Date: 2022-09-07 15:57:33 -0400 (Wed, 07 Sep 2022) $


import cgi
import sys
from SQLparsing import *
from isfdb import *
from library import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *
from pubClass import pubs


###################################################################
# This function outputs a publication record in table format
###################################################################
def printpubrecord(record):
        help = HelpGeneral()
        pub = pubs(db)
        pub.load(record[PUB_PUBID])
        print('<h2 class="editheadline">Publication Metadata</h2>')
        print('<table id="metadata">')
        print('<tbody id="pubBody">')
        printfield("Title", "pub_title", help, pub.pub_title, 1)

        authors = SQLPubAuthors(pub.pub_id)
        printmultiple(authors, "Author", "pub_author", help, 1)

        printfield("Date", "pub_year", help, pub.pub_year, 1)

        printfield("Publisher", "pub_publisher", help, pub.pub_publisher, 1)

        printfield("Pub. Series", "pub_series", help, pub.pub_series, 1)

        printfield("Pub. Series #", "pub_series_num", help, pub.pub_series_num, 1)
        printfield("Pages", "pub_pages", help, pub.pub_pages, 1)
        printfield("Pub Format", "pub_ptype", help, pub.pub_ptype, 1)
        printfield("Pub Type", "pub_ctype", help, pub.pub_ctype, 1)
        printfield("ISBN", "pub_isbn", help, pub.pub_isbn, 1)
        printfield("Catalog ID", "pub_catalog", help, pub.pub_catalog, 1)
        printfield("Price", "pub_price", help, pub.pub_price, 1)
        printfield("Image URL", "pub_image", help, pub.pub_image, 1)
        printWebPages(pub.pub_webpages, 'pub', help, '', 1)
        printtextarea('Pub Note', 'pub_note', help, pub.pub_note, readonly=True)
        printExternalIDs(pub.identifiers, 'External ID', 'external_id', help, 1)

        printtextarea('Note to Moderator', 'mod_note', help, '')

        print('</tbody>')
        print('</table>')

def errorPage(text):
        print("<h3>Error: %s</h3>" % (text))
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)

if __name__ == '__main__':

        sys.stderr = sys.stdout

        ##################################################################
        # Output the leading HTML stuff
        ##################################################################
        PrintPreSearch("Import/Export Contents")
        PrintNavBar('edit/editpub.cgi', 0)

        print('<div id="HelpBox">')
        print('<a href="%s://%s/index.php/Help:Screen:EditPub">Help on entering additional contents</a><p>' % (PROTOCOL, WIKILOC))
        print('</div>')

        form = IsfdbFieldStorage()
        if 'ExportTo' in form:
                ToTag = form['ExportTo'].value
                # Drop everything to the left of the last question mark in case a pub URL was entered
                ToTag = ToTag.split('?')[-1]
        else:
                errorPage("Publication to import content into is not specified")
                
        try:
                clone_to = int(ToTag)
        except:
                publication = SQLGetPubByTag(ToTag)
                if not publication:
                        errorPage("Specified tag/ID does not exist")
                clone_to = publication[PUB_PUBID]
        publication_to = SQLGetPubById(clone_to)
        if not publication_to:
                errorPage("Publication ID to clone to does not exist")

        pub_id = 0
        pub_type = ''
        # Check if we are importing/exporting the contents of a publication
        if 'ExportFrom' in form:
                FromTag = form['ExportFrom'].value
                # Drop everything to the left of the last question mark in case a pub URL was entered
                FromTag = FromTag.split('?')[-1]
                try:
                        clone_from = int(FromTag)
                except:
                        publication = SQLGetPubByTag(FromTag)
                        if not publication:
                               errorPage("Specified tag/ID does not exist")
                        clone_from = publication[PUB_PUBID]

                publication = SQLGetPubById(clone_from)
                if not publication:
                        errorPage("Specified tag/ID does not exist")
                titles = getSortedTitlesInPub(publication[PUB_PUBID])
                # Set pub_id to the Publication ID only if we need to include page numbers
                if 'IncludePages' in form:
                        pub_id=clone_from
                pub_type = publication[PUB_CTYPE]
                if 'IncludeCoverArt' in form:
                        include_coverart = 1
                else:
                        include_coverart = 0
                if 'IncludeInteriorArt' in form:
                        include_interiorart = 1
                else:
                        include_interiorart = 0

        # Check if we are importing individual titles
        elif 'ImportTitles1' in form:
                # Always include COVERART and INTERIORART titles when importing individual titles
                include_coverart = 1
                include_interiorart = 1
                titles = []
                titles_dict = {}
                for key in list(form.keys()):
                        if 'ImportTitles' not in key:
                                continue
                        title_id = XMLescape(form[key].value)
                        # Drop everything to the left of the last question mark in case a title URL was entered
                        title_id = title_id.split('?')[-1]
                        # Check that the title ID is an integer
                        try:
                                title_id = int(title_id)
                        except:
                                errorPage("Title ID must be an integer number")
                        # Load the title's data
                        title_data = tuple(SQLloadTitle(title_id))
                        if not title_data:
                                errorPage("At least one specified title does not exist")
                        # Skip duplicate titles
                        if title_data in titles:
                                continue
                        title_order = int(key.split('ImportTitles')[1])
                        titles_dict[title_order] = title_data
                # Re-sort titles by the order they were entered in
                for title_order in sorted(titles_dict.keys()):
                        title_data = titles_dict[title_order]
                        titles.append(title_data)
        else:
                errorPage("Publication or title to import content from is not specified")

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitclone.cgi">')
        printpubrecord(publication_to)

        # Retrieve the titles that are currently in publication_to and remove them from the
        # list of "titles to import" in order to avoid title duplicates
        current_titles = SQLloadTitlesXBT(publication_to[PUB_PUBID])
        for current_title in current_titles:
                if current_title in titles:
                        titles.remove(current_title)

        print('<hr class="topspace">')
        print('<h2 class="editheadline">Content</h2>')
        print('<p>')
        print('This tool imports or exports titles to a publication. You may add titles, but you')
        print('cannot delete or modify grayed out titles. ')
        print('The existing titles listed here will be automatically merged. New titles may need to')
        print('be manually merged with pre-existing titles after this submission has been approved.')
        print('<p>')
        print('<p>')

        covers = []
        for title in titles:
                if (title[TITLE_TTYPE] == 'COVERART') and include_coverart:
                        covers.append(title)
        if covers:
                # Retrieve the Help text for covers
                help = HelpCoverArt()
                print('<hr class="topspace">')
                print("<h2>Cover Art</h2>")
                print('<table class="coveredit">')
                print('<tbody id="coverBody">')

                print('<tr>')
                print('<td>&nbsp;</td>')
                printContentHeader('Title', help)
                printContentHeader('Date', help)
                print('</tr>')
                index = 1
                for cover in covers:
                        printfullcoverart(cover, index, help, 1)
                        index += 1
                printNewFullCoverButton()
                print('</tbody>')
                print('</table>')

        print('<hr class="topspace">')
        print('<h2>Regular Titles</h2>')
        print('<table class="titleedit">')
        print('<tbody id="titleBody">')
        print('<tr>')
        # Retrieve the Help text for publication content
        help = HelpTitleContent()
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        printContentHeader('Title Type', help)
        printContentHeader('Length', help)
        print('</tr>')

        NeedReviewSection = 0
        NeedInterviewSection = 0
        index = 1
        for title in titles:
                if title[TITLE_TTYPE] in ('COVERART', 'EDITOR'):
                        continue
                elif title[TITLE_TTYPE] == pub_type:
                        continue
                elif title[TITLE_TTYPE] == 'INTERIORART' and not include_interiorart:
                        continue
                elif title[TITLE_TTYPE] == 'REVIEW':
                        NeedReviewSection = 1
                elif title[TITLE_TTYPE] == 'INTERVIEW':
                        NeedInterviewSection = 1
                else:
                        printtitlerecord(title, index, pub_id, help)
                        index += 1

        if index == 1:
                printblanktitlerecord(index, help, publication_to[PUB_CTYPE])
                index += 1

        printNewTitleButton()
        print("</tbody>")
        print("</table>")

        print("<hr class=\"topspace\">")
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
        if NeedReviewSection:
                for title in titles:
                        if (title[TITLE_TTYPE] == 'REVIEW'):
                                printreviewrecord(title, index, pub_id, help)
                                index += 1
        else:
                printblankreviewrecord(index, help)
                index += 1
        printNewReviewButton()
        print("</tbody>")
        print("</table>")

        print("<hr class=\"topspace\">")
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
        if NeedInterviewSection:
                for title in titles:
                        if (title[TITLE_TTYPE] == 'INTERVIEW'):
                                printinterviewrecord(title, index, pub_id, help)
                                index += 1
        else:
                printblankinterviewrecord(index, help)
                index += 1
        printNewInterviewButton()
        print("</tbody>")
        print("</table>")

        print("<hr class=\"topspace\">")
        print("<p>")
        print('<input name="pub_id" value="0" type="HIDDEN">')
        print('<input name="child_id" value="%d" type="HIDDEN">' % int(clone_to))
        print('<input type="SUBMIT" value="Submit Data" tabindex="1">')
        print("</form>")

        PrintPostSearch(tableclose=False)
