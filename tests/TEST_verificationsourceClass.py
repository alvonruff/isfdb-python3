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
from verificationsourceClass import *
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


def printClass(vs):
        print("used_id    =", vs.used_id)
        print("used_label =", vs.used_label)
        print("used_name  =", vs.used_name)
        print("used_url   =", vs.used_url)
        print("id         =", vs.id)
        print("label      =", vs.label)
        print("name       =", vs.name)
        print("url        =", vs.url)
        print("error      =", vs.error)


class MyTestCase(unittest.TestCase):

        def test_01_init(self):
                print("\nTEST: VerificationSource.__init__")
                vs = VerificationSource()
                self.assertEqual(0, vs.used_id, "Bad used_id init")
                self.assertEqual(0, vs.used_label, "Bad used_label init")
                self.assertEqual(0, vs.used_name, "Bad used_name init")
                self.assertEqual(0, vs.used_url, "Bad used_url init")
                self.assertEqual('', vs.id, "Bad id init")
                self.assertEqual('', vs.label, "Bad label init")
                self.assertEqual('', vs.name, "Bad name init")
                self.assertEqual('', vs.url, "Bad url init")
                self.assertEqual('', vs.error, "Bad error init")
                print("  Init state verified.")

        def test_02_load(self):
                print("\nTEST: VerificationSource.load - by id")
                vs = VerificationSource()
                vs.load(1)
                print_values = 1
                if print_values:
                        printClass(vs)
                else:
                        self.assertEqual(1, vs.used_id, "Bad used_id")
                        self.assertEqual(1, vs.used_label, "Bad used_label")
                        self.assertEqual('', vs.error, "Unexpected error")
                        print("  Received label:", vs.label)

        def test_03_load_id_zero(self):
                print("\nTEST: VerificationSource.load - id=0 (falsy)")
                vs = VerificationSource()
                vs.load(0)
                # load() returns immediately for falsy id; nothing is set
                print("  used_id:", vs.used_id)
                self.assertEqual(0, vs.used_id, "load(0) should not set used_id")
                self.assertEqual('', vs.id, "load(0) should not set id")
                self.assertEqual('', vs.error, "load(0) should not set error")

        def test_04_load_not_found(self):
                print("\nTEST: VerificationSource.load - id not found")
                vs = VerificationSource()
                vs.load(999999999)
                # load() sets used_id=1 and stores the id before the DB lookup,
                # then returns silently when no record is found; no error is set
                print("  used_id:", vs.used_id)
                print("  id:", vs.id)
                print("  error:", vs.error)
                self.assertEqual(1, vs.used_id, "used_id should be set even when record not found")
                self.assertEqual(999999999, vs.id, "id should be stored even when record not found")
                self.assertEqual(0, vs.used_label, "used_label should remain 0 when record not found")
                self.assertEqual('', vs.error, "error should remain '' when record not found")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
