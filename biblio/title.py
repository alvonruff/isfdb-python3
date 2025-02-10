#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley, Uzume, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1004 $
#     Date: $Date: 2022-09-16 07:43:01 -0400 (Fri, 16 Sep 2022) $


from SQLparsing import *
from awardClass import *
from common import *
from library import *
from login import *


def displayCommon(title, user):
        printRecordID('Title', title[TITLE_PUBID], user.id)

def PrintOneVariantType(variants, title, authors, translation):
        print '<td class="variants">'
        print '<table class="variantscolumn">'
        print '<tr class="table2">'
        print '<th>Year</th>'
        if translation:
                print '<th>Language</th>'
        print '<th>Title</th>'
        print '</tr>'
        bgcolor = 0
        for variant in variants:
                PrintOneVariant(variant, title, authors, bgcolor, translation)
                bgcolor ^= 1
        print '</table>'
        print '</td>'

def PrintOneVariant(variant, parent, parent_authors, bgcolor, translation):
        print '<tr class="table%d">' % (bgcolor+1)
        # Display variant year and VT notes in a mouseover bubble
        print '<td>'
        if variant[TITLE_NOTE]:
                bubble_values = []
                notes = SQLgetNotes(variant[TITLE_NOTE])
                bubble_values.append(FormatNote(notes, '', 'full', 0, '', 0))
                print ISFDBMouseover(bubble_values, convertTitleYear(variant), '', SESSION.ui.info_sign, note = 1)
        else:
                print convertTitleYear(variant)
        print '</td>'
        # Display translation language
        if translation:
                print '<td>'
                print LANGUAGES[int(variant[TITLE_LANGUAGE])]
                print '</td>'
        # Display variant title and, optionally, type and author(s)
        print '<td>'
        output = ISFDBLink('title.cgi', variant[TITLE_PUBID], variant[TITLE_TITLE])
        # Display the title type of the variant only if:
        #  1. it's different from the title type of the parent
        #  2. it is not SERIAL
        #  3. it is not a COVERART title reprinted as an INTERIORART title
        #  4. it is not an INTERIORART title reprinted as a COVERART title
        if ((variant[TITLE_TTYPE] != parent[TITLE_TTYPE])
            and (variant[TITLE_TTYPE] != 'SERIAL')
            and not ((variant[TITLE_TTYPE] == 'INTERIORART' and parent[TITLE_TTYPE] == 'COVERART'))
            and not ((variant[TITLE_TTYPE] == 'COVERART' and parent[TITLE_TTYPE] == 'INTERIORART'))):
                output += ' [%s]' % variant[TITLE_TTYPE]
        print output
        variant_authors = SQLTitleBriefAuthorRecords(variant[TITLE_PUBID])
        # Display the variant's authors only if they are different from the parent title's authors
        if set(variant_authors) != set(parent_authors):
                displayVariantAuthors(variant_authors, '', None)
        print '</td>'
        print '</tr>'
        return

