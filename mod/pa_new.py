#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2024   Al von Ruff, Ahasuerus, Bill Longley and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1166 $
#     Date: $Date: 2024-02-08 14:50:44 -0500 (Thu, 08 Feb 2024) $


import random
from isfdb import *
from isfdblib import *
from pubClass import *
from SQLparsing import *
from common import *
from library import *

debug = 0

def Unique(db, tag):
	query = "select pub_tag from pubs where pub_tag='%s'" % (tag)
	db.query(query)
        result = db.store_result()
	if result.num_rows():
		return 0
	else:
		return 1

charmap = ['B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Z']

def CreateTag(db, title, year):

	########################################################
	# STEP 1 - Convert the entire title string to upper case
	########################################################
	newtitle = string.upper(title)

	########################################################
	# STEP 2 - Extract the consonants. Max length = 10
	########################################################
	counter = 0
	chars   = 0
	base = ''
	while counter < len(newtitle):
		if newtitle[counter] in charmap:
			base += newtitle[counter]
			chars += 1
		if chars > 9:
			break
		counter += 1

	########################################################
	# STEP 3 - If length < 10, pad with random consonants
	########################################################
	while chars < 10:
		# create random characters until there are 10
		char = random.choice(charmap)
		base += char
		chars += 1
	
	########################################################
	# STEP 4 - Test uniqueness of tag. If already exists
	#          generate random last characters until good
	########################################################
	tag = base + year
	tries = 0
	while Unique(db, tag) == 0:
		base = base[:len(base)-1]
		try:
			char = charmap[tries]
		except:
			char = str(tries)
			# Reset tries so we go back to letters rather than
			# adding '20' then '221' then '2222' then '22223' etc
			tries = -1
		base += char
		tag = base + year
		tries += 1
	return tag



def UpdatePubColumn(doc, tag, column, id):
	value = GetElementValue(doc, tag)

	if TagPresent(doc, tag):
		value = XMLunescape(value)
		value = db.escape_string(value)
		update = "update pubs set %s='%s' where pub_id=%s" % (column, value, id)
		print "<li> ", update
		if debug == 0:
        		db.query(update)

	if tag == 'Tag':
		# Create a unique pub tag
                title = GetElementValue(doc, 'Title')
                title = XMLunescape(title)
                title = db.escape_string(title)
                year = GetElementValue(doc, 'Year')
                year = year[:4]
                tag = CreateTag(db, title, year)
		update = "update pubs set %s='%s' where pub_id=%s" % (column, tag, id)
		print "<li> ", update
		if debug == 0:
        		db.query(update)

def UpdateTitleColumn(doc, tag, column, id):
	value = GetElementValue(doc, tag)
	if TagPresent(doc, tag):
		value = XMLunescape(value)

		if column == 'title_ttype':
        		if (value == 'MAGAZINE') or (value == 'FANZINE'):
                                value = 'EDITOR'

                elif column in ('title_synopsis', 'note_id'):
                        insert = "insert into notes(note_note) values('%s')" % db.escape_string(value)
                        print "<li> ", insert
                        if debug == 0:
                                db.query(insert)
                        # Get the ID of the created Notes record
                        value = str(db.insert_id())

		elif column == 'title_language':
                        value = SQLGetLangIdByName(value)
                        value = str(value)

		update = "update titles set %s='%s' where title_id=%d" % (db.escape_string(column), db.escape_string(value), int(id))
		print "<li> ", update
		if debug == 0:
        		db.query(update)


def addPubAuthor(author, pub_id):
	##############################################
	# STEP 1 - Get the author_id for this name,
	#          or else create one
	##############################################
	query = "select author_id from authors where author_canonical='%s'" % (db.escape_string(author))
        db.query(query)
        result = db.store_result()
	if result.num_rows():
        	record = result.fetch_row()
		author_id = record[0][0]
	else:
		author_id = insertAuthorCanonical(author)

	##############################################
	# STEP 2 - Insert author mapping into 
	#          pub_authors
	##############################################
	insert = "insert into pub_authors(pub_id, author_id) values('%d', '%d');" % (int(pub_id), author_id)
	print "<li> ", insert
	if debug == 0:
		db.query(insert)

