#!_PYTHONLOC
#
#     (C) COPYRIGHT 2025    Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 717 $
#     Date: $Date: 2021-08-28 11:04:26 -0400 (Sat, 28 Aug 2021) $


from SQLparsing import *
from authorClass import authors
from xml.dom import minidom
from xml.dom import Node
import unittest

#####################################################################################
# Test for authorClass.py. This indirectly tests the following SQLparsing methods:
#
# SQLgetAuthorData
# SQLisUserModerator
# SQLLoadAllLanguages
# SQLloadAuthorData
# SQLloadEmails
# SQLloadTransAuthorNames
# SQLloadTransLegalNames
# SQLloadWebpages
# SQLUpdateQueries
#
#####################################################################################

def TryPrint(label, value):
        try:
                print("%s %s" % (label, value))
        except:
                pass

INT_TYPE  = "<class 'int'>"
STR_TYPE  = "<class 'str'>"
DICT_TYPE = "<class 'dict'>"
NONE_TYPE = "<class 'NoneType'>"
LIST_TYPE = "<class 'list'>"
TUPLE_TYPE = "<class 'tuple'>"

debug = 0

def printAuthorRecord(author):
        print("-------------------------------------------------")
        TryPrint("CANONICAL       =", author.author_canonical)
        TryPrint("LEGALNAME       =", author.author_legalname)
        TryPrint("BIRTHPLACE      =", author.author_birthplace)
        TryPrint("BIRTHDATE       =", author.author_birthdate)
        TryPrint("DEATHDATE       =", author.author_deathdate)
        TryPrint("LEGALNAME       =", author.author_legalname)
        TryPrint("IMAGE           =", author.author_image)
        TryPrint("LASTNAME        =", author.author_lastname)
        TryPrint("LANGUAGE        =", author.author_language)
        TryPrint("NOTE_ID         =", author.author_note)
        # Lists
        print("TRANS NAMES:")
        for transname in author.author_trans_names:
                TryPrint("  TRANS NAME      =", transname)
        print("TRANS LEGAL NAMES:")
        for transname in author.author_trans_legal_names:
                TryPrint("  TRANS LEGAL NAME=", transname)
        print("EMAILS:")
        for email in author.author_emails:
                TryPrint("  EMAIL           =", email)
        print("WEBPAGES:")
        for webpage in author.author_webpages:
                TryPrint("  WEBPAGE         =", webpage)
        print("-------------------------------------------------")

def printAuthorRecordTypes(author):
        TryPrint("CANONICAL       =", str(type(author.author_canonical)))
        TryPrint("LEGALNAME       =", str(type(author.author_legalname)))
        TryPrint("BIRTHPLACE      =", str(type(author.author_birthplace)))
        TryPrint("BIRTHDATE       =", str(type(author.author_birthdate)))
        TryPrint("DEATHDATE       =", str(type(author.author_deathdate)))
        TryPrint("LEGALNAME       =", str(type(author.author_legalname)))
        TryPrint("IMAGE           =", str(type(author.author_image)))
        TryPrint("LASTNAME        =", str(type(author.author_lastname)))
        TryPrint("LANGUAGE        =", str(type(author.author_language)))
        TryPrint("NOTE_ID         =", str(type(author.author_note)))
        TryPrint("TRANSNAMES      =", str(type(author.author_trans_names)))
        TryPrint("TRANSLEGALNAMES =", str(type(author.author_trans_legal_names)))
        TryPrint("EMAILS          =", str(type(author.author_emails)))
        TryPrint("WEBPAGES        =", str(type(author.author_webpages)))

class TestStorage(dict):
        def __init__(self, s=None):
                self.value = s
        def getvalue(self, theKey):
                return self[theKey]

