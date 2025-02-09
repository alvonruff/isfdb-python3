#
#     (C) COPYRIGHT 2005-2024 	Al von Ruff, Kevin Pulliam (kevin.pulliam@gmail.com), Ahasuerus, Bill Longley and Dirk Stoecker
#		ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1176 $
#     Date: $Date: 2024-05-02 19:26:24 -0400 (Thu, 02 May 2024) $

from isfdb import *
from SQLparsing import *
from awardClass import *
from login import *
from library import *
from navbar import *
from isbn import ISBNValidFormat


def validateMonth(string):
        now = datetime.datetime.now()
        # Validate that the passed string is in the YYYY-MM format
        error = "Month must be specified using the YYYY-MM format"
        if len(string ) != 7:
                return (0, 0, error)

        if string[4:5] != '-':
                return (0, 0, error)
        try:
                year=int(string[0:4])
                month=int(string[5:7])
                if (year < 1) or (year > (now.year +1)):
                        return (0, 0 , "Year must be between 1 and one year in the future")
                if (month <1) or (month > 12):
                        return (0, 0 , "Month must be between 01 and 12")
                return (year, month, '')

        except:
                return (0, 0, error)

def displayPersonLabel(person_type, persons, line_start = '<br>'):
        if len(persons) > 1:
                many = 's'
        else:
                many = ''
        print "%s<b>%s%s:</b>" % (line_start, person_type, many)

def displayPersons(persons):
        counter = 0
        for person in persons:
                if counter:
                        print " <b>and</b> "
                displayAuthorById(person[0], person[1])
                counter += 1

def PrintNewPubs(userid):
	print '<div class="divider">'
        print 'Add New Data:'
	print '</div>'
	print '<ul class="navbar">'
	for pub_type in SESSION.db.pub_types:
                print '<li>%s' % ISFDBLinkNoName('edit/newpub.cgi', pub_type.title(), 'Add New %s' % pub_type.title())
        print '<li>%s' % ISFDBLinkNoName('edit/select_award_type.cgi', '0', 'Add Untitled Award')
	print '</ul>'
	return

def convertTitleYear(title):
	try:
		yearstr = ISFDBconvertYear(title[TITLE_YEAR][:4])
	except:
		yearstr = ISFDBconvertYear('0000')
	return yearstr

def displayTitle(title, author_id, parent_authors, series_type, variants, serials,
                 parents_with_pubs, variant_authors, translit_titles, translit_authors,
                 user, original_language = 0, nongenre = 0):
        displayMainTitle(title, author_id, parent_authors, series_type,
                         original_language, translit_titles, translit_authors, nongenre)
        displayVariants(title, parent_authors, variants, serials, variant_authors,
                        author_id, parents_with_pubs, translit_titles, translit_authors)

def displayMainTitle(title, author_id, authors, series_type, original_language, translit_titles, translit_authors, nongenre):
        output = buildCoreTitleLine(title, original_language, translit_titles)

	# Novel never gets a tag
	if title[TITLE_TTYPE] == 'NOVEL':
		pass
	# Omnibus always gets a tag
	elif title[TITLE_TTYPE] == 'OMNIBUS':
		if title[TITLE_CONTENT]:
			output += ' <b>[O/%s]</b> ' % title[TITLE_CONTENT]
		else:
			output += ' <b>[O]</b> '
	# Collection always gets a tag unless not in a series
	elif title[TITLE_TTYPE] == 'COLLECTION':
		if series_type != SERIES_TYPE_OTHER:
			output += ' <b>[C]</b> '
	# Other things get a tag if not in a series of matching type
	elif series_type != SERIES_TYPE_OTHER:
		if title[TITLE_TTYPE] == 'ANTHOLOGY':
			if series_type != SERIES_TYPE_ANTH:
				output += ' <b>[A]</b> '
		elif title[TITLE_TTYPE] == 'SHORTFICTION':
			if series_type != SERIES_TYPE_SF:
				output += ' <b>[SF]</b> '
		elif title[TITLE_TTYPE] == 'ESSAY':
			if series_type != SERIES_TYPE_ESSAY:
				output += ' <b>[ES]</b> '
		elif title[TITLE_TTYPE] == 'EDITOR':
			if series_type != SERIES_TYPE_EDIT:
				output += ' <b>[ED]</b> '
		elif title[TITLE_TTYPE] == 'NONFICTION':
			if series_type != SERIES_TYPE_NONFIC:
				output += ' <b>[NF]</b> '
		elif title[TITLE_TTYPE] == 'POEM':
			if series_type != SERIES_TYPE_POEM:
				output += ' <b>[POEM]</b> '
		elif title[TITLE_TTYPE] == 'COVERART':
			if series_type != SERIES_TYPE_COVERART:
				output += ' <b>[COVERART]</b> '
		elif title[TITLE_TTYPE] == 'INTERIORART':
			if series_type != SERIES_TYPE_INTERIORART:
				output += ' <b>[INTERIORART]</b> '
		elif title[TITLE_TTYPE] == 'REVIEW':
			if series_type != SERIES_TYPE_REVIEW:
				output += ' <b>[REVIEW]</b> '
		elif title[TITLE_TTYPE] == 'INTERVIEW':
			if series_type != SERIES_TYPE_INTERVIEW:
				output += ' <b>[INTERVIEW]</b> '
		else:
			# These have no tag and no series and should probably never appear
			# in a series' contents.  But we use their type as a tag so we can
			# see what happened
			output = output + ' <b>[' + title[TITLE_TTYPE] + ']</b> '
	# If this is a non-genre title and we are displaying genre titles, then this means
	# either (a) that this non-genre title is part of a genre series or (b) that we
	# are displaying a series bibliography. Show "[non-genre]" on the page.
	if not nongenre and title[TITLE_NON_GENRE] == 'Yes':
                output += ' <b>[non-genre]</b>'
        # If this is a graphic title, display the graphic designation
	if title[TITLE_GRAPHIC] == 'Yes':
                output += ' <b>[graphic format]</b>'
	print output

        # Display review authors
        if title[TITLE_TTYPE] == 'REVIEW':
                displayAuthorsforReview(authors.get(title[TITLE_PUBID], []), title, author_id, translit_authors)
        # Display interview authors
        elif title[TITLE_TTYPE] == 'INTERVIEW':
                displayAuthorsforInterview(authors.get(title[TITLE_PUBID], []), title, author_id, translit_authors)
	# Display all authors (for series pages) or just co-authors (for author pages)
	elif title[TITLE_PUBID] in authors:
                displayAuthors(authors[title[TITLE_PUBID]], author_id, translit_authors)

def buildCoreTitleLine(title, original_language, translit_titles):
	output = ' %s ' % ISFDBLink('title.cgi',
                                    int(title[TITLE_PUBID]),
                                    title[TITLE_TITLE],
                                    False, 'class = "italic"',
                                    translit_titles)

	# Only display the current language if it is defined, the original (i.e. author's or, for
	# serializations, parent title's) language is defined and not the same as the current language
	if title[TITLE_LANGUAGE] and original_language and (title[TITLE_LANGUAGE] != original_language):
                output += '[%s] ' % LANGUAGES[title[TITLE_LANGUAGE]]

        # Build the year string, which is somewhat different from other pages' year/date strings
        year = title[TITLE_YEAR][:4]
	# Convert special years to strings.  Anything unconverted and in
	# the future is given an alternate-format label.
	cnvyear = convertTitleYear(title)
	if cnvyear == year and title[TITLE_YEAR] > ISFDBDate():
		output += '[<b>forthcoming: %s</b>]' % ISFDBconvertForthcoming(title[TITLE_YEAR])
	else:
		output += '(<b>%s</b>)' % cnvyear
	return output

