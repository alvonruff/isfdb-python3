#
#     (C) COPYRIGHT 2005-2023   Al von Ruff, Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1099 $
#     Date: $Date: 2023-02-07 18:29:53 -0500 (Tue, 07 Feb 2023) $

import cgi
import sys
import re
import os
import MySQLdb
from isfdb import *
from isfdblib import *
from library import *
from xml.dom import minidom
from xml.dom import Node

class titles:
	def __init__(self, db):
		self.db = db
		self.used_id         = 0
		self.used_title      = 0
		self.used_trans_titles = 0
		self.used_xlate      = 0
		self.used_year       = 0
		self.used_synop_id   = 0
		self.used_synop      = 0
		self.used_series     = 0
		self.used_seriesnum  = 0
		self.used_ttype      = 0
		self.used_storylen   = 0
		self.used_webpages   = 0
		self.used_language   = 0
		self.used_note_id    = 0
		self.used_note       = 0
		self.used_parent     = 0
		self.used_non_genre  = 0
		self.used_graphic    = 0
		self.used_nvz        = 0
		self.used_jvn        = 0
		self.used_content    = 0

		self.num_authors      = 0
		self.title_authors    = []
		self.title_author_tuples = []
		self.num_subjauthors  = 0
		self.title_subjauthors= []
		self.title_id         = ''
		self.title_title      = ''
		self.title_trans_titles = []
		self.title_xlate      = ''
		self.title_year       = ''
		self.title_synop_id   = ''
		self.title_synop      = ''
		self.title_series     = ''
		self.title_seriesnum  = ''
		self.title_ttype      = ''
		self.title_storylen   = ''
		self.title_webpages   = []
		self.title_language   = ''
		self.title_language_id= ''
		self.title_note_id    = ''
		self.title_note       = ''
		self.title_parent     = ''
		self.title_non_genre  = ''
		self.title_graphic    = ''
		self.title_nvz        = ''
		self.title_jvn        = ''
		self.title_content    = ''

		self.error = ''

	def authors(self):
		counter = 0
		authors = []
		while counter < self.num_authors:
                        authors.append(ISFDBText(ISFDBnormalizeAuthor(self.title_authors[counter])))
			counter += 1
		# Return a '+'-delimited sorted string of author names
		return '<span class="mergesign">+</span>'.join(sorted(authors))

	def load(self, id):
		self.loadCommon(id, 0)

	def loadXML(self, id):
		self.loadCommon(id, 1)

	def loadCommon(self, id, doXML):
		if id == 0:
			return
		record = SQLloadTitle(id)
		if record:
			if record[TITLE_PUBID]:
				self.title_id = record[TITLE_PUBID]
				self.used_id = 1
			if record[TITLE_TITLE]:
				self.title_title = record[TITLE_TITLE]
				self.used_title = 1
			if record[TITLE_XLATE]:
				self.title_xlate  = record[TITLE_XLATE]
				self.used_xlate = 1
			if record[TITLE_SERIESNUM] is not None:
				self.title_seriesnum = str(record[TITLE_SERIESNUM])
				self.used_seriesnum = 1
				if record[TITLE_SERIESNUM_2] is not None:
                                        self.title_seriesnum = '%s.%s' % (self.title_seriesnum, record[TITLE_SERIESNUM_2])
			if record[TITLE_YEAR]:
				self.title_year = record[TITLE_YEAR]
				self.used_year = 1
			if record[TITLE_TTYPE]:
				self.title_ttype = record[TITLE_TTYPE]
				self.used_ttype = 1
			if record[TITLE_STORYLEN]:
				self.title_storylen = record[TITLE_STORYLEN]
				self.used_storylen = 1
			if record[TITLE_PARENT]:
				self.title_parent = record[TITLE_PARENT]
				self.used_parent = 1
			if record[TITLE_LANGUAGE]:
                                self.title_language_id = int(record[TITLE_LANGUAGE])
                                self.title_language = LANGUAGES[self.title_language_id]
                                self.used_language = 1
			if record[TITLE_SERIES]:
                                self.title_series = SQLgetSeriesName(record[TITLE_SERIES])
				self.used_series = 1
			if record[TITLE_NON_GENRE]:
				self.title_non_genre = record[TITLE_NON_GENRE]
				self.used_non_genre = 1
			if record[TITLE_GRAPHIC]:
				self.title_graphic = record[TITLE_GRAPHIC]
				self.used_graphic = 1
			if record[TITLE_JVN]:
				self.title_jvn = record[TITLE_JVN]
				self.used_jvn = 1
			if record[TITLE_NVZ]:
				self.title_nvz = record[TITLE_NVZ]
				self.used_nvz = 1
			if record[TITLE_CONTENT]:
				self.title_content = record[TITLE_CONTENT]
				self.used_content = 1
			
			author_tuples = SQLTitleBriefAuthorRecords(record[TITLE_PUBID])
			for author_tuple in author_tuples:
                                self.title_authors.append(author_tuple[1])
                                self.title_author_tuples.append((author_tuple[0], author_tuple[1]))
                                self.num_authors += 1

                        subj_authors = []
			if record[TITLE_TTYPE] == 'REVIEW':
                                subj_authors = SQLReviewedAuthors(record[TITLE_PUBID])
                        elif record[TITLE_TTYPE] == 'INTERVIEW':
                                subj_authors = SQLIntervieweeAuthors(record[TITLE_PUBID])
                        for subj_author in subj_authors:
                                self.title_subjauthors.append(subj_author[1])
                                self.num_subjauthors += 1

			if record[TITLE_SYNOP]:
                                self.title_synop_id = record[TITLE_SYNOP]
                                self.used_synop_id = 1
                                self.title_synop = SQLgetNotes(record[TITLE_SYNOP])
                                self.used_synop = 1

			if record[TITLE_NOTE]:
                                self.title_note_id = record[TITLE_NOTE]
                                self.used_note_id = 1
                                self.title_note = SQLgetNotes(record[TITLE_NOTE])
                                self.used_note = 1

                        self.title_webpages = SQLloadTitleWebpages(record[TITLE_PUBID])
                        if self.title_webpages:
                                self.used_webpages = 1

                        self.title_trans_titles = SQLloadTransTitles(record[TITLE_PUBID])
                        if self.title_trans_titles:
                                self.used_trans_titles = 1

		else:
			self.error = 'title record not found'
			return

	def cgi2obj(self, from_form = 0):
		sys.stderr = sys.stdout
		if from_form == 0:
                        self.form = cgi.FieldStorage()
                else:
                        self.form = from_form
		try:
			# Check that the submitted Title ID is an integer
                        self.title_id = str(int(self.form['title_id'].value))
                        self.used_id = 1
                except:
                        self.error = 'Title ID must be a valid integer number'
                        return

		try:
			self.title_title = XMLescape(self.form['title_title'].value)
			self.used_title = 1
			if not self.title_title:
                                raise
		except:
                        self.error = 'Title not specified'
                        return

      		for key in self.form:
                        if 'trans_titles' in key:
                                value = XMLescape(self.form[key].value)
                                if value:
                                        self.title_trans_titles.append(value)
                                        self.used_trans_titles = 1

		self.num_authors = 0
		self.title_authors = []
		counter = 0
		while counter < 200:
			if self.form.has_key('title_author'+str(counter+1)):
                                value = self.form['title_author'+str(counter+1)].value
                                value = XMLescape(ISFDBnormalizeAuthor(value))
                                self.error = ISFDBAuthorError(value)
                                if self.error:
                                        return
                                if not ISFDBAuthorInAuthorList(value, self.title_authors):
        				self.title_authors.append(value)
        				self.num_authors += 1
			elif self.form.has_key('review_reviewer1.'+str(counter+1)):
                                value = self.form['review_reviewer1.'+str(counter+1)].value
                                value = XMLescape(ISFDBnormalizeAuthor(value))
                                self.error = ISFDBAuthorError(value)
                                if self.error:
                                        return
                                if not ISFDBAuthorInAuthorList(value, self.title_authors):
        				self.title_authors.append(value)
        				self.num_authors += 1
			elif self.form.has_key('interviewer_author1.'+str(counter+1)):
                                value = self.form['interviewer_author1.'+str(counter+1)].value
                                value = XMLescape(ISFDBnormalizeAuthor(value))
                                self.error = ISFDBAuthorError(value)
                                if self.error:
                                        return
                                if not ISFDBAuthorInAuthorList(value,self.title_authors):
                                        self.title_authors.append(value)
                                        self.num_authors += 1
			counter += 1
                if self.num_authors == 0:
                        self.error = "No authors were specified"
                        return

		self.num_subjauthors = 0
		self.title_subjauthors = []
		counter = 0
		while counter < 200:
			if self.form.has_key('review_author1.'+str(counter+1)):
                                value = self.form['review_author1.'+str(counter+1)].value
                                value = XMLescape(ISFDBnormalizeAuthor(value))
                                self.error = ISFDBAuthorError(value)
                                if self.error:
                                        return
                                if not ISFDBAuthorInAuthorList(value, self.title_subjauthors):
        				self.title_subjauthors.append(value)
        				self.num_subjauthors += 1
			elif self.form.has_key('interviewee_author1.'+str(counter+1)):
                                value = self.form['interviewee_author1.'+str(counter+1)].value
                                value = XMLescape(ISFDBnormalizeAuthor(value))
                                self.error = ISFDBAuthorError(value)
                                if self.error:
                                        return
                                if not ISFDBAuthorInAuthorList(value, self.title_subjauthors):
        				self.title_subjauthors.append(value)
        				self.num_subjauthors += 1
			counter += 1


		try:
			self.title_year = XMLescape(self.form['title_copyright'].value)
			if not self.title_year:
                                raise
			# Validate and normalize the date - change to 0000-00-00 if it's invalid
			self.title_year = ISFDBnormalizeDate(self.title_year)
			self.used_year = 1
		except:
                        self.error = 'Date not specified'
                        return

                try:
                        value = self.form['title_ttype'].value
                        if value not in ('ANTHOLOGY','COLLECTION','COVERART',
                                     'INTERIORART','EDITOR','ESSAY','INTERVIEW','NOVEL',
                                     'NONFICTION','OMNIBUS','POEM','REVIEW','SERIAL',
                                     'SHORTFICTION','CHAPBOOK'):
                                raise
                        self.title_ttype = value
                        self.used_ttype = 1
                except:
                        self.error = 'Invalid Title Type'
                        return

                # Validate optional fields
                self.validateOptional()

        def validateOptional(self):
                # This method is called from the NewPub submission script
                # as well as from method cg2obj above
		if self.form.has_key('title_series'):
                        value = XMLescape(self.form['title_series'].value)
                        if value:
        			self.title_series = value
        			self.used_series = 1
        			
		if self.form.has_key('title_seriesnum'):
                        value = XMLescape(self.form['title_seriesnum'].value)
                        if value:
        			self.title_seriesnum = value
        			self.used_seriesnum = 1
                                # Check that the entered series number is a decimal number - duplication
                                # of the Javascript check in case Javascript is disabled in the browser
                                if not re.match(r'[0-9]{1,9}([\.]{1}[0-9]{1,4}){0,1}$', self.title_seriesnum):
                                        self.error = """Series numbers must be between 1 and 999999999.
                                                You can use a decimal point and up to 4 digits after it to
                                                position titles in between other titles in the series,
                                                e.g. 3.5 will appear between 3 and 4"""
                                        return
                                
		if self.form.has_key('title_translator'):
                        value = XMLescape(self.form['title_translator'].value)
                        if value:
        			self.title_xlate = value
        			self.used_xlate = 1

		for key in self.form:
                        if key.startswith('title_webpages') or key.startswith('shared_title_webpages'):
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.title_webpages:
                                                continue
                                        self.error = invalidURL(value)
                                        if self.error:
                                                return
                                        self.title_webpages.append(value)
                                        self.used_webpages = 1
	
		if self.form.has_key('language'):
                        value = XMLescape(self.form['language'].value)
                        if value:
                                if value not in LANGUAGES:
                                        self.error = 'Invalid Language - %s' % value
                                        return
        			self.title_language = value
        			self.used_language = 1
        			
		if self.form.has_key('title_storylen'):
                        value = XMLescape(self.form['title_storylen'].value)
                        if value:
                                if value not in SESSION.db.storylen_codes:
                                        self.error = 'Invalid length - %s' % value
                                        return
                                self.title_storylen = value
                                if self.title_ttype != 'SHORTFICTION' and self.title_storylen:
                                        self.error = 'Only SHORTFICTION titles can have length specified'
                                        return
                                self.used_storylen = 1

		if self.form.has_key('title_parent'):
                        value = XMLescape(self.form['title_parent'].value)
                        if value:
        			self.title_parent = value
        			self.used_parent = 1
        			
		if self.form.has_key('title_synopsis'):
                        value = XMLescape(self.form['title_synopsis'].value)
                        if value:
        			self.title_synop = value
        			self.used_synop = 1
        			
		if self.form.has_key('title_note'):
                        value = XMLescape(self.form['title_note'].value)
                        if value:
        			self.title_note = value
        			self.used_note = 1

		if self.form.has_key('title_non_genre'):
                        self.title_non_genre = 'Yes'
                        self.used_non_genre = 1
                else:
                        self.title_non_genre = 'No'
                        self.used_non_genre = 1                        

		if self.form.has_key('title_graphic'):
                        self.title_graphic = 'Yes'
                        self.used_graphic = 1
                else:
                        self.title_graphic = 'No'
                        self.used_graphic = 1

		if self.form.has_key('title_nvz'):
                        self.title_nvz = 'Yes'
                        self.used_nvz = 1
                else:
                        self.title_nvz = 'No'
                        self.used_nvz = 1

		if self.form.has_key('title_jvn'):
                        self.title_jvn = 'Yes'
                        self.used_jvn = 1
                else:
                        self.title_jvn = 'No'
                        self.used_jvn = 1

		if self.form.has_key('title_content'):
                        value = XMLescape(self.form['title_content'].value)
                        if value:
                                if self.title_ttype != 'OMNIBUS':
                                        self.error = 'Only OMNIBUS titles can have Content data'
                                        return
                                if len(value) > 254:
                                        self.error = 'Content value must be 254 characters or less'
                                        return
                                if value[0] == '/':
                                        self.error = 'Content value cannot begin with a slash'
                                        return
                                self.title_content = value
                                self.used_content = 1

		# Additional validation for CHAPBOOK titles
                if self.title_ttype == 'CHAPBOOK':
                        if self.used_synop:
                                self.error = 'CHAPBOOKs cannot have synopsis data'
                                return
                        if self.used_series:
                                self.error = 'CHAPBOOKs cannot have series data'
                                return
                        if self.used_seriesnum:
                                self.error = 'CHAPBOOKs cannot have series data'
                                return

                # Additional validation for COVERART/INTERIORART titles
                if self.title_ttype in ('COVERART', 'INTERIORART'):
                        if self.title_graphic == 'Yes':
                                self.error = 'COVERART and INTERIORART titles can\'t be graphic'
                                return
                
        def delete(self):
                # This method tries to delete a single title record.
                #  It returns 1 if the delete operation was a success
                #  and 0 if the title couldn't be deleted
                Record = int(self.title_id)
                # Check that the title is not in any pubs
                query = "select * from pub_content where title_id = %d" % Record
                db.query(query)
                res = db.store_result()
                if res.num_rows():
                        # If this title is in a pub, do not delete it
                        # and return with the status code set to failure 
                        return 0
                
		##########################################################
		# Delete Note
		##########################################################
		if self.title_note_id:
			update = "delete from notes where note_id=%d" % (self.title_note_id)
			print "<li> ", update
			db.query(update)

		##########################################################
		# Delete Synopsis
		##########################################################
		if self.title_synop_id:
                        update = "delete from notes where note_id=%d" % (self.title_synop_id)
                        print "<li> ", update
                        db.query(update)

		##########################################################
		# Delete Any Stranded Series
		##########################################################
		#query = 'select series_id from titles where title_id=%d and series_id is not null' % (Record)
        	#db.query(query)
        	#res = db.store_result()
		#if res.num_rows():
        	#	record = res.fetch_row()
		#	Series = record[0][0]
		#	query = 'select COUNT(series_id) from titles where series_id=%d' % (int(Series))
        	#	db.query(query)
        	#	res = db.store_result()
        	#	rec = res.fetch_row()
		#	if rec[0][0] == 1:
		#		query = 'delete from series where series_id=%d' % (int(Series))
		#		print "<li> ", query
        	#		db.query(query)

		##########################################################
		# Delete Any Stranded Authors
		##########################################################
		query = """select a.author_id from authors a, canonical_author ca
                        where a.author_id=ca.author_id and ca.title_id=%d""" % (Record)
		db.query(query)
		res = db.store_result()
		author = res.fetch_row()
		while author:
			self.deleteAuthor(author[0][0])
			author = res.fetch_row()

		##########################################################
		# Delete pub/title map
		##########################################################
		query = "delete from pub_content where title_id=%d" % (Record)
		print "<li> ", query
		db.query(query)

		##########################################################
		# Delete any title relationships
		##########################################################
		query = "delete from title_relationships where title_id=%d" % (Record)
		print "<li> ", query
		db.query(query)
		query = "delete from title_relationships where review_id=%d" % (Record)
		print "<li> ", query
		db.query(query)

		##########################################################
		# Delete Votes
		##########################################################
		query = "delete from votes where title_id=%d" % (Record)
		print "<li> ", query
		db.query(query)

		##########################################################
		# Delete Tag Mappings for this Title
		##########################################################
		query = "delete from tag_mapping where title_id=%d" % (Record)
		print "<li> ", query
		db.query(query)

		##########################################################
		# Delete any Tags that are no longer used by other Titles
		##########################################################
		query = "delete from tags where not exists (select 1 from tag_mapping where tags.tag_id=tag_mapping.tag_id)"
		print "<li> ", query
		db.query(query)

		##########################################################
		# Delete Webpages
		##########################################################
		query = "delete from webpages where title_id=%d" % (Record)
		print "<li> ", query
		db.query(query)

		##########################################################
		# Delete Transliterated Titles
		##########################################################
                delete = 'delete from trans_titles where title_id=%d' % Record
                print "<li> ", delete
                db.query(delete)

		##########################################################
		# Delete title views
		##########################################################
                delete = 'delete from title_views where title_id=%d' % Record
                print "<li> ", delete
                db.query(delete)

		##########################################################
		# Delete the title itself
		##########################################################
		query = "delete from titles where title_id=%d" % (Record)
		print "<li> ", query
		db.query(query)
		return 1

        def deleteAuthor(self, author_id):
                from common import deleteFromAuthorTable

                ##############################################
                # STEP 1 - Delete the author entry for this
                #          title from canonical_author
                ##############################################
                query = "delete from canonical_author where author_id=%d and title_id=%d" % (int(author_id), self.title_id)
                print "<li> ", query
                db.query(query)

                ##############################################
                # STEP 2 - If the author still has an entry
                #          in any of the mapping tables, do not delete it
                ##############################################
                for i in ['canonical_author', 'pub_authors']:
                        query = 'select COUNT(author_id) from %s where author_id=%d' % (i, int(author_id))
                        print "<li> ", query
                        db.query(query)
                        res = db.store_result()
                        record = res.fetch_row()
                        if record[0][0]:
                                return

                ##############################################
                # STEP 3 - If no other record references this author,
                #          delete it
                ##############################################
                deleteFromAuthorTable(author_id)