def PrintReviews(reviews, title_language):
        # First, create a multi-level dictionary of review Titles sorted by
        # canonical review date, canonical review ID, pub date, pub ID and review ID
        review_dict = AutoVivification()
        for review in reviews:
                review_id = review[0]
                review_date = review[1]
                sort_id = review[3]
                if not sort_id:
                        sort_id = review_id
                sort_date = review[4]
                if not sort_date:
                        sort_date = review_date
                pub_id = review[5]
                pub_date = review[7]
                # Change '0000-00-00' to '9999-99-99' so that they appear last
                if sort_date == '0000-00-00':
                        sort_date = '9999-99-99'
                # If this review's month is 00, display it after the reviews whose month is not 00
                if sort_date[5:7] == '00':
                        sort_date = sort_date[:4] + '-13-' + sort_date[8:]
                # Pubs with a '0000-00-00' date should appear last
                if pub_date == '0000-00-00':
                        pub_date = '9999-99-99'
                # If this pub's month is 00, display it after the pubs whose month is not 00
                if pub_date[5:7] == '00':
                        pub_date = pub_date[:4] + '-13-' + pub_date[8:]
                review_dict[sort_date][sort_id][pub_date][pub_id][review_id] = review

        # If no eligible pubs were found, don't print anything
        if not review_dict:
                return
        
        print '<div class="ContentBox">'
        print '<h3 class="contentheader">Reviews</h3>'
        print '<ul class="noindent">'

        for sort_date in sorted(review_dict.keys()):
                for sort_id in review_dict[sort_date]:
                        # Initialize the counter of publications for this review
                        pub_counter = 0
                        for pub_date in sorted(review_dict[sort_date][sort_id]):
                                for pub_id in review_dict[sort_date][sort_id][pub_date]:
                                        for review_id in review_dict[sort_date][sort_id][pub_date][pub_id]:
                                                review_data = review_dict[sort_date][sort_id][pub_date][pub_id][review_id]
                                                pub_title = review_data[6]
                                                review_language = review_data[2]
                                                parent_review_id = review_data[3]
                                                display_review_date = sort_date
                                                if display_review_date == '9999-99-99':
                                                        display_review_date = '0000-00-00'
                                                display_pub_date = pub_date
                                                if display_pub_date == '9999-99-99':
                                                        display_pub_date = '0000-00-00'
                                                if parent_review_id:
                                                        parent_review_authors = SQLTitleBriefAuthorRecords(parent_review_id)
                                                        parent_review_author_ids = [item[0] for item in parent_review_authors]
                                                        variant_review_authors = SQLTitleBriefAuthorRecords(review_id)
                                                        variant_review_author_ids = [item[0] for item in variant_review_authors]
                                                else:
                                                        parent_review_authors = SQLTitleBriefAuthorRecords(review_id)
                                                        parent_review_author_ids = [item[0] for item in parent_review_authors]
                                                        variant_review_authors = []
                                                        variant_review_author_ids = []
                                                
                                                pub_counter += 1
                                                if pub_counter == 1:
                                                        print '<li>%s ' % ISFDBLinkNoName('title.cgi', review_id, 'Review')
                                                        # Only display the review language if both languages are defined and are different
                                                        if review_language and title_language and (review_language != title_language):
                                                                print ' [%s] ' % LANGUAGES[int(review_language)]
                                                        print ' by '
                                                        if parent_review_id:
                                                                PrintAllAuthors(parent_review_id)
                                                                if set(variant_review_author_ids) != set(parent_review_author_ids):
                                                                        displayVariantAuthors(variant_review_authors, '', None)
                                                        else:
                                                                PrintAllAuthors(review_id)

                                                        print ' (%s) ' % ISFDBconvertYear(display_review_date[0:4])
                                                        output = ' in %s' % ISFDBLink('pl.cgi', pub_id, pub_title)
                                                        if display_review_date != display_pub_date:
                                                                output += ', (%s)' % ISFDBconvertYear(display_pub_date[0:4])
                                                        print output
                                                else:
                                                        if pub_counter == 2:
                                                                print ', reprinted in:'
                                                        # Only display the review language if both languages are defined and are different
                                                        if review_language and title_language and (review_language != title_language):
                                                                language_statement = ' [%s] ' % LANGUAGES[int(review_language)]
                                                        else:
                                                                language_statement = ''
                                                        print '<li>%s %s %s' % (SESSION.ui.enspace,
                                                                                SESSION.ui.enspace,
                                                                                language_statement)
                                                        if parent_review_id and (set(variant_review_author_ids) != set(parent_review_author_ids)):
                                                                        displayVariantAuthors(variant_review_authors, '', None)
                                                        print ISFDBLink('pl.cgi', pub_id, pub_title)
                                                        print ' (%s)' % ISFDBconvertYear(display_pub_date[0:4])
                                                
        print '</ul>'
        print '</div>'
        return