def displayVariants(title, parent_authors, variants, serials, variant_authors, author_id,
                    parents_with_pubs, translit_titles, translit_authors):
        variant_list = variants.get(title[TITLE_PUBID], ())
        serial_list = serials.get(title[TITLE_PUBID], ())
	if not variant_list and not serial_list:
		return

	###################################################
	# STEP 1: Determine whether to display the variant
	#         info on the same line as the parent title
	###################################################
	titleVariation = 1
	# Display VT info on the same line as the parent if there is only one VT 
	# AND its title AND its title type match those of the parent title
	if (len(variant_list) == 1
            and variant_list[0][TITLE_TITLE] == title[TITLE_TITLE]
            and variant_list[0][TITLE_TTYPE] == title[TITLE_TTYPE]):
                # Only shorten the display to one line if the language of the variant
                # is the same or one of the languages is not defined
                if ((variant_list[0][TITLE_LANGUAGE] == title[TITLE_LANGUAGE])
                    or (title[TITLE_LANGUAGE] == None)
                    or (variant_list[0][TITLE_LANGUAGE] == None)):
                        titleVariation = 0

        if title[TITLE_PUBID] in parents_with_pubs:
                parentHasPubs = 1
        else:
                parentHasPubs = 0

	######################################################
	# STEP 2a: If either (a) the parent and variant titles
	#          differ or (b) multiple variants, then display
	#          variant information as an HTML list
	######################################################
	if titleVariation:
		if parentHasPubs:
			print " also appeared as:"
		else:
			print " only appeared as:"
		firstvariant = 1
		for variant in variant_list:
                        if firstvariant:
                                firstvariant = 0
                                print "<ul>"
                        print "<li>"
                        displayVariantTitle(variant, title, 'variant',
                                            parent_authors, author_id,
                                            variant_authors, translit_titles,
                                            translit_authors)
		if firstvariant == 0:
			print "</ul>"
	###############################################################
	# STEP 2b: If there is only 1 variant and its title, title type
	# and language are the same as the parent title's, then display
	# the variant's authors on the same line as the parent
	###############################################################
	elif variant_list:
                qualifier = ""
                if parentHasPubs:
                        qualifier = "also "
                else:
                        qualifier = "only "
                variantAuthors = variant_authors.get(variant_list[0][TITLE_PUBID], [])
                displayVariantAuthors(variantAuthors, qualifier, translit_authors)

	######################################################
	# STEP 3: Display serializations
	######################################################
	if serial_list:
                print '<ul>'
                print '<li><b>Serializations:</b>'
                for serial in serial_list:
                        print "<li>"
                        displayVariantTitle(serial, title, 'serial',
                                            parent_authors, author_id,
                                            variant_authors, translit_titles, translit_authors)
                print '</ul>'

def displayVariantTitle(title, origTitle, variant_type, parent_authors,
                        author_id, variant_authors, translit_titles, translit_authors):
        # Determine if this variant is a translation
        translation = 0
        if title[TITLE_LANGUAGE] and origTitle[TITLE_LANGUAGE] and title[TITLE_LANGUAGE] != origTitle[TITLE_LANGUAGE]:
                translation = 1
        if translation:
                label = 'Translation'
        elif variant_type == 'serial':
                label = ''
        else:
                label = 'Variant'
                # If this is an interior art title and its parent is a cover art title,
                # then the label will be "Interior Art"
                if (title[TITLE_TTYPE] == 'INTERIORART') and (origTitle[TITLE_TTYPE] == 'COVERART'):
                        label = 'Interior Art'
                # If this is a cover art title and its parent is an interior art title,
                # then the label will be "Cover Art"
                elif (origTitle[TITLE_TTYPE] == 'INTERIORART') and (title[TITLE_TTYPE] == 'COVERART'):
                        label = 'Cover Art'
        if label:
                label = ' <b>%s:</b>' % label

	output = '%s %s ' % (label, ISFDBLink('title.cgi', int(title[TITLE_PUBID]),
                                              title[TITLE_TITLE], False, 'class="italic"', translit_titles))

	if translation:
                output += '[%s] ' % LANGUAGES[title[TITLE_LANGUAGE]]
        
	try:
		year = title[TITLE_YEAR][:4]
	except:
		year = '0000'

	# Convert special years to strings.  Anything unconverted and in
	# the future is given an alternate-format label.
	cnvyear = convertTitleYear(title)
	if cnvyear == year and title[TITLE_YEAR] > ISFDBDate():
		output += '[<b>forthcoming: %s</b>]' % ISFDBconvertForthcoming(title[TITLE_YEAR])
	else:
		output += '(<b>%s</b>)' % cnvyear

        # Show the omnibus content indicator
	if title[TITLE_TTYPE] == 'OMNIBUS':
		if title[TITLE_CONTENT]:
			output += ' <b>[O/%s]</b> ' % title[TITLE_CONTENT]
		else:
			output += ' <b>[O]</b> '
	print output

	canonical_authors = parent_authors.get(origTitle[TITLE_PUBID], [])
	canonical_author_ids = []
	for canonical_author in canonical_authors:
                canonical_author_ids.append(canonical_author[0])
        # If there is an author ID was passed in and the list of parent author IDs
        # does not include it, then the latter is a list of collaborators only
        # and we need to add the main author ID to the list
	if author_id and author_id not in canonical_author_ids:
                canonical_author_ids.append(author_id)

	variantAuthors = variant_authors.get(title[TITLE_PUBID], [])
	variant_author_ids = []
	for variant_author_tuple in variantAuthors:
                variant_author_ids.append(variant_author_tuple[0])
        # Only display the "as by" portion if the authors are different;
        # the order in which they appear doesn't matter for the purposes
        # of determining whether they are different
        if set(canonical_author_ids) != set(variant_author_ids):
		displayVariantAuthors(variantAuthors, "", translit_authors)

def displayAuthors(authors, author_id, translit_authors):
	if not authors:
		return
	if not author_id:
                print " <b>by</b>"
        else:
        	print " <b>with</b> "
	counter = 0
	for author in authors:
		if counter:
			print " <b>and</b> "
		displayAuthorById(author[0], author[1], translit_authors)
		counter += 1

def displayAuthorsforReview(reviewer_authors, title, author_id, translit_authors):
        reviewed_authors = SQLReviewedAuthors(title[TITLE_PUBID])
	print " <b>by</b> "
        counter = 0
        for author in reviewed_authors:
                if counter:
                        print " <b>and</b> "
                displayAuthorById(author[0], author[1])
                counter += 1
	
	if not reviewer_authors:
                return
        
        counter = 0
        output = ''
        for author in reviewer_authors:
                if not counter:
                        # Author biblio pages display only co-reviewers
                        if author_id:
                                output += "(co-reviewed with "
                        # Series pages display all reviewers
                        else:
                                output += "(reviewed by "
                else:
                        output += " <b>and</b> "
                output += buildAuthorById(author[0], author[1], translit_authors)
                counter += 1
        if counter:
                output += ")"
        print output

