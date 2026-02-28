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
import io

if sys.version_info.major == 3:
        PYTHONVER = "python3"
elif sys.version_info.major == 2:
        PYTHONVER = "python2"

from SQLparsing import *
from seriesClass import *
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
# cgi2obj              - requires IsfdbFieldStorage / CGI input
# PrintMetaData        - prints to stdout
# PrintSeriesTagsBrief - prints to stdout
# PrintSeriesTagsFull  - prints to stdout
# BuildTreeData        - requires a full series tree context
# BuildSeriesTree      - requires seriesData and seriesTree dicts from BuildTreeData


def captureOutput(func, *args, **kwargs):
        old_stdout = sys.stdout
        if PYTHONVER == 'python2':
                import StringIO
                sys.stdout = StringIO.StringIO()
        else:
                sys.stdout = io.StringIO()
        try:
                func(*args, **kwargs)
                output = sys.stdout.getvalue()
        finally:
                sys.stdout = old_stdout
        return output


def printClass(ser):
        print("used_id               =", ser.used_id)
        print("used_name             =", ser.used_name)
        print("used_trans_names      =", ser.used_trans_names)
        print("used_parent_id        =", ser.used_parent_id)
        print("used_parent           =", ser.used_parent)
        print("used_type             =", ser.used_type)
        print("used_parentposition   =", ser.used_parentposition)
        print("used_webpages         =", ser.used_webpages)
        print("used_note_id          =", ser.used_note_id)
        print("used_note             =", ser.used_note)
        print("series_id             =", ser.series_id)
        print("series_name           =", ser.series_name)
        print("series_trans_names    =", ser.series_trans_names)
        print("series_parent_id      =", ser.series_parent_id)
        print("series_parent         =", ser.series_parent)
        print("series_type           =", ser.series_type)
        print("series_parentposition =", ser.series_parentposition)
        print("series_note_id        =", ser.series_note_id)
        print("series_note           =", ser.series_note)
        print("series_webpages       =", ser.series_webpages)
        print("error                 =", ser.error)


