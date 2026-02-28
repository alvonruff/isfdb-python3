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
from pubClass import *
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
# pubs.cgi2obj             - requires IsfdbFieldStorage / CGI input
# pubs.ValidatePageNumber  - requires self.form set by cgi2obj
# pubs.PrintPrimaryVerifications   - prints to stdout; requires verified pub
# pubs.PrintAllSecondaryVerifications - prints to stdout
# pubs.PrintActiveSecondaryVerifications - prints to stdout
# pubs.PrintTitleLine      - prints to stdout; requires live title record
# pubs.printExternalIDs    - prints to stdout
# pubs.printModNoteRequired - prints to stdout
# titleEntry.xmlTitle      - edit path (self.id != 0) requires self.oldtitle object
# reviewEntry.xmlTitle     - edit path requires self.oldreview object
# interviewEntry.xmlTitle  - edit path requires self.oldinterview object
# pubBody                  - prints to stdout; requires live pub record


def printClass(pub):
        print("used_id        =", pub.used_id)
        print("used_title     =", pub.used_title)
        print("used_year      =", pub.used_year)
        print("used_publisher =", pub.used_publisher)
        print("used_isbn      =", pub.used_isbn)
        print("used_ptype     =", pub.used_ptype)
        print("pub_id         =", pub.pub_id)
        print("pub_title      =", pub.pub_title)
        print("pub_year       =", pub.pub_year)
        print("pub_publisher  =", pub.pub_publisher)
        print("pub_isbn       =", pub.pub_isbn)
        print("pub_ptype      =", pub.pub_ptype)
        print("pub_authors    =", pub.pub_authors)
        print("num_authors    =", pub.num_authors)
        print("error          =", pub.error)