def displayAuthorsforInterview(interviewer_authors, title, author_id, translit_authors):
        interviewee_authors = SQLIntervieweeAuthors(title[TITLE_PUBID])
	print " <b>with</b> "
	counter = 0
	for author in interviewee_authors:
		if counter:
			print " <b>and</b> "
		displayAuthorById(author[0], author[1])
		counter += 1

	if not interviewer_authors:
                return

        counter = 0
        output = ''
        for author in interviewer_authors:
                if not counter:
                        # Author biblio pages display only co-interviewers
                        if author_id:
                                if len(interviewer_authors) == 1:
                                        output += '(co-interviewer '
                                else:
                                        output += '(co-interviewers '
                        # Series pages display all interviewers
                        else:
                                output += '(interviewed by '
                else:
                        output += " <b>and</b> "
                output += buildAuthorById(author[0], author[1], translit_authors)
                counter += 1
        if counter:
                output += ")"	
        print output

def displayVariantAuthors(authors, qualifier, translit_authors):
	if len(authors) == 0:
		return

	if not qualifier:
		qualifier = ""

	output = " [<b>%sas by</b> " % (qualifier)
	counter = 0
	for author in authors:
		if counter:
			output += " <b>and</b> "
                output += ISFDBLink('ea.cgi', author[0], author[1], False, '', translit_authors)
		counter += 1
	output += "]"
	print output

def buildVariants(canonical_titles, variants, user):
	variant_dict = {}
	serial_dict = {}
	parents = {}
	# Build a dictionary of parent titles indexed by title ID
	for title in canonical_titles:
                title_id = title[TITLE_PUBID]
                parents[title_id] = title
        
        for variant in variants:
                parent_id = variant[TITLE_PARENT]
                if parent_id not in parents:
                        continue
                parent = parents[parent_id]
                lang_filter = 0
                # Always display VTs with no language code
                if variant[TITLE_LANGUAGE] == None:
                        lang_filter = 1
                # Always display VTs with the same language as the language of the parent title
                elif variant[TITLE_LANGUAGE] == parent[TITLE_LANGUAGE]:
                        lang_filter = 1
                # Display all translations if the user chose "All" in User Preferences or cookies
                elif user.display_all_languages == 'All':
                        lang_filter = 1
                # Display VT if the language of the translation is in the user's list of requested languages
                elif (user.display_all_languages == 'Selected') and (variant[TITLE_LANGUAGE] in user.languages):
                        lang_filter = 1
		if lang_filter:
			if variant[TITLE_TTYPE] == 'SERIAL':
                                if parent_id not in serial_dict:
                                        serial_dict[parent_id] = []
				serial_dict[parent_id].append(variant)
			else:
                                if parent_id not in variant_dict:
                                        variant_dict[parent_id] = []
				variant_dict[parent_id].append(variant)

        return (variant_dict, serial_dict)

def buildVTAuthors(variant_titles, variant_serials):
        vt_author_list = []
        for parent_id in variant_titles:
                variants = variant_titles[parent_id]
                for variant in variants:
                        vt_id = str(variant[TITLE_PUBID])
                        vt_author_list.append(vt_id)
        for parent_id in variant_serials:
                serials = variant_serials[parent_id]
                for serial in serials:
                        vt_id = str(serial[TITLE_PUBID])
                        vt_author_list.append(vt_id)
        title_string = ", ".join(vt_author_list)
        if not title_string:
                return {}
        return SQLTitleListBriefAuthorRecords(title_string)

def builtTranslitTitles(canonical_titles, variant_titles, variant_serials, interviews = []):
        title_ids = []
        for title_list in (canonical_titles, interviews):
                for title in title_list:
                        title_id = title[TITLE_PUBID]
                        if title_id not in title_ids:
                                title_ids.append(title_id)

        for title_dict in (variant_titles, variant_serials):
                for parent_id in title_dict:
                        variants = title_dict[parent_id]
                        for variant in variants:
                                variant_id = variant[TITLE_PUBID]
                                if variant_id not in title_ids:
                                        title_ids.append(variant_id)
        return SQLLoadTransTitlesList(title_ids)

def builtTranslitAuthors(parent_authors, variant_authors):
        author_ids = []
        for author_dict in (parent_authors, variant_authors):
                for title_id in author_dict:
                        authors = author_dict[title_id]
                        for author in authors:
                                author_id = author[0]
                                author_ids.append(author_id)
        return SQLLoadTransAuthorNamesList(author_ids)

##################################################
#
#	Function appears in three different locations
#	See /mod/isfdblib.py for Moderator PrintUserInfo function
#	see /edit/isfdblib.py for Edit PrintUserInfo function
#       "executable" is the name of the CGI script to call
#       "argument" is the argument to pass to the CGI script
#
##################################################
def PrintUserInfo(executable, argument):
	(userid, username, usertoken) = GetUserData()
	if username:
                PrintLoggedIn(userid, username)
	else:
                PrintNotLoggedIn(executable,argument)
	return userid

def PrintHeader(title):
        PrintHTMLHeaders(title)

        print '<script type="text/javascript" src="%s://%s/isfdb_main.js"></script>' % (PROTOCOL, HTMLLOC)
        # Advanced Search pages only:
        if title.startswith('Advanced'):
                # Import functions to change drop-down values dynamically
                print '<script type="text/javascript" src="%s://%s/adv_search.js"></script>' % (PROTOCOL, HTMLLOC)

	# GOOGLE Analytics - will need to be rewritten to work with CSP before it can be activated
	if DO_ANALYTICS:
		print '<script src="https://www.google-analytics.com/urchin.js" type="text/javascript">'
		print '</script>'
		print '<script type="text/javascript">'
		print '_uacct = "UA-253096-1";'
		print 'urchinTracker();'
		print '</script>'

	(userid, username, usertoken) = GetUserData()
	if not userid:
                print '<h3>You are not logged in. If you'
                print ' <a href="%s://%s/index.php?title=Special:Userlogin&amp;type=signup">' % (PROTOCOL, WIKILOC)
                print '<span class="newuser">create a free account</span></a>'
                print ' and sign in, you will be able to customize what is displayed.</h3>'
        elif SQLhasNewTalk(userid):
                print '<div class="newtalk"><h3>There are new messages on your Talk page. Please follow '
                print '<a href="%s://%s/index.php/User_talk:%s">this link</a> and respond.</h3></div>' % (PROTOCOL, WIKILOC, username)
	print '</div>'

