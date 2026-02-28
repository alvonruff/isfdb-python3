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
from recognizeddomainClass import *
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


def printClass(rd):
        print("used_domain_id                    =", rd.used_domain_id)
        print("used_domain_name                  =", rd.used_domain_name)
        print("used_linking_allowed              =", rd.used_linking_allowed)
        print("used_linking_allowed_display      =", rd.used_linking_allowed_display)
        print("used_explicit_link_required       =", rd.used_explicit_link_required)
        print("used_explicit_link_required_display =", rd.used_explicit_link_required_display)
        print("used_required_segment             =", rd.used_required_segment)
        print("used_site_name                    =", rd.used_site_name)
        print("used_site_url                     =", rd.used_site_url)
        print("domain_id                         =", rd.domain_id)
        print("domain_name                       =", rd.domain_name)
        print("linking_allowed                   =", rd.linking_allowed)
        print("linking_allowed_display           =", rd.linking_allowed_display)
        print("explicit_link_required            =", rd.explicit_link_required)
        print("explicit_link_required_display    =", rd.explicit_link_required_display)
        print("required_segment                  =", rd.required_segment)
        print("site_name                         =", rd.site_name)
        print("site_url                          =", rd.site_url)
        print("error                             =", rd.error)


class MyTestCase(unittest.TestCase):

        def test_01_init(self):
                print("\nTEST: RecognizedDomain.__init__")
                rd = RecognizedDomain()
                self.assertEqual(0, rd.used_domain_id, "Bad used_domain_id init")
                self.assertEqual(0, rd.used_domain_name, "Bad used_domain_name init")
                self.assertEqual(0, rd.used_explicit_link_required, "Bad used_explicit_link_required init")
                self.assertEqual(0, rd.used_explicit_link_required_display, "Bad used_explicit_link_required_display init")
                self.assertEqual(0, rd.used_linking_allowed, "Bad used_linking_allowed init")
                self.assertEqual(0, rd.used_linking_allowed_display, "Bad used_linking_allowed_display init")
                self.assertEqual(0, rd.used_required_segment, "Bad used_required_segment init")
                self.assertEqual(0, rd.used_site_name, "Bad used_site_name init")
                self.assertEqual(0, rd.used_site_url, "Bad used_site_url init")
                self.assertEqual('', rd.domain_id, "Bad domain_id init")
                self.assertEqual('', rd.domain_name, "Bad domain_name init")
                self.assertEqual(0, rd.explicit_link_required, "Bad explicit_link_required init")
                self.assertEqual('No', rd.explicit_link_required_display, "Bad explicit_link_required_display init")
                self.assertEqual(0, rd.linking_allowed, "Bad linking_allowed init")
                self.assertEqual('No', rd.linking_allowed_display, "Bad linking_allowed_display init")
                self.assertEqual('', rd.required_segment, "Bad required_segment init")
                self.assertEqual('', rd.site_name, "Bad site_name init")
                self.assertEqual('', rd.site_url, "Bad site_url init")
                self.assertEqual('', rd.error, "Bad error init")
                print("  Init state verified.")

        def test_02_load(self):
                print("\nTEST: RecognizedDomain.load - by id")
                rd = RecognizedDomain()
                rd.load(1)
                print_values = 1
                if print_values:
                        printClass(rd)
                else:
                        self.assertEqual(1, rd.used_domain_id, "Bad used_domain_id")
                        self.assertEqual(1, rd.used_domain_name, "Bad used_domain_name")
                        self.assertEqual('', rd.error, "Unexpected error")
                        print("  Received domain_name:", rd.domain_name)

        def test_03_load_id_zero(self):
                print("\nTEST: RecognizedDomain.load - id=0 (falsy)")
                rd = RecognizedDomain()
                rd.load(0)
                # Unlike Template/VerificationSource, this class sets an error on falsy id
                print("  error:", rd.error)
                self.assertEqual('No Recognized Domain ID specified.', rd.error, "Bad error for falsy id")
                self.assertEqual(0, rd.used_domain_id, "used_domain_id should remain 0")
                self.assertEqual('', rd.domain_id, "domain_id should remain ''")

        def test_04_load_not_found(self):
                print("\nTEST: RecognizedDomain.load - id not found")
                rd = RecognizedDomain()
                rd.load(999999999)
                # used_domain_id and domain_id are set before the DB lookup fails
                print("  used_domain_id:", rd.used_domain_id)
                print("  domain_id:", rd.domain_id)
                print("  error:", rd.error)
                self.assertEqual(1, rd.used_domain_id, "used_domain_id should be set before the lookup")
                self.assertEqual(999999999, rd.domain_id, "domain_id should be stored before the lookup")
                self.assertEqual('Specified Recognized Domain ID does not exist.', rd.error, "Bad error for missing id")
                self.assertEqual(0, rd.used_domain_name, "used_domain_name should remain 0")

        def test_05_CheckYesNoValue(self):
                print("\nTEST: RecognizedDomain._CheckYesNoValue")
                rd = RecognizedDomain()

                # TEST 1 - 'Yes' is valid
                value = rd._CheckYesNoValue('Yes', 'Test Field')
                print("  Received ('Yes'):", value)
                self.assertEqual('Yes', value, "Bad return for 'Yes'")
                self.assertEqual('', rd.error, "error should not be set for 'Yes'")

                # TEST 2 - 'No' is valid
                value = rd._CheckYesNoValue('No', 'Test Field')
                print("  Received ('No'):", value)
                self.assertEqual('No', value, "Bad return for 'No'")
                self.assertEqual('', rd.error, "error should not be set for 'No'")

                # TEST 3 - Invalid value sets error
                rd._CheckYesNoValue('Maybe', 'Test Field')
                print("  error (invalid value):", rd.error)
                self.assertIn('Test Field', rd.error, "Field name missing from error message")
                self.assertIn('Yes', rd.error, "Expected values missing from error message")
                self.assertIn('No', rd.error, "Expected values missing from error message")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
