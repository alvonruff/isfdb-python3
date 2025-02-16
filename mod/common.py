from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Bill Longley, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1176 $
#     Date: $Date: 2024-05-02 19:26:24 -0400 (Thu, 02 May 2024) $


import sys
import MySQLdb
from isfdb import *
from SQLparsing import *
from library import *
from login import *
from urlparse import urlparse
from isbn import ISBNValidFormat
from xml.dom import minidom
from xml.dom import Node

debug = 0


def findReferralLang(pub_id):
        # Find the language of the "referral" title record in this publication
        #
        # Retrieve publication data for this pub
        pub = SQLGetPubById(pub_id)
        # Retrieve the "referral" title for this pub
        # Pass a third parameter to SQLgetTitleReferral to indicate that we want EDITOR titles for magazines/fanzines
        referral_id = SQLgetTitleReferral(pub_id, pub[PUB_CTYPE], 1)
        # If a referral title record has been found, then load its data
        if referral_id != 0:
                referral_title = SQLloadTitle(referral_id)
                # Extract the referral title's language
                referral_lang = referral_title[TITLE_LANGUAGE]
        # If there is no referral title for this pub, then set the language code to None
        else:
                referral_lang = None
        return referral_lang
        
def PrintSubmissionLinks(submission_id, reviewer_id):
        # If the reviewer is a self-approver, display the reviewer's next submission
        if not SQLisUserModerator(reviewer_id):
                next_sub = SQLloadNextSelfApproverSubmission(submission_id, reviewer_id)
                PrintNextSubmissionLink(next_sub)
                return
        # If the reviewer is a moderator, display the next submission by a non-self-approver
        next_sub = SQLloadNextSubmission(submission_id, reviewer_id)
        PrintNextSubmissionLink(next_sub)
        print(ISFDBLink('mod/list.cgi', 'N', 'Submission List', False, 'class="approval"'))

def PrintNextSubmissionLink(next_sub):
        if not next_sub:
                return
        subtype = next_sub[SUB_TYPE]
        if SUBMAP.has_key(subtype):
                print(ISFDBLink('mod/submission_review.cgi', next_sub[SUB_ID], 'Next Submission', False, 'class="approval"'))

        
########################################################################
#                      T I T L E   F I E L D S
########################################################################
def createNewTitle(title):
        query = "insert into titles(title_title) values('%s');" % (db.escape_string(title))
        print("<li> ", query)
        if debug == 0:
                db.query(query)
        Record = db.insert_id()
        return(Record)

def setTitleName(record, title):
        update = 'update titles set title_title="%s" where title_id=%d' % (db.escape_string(title), int(record))
        print("<li>", update)
        if debug == 0:
                db.query(update)

def setTitleDate(record, date):
        update = 'update titles set title_copyright="%s" where title_id=%d' % (db.escape_string(date), int(record))
        print("<li>", update)
        if debug == 0:
                db.query(update)

def setTitleType(record, type):
        update = 'update titles set title_ttype="%s" where title_id=%d' % (db.escape_string(type), int(record))
        print("<li>", update)
        if debug == 0:
                db.query(update)

def setTitleLength(record, length):
        if not length:
                update = 'update titles set title_storylen=NULL where title_id=%d' % int(record)
        else:
                update = 'update titles set title_storylen="%s" where title_id=%d' % (db.escape_string(length), int(record))
        print("<li>", update)
        if debug == 0:
                db.query(update)

def setTitlePage(record, page, pub_id):
        query = "select * from pub_content where pub_id=%d and title_id=%d;" % (int(pub_id), int(record))
        db.query(query)
        result = db.store_result()
        if result.num_rows() == 0:
                update = "insert into pub_content(pub_id, title_id, pubc_page) values(%d, %d, '%s');" % (int(pub_id), int(record), db.escape_string(page))
        elif page == '':
                update = "update pub_content set pubc_page=NULL where title_id=%d and pub_id=%d" % (int(record), int(pub_id))
        else:
                update = "update pub_content set pubc_page='%s' where title_id=%d and pub_id=%d" % (db.escape_string(page), int(record), int(pub_id))
        print("<li>", update)
        if debug == 0:
                db.query(update)