########################################################################
#	"page_type" defines the type of page the Navbar will be displayed on
#	"arg1" is the record to be displayed. Note that it contains
#              different types of data for different pages. For example,
#              for publication pages it contains the full publication
#              publication record as retrieved from the database. For
#              title records, it contains the title type. For series
#              and some other records, it contains the record ID.
#	"arg2" is the record number for pages where arg1 is NOT the record
#              number -- see "arg1" for details.
#	"executable" is the name of the CGI script to call
#	"argument" is the argument to be passed to the CGI script
#       "search_value" is the search value previously entered by the user.
#              It will be re-displayed in the search box if specified.
#              It is only specified when called from the search results page.
#       "search_type" is the search type previously selected by the user.
#              It will be re-displayed in the search box if specified.
#              It is only specified when called from the search results page.
#
#	Edit NavBar function.
#	See /mod/isfdblib.py for Moderator NavBar function
#	see /edit/isfdblib.py for Edit NavBar function
########################################################################
def PrintNavbar(page_type, arg1, arg2, executable, argument, search_value = '', search_type = ''):
	print '<div id="nav">'

	# Display the search box
	PrintSearchBox(page_type, search_value, search_type)
	
	userid = PrintUserInfo(executable, argument)

        # Print nav bar items common to all pages
        PrintOtherPages(page_type)

	#############################################################
	# SPECIFIC - navbar items specific to this page
	#############################################################
	if page_type == 'publication':
		# Display links to other sites using an embedded ISBN, but only for properly formatted ISBN values.
		if arg1[PUB_ISBN] and ISBNValidFormat(arg1[PUB_ISBN]):
			#Retrieve the Web sites for this user
			websites = SQLLoadWebSites(arg1[PUB_ISBN], userid, arg1[PUB_PTYPE])
			if websites:
                                PrintThirdPartyLinks(websites, 'Amazon')
                                PrintThirdPartyLinks(websites, 'Other')
                #For Project Gutenberg pubs, display a link to the PG site
                elif arg1[PUB_PUBLISHER]:
                        publisher = SQLGetPublisher(arg1[PUB_PUBLISHER])
                        if publisher[PUBLISHER_NAME] == 'Project Gutenberg' and arg1[PUB_CATALOG]:
                                print '<div class="divider">'
                                print 'Other Links:'
                                print '</div>'
                                print '<ul class="navbar">'
                                print '<li><a href="https://www.gutenberg.org/ebooks/%s" target="_blank">Project Gutenberg</a>' % arg1[PUB_CATALOG]
                                print '</ul>'

	PrintEditTools(page_type, userid, arg1, arg2)

        PrintNewPubs(userid)

	if page_type == 'frontpage':
		print '<div class="divider">'
		print 'Tools Used to Create This Site:'
		print '</div>'
		print '<ul class="navbar">'
		print '<li><a href="https://www.fabforce.net/dbdesigner4/">DBDesigner 4</a>'
		print '<li><a href="https://www.mysql.com">MySQL</a>'
		print '<li><a href="https://www.python.org">Python</a>'
		print '<li><a href="https://wiki.mozilla.org/Venkman">Venkman</a>'
		print '<li><a href="https://www.vim.org">Vim</a>'
		print '</ul>'

	print '<div class="divider">'
	print 'Policies:'
	print '</div>'
	print '<ul class="navbar">'
	print '<li><a href="%s://%s/index.php/ISFDB:General_disclaimer">Disclaimer</a>' % (PROTOCOL, WIKILOC)
	print '<li><a href="%s://%s/index.php/ISFDB:Privacy_policy">Privacy Policy</a>' % (PROTOCOL, WIKILOC)
	print '<li><a href="%s://%s/index.php/Banner_Art_Credits">Banner Art Credits</a>' % (PROTOCOL, WIKILOC)
	print '</ul>'

	print '<div class="divider">'
	print 'License:'
	print '</div>'
	print '<div id="cclicense">'
	print '<a rel="license" href="https://creativecommons.org/licenses/by/4.0/">'
	print '<img alt="Creative Commons License" src="https://i.creativecommons.org/l/by/4.0/88x31.png"></a><br>'
	print 'This work is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.'
	print '</div>'

        # nav div
	print '</div>'
	if page_type == 'login':
		print '<div id="main2">'
	elif page_type in ('author', 'publication', 'title', 'publisher', 'pub_series', 'series', 'seriestags', 'seriesgrid'):
		print '<div id="content">'
	else:
		print '<div id="main">'
	dbStatus = SQLgetDatabaseStatus()
	if dbStatus == 0:
		print "<h3>The ISFDB database is currently offline. Please check back in a few minutes.</h3>"
		PrintTrailer('frontpage', 0, 0)
		sys.exit(0)

	onlineVersion = SQLgetSchemaVersion()
	if onlineVersion != SCHEMA_VER:
		print "<h3>Warning: database schema mismatch (%s vs %s)</h3>" % (onlineVersion, SCHEMA_VER)

def PrintThirdPartyLinks(websites, type_of_sites):
        displayed_sites = []
        for website in websites:
                if type_of_sites == 'Amazon' and 'www.amazon.' in website[1]:
                        displayed_sites.append(website)
                if type_of_sites != 'Amazon' and 'www.amazon.' not in website[1]:
                        displayed_sites.append(website)
        if not displayed_sites:
                return
        print '<div class="divider">'
        print '%s Links <i class="downarrow"></i>' % type_of_sites
        print '<div id="div%ssites" class="divothersites">' % type_of_sites
        print '<ul class="listothersites">'
        for website in displayed_sites:
                displayed_site_name = ISFDBText(website[0])
                suffix=''
                if type_of_sites == 'Amazon':
                        displayed_site_name = displayed_site_name.replace('Amazon ','')
                        if displayed_site_name in ('US','UK'):
                                suffix = ' (commissions earned)'
                print '<li><a href="%s" target="_blank">%s</a>%s' % (website[1], displayed_site_name, suffix)
        print '</ul>'
        print '</div>'
        print '</div>'

def AuthorSearchLink(author_name):
        return AdvSearchLink((('TYPE', 'Title'),
                             ('USE_1', 'author_canonical'),
                             ('O_1', 'exact'),
                             ('TERM_1', author_name),
                             ('ORDERBY', 'title_title'),
                             ('C', 'AND')))

def PrintEditTools(page_type, userid, arg1, arg2):
	#############################################################
	# EDITING - navbar items relevant to editing this page
	#############################################################
	moderator = SQLisUserModerator(userid)
	output = []
	if moderator:
                output.append(ISFDBLink('mod/list.cgi', 'N', 'Moderator'))
	if (page_type == 'author') and (int(arg2) > 0):
		output.append(ISFDBLink('edit/editauth.cgi', arg2, 'Edit Author Data'))
		output.append(ISFDBLink('edit/mkpseudo.cgi', arg2, 'Make/Remove Alternate Name'))
                output.append('%s%s</a>' % (AuthorSearchLink(arg1), 'Show All Titles'))
		output.append(ISFDBLink('edit/find_dups.cgi', arg2, 'Check for Duplicate Titles'))
	elif page_type == 'title':
		output.append(ISFDBLink('edit/edittitle.cgi', arg2, 'Edit Title Data'))
		output.append(ISFDBLink('diffselect.cgi', arg2, 'Compare Publications'))
		output.append(ISFDBLink('edit/deletetitle.cgi', arg2, 'Delete This Title'))
		output.append(ISFDBLink('edit/mkvariant.cgi', arg2, 'Make This Title a Variant'))
		if arg1 in ('NOVEL', 'COLLECTION', 'OMNIBUS', 'ANTHOLOGY', 'CHAPBOOK', 'NONFICTION'):
                        output.append(ISFDBLink('edit/addpub.cgi', arg2, 'Add Publication to This Title'))
		if (arg1 != 'REVIEW') and (arg1 != 'INTERVIEW'):
                        output.append(ISFDBLink('edit/addvariant.cgi', arg2, 'Add a Variant to This Title'))
		if arg1 == 'REVIEW':
			output.append(ISFDBLink('edit/linkreview.cgi', arg2, 'Link Review to Title'))
                output.append(ISFDBLink('edit/select_award_type.cgi', arg2, 'Add an Award to This Title'))
		output.append(ISFDBLink('edit/tv_unmerge.cgi', arg2, 'Unmerge Titles'))
		output.append(ISFDBLink('edit/find_title_dups.cgi', arg2, 'Check for Duplicate Titles'))
	elif page_type == 'series':
		output.append(ISFDBLink('edit/editseries.cgi', arg1, 'Edit Series'))
		output.append(ISFDBLink('edit/deleteseries.cgi', arg1, 'Delete Series'))
	elif page_type == 'award':
                output.append(ISFDBLink('edit/addaward.cgi', '0+%s' % arg2, 'Add Untitled Award of This Type'))
                if arg1:
                        output.append(ISFDBLink('edit/editaward.cgi', arg1, 'Edit Award'))
                        output.append(ISFDBLink('edit/linkaward.cgi', arg1, 'Link Award'))
                        output.append(ISFDBLink('edit/deleteaward.cgi', arg1, 'Delete Award'))
	elif page_type == 'award_type':
                output.append(ISFDBLink('edit/addaward.cgi', '0+%s' % arg1, 'Add Untitled Award of This Type'))
		# Award Types can only be edited by moderators at this time
		if moderator:
                        output.append(ISFDBLink('edit/addawardcat.cgi', arg1, 'Add New Award Category to This Award Type'))
			output.append(ISFDBLink('edit/deleteawardtype.cgi', arg1, 'Delete This Award Type'))
			output.append(ISFDBLink('edit/editawardtype.cgi', arg1, 'Edit This Award Type'))
	elif page_type == 'award_cat':
                output.append(ISFDBLink('edit/editawardcat.cgi', arg1, 'Edit This Award Category'))
		# Award Types can only be deleted by moderators at this time
		if moderator:
			output.append(ISFDBLink('edit/deleteawardcat.cgi', arg1, 'Delete This Award Category'))
	elif page_type == 'publication':
		output.append(ISFDBLink('edit/find_pub_dups.cgi', arg1[PUB_PUBID], 'Check for Duplicate Titles'))
		output.append(ISFDBLink('edit/editpub.cgi', arg1[PUB_PUBID], 'Edit This Pub'))
		output.append(ISFDBLink('edit/clone_intermediate.cgi', arg1[PUB_PUBID], 'Clone This Pub'))
		output.append(ISFDBLink('edit/exportcontent.cgi', arg1[PUB_PUBID], 'Export Content'))
		output.append(ISFDBLink('edit/importcontent.cgi', arg1[PUB_PUBID], 'Import Content'))
		output.append(ISFDBLink('edit/rmtitles.cgi', arg1[PUB_PUBID], 'Remove Titles From This Pub'))
		output.append(ISFDBLink('edit/deletepub.cgi', arg1[PUB_PUBID], 'Delete This Pub'))
		output.append(ISFDBLink('edit/verify.cgi', arg1[PUB_PUBID], 'Verify This Pub'))
	elif page_type == 'publisher':
                output.append(ISFDBLink('edit/editpublisher.cgi', arg2, 'Edit This Publisher'))
	elif page_type == 'pub_series':
                output.append(ISFDBLink('edit/editpubseries.cgi', arg2, 'Edit This Publication Series'))
	if output:
                print '<div class="divider">'
                print 'Editing Tools:'
                print '</div>'
                print '<ul class="navbar">'
                for line in output:
                        print '<li>%s' % line
                print '</ul>'