class MyTestCase(unittest.TestCase):

        def test_01_lastRecord(self):
                print("\nTEST: lastRecord")

                # TEST 1 - No next field exists -> last record
                form = {'title_title1': 'something'}
                value = lastRecord(form, 'title_title', 1)
                print("  Received (no next field):", value)
                self.assertEqual(1, value, "Should be last record when no next field")

                # TEST 2 - Next field exists -> not last record
                form = {'title_title1': 'first', 'title_title2': 'second'}
                value = lastRecord(form, 'title_title', 1)
                print("  Received (next field present):", value)
                self.assertEqual(0, value, "Should not be last record when next field exists")

                # TEST 3 - Counter at a high value, no next field -> last record
                form = {'title_title5': 'only'}
                value = lastRecord(form, 'title_title', 5)
                print("  Received (high counter, no next):", value)
                self.assertEqual(1, value, "Should be last record at high counter")

        def test_02_titleEntry_init(self):
                print("\nTEST: titleEntry.__init__")
                entry = titleEntry()
                self.assertEqual('', entry.page, "Bad page init")
                self.assertEqual('', entry.title, "Bad title init")
                self.assertEqual('', entry.date, "Bad date init")
                self.assertEqual('', entry.type, "Bad type init")
                self.assertEqual('', entry.length, "Bad length init")
                self.assertEqual('', entry.authors, "Bad authors init")
                self.assertEqual('', entry.next, "Bad next init")
                self.assertEqual(0, entry.id, "Bad id init")
                self.assertEqual(0, entry.oldtitle, "Bad oldtitle init")
                print("  titleEntry init state verified.")

        def test_03_titleEntry_setters(self):
                print("\nTEST: titleEntry setters")
                entry = titleEntry()

                entry.setPage('42')
                print("  page:", entry.page)
                self.assertEqual('42', entry.page, "Bad setPage")

                entry.setTitle('The Shining')
                print("  title:", entry.title)
                self.assertEqual('The Shining', entry.title, "Bad setTitle")

                # setID: positive int -> stored; 0 -> not stored
                entry.setID('100')
                print("  id:", entry.id)
                self.assertEqual(100, entry.id, "Bad setID for positive int")

                entry2 = titleEntry()
                entry2.setID('0')
                self.assertEqual(0, entry2.id, "setID(0) should leave id at 0")

                entry.setType('SHORTFICTION')
                print("  type:", entry.type)
                self.assertEqual('SHORTFICTION', entry.type, "Bad setType")

                entry.setLength('short story')
                print("  length:", entry.length)
                self.assertEqual('short story', entry.length, "Bad setLength")

                # setLength with None -> stored as ''
                entry.setLength(None)
                print("  length (None):", entry.length)
                self.assertEqual('', entry.length, "setLength(None) should produce ''")

                entry.setAuthors('Stephen King')
                print("  authors:", entry.authors)
                self.assertEqual('Stephen King', entry.authors, "Bad setAuthors")

        def test_04_titleEntry_xmlTitle_new(self):
                print("\nTEST: titleEntry.xmlTitle - new entry (id=0)")
                entry = titleEntry()
                entry.setTitle('The Shining')
                entry.setAuthors('Stephen King')
                entry.setDate('1977-01-01')
                entry.setPage('1')
                entry.setType('NOVEL')

                xml = entry.xmlTitle()
                print("  xml:", xml)
                self.assertIn('<ContentTitle>', xml, "Missing <ContentTitle>")
                self.assertIn('<cTitle>The Shining</cTitle>', xml, "Missing cTitle")
                self.assertIn('<cAuthors>Stephen King</cAuthors>', xml, "Missing cAuthors")
                self.assertIn('<cPage>1</cPage>', xml, "Missing cPage")
                self.assertIn('<cType>NOVEL</cType>', xml, "Missing cType")
                self.assertIn('</ContentTitle>', xml, "Missing </ContentTitle>")

                # Without page or type, those tags should be absent
                entry2 = titleEntry()
                entry2.setTitle('Untitled')
                entry2.setAuthors('Unknown')
                xml2 = entry2.xmlTitle()
                self.assertNotIn('<cPage>', xml2, "cPage should be absent when empty")
                self.assertNotIn('<cType>', xml2, "cType should be absent when empty")
                self.assertNotIn('<cLength>', xml2, "cLength should be absent when empty")

        def test_05_reviewEntry_xmlTitle_new(self):
                print("\nTEST: reviewEntry.xmlTitle - new entry (id=0)")
                entry = reviewEntry()
                entry.setTitle('A Review of Something')
                entry.setBookAuthors('Stephen King')
                entry.setReviewers('John Doe')
                entry.setDate('2000-01-01')
                entry.setPage('15')

                xml = entry.xmlTitle()
                print("  xml:", xml)
                self.assertIn('<ContentReview>', xml, "Missing <ContentReview>")
                self.assertIn('<cTitle>A Review of Something</cTitle>', xml, "Missing cTitle")
                self.assertIn('<cBookAuthors>Stephen King</cBookAuthors>', xml, "Missing cBookAuthors")
                self.assertIn('<cReviewers>John Doe</cReviewers>', xml, "Missing cReviewers")
                self.assertIn('<cPage>15</cPage>', xml, "Missing cPage")
                self.assertIn('</ContentReview>', xml, "Missing </ContentReview>")

        def test_06_interviewEntry_xmlTitle_new(self):
                print("\nTEST: interviewEntry.xmlTitle - new entry (id=0)")
                entry = interviewEntry()
                entry.setTitle('Interview with the Author')
                entry.setInterviewees('Stephen King')
                entry.setInterviewers('Jane Smith')
                entry.setDate('2005-06-01')

                xml = entry.xmlTitle()
                print("  xml:", xml)
                self.assertIn('<ContentInterview>', xml, "Missing <ContentInterview>")
                self.assertIn('<cTitle>Interview with the Author</cTitle>', xml, "Missing cTitle")
                self.assertIn('<cInterviewees>Stephen King</cInterviewees>', xml, "Missing cInterviewees")
                self.assertIn('<cInterviewers>Jane Smith</cInterviewers>', xml, "Missing cInterviewers")
                self.assertIn('</ContentInterview>', xml, "Missing </ContentInterview>")

                # No page set -> cPage absent
                self.assertNotIn('<cPage>', xml, "cPage should be absent when empty")

        def test_07_pubs_authors(self):
                print("\nTEST: pubs.authors")
                pub = pubs(db)

                # TEST 1 - No authors -> empty string
                value = pub.authors()
                print("  Received (0 authors):", value)
                self.assertEqual('', value, "0 authors should return ''")

                # TEST 2 - One author
                pub.pub_authors = ['Stephen King']
                pub.num_authors = 1
                value = pub.authors()
                print("  Received (1 author):", value)
                self.assertIn('Stephen King', value, "Author name missing")

                # TEST 3 - Two authors joined with '+'
                pub.pub_authors = ['Stephen King', 'Peter Straub']
                pub.num_authors = 2
                value = pub.authors()
                print("  Received (2 authors):", value)
                self.assertIn('Stephen King', value, "First author missing")
                self.assertIn('Peter Straub', value, "Second author missing")
                self.assertIn('+', value, "Authors should be joined with '+'")

        def test_08_pubs_artists(self):
                print("\nTEST: pubs.artists")
                pub = pubs(db)

                # TEST 1 - No artists -> empty string
                value = pub.artists()
                print("  Received (0 artists):", value)
                self.assertEqual('', value, "0 artists should return ''")

                # TEST 2 - One artist
                pub.pub_artists = ['Joe Artist']
                pub.num_artists = 1
                value = pub.artists()
                print("  Received (1 artist):", value)
                self.assertIn('Joe Artist', value, "Artist name missing")

        def test_09_pubs_load(self):
                print("\nTEST: pubs.load - by id (pub 24052, Night Shift)")
                pub = pubs(db)
                pub.load(24052)
                print_values = 1
                if print_values:
                        printClass(pub)
                else:
                        self.assertEqual(1, pub.used_id, "Bad used_id")
                        self.assertEqual(1, pub.used_title, "Bad used_title")
                        self.assertEqual('', pub.error, "Unexpected error")
                        print("  Received title:", pub.pub_title)
                        self.assertEqual('Night Shift', pub.pub_title, "Bad pub_title")

        def test_10_pubs_load_not_found(self):
                print("\nTEST: pubs.load - edge cases")

                # TEST 1 - id=0: returns silently, error stays ''
                pub = pubs(db)
                pub.load(0)
                print("  error (id=0):", pub.error)
                self.assertEqual('', pub.error, "load(0) should not set error")
                self.assertEqual(0, pub.used_id, "load(0) should not set used_id")

                # TEST 2 - Non-existent id: sets error
                pub2 = pubs(db)
                pub2.load(999999999)
                print("  error (not found):", pub2.error)
                self.assertEqual('Pub record not found', pub2.error, "Bad error for missing pub")

        def test_11_pubs_obj2xml(self):
                print("\nTEST: pubs.obj2xml")
                pub = pubs(db)

                # TEST 1 - No used_id: returns empty string (and prints "XML: pass")
                xml = pub.obj2xml()
                print("  xml (no used_id):", xml)
                self.assertEqual('', xml, "obj2xml with no used_id should return ''")

                # TEST 2 - With used_id and several fields set
                pub.pub_id = 24052
                pub.used_id = 1
                pub.pub_title = 'Night Shift'
                pub.used_title = 1
                pub.pub_year = '1978-01-01'
                pub.used_year = 1
                pub.pub_isbn = '0385120400'
                pub.used_isbn = 1

                xml = pub.obj2xml()
                print("  xml (with fields):", xml[:200])
                self.assertIn('<Publication>', xml, "Missing <Publication>")
                self.assertIn('<Record>24052</Record>', xml, "Missing Record")
                self.assertIn('<Title>Night Shift</Title>', xml, "Missing Title")
                self.assertIn('<Year>1978-01-01</Year>', xml, "Missing Year")
                self.assertIn('<Isbn>0385120400</Isbn>', xml, "Missing Isbn")
                self.assertIn('</Publication>', xml, "Missing </Publication>")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