def integrateCover(title, authors, date, pub_id, lang_id):

	########################################################
	# STEP 1 - Create a new Title record in the titles table
	########################################################
        query = """insert into titles(title_title, title_copyright, title_ttype)
                values('%s', '%s', '%s')""" % (db.escape_string(title), db.escape_string(date), 'COVERART')
	print "<li> ", query
	if debug == 0:
		db.query(query)
	TitleRecord = db.insert_id()
	# Copy the language ID from the main Title record to this Cover title
	if lang_id:
                query = "update titles set title_language = '%s' where title_id = %d" % (str(lang_id), int(TitleRecord))
        	print "<li> ", query
        	if debug == 0:
        		db.query(query)

	####################################################
	# STEP 2 - Create author records for any new artists
	####################################################
	artist_list = string.split(authors, "+")
	for artist in artist_list:
		addTitleAuthor(artist, TitleRecord, 'CANONICAL')

	####################################################
	# STEP 3 - Create an entry in the pub_content table
	####################################################
        query = "insert into pub_content(pub_id, title_id) values(%d, %d)" % (int(pub_id), int(TitleRecord))
	print "<li> ", query
	if debug == 0:
		db.query(query)
	return TitleRecord


def integrateTitle(title, authors, date, page, type, length, pub_id, lang_id):

	####################################################
	# STEP 1 - Update the title table
	####################################################
	if type == 'SHORTFICTION' and length:
		query = "insert into titles(title_title, title_copyright, title_ttype, title_storylen) values('%s', '%s', '%s', '%s');" % (db.escape_string(title), date, type, length)
	else:
		query = "insert into titles(title_title, title_copyright, title_ttype) values('%s', '%s', '%s');" % (db.escape_string(title), date, type)
	print "<li> ", query
	if debug == 0:
		db.query(query)
	TitleRecord = db.insert_id()
	# Copy the language ID from the main Title record to this Content Title record
	if lang_id:
                query = "update titles set title_language = '%s' where title_id = '%d'" % (str(lang_id), int(TitleRecord))
        	print "<li> ", query
        	if debug == 0:
        		db.query(query)

	####################################################
	# STEP 2 - Take care of the authors
	####################################################
	authorlist = string.split(authors, "+")
	for author in authorlist:
		addTitleAuthor(author, TitleRecord, 'CANONICAL')
		
	####################################################
	# STEP 3 - Take care of pub linkage and page number
	####################################################
	if page == '':
		query = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(pub_id), int(TitleRecord))
	else:
		query = "insert into pub_content(pub_id, title_id, pubc_page) values(%d, %d, '%s');" % (int(pub_id), int(TitleRecord), db.escape_string(page))
	print "<li> ", query
	if debug == 0:
		db.query(query)


def integrateReview(title, authors, reviewers, date, page, pub_id, lang_id):

	####################################################
	# STEP 1 - Update the title table
	####################################################
	query = "insert into titles(title_title, title_copyright, title_ttype) values('%s', '%s', 'REVIEW');" % (db.escape_string(title), date)
	print "<li> ", query
	if debug == 0:
		db.query(query)
	TitleRecord = db.insert_id()
	# Copy the language ID from the main Title record to this Review record
	if lang_id:
                query = "update titles set title_language = '%s' where title_id = '%d'" % (str(lang_id), int(TitleRecord))
        	print "<li> ", query
        	if debug == 0:
        		db.query(query)

	####################################################
	# STEP 2 - Take care of the reviewers
	####################################################
	authorlist = string.split(reviewers, "+")
	for author in authorlist:
		addTitleAuthor(author, TitleRecord, 'CANONICAL')
		
	####################################################
	# STEP 3 - Take care of the reviewees
	####################################################
	authorlist = string.split(authors, "+")
	for author in authorlist:
		addTitleAuthor(author, TitleRecord, 'REVIEWEE')

	####################################################
	# STEP 4 - Generate title relationship entries
	####################################################
	for author in authorlist:
                parent = SQLFindReviewParent(title, author, lang_id)
                if parent:
                        update = "insert into title_relationships(title_id, review_id) values(%d, %d);" % (parent, TitleRecord)
                        print "<li>", update
                        if debug == 0:
                                db.query(update)
                        break
		
	####################################################
	# STEP 5 - Take care of pub linkage and page number
	####################################################
	if page == '':
		query = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(pub_id), int(TitleRecord))
	else:
		query = "insert into pub_content(pub_id, title_id, pubc_page) values(%d, %d, '%s');" % (int(pub_id), int(TitleRecord), db.escape_string(page))
	print "<li> ", query
	if debug == 0:
		db.query(query)


