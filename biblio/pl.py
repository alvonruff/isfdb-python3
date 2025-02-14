#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Kevin Pulliam (kevin.pulliam@gmail.com), Bill Longley, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1197 $
#     Date: $Date: 2024-11-23 17:33:18 -0500 (Sat, 23 Nov 2024) $


from isfdb import *
from common import *
from SQLparsing import *
from library import *
from isbn import convertISBN, ISBNValidFormat, validISBN, toISBN10, toISBN13
from pubClass import pubs, pubBody

def PrintContents(titles, pub, concise):
        print('<div class="ContentBox">')

        # Display the Container title if there is one
        reference_title = None
        reference_lang = None
        if pub.pub_ctype:
                referral_title_id = SQLgetTitleReferral(pub.pub_id, pub.pub_ctype, 1)
                if referral_title_id:
                        reference_title = SQLloadTitle(referral_title_id)
                        reference_lang = reference_title[TITLE_LANGUAGE]
                        # NOVEL reference titles are not displayed here; they will be displayed in the Contents section below
                        if reference_title[TITLE_TTYPE] != 'NOVEL':
                                print('<span class="containertitle">%s Title:</span>' % reference_title[TITLE_TTYPE].title())
                                pub.PrintTitleLine(reference_title, None, reference_lang, 1)

        # Determine if there are Contents titles to display
        display_contents = 0
        for title in titles:
                # Non-NOVEL reference titles are displayed on a separate line above
                if reference_title and (title[TITLE_PUBID] == reference_title[TITLE_PUBID]) and title[TITLE_TTYPE] != 'NOVEL':
                        continue
                # COVERART titles are not to be displayed in the Contents section
                if title[TITLE_TTYPE] == 'COVERART':
                        continue
                # We have found a Contents title, so we break out of the loop
                display_contents = 1
                break

        # Display Contents items if there are any
        if display_contents:
                # Get a list of pub_content records sorted by page number
                pages = getPubContentList(pub.pub_id)

                if concise:
                        mode_word = 'Full'
                        mode_letter = 'f'
                        label = 'Fiction and Essays'
                else:
                        mode_word = 'Concise'
                        mode_letter = 'c'
                        label = 'Contents'
                output = '<h2>%s ' % label
                output += ISFDBLinkNoName('pl.cgi',
                                          '%d+%s' % (pub.pub_id, mode_letter),
                                          '(view %s Listing)' % mode_word,
                                          False,
                                          'class="listingtext"')
                output += '</h2>'
                print(output)
                print('<ul>')
                printed = []
                containers = ('OMNIBUS', 'COLLECTION', 'ANTHOLOGY', 'NONFICTION', 'CHAPBOOK')
                first_container = 1
                for item in pages:
                        content_title_id = item[PUB_CONTENTS_TITLE]
                        displayed_page_num = item[PUB_CONTENTS_PAGE]
                        # For display purposes, only use the part of the page number to the left of the first pipe (|) character
                        if displayed_page_num:
                                displayed_page_num = displayed_page_num.split('|')[0]
                        for title in titles:
                                if title[TITLE_PUBID] == content_title_id:
                                        # If this user has chosen concise display, skip INTERIORART and REVIEW records
                                        if concise and (title[TITLE_TTYPE] in ('INTERIORART', 'REVIEW')):
                                                continue
                                        # If this title has already been printed, do not print 2+ occurrences
                                        if title[TITLE_PUBID] in printed:
                                                continue
                                        # Do not display COVERART and magazine editor titles in the Content section
                                        if title[TITLE_TTYPE] in ('COVERART', 'EDITOR', 'MAGAZINE', 'FANZINE'):
                                                continue
                                        # Skip titles without a title type -- this should never happen
                                        if not title[TITLE_TTYPE]:
                                                continue
                                        # Suppress the display of the FIRST container title which matches this publication's type;
                                        # subsequent container titles of the same type will be displayed
                                        if (title[TITLE_TTYPE] in containers) and (pub.pub_ctype == title[TITLE_TTYPE]):
                                                if first_container:
                                                        first_container = 0
                                                        continue
                                        pub.PrintTitleLine(title, displayed_page_num, reference_lang)
                                        printed.append(title[TITLE_PUBID])
                print('</ul>')

        print('</div>')


#==========================================================
#                       M A I N
#==========================================================