class MyTestCase(unittest.TestCase):

        def test_001_load(self):
                print("TEST: authorClass::load")
                author = authors(db)
                author.load(159)

                if debug:
                        printAuthorRecord(author)
                        printAuthorRecordTypes(author)

                self.assertEqual(author.error, '')
                self.assertEqual(STR_TYPE, str(type(author.author_canonical)))
                self.assertEqual(STR_TYPE, str(type(author.author_legalname)))
                self.assertEqual(STR_TYPE, str(type(author.author_birthplace)))
                self.assertEqual(STR_TYPE, str(type(author.author_birthdate)))
                self.assertEqual(STR_TYPE, str(type(author.author_deathdate)))
                self.assertEqual(STR_TYPE, str(type(author.author_legalname)))
                self.assertEqual(STR_TYPE, str(type(author.author_image)))
                self.assertEqual(STR_TYPE, str(type(author.author_lastname)))
                self.assertEqual(STR_TYPE, str(type(author.author_language)))
                self.assertEqual(STR_TYPE, str(type(author.author_note)))
                self.assertEqual(LIST_TYPE, str(type(author.author_trans_names)))
                self.assertEqual(LIST_TYPE, str(type(author.author_trans_legal_names)))
                self.assertEqual(LIST_TYPE, str(type(author.author_emails)))
                self.assertEqual(LIST_TYPE, str(type(author.author_webpages)))

        def test_002_obj2xml(self):
                print("TEST: authorClass::obj2xml")
                author = authors(db)
                author.load(159)

                # Convert to XML
                xml = author.obj2xml()
                if debug:
                        print(xml)

                try:
                        doc = minidom.parseString(xml)
                except:
                        print("XML Parse FAILED")

                tag = doc.getElementsByTagName('AuthorId')
                value = tag[0].firstChild.data
                self.assertEqual(value, '159')

                tag = doc.getElementsByTagName('AuthorCanonical')
                value = tag[0].firstChild.data
                self.assertEqual(value, 'Jules Verne')

                tag = doc.getElementsByTagName('AuthorLegalname')
                value = tag[0].firstChild.data
                self.assertEqual(value, 'Verne, Jules Gabriel')

                tag = doc.getElementsByTagName('AuthorLastname')
                value = tag[0].firstChild.data
                self.assertEqual(value, 'Verne')

                tag = doc.getElementsByTagName('AuthorBirthplace')
                value = tag[0].firstChild.data
                self.assertEqual(value, 'Nantes, Loire-Inférieure, France')

                tag = doc.getElementsByTagName('AuthorBirthdate')
                value = tag[0].firstChild.data
                self.assertEqual(value, '1828-02-08')

                tag = doc.getElementsByTagName('AuthorDeathdate')
                value = tag[0].firstChild.data
                self.assertEqual(value, '1905-03-24')

                tag = doc.getElementsByTagName('AuthorLanguage')
                value = tag[0].firstChild.data
                self.assertEqual(value, 'French')

                tag = doc.getElementsByTagName('AuthorImage')
                value = tag[0].firstChild.data
                self.assertEqual(value, 'http://www.isfdb.org/wiki/images/b/b6/Jules_Verne.jpg')

                try:
                        elements = doc.getElementsByTagName('AuthorWebpage')
                        for element in elements:
                                value = element.firstChild.data
                                if debug:
                                        print("AuthorWebage:", value)
                except:
                        self.assertEqual(' ', 'AuthorWebpage')

                try:
                        elements = doc.getElementsByTagName('AuthorEmail')
                        for element in elements:
                                value = element.firstChild.data
                                if debug:
                                        print("AuthorEmail:", value)
                except:
                        self.assertEqual(' ', 'AuthorEmail')


        def test_003_xml2obj_webpages(self):
                print("TEST: authorClass::xml2obj")
                author = authors(db)
                author.load(159)

                # Convert to XML
                xml = author.obj2xml()
                if debug:
                        print(xml)

                try:
                        doc = minidom.parseString(xml)
                except:
                        print("XML Parse FAILED")

                # Convert XML to OBJ
                author.xml2obj(xml)

                if debug:
                        printAuthorRecord(author)
                        printAuthorRecordTypes(author)

                self.assertEqual(STR_TYPE, str(type(author.author_canonical)))
                self.assertEqual(STR_TYPE, str(type(author.author_legalname)))
                self.assertEqual(STR_TYPE, str(type(author.author_birthplace)))
                self.assertEqual(STR_TYPE, str(type(author.author_birthdate)))
                self.assertEqual(STR_TYPE, str(type(author.author_deathdate)))
                self.assertEqual(STR_TYPE, str(type(author.author_legalname)))
                self.assertEqual(STR_TYPE, str(type(author.author_image)))
                self.assertEqual(STR_TYPE, str(type(author.author_lastname)))
                self.assertEqual(STR_TYPE, str(type(author.author_language)))
                self.assertEqual(STR_TYPE, str(type(author.author_note)))
                self.assertEqual(LIST_TYPE, str(type(author.author_trans_legal_names)))
                self.assertEqual(LIST_TYPE, str(type(author.author_trans_names)))
                self.assertEqual(LIST_TYPE, str(type(author.author_emails)))
                self.assertEqual(LIST_TYPE, str(type(author.author_webpages)))

        def test_004_xml2obj_translegal(self):
                print("TEST: authorClass::xml2obj")
                author = authors(db)
                author.load(166136)

                # Convert to XML
                xml = author.obj2xml()
                if debug:
                        print(xml)

                try:
                        doc = minidom.parseString(xml)
                except:
                        print("XML Parse FAILED")

                # Convert XML to OBJ
                author.xml2obj(xml)

                if debug:
                        printAuthorRecord(author)
                        printAuthorRecordTypes(author)

                self.assertEqual(STR_TYPE, str(type(author.author_canonical)))
                self.assertEqual(STR_TYPE, str(type(author.author_legalname)))
                self.assertEqual(STR_TYPE, str(type(author.author_birthplace)))
                self.assertEqual(STR_TYPE, str(type(author.author_birthdate)))
                self.assertEqual(STR_TYPE, str(type(author.author_deathdate)))
                self.assertEqual(STR_TYPE, str(type(author.author_legalname)))
                self.assertEqual(STR_TYPE, str(type(author.author_image)))
                self.assertEqual(STR_TYPE, str(type(author.author_lastname)))
                self.assertEqual(STR_TYPE, str(type(author.author_language)))
                self.assertEqual(STR_TYPE, str(type(author.author_note)))
                self.assertEqual(LIST_TYPE, str(type(author.author_trans_legal_names)))
                self.assertEqual(LIST_TYPE, str(type(author.author_trans_names)))
                self.assertEqual(LIST_TYPE, str(type(author.author_emails)))
                self.assertEqual(LIST_TYPE, str(type(author.author_webpages)))

        def test_005_xml2obj_email(self):
                print("TEST: authorClass::xml2obj")
                author = authors(db)
                author.load(2200)

                # Convert to XML
                xml = author.obj2xml()
                if debug:
                        print(xml)

                try:
                        doc = minidom.parseString(xml)
                except:
                        print("XML Parse FAILED")

                # Convert XML to OBJ
                author.xml2obj(xml)

                if debug:
                        printAuthorRecord(author)
                        printAuthorRecordTypes(author)

                self.assertEqual(STR_TYPE, str(type(author.author_canonical)))
                self.assertEqual(STR_TYPE, str(type(author.author_legalname)))
                self.assertEqual(STR_TYPE, str(type(author.author_birthplace)))
                self.assertEqual(STR_TYPE, str(type(author.author_birthdate)))
                self.assertEqual(STR_TYPE, str(type(author.author_deathdate)))
                self.assertEqual(STR_TYPE, str(type(author.author_legalname)))
                self.assertEqual(STR_TYPE, str(type(author.author_image)))
                self.assertEqual(STR_TYPE, str(type(author.author_lastname)))
                self.assertEqual(STR_TYPE, str(type(author.author_language)))
                self.assertEqual(STR_TYPE, str(type(author.author_note)))
                self.assertEqual(LIST_TYPE, str(type(author.author_trans_legal_names)))
                self.assertEqual(LIST_TYPE, str(type(author.author_trans_names)))
                self.assertEqual(LIST_TYPE, str(type(author.author_emails)))
                self.assertEqual(LIST_TYPE, str(type(author.author_webpages)))

        def test_006_cgi2obj(self):
                print("TEST: authorClass::cgi2obj")

                # Test 1 - Missing author ID
                form = {
                    'author_canonical': TestStorage("Dan Simmons"),
                }
                author = authors(db)
                author.cgi2obj(form)
                self.assertEqual(author.error, "Author ID not specified")

                # Test 2 - Missing canonical name
                form = {
                    'author_id': TestStorage(170),
                }
                author = authors(db)
                author.cgi2obj(form)
                self.assertEqual(author.error, "Canonical name is required")

                # Test 3 - Incorrect author ID
                form = {
                    'author_id': TestStorage(17),
                    'author_canonical': TestStorage("Dan Simmons"),
                }
                author = authors(db)
                author.cgi2obj(form)
                self.assertEqual(author.error, "Canonical name 'Dan Simmons' already exists, duplicates are not allowed")

                # Test 4 - Bad characters
                form = {
                    'author_id': TestStorage(170),
                    'author_canonical': TestStorage("Dan+Simmons"),
                }
                author = authors(db)
                author.cgi2obj(form)
                self.assertEqual(author.error, "Plus signs are currently not allowed in canonical names")

                # Test 5 - No Lastname
                form = {
                    'author_id': TestStorage(170),
                    'author_canonical': TestStorage("Dan Simmons"),
                }
                author = authors(db)
                author.cgi2obj(form)
                self.assertEqual(author.error, "Directory Entry is required")

                # Test 6 - Bad URL
                form = {
                    'author_id': TestStorage(170),
                    'author_canonical': TestStorage("Dan Simmons"),
                    'author_lastname': TestStorage("Simmons"),
                    'author_image': TestStorage("httttp://stuff.com"),
                }
                author = authors(db)
                author.cgi2obj(form)
                self.assertEqual(author.error, "Author image error:  URLs must start with http or https")

                # Test 7 - Missing Language
                form = {
                    'author_id': TestStorage(170),
                    'author_canonical': TestStorage("Dan Simmons"),
                    'author_lastname': TestStorage("Simmons"),
                }
                author = authors(db)
                author.cgi2obj(form)
                self.assertEqual(author.error, "Language is required")

                # Test 8 - Bad email
                form = {
                    'author_id': TestStorage(170),
                    'author_canonical': TestStorage("Dan Simmons"),
                    'author_language': TestStorage("English"),
                    'author_lastname': TestStorage("Simmons"),
                    'author_emails': TestStorage("simmons.com"),
                }
                author = authors(db)
                author.cgi2obj(form)
                self.assertEqual(author.error, "Invalid email address")

                # Test 9 - Bad webpage
                form = {
                    'author_id': TestStorage(170),
                    'author_canonical': TestStorage("Dan Simmons"),
                    'author_language': TestStorage("English"),
                    'author_lastname': TestStorage("Simmons"),
                    'author_webpages': TestStorage("httttp://stuff.com"),
                }
                author = authors(db)
                author.cgi2obj(form)
                self.assertEqual(author.error, "Author Web page error:  URLs must start with http or https")

                # Test 10 - Valid Entry
                form = {
                    'author_id': TestStorage(170),
                    'author_canonical': TestStorage("Dan Simmons"),
                    'author_lastname': TestStorage("Simmons"),
                    'author_language': TestStorage("English"),
                    'author_trans_names': TestStorage("Bogus"),
                    'author_legalname': TestStorage("Bogus Entry"),
                    'trans_legal_names': TestStorage("Dude Entry"),
                    'author_birthplace': TestStorage("Georgetown, Texas, USA"),
                    'author_birthdate': TestStorage("1948-09-04"),
                    'author_deathdate': TestStorage("2025-01-01"),
                    'author_emails': TestStorage("bogus@gmail.com"),
                    'author_webpages': TestStorage("http://stuff.com"),
                    'author_image': TestStorage("http://stuff.com/image.jpg"),
                }

                author = authors(db)
                author.cgi2obj(form)
                if author.error != '':
                        print("ERROR:", author.error)

                if debug:
                        printAuthorRecord(author)
                        printAuthorRecordTypes(author)

                self.assertEqual(author.error, '')
                self.assertEqual(STR_TYPE, str(type(author.author_canonical)))
                self.assertEqual(STR_TYPE, str(type(author.author_legalname)))
                self.assertEqual(STR_TYPE, str(type(author.author_birthplace)))
                self.assertEqual(STR_TYPE, str(type(author.author_birthdate)))
                self.assertEqual(STR_TYPE, str(type(author.author_deathdate)))
                self.assertEqual(STR_TYPE, str(type(author.author_legalname)))
                self.assertEqual(STR_TYPE, str(type(author.author_image)))
                self.assertEqual(STR_TYPE, str(type(author.author_lastname)))
                self.assertEqual(STR_TYPE, str(type(author.author_language)))
                self.assertEqual(STR_TYPE, str(type(author.author_note)))
                self.assertEqual(LIST_TYPE, str(type(author.author_trans_names)))
                self.assertEqual(LIST_TYPE, str(type(author.author_trans_legal_names)))
                self.assertEqual(LIST_TYPE, str(type(author.author_emails)))
                self.assertEqual(LIST_TYPE, str(type(author.author_webpages)))

        def test_100_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()

if __name__ == '__main__':
        unittest.main()
