#!_PYTHONLOC
# -*- coding: utf-8 -*-
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
from isfdb import *
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
# UNTESTED Functions/Sections
##############################################################
# PrintHTMLHeaders              - prints to stdout
# Session.ParseParameters       - invoked at module load; depends on CGI environment
# Session.Parameter             - calls DisplayError which calls sys.exit(0)
# Session.DisplayError          - calls sys.exit(0)
# Session._DisplayBiblioError   - prints to stdout
# Session._DisplayEditError     - prints to stdout
# Session._DisplayModError      - prints to stdout

class MyTestCase(unittest.TestCase):

        def test_01_Session_db(self):
                print("\nTEST: SESSION.db")

                print("  Received pub_types:", SESSION.db.pub_types)
                self.assertEqual(8, len(SESSION.db.pub_types), "Bad pub_types length")
                self.assertIn('NOVEL', SESSION.db.pub_types, "NOVEL missing from pub_types")
                self.assertIn('ANTHOLOGY', SESSION.db.pub_types, "ANTHOLOGY missing from pub_types")
                self.assertIn('MAGAZINE', SESSION.db.pub_types, "MAGAZINE missing from pub_types")

                print("  Received regular_title_types:", SESSION.db.regular_title_types)
                self.assertEqual(12, len(SESSION.db.regular_title_types), "Bad regular_title_types length")
                self.assertIn('NOVEL', SESSION.db.regular_title_types, "NOVEL missing from regular_title_types")
                self.assertIn('SHORTFICTION', SESSION.db.regular_title_types, "SHORTFICTION missing from regular_title_types")

                print("  Received all_title_types:", SESSION.db.all_title_types)
                self.assertEqual(15, len(SESSION.db.all_title_types), "Bad all_title_types length")
                # Verify sorted order
                self.assertEqual(list(sorted(SESSION.db.all_title_types)), list(SESSION.db.all_title_types), "all_title_types not sorted")
                self.assertIn('COVERART', SESSION.db.all_title_types, "COVERART missing from all_title_types")
                self.assertIn('REVIEW', SESSION.db.all_title_types, "REVIEW missing from all_title_types")
                self.assertIn('INTERVIEW', SESSION.db.all_title_types, "INTERVIEW missing from all_title_types")

                print("  Received storylen_codes:", SESSION.db.storylen_codes)
                self.assertEqual(4, len(SESSION.db.storylen_codes), "Bad storylen_codes length")
                self.assertEqual('', SESSION.db.storylen_codes[0], "Bad storylen_codes[0]")
                self.assertEqual('novella', SESSION.db.storylen_codes[1], "Bad storylen_codes[1]")
                self.assertEqual('short story', SESSION.db.storylen_codes[2], "Bad storylen_codes[2]")
                self.assertEqual('novelette', SESSION.db.storylen_codes[3], "Bad storylen_codes[3]")

                print("  Received formats count:", len(SESSION.db.formats))
                self.assertIn('hc', SESSION.db.formats, "hc missing from formats")
                self.assertIn('pb', SESSION.db.formats, "pb missing from formats")
                self.assertIn('ebook', SESSION.db.formats, "ebook missing from formats")

        def test_02_Session_ui(self):
                print("\nTEST: SESSION.ui")

                print("  Received bullet:", SESSION.ui.bullet)
                self.assertEqual('&#8226;', SESSION.ui.bullet, "Bad bullet")

                print("  Received enspace:", SESSION.ui.enspace)
                self.assertEqual('&#8194;', SESSION.ui.enspace, "Bad enspace")

                print("  Received info_sign:", SESSION.ui.info_sign)
                self.assertEqual('&#x24d8;', SESSION.ui.info_sign, "Bad info_sign")

                print("  Received question_mark:", SESSION.ui.question_mark)
                self.assertEqual('?', SESSION.ui.question_mark, "Bad question_mark")

                print("  Received page_numbers keys:", list(sorted(SESSION.ui.page_numbers.keys())))
                self.assertEqual(7, len(SESSION.ui.page_numbers), "Bad page_numbers length")
                self.assertIn('fc', SESSION.ui.page_numbers, "fc missing from page_numbers")
                self.assertIn('bc', SESSION.ui.page_numbers, "bc missing from page_numbers")
                self.assertIn('rj', SESSION.ui.page_numbers, "rj missing from page_numbers")
                self.assertEqual('front cover', SESSION.ui.page_numbers['fc'], "Bad page_numbers['fc']")
                self.assertEqual('back cover', SESSION.ui.page_numbers['bc'], "Bad page_numbers['bc']")

        def test_03_Session_currency(self):
                print("\nTEST: SESSION.currency")

                # These use HTML entity strings and are unaffected by Python2->Python3
                print("  Received baht:", SESSION.currency.baht)
                self.assertEqual('&#3647;', SESSION.currency.baht, "Bad baht")

                print("  Received czech_koruna:", SESSION.currency.czech_koruna)
                self.assertEqual('K&#269;', SESSION.currency.czech_koruna, "Bad czech_koruna")

                print("  Received indian_rupee:", SESSION.currency.indian_rupee)
                self.assertEqual('&#8377;', SESSION.currency.indian_rupee, "Bad indian_rupee")

                print("  Received yuan:", SESSION.currency.yuan)
                self.assertEqual('&#20803;', SESSION.currency.yuan, "Bad yuan")

                # These use chr() which behaves differently in Python2 vs Python3.
                # In Python2, chr() returns a byte in the current encoding (Windows-1252).
                # In Python3, chr() returns a Unicode code point.
                # chr(163)='£' and chr(165)='¥' are consistent across both versions.
                # chr(128) for euro and chr(131) for guilder are NOT correct in Python3.
                print("  Received pound:", SESSION.currency.pound)
                self.assertEqual(chr(163), SESSION.currency.pound, "Bad pound")

                print("  Received yen:", SESSION.currency.yen)
                self.assertEqual(chr(165), SESSION.currency.yen, "Bad yen")

                print("  Received euro:", SESSION.currency.euro)
                self.assertEqual(chr(128), SESSION.currency.euro, "Bad euro")

                print("  Received guilder:", SESSION.currency.guilder)
                self.assertEqual(chr(131), SESSION.currency.guilder, "Bad guilder")

        def test_04_Session_special_authors(self):
                print("\nTEST: SESSION.special_authors_to_ignore")
                special = SESSION.special_authors_to_ignore
                print("  Received:", special)
                self.assertEqual(7, len(special), "Bad special_authors_to_ignore length")
                self.assertIn('unknown', special, "unknown missing")
                self.assertIn('uncredited', special, "uncredited missing")
                self.assertIn('various', special, "various missing")
                self.assertIn('Anonymous', special, "Anonymous missing")

        def test_05_field_offsets(self):
                print("\nTEST: field offsets")

                # Publication field offsets
                self.assertEqual(0, PUB_PUBID, "Bad PUB_PUBID")
                self.assertEqual(1, PUB_TITLE, "Bad PUB_TITLE")
                self.assertEqual(8, PUB_ISBN, "Bad PUB_ISBN")
                self.assertEqual(9, PUB_IMAGE, "Bad PUB_IMAGE")

                # Author field offsets
                self.assertEqual(0, AUTHOR_ID, "Bad AUTHOR_ID")
                self.assertEqual(1, AUTHOR_CANONICAL, "Bad AUTHOR_CANONICAL")
                self.assertEqual(4, AUTHOR_BIRTHDATE, "Bad AUTHOR_BIRTHDATE")
                self.assertEqual(13, AUTHOR_LASTNAME, "Bad AUTHOR_LASTNAME")
                self.assertEqual(14, AUTHOR_LANGUAGE, "Bad AUTHOR_LANGUAGE")

                # Title field offsets
                self.assertEqual(0, TITLE_PUBID, "Bad TITLE_PUBID")
                self.assertEqual(1, TITLE_TITLE, "Bad TITLE_TITLE")
                self.assertEqual(7, TITLE_YEAR, "Bad TITLE_YEAR")
                self.assertEqual(9, TITLE_TTYPE, "Bad TITLE_TTYPE")
                self.assertEqual(12, TITLE_PARENT, "Bad TITLE_PARENT")

                # Award field offsets
                self.assertEqual(0, AWARD_ID, "Bad AWARD_ID")
                self.assertEqual(6, AWARD_LEVEL, "Bad AWARD_LEVEL")
                self.assertEqual(8, AWARD_TYPEID, "Bad AWARD_TYPEID")
                self.assertEqual(9, AWARD_CATID, "Bad AWARD_CATID")

                # Award type field offsets
                self.assertEqual(0, AWARD_TYPE_ID, "Bad AWARD_TYPE_ID")
                self.assertEqual(2, AWARD_TYPE_NAME, "Bad AWARD_TYPE_NAME")
                self.assertEqual(7, AWARD_TYPE_SHORT_NAME, "Bad AWARD_TYPE_SHORT_NAME")
                self.assertEqual(8, AWARD_TYPE_POLL, "Bad AWARD_TYPE_POLL")

                # Submission field offsets
                self.assertEqual(0, SUB_ID, "Bad SUB_ID")
                self.assertEqual(2, SUB_TYPE, "Bad SUB_TYPE")
                self.assertEqual(3, SUB_DATA, "Bad SUB_DATA")

                print("  All field offsets verified.")

        def test_06_SUBMAP(self):
                print("\nTEST: SUBMAP")

                print("  Received SUBMAP entry count:", len(SUBMAP))
                self.assertGreater(len(SUBMAP), 30, "Bad SUBMAP length")

                # Spot-check a few well-known submission types
                self.assertIn(MOD_AUTHOR_UPDATE, SUBMAP, "MOD_AUTHOR_UPDATE missing from SUBMAP")
                self.assertEqual('AuthorUpdate', SUBMAP[MOD_AUTHOR_UPDATE][1], "Bad SUBMAP AuthorUpdate short name")
                self.assertEqual('Author Update', SUBMAP[MOD_AUTHOR_UPDATE][3], "Bad SUBMAP AuthorUpdate full name")

                self.assertIn(MOD_TITLE_UPDATE, SUBMAP, "MOD_TITLE_UPDATE missing from SUBMAP")
                self.assertEqual('TitleUpdate', SUBMAP[MOD_TITLE_UPDATE][1], "Bad SUBMAP TitleUpdate short name")
                self.assertEqual('Title Update', SUBMAP[MOD_TITLE_UPDATE][3], "Bad SUBMAP TitleUpdate full name")

                self.assertIn(MOD_PUB_NEW, SUBMAP, "MOD_PUB_NEW missing from SUBMAP")
                self.assertEqual('NewPub', SUBMAP[MOD_PUB_NEW][1], "Bad SUBMAP NewPub short name")
                self.assertEqual('New Publication', SUBMAP[MOD_PUB_NEW][3], "Bad SUBMAP NewPub full name")

                print("  SUBMAP spot-checks passed.")

        def test_07_SUBMISSION_DISPLAY(self):
                print("\nTEST: SUBMISSION_DISPLAY")

                print("  Received SUBMISSION_DISPLAY entry count:", len(SUBMISSION_DISPLAY))
                self.assertGreater(len(SUBMISSION_DISPLAY), 20, "Bad SUBMISSION_DISPLAY length")

                self.assertEqual('Format', SUBMISSION_DISPLAY['Binding'], "Bad Binding display")
                self.assertEqual('ISBN', SUBMISSION_DISPLAY['Isbn'], "Bad Isbn display")
                self.assertEqual('Date', SUBMISSION_DISPLAY['Year'], "Bad Year display")
                self.assertEqual('Birth Date', SUBMISSION_DISPLAY['Birthdate'], "Bad Birthdate display")
                self.assertEqual('Directory Entry', SUBMISSION_DISPLAY['Familyname'], "Bad Familyname display")

                print("  SUBMISSION_DISPLAY spot-checks passed.")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