if __name__ == '__main__':

        tag = SESSION.Parameter(0, 'str')

        arg2 = ''
        if len(SESSION.parameters) > 1:
                arg2 = SESSION.Parameter(1, 'str', None, ('c', 'f'))

        #Retrieve this user's data
        (userid, username, usertoken) = GetUserData()

        #If the format, i.e. 'c'oncise or 'f'ull, was specified explicitly in the second paratemer,
        #it overrides the default
        if arg2 == 'c':
                concise = 1
        elif arg2 == 'f':
                concise = 0
        else:
                #Retrieve this user's preferences to determine whether to use the Concise format by default
                preferences = SQLLoadUserPreferences(userid)
                concise = preferences[USER_CONCISE_DISP]

        try:
                numeric_record = int(tag)
        except:
                numeric_record = 0

        if numeric_record:
                publication = SQLGetPubById(numeric_record)
                if not publication and SQLDeletedPub(numeric_record):
                        SESSION.DisplayError('This publication has been deleted. See %s for details.' % ISFDBLink('pub_history.cgi', numeric_record, 'Edit History'))
        else:
                publication = SQLGetPubByTag(tag)

        if not publication:
                SESSION.DisplayError('Specified publication does not exist')

        pub = pubs(db)
        pub.load(publication[PUB_PUBID])

        PrintHeader('Publication: %s' % pub.pub_title)
        PrintNavbar('publication', publication, concise, 'pl.cgi', publication[PUB_PUBID])

        pub_body = pubBody()
        pub_body.pub = pub
        pub_body.userid = userid
        titles = SQLloadTitlesXBT(pub.pub_id)
        pub_body.titles = titles
        pub_body.build_page_body()
        print(pub_body.body)

        print('<li>')
        authors = SQLPubBriefAuthorRecords(pub.pub_id)
        if pub.pub_ctype in ('ANTHOLOGY', 'MAGAZINE', 'FANZINE'):
                displayPersonLabel('Editor', authors, '')
        else:
                displayPersonLabel('Author', authors, '')
        displayAuthorList(authors)

        if pub.pub_year:
                print('<li> <b>Date:</b> %s' % (ISFDBconvertDate(pub.pub_year, 1)))

        if pub.pub_isbn:
                compact = string.replace(pub.pub_isbn, '-', '')
                compact = string.replace(compact, ' ', '')

                # Bad ISBN format
                if not ISBNValidFormat(pub.pub_isbn):
                        print('  <li id="badISBN">ISBN: %s  (Bad format)' % ISFDBText(pub.pub_isbn))
                else:
                        # ISBN fails checksum validation
                        if not validISBN(pub.pub_isbn):
                                print('  <li id="badISBN">ISBN: %s  (Bad Checksum)' % ISFDBText(pub.pub_isbn))
                        # ISBN-10: display the ISBN-10 as well as the ISBN-13 in "small"
                        elif len(compact) == 10:
                                print('  <li><b>ISBN:</b> %s [<small>%s</small>]' % (convertISBN(compact), convertISBN(toISBN13(compact))))
                        # ISBN-13
                        else:
                                # ISBN-13s which start with 978 can be converted to ISBN-10, so we also display the ISBN-10
                                if compact[:3] == '978':
                                        print('  <li><b>ISBN:</b> %s [<small>%s</small>]' % (convertISBN(compact), convertISBN(toISBN10(compact))))
                                # ISBN-13s that do not start with 978 (currently 979), can't be converted to ISBN-10s
                                else:
                                        print('  <li><b>ISBN:</b> %s' % convertISBN(compact))

        if pub.pub_catalog:
                print('  <li><b>Catalog ID:</b>', ISFDBText(pub.pub_catalog))

        if pub.pub_publisher_id:
                print('<li>')
                print('  <b>Publisher:</b> %s' % ISFDBLink('publisher.cgi', pub.pub_publisher_id, pub.pub_publisher))

        if pub.pub_series_id:
                print('<li>')
                print('  <b>Pub. Series:</b> %s' % ISFDBLink('pubseries.cgi', pub.pub_series_id, pub.pub_series))

        if pub.pub_series_num:
                print('<li>')
                print('  <b>Pub. Series #:</b>', ISFDBText(pub.pub_series_num))

        if pub.pub_price:
                print('<li>')
                print('  <b>Price:</b>', ISFDBPrice(pub.pub_price))
        if pub.pub_pages:
                print('<li>')
                print('  <b>Pages:</b>', ISFDBText(pub.pub_pages))
        if pub.pub_ptype:
                print('<li>')
                print('  <b>Format:</b>', ISFDBPubFormat(pub.pub_ptype))
        if pub.pub_ctype:
                print('<li>')
                print('  <b>Type:</b>', ISFDBText(pub.pub_ctype))

        cover_art_titles = []
        cover_count = 1
        for title in titles:
                if title[TITLE_TTYPE] == 'COVERART':
                        cover_indicator = ''
                        if cover_count > 1:
                                cover_indicator = str(cover_count)
                        print('<li><b>Cover%s:</b>' % cover_indicator)
                        cover_art_titles.append(title[TITLE_PUBID])
                        pub.PrintTitleLine(title, None, None, 1)
                        cover_count += 1

        # Webpages
        webpages = SQLloadPubWebpages(int(pub.pub_id))
        PrintWebPages(webpages)

        if pub.pub_note:
                print('<li>')
                print(FormatNote(pub.pub_note, 'Notes', 'short', pub.pub_id, 'Publication'))

        if pub.identifiers:
                print('<li>')
                print('  <b>External IDs:</b>')
                pub.printExternalIDs()

        if pub.pub_tag and SQLwikiLinkExists('Publication', pub.pub_tag):
                print("<li><b>Bibliographic Comments:</b>")
                print('<a href="%s://%s/index.php/Publication:%s" dir="ltr"> View Publication comment</a> (%s)' % (PROTOCOL, WIKILOC, pub.pub_tag, pub.pub_tag))

        #Only display the image upload link if the user is logged in
        if userid:
                tag = str(pub.pub_tag)
                if pub.pub_publisher:
                        publisher_string = pub.pub_publisher
                else:
                        publisher_string = 'Unknown'
                if pub.pub_ptype:
                        format = pub.pub_ptype
                else:
                        format = ''
                pub_year = ISFDBconvertYear(pub.pub_year)
                if pub_year == 'unknown':
                        pub_year = 'Unknown year'
                cover_artists = []
                #Retrieve the cover artists for the Cover Art Titles
                for cover_art_title in cover_art_titles:
                        artists_for_title = SQLTitleBriefAuthorRecords(cover_art_title)
                        #Create a list of unique cover artists
                        for cover_artist in artists_for_title:
                                if cover_artist not in cover_artists:
                                        cover_artists.append(cover_artist)

                #For 0 or 1 cover artist, use template CID1
                if len(cover_artists) == 0:
                        template = 'CID1'
                elif len(cover_artists) == 1:
                        template = 'CID1'
                elif len(cover_artists) == 2:
                        template = 'CID1-2'
                #When 3 or more artists, use template CID1-3; only the first 3 artists will be defaulted
                else:
                        template = 'CID1-3'

                param = template + '\n|Title=' + pub.pub_title
                param += '\n|Edition=' + publisher_string
                if publisher_string == 'Unknown':
                        param += ' publisher'
                param += ' ' + pub_year
                if format:
                        param += ' ' + format
                param += '\n|Pub=' + tag
                if publisher_string:
                        param += '\n|Publisher=' + publisher_string
                if template == 'CID1':
                        if len(cover_artists) == 0:
                                param += '\n|Artist=' + 'Unknown'
                        else:
                                param += '\n|Artist=%s\n|ArtistId=%d' % (cover_artists[0][1], cover_artists[0][0])
                elif template == 'CID1-2':
                        param += '\n|Artist1=%s\n|Artist2=%s' % (cover_artists[0][1], cover_artists[1][1])
                elif template == 'CID1-3':
                        param += '\n|Artist1=%s\n|Artist2=%s' % (cover_artists[0][1], cover_artists[1][1])
                        param += '\n|Artist3=%s' % cover_artists[2][1]
                param += '\n|Source=Scanned by [[User:' + username + ']]'
                param = urllib.quote("{{%s}}" % param)
                upload = 'wpDestFile=%s.jpg&amp;wpUploadDescription=%s' % (tag, param)
                print("<li>")
                if not pub.pub_image:
                        message = 'Upload cover scan'
                else:
                        message = 'Upload new cover scan'
                print('<a href="%s://%s/index.php/Special:Upload?%s" target="_blank">%s</a>' % (PROTOCOL, WIKILOC, upload, message))

        print('</ul>')
        if pub.pub_image:
                print('</td>')
                print('</table>')
                (webpage, credit, home_page, linked_page) = BuildDisplayedURL(pub.pub_image)
                print('Cover art supplied by <a href="%s" target="_blank">%s</a>' % (home_page, credit))
                if linked_page:
                        print(' on <a href="%s" target="_blank">this Web page</a>' % linked_page)
                if 'amazon.com' in pub.pub_image:
                        if '/images/P/' in pub.pub_image:
                                print("""<br>The displayed Amazon image is based on the publication's ISBN. It may no
                                        longer reflect the actual cover of this particular edition.""")
                        elif '/images/G/' in pub.pub_image:
                                print("""<br>The displayed Amazon image is possibly unstable and may no
                                        longer reflect the actual cover of this particular edition.""")

        print('</div>')

        PrintContents(titles, pub, concise)

        pub.PrintPrimaryVerifications()
        #pub.PrintAllSecondaryVerifications()
        active_secondary_vers = pub.PrintActiveSecondaryVerifications()
        if userid:
                if active_secondary_vers:
                        print(ISFDBLink('edit/verify.cgi', pub.pub_id, 'Show/Add other Verifications'))
                else:
                        print(ISFDBLink('edit/verify.cgi', pub.pub_id, 'Add Verifications'))

        PrintTrailer('publication', 0, 0)


