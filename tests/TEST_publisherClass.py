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
from publisherClass import *
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
# cgi2obj   - requires IsfdbFieldStorage / CGI input; also calls login.User
# delete    - executes DELETE SQL


def printClass(pub):
        print("used_id             =", pub.used_id)
        print("used_name           =", pub.used_name)
        print("used_trans_names    =", pub.used_trans_names)
        print("used_webpages       =", pub.used_webpages)
        print("used_note           =", pub.used_note)
        print("publisher_id        =", pub.publisher_id)
        print("publisher_name      =", pub.publisher_name)
        print("publisher_trans_names =", pub.publisher_trans_names)
        print("publisher_note      =", pub.publisher_note)
        print("publisher_webpages  =", pub.publisher_webpages)
        print("error               =", pub.error)


class MyTestCase(unittest.TestCase):

        def test_01_init(self):
                print("\nTEST: publishers.__init__")
                pub = publishers(db)
                self.assertEqual(0, pub.used_id, "Bad used_id init")
                self.assertEqual(0, pub.used_name, "Bad used_name init")
                self.assertEqual(0, pub.used_trans_names, "Bad used_trans_names init")
                self.assertEqual(0, pub.used_webpages, "Bad used_webpages init")
                self.assertEqual(0, pub.used_note, "Bad used_note init")
                self.assertEqual('', pub.publisher_id, "Bad publisher_id init")
                self.assertEqual('', pub.publisher_name, "Bad publisher_name init")
                self.assertEqual([], pub.publisher_trans_names, "Bad publisher_trans_names init")
                self.assertEqual('', pub.publisher_note, "Bad publisher_note init")
                self.assertEqual([], pub.publisher_webpages, "Bad publisher_webpages init")
                self.assertEqual('', pub.error, "Bad error init")
                print("  Init state verified.")

        def test_02_load(self):
                print("\nTEST: publishers.load - by id")
                pub = publishers(db)
                pub.load(22)
                print_values = 1
                if print_values:
                        printClass(pub)
                else:
                        self.assertEqual(1, pub.used_id, "Bad used_id")
                        self.assertEqual(1, pub.used_name, "Bad used_name")
                        self.assertEqual('', pub.error, "Unexpected error")
                        print("  Received name:", pub.publisher_name)

        def test_03_load_not_found(self):
                print("\nTEST: publishers.load - not found")
                pub = publishers(db)
                pub.load(999999999)
                print("  Received error:", pub.error)
                self.assertEqual('Publisher record not found', pub.error, "Bad error message")
                self.assertEqual(0, pub.used_id, "used_id should remain 0")
                self.assertEqual(0, pub.used_name, "used_name should remain 0")

        def test_04_obj2xml(self):
                print("\nTEST: publishers.obj2xml")

                # TEST 1 - No used_id: returns '' (also prints "XML: pass")
                pub = publishers(db)
                xml = pub.obj2xml()
                print("  xml (no used_id):", xml)
                self.assertEqual('', xml, "obj2xml with no used_id should return ''")

                # TEST 2 - With used_id and name set
                pub2 = publishers(db)
                pub2.publisher_id = 22
                pub2.used_id = 1
                pub2.publisher_name = 'Ace Books'
                pub2.used_name = 1

                xml = pub2.obj2xml()
                print("  xml (with fields):", xml)
                self.assertIn('<UpdatePublisher>', xml, "Missing <UpdatePublisher>")
                self.assertIn('<PublisherId>22</PublisherId>', xml, "Missing PublisherId")
                self.assertIn('<PublisherName>Ace Books</PublisherName>', xml, "Missing PublisherName")
                self.assertIn('</UpdatePublisher>', xml, "Missing </UpdatePublisher>")

                # TEST 3 - used_id set but not used_name: name tag absent
                pub3 = publishers(db)
                pub3.publisher_id = 22
                pub3.used_id = 1
                xml3 = pub3.obj2xml()
                self.assertNotIn('<PublisherName>', xml3, "PublisherName should be absent when not used")

        def test_05_xml2obj(self):
                print("\nTEST: publishers.xml2obj")
                pub = publishers(db)

                xml = '<UpdatePublisher><PublisherName>Test Publisher</PublisherName></UpdatePublisher>'
                pub.xml2obj(xml)
                print("  publisher_name:", pub.publisher_name)
                print("  used_name:", pub.used_name)
                self.assertEqual(1, pub.used_name, "Bad used_name after xml2obj")
                self.assertEqual('Test Publisher', pub.publisher_name, "Bad publisher_name after xml2obj")

                # Absent element -> field not set
                pub2 = publishers(db)
                xml2 = '<UpdatePublisher></UpdatePublisher>'
                pub2.xml2obj(xml2)
                self.assertEqual(0, pub2.used_name, "used_name should stay 0 for absent element")
                self.assertEqual('', pub2.publisher_name, "publisher_name should stay '' for absent element")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