def PrintTrailer(page_type, arg1, arg2):
	print '</div>'
	print '<div id="bottom">'
	print COPYRIGHT
	print '<br>'
	print ENGINE
	if page_type == 'publication':
                print '<br>'
                print 'ISFDB is an Amazon Associate in order to have access to Amazon\'s product data. As an Amazon Associate ISFDB earns from qualifying purchases.'
	print '</div>'
	print '</div>'
	print '</body>'
	print '</html>'

def escape_spaces(input):
        return string.replace(input, ' ', '%20')

def escapeLink2(input):
        retval = string.replace(input, '\\', '')
        retval = string.replace(retval, ' ', '%20')
        retval = string.replace(retval, '&rsquo;', "'")
	return retval

def escapeLink(input):
	retval = string.replace(input, ' ', '_')
	retval = string.replace(retval, "'", '&rsquo;')
	retval = string.replace(retval, '"', '&quot;')
	return retval

def displayAuthorList(authors):
        displayRecordList('author', authors)

def displayRecordList(record_type, records):
        print LIBbuildRecordList(record_type, records)

def displayAuthorById(id, name, trans_authors = None):
	print buildAuthorById(id, name, trans_authors = None)

def buildAuthorById(id, name, trans_authors = None):
	return ISFDBLink('ea.cgi', id, name, False, '', trans_authors)

def PrintAllAuthors(title_id, prefix = '', suffix = ''):
        print ISFDBFormatAllAuthors(title_id, prefix, suffix)

def PrintWebPages(webpages, format = '<li>'):
        if not webpages:
                return
        printed = {}
	for webpage in webpages:
                # Get the corrected link and the displayed form of this URL
                (corrected_webpage, display, home_page, linked_page) = BuildDisplayedURL(webpage)
                # Add this URL to the list of sites for this domain
                if display not in printed:
                        printed[display] = []
                printed[display].append(corrected_webpage)
        total = 0
        # Sort all domain names, recognized as well as unrecognized, in a case-insensitive way
        for display in sorted(printed.keys(), key=lambda x: x.lower()):
                count = 1
                # Retrieve Web page urls for this domain name
                for webpage in printed[display]:
                        if not total:
                                output = "%s<b>Webpages:</b> " % format
                                total = 1
                        else:
                                output += ", "
                        # If there is more than one URL with this domain for this author, show its relative number
                        qualifier = ''
                        if len(printed[display]) > 1:
                                qualifier = "-%d" % (count)
                        output += '<a href="%s" target="_blank">%s%s</a>' % (webpage, display, qualifier)
                        count += 1
	print output

def BuildDisplayedURL(webpage):
        linked_page = ''
        webpage = ISFDBHostCorrection(webpage)
        if '|' in webpage:
                linked_page = webpage.split('|')[1]
                webpage = webpage.split('|')[0]
        from urlparse import urlparse
        parsed_url = urlparse(webpage)
        # Extract the "domain:port" part of the URL
        netloc = parsed_url[1].lower()
        # Drop the port number, if any
        domain = netloc.split(':')[0]
        # If the URL doesn't follow the standard URI rules, display the raw URL
        if not domain:
                domain = webpage
        # If there is no recognized "scheme" (http, ftp, etc), pad the webpage URL
        # with 'https'. This will ensure that the link goes to a third party site and
        # not to a location on the local server, which could cause a security issue.
        if not parsed_url[0]:
                webpage = "https://%s" % webpage
        domains = SQLLoadRecognizedDomains()
        display = ''
        # Extract the last 4, then 3, then 2 period-delimited parts of the domain name and evaluate them
        for index in (4, 3, 2):
                part = ".".join(domain.split('.')[-index:])
                credit_data = ''
                for domain_tuple in domains:
                        if part != domain_tuple[DOMAIN_NAME]:
                                continue
                        # If an optional "required url segment" is defined for this domain, check its presence in the URL
                        required_url_segment = domain_tuple[DOMAIN_REQUIRED_SEGMENT]
                        if required_url_segment and required_url_segment not in parsed_url[2]:
                                continue
                        credit_data = domain_tuple
                        break
                if not credit_data:
                        continue
                recognized_domain = credit_data[DOMAIN_NAME]
                display = credit_data[DOMAIN_SITE_NAME]
                home_page = credit_data[DOMAIN_SITE_URL]
                if part == 'wikipedia.org':
                        # For Wikipedia, display the language
                        language = domain.split('.')[0]
                        display += '-%s' % language.upper()
                # If the image is hosted by ISFDB, also link to the Wiki-based image description page
                if display == 'ISFDB':
                        linked_page = "%s://%s/index.php/Image:%s" % (PROTOCOL, WIKILOC, parsed_url[2].rpartition('/')[-1])
                break
        # If this is not a "recognized" Web site, then display the raw domain name
        if not display:
                display = domain
                home_page = domain
                # If the first four letters are 'www.', strip them
                if display[:4] == 'www.':
                        display = display[4:]
        return (webpage, display, home_page, linked_page)
        