def integrateInterview(title, interviewees, interviewers, date, page, pub_id, lang_id):

	####################################################
	# STEP 1 - Update the title table
	####################################################
	query = "insert into titles(title_title, title_copyright, title_ttype) values('%s', '%s', 'INTERVIEW');" % (db.escape_string(title), date)
	print "<li> ", query
	if debug == 0:
		db.query(query)
	TitleRecord = db.insert_id()
	# Copy the language ID from the main Title record to this Interview record
	if lang_id:
                query = "update titles set title_language = '%s' where title_id = '%d'" % (str(lang_id), int(TitleRecord))
        	print "<li> ", query
        	if debug == 0:
        		db.query(query)

	####################################################
	# STEP 2 - Take care of the interviewers
	####################################################
	authorlist = string.split(interviewers, "+")
	for author in authorlist:
		addTitleAuthor(author, TitleRecord, 'CANONICAL')
		
	####################################################
	# STEP 3 - Take care of the interviewees
	####################################################
	authorlist = string.split(interviewees, "+")
	for author in authorlist:
		addTitleAuthor(author, TitleRecord, 'INTERVIEWEE')
		
	####################################################
	# STEP 3 - Take care of pub linkage and page number
	####################################################
	if page == '':
		query = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(pub_id), int(TitleRecord))
	else:
		query = "insert into pub_content(pub_id, title_id, pubc_page) values(%d, %d, '%s');" % (int(pub_id), int(TitleRecord), db.escape_string(page))
	print "<li> ", query
	if debug == 0:
		db.query(query)

