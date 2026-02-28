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
from awardtypeClass import *
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
# display_table_grid    - prints to stdout
# display_categories    - prints to stdout
# display_awards_for_year - prints to stdout

def printClass(at):
        print("used_id             =", at.used_id)
        print("used_code           =", at.used_code)
        print("used_by             =", at.used_by)
        print("used_for            =", at.used_for)
        print("used_name           =", at.used_name)
        print("used_short_name     =", at.used_short_name)
        print("used_note           =", at.used_note)
        print("used_note_id        =", at.used_note_id)
        print("used_poll           =", at.used_poll)
        print("used_webpages       =", at.used_webpages)
        print("used_non_genre      =", at.used_non_genre)
        print("award_type_id       =", at.award_type_id)
        print("award_type_code     =", at.award_type_code)
        print("award_type_by       =", at.award_type_by)
        print("award_type_for      =", at.award_type_for)
        print("award_type_name     =", at.award_type_name)
        print("award_type_short_name =", at.award_type_short_name)
        print("award_type_poll     =", at.award_type_poll)
        print("award_type_note_id  =", at.award_type_note_id)
        print("award_type_note     =", at.award_type_note)
        print("award_type_webpages =", at.award_type_webpages)
        print("award_type_non_genre =", at.award_type_non_genre)
        print("error               =", at.error)

class MyTestCase(unittest.TestCase):

        def test_01_load_by_id(self):
                print("\nTEST: award_type.load - by id")
                at = award_type()
                at.award_type_id = 9    # BSFA
                at.load()
                print_values = 1
                if print_values:
                        printClass(at)
                else:
                        self.assertEqual(1, at.used_id, "Bad used_id")
                        self.assertEqual(1, at.used_code, "Bad used_code")
                        self.assertEqual(1, at.used_name, "Bad used_name")
                        self.assertEqual(1, at.used_short_name, "Bad used_short_name")
                        self.assertEqual('', at.error, "Unexpected error")
                        print("  Received name:", at.award_type_name)
                        self.assertEqual('British Science Fiction Association Award', at.award_type_name, "Bad award_type_name")
                        print("  Received short name:", at.award_type_short_name)
                        self.assertEqual('BSFA', at.award_type_short_name, "Bad award_type_short_name")

        def test_02_load_by_code(self):
                print("\nTEST: award_type.load - by code")
                at = award_type()
                at.award_type_code = 'BSFA'
                at.load()
                print_values = 1
                if print_values:
                        printClass(at)
                else:
                        self.assertEqual(1, at.used_id, "Bad used_id")
                        self.assertEqual(1, at.used_code, "Bad used_code")
                        self.assertEqual(1, at.used_name, "Bad used_name")
                        self.assertEqual('', at.error, "Unexpected error")
                        print("  Received name:", at.award_type_name)
                        self.assertEqual('British Science Fiction Association Award', at.award_type_name, "Bad award_type_name")

        def test_03_load_no_args(self):
                print("\nTEST: award_type.load - no args")
                # load() sets an error when neither award_type_id nor award_type_code is set
                at = award_type()
                at.load()
                print("  Received error:", at.error)
                expected = 'Award type not specified'
                self.assertEqual(expected, at.error, "Bad error message")
                self.assertEqual(0, at.used_id, "Bad used_id")
                self.assertEqual(0, at.used_name, "Bad used_name")

        def test_04_load_id_not_found(self):
                print("\nTEST: award_type.load - id not found")
                at = award_type()
                at.award_type_id = 999999    # Non-existent award type ID
                at.load()
                print("  Received error:", at.error)
                expected = 'Award type not found: 999999'
                self.assertEqual(expected, at.error, "Bad error message")

        def test_05_load_code_not_found(self):
                print("\nTEST: award_type.load - code not found")
                at = award_type()
                at.award_type_code = 'XXXXXXXXXX'    # Non-existent award type code
                at.load()
                print("  Received error:", at.error)
                expected = 'Award type not found: XXXXXXXXXX'
                self.assertEqual(expected, at.error, "Bad error message")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