def PrintAwardResults(results, limit):
	print '<table class="generic_table">'
	print '<tr align="left" class="generic_table_header">'
	print '<th>Short Award Name</th>'
	print '<th>Full Award Name</th>'
	print '<th>Awarded For</th>'
	print '<th>Awarded By</th>'
	print '<th>Poll</th>'
	print '<th>Non-Genre</th>'
 	print '</tr>'

        bgcolor = 1
        counter = 0
        for award in results:
                PrintAwardRecord(award, bgcolor)
                bgcolor ^= 1
                counter += 1
                if counter > limit:
                        break
        print '</table>'

def PrintAwardRecord(award, bgcolor):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%s</td>' % ISFDBLink('awardtype.cgi', award[AWARD_TYPE_ID], award[AWARD_TYPE_SHORT_NAME])
        print '<td>%s</td>' % award[AWARD_TYPE_NAME]
        award_for = award[AWARD_TYPE_FOR]
        if award_for is None:
                award_for = '-'
        print '<td>%s</td>' % award_for
        award_by = award[AWARD_TYPE_BY]
        if award_by is None:
                award_by = '-'
        print '<td>%s</td>' % award_by
        print '<td>%s</td>' % award[AWARD_TYPE_POLL]
        print '<td>%s</td>' % award[AWARD_TYPE_NONGENRE]
        print '</tr>'

def PrintAwardCatResults(results, limit):
	print '<table class="generic_table">'
	print '<tr align="left" class="generic_table_header">'
	print '<th>Award Category Name</th>'
	print '<th>Parent Award Type</th>'
	print '<th>Award Category Order</th>'
 	print '</tr>'

        bgcolor = 1
        counter = 0
        for award in results:
                PrintAwardCatRecord(award, bgcolor)
                bgcolor ^= 1
                counter += 1
                if counter > limit:
                        break
        print '</table>'

def PrintAwardCatRecord(award_cat, bgcolor):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%s</td>' % ISFDBLink('award_category.cgi', award_cat[AWARD_CAT_ID], award_cat[AWARD_CAT_NAME])
        award_type_id = award_cat[AWARD_CAT_TYPE_ID]
        award_type = SQLGetAwardTypeById(award_type_id)
        print '<td>%s</td>' % ISFDBLink('awardtype.cgi', award_type[AWARD_TYPE_ID], award_type[AWARD_TYPE_SHORT_NAME])
        if award_cat[AWARD_CAT_ORDER]:
                print '<td>%s</td>' % award_cat[AWARD_CAT_ORDER]
        else:
                print '<td>&nbsp;</td>'
        print '</tr>'

def CoverInfo(link, preview=False, direct=False):
        (finallink, credit, home_page, linked_page) = BuildDisplayedURL(link)
        if credit == 'ISFDB':
                site_name = 'ISFDB'
                if not direct:
                        finallink = home_page
        elif 'Amazon' in credit:
                site_name = 'Amazon'
        else:
                site_name = 'other'
        if preview:
                return '<a href="%s"><img src="%s" class="coversmall" alt="Cover"></a>' % (finallink, link)
        elif credit == "ISFDB":
                return '<a class="coverisfdb" href="%s">%s</a>' % (finallink, site_name)
        else:
                return '<a class="coverexists" href="%s">%s</a>' % (finallink, site_name)

def PrintPubsTable(pubs, display_type, user = None, limit = 100000):
        # Supported values of display_type are:
        # 'publisher', 'title', 'diffselect', 'pubseries', 'isbn_search', 'adv_search'
	if not pubs:
                return
        if not user:
                user = User()
                user.load()
        print '<table class="publications">'
        print '<tr class="table2">'

        if display_type == 'diffselect':
                print '<th class="publication_checkbox">&nbsp;</th>'
                print '<th class="publication_title_short">Title</th>'
        elif display_type == 'pubseries':
                print '<th class="publication_date">Date</th>'
                print '<th class="publication_series_number">Pub. Series #</th>'
                print '<th class="publication_title">Title</th>'
        else:
                print '<th class="publication_title">Title</th>'

        if display_type != 'pubseries':
                print '<th class="publication_date">Date</th>'
        print '<th class="publication_author_editor">Author/Editor</th>'

        if display_type == 'publisher':
                print '<th class="publication_publisher">Publication series</th>'
        elif display_type == 'pubseries':
                print '<th class="publication_publisher">Publisher</th>'
        else:
                print '<th class="publication_publisher">Publisher/Pub. Series</th>'

        print '<th class="publication_isbn_catalog">ISBN/Catalog ID</th>'
        print '<th class="publication_price">Price</th>'
        print '<th class="publication_pages">Pages</th>'
        print '<th class="publication_format">Format</th>'
        print '<th class="publication_type">Type</th>'
        print '<th class="publication_cover_artist">Cover Artist</th>'
        print '<th class="publication_verif">Verif</th>'
        if user.cover_links_display:
                print '<th class="publication_cover">Cover</th>'
        print '</tr>'

        # Build lists of pub IDs, publisher IDs and pub series IDs to be used in SQL statements
        pub_list = []
        publisher_list = []
        pub_series_list = []
        for pub in pubs:
                pub_list.append(str(pub[PUB_PUBID]))
                if pub[PUB_PUBLISHER] and str(pub[PUB_PUBLISHER]) not in publisher_list:
                        publisher_list.append(str(pub[PUB_PUBLISHER]))
                if pub[PUB_SERIES] and str(pub[PUB_SERIES]) not in pub_series_list:
                        pub_series_list.append(str(pub[PUB_SERIES]))

        pub_authors = SQLPubListBriefAuthorRecords(pub_list)
        pub_publishers = SQLGetPublisherList(publisher_list)
        pub_series = SQLGetPubSeriesList(pub_series_list)
        cover_artists = SQLGetCoverAuthorsForPubs(pub_list)
        
        bgcolor = 1
        index = 1
        for pub in pubs:
                PrintOnePub(pub, pub_authors, pub_publishers, pub_series, cover_artists, bgcolor, display_type, user, index)
                bgcolor ^= 1
                index += 1
                if index > limit:
                        break
        print '</table>'
        return

