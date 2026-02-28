#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2026   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 717 $
#     Date: $Date: 2021-08-28 11:04:26 -0400 (Sat, 28 Aug 2021) $

import sys
if sys.version_info.major == 3:
        PYTHONVER = "python3"
elif sys.version_info.major == 2:
        PYTHONVER = "python2"

from xml.dom import minidom
from SQLparsing import *
from authorClass import *
import unittest

#
# This test suite was create to provide some coverage for the Python2 to
# Python3 upgrade. The purpose is to drive the interpreter through the
# main code line to help find any required API changes or deprecations.
#
# These tests are not intended to exhaustively test all of a
# function's operational requirements.
#

##############################################################
# UNTESTED Methods
##############################################################
# cgi2obj       - requires input from cgi

def printClass(auth):
        print("DB                        =", auth.db)
        print("used_id                   =", auth.used_id)
        print("used_canonical            =", auth.used_canonical)
        print("used_trans_names          =", auth.used_trans_names)
        print("used_legalname            =", auth.used_legalname)
        print("used_lastname             =", auth.used_lastname)
        print("used_trans_legal_names    =", auth.used_trans_legal_names)
        print("used_birthplace           =", auth.used_birthplace)
        print("used_birthdate            =", auth.used_birthdate)
        print("used_deathdate            =", auth.used_deathdate)
        print("used_emails               =", auth.used_emails)
        print("used_webpages             =", auth.used_webpages)
        print("used_image                =", auth.used_image)
        print("used_language             =", auth.used_language)
        print("used_note                 =", auth.used_note)
        print("author_canonical          =", auth.author_canonical)
        print("author_trans_names        =", auth.author_trans_names)
        print("author_legalname          =", auth.author_legalname)
        print("author_lastname           =", auth.author_lastname)
        print("author_trans_legal_names  =", auth.author_trans_legal_names)
        print("author_birthplace         =", auth.author_birthplace)
        print("author_birthdate          =", auth.author_birthdate)
        print("author_deathdate          =", auth.author_deathdate)
        print("author_emails             =", auth.author_emails)
        print("author_webpages           =", auth.author_webpages)
        print("author_image              =", auth.author_image)
        print("author_language           =", auth.author_language)
        print("author_note               =", auth.author_note)
        print("error                     =", auth.error)

class MyTestCase(unittest.TestCase):

        def test_01_load(self):
                print("\nTEST: authors.load")
                auth = authors(db)
                auth.load(70)    # Stephen King
                print_values = 0
                if print_values:
                        printClass(auth)
                else:
                        self.assertEqual(1, auth.used_id, "Bad used_id")
                        self.assertEqual(1, auth.used_canonical, "Bad used_canonical")
                        self.assertEqual(1, auth.used_lastname, "Bad used_lastname")
                        self.assertEqual(1, auth.used_birthdate, "Bad used_birthdate")
                        self.assertEqual(1, auth.used_language, "Bad used_language")

                        print("  Received canonical name:", auth.author_canonical)
                        self.assertEqual('Stephen King', auth.author_canonical, "Bad canonical name")

                        print("  Received lastname:", auth.author_lastname)
                        self.assertEqual('King', auth.author_lastname, "Bad lastname")

                        print("  Received birthdate:", auth.author_birthdate)
                        self.assertEqual('1947-09-21', auth.author_birthdate, "Bad birthdate")

                        print("  Received language:", auth.author_language)
                        self.assertEqual('English', auth.author_language, "Bad language")

                        print("  Received error:", auth.error)
                        self.assertEqual('', auth.error, "Unexpected error")

        def test_02_load_not_found(self):
                print("\nTEST: authors.load - author not found")
                auth = authors(db)
                auth.load(0)    # Non-existent author ID
                print("  Received error:", auth.error)
                expected = 'Author record not found'
                self.assertEqual(expected, auth.error, "Bad error message")

        def test_03_obj2xml(self):
                print("\nTEST: authors.obj2xml")
                auth = authors(db)
                auth.load(70)    # Stephen King
                xml = auth.obj2xml()
                print("  Received XML:\n", xml)
                self.assertIn('<UpdateAuthor>', xml, "Missing UpdateAuthor tag")
                self.assertIn('<AuthorId>70</AuthorId>', xml, "Missing AuthorId tag")
                self.assertIn('<AuthorCanonical>Stephen King</AuthorCanonical>', xml, "Missing AuthorCanonical tag")
                self.assertIn('<AuthorLastname>King</AuthorLastname>', xml, "Missing AuthorLastname tag")
                self.assertIn('</UpdateAuthor>', xml, "Missing closing UpdateAuthor tag")

        def test_04_obj2xml_no_id(self):
                print("\nTEST: authors.obj2xml - no id set")
                auth = authors(db)
                # Do not call load() - used_id remains 0
                xml = auth.obj2xml()
                print("  Received XML:", repr(xml))
                expected = ""
                self.assertEqual(expected, xml, "Expected empty string when no ID set")

        def test_05_xml2obj(self):
                print("\nTEST: authors.xml2obj")
                auth = authors(db)
                xml = """<?xml version="1.0" encoding="UTF-8"?>
                         <UpdateAuthor>
                             <AuthorCanonical>Test Author</AuthorCanonical>
                             <AuthorLastname>Author</AuthorLastname>
                             <AuthorLegalname>Test Legal Author</AuthorLegalname>
                             <AuthorBirthplace>Springfield</AuthorBirthplace>
                             <AuthorBirthdate>1970-01-01</AuthorBirthdate>
                             <AuthorDeathdate>2020-06-15</AuthorDeathdate>
                             <AuthorImage>http://www.example.com/image.jpg</AuthorImage>
                             <AuthorLanguage>English</AuthorLanguage>
                         </UpdateAuthor>"""
                auth.xml2obj(xml)

                print("  Received canonical name:", auth.author_canonical)
                self.assertEqual('Test Author', auth.author_canonical, "Bad canonical name")
                self.assertEqual(1, auth.used_canonical, "Bad used_canonical flag")

                print("  Received lastname:", auth.author_lastname)
                self.assertEqual('Author', auth.author_lastname, "Bad lastname")
                self.assertEqual(1, auth.used_lastname, "Bad used_lastname flag")

                print("  Received legalname:", auth.author_legalname)
                self.assertEqual('Test Legal Author', auth.author_legalname, "Bad legalname")
                self.assertEqual(1, auth.used_legalname, "Bad used_legalname flag")

                print("  Received birthplace:", auth.author_birthplace)
                self.assertEqual('Springfield', auth.author_birthplace, "Bad birthplace")
                self.assertEqual(1, auth.used_birthplace, "Bad used_birthplace flag")

                print("  Received birthdate:", auth.author_birthdate)
                self.assertEqual('1970-01-01', auth.author_birthdate, "Bad birthdate")
                self.assertEqual(1, auth.used_birthdate, "Bad used_birthdate flag")

                print("  Received deathdate:", auth.author_deathdate)
                self.assertEqual('2020-06-15', auth.author_deathdate, "Bad deathdate")
                self.assertEqual(1, auth.used_deathdate, "Bad used_deathdate flag")

                print("  Received image:", auth.author_image)
                self.assertEqual('http://www.example.com/image.jpg', auth.author_image, "Bad image")
                self.assertEqual(1, auth.used_image, "Bad used_image flag")

                print("  Received language:", auth.author_language)
                self.assertEqual('English', auth.author_language, "Bad language")
                self.assertEqual(1, auth.used_language, "Bad used_language flag")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
