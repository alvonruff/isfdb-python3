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
from awardClass import *
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
# cgi2obj           - requires input from cgi
# PrintAwardTable   - prints to stdout
# PrintAwardRow     - prints to stdout
# PrintYear         - prints to stdout
# PrintLevel        - prints to stdout
# PrintTitle        - prints to stdout
# PrintAwardSummary - prints to stdout
# PrintAwardAuthors - prints to stdout
# PrintOneAwardList - prints to stdout
# PrintOneAward     - prints to stdout
# displayAuthor     - prints to stdout
# BuildDisplayLevel - requires SESSION.ui context
# loadXML           - sufficiently tested via load()

def printClass(aw):
        print("db                      =", aw.db)
        print("used_id                 =", aw.used_id)
        print("used_title              =", aw.used_title)
        print("used_year               =", aw.used_year)
        print("used_cat_id             =", aw.used_cat_id)
        print("used_cat_name           =", aw.used_cat_name)
        print("used_level              =", aw.used_level)
        print("used_movie              =", aw.used_movie)
        print("used_title_id           =", aw.used_title_id)
        print("used_type_name          =", aw.used_type_name)
        print("used_type_short_name    =", aw.used_type_short_name)
        print("used_type_id            =", aw.used_type_id)
        print("used_type_poll          =", aw.used_type_poll)
        print("used_note_id            =", aw.used_note_id)
        print("used_note               =", aw.used_note)
        print("award_id                =", aw.award_id)
        print("title_id                =", aw.title_id)
        print("award_title             =", aw.award_title)
        print("award_year              =", aw.award_year)
        print("award_cat_id            =", aw.award_cat_id)
        print("award_cat_name          =", aw.award_cat_name)
        print("award_level             =", aw.award_level)
        print("award_displayed_level   =", aw.award_displayed_level)
        print("award_movie             =", aw.award_movie)
        print("award_type_name         =", aw.award_type_name)
        print("award_type_short_name   =", aw.award_type_short_name)
        print("award_type_id           =", aw.award_type_id)
        print("award_type_poll         =", aw.award_type_poll)
        print("award_note_id           =", aw.award_note_id)
        print("award_note              =", aw.award_note)
        print("award_authors           =", aw.award_authors)
        print("num_authors             =", aw.num_authors)
        print("error                   =", aw.error)

class MyTestCase(unittest.TestCase):

        def test_01_SpecialAwards(self):
                print("\nTEST: awards.SpecialAwards")
                special = awards(db).SpecialAwards()

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

                print("  Received key '82':", special['82'])
                self.assertEqual('Withdrawn -- Nomination Declined', special['82'], "Bad SpecialAwards value")

                print("  Received key '83':", special['83'])
                self.assertEqual('Withdrawn -- Conflict of Interest', special['83'], "Bad SpecialAwards value")

                print("  Received key '84':", special['84'])
                self.assertEqual('Withdrawn -- Official Publication in a Previous Year', special['84'], "Bad SpecialAwards value")

                print("  Received key '85':", special['85'])
                self.assertEqual('Withdrawn -- Ineligible', special['85'], "Bad SpecialAwards value")

                print("  Received key '90':", special['90'])
                self.assertEqual('Finalists', special['90'], "Bad SpecialAwards value")

                print("  Received key '91':", special['91'])
                self.assertEqual('Made First Ballot', special['91'], "Bad SpecialAwards value")

                print("  Received key '92':", special['92'])
                self.assertEqual('Preliminary Nominees', special['92'], "Bad SpecialAwards value")

                print("  Received key '93':", special['93'])
                self.assertEqual('Honorable Mentions', special['93'], "Bad SpecialAwards value")

                print("  Received key '98':", special['98'])
                self.assertEqual('Early Submissions', special['98'], "Bad SpecialAwards value")

                print("  Received key '99':", special['99'])
                self.assertEqual('Nominations Below Cutoff', special['99'], "Bad SpecialAwards value")

        def test_02_authors(self):
                print("\nTEST: awards.authors")

                # TEST 1 - No authors
                aw = awards(db)
                value = aw.authors()
                print("  Received (no authors):", repr(value))
                self.assertEqual('', value, "Bad authors string")

                # TEST 2 - One author
                aw = awards(db)
                aw.award_authors = ['Stephen King']
                aw.num_authors = 1
                value = aw.authors()
                print("  Received (one author):", value)
                self.assertEqual('Stephen King', value, "Bad authors string")

                # TEST 3 - Two authors
                aw = awards(db)
                aw.award_authors = ['Stephen King', 'Peter Straub']
                aw.num_authors = 2
                value = aw.authors()
                print("  Received (two authors):", value)
                self.assertEqual('Stephen King+Peter Straub', value, "Bad authors string")

        def test_03_load(self):
                print("\nTEST: awards.load")
                aw = awards(db)
                aw.load(1)
                print_values = 1
                if print_values:
                        printClass(aw)
                else:
                        self.assertEqual(1, aw.used_id, "Bad used_id")
                        self.assertEqual(1, aw.used_title, "Bad used_title")
                        self.assertEqual(1, aw.used_year, "Bad used_year")
                        self.assertEqual(1, aw.used_cat_id, "Bad used_cat_id")
                        self.assertEqual(1, aw.used_cat_name, "Bad used_cat_name")
                        self.assertEqual(1, aw.used_level, "Bad used_level")
                        self.assertEqual(1, aw.used_type_id, "Bad used_type_id")
                        self.assertEqual(1, aw.used_type_name, "Bad used_type_name")
                        self.assertEqual(1, aw.used_type_poll, "Bad used_type_poll")
                        self.assertEqual('', aw.error, "Unexpected error")

        def test_04_load_zero(self):
                print("\nTEST: awards.load - id zero")
                # load(0) returns immediately; no data, no error
                aw = awards(db)
                aw.load(0)
                print("  Received error:", aw.error)
                self.assertEqual('', aw.error, "Unexpected error")
                self.assertEqual(0, aw.used_id, "Bad used_id")
                self.assertEqual('', aw.award_title, "Bad award_title")

        def test_05_load_not_found(self):
                print("\nTEST: awards.load - award not found")
                aw = awards(db)
                aw.load(999999)    # Non-existent award ID
                print("  Received error:", aw.error)
                expected = 'Award record not found'
                self.assertEqual(expected, aw.error, "Bad error message")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
