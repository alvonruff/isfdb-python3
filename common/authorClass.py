from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 970 $
#     Date: $Date: 2022-08-15 12:47:52 -0400 (Mon, 15 Aug 2022) $

import cgi
import sys
import os
from isfdb import *
from isfdblib import *
from library import *
from xml.dom import minidom
from xml.dom import Node


class authors:
        def __init__(self, db):
                self.db = db
                self.used_id = 0
                self.used_canonical = 0
                self.used_trans_names = 0
                self.used_legalname = 0
                self.used_lastname = 0
                self.used_trans_legal_names = 0
                self.used_birthplace = 0
                self.used_birthdate = 0
                self.used_deathdate = 0
                self.used_emails = 0
                self.used_webpages = 0
                self.used_image = 0
                self.used_language = 0
                self.used_note = 0

                self.author_canonical = ''
                self.author_trans_names = []
                self.author_legalname = ''
                self.author_lastname = ''
                self.author_trans_legal_names = []
                self.author_birthplace = ''
                self.author_birthdate = ''
                self.author_deathdate = ''
                self.author_emails = []
                self.author_webpages = []
                self.author_image = ''
                self.author_language = ''
                self.author_note = ''

                self.error = ''

        def load(self, author_id):
                record = SQLloadAuthorData(author_id)
                if record:
                        if record[AUTHOR_ID]:
                                self.author_id = record[AUTHOR_ID]
                                self.used_id = 1
                        if record[AUTHOR_CANONICAL]:
                                self.author_canonical = record[AUTHOR_CANONICAL]
                                self.used_canonical = 1

                        res2 = SQLloadTransAuthorNames(record[AUTHOR_ID])
                        if res2:
                                self.author_trans_names = res2
                                self.used_trans_names = 1

                        if record[AUTHOR_LEGALNAME]:
                                self.author_legalname  = record[AUTHOR_LEGALNAME]
                                self.used_legalname = 1

                        res2 = SQLloadTransLegalNames(record[AUTHOR_ID])
                        if res2:
                                self.author_trans_legal_names = res2
                                self.used_trans_legal_names = 1

                        if record[AUTHOR_LASTNAME]:
                                self.author_lastname = record[AUTHOR_LASTNAME]
                                self.used_lastname = 1
                        if record[AUTHOR_BIRTHPLACE]:
                                self.author_birthplace = record[AUTHOR_BIRTHPLACE]
                                self.used_birthplace = 1
                        if record[AUTHOR_BIRTHDATE]:
                                self.author_birthdate = record[AUTHOR_BIRTHDATE]
                                self.used_birthdate = 1
                        if record[AUTHOR_DEATHDATE]:
                                self.author_deathdate = record[AUTHOR_DEATHDATE]
                                self.used_deathdate = 1
                        if record[AUTHOR_IMAGE]:
                                self.author_image = record[AUTHOR_IMAGE]
                                self.used_image = 1
                        # If a working language is defined for this author, get the name of the language
                        if record[AUTHOR_LANGUAGE]:
                                self.author_language = LANGUAGES[int(record[AUTHOR_LANGUAGE])]
                                self.used_language = 1

                        res2 = SQLloadEmails(record[AUTHOR_ID])
                        if res2:
                                self.author_emails = res2
                                self.used_emails = 1

                        res2 = SQLloadWebpages(record[AUTHOR_ID])
                        if res2:
                                self.author_webpages = res2
                                self.used_webpages = 1

                        if record[AUTHOR_NOTE]:
                                self.author_note = record[AUTHOR_NOTE]
                                self.used_note = 1

                else:
                        print("ERROR: author record not found: ", author_id)
                        self.error = 'Author record not found'
                        return

        def obj2xml(self):
                if self.used_id:
                        container = "<UpdateAuthor>\n"
                        container += "  <AuthorId>%s</AuthorId>\n" % (self.author_id)
                        if self.used_canonical:
                                container += "  <AuthorCanonical>%s</AuthorCanonical>\n" % \
                                                (self.author_canonical)

                        if self.used_trans_names:
                                container += "  <AuthorTransNames>%s</AuthorTransNames>\n" % \
                                                (self.author_trans_names)

                        if self.used_legalname:
                                container += "  <AuthorLegalname>%s</AuthorLegalname>\n" % \
                                                (self.author_legalname)

                        if self.used_trans_legal_names:
                                container += "  <AuthorTransLegalNames>%s</AuthorTransLegalNames>\n" % \
                                                (self.author_trans_legal_names)

                        if self.used_lastname:
                                container += "  <AuthorLastname>%s</AuthorLastname>\n" % \
                                                (self.author_lastname)

                        if self.used_birthplace:
                                container += "  <AuthorBirthplace>%s</AuthorBirthplace>\n" % \
                                                (self.author_birthplace)

                        if self.used_birthdate:
                                container += "  <AuthorBirthdate>%s</AuthorBirthdate>\n" % \
                                                (self.author_birthdate)

                        if self.used_deathdate:
                                container += "  <AuthorDeathdate>%s</AuthorDeathdate>\n" % \
                                                (self.author_deathdate)

                        if self.used_emails:
                                container += "  <AuthorEmails>%s</AuthorEmails>\n" % \
                                                (self.author_emails)

                        if self.used_webpages:
                                container += "  <AuthorWebpages>%s</AuthorWebpages>\n" % \
                                                (self.author_webpages)

                        if self.used_image:
                                container += "  <AuthorImage>%s</AuthorImage>\n" % \
                                                (self.author_image)

                        if self.used_language:
                                container += "  <AuthorLanguage>%s</AuthorLanguage>\n" % \
                                                (self.author_language)

                        container += "</UpdateAuthor>\n"
                else:
                        print("XML: pass")
                        container = ""
                return container

        def xml2obj(self, xml):
                doc = minidom.parseString(xml)
                metadata = doc.getElementsByTagName('UpdateAuthor')
                if metadata == 0:
                        metadata = doc.getElementsByTagName('NewAuthor')
                if metadata == 0:
                        return

                elem = GetElementValue(metadata, 'AuthorCanonical')
                if elem:
                        self.used_canonical = 1
                        self.author_canonical = elem

                elem = GetElementValue(metadata, 'AuthorTransNames')
                if elem:
                        self.used_trans_names = 1
                        self.author_trans_names = elem

                elem = GetElementValue(metadata, 'AuthorLegalname')
                if elem:
                        self.used_legalname = 1
                        self.author_legalname = elem

                elem = GetElementValue(metadata, 'AuthorTransLegalNames')
                if elem:
                        self.used_trans_legal_names = 1
                        self.author_trans_legal_names = elem

                elem = GetElementValue(metadata, 'AuthorLastname')
                if elem:
                        self.used_lastname = 1
                        self.author_lastname = elem

                elem = GetElementValue(metadata, 'AuthorBirthplace')
                if elem:
                        self.used_birthplace = 1
                        self.author_birthplace = elem

                elem = GetElementValue(metadata, 'AuthorBirthdate')
                if elem:
                        self.used_birthdate = 1
                        self.author_birthdate = elem

                elem = GetElementValue(metadata, 'AuthorDeathdate')
                if elem:
                        self.used_deathdate = 1
                        self.author_deathdate = elem

                elem = GetElementValue(metadata, 'AuthorImage')
                if elem:
                        self.used_image = 1
                        self.author_image = elem

                elem = GetElementValue(metadata, 'AuthorLanguage')
                if elem:
                        self.used_language = 1
                        self.author_language = elem

                elem = GetElementValue(metadata, 'AuthorEmails')
                if elem:
                        self.used_emails = 1
                        self.author_emails = elem

                elem = GetElementValue(metadata, 'AuthorWebpages')
                if elem:
                        self.used_webpages = 1
                        self.author_webpages = elem

        def cgi2obj(self):
                import re
                self.form = IsfdbFieldStorage()
                try:
                        self.author_id = str(int(self.form['author_id'].value))
                        self.used_id = 1
                except:
                        self.error = 'Author ID not specified'
                        return

                try:
                        self.author_canonical = XMLescape(self.form['author_canonical'].value)
                        self.used_canonical = 1
                        if not self.author_canonical:
                                raise
                except:
                        self.error = 'Canonical name is required'
                        return

                # Unescape the canonical name so that the lookup would find it in the database
                unescaped_name = XMLunescape(self.author_canonical)
                current_name = SQLgetAuthorData(unescaped_name)
                if current_name:
                        if int(self.author_id) != current_name[AUTHOR_ID]:
                                self.error = "Canonical name '%s' already exists, duplicates are not allowed" % current_name[AUTHOR_CANONICAL]
                                return
                if '"' in unescaped_name:
                        self.error = 'Double quotes are not allowed in canonical names, use single quotes instead'
                        return
                if '+' in unescaped_name:
                        self.error = 'Plus signs are currently not allowed in canonical names'
                        return

                # Limit the ability to edit canonical names to moderators
                user = User()
                user.load()
                user.load_moderator_flag()
                if not user.moderator:
                        # Retrieve the author name that is currently on file for this author
                        name_on_file = SQLloadAuthorData(self.author_id)
                        if name_on_file[AUTHOR_CANONICAL] != unescaped_name:
                                self.error = 'Only moderators can edit canonical names'
                                return

                for key in self.form:
                        if 'trans_names' in key:
                                value = XMLescape(self.form[key].value)
                                if value:
                                        self.author_trans_names.append(value)
                                        self.used_trans_names = 1

                if 'author_legalname' in self.form:
                        value = XMLescape(self.form['author_legalname'].value)
                        if value:
                                self.author_legalname = value
                                self.used_legalname = 1

                for key in self.form:
                        if 'trans_legal_names' in key:
                                value = XMLescape(self.form[key].value)
                                if value:
                                        self.author_trans_legal_names.append(value)
                                        self.used_trans_legal_names = 1

                try:
                        self.author_lastname = XMLescape(self.form['author_lastname'].value)
                        self.used_lastname = 1
                        if not self.author_lastname:
                                raise
                except:
                        self.error = 'Directory Entry is required'
                        return

                if 'author_birthplace' in self.form:
                        value = XMLescape(self.form['author_birthplace'].value)
                        if value:
                                self.author_birthplace = value
                                self.used_birthplace = 1

                if 'author_birthdate' in self.form:
                        # Handle XML escaping, strip leading and trailing spaces, normalize the date
                        value = ISFDBnormalizeDate(XMLescape(self.form['author_birthdate'].value))
                        if value:
                                self.author_birthdate = value
                                self.used_birthdate = 1

                if 'author_deathdate' in self.form:
                        # Handle XML escaping, strip leading and trailing spaces, normalize the date
                        value = ISFDBnormalizeDate(XMLescape(self.form['author_deathdate'].value))
                        if value:
                                self.author_deathdate = value
                                self.used_deathdate = 1

                if 'author_image' in self.form:
                        value = XMLescape(self.form['author_image'].value)
                        if value:
                                self.error = invalidURL(value)
                                if self.error:
                                        self.error = 'Author image error: %s' % self.error
                                        return
                                self.author_image = value
                                self.used_image = 1

                try:
                        value = XMLescape(self.form['author_language'].value)
                        if value:
                                self.author_language = value
                                self.used_language = 1
                        else:
                                raise
                except:
                        self.error = 'Language is required'
                        return

                for key in self.form:
                        if key[:13] == 'author_emails':
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.author_emails:
                                                continue
                                        if not re.match(r"[^@]+@[^@]+\.[^@]+",value):
                                                self.error = 'Invalid email address'
                                                return
                                        self.author_emails.append(value)
                                        self.used_emails = 1

                for key in self.form:
                        if key[:15] == 'author_webpages':
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.author_webpages:
                                                continue
                                        self.error = invalidURL(value)
                                        if self.error:
                                                self.error = 'Author Web page error: %s' % self.error
                                                return
                                        self.author_webpages.append(value)
                                        self.used_webpages = 1

                if 'author_note' in self.form:
                        value = XMLescape(self.form['author_note'].value)
                        if value:
                                self.author_note = value
                                self.used_note = 1
