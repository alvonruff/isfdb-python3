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
from templateClass import *
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


def printClass(t):
        print("used_id             =", t.used_id)
        print("used_name           =", t.used_name)
        print("used_displayed_name =", t.used_displayed_name)
        print("used_type           =", t.used_type)
        print("used_url            =", t.used_url)
        print("used_mouseover      =", t.used_mouseover)
        print("id                  =", t.id)
        print("name                =", t.name)
        print("displayed_name      =", t.displayed_name)
        print("type                =", t.type)
        print("url                 =", t.url)
        print("mouseover           =", t.mouseover)
        print("error               =", t.error)


class MyTestCase(unittest.TestCase):

        def test_01_init(self):
                print("\nTEST: Template.__init__")
                t = Template()
                self.assertEqual(0, t.used_id, "Bad used_id init")
                self.assertEqual(0, t.used_name, "Bad used_name init")
                self.assertEqual(0, t.used_displayed_name, "Bad used_displayed_name init")
                self.assertEqual(0, t.used_type, "Bad used_type init")
                self.assertEqual(0, t.used_url, "Bad used_url init")
                self.assertEqual(0, t.used_mouseover, "Bad used_mouseover init")
                self.assertEqual('', t.id, "Bad id init")
                self.assertEqual('', t.name, "Bad name init")
                self.assertEqual('', t.displayed_name, "Bad displayed_name init")
                self.assertEqual('', t.type, "Bad type init")
                self.assertEqual('', t.url, "Bad url init")
                self.assertEqual('', t.mouseover, "Bad mouseover init")
                self.assertEqual('', t.error, "Bad error init")
                print("  Init state verified.")

        def test_02_load(self):
                print("\nTEST: Template.load - by id")
                t = Template()
                t.load(1)
                print_values = 1
                if print_values:
                        printClass(t)
                else:
                        self.assertEqual(1, t.used_id, "Bad used_id")
                        self.assertEqual(1, t.used_name, "Bad used_name")
                        self.assertEqual('', t.error, "Unexpected error")
                        print("  Received name:", t.name)

        def test_03_load_id_zero(self):
                print("\nTEST: Template.load - id=0 (falsy)")
                t = Template()
                t.load(0)
                # load() returns immediately for falsy id; nothing is set
                print("  used_id:", t.used_id)
                self.assertEqual(0, t.used_id, "load(0) should not set used_id")
                self.assertEqual('', t.id, "load(0) should not set id")
                self.assertEqual('', t.error, "load(0) should not set error")

        def test_04_load_not_found(self):
                print("\nTEST: Template.load - id not found")
                t = Template()
                t.load(999999999)
                # load() sets used_id=1 and stores the id, but returns silently
                # when SQLGetTemplate finds no record; no error is set
                print("  used_id:", t.used_id)
                print("  id:", t.id)
                print("  error:", t.error)
                self.assertEqual(1, t.used_id, "used_id should be set even when record not found")
                self.assertEqual(999999999, t.id, "id should be stored even when record not found")
                self.assertEqual(0, t.used_name, "used_name should remain 0 when record not found")
                self.assertEqual('', t.error, "error should remain '' when record not found")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
