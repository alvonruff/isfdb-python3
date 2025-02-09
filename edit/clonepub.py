#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2022   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1061 $
#     Date: $Date: 2022-12-27 13:43:52 -0500 (Tue, 27 Dec 2022) $


import cgi
import sys
import MySQLdb
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
def printpubrecord(pub, image_url, reuse_external_ids):
        help = HelpPub()
	print '<h2>Publication Metadata</h2>'
	print '<table border="0" id="metadata">'
	print '<tbody id="pubBody">'
	printfield("Title", "pub_title", help, pub.pub_title, 1)

        trans_titles = SQLloadTransPubTitles(pub.pub_id)
        printmultiple(trans_titles, "Transliterated Title", "trans_titles", help, 1)

	authors = SQLPubAuthors(pub.pub_id)
        printmultiple(authors, "Author", "pub_author", help, 1)

	printfield("Date", "pub_year", help, pub.pub_year)

        printfield("Publisher", "pub_publisher", help, pub.pub_publisher)

	printfield("Pages", "pub_pages", help, pub.pub_pages)
	
	printformat("pub_ptype", "Format", help, pub.pub_ptype)

	print '<tr>'
	printContentHeader('Pub Type:', help)

        print '<td><select tabindex="1" name="pub_ctype">'
        print '<option selected="selected">%s</option>' % pub.pub_ctype
        for ctype in ['ANTHOLOGY','CHAPBOOK','COLLECTION','FANZINE','MAGAZINE','NONFICTION','NOVEL','OMNIBUS']:
		if ctype != pub.pub_ctype:
        		print '<option>%s</option>' % (ctype)
        print '</select>'
        print '</tr>'
	
        printISBN(help, pub.pub_isbn)
	printfield("Catalog ID", "pub_catalog", help, pub.pub_catalog)
	printfield("Price", "pub_price", help, pub.pub_price)

        if image_url:
                cover_url = pub.pub_image
        else:
                cover_url = ''

	printfield("Image URL", "pub_image", help, cover_url)
	printfield("Pub Series", "pub_series", help, pub.pub_series)
	printfield("Pub Series #", "pub_series_num", help, pub.pub_series_num)
        printWebPages([], 'pub', help)
        printsource(help)
        printtextarea('Pub Note', 'pub_note', help, pub.pub_note)

        if reuse_external_ids:
                printExternalIDs(pub.identifiers, "External ID", "external_id", help)
        else:
                printExternalIDs(None, "External ID", "external_id", help)

        printtextarea('Note to Moderator', 'mod_note', help)

	print '</tbody>'
        print '</table>'