def PrintOnePub(pub, pub_authors, pub_publishers, pub_series, cover_artists, bgcolor, display_type, user, index):
        from isbn import convertISBN
        print '<tr class="table%d">' % bgcolor

        # Display the checkbox column for "Diff Select" only
        if display_type == 'diffselect':
                print '<td><input type="checkbox" value="%d" name="pub%d"></td>' % (pub[PUB_PUBID], index)

        # For publication series, display the Date and Pub. Series Number columns first
        elif display_type == 'pubseries':
                print '<td>%s</td>' % ISFDBconvertDate(pub[PUB_YEAR], 1)
                pub_series_number = '&nbsp;'
                if pub[PUB_SERIES_NUM]:
                        pub_series_number = ISFDBText(pub[PUB_SERIES_NUM])
                print '<td dir="ltr">%s</td>' % pub_series_number

        # Publication title
        print '<td dir="ltr">%s</td>' % ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE])

        # Publication date unless this is a Publication Series, in which case we have already displayed the date
        if display_type != 'pubseries':
                print '<td>%s</td>' % ISFDBconvertDate(pub[PUB_YEAR], 1)

        # Author(s)/editor(s)
        print '<td>'
        if pub[PUB_CTYPE] in ('ANTHOLOGY', 'MAGAZINE', 'FANZINE'):
                print 'ed. '
	author_list = ''
        for author in pub_authors[pub[PUB_PUBID]]:
		if author_list:
			author_list += ", "
		author_list += ISFDBLink('ea.cgi', author[0], author[1])
        print '%s</td>' % author_list

        # Publisher and publication series
        displayed_publisher = FormatPublisher(pub, pub_publishers)
        displayed_pub_series = FormatPubSeries(pub, pub_series)
        if display_type == 'publisher':
                output = displayed_pub_series
        elif  display_type == 'pubseries':
                output = displayed_publisher
        else:
                if displayed_publisher and displayed_pub_series:
                        output = '%s (%s)' % (displayed_publisher, displayed_pub_series)
                elif displayed_publisher and not displayed_pub_series:
                        output = displayed_publisher
                elif not displayed_publisher and displayed_pub_series:
                        output = displayed_pub_series
                else:
                        output = ''

        if output:
                print '<td dir="ltr">%s</td>' % output
        else:
                print '<td>&nbsp;</td>'

        # ISBN/Catalog ID
        printISBNCatalog(pub)

        # Price
	if pub[PUB_PRICE]:
		print '<td dir="ltr">%s</td>' % ISFDBPrice(pub[PUB_PRICE])
        else:
                print '<td>&nbsp;</td>'

        # Pages
        if pub[PUB_PAGES]:
                page_list = string.split(pub[PUB_PAGES],'+')
                print '<td>'
                first = 1
                output = ''
                for page_number in page_list:
                        if not first:
                                output += '+<br>'
                        else:
                                first = 0
                        output += ISFDBText(page_number)
                print output
                print '</td>' 
        else:
                print '<td>&nbsp;</td>'

        if pub[PUB_PTYPE]:
                print '<td>%s</td>' % ISFDBPubFormat(pub[PUB_PTYPE])
        else:
                print '<td>&nbsp;</td>'

        # Type
        if pub[PUB_CTYPE]:
                short_names = {'NOVEL': 'novel',
                              'OMNIBUS': 'omni',
                              'MAGAZINE': 'mag',
                              'COLLECTION': 'coll',
                              'ANTHOLOGY': 'anth',
                              'CHAPBOOK': 'chap',
                              'FANZINE': 'fanzine',
                              'NONFICTION': 'non-fic'}
                if pub[PUB_CTYPE] in short_names:
                        print '<td>%s</td>' % short_names[pub[PUB_CTYPE]]
                else:
                        print '<td>%s</td>' % pub[PUB_CTYPE]
        else:
                print '<td>&nbsp;</td>'

        # Cover artists
        print '<td>'
        if pub[PUB_PUBID] in cover_artists:
                artist_count = 0
                for cover_artist in cover_artists[pub[PUB_PUBID]]:
                        artist_id = cover_artist[0]
                        artist_name = cover_artist[1]
                        if artist_count:
                                print ', '
                        displayAuthorById(artist_id, artist_name)
                        artist_count += 1
        else:
                '&nbsp;'
        print '</td>'

        # Verification status
        if SQLPrimaryVerifiers(pub[PUB_PUBID]):
                print '<td class="checkmark"><img src="%s://%s/checkmark.png" alt="Checkmark" height="15" width="15"></td>' % (PROTOCOL, HTMLLOC)
        else:
                print '<td>&nbsp;</td>'

        if user.cover_links_display:
                if pub[PUB_IMAGE]:
                        print '<td>%s</td>' % CoverInfo(pub[PUB_IMAGE], False, True)
                else:
                        print '<td>&nbsp;</td>'
        print '</tr>'

def printISBNCatalog(pub):
        from isbn import convertISBN
        if pub[PUB_ISBN] or pub[PUB_CATALOG]:
                value = ''
                if pub[PUB_ISBN]:
                        value = ISFDBText(convertISBN(pub[PUB_ISBN]))
                if pub[PUB_CATALOG]:
                        if value:
                                value += ' / '
                        value += ISFDBText(pub[PUB_CATALOG])
        else:
                value = '&nbsp;'
        print '<td dir="ltr">%s</td>' % value

def FormatPubSeries(pub, pub_series):
        displayed_pub_series = ''
        if pub[PUB_SERIES] or pub[PUB_SERIES_NUM]:
                if pub[PUB_SERIES]:
                        pub_series_name = pub_series[pub[PUB_SERIES]]
                        displayed_pub_series = ISFDBLink('pubseries.cgi', pub[PUB_SERIES], pub_series_name)
                if pub[PUB_SERIES_NUM]:
                        displayed_pub_series += ' #%s' % ISFDBText(pub[PUB_SERIES_NUM])
        return displayed_pub_series

def FormatPublisher(pub, pub_publishers):
        displayed_publisher = ''
        if pub[PUB_PUBLISHER]:
                publisher_name = pub_publishers[pub[PUB_PUBLISHER]]
                displayed_publisher = ISFDBLink('publisher.cgi', pub[PUB_PUBLISHER], publisher_name)
        return displayed_publisher

def PrintTitleTable(titles, merge, limit = 100, user = None):
	print '<table class="generic_table">'
	print '<tr align="left" class="generic_table_header">'
	if merge:
                print "<th>Merge</th>"
	print "<th>Date</th>"
	print "<th>Type</th>"
	print "<th>Language</th>"
	print "<th>Title</th>"
	print "<th>Authors</th>"
	print "<th>Parent Title</th>"
	print "<th>Parent Authors</th>"
	print "<th>Tags</th>"
 	print "</tr>"
	counter = 1
        bgcolor = 1
        for title in titles:
                PrintTitleRecord(title, merge, limit, bgcolor, user)
                bgcolor ^= 1
                counter += 1
                if counter > limit:
                        break
        print "</table>"

def PrintTitleRecord(title, merge, limit, bgcolor, user):
        title_id = title[TITLE_PUBID]
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        if merge:
                print '<td><INPUT TYPE="checkbox" NAME="merge" VALUE="%s"></td>' % title_id
	print "<td>%s</td>" % ISFDBconvertDate(title[TITLE_YEAR], 1)
	print "<td>%s</td>" % title[TITLE_TTYPE]
	if title[TITLE_LANGUAGE]:
		print "<td>%s</td>" % (LANGUAGES[int(title[TITLE_LANGUAGE])])
	else:
		print "<td>&nbsp;</td>"

	displayed_title = ISFDBLink('title.cgi', title_id, title[TITLE_TITLE])
        print '<td dir="ltr">%s</td>' % displayed_title

	authors = SQLTitleBriefAuthorRecords(title_id)
	print "<td>%s</td>" % FormatAuthors(authors)
	
	if title[TITLE_PARENT]:
                print '<td>'
                parent_data = SQLloadTitle(title[TITLE_PARENT])
                print ISFDBLink('title.cgi', parent_data[TITLE_PUBID], parent_data[TITLE_TITLE])
                print '</td>'
                print '<td>'
		parent_authors = SQLTitleBriefAuthorRecords(parent_data[TITLE_PUBID])
		# Only display the parent author(s) if they are not the same as the variant's author(s)
		if set(authors) != set(parent_authors):
                        print FormatAuthors(parent_authors)
                print '</td>'
	else:
		print '<td>&nbsp;</td>'
		print '<td>&nbsp;</td>'

	print '<td>'
	tags = SQLgetAllTitleTags(title_id, title[TITLE_PARENT], int(user.id))
	if tags:
                first_tag = 1
                output = ''
                for tag in tags:
                        if first_tag:
                                output = '%s (%d)' % (ISFDBLink('tag.cgi', tag[0], tag[1]), tag[2])
                                first_tag = 0
                        else:
                                output += ', %s (%d)' % (ISFDBLink('tag.cgi', tag[0], tag[1]), tag[2])
                print output
        else:
                print '&nbsp;'
	print '</td>'

        print '</tr>'