class MyTestCase(unittest.TestCase):

        def test_01_init(self):
                print("\nTEST: series.__init__")
                ser = series(db)
                self.assertEqual(0, ser.used_id, "Bad used_id init")
                self.assertEqual(0, ser.used_name, "Bad used_name init")
                self.assertEqual(0, ser.used_trans_names, "Bad used_trans_names init")
                self.assertEqual(0, ser.used_parent_id, "Bad used_parent_id init")
                self.assertEqual(0, ser.used_parent, "Bad used_parent init")
                self.assertEqual(0, ser.used_type, "Bad used_type init")
                self.assertEqual(0, ser.used_parentposition, "Bad used_parentposition init")
                self.assertEqual(0, ser.used_webpages, "Bad used_webpages init")
                self.assertEqual(0, ser.used_note_id, "Bad used_note_id init")
                self.assertEqual(0, ser.used_note, "Bad used_note init")
                self.assertEqual('', ser.series_id, "Bad series_id init")
                self.assertEqual('', ser.series_name, "Bad series_name init")
                self.assertEqual([], ser.series_trans_names, "Bad series_trans_names init")
                self.assertEqual('', ser.series_parent_id, "Bad series_parent_id init")
                self.assertEqual('', ser.series_parent, "Bad series_parent init")
                self.assertEqual('', ser.series_type, "Bad series_type init")
                self.assertEqual('', ser.series_parentposition, "Bad series_parentposition init")
                self.assertEqual('', ser.series_note_id, "Bad series_note_id init")
                self.assertEqual('', ser.series_note, "Bad series_note init")
                self.assertEqual([], ser.series_webpages, "Bad series_webpages init")
                self.assertEqual('', ser.error, "Bad error init")
                print("  Init state verified.")

        def test_02_load(self):
                print("\nTEST: series.load - by id (series 3581, Isaac Asimov's Robot City)")
                ser = series(db)
                ser.load(3581)
                print_values = 1
                if print_values:
                        printClass(ser)
                else:
                        self.assertEqual(1, ser.used_id, "Bad used_id")
                        self.assertEqual(1, ser.used_name, "Bad used_name")
                        self.assertEqual(0, ser.used_trans_names, "Bad used_trans_names")
                        self.assertEqual(1, ser.used_parent_id, "Bad used_parent_id")
                        self.assertEqual(1, ser.used_parent, "Bad used_parent")
                        self.assertEqual(1, ser.used_type, "Bad used_type")
                        self.assertEqual(0, ser.used_parentposition, "Bad used_parentposition")
                        self.assertEqual(1, ser.used_webpages, "Bad used_webpages")
                        self.assertEqual(0, ser.used_note_id, "Bad used_note_id")
                        self.assertEqual(0, ser.used_note, "Bad used_note")
                        self.assertEqual(3581, ser.series_id, "Bad series_id")
                        self.assertEqual("Isaac Asimov's Robot City", ser.series_name, "Bad series_name")
                        self.assertEqual([], ser.series_trans_names, "Bad series_trans_names")
                        self.assertEqual(647, ser.series_parent_id, "Bad series_parent_id")
                        self.assertEqual("The Positronic Robot Stories", ser.series_parent, "Bad series_parent")
                        self.assertEqual(1, ser.series_type, "Bad series_type")
                        self.assertEqual('', ser.series_parentposition, "Bad series_parentposition")
                        self.assertEqual('', ser.series_note_id, "Bad series_note_id")
                        self.assertEqual('', ser.series_note, "Bad series_note")
                        self.assertEqual(['https://web.archive.org/web/20220603165058/https://en.wikipedia.org/wiki/Isaac_Asimov%27s_Robot_City'], ser.series_webpages, "Bad series_webpages")
                        self.assertEqual('', ser.error, "Unexpected error")

        def test_03_load_trans_names(self):
                print("\nTEST: series.load - series with trans names (series 35069, Metro 2033)")
                ser = series(db)
                ser.load(35069)
                print_values = 0
                if print_values:
                        printClass(ser)
                else:
                        self.assertEqual(1, ser.used_id, "Bad used_id")
                        self.assertEqual(1, ser.used_name, "Bad used_name")
                        self.assertEqual(1, ser.used_trans_names, "Bad used_trans_names")
                        self.assertEqual(1, ser.used_parent_id, "Bad used_parent_id")
                        self.assertEqual(1, ser.used_parent, "Bad used_parent")
                        self.assertEqual(0, ser.used_type, "Bad used_type")
                        self.assertEqual(0, ser.used_parentposition, "Bad used_parentposition")
                        self.assertEqual(0, ser.used_webpages, "Bad used_webpages")
                        self.assertEqual(0, ser.used_note_id, "Bad used_note_id")
                        self.assertEqual(0, ser.used_note, "Bad used_note")
                        self.assertEqual(35069, ser.series_id, "Bad series_id")
                        self.assertEqual("&#1052;&#1077;&#1090;&#1088;&#1086; 2033 / Metro 2033", ser.series_name, "Bad series_name")
                        self.assertEqual(['Metro 2033'], ser.series_trans_names, "Bad series_trans_names")
                        self.assertEqual(41995, ser.series_parent_id, "Bad series_parent_id")
                        self.assertEqual("&#1052;&#1077;&#1090;&#1088;&#1086; 2033 / Metro 2033 Universe", ser.series_parent, "Bad series_parent")
                        self.assertEqual('', ser.series_type, "Bad series_type")
                        self.assertEqual('', ser.series_parentposition, "Bad series_parentposition")
                        self.assertEqual('', ser.series_note_id, "Bad series_note_id")
                        self.assertEqual('', ser.series_note, "Bad series_note")
                        self.assertEqual([], ser.series_webpages, "Bad series_webpages")
                        self.assertEqual('', ser.error, "Unexpected error")

        def test_04_load_parentposition(self):
                print("\nTEST: series.load - series with parentposition (series 171, Honor Harrington)")
                ser = series(db)
                ser.load(171)
                print_values = 0
                if print_values:
                        printClass(ser)
                else:
                        self.assertEqual(1, ser.used_id, "Bad used_id")
                        self.assertEqual(1, ser.used_name, "Bad used_name")
                        self.assertEqual(0, ser.used_trans_names, "Bad used_trans_names")
                        self.assertEqual(1, ser.used_parent_id, "Bad used_parent_id")
                        self.assertEqual(1, ser.used_parent, "Bad used_parent")
                        self.assertEqual(1, ser.used_type, "Bad used_type")
                        self.assertEqual(1, ser.used_parentposition, "Bad used_parentposition")
                        self.assertEqual(0, ser.used_webpages, "Bad used_webpages")
                        self.assertEqual(0, ser.used_note_id, "Bad used_note_id")
                        self.assertEqual(0, ser.used_note, "Bad used_note")
                        self.assertEqual(171, ser.series_id, "Bad series_id")
                        self.assertEqual("Honor Harrington", ser.series_name, "Bad series_name")
                        self.assertEqual([], ser.series_trans_names, "Bad series_trans_names")
                        self.assertEqual(11647, ser.series_parent_id, "Bad series_parent_id")
                        self.assertEqual("Honor Harrington Universe", ser.series_parent, "Bad series_parent")
                        self.assertEqual(1, ser.series_type, "Bad series_type")
                        self.assertEqual(1, ser.series_parentposition, "Bad series_parentposition")
                        self.assertEqual('', ser.series_note_id, "Bad series_note_id")
                        self.assertEqual('', ser.series_note, "Bad series_note")
                        self.assertEqual([], ser.series_webpages, "Bad series_webpages")
                        self.assertEqual('', ser.error, "Unexpected error")

        def test_05_load_note(self):
                print("\nTEST: series.load - series with note (series 23, Pellucidar)")
                ser = series(db)
                ser.load(23)
                print_values = 0
                if print_values:
                        printClass(ser)
                else:
                        self.assertEqual(1, ser.used_id, "Bad used_id")
                        self.assertEqual(1, ser.used_name, "Bad used_name")
                        self.assertEqual(0, ser.used_trans_names, "Bad used_trans_names")
                        self.assertEqual(1, ser.used_parent_id, "Bad used_parent_id")
                        self.assertEqual(1, ser.used_parent, "Bad used_parent")
                        self.assertEqual(1, ser.used_type, "Bad used_type")
                        self.assertEqual(1, ser.used_parentposition, "Bad used_parentposition")
                        self.assertEqual(1, ser.used_webpages, "Bad used_webpages")
                        self.assertEqual(1, ser.used_note_id, "Bad used_note_id")
                        self.assertEqual(1, ser.used_note, "Bad used_note")
                        self.assertEqual(23, ser.series_id, "Bad series_id")
                        self.assertEqual("Pellucidar", ser.series_name, "Bad series_name")
                        self.assertEqual([], ser.series_trans_names, "Bad series_trans_names")
                        self.assertEqual(67313, ser.series_parent_id, "Bad series_parent_id")
                        self.assertEqual("Edgar Rice Burroughs' Pellucidar universe", ser.series_parent, "Bad series_parent")
                        self.assertEqual(1, ser.series_type, "Bad series_type")
                        self.assertEqual(1, ser.series_parentposition, "Bad series_parentposition")
                        self.assertEqual(428890, ser.series_note_id, "Bad series_note_id")
                        self.assertEqual('Book 4 of this series, "Tarzan at the Earth\'s Core", is listed as book 13 in the Tarzan series.', ser.series_note, "Bad series_note")
                        self.assertEqual(['https://en.wikipedia.org/wiki/Pellucidar'], ser.series_webpages, "Bad series_webpages")
                        self.assertEqual('', ser.error, "Unexpected error")

        def test_06_load_id_zero(self):
                print("\nTEST: series.load - id=0")
                ser = series(db)
                ser.load(0)
                # load() returns immediately for id==0; nothing is set
                print("  used_id:", ser.used_id)
                self.assertEqual(0, ser.used_id, "load(0) should not set used_id")
                self.assertEqual('', ser.series_id, "load(0) should not set series_id")
                self.assertEqual('', ser.error, "load(0) should not set error")

        def test_07_load_not_found(self):
                print("\nTEST: series.load - id not found")
                ser = series(db)
                # load() prints to stdout on error; capture to suppress it
                captureOutput(ser.load, 999999999)
                print("  error:", ser.error)
                self.assertEqual('Series record not found', ser.error, "Bad error message")
                self.assertEqual(0, ser.used_id, "used_id should remain 0")
                self.assertEqual('', ser.series_id, "series_id should remain ''")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
