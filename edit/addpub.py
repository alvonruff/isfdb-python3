#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2025   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 735 $
#     Date: $Date: 2021-09-06 16:25:55 -0400 (Mon, 06 Sep 2021) $


from SQLparsing import *
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *


if __name__ == '__main__':

        title = SESSION.Parameter(0, 'int')
        record = SQLloadTitle(title)
        if not record:
                SESSION.DisplayError('Record Does Not Exist')
        pub = 0

        pub_type = record[TITLE_TTYPE]
        if pub_type not in ('NOVEL', 'COLLECTION', 'OMNIBUS', 'ANTHOLOGY', 'CHAPBOOK', 'NONFICTION'):
                SESSION.DisplayError('Adding a publication to a %s record is not supported' % pub_type)

        PrintPreSearch('Add Publication')
        PrintNavBar('edit/addpub.cgi', title)

        print '<div id="HelpBox">'
        print '<b>Help on adding new publication records: </b>'
        print '<a href="%s://%s/index.php/Help:Screen:AddPublication">Help:Screen:AddPublication</a><p>' % (PROTOCOL, WIKILOC)
        print '</div>'

        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitaddpub.cgi">'
        print '<h2>Publication Metadata</h2>'
        print '<table class="pub_metadata" id="metadata">'
        print '<tbody id="pubBody">'

        help = HelpPub()

        printfield("Title", "pub_title", help, record[TITLE_TITLE], 1)

        trans_titles = SQLloadTransTitles(record[TITLE_PUBID])
        printmultiple(trans_titles, "Transliterated Title", "trans_titles", help, 1)

        authors = SQLTitleAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Author", "pub_author", help, 1)

        printfield("Date", "pub_year", help)
        printfield("Publisher", "pub_publisher", help)
        printfield("Pages", "pub_pages", help)

        printformat("pub_ptype", "Format", help)

        printfield("Pub Type", "pub_ctype", help, pub_type, 1)

        printISBN(help, None)
        printfield("Catalog ID", "pub_catalog", help)
        printfield("Price", "pub_price", help)

        printfield("Image URL", "pub_image", help)

        printfield("Pub Series", "pub_series", help)
        printfield("Pub Series #", "pub_series_num", help)
        printWebPages([], 'pub', help)

        printsource(help)

        printtextarea('Pub Note', 'pub_note', help)
        printExternalIDs(None, "External ID", "external_id", help)
        printtextarea('Note to Moderator', 'mod_note', help)

        print '</tbody>'
        print '</table>'

        print '<p>'
        print '<hr>'
        print '<p>'

        ###################
        # Cover Art section
        ###################
        help = HelpCoverArt()
        print '<h2 class="editheadline">Cover Art</h2>'
        print '<p>'
        print '<table class="coveredit">'
        print '<tbody id="coverBody">'

        printbriefblankcoverart(1, help)
        printNewBriefCoverButton()

        print "</tbody>"
        print "</table>"

        #################################
        # Regular Titles
        #################################
        print '<p>'
        print '<hr>'
        print '<p>'
        # Retrieve the Help text for publication content
        help = HelpTitleContent()
        if pub_type == 'NOVEL':
                print '<h2>Additional Regular Titles</h2>'
        else:
                print '<h2>Regular Titles</h2>'
        print '<p>'

        print '<table class="titleedit">'
        print '<tbody id="titleBody">'
        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        printContentHeader('Title Type', help)
        printContentHeader('Length', help)
        print '</tr>'

        counter = 1
        max = 10
        # For NOVELs, display only 3 (i.e. 4-1) blank Content titles
        # to account for essays, interior art, bonus stories, etc
        if pub_type == 'NOVEL':
                max = 4
        while counter < max:
                printblanktitlerecord(counter, help, pub_type)
                counter += 1
        printNewTitleButton()
        print "</tbody>"
        print "</table>"

        #####################################################
        print '<p>'
        print '<hr>'
        print '<p>'
        # Retrieve the Help text for reviews
        help = HelpReviewContent()
        print '<h2>Reviews</h2>'
        print '<p>'

        print '<table class="reviewedit">'
        print '<tbody id="reviewBody">'
        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        print '</tr>'

        counter = 1
        max = 4
        # For Novels, Display only 1 blank Content review
        if pub_type == 'NOVEL':
                max = 2
        while counter < max:
                printblankreviewrecord(counter, help)
                counter += 1

        printNewReviewButton()
        print "</tbody>"
        print "</table>"

        #####################################################
        print '<p>'
        print '<hr>'
        print '<p>'
        # Retrieve the Help text for interviews
        help = HelpInterviewContent()
        print '<h2>Interviews</h2>'
        print '<p>'

        print '<table class="interviewedit">'
        print '<tbody id="interviewBody">'
        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Interview Title', help)
        printContentHeader('Date', help)
        print '</tr>'

        counter = 1
        max = 3
        # For Novels, display only 1 blank Content interview
        if pub_type == 'NOVEL':
                max = 2
        while counter < max:
                printblankinterviewrecord(counter, help)
                counter += 1

        printNewInterviewButton()

        print '</tbody>'
        print '</table>'

        print '<p>'
        print '<hr>'
        print '<p>'
        print '<input tabindex="0" NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % (title)
        print '<input tabindex="0" name="editor" value="addpub" type="HIDDEN">'
        print '<input tabindex="0" NAME="pub_id" VALUE="%d" TYPE="HIDDEN">' % (pub)
        print '<input tabindex="1" TYPE="SUBMIT" VALUE="Submit Data">'
        print '</form>'
        print '<p>'

        PrintPostSearch(tableclose=False)