def PrintPublisherTable(publishers, merge, limit = 100, user = None):
	print '<table class="generic_table">'
	print '<tr align="left" class="generic_table_header">'
	if merge and user.moderator:
        	print '<th>Merge</th>'
	print '<th>Publisher</th>'
 	print '</tr>'
	counter = 1
        bgcolor = 1
        for publisher in publishers:
                PrintPublisherRecord(publisher, bgcolor, user, merge)
                bgcolor ^= 1
                counter += 1
                if counter > limit:
                        break
        print '</table>'

def PrintPublisherRecord(record, bgcolor, user, merge):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

	if merge and user.moderator:
                print '<td><INPUT TYPE="checkbox" NAME="merge" VALUE="%s"></td>' % record[PUBLISHER_ID]
        print '<td>%s</td>' % ISFDBLink('publisher.cgi', record[PUBLISHER_ID], record[PUBLISHER_NAME])
        print '</tr>'

def PrintPubSeriesTable(pub_series, limit = 100):
	print '<table class="generic_table">'
	print '<tr align="left" class="generic_table_header">'
	print '<th>Publication Series</th>'
 	print '</tr>'
	counter = 1
        bgcolor = 1
        for one_pub_series in pub_series:
                PrintPubSeriesRecord(one_pub_series, bgcolor)
                bgcolor ^= 1
                counter += 1
                if counter > limit:
                        break
        print '</table>'

def PrintPubSeriesRecord(record, bgcolor):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'
        print '<td>%s</td>' % ISFDBLink('pubseries.cgi', record[PUB_SERIES_ID], record[PUB_SERIES_NAME])
        print '</tr>'

def PrintSeriesTable(series_list, limit = 100):
	print '<table class="generic_table">'
	print '<tr align="left" class="generic_table_header">'
	print '<th>Series</th>'
	print '<th>Parent Series</th>'
	print '<th>Position Within Parent Series</th>'
 	print '</tr>'
	counter = 1
        bgcolor = 1
        for series in series_list:
                PrintSeriesRecord(series, bgcolor)
                bgcolor ^= 1
                counter += 1
                if counter > limit:
                        break
        print '</table>'

def PrintSeriesRecord(record, bgcolor):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'
        print '<td>%s</td>' % ISFDBLink('pe.cgi', record[SERIES_PUBID], record[SERIES_NAME])
        parent_id = record[SERIES_PARENT]
        if parent_id:
		parent_name = SQLgetSeriesName(parent_id)
                print '<td>%s</td>' % ISFDBLink('pe.cgi', parent_id, parent_name)
        else:
                print '<td>&nbsp;</td>'
        if record[SERIES_PARENT_POSITION]:
                print '<td>%s</td>' % record[SERIES_PARENT_POSITION]
        else:
                print '<td>&nbsp;</td>'
        print '</tr>'

def PrintAuthorTable(authors, merge, limit = 100, user = None):
        author_ids = []
        for author in authors:
                author_ids.append(author[AUTHOR_ID])
        trans_names = SQLLoadTransAuthorNamesList(author_ids)
        trans_legal_names = SQLtransLegalNames(author_ids)

	print '<table class="generic_table">'
	print '<tr align="left" class="generic_table_header">'
	if merge and user.moderator:
        	print "<th>Merge</th>"
	print "<th>Author</th>"
	print "<th>Alternate Name?</th>"
	print "<th>Working Language</th>"
	print "<th>Directory Entry</th>"
	print "<th>Legal Name</th>"
	print "<th>Birth Place</th>"
	print "<th>Birth Date</th>"
	print "<th>Death Date</th>"
 	print "</tr>"
	counter = 1
        bgcolor = 1
        for author in authors:
                pseudonym = SQLauthorIsPseudo(author[AUTHOR_ID])
                PrintAuthorRecord(author, pseudonym, bgcolor, user, trans_names, trans_legal_names, merge)
                bgcolor ^= 1
                counter += 1
                if counter > limit:
                        break
        print "</table>"

def PrintAuthorRecord(record, pseudonym, bgcolor, user, trans_names, trans_legal_names, merge):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

	if merge and user.moderator:
                print '<td><INPUT TYPE="checkbox" NAME="merge" VALUE="' +str(record[AUTHOR_ID])+ '"></td>'
        print "<td>%s</td>" % ISFDBLink('ea.cgi', record[AUTHOR_ID], record[AUTHOR_CANONICAL], False, '', trans_names)
	if pseudonym == 1:
		query = "select 1 from dual where exists (select * from canonical_author a, titles t"
                query += " WHERE a.author_id ='%d'" % (record[AUTHOR_ID])
                query += " AND t.title_id = a.title_id AND t.title_parent = 0 AND a.ca_status = 1);"
		db.query(query)
		result = db.store_result()
		count = result.fetch_row()
		if count:
                        print "<td>Has pseud. titles"
                else:
                        print "<td>Alternate Name"
                print "</td>"
        else:
		print "<td>-</td>"
	if record[AUTHOR_LANGUAGE]:
		print "<td>%s</td>" % LANGUAGES[record[AUTHOR_LANGUAGE]]
	else:
		print "<td>-</td>"
	if record[AUTHOR_LASTNAME]:
		print "<td>" +record[AUTHOR_LASTNAME]+ "</td>"
	else:
		print "<td>-</td>"
	if record[AUTHOR_LEGALNAME]:
                author_id = record[AUTHOR_ID]
		if author_id in trans_legal_names:
                        display_value = ISFDBMouseover(trans_legal_names[author_id], record[AUTHOR_LEGALNAME], 'td')
                        print display_value
                else:
                        print "<td>%s</td>" % record[AUTHOR_LEGALNAME]
	else:
		print "<td>-</td>"
	if record[AUTHOR_BIRTHPLACE]:
		print "<td>" +record[AUTHOR_BIRTHPLACE]+ "</td>"
	else:
		print "<td>-</td>"
	if record[AUTHOR_BIRTHDATE]:
		print "<td>" +record[AUTHOR_BIRTHDATE]+ "</td>"
	else:
		print "<td>-</td>"
	if record[AUTHOR_DEATHDATE]:
		print "<td>" +record[AUTHOR_DEATHDATE]+ "</td>"
	else:
		print "<td>-</td>"
        print "</tr>"

def PrintAnnualGrid(starting_decade, link, year_parameter, display_decade, decade_parameter):
        # Get the current year based on system time
        current_year = localtime()[0]
        # Determine the current decade - Python division returns integers by default
        current_decade = current_year/10*10
        bgcolor = 0
        # Display all decades since the starting decade in reverse chronological order
        for decade in range(current_decade, starting_decade-10, -10):
                print '<tr class="table%d">' % (bgcolor+1)
                if display_decade:
                        print '<td>%s</td>' % ISFDBLinkNoName('%s.cgi' % link, '%s%d' % (decade_parameter, decade), '%ds' % decade)
                for year in range(decade, decade+10):
                        # Skip future years
                        if year > current_year:
                                print '<td>&nbsp;</td>'
                                continue
                        print '<td>%s</td>' % ISFDBLinkNoName('%s.cgi' % link, '%s%d' % (year_parameter, year), '%d' % year)
                print '</tr>'
                bgcolor ^= 1
        print '</table>'
