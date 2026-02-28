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
from pubseriesClass import *
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
# cgi2obj   - requires IsfdbFieldStorage / CGI input
# delete    - executes DELETE SQL


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


def printClass(ps):
        print("used_id              =", ps.used_id)
        print("used_name            =", ps.used_name)
        print("used_trans_names     =", ps.used_trans_names)
        print("used_webpages        =", ps.used_webpages)
        print("used_note            =", ps.used_note)
        print("pub_series_id        =", ps.pub_series_id)
        print("pub_series_name      =", ps.pub_series_name)
        print("pub_series_trans_names =", ps.pub_series_trans_names)
        print("pub_series_note      =", ps.pub_series_note)
        print("pub_series_webpages  =", ps.pub_series_webpages)
        print("error                =", ps.error)


class MyTestCase(unittest.TestCase):

        def test_01_init(self):
                print("\nTEST: pub_series.__init__")
                ps = pub_series(db)
                self.assertEqual(0, ps.used_id, "Bad used_id init")
                self.assertEqual(0, ps.used_name, "Bad used_name init")
                self.assertEqual(0, ps.used_trans_names, "Bad used_trans_names init")
                self.assertEqual(0, ps.used_webpages, "Bad used_webpages init")
                self.assertEqual(0, ps.used_note, "Bad used_note init")
                self.assertEqual('', ps.pub_series_id, "Bad pub_series_id init")
                self.assertEqual('', ps.pub_series_name, "Bad pub_series_name init")
                self.assertEqual([], ps.pub_series_trans_names, "Bad pub_series_trans_names init")
                self.assertEqual('', ps.pub_series_note, "Bad pub_series_note init")
                self.assertEqual([], ps.pub_series_webpages, "Bad pub_series_webpages init")
                self.assertEqual('', ps.error, "Bad error init")
                print("  Init state verified.")

        def test_02_load(self):
                print("\nTEST: pub_series.load - by id")
                ps = pub_series(db)
                ps.load(1)
                print_values = 1
                if print_values:
                        printClass(ps)
                else:
                        self.assertEqual(1, ps.used_id, "Bad used_id")
                        self.assertEqual(1, ps.used_name, "Bad used_name")
                        self.assertEqual('', ps.error, "Unexpected error")
                        print("  Received name:", ps.pub_series_name)

        def test_03_load_not_found(self):
                print("\nTEST: pub_series.load - not found")
                ps = pub_series(db)
                # load() prints to stdout on error; capture to suppress it
                captureOutput(ps.load, 999999999)
                print("  Received error:", ps.error)
                self.assertEqual('Publication series record not found', ps.error, "Bad error message")
                self.assertEqual(0, ps.used_id, "used_id should remain 0")
                self.assertEqual(0, ps.used_name, "used_name should remain 0")

        def test_04_obj2xml(self):
                print("\nTEST: pub_series.obj2xml")

                # TEST 1 - No used_id: returns '' (also prints "XML: pass")
                ps = pub_series(db)
                xml = captureOutput(ps.obj2xml)
                # obj2xml returns the container string; capture stdout but also call directly
                ps2 = pub_series(db)
                result = ps2.obj2xml()
                print("  xml (no used_id):", result)
                self.assertEqual('', result, "obj2xml with no used_id should return ''")

                # TEST 2 - With used_id and name set
                ps3 = pub_series(db)
                ps3.pub_series_id = 1
                ps3.used_id = 1
                ps3.pub_series_name = 'Ace Science Fiction'
                ps3.used_name = 1

                result = ps3.obj2xml()
                print("  xml (with fields):", result)
                self.assertIn('<UpdatePubSeries>', result, "Missing <UpdatePubSeries>")
                self.assertIn('<PubSeriesId>1</PubSeriesId>', result, "Missing PubSeriesId")
                self.assertIn('<PubSeriesName>Ace Science Fiction</PubSeriesName>', result, "Missing PubSeriesName")
                self.assertIn('</UpdatePubSeries>', result, "Missing </UpdatePubSeries>")

                # TEST 3 - used_id set but not used_name: name tag absent
                ps4 = pub_series(db)
                ps4.pub_series_id = 1
                ps4.used_id = 1
                result4 = ps4.obj2xml()
                self.assertNotIn('<PubSeriesName>', result4, "PubSeriesName should be absent when not used")

        def test_05_xml2obj(self):
                print("\nTEST: pub_series.xml2obj")

                # TEST 1 - Name present -> field set
                ps = pub_series(db)
                xml = '<UpdatePubSeries><PubSeriesName>Ace SF</PubSeriesName></UpdatePubSeries>'
                ps.xml2obj(xml)
                print("  pub_series_name:", ps.pub_series_name)
                print("  used_name:", ps.used_name)
                self.assertEqual(1, ps.used_name, "Bad used_name after xml2obj")
                self.assertEqual('Ace SF', ps.pub_series_name, "Bad pub_series_name after xml2obj")

                # TEST 2 - Absent element -> field not set
                ps2 = pub_series(db)
                xml2 = '<UpdatePubSeries></UpdatePubSeries>'
                ps2.xml2obj(xml2)
                self.assertEqual(0, ps2.used_name, "used_name should stay 0 for absent element")
                self.assertEqual('', ps2.pub_series_name, "pub_series_name should stay '' for absent element")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