def DoSubmission(db, submission):
	xml = SQLloadXML(submission)
	doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('NewPub'):

		print "<ul>"
		query = "insert into pubs(pub_title) values('xxx');"
		print "<li> ", query
		if debug == 0:
			db.query(query)
		Record = db.insert_id()

		merge = doc.getElementsByTagName('NewPub')
		UpdatePubColumn(merge, 'Title',   'pub_title',      Record)

                # Transliterated Titles
		value = GetElementValue(merge, 'TransTitles')
        	if value:
			trans_titles = doc.getElementsByTagName('TransTitle')
			for trans_title in trans_titles:
                                title_value = XMLunescape(trans_title.firstChild.data.encode('iso-8859-1'))
                                update = """insert into trans_pubs(pub_id, trans_pub_title)
                                            values(%d, '%s')""" % (int(Record), db.escape_string(title_value))
                                print "<li> ", update
                                db.query(update)

		UpdatePubColumn(merge, 'Tag',     'pub_tag',        Record)
		UpdatePubColumn(merge, 'Year',    'pub_year',       Record)
		UpdatePubColumn(merge, 'Pages',   'pub_pages',      Record)
		UpdatePubColumn(merge, 'PubSeriesNum',   'pub_series_num',      Record)
		UpdatePubColumn(merge, 'Binding', 'pub_ptype',      Record)
		UpdatePubColumn(merge, 'PubType', 'pub_ctype',      Record)
		UpdatePubColumn(merge, 'Isbn',    'pub_isbn',       Record)
		UpdatePubColumn(merge, 'Catalog', 'pub_catalog',    Record)
		UpdatePubColumn(merge, 'Price',   'pub_price',      Record)
		UpdatePubColumn(merge, 'Image',   'pub_frontimage', Record)

		##########################################################
		# Auto-verifications
		##########################################################
		submitter = GetElementValue(merge, 'Submitter')
		submitterid = SQLgetSubmitterID(submitter)
		source = GetElementValue(merge, 'Source')
        	if source == 'Primary':
			insert = SQLInsertPrimaryVerification(Record, 0, submitterid)
			print '<li>%s' % (insert)
        	elif source == 'Transient':
			insert = SQLInsertPrimaryVerification(Record, 1, submitterid)
			print '<li>%s' % (insert)

		#################################################################
		# NOTE, auto-updated with the Source information for some sources
		#################################################################
		note = GetElementValue(merge, 'Note')
		if source == 'PublisherWebsite':
                        note = 'Data from publisher\'s website. %s' % (note)
		elif source == 'AuthorWebsite':
                        note = 'Data from author\'s website. %s' % (note)
        	if note:
			query = 'select note_id from pubs where pub_id=%s and note_id is not null;' % Record
        		db.query(query)
        		res = db.store_result()
			if res.num_rows():
        			rec = res.fetch_row()
				note_id = rec[0][0]
				update = "update notes set note_note='%s' where note_id=%d" % (db.escape_string(note), note_id)
				print "<li> ", update
				if debug == 0:
					db.query(update)
			else:
				insert = "insert into notes(note_note) values('%s');" % db.escape_string(note)
				print "<li> ", insert
				if debug == 0:
					db.query(insert)
				retval = db.insert_id()
                                update = "update pubs set note_id='%d' where pub_id=%s" % (retval, Record)
                                print "<li> ", update
				if debug == 0:
                                	db.query(update)

		##########################################################
		# PUBLISHER
		##########################################################
		value = GetElementValue(merge, 'Publisher')
        	if value:

			# STEP 1 - Get the ID for the new publisher
			query = "select publisher_id from publishers where publisher_name='%s';" % (db.escape_string(value))
			print "<li> ", query
        		db.query(query)
        		res = db.store_result()
			if res.num_rows():
        			record = res.fetch_row()
				NewPublisher = record[0][0]
			else:
				query = "insert into publishers(publisher_name) values('%s');" % (db.escape_string(value))
				print "<li> ", query
				if debug == 0:
        				db.query(query)
				NewPublisher = db.insert_id()

			# STEP 2 - Update the publication record
			update = "update pubs set publisher_id='%d' where pub_id=%s" % (NewPublisher, Record)
			print "<li> ", update
			if debug == 0:
        			db.query(update)

		##########################################################
		# PUBLICATION SERIES
		##########################################################
		value = GetElementValue(merge, 'PubSeries')
        	if value:

			# STEP 1 - Get the ID for the new Publication Series
			query = "select pub_series_id from pub_series where pub_series_name='%s';" % (db.escape_string(value))
			print "<li> ", query
        		db.query(query)
        		res = db.store_result()
			if res.num_rows():
        			record = res.fetch_row()
				NewPublisher = record[0][0]
			else:
				query = "insert into pub_series(pub_series_name) values('%s');" % (db.escape_string(value))
				print "<li> ", query
				if debug == 0:
        				db.query(query)
				NewPublisher = db.insert_id()

			# STEP 2 - Update the publication record
			update = "update pubs set pub_series_id='%d' where pub_id=%s" % (NewPublisher, Record)
			print "<li> ", update
			if debug == 0:
        			db.query(update)

                # Web Pages for the Publication record
                value = GetElementValue(merge, 'PubWebpages')
                if value:
                        webpages = doc.getElementsByTagName('PubWebpage')
                        for webpage in webpages:
                                address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                                update = "insert into webpages(pub_id, url) values(%d, '%s')" % (int(Record), db.escape_string(address))
                                print "<li> ", update
                                db.query(update)

		##########################################################
		# PUBLICATION AUTHORS
		##########################################################
		value = GetElementValue(merge, 'Authors')
		if value:
			authors = doc.getElementsByTagName('Author')
			for author in authors:
				data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
				addPubAuthor(data, Record)

		##########################################################
		# EXTERNAL IDENTIFIERS
		##########################################################
                if GetElementValue(merge, 'External_IDs'):
                        external_id_elements = doc.getElementsByTagName('External_ID')
                        for external_id_element in external_id_elements:
                                type_id = GetChildValue(external_id_element, 'IDtype')
                                id_value = XMLunescape(GetChildValue(external_id_element, 'IDvalue'))
                                insert = """insert into identifiers(identifier_type_id, identifier_value,
                                            pub_id) values(%d, '%s', %d)
                                            """ % (int(type_id), db.escape_string(id_value), Record)
                                print "<li> ", insert
                                db.query(insert)

                # Create a new Title record and populate its fields if specified
		if TagPresent(merge, 'Parent'):
			TitleRecord = GetElementValue(merge, 'Parent')
			lang_id = SQLGetLangIdByTitle(TitleRecord)
		else:
			##########################################################
			# TITLE
			##########################################################
			query = "insert into titles(title_title) values('xxx');"
			print "<li> ", query
			if debug == 0:
				db.query(query)
			TitleRecord = db.insert_id()
			UpdateTitleColumn(merge, 'Title',     'title_title',     TitleRecord)
			UpdateTitleColumn(merge, 'Year',      'title_copyright', TitleRecord)
			UpdateTitleColumn(merge, 'PubType',   'title_ttype',     TitleRecord)
			UpdateTitleColumn(merge, 'Synopsis',  'title_synopsis',  TitleRecord)
			UpdateTitleColumn(merge, 'TitleNote', 'note_id',         TitleRecord)
			UpdateTitleColumn(merge, 'Language',  'title_language',  TitleRecord)
			UpdateTitleColumn(merge, 'ContentIndicator', 'title_content', TitleRecord)
			UpdateTitleColumn(merge, 'Juvenile',  'title_jvn',       TitleRecord)
			UpdateTitleColumn(merge, 'Novelization', 'title_nvz',    TitleRecord)
			UpdateTitleColumn(merge, 'NonGenre',  'title_non_genre', TitleRecord)
			UpdateTitleColumn(merge, 'Graphic',   'title_graphic',   TitleRecord)
			lang_id = SQLGetLangIdByTitle(TitleRecord)

                        ##########################################################
                        # SERIES
                        ##########################################################
                        if TagPresent(merge, 'Series'):
                                value = GetElementValue(merge, 'Series')
                                if value:
                                        series_id = SQLFindSeriesId(value)
                                        if not series_id:
                                                query = "insert into series(series_title) values('%s')" % (db.escape_string(value))
                                                print "<li> ", query
                                                if debug == 0:
                                                        db.query(query)
                                                series_id = db.insert_id()

                                        update = "update titles set series_id=%d where title_id=%d" % (int(series_id), int(TitleRecord))
                                        print "<li> ", update
                                        if debug == 0:
                                                db.query(update)

                        ##########################################################
                        # Series numbers 1 and 2
                        ##########################################################
                        if TagPresent(merge, 'SeriesNum'):
                                value = GetElementValue(merge, 'SeriesNum')
                                if value:
                                        series_list = value.split('.')
                                        if len(series_list):
                                                update = "update titles set title_seriesnum=%d where title_id=%d" % (int(series_list[0]), int(TitleRecord))
                                                print "<li> ", update
                                                if debug == 0:
                                                        db.query(update)
                                        if len(series_list) > 1:
                                                # The secondary series number is a string rather than an integer, e.g. "05" is allowed
                                                update = "update titles set title_seriesnum_2='%s' where title_id=%d" % (db.escape_string(series_list[1]), int(TitleRecord))
                                                print "<li> ", update
                                                if debug == 0:
                                                        db.query(update)

                        # Transliterated Titles
                        value = GetElementValue(merge, 'TransTitles')
                        if value:
                                trans_titles = doc.getElementsByTagName('TransTitle')
                                for trans_title in trans_titles:
                                        title_value = XMLunescape(trans_title.firstChild.data.encode('iso-8859-1'))
                                        update = """insert into trans_titles(title_id, trans_title_title)
                                                    values(%d, '%s')""" % (int(TitleRecord), db.escape_string(title_value))
                                        print "<li> ", update
                                        db.query(update)

                        # Web Pages for the Title record
                        value = GetElementValue(merge, 'Webpages')
                        if value:
                                webpages = doc.getElementsByTagName('Webpage')
                                for webpage in webpages:
                                        address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                                        update = "insert into webpages(title_id, url) values(%d, '%s')" % (int(TitleRecord), db.escape_string(address))
                                        print "<li> ", update
                                        db.query(update)

			##########################################################
			# TITLE AUTHORS
			##########################################################
			value = GetElementValue(merge, 'Authors')
			if value:
				authors = doc.getElementsByTagName('Author')
				for author in authors:
					data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
					addTitleAuthor(data, TitleRecord, 'CANONICAL')

		query = "insert into pub_content(pub_id, title_id) values(%d, %d);" % (int(Record), int(TitleRecord))
		print "<li> ", query
		if debug == 0:
			db.query(query)


        	if doc.getElementsByTagName('Content'):
			##########################################################
			# Covers
			##########################################################
			children = doc.getElementsByTagName('Cover')
			if len(children):
				for child in children:
					title   = GetChildValue(child, 'cTitle')
					artists = GetChildValue(child, 'cArtists')
					date    = GetChildValue(child, 'cDate')
					coverTitle = integrateCover(title, artists, date, Record, lang_id)
                                        # Transliterated Cover Art Titles
                                        value = GetElementValue(merge, 'TransTitles')
                                        if value:
                                                trans_titles = doc.getElementsByTagName('TransTitle')
                                                for trans_title in trans_titles:
                                                        title_value = XMLunescape(trans_title.firstChild.data.encode('iso-8859-1'))
                                                        update = """insert into trans_titles(title_id, trans_title_title)
                                                                    values(%d, '%s')""" % (int(coverTitle), db.escape_string(title_value))
                                                        print "<li> ", update
                                                        db.query(update)

			##########################################################
			# Content
			##########################################################
			children = doc.getElementsByTagName('ContentTitle')
			if len(children):
				for child in children:
					title   = GetChildValue(child, 'cTitle')
					authors = GetChildValue(child, 'cAuthors')
					date    = GetChildValue(child, 'cDate')
					page    = GetChildValue(child, 'cPage')
					type    = GetChildValue(child, 'cType')
					length  = GetChildValue(child, 'cLength')
					integrateTitle(title, authors, date, page, type, length, Record, lang_id)
			
			##########################################################
			# Reviews
			##########################################################
			children = doc.getElementsByTagName('ContentReview')
			if len(children):
				for child in children:
					title     = GetChildValue(child, 'cTitle')
					authors   = GetChildValue(child, 'cBookAuthors')
					reviewers = GetChildValue(child, 'cReviewers')
					date      = GetChildValue(child, 'cDate')
					page      = GetChildValue(child, 'cPage')
					integrateReview(title, authors, reviewers, date, page, Record, lang_id)

			##########################################################
			# Interviews
			##########################################################
			children = doc.getElementsByTagName('ContentInterview')
			if len(children):
				for child in children:
					title        = GetChildValue(child, 'cTitle')
					interviewees = GetChildValue(child, 'cInterviewees')
					interviewers = GetChildValue(child, 'cInterviewers')
					date         = GetChildValue(child, 'cDate')
					page         = GetChildValue(child, 'cPage')
					integrateInterview(title, interviewees, interviewers, date, page, Record, lang_id)

		if debug == 0:
			markIntegrated(db, submission, Record)

	return(Record)

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('New Publication - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

	print "<h1>SQL Updates:</h1>"
	print "<hr>"

	Record = DoSubmission(db, submission)

        print ISFDBLinkNoName('edit/editpub.cgi', Record, 'Edit This Pub', True)
        print ISFDBLinkNoName('pl.cgi', Record, 'View This Pub', True)
        print ISFDBLinkNoName('edit/find_pub_dups.cgi', Record, 'Check for Duplicate Titles', True)
	print '<p>'
        LIBPrintDuplicateWarning(Record)

	PrintPostMod(0)
