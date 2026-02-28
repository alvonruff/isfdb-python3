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

from SQLparsing import *
from titleClass import *
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
# cgi2obj           - requires IsfdbFieldStorage / CGI input
# validateOptional  - requires self.form set by cgi2obj
# delete            - executes DELETE SQL
# deleteAuthor      - executes DELETE SQL


def printClass(t):
        print("used_id        =", t.used_id)
        print("used_title     =", t.used_title)
        print("used_year      =", t.used_year)
        print("used_ttype     =", t.used_ttype)
        print("used_series    =", t.used_series)
        print("used_language  =", t.used_language)
        print("title_id       =", t.title_id)
        print("title_title    =", t.title_title)
        print("title_year     =", t.title_year)
        print("title_ttype    =", t.title_ttype)
        print("title_series   =", t.title_series)
        print("title_language =", t.title_language)
        print("title_authors  =", t.title_authors)
        print("num_authors    =", t.num_authors)
        print("error          =", t.error)


class MyTestCase(unittest.TestCase):

        def test_01_init(self):
                print("\nTEST: titles.__init__")
                t = titles(db)
                self.assertEqual(0, t.used_id, "Bad used_id init")
                self.assertEqual(0, t.used_title, "Bad used_title init")
                self.assertEqual(0, t.used_year, "Bad used_year init")
                self.assertEqual(0, t.used_ttype, "Bad used_ttype init")
                self.assertEqual(0, t.used_series, "Bad used_series init")
                self.assertEqual(0, t.used_language, "Bad used_language init")
                self.assertEqual(0, t.num_authors, "Bad num_authors init")
                self.assertEqual([], t.title_authors, "Bad title_authors init")
                self.assertEqual([], t.title_author_tuples, "Bad title_author_tuples init")
                self.assertEqual([], t.title_trans_titles, "Bad title_trans_titles init")
                self.assertEqual([], t.title_webpages, "Bad title_webpages init")
                self.assertEqual('', t.title_id, "Bad title_id init")
                self.assertEqual('', t.title_title, "Bad title_title init")
                self.assertEqual('', t.error, "Bad error init")
                print("  Init state verified.")

        def test_02_authors(self):
                print("\nTEST: titles.authors")
                t = titles(db)

                # TEST 1 - No authors -> empty string
                value = t.authors()
                print("  Received (0 authors):", value)
                self.assertEqual('', value, "0 authors should return ''")

                # TEST 2 - One author
                t.title_authors = ['Stephen King']
                t.num_authors = 1
                value = t.authors()
                print("  Received (1 author):", value)
                self.assertIn('Stephen King', value, "Author name missing")

                # TEST 3 - Two authors: output is sorted and joined with merge sign
                t.title_authors = ['Stephen King', 'Peter Straub']
                t.num_authors = 2
                value = t.authors()
                print("  Received (2 authors):", value)
                self.assertIn('Stephen King', value, "First author missing")
                self.assertIn('Peter Straub', value, "Second author missing")
                self.assertIn('<span class="mergesign">+</span>', value, "Authors should be joined with merge sign")
                # Sorted: 'Peter Straub' < 'Stephen King', so Peter comes first
                self.assertLess(value.index('Peter Straub'), value.index('Stephen King'), "Authors should be sorted")

        def test_03_load(self):
                print("\nTEST: titles.load - by id (title 1050, The Talisman)")
                t = titles(db)
                t.load(1050)
                print_values = 1
                if print_values:
                        printClass(t)
                else:
                        self.assertEqual(1, t.used_id, "Bad used_id")
                        self.assertEqual(1, t.used_title, "Bad used_title")
                        self.assertEqual('', t.error, "Unexpected error")
                        print("  Received title:", t.title_title)
                        self.assertEqual('The Talisman', t.title_title, "Bad title_title")
                        self.assertGreater(t.num_authors, 0, "Should have at least one author")

        def test_04_load_id_zero(self):
                print("\nTEST: titles.load - id=0")
                t = titles(db)
                t.load(0)
                self.assertEqual(0, t.used_id, "load(0) should not set used_id")
                self.assertEqual('', t.title_id, "load(0) should not set title_id")
                self.assertEqual('', t.error, "load(0) should not set error")

        def test_05_load_not_found(self):
                print("\nTEST: titles.load - not found")
                t = titles(db)
                t.load(999999999)
                print("  Received error:", t.error)
                self.assertEqual('title record not found', t.error, "Bad error message")
                self.assertEqual(0, t.used_id, "used_id should remain 0")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
