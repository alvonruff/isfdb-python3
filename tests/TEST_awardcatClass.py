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
from awardcatClass import *
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
# cgi2obj               - requires input from cgi
# PrintAwardCatYear     - prints to stdout
# PrintAwardCatTable    - prints to stdout
# PrintAwardCatSummary  - prints to stdout
# PrintAwardCatPageHeader - prints to stdout; imports from awardtypeClass, common, login

def printClass(cat):
        print("used_cat_id        =", cat.used_cat_id)
        print("used_cat_name      =", cat.used_cat_name)
        print("used_cat_type_id   =", cat.used_cat_type_id)
        print("used_cat_order     =", cat.used_cat_order)
        print("used_note          =", cat.used_note)
        print("used_note_id       =", cat.used_note_id)
        print("used_webpages      =", cat.used_webpages)
        print("award_cat_id       =", cat.award_cat_id)
        print("award_cat_name     =", cat.award_cat_name)
        print("award_cat_type_id  =", cat.award_cat_type_id)
        print("award_cat_order    =", cat.award_cat_order)
        print("award_cat_note_id  =", cat.award_cat_note_id)
        print("award_cat_note     =", cat.award_cat_note)
        print("award_cat_webpages =", cat.award_cat_webpages)
        print("error              =", cat.error)

class MyTestCase(unittest.TestCase):

        def test_01_SpecialAwards(self):
                print("\nTEST: award_cat.SpecialAwards")
                special = award_cat().SpecialAwards()

                print("  Received dict length:", len(special))
                self.assertEqual(14, len(special), "Bad SpecialAwards length")

                print("  Received key '71':", special['71'])
                self.assertEqual('No Winner -- Insufficient Votes', special['71'], "Bad SpecialAwards value")

                print("  Received key '72':", special['72'])
                self.assertEqual('Not on ballot -- Insufficient Nominations', special['72'], "Bad SpecialAwards value")

                print("  Received key '73':", special['73'])
                self.assertEqual('No Award Given This Year', special['73'], "Bad SpecialAwards value")

                print("  Received key '81':", special['81'])
                self.assertEqual('Withdrawn', special['81'], "Bad SpecialAwards value")

                print("  Received key '92':", special['92'])
                self.assertEqual('Preliminary Nominees', special['92'], "Bad SpecialAwards value")

                print("  Received key '99':", special['99'])
                self.assertEqual('Nominations Below Cutoff', special['99'], "Bad SpecialAwards value")

        def test_02_load(self):
                print("\nTEST: award_cat.load")
                cat = award_cat()
                cat.award_cat_id = 1
                cat.load()
                print_values = 1
                if print_values:
                        printClass(cat)
                else:
                        self.assertEqual(1, cat.used_cat_id, "Bad used_cat_id")
                        self.assertEqual(1, cat.used_cat_name, "Bad used_cat_name")
                        self.assertEqual(1, cat.used_cat_type_id, "Bad used_cat_type_id")
                        self.assertEqual('', cat.error, "Unexpected error")

        def test_03_load_no_id(self):
                print("\nTEST: award_cat.load - no id set")
                # load() returns immediately if award_cat_id is not set
                cat = award_cat()
                cat.load()
                print("  Received error:", cat.error)
                self.assertEqual('', cat.error, "Unexpected error")
                self.assertEqual(0, cat.used_cat_id, "Bad used_cat_id")
                self.assertEqual(0, cat.used_cat_name, "Bad used_cat_name")
                self.assertEqual(0, cat.used_cat_type_id, "Bad used_cat_type_id")
                self.assertEqual('', cat.award_cat_name, "Bad award_cat_name")

        def test_04_load_not_found(self):
                print("\nTEST: award_cat.load - category not found")
                cat = award_cat()
                cat.award_cat_id = 999999    # Non-existent category ID
                cat.load()
                print("  Received error:", cat.error)
                expected = "Award Category doesn't exist"
                self.assertEqual(expected, cat.error, "Bad error message")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