def setTitleLang(record, referral_lang):
        # Only update the language field if the language code is not None
        if not referral_lang:
                return
        update = 'update titles set title_language=%d where title_id=%d' % (int(referral_lang), int(record))
        print("<li>", update)
        if debug == 0:
                db.query(update)

########################################################################
#                      T I T L E   A U T H O R
########################################################################

def addTitleAuthor(author, title_id, status):
        if not author:
                return

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
        #          title_authors
        ##############################################
        if status == 'CANONICAL':
                ca_status = 1
        elif status == 'INTERVIEWEE':
                ca_status = 2
        elif status == 'REVIEWEE':
                ca_status = 3
        insert = "insert into canonical_author(title_id, author_id, ca_status) values('%d', '%d', '%d');" % (int(title_id), author_id, ca_status)
        print("<li> ", insert)
        if debug == 0:
                db.query(insert)

def update_directory(lastname):
        lastname = string.replace(lastname, '.', '')
        lastname = string.replace(lastname, ',', '')
        lastname = string.replace(lastname, '"', '')
        #lastname = string.replace(lastname, "'", '')
        lastname = string.replace(lastname, "(", '')
        lastname = string.replace(lastname, ")", '')
        lastname = string.replace(lastname, " ", '')
        section  = lastname[0:2]

        # Bullet proofing section - Make sure section is in the range Aa-Zz
        if len(section) != 2:
                return

        if section[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                return

        # Allow an apostrophe in the second place
        if section[1] not in "abcdefghijklmnopqrstuvwxyz'":
                return

        if section[1] == "'":
                query = 'select COUNT(author_lastname) from authors where author_lastname like "%s\'%%" order by author_lastname, author_canonical' % (section[0:1])
        else:
                query = 'select COUNT(author_lastname) from authors where author_lastname like "%s%%" order by author_lastname, author_canonical' % (section[0:2])
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()

        count = int(record[0][0])
        print("<li> count %d for section [%s]" % (count, section))

        query = "select directory_mask from directory where directory_index='%s'" % (section[0])
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        bitmap = record[0][0]
        print("<li> Old bitmap: %08x" % bitmap)
        bitmask = 1
        for x in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'"]:
                if x == section[1]:
                        if count == 0:
                                bitmap &= ~bitmask
                        else:
                                bitmap |= bitmask
                        print("<li> New bitmap: %08x" % bitmap)
                        query = "update directory set directory_mask='%d' where directory_index='%s'" % (bitmap, section[0])
                        print("<li> ", query)
                        db.query(query)
                        return
                else:
                        bitmask = bitmask<<1

def deleteFromAuthorTable(author_id):
        query = "select author_lastname from authors where author_id='%d'" % int(author_id)
        db.query(query)
        result = db.store_result()
        if result.num_rows():
                record = result.fetch_row()
                author_lastname = str(record[0][0])
                print("<li>LASTNAME: [%s]" % author_lastname)
        else:
                return

        query = "delete from authors where author_id='%d'" % (int(author_id))
        print("<li> ", query)
        if debug == 0:
                db.query(query)

        #Delete this author from the Pseudonym table where the author is the parent
        query = "delete from pseudonyms where author_id='%d'" % (int(author_id))
        print("<li> ", query)
        if debug == 0:
                db.query(query)

        #Delete this author from the Pseudonym table where the author is the alternate name
        query = "delete from pseudonyms where pseudonym='%d'" % (int(author_id))
        print("<li> ", query)
        if debug == 0:
                db.query(query)

        #Delete author's webpages
        query = "delete from webpages where author_id='%d'" % (int(author_id))
        print("<li> ", query)
        if debug == 0:
                db.query(query)

        #Delete author's emails
        query = "delete from emails where author_id='%d'" % (int(author_id))
        print("<li> ", query)
        if debug == 0:
                db.query(query)

        #Delete author's transliterated legal names
        query = "delete from trans_legal_names where author_id='%d'" % (int(author_id))
        print("<li> ", query)
        if debug == 0:
                db.query(query)

        #Delete author's transliterated canonical names
        query = "delete from trans_authors where author_id=%d" % (int(author_id))
        print("<li> ", query)
        if debug == 0:
                db.query(query)

        #Delete author's views
        query = "delete from author_views where author_id=%d" % (int(author_id))
        print("<li> ", query)
        if debug == 0:
                db.query(query)

        update_directory(author_lastname)

def deleteTitleAuthor(author, title_id, status):

        if status == 'CANONICAL':
                ca_status = 1
        elif status == 'INTERVIEWEE':
                ca_status = 2
        elif status == 'REVIEWEE':
                ca_status = 3

        ##############################################
        # STEP 1 - Get the author_id for this name
        ##############################################
        query = "select author_id from authors where author_canonical='%s'" % (db.escape_string(author))
        db.query(query)
        result = db.store_result()
        if result.num_rows():
                record = result.fetch_row()
                author_id = record[0][0]
        else:
                return

        ##############################################
        # STEP 2 - Delete the author entry for this
        #          title from canonical_author
        ##############################################
        query = "delete from canonical_author where author_id='%d' and title_id='%d' and ca_status='%d'" % (int(author_id), int(title_id), int(ca_status))
        print("<li> ", query)
        if debug == 0:
                db.query(query)

        ##############################################
        # STEP 3 - If the author still has an entry
        #          in any of the mapping tables, done.
        ##############################################
        for i in ['canonical_author', 'pub_authors']:
                query = 'select COUNT(author_id) from %s where author_id=%d' % (i, author_id)
                print("<li> ", query)
                db.query(query)
                res = db.store_result()
                record = res.fetch_row()
                if record[0][0]:
                        return

        ##############################################
        # STEP 4 - If no one references the author,
        #          delete it.
        ##############################################
        deleteFromAuthorTable(author_id)


def setTitleAuthors(Record, NewAuthors):
        OldAuthors = SQLTitleAuthors(int(Record))
        for author in OldAuthors:
                if author not in NewAuthors:
                        deleteTitleAuthor(author, Record, 'CANONICAL')
        for author in NewAuthors:
                if author not in OldAuthors:
                        addTitleAuthor(author, Record, 'CANONICAL')

def setReviewees(Record, NewReviewees):
        OldReviewees = SQLReviewAuthors(int(Record))
        for author in OldReviewees:
                if author not in NewReviewees:
                        deleteTitleAuthor(author, Record, 'REVIEWEE')
        for author in NewReviewees:
                if author not in OldReviewees:
                        addTitleAuthor(author, Record, 'REVIEWEE')

def setInterviewees(Record, NewInterviewees):
        OldInterviewees = SQLInterviewAuthors(int(Record))
        for author in OldInterviewees:
                if author not in NewInterviewees:
                        deleteTitleAuthor(author, Record, 'INTERVIEWEE')
        for author in NewInterviewees:
                if author not in OldInterviewees:
                        addTitleAuthor(author, Record, 'INTERVIEWEE')

########################################################################
#                    A U T H O R   T A B L E
########################################################################

def insertAuthorCanonical(author):

        # STEP 1: Insert the author into the author table
        insert = "insert into authors(author_canonical) values('%s');" % db.escape_string(author)
        print("<li> ", insert)
        if debug == 0:
                db.query(insert)
        author_id = db.insert_id()

        # STEP 2: Make a first pass at calculating the author's lastname
        #
        # Step 2.1: Remove everything to the right of the first parenthesis since it's a disambiguator.
        #       The only exception is when the first parenthesis is also the first character in the name
        first_parent = author.find('(')
        if first_parent > 0:
                author = author[0:first_parent]
                author = string.strip(author)
        # Step 2.2: Get the last space-delimited segment of the author's name
        fields = string.split(author, " ")
        lastname = fields[-1]
        # If the last segment is a recognized suffix like 'Jr.' or 'III', skip it and get the previous segment
        if len(fields) > 1 and lastname in SESSION.recognized_suffixes:
                lastname = fields[-2]
        # Strip trailing comma
        if lastname[-1] == ',':
                lastname = lastname[0:-1]
        update = "update authors set author_lastname='%s' where author_id='%d'" %  (db.escape_string(lastname), author_id)
        print("<li> ", update)
        if debug == 0:
                db.query(update)

        # STEP 3: Update the directory bitmap
        update_directory(lastname)

        return author_id


########################################################################
#                          H I S T O R Y
########################################################################

doHistory = 1

def setHistory(table, record, field, submission, submitter, orig, to):

        (reviewer, xxx, yyy) = GetUserData()

        table      = int(table)
        record     = int(record)
        field      = int(field)
        submission = int(submission)
        submitter  = int(submitter)
        reviewer   = int(reviewer)

        if orig:
                orig       = db.escape_string(orig)
        else:
                orig = 'NULL'
        if to:
                to         = db.escape_string(to)
        else:
                to = 'NULL'

        insert = "insert into history(history_time, history_table, history_record, history_field, history_submission, history_submitter, history_reviewer, history_from, history_to) values(NOW(), %d, %d, %d, %d, %d, %d,'%s', '%s');" % (table, record, field, submission, submitter, reviewer, orig, to)
        if (debug == 0) and (doHistory == 1):
                db.query(insert)

def display_sources(submission_id):
        xml = SQLloadXML(submission_id)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('NewPub')

        isbn = GetElementValue(merge, 'Isbn')
        format = GetElementValue(merge, 'Binding')

        if not isbn:
                return
        
        if not ISBNValidFormat(isbn):
                return

        # Retrieve all Web sites that ISFDB knows about
        websites = SQLLoadWebSites(isbn, None, format)
        print('<b>Additional sources:</b> ')
        print('<ul>')
        for website in websites:
                print('<li><a href="%s" target="_blank">%s</a>' % (website[1], website[0]))
        print('</ul>')

class Submission:
        def __init__(self, queue, submission_id):
                self.queue = queue
                self.submission_id = submission_id

                self.css = ''
                self.holder_id = 0
                self.lang = ''
                self.pub_id = ''
                self.submission_type = ''
                self.subject = ''
                self.submitter_id = 0
                self.submitter_name = ''
                self.sub_time = ''
                self.sub_type_id = ''

        def parse(self, record):
                self.sub_type_id = record[SUB_TYPE]
                self.submission_type = SUBMAP[self.sub_type_id][1]
                self.holder_id = record[SUB_HOLDID]
                self.submitter_id = record[SUB_SUBMITTER]
                self.sub_time = record[SUB_TIME]

                # Extract subject, submitter name and submission type from the XML payload
                try:
                        doc = minidom.parseString(XMLunescape2(record[SUB_DATA]))
                        doc2 = doc.getElementsByTagName(self.submission_type)
                        self.subject = XMLunescape(GetElementValue(doc2, 'Subject'))
                        self.submitter_name = GetElementValue(doc2, 'Submitter')
                        # Determine the actual submission type by parsing the XML payload
                        self.submission_type = ISFDBSubmissionType(self.submission_type, self.sub_type_id, doc2)
                        if self.submission_type == 'NewPub':
                                self.lang = GetElementValue(doc2, 'Language')
                        elif self.submission_type == 'PubUpdate':
                                self.pub_id = int(GetElementValue(doc2, 'Record'))
                except:
                        self.subject = 'XML PARSE ERROR'
                        self.submitter_name = SQLgetUserName(self.submitter_id)

        def print_submission(self):
                record = self.queue.submissions[self.submission_id]
                if self.queue.color:
                        print('<tr align=left class="table1">')
                else:
                        print('<tr align=left class="table2">')
               
                print('<td%s>%s</td>' % (self.queue.css[self.submitter_name],
                                         ISFDBLink("mod/submission_review.cgi", self.submission_id, self.submission_id)))
                if self.holder_id in self.queue.holder_ids:
                        print('<td>%s</td>' % WikiLink(self.queue.holder_ids[self.holder_id]))
                else:
                        print('<td>&nbsp;</td>')
                print('<td>%s</td>' % self.submission_type)
                print('<td>%s</td>' % self.sub_time)
                if not self.queue.single_submitter_id:
                        single_submitter_link = self.queue.single_submitter_link(self.submitter_name)
                else:
                        single_submitter_link = ''
                print('<td>%s%s</td>' % (WikiLink(self.submitter_name), single_submitter_link))
                print('<td>%s</td>' % ISFDBText(self.subject))
                print('</tr>')

class Queue:
        def __init__(self):
                self.arg = ''
                self.bot_users = {}
                self.changed_verified_pubs = []
                self.color = 0
                self.css = {}
                self.held_submissions = {}
                self.holder_ids = {}
                self.lang_totals = {}
                self.lang_held = {}
                self.language_name = ''
                self.moderators = {}
                self.result = ''
                self.self_approvers = {}
                self.single_submitter_id = ''
                self.submission_id = 0
                self.submissions = {}
                self.submitter_counts = {}
                self.submitter_ids = []
                self.submitter_names = {}
                self.wiki_edits = {}

                user_data = GetUserData()
                self.reviewer = int(user_data[0])

        def parse_arguments(self):
                self.arg = SESSION.Parameter(0, 'str', None, ('N', ))

        def display_headers(self):
                from isfdblib import PrintPreMod, PrintNavBar
                PrintPreMod('New Submissions')
                PrintNavBar()
                self.display_help()

        def display_help(self):
                print('<div id="HelpBox">')
                print('<b>Help on moderating: </b>')
                print('<a href="%s://%s/index.php/Help:Screen:Moderator">Help:Screen:Moderator</a><p>' % (PROTOCOL, WIKILOC))
                print('</div>')
                ISFDBprintTime()

        def retrieve_submissions(self):
                from isfdblib import PrintPostMod
                query = """select * from submissions where sub_state='%s'""" % db.escape_string(self.arg)
                if self.single_submitter_id:
                        query += " and sub_submitter = %d" % self.single_submitter_id
                elif self.language_name:
                        query += " and sub_type = %d and sub_data like '%%<Language>%s</Language>%%'" % (MOD_PUB_NEW, db.escape_string(self.language_name))
                query += ' order by sub_reviewed, sub_id'
                db.query(query)
                self.result = db.store_result()
                if self.result.num_rows() == 0:
                        print('<h3>No submissions present</h3>')
                        PrintPostMod()
                        sys.exit(0)

        def parse_submissions(self):
                record = self.result.fetch_row()
                while record:
                        submission_id = int(record[0][SUB_ID])
                        submission = Submission(self, submission_id)
                        submission.parse(record[0])
                        self.submissions[submission_id] = submission
                        record = self.result.fetch_row()

        def build_user_and_sub_lists(self):
                pub_edits = {}
                for submission_id in self.submissions.keys():
                        submission = self.submissions[submission_id]
                        self.submitter_counts[submission.submitter_name] = self.submitter_counts.get(submission.submitter_name, 0) + 1
                        if self.reviewer != submission.submitter_id and submission.pub_id:
                                if submission.pub_id not in pub_edits:
                                        pub_edits[submission.pub_id] = []
                                pub_edits[submission.pub_id].append(submission_id)
                        if submission.lang:
                                self.lang_totals[submission.lang] = self.lang_totals.get(submission.lang, 0) + 1
                                if submission.holder_id:
                                        self.lang_held[submission.lang] = self.lang_held.get(submission.lang, 0) + 1
                        self.submitter_names[submission.submitter_name] = submission.submitter_id
                        if submission.holder_id:
                                self.held_submissions[submission.submitter_name] = self.held_submissions.get(submission.submitter_name, 0) + 1
                        if submission.submitter_id not in self.submitter_ids:
                                self.submitter_ids.append(submission.submitter_id)
                        if submission.holder_id and submission.holder_id not in self.holder_ids:
                                self.holder_ids[submission.holder_id] = ''

                # Get PubUpdate submissions which will change the viewing moderator's pubs
                if pub_edits:
                        query = """select distinct pub_id from primary_verifications
                                where pub_id in (%s)
                                and user_id = %d""" % (dict_to_in_clause(pub_edits), self.reviewer)
                        db.query(query)
                        result = db.store_result()
                        record = result.fetch_row()
                        while record:
                                pub_id = record[0][0]
                                for submission_id in pub_edits[pub_id]:
                                        self.changed_verified_pubs.append(submission_id)
                                record = result.fetch_row()

        def get_wiki_edit_counts(self):
                edit_counts = SQLWikiEditCountsForIDs(self.submitter_ids)
                for count_data in edit_counts:
                        editor_id = count_data[0]
                        edit_count = count_data[1]
                        self.wiki_edits[editor_id] = edit_count

        def get_holder_names(self):
                holders_data = SQLgetUserNamesForDict(self.holder_ids)
                for holder in holders_data:
                        holder_id = holder[0]
                        holder_name = holder[1]
                        self.holder_ids[holder_id] = holder_name

        def get_bot_users(self):
                bot_users = SQLGetUserBotFlagsForList(self.submitter_ids)
                for bot_user in bot_users:
                        user_id = bot_users[0]
                        self.bot_users[user_id] = ''

        def get_moderator_users(self):
                moderators = SQLModeratorFlagsForUserList(self.submitter_ids)
                for moderator in moderators:
                        user_id = moderator[0]
                        self.moderators[user_id] = ''
        
        def get_self_approvers(self):
                self_approvers_list = SQLGetSelfApprovers()
                for self_approver in self_approvers_list:
                        self_approver_id = self_approver[0]
                        self.self_approvers[self_approver_id] = ''

        def determine_css_class(self):
                for submitter_name in self.submitter_names:
                        submitter_id = self.submitter_names[submitter_name]
                        css = ''
                        # Submissions by self-approvers appear as cyan/aqua
                        if submitter_id in self.self_approvers:
                                css = 'submissionselfapprover'
                        # Submissions by the reviewing moderator appear in blue
                        elif submitter_id == self.reviewer:
                                css = 'submissionown'
                        # Submissions by other moderators appear in yellow
                        elif submitter_id in self.moderators:
                                css = 'submissionmoderator'
                        # Submissions by users with fewer than SESSION.new_editor_threshold Wiki edits appear in green
                        elif ((submitter_id not in self.bot_users) and
                              (self.wiki_edits[submitter_id] < SESSION.new_editor_threshold)):
                                css = 'submissionnewbie'
                        if css:
                                css = ' class="%s"' % css
                        self.css[submitter_name] = css

        def display_table_header(self, header):
                print('<h3>%s</h3>' % header)
                print('<table class="review">')
                print('<tr>')
                print('<th>Submission</th>')
                print('<th>Held By</th>')
                print('<th>Type</th>')
                print('<th>Date/Time</th>')
                print('<th>Submitter</th>')
                print('<th>Subject</th>')
                print('</tr>')

        def display_table_body(self):
                for submission_id in sorted(self.submissions.keys()):
                        submission = self.submissions[submission_id]
                        submission.print_submission()
                        self.color = self.color ^ 1
                print('</table>')

        def display_changed_verified_body(self):
                for submission_id in sorted(self.changed_verified_pubs):
                        submission = self.submissions[submission_id]
                        submission.print_submission()
                        self.color = self.color ^ 1
                print('</table>')

        def display_table_footers(self):
                print('<br>')
                print('Background colors:<br>')
                print('<ul>')
                print('<li>Your submissions: blue')
                print('<li>Submissions by other moderators: yellow')
                print('<li>Submissions by editors with fewer than %d Wiki comments: green' % SESSION.new_editor_threshold)
                print('<li>Submissions by self-approvers: cyan')
                print('</ul>')

        def single_submitter_link(self, submitter_name):
                return ISFDBLinkNoName('mod/submission_search_results.cgi',
                                       'submitter_name=%s&amp;status=Pending' % submitter_name,
                                       ' [all]')

        def display_submitter_breakdown(self):
                if not self.submitter_counts:
                        return
                self.display_breakdown_header('Submitter')
                color = 0
                combined_total = 0
                combined_held = 0
                combined_unheld = 0
                for submitter_name in sorted(self.submitter_counts.keys()):
                        total = self.submitter_counts[submitter_name]
                        combined_total += total
                        held = self.held_submissions.get(submitter_name, 0)
                        combined_held += held
                        unheld = total - held
                        combined_unheld += unheld
                        self.display_breakdown_row(color)
                        print('<td%s>%s %s</td>' % (self.css[submitter_name],
                                                    WikiLink(submitter_name),
                                                    self.single_submitter_link(submitter_name)))
                        self.display_breakdown_values(unheld, held, total)
                        color ^= 1
                self.display_breakdown_footer(combined_unheld, combined_held, combined_total)

        def display_lang_breakdown(self):
                if not self.lang_totals:
                        return
                self.display_breakdown_header('NewPub Language')
                color = 0
                combined_total = 0
                combined_held = 0
                combined_unheld = 0
                for lang_name in sorted(self.lang_totals.keys()):
                        total = self.lang_totals[lang_name]
                        combined_total += total
                        held = self.lang_held.get(lang_name, 0)
                        combined_held += held
                        unheld = total - held
                        combined_unheld += unheld
                        self.display_breakdown_row(color)
                        link = ISFDBLink('mod/submissions_by_language.cgi', 'language=%s' % lang_name, lang_name)
                        print('<td>%s</td>' % link)
                        self.display_breakdown_values(unheld, held, total)
                        color ^= 1
                self.display_breakdown_footer(combined_unheld, combined_held, combined_total)

        def display_breakdown_header(self, breakdown_type):
                print('<table class="review">')
                print('<tr>')
                print('<th>%s</th>' % breakdown_type)
                print('<th>Unheld</th>')
                print('<th>Held</th>')
                print('<th>Total</th>')
                print('</tr>')

        def display_breakdown_row(self, color):
                if color:
                        print('<tr align=left class="table1">')
                else:
                        print('<tr align=left class="table2">')

        def display_breakdown_values(self, unheld, held, total):
                print('<td>%d</td>' % unheld)
                print('<td>%d</td>' % held)
                print('<td>%d</td>' % total)
                print('</tr>')

        def display_breakdown_footer(self, combined_unheld, combined_held, combined_total):
                print('<tr>')
                print('<td><b>Total</b></td>')
                print('<td><b>%d</b></td>' % combined_unheld)
                print('<td><b>%d</b></td>' % combined_held)
                print('<td><b>%d</b></td>' % combined_total)
                print('</tr>')
                print('</table>')
                print('<p>')

        def display_breakdowns(self):
                if not self.submitter_counts and not self.lang_totals:
                        return
                print('<h3>Counts of pending submissions by submitter and language</h3>')
                print('<table>')
                print('<tr>')
                print('<td class="submissionbreakdowns">')
                self.display_submitter_breakdown()
                print('</td>')
                print('<td class="submissionbreakdowns">')
                self.display_lang_breakdown()
                print('</td>')
                print('</tr>')
                print('</table>')

        def get_submissions_and_users(self):
                self.retrieve_submissions()
                self.parse_submissions()
                self.build_user_and_sub_lists()
                self.get_self_approvers()
                self.get_wiki_edit_counts()
                self.get_bot_users()
                self.get_holder_names()
                self.get_moderator_users()
                self.determine_css_class()

        def display_verified_changes_table(self):
                if self.changed_verified_pubs:
                        self.display_table_header('Pending submissions which will change my primary verified publications')
                        self.display_changed_verified_body()

        def display_table(self):
                self.display_table_header('All pending submissions')
                self.display_table_body()
                self.display_table_footers()

        def display_pending_for_editor(self, submitter_id):
                self.arg = 'N'
                self.single_submitter_id = submitter_id
                self.display_help()
                self.get_submissions_and_users()
                self.display_table()

        def display_pending_for_language(self, language_name):
                self.arg = 'N'
                self.language_name = language_name
                self.display_help()
                self.get_submissions_and_users()
                self.display_table()

        def display_queue(self):
                self.parse_arguments()
                self.display_headers()
                self.get_submissions_and_users()
                self.display_verified_changes_table()
                self.display_breakdowns()
                self.display_table()