if __name__ == '__main__':

        title_id = SESSION.Parameter(0, 'int')

        user = User()
        user.load()

        # Get the variant display option:
        # 0 means display all variants
        # 1 means do not display translations, but display same-language variants
        # 2 means do not display any variants, either translated or same-language
        if user.display_title_translations:
                default_variant_display = 0
        else:
                default_variant_display = 1
        variant_display = SESSION.Parameter(1, 'int', default_variant_display, (0, 1, 2))

        ########################################
        # STEP 1 - Get the title record
        ########################################
        title = SQLloadTitle(title_id)
        if not title:
                if SQLDeletedTitle(title_id):
                        SESSION.DisplayError('This title has been deleted. See %s for details.' % ISFDBLink('title_history.cgi', title_id, 'Edit History'))
                else:
                        SESSION.DisplayError('Unknown Title Record')

        browser_title = "Title: " + title[TITLE_TITLE]
        PrintHeader(browser_title)
        PrintNavbar('title', title[TITLE_TTYPE], title_id, 'title.cgi', title_id)

        SQLupdateTitleViews(title_id)

        # Retrieve this title's variants
        titles = SQLgetTitleVariants(title_id)

        print '<div class="ContentBox">'

        # Transliterated title(s)
        trans_titles = SQLloadTransTitles(title_id)

        if title[TITLE_TTYPE] == 'REVIEW':
                reviewed_title = SQLfindReviewedTitle(title_id)
                # If this is a VT'd REVIEW and not linked to a regular title, check
                # if its parent is linked to a regular title
                if not reviewed_title and title[TITLE_PARENT]:
                        parent_title = SQLloadTitle(title[TITLE_PARENT])
                        reviewed_title = SQLfindReviewedTitle(parent_title[TITLE_PUBID])
                if reviewed_title:
                        trans_titles_dict = {reviewed_title: trans_titles}
                        print '<b>Review of:</b> %s' % ISFDBLink('title.cgi', reviewed_title,
                                                                 title[TITLE_TITLE], False, '', trans_titles_dict)
                else:
                        print "<b>Review of:</b>", ISFDBMouseover(trans_titles, title[TITLE_TITLE], '')
                displayCommon(title, user)
                authors = SQLReviewBriefAuthorRecords(title_id)
                displayPersonLabel('Author', authors)
                displayPersons(authors)
        elif title[TITLE_TTYPE] == 'INTERVIEW':
                print "<b>Interview Title:</b>", ISFDBMouseover(trans_titles, title[TITLE_TITLE], '')
                displayCommon(title, user)
                authors = SQLInterviewBriefAuthorRecords(title_id)
                displayPersonLabel('Interviewee', authors)
                displayPersons(authors)
        else:
                print "<b>Title:</b>", ISFDBMouseover(trans_titles, title[TITLE_TITLE], '')
                displayCommon(title, user)

        ########################################
        # STEP 2 - Get the title's authors
        ########################################
        authors = SQLTitleBriefAuthorRecords(title_id)
        if title[TITLE_TTYPE] in ('ANTHOLOGY', 'EDITOR'):
                displayPersonLabel('Editor', authors)
        elif title[TITLE_TTYPE] == 'REVIEW':
                displayPersonLabel('Reviewer', authors)
        elif title[TITLE_TTYPE] == 'INTERVIEW':
                displayPersonLabel('Interviewer', authors)
        else:
                displayPersonLabel('Author', authors)
        displayPersons(authors)
        print '<br>'

        print '<b>Date:</b> ', ISFDBconvertDate(title[TITLE_YEAR], 1)

        if title[TITLE_PARENT]:
                parent_title = SQLloadTitle(title[TITLE_PARENT])
                if parent_title == []:
                        print "<br>"
                        print '<b>Variant Title ERROR:</b> Parent Title=%d' % title[TITLE_PARENT]
                else:
                        print "<br>"
                        label = 'Variant Title of'
                        if title[TITLE_TTYPE] == 'COVERART' and parent_title[TITLE_TTYPE] == 'INTERIORART':
                                label = '%s interior art' % label
                        if parent_title[TITLE_TTYPE] == 'COVERART' and title[TITLE_TTYPE] == 'INTERIORART':
                                label = '%s cover art for' % label
                        print '<b>%s:</b> %s' % (label, ISFDBLink('title.cgi', title[TITLE_PARENT], parent_title[TITLE_TITLE]))
                        if parent_title[TITLE_LANGUAGE] and title[TITLE_LANGUAGE] != parent_title[TITLE_LANGUAGE]:
                                print '[%s]' % LANGUAGES[int(parent_title[TITLE_LANGUAGE])]
                        if title[TITLE_YEAR] != parent_title[TITLE_YEAR]:
                                print '(%s)' % ISFDBconvertYear(parent_title[TITLE_YEAR][:4])
                        vauthors = SQLTitleBriefAuthorRecords(parent_title[TITLE_PUBID])
                        if set(authors) != set(vauthors):
                                output = ' (by '
                                counter = 0
                                for vauthor in vauthors:
                                        if counter:
                                                output += ' <b>and</b> '
                                        output += ISFDBLink('ea.cgi', vauthor[0], vauthor[1])
                                        counter += 1
                                output += ')'
                                print output
                        print ' [may list more publications, awards, reviews, votes and covers]'

        if title[TITLE_TTYPE]:
                print "<br>"
                print "<b>Type:</b>", title[TITLE_TTYPE]
                if title[TITLE_JVN] == 'Yes':
                        print ' [juvenile]'
                if title[TITLE_NVZ] == 'Yes':
                        print ' [novelization]'
                if title[TITLE_NON_GENRE] == 'Yes':
                        print ' [non-genre]'
                if title[TITLE_GRAPHIC] == 'Yes':
                        print ' [graphic format]'

        if title[TITLE_STORYLEN]:
                print "<br>"
                print "<b>Length:</b>"
                print title[TITLE_STORYLEN]

        if title[TITLE_CONTENT]:
                print '<br>'
                print '<b>Content:</b>'
                print ISFDBText(title[TITLE_CONTENT])

        if title[TITLE_SERIES]:
                series = SQLget1Series(title[TITLE_SERIES])
                print '<br>'
                print '<b>Series:</b> %s' % ISFDBLink('pe.cgi', series[SERIES_PUBID], series[SERIES_NAME])
                if title[TITLE_SERIESNUM] is not None:
                        print "<br>"
                        output = '<b>Series Number:</b> %d' % title[TITLE_SERIESNUM]
                        if title[TITLE_SERIESNUM_2] is not None:
                                output += '.%s' % title[TITLE_SERIESNUM_2]
                        print output
        elif title[TITLE_PARENT]:
                parent_title = SQLloadTitle(title[TITLE_PARENT])
                if parent_title == []:
                        # Already generated an error message above
                        pass
                else:
                        if parent_title[TITLE_SERIES]:
                                series = SQLget1Series(parent_title[TITLE_SERIES])
                                print '<br>'
                                print '<b>Series:</b> %s' % ISFDBLink('pe.cgi', series[SERIES_PUBID], series[SERIES_NAME])
                        if parent_title[TITLE_SERIESNUM] is not None:
                                print "<br>"
                                output = '<b>Series Number:</b> %d' % parent_title[TITLE_SERIESNUM]
                                if parent_title[TITLE_SERIESNUM_2] is not None:
                                        output += '.%s' % parent_title[TITLE_SERIESNUM_2]
                                print output


        # Webpages
        webpages = SQLloadTitleWebpages(int(title_id))
        PrintWebPages(webpages, '<br>')

        if title[TITLE_LANGUAGE]:
                print '<br><b>Language:</b> %s' % (LANGUAGES[int(title[TITLE_LANGUAGE])])

        br_required = 1
        if title[TITLE_NOTE]:
                note = SQLgetNotes(title[TITLE_NOTE])
                print FormatNote(note, "Note", 'short', title_id, 'Title')
                br_required = 0
        if title[TITLE_SYNOP]:
                note = SQLgetNotes(title[TITLE_SYNOP])
                print FormatNote(note, "Synopsis", 'short', title_id, 'Synopsis')
                br_required = 0

        if br_required:
                print '<br>'

        # Votes
        (vote_count, average_vote, composite_vote_count, composite_average_vote, user_vote) = SQLLoadVotes(title[TITLE_PUBID], titles, user.id)
        print '<b>User Rating:</b>'
        if composite_vote_count:
                if vote_count:
                        if vote_count > 1:
                                plural = 's'
                        else:
                                plural = ''
                        print ' %2.2f (%d vote%s)' % (average_vote, vote_count, plural)
                elif composite_vote_count:
                        print 'None.'
                if composite_vote_count != vote_count:
                        if composite_vote_count > 1:
                                plural = 's'
                        else:
                                plural = ''
                        print ' <b>Including variants and translations:</b> %2.2f (%d vote%s)' % (composite_average_vote, composite_vote_count, plural)
                print '<b>Your vote:</b>'
                if user_vote:
                        print user_vote
                else:
                        print 'Not cast'
        else:
                print 'This title has no votes.'
        print ISFDBLink('edit/vote.cgi', title[TITLE_PUBID], 'VOTE', False, 'class="inverted bold"')

        # Retrieve all tags for this title and its parent (if present)
        tags = SQLgetAllTitleTags(title[TITLE_PUBID], title[TITLE_PARENT], int(user.id))
        print '<br>'
        print '<b>Current Tags:</b>'
        if not tags:
                print 'None'
        else:
                first = 1
                output = ''
                for tag in tags:
                        if first:
                                output = '%s (%d)' % (ISFDBLink('tag.cgi', tag[0], tag[1]), tag[2])
                                first = 0
                        else:
                                output += ', %s (%d)' % (ISFDBLink('tag.cgi', tag[0], tag[1]), tag[2])
                print output
                if SQLisUserModerator(user.id):
                        print ISFDBLink('mod/tag_breakdown.cgi', title[TITLE_PUBID], 'View Tag Breakdown', False, 'class="inverted" ')

        # Only allow adding tags if the current title is not a variant of another one
        if not title[TITLE_PARENT]:
                if user.id:
                        my_tags = SQLgetUserTags(title_id, user.id)
                        print '<br>'
                        print '<form method="post" action="%s:/%s/edit/addquicktag.cgi" name="quicktag">' % (PROTOCOL, HTFAKE)
                        # We need a div here because "strict" HTML rules only allow block level elements in forms
                        print '<div class="quicktag">'
                        print '<b>Add quick tag:</b> '
                        print '<select name="tag">'
                        print '<option value="">select a value</option>'
                        options = ['alternate history',
                                   'fantasy',
                                   'historical fantasy',
                                   'horror',
                                   'juvenile fantasy',
                                   'juvenile sf',
                                   'military sf',
                                   'near future',
                                   'parallel universe',
                                   'paranormal romance',
                                   'science fiction',
                                   'space opera',
                                   'steampunk',
                                   'time travel',
                                   'urban fantasy',
                                   'vampires',
                                   'werewolf',
                                   'young-adult fantasy',
                                   'young-adult horror',
                                   'young-adult sf',
                                   'zombies']
                        #Create an all-lowercase version of "my tag" list
                        my_tags_lower = []
                        for my_tag in my_tags:
                                my_tags_lower.append(my_tag.lower())
                        for option in options:
                                #Ignore any tags that this user has already used for this title
                                if option.lower() in my_tags_lower:
                                        continue
                                print '<option>%s</option>' % (option)
                        print '</select>'
                        print '<input NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % int(title_id)
                        print '<input type="Submit" VALUE="Submit Tag">'
                        print '%s ' % ISFDBLink('edit/edittags.cgi', title[TITLE_PUBID], 'or manage Tags', False, 'class="inverted bold"')
                        print '</div>'
                        print '</form>'
                else:
                        print '%s ' % ISFDBLink('edit/edittags.cgi', title[TITLE_PUBID], 'Add Tags', False, 'class="inverted bold"')
                print '</div>'

        ########################################
        # STEP 3 - Get any variants
        ########################################
        if titles:
                headers = []
                variants = []
                translations = []
                serials = []
                translated_serials = []
                coverart = []
                translated_coverart = []
                interiorart = []
                translated_interiorart = []
                print '<div class="ContentBox">'
                print '<h3 class="contentheader">Other Titles</h3>'
                # Split the list of variants into four lists:
                #   variants
                #   translations
                #   serializations
                #   translated serializations
                # Each list is displayed in its own table column
                for variant in titles:
                        if not variant[TITLE_LANGUAGE]:
                                same_language = 1
                        elif not title[TITLE_LANGUAGE]:
                                same_language = 1
                        elif variant[TITLE_LANGUAGE] == title[TITLE_LANGUAGE]:
                                same_language = 1
                        else:
                                same_language = 0
                        if variant[TITLE_TTYPE] == 'SERIAL':
                                if same_language:
                                        serials.append(variant)
                                else:
                                        translated_serials.append(variant)
                        elif variant[TITLE_TTYPE] == 'COVERART' and title[TITLE_TTYPE] == 'INTERIORART':
                                if same_language:
                                        coverart.append(variant)
                                else:
                                        translated_coverart.append(variant)
                        elif variant[TITLE_TTYPE] == 'INTERIORART' and title[TITLE_TTYPE] == 'COVERART':
                                if same_language:
                                        interiorart.append(variant)
                                else:
                                        translated_interiorart.append(variant)
                        else :
                                if same_language:
                                        variants.append(variant)
                                else:
                                        translations.append(variant)
                if variants:
                        headers.append('Variant Titles')
                if translations:
                        headers.append('Translations')
                if serials:
                        headers.append('Serializations')
                if translated_serials:
                        headers.append('Translated Serializations')
                if coverart:
                        headers.append('As Cover Art')
                if translated_coverart:
                        headers.append('Translated as Cover Art')
                if interiorart:
                        headers.append('As Interior Art')
                if translated_interiorart:
                        headers.append('Translated as Interior Art')

                print '<table>'
                print '<tr class="table2">'
                for header in headers:
                        print '<th>%s</th>' % header
                print '</tr>'
                print '<tr>'
                if variants:
                        PrintOneVariantType(variants, title, authors, 0)
                if translations:
                        PrintOneVariantType(translations, title, authors, 1)
                if serials:
                        PrintOneVariantType(serials, title, authors, 0)
                if translated_serials:
                        PrintOneVariantType(translated_serials, title, authors, 1)
                if coverart:
                        PrintOneVariantType(coverart, title, authors, 0)
                if translated_coverart:
                        PrintOneVariantType(translated_coverart, title, authors, 1)
                if interiorart:
                        PrintOneVariantType(interiorart, title, authors, 0)
                if translated_interiorart:
                        PrintOneVariantType(translated_interiorart, title, authors, 1)
                print '</tr>'
                print '</table>'
                print '</div>'

        ########################################
        # STEP 4 - Get the title's award data
        ########################################
        if not user.suppress_awards:
                awards_list = SQLTitleAwards(title_id)
                if awards_list:
                        print '<div class="ContentBox">'
                        print '<h3 class="contentheader">Awards</h3>'
                        award = awards(db)
                        award.PrintAwardTable(awards_list, 0)
                        print '</div>'

        ########################################################
        # STEP 5 - Get the title's pub data and display all pubs
        ########################################################
        print '<div class="ContentBox">'
        print '<h3 class="contentheader">Publications</h3>'
        retrieval_function = SQLGetPubsByTitle
        # If there are variants and/or translations, let the user limit
        # the list if displayed pubs in different ways
        if titles:
                options = {}
                options[0] = ('Displaying all variants and translations',
                              'Display all variants and translations',
                              SQLGetPubsByTitle)
                options[1] = ('Not displaying translations',
                              'Do not display translations',
                              SQLGetPubsByTitleNoTranslations)
                options[2] = ('Not displaying variants or translations',
                              'Do not display variants or translations',
                              SQLGetPubsByTitleNoParent)
                output = options[variant_display][0]
                retrieval_function = options[variant_display][2]
                for option_number in sorted(options.keys()):
                        if option_number != variant_display:
                                output += ' %s ' % SESSION.ui.bullet
                                output += ISFDBLink('title.cgi',
                                                    '%d+%d' % (int(title_id), option_number),
                                                    options[option_number][1],
                                                    False,
                                                    '',
                                                    {})
                print output
                print '<p>'
        pubs = retrieval_function(title_id)
        PrintPubsTable(pubs, "title", user)

        ###################################################################
        # STEP 6a - Display cover art of the pubs for COVERART records only
        ###################################################################
        if title[TITLE_TTYPE] == 'COVERART':
                title_ids = [title_id]
                for one_title in titles:
                        title_ids.append(one_title[TITLE_PUBID])
                for pub in pubs:
                        # Skip pubs without a cover image
                        if not pub[PUB_IMAGE]:
                                continue
                        # Skip pubs with INTERIORART variants of this cover art title
                        covers = SQLPubCovers(pub[PUB_PUBID])
                        eligible = 0
                        for cover in covers:
                                cover_id = cover[TITLE_PUBID]
                                if cover_id in title_ids:
                                        eligible = 1
                        if eligible:
                                print ISFDBScan(pub[PUB_PUBID], pub[PUB_IMAGE])
        #####################################################################
        # STEP 6b - Display a link to the cover page for non-COVERART records
        #####################################################################
        elif pubs:
                for pub in pubs:
                        if pub[PUB_IMAGE]:
                                if user.covers_display:
                                        print ISFDBScan(pub[PUB_PUBID], pub[PUB_IMAGE])
                                else:
                                        print ISFDBLink('titlecovers.cgi', title[TITLE_PUBID],
                                                        'View all covers for %s' % title[TITLE_TITLE],
                                                        False, 'class="bold"')
                                        if user.id:
                                                print ' (or change %s to always display covers on this page)' % ISFDBLink('mypreferences.cgi', '', 'User Preferences')
                                        else:
                                                print ' (logged in users can change User Preferences to always display covers on this page)'
                                        break
        print '</div>'

        ########################################
        # STEP 7 - Get the title's reviews
        ########################################
        if user.suppress_reviews:
                pass
        else:
                reviews = SQLloadAllTitleReviews(title[TITLE_PUBID])
                PrintReviews(reviews, title[TITLE_LANGUAGE])

        ###################################################################################
        # STEP 8 - Print bibliographic warnings only if this user's Preferences call for it
        ###################################################################################
        if user.id and not user.suppress_bibliographic_warnings and len(pubs):

                print '<div class="ContentBox">'
                print '<h3 class="contentheader">Bibliographic Warnings</h3>'
                print '<ul class="noindent">'
                nonefound = 1
                for pub in pubs:

                        # Check to make sure that if the title is a collection, then the 
                        # pub is a collection, an omnibus or a magazine
                        if title[TITLE_TTYPE] == 'COLLECTION':
                                if pub[PUB_CTYPE] not in ('COLLECTION', 'OMNIBUS', 'MAGAZINE'):
                                        print '<li> Type Mismatch (Pub=<i>%s</i>, should be <i>%s</i>): ' % (pub[PUB_CTYPE], title[TITLE_TTYPE])
                                        print ISFDBLink("pl.cgi", pub[PUB_PUBID], pub[PUB_TITLE])
                                        nonefound = 0

                        # Check to make sure that if the title is an anthology, then the 
                        # pub is an anthology, an omnibus or a magazine
                        if title[TITLE_TTYPE] == 'ANTHOLOGY':
                                if pub[PUB_CTYPE] not in ('ANTHOLOGY', 'OMNIBUS', 'MAGAZINE'):
                                        print '<li> Type Mismatch (Pub=<i>%s</i>, should be <i>%s</i>): ' % (pub[PUB_CTYPE], title[TITLE_TTYPE])
                                        print ISFDBLink("pl.cgi", pub[PUB_PUBID], pub[PUB_TITLE])
                                        nonefound = 0

                        if pub[PUB_YEAR] == '0000-00-00':
                                print '<li> Unknown Publication Date:'
                                print '%s (%s)' % (ISFDBLink("pl.cgi", pub[PUB_PUBID], pub[PUB_TITLE]), ISFDBconvertDate(pub[PUB_YEAR], 1))
                                nonefound = 0

                        year_num = int(pub[PUB_YEAR][0:4])
                        # If the book has an ISBN or a catalog ID or is an e-book, magazine, fanzine, then we are OK
                        if (pub[PUB_ISBN]
                            or pub[PUB_CATALOG]
                            or pub[PUB_PTYPE] in ('ebook', 'digital audio download')
                            or pub[PUB_CTYPE] in ('MAGAZINE', 'FANZINE')):
                                pass
                        elif year_num > 1950:
                                # Do not check for catalog ID/ISBN for hardcovers published prior to 1972
                                if (year_num < 1972) and (pub[PUB_PTYPE] == 'hc'):
                                        pass
                                else:
                                        print '<li> Missing ISBN/Catalog ID:'
                                        print '%s (%s)' % (ISFDBLink("pl.cgi", pub[PUB_PUBID], pub[PUB_TITLE]), ISFDBconvertDate(pub[PUB_YEAR], 1))
                                        nonefound = 0

                        if pub[PUB_PRICE] or pub[PUB_PTYPE] == 'webzine':
                                pass
                        else:
                                print '<li> Missing price:'
                                print '%s (%s)' % (ISFDBLink("pl.cgi", pub[PUB_PUBID], pub[PUB_TITLE]), ISFDBconvertDate(pub[PUB_YEAR], 1))
                                nonefound = 0

                        if (pub[PUB_PAGES]
                            or (pub[PUB_PTYPE] in ('ebook', 'webzine'))
                            or ('audio' in pub[PUB_PTYPE])
                            or ('digital' in pub[PUB_PTYPE])):
                                pass
                        else:
                                print '<li> Missing page count:'
                                print '%s (%s)' % (ISFDBLink("pl.cgi", pub[PUB_PUBID], pub[PUB_TITLE]), ISFDBconvertDate(pub[PUB_YEAR], 1))
                                nonefound = 0

                        if pub[PUB_PTYPE]:
                                if pub[PUB_PTYPE] == 'unknown':
                                        print '<li> Unknown publication format:'
                                        print '%s (%s)' % (ISFDBLink("pl.cgi", pub[PUB_PUBID], pub[PUB_TITLE]), ISFDBconvertDate(pub[PUB_YEAR], 1))
                                        nonefound = 0

                if nonefound:
                        print "<li> None."
                print "</ul>"
                print '</div>'
        
        PrintTrailer('title', title_id, title_id)