if __name__ == '__main__':

        form = cgi.FieldStorage()
	try:
                pub_id = int(form['CloneTo'].value)
                pub = pubs(db)
                pub.load(pub_id)
                if pub.error:
                        raise
                titles = getSortedTitlesInPub(pub_id)
                covers = SQLPubCovers(pub_id)
	except:
                PrintPreSearch("Clone Publication")
                PrintNavBar('edit/clonepub.cgi', 0)
                print "<h3>Error: Publication to clone is not specified.</h3>"
                PrintPostSearch(0, 0, 0, 0, 0)
                sys.exit(0)

        # Check if the editor wants to clone COVERART and image URL
        cover_art = 0
        image_url = 0
        if form.has_key('ReuseCoverArt'):
                image_url = 1
                if covers:
                        cover_art = 1

        # Check if the editor wants to clone INTERIORART
        if form.has_key('ReuseInteriorArt'):
                interior_art = 1
        else:
                interior_art = 0

        # Check if the editor wants to reuse old page numbers
        if form.has_key('ReusePageNumbers'):
                reuse_page_numbers = 1
        else:
                reuse_page_numbers = 0

        # Check if the editor wants to reuse external identifiers
        if form.has_key('ReuseExternalIDs'):
                reuse_external_ids = 1
        else:
                reuse_external_ids = 0

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Clone Publication")
	PrintNavBar('edit/clonepub.cgi', pub_id)

        print '<div id="HelpBox">'
        print '<b>Help on cloning publications: </b>'
        print '<a href="%s://%s/index.php/Help:Screen:ClonePub">Help:Screen:ClonePub</a><p>' % (PROTOCOL, WIKILOC)
        print '</div>'

	title_id = SQLgetTitleReferral(pub_id, pub.pub_ctype, 1)
	if title_id == 0:
        	print "<h3>Error: This publication is not in a cloneable state.</h3>"
		print "<p>Unable to determine the parent title of this publication."
		print "The most likely cause is that the parent title is missing or "
		print "the publication type is wrong. For instance, if this publication "
		print "is a COLLECTION, look to see that its type is set to COLLECTION "
		print "and that the parent title is set to COLLECTION as well. If the type "
		print "is wrong, edit the publication and change the type. "
		print "Then the record will be cloneable."
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitclone.cgi">'

	printpubrecord(pub, image_url, reuse_external_ids)

        print '<p>'
        print '<hr>'
        print '<p>'
        # Retrieve the Help text for publication content
        help = HelpTitleContent()
        print '<h2>Content Section</h2>'
        print """<p>This tool performs a clone operation on a publication. You may add titles, but you
                 cannot delete or modify titles. The existing titles listed here will be automatically
                 merged. Any titles that you add may need to be manually merged after submission approval.</p>"""
        print '<p>'

        # Retrieve the Help text for covers
        help = HelpCoverArt()
        print "<h2>Cover Art</h2>"
        print '<table class="coveredit">'
        print '<tbody id="coverBody">'

        if not cover_art:
                index = 1
                printbriefblankcoverart(index, help)
                index += 1
                printNewBriefCoverButton()
        else:
                print '<tr>'
                print '<td>&nbsp;</td>'
                printContentHeader('Title', help)
                printContentHeader('Date', help)
                print '</tr>'
                index = 1
                for cover in covers:
                        printfullcoverart(cover, index, help, 1)
                        index += 1
                printNewFullCoverButton()
        print "</tbody>"
        print "</table>"

        print "<p>"
        print "<hr>"
        print "<p>"

        # Retrieve the Help text for publication content
        help = HelpTitleContent()
        print "<h2>Regular Titles</h2>"

        print '<table border="0">'
        print '<tbody id="titleBody">'

        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        printContentHeader('Title Type', help)
        printContentHeader('Length', help)
        print '</tr>'

        index = 1
        for title in titles:
                if (title[TITLE_TTYPE] == 'COVERART') or (title[TITLE_TTYPE] == 'EDITOR'):
                        continue
                elif (title[TITLE_TTYPE] == 'OMNIBUS') and (pub.pub_ctype == 'OMNIBUS'):
                        continue
                elif (title[TITLE_TTYPE] == 'COLLECTION') and (pub.pub_ctype == 'COLLECTION'):
                        continue
                elif (title[TITLE_TTYPE] == 'ANTHOLOGY') and (pub.pub_ctype == 'ANTHOLOGY'):
                        continue
                # Skip INTERIORART titles if the editor doesn't want to reuse them
                elif (title[TITLE_TTYPE] == 'INTERIORART') and not interior_art:
                        continue
                elif (title[TITLE_TTYPE] == 'REVIEW'):
                        continue
                elif (title[TITLE_TTYPE] == 'INTERVIEW'):
                        continue
                else:
                        printtitlerecord(title, index, pub_id, help, reuse_page_numbers)
                        index += 1

        printblanktitlerecord(index, help, pub.pub_ctype)
        index += 1
        printNewTitleButton()
        print "</tbody>"
        print "</table>"

        print "<p>"
        print "<hr>"
        print "<p>"
        # Retrieve the Help text for reviews
        help = HelpReviewContent()
        print "<h2>Reviews</h2>"
        print '<table border="0">'
        print '<tbody id="reviewBody">'
        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        print '</tr>'
        index = 1
        for title in titles:
                if (title[TITLE_TTYPE] == 'REVIEW'):
                        printreviewrecord(title, index, pub_id, help, reuse_page_numbers)
                        index += 1
        printblankreviewrecord(index, help)
        index += 1
        printNewReviewButton()
        print "</tbody>"
        print "</table>"

        print "<p>"
        print "<hr>"
        print "<p>"
        # Retrieve the Help text for interviews
        help = HelpInterviewContent()
        print "<h2>Interviews</h2>"
        print '<table border="0">'
        print '<tbody id="interviewBody">'
        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Interview Title', help)
        printContentHeader('Date', help)
        print '</tr>'
        index = 1
        for title in titles:
                if (title[TITLE_TTYPE] == 'INTERVIEW'):
                        printinterviewrecord(title, index, pub_id, help, reuse_page_numbers)
                        index += 1
        printblankinterviewrecord(index, help)
        index += 1
        printNewInterviewButton()
        print "</tbody>"
        print "</table>"

	print "<p>"
	print "<hr>"
	print "<p>"
	print '<input name="pub_id" value="%d" type="HIDDEN">' % pub_id
	print "<input NAME=\"title_id\" VALUE=\"%d\" TYPE=\"HIDDEN\">" % title_id
	print '<input type="SUBMIT" tabindex="1" value="Clone Pub">'
	print "</form>"
	print "<p>"

	PrintPostSearch(tableclose=False)
