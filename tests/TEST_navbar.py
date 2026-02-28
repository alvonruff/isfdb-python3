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
from navbar import *
import unittest

#
# This test suite was create to provide some coverage for the Python2 to
# Python3 upgrade. The purpose is to drive the interpreter through the
# main code line to help find any required API changes or deprecations.
#
# These tests are not intended to exhaustively test all of a
# function's operational requirements.
#
# NOTE: Every function in navbar.py prints to stdout. Tests redirect
# stdout to a StringIO buffer so that output is suppressed during the
# test run and can be inspected for key substrings.
#

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

class MyTestCase(unittest.TestCase):

        def test_01_PrintSearchBox_frontpage(self):
                print("\nTEST: PrintSearchBox - frontpage")
                output = captureOutput(PrintSearchBox, 'frontpage')
                print("  Output length:", len(output))
                self.assertIn('id="searchform"', output, "Missing searchform id")
                self.assertIn('<select name="type"', output, "Missing type select")
                self.assertIn('isfdb_logo.jpg', output, "Missing frontpage logo")
                self.assertNotIn('isfdb.gif', output, "Should not use small logo on frontpage")

        def test_02_PrintSearchBox_other(self):
                print("\nTEST: PrintSearchBox - non-frontpage")
                output = captureOutput(PrintSearchBox, 'title')
                print("  Output length:", len(output))
                self.assertIn('id="searchform"', output, "Missing searchform id")
                self.assertIn('isfdb.gif', output, "Missing small logo")
                self.assertNotIn('isfdb_logo.jpg', output, "Should not use large logo on non-frontpage")

        def test_03_PrintSearchBox_with_value(self):
                print("\nTEST: PrintSearchBox - with search value and type")
                output = captureOutput(PrintSearchBox, 'title', 'Stephen King', 'Name')
                print("  Output length:", len(output))
                self.assertIn('Stephen King', output, "Missing search value")
                self.assertIn('selected="selected"', output, "Missing selected option")

        def test_04_PrintOtherPages_frontpage(self):
                print("\nTEST: PrintOtherPages - frontpage")
                output = captureOutput(PrintOtherPages, 'frontpage')
                print("  Output length:", len(output))
                # Home Page link is suppressed on the frontpage
                self.assertNotIn('Home Page', output, "Home Page should be hidden on frontpage")
                self.assertIn('ISFDB Wiki', output, "Missing ISFDB Wiki link")
                self.assertIn('ISFDB FAQ', output, "Missing ISFDB FAQ link")
                self.assertIn('Author Directory', output, "Missing Author Directory link")
                self.assertIn('Award Directory', output, "Missing Award Directory link")

        def test_05_PrintOtherPages_non_frontpage(self):
                print("\nTEST: PrintOtherPages - non-frontpage")
                output = captureOutput(PrintOtherPages, 'title')
                print("  Output length:", len(output))
                self.assertIn('Home Page', output, "Missing Home Page link")
                self.assertNotIn('Moderator', output, "Moderator link should not appear for non-moderator")

        def test_06_PrintOtherPages_moderator(self):
                print("\nTEST: PrintOtherPages - moderator")
                output = captureOutput(PrintOtherPages, 'Moderator')
                print("  Output length:", len(output))
                self.assertIn('Moderator', output, "Missing Moderator link")

        def test_07_PrintNotLoggedIn(self):
                print("\nTEST: PrintNotLoggedIn")
                output = captureOutput(PrintNotLoggedIn, 'title.cgi', '1050')
                print("  Output length:", len(output))
                self.assertIn('Not Logged In', output, "Missing Not Logged In header")
                self.assertIn('Log In', output, "Missing Log In link")
                self.assertIn('Help Navigating', output, "Missing Help Navigating link")

        def test_08_PrintMessagesLink(self):
                print("\nTEST: PrintMessagesLink")
                # Use userid 0 (non-existent); SQLhasNewTalk should return false,
                # producing the standard (no new messages) link
                output = captureOutput(PrintMessagesLink, 0, 'TestUser')
                print("  Output length:", len(output))
                self.assertIn('My Messages', output, "Missing My Messages link")
                self.assertIn('TestUser', output, "Missing username in link")

        def test_09_PrintLoggedIn(self):
                print("\nTEST: PrintLoggedIn")
                # Use userid 0 (non-existent); SQLChangedVerifications should return false
                output = captureOutput(PrintLoggedIn, 0, 'TestUser')
                print("  Output length:", len(output))
                self.assertIn('Logged In As', output, "Missing Logged In As header")
                self.assertIn('TestUser', output, "Missing username")
                self.assertIn('Log Out', output, "Missing Log Out link")
                self.assertIn('My Preferences', output, "Missing My Preferences link")
                self.assertIn('My Recent Edits', output, "Missing My Recent Edits link")

        def test_10_PrintWikiPointer(self):
                print("\nTEST: PrintWikiPointer")
                # Use a submitter name with no wiki edits; output should be printed
                output = captureOutput(PrintWikiPointer, 'NonExistentTestUser99999')
                print("  Output length:", len(output))
                self.assertIn('must be approved by a moderator', output, "Missing moderator approval message")
                self.assertIn('Wiki Talk page', output, "Missing Wiki Talk page reference")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
