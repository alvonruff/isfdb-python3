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
from viewers import *
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
# ContentTable.PrintTable         - prints to stdout
# ContentRow.AddCell              - requires xml_record and GetChildValue
# ContentRow.AddAuthorCell        - requires xml_record and GetChildValue
# ContentRow.AddTitleCell         - requires xml_record and SQLloadTitle
# ContentFragment.CheckValue      - requires SESSION.max_future_days and live submission context
# ContentFragment.NormalizeName   - requires SQLMultipleAuthors, SQLgetAuthorData
# ContentFragment.Title           - requires SQLloadTitle
# ContentFragment.MergeMethod     - requires GetChildValue
# SubmissionTable.PrintTable      - prints to stdout
# SubmissionFragment.GetValueFromMetadata    - requires valid submission XML context
# SubmissionFragment.GetAttributeValue       - requires valid submission XML context
# SubmissionFragment.GetMultiValueFromMetadata - requires valid submission XML context
# SubmissionViewer.DisplayXxx     - all print to stdout; DisplayTitleEdit smoke-tested below
# SubmissionViewer._InvalidSubmission - calls sys.exit(0)


##############################################################
# Mock/stub helper classes for pure-logic tests
##############################################################

class MockFragment:
        def __init__(self, value=''):
                self.value = value

class MockCell:
        """Minimal cell stub with a single fragment. Pass value=None for empty fragments."""
        def __init__(self, value=None):
                if value is not None:
                        self.fragments = [MockFragment(value)]
                else:
                        self.fragments = []


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

        def test_01_ContentTable_init(self):
                print("\nTEST: ContentTable.__init__")

                class MockSubmission: pass
                table = ContentTable(MockSubmission())

                self.assertEqual('', table.caption, "Bad caption init")
                self.assertEqual('generic_table', table.css_table, "Bad css_table init")
                self.assertEqual('warn', table.css_warning, "Bad css_warning init")
                self.assertEqual('-', table.empty_cell, "Bad empty_cell init")
                self.assertEqual([], table.headers, "Bad headers init")
                self.assertEqual([], table.rows, "Bad rows init")
                self.assertEqual(0, table.warnings_exist, "Bad warnings_exist init")
                self.assertIsInstance(table.fragment_separator, str, "fragment_separator should be str")
                print("  ContentTable init state verified.")

        def test_02_ContentFragment_AddWarning(self):
                print("\nTEST: ContentFragment._AddWarning")

                class MockSubmission: pass
                table = ContentTable(MockSubmission())
                row = ContentRow(table)
                cell = ContentCell(row)
                fragment = ContentFragment(cell)

                # Warning propagates to the row's warnings list and sets table.warnings_exist
                fragment._AddWarning('Test warning')
                print("  row.warnings:", row.warnings)
                self.assertIn('Test warning', row.warnings, "Warning not in row.warnings")
                self.assertEqual(1, table.warnings_exist, "warnings_exist should be 1")

                # A duplicate warning should not be added a second time
                fragment._AddWarning('Test warning')
                self.assertEqual(1, len(row.warnings), "Duplicate warning should not be added")

                # An empty warning string should be ignored
                fragment._AddWarning('')
                self.assertEqual(1, len(row.warnings), "Empty warning should be ignored")

                # A second distinct warning is accepted
                fragment._AddWarning('Second warning')
                self.assertEqual(2, len(row.warnings), "Second warning should be added")
                print("  Warning propagation verified.")

        def test_03_SubmissionTable_init(self):
                print("\nTEST: SubmissionTable.__init__")

                class MockSubmission: pass
                table = SubmissionTable(MockSubmission())

                self.assertEqual(0, table.display_diffs, "Bad display_diffs init")
                self.assertEqual(0, table.display_warnings, "Bad display_warnings init")
                self.assertEqual('generic_table', table.css_table, "Bad css_table init")
                self.assertEqual(1, table.update, "Bad update init")
                self.assertEqual(0, table.suppress_warnings, "Bad suppress_warnings init")
                self.assertEqual([], table.rows, "Bad rows init")
                self.assertEqual([], table.headers, "Bad headers init")
                self.assertEqual('keep', table.css_active_background, "Bad css_active_background init")
                self.assertEqual('drop', table.css_superseeded_background, "Bad css_superseeded_background init")
                print("  SubmissionTable init state verified.")

        def test_04_SubmissionRow_AddWarning(self):
                print("\nTEST: SubmissionRow.AddWarning")

                class MockSubmission: pass
                table = SubmissionTable(MockSubmission())
                row = SubmissionRow(table, 'Test Label')

                row.AddWarning('Warning 1')
                row.AddWarning('Warning 2')
                print("  row.warnings:", row.warnings)
                self.assertIn('Warning 1', row.warnings, "Warning 1 missing")
                self.assertIn('Warning 2', row.warnings, "Warning 2 missing")
                self.assertEqual(2, len(row.warnings), "Bad warnings length")

                # Empty string should be ignored
                row.AddWarning('')
                self.assertEqual(2, len(row.warnings), "Empty warning should not be added")
                print("  AddWarning behavior verified.")

        def test_05_SubmissionRow_CreateDiffsFromLists(self):
                print("\nTEST: SubmissionRow._CreateDiffsFromLists")

                class MockSubmission: pass
                table = SubmissionTable(MockSubmission())
                row = SubmissionRow(table, 'Test Label')

                # TEST 1 - before=['a','b'], after=['b','c'] -> 'a' removed, 'c' added
                row._CreateDiffsFromLists(['a', 'b'], ['b', 'c'])
                print("  Received diffs:", row.diffs)
                self.assertIn('- a', row.diffs, "Missing '- a' diff")
                self.assertIn('+ c', row.diffs, "Missing '+ c' diff")
                self.assertNotIn('- b', row.diffs, "Shared element 'b' should not appear as removed")
                self.assertNotIn('+ b', row.diffs, "Shared element 'b' should not appear as added")
                self.assertEqual(2, len(row.diffs), "Bad diffs length")

                # TEST 2 - Identical lists -> no diffs
                row._CreateDiffsFromLists(['x', 'y'], ['x', 'y'])
                print("  Diffs for identical lists:", row.diffs)
                self.assertEqual([], row.diffs, "Identical lists should produce no diffs")

                # TEST 3 - Empty before list -> only additions
                row._CreateDiffsFromLists([], ['new'])
                print("  Diffs for empty before:", row.diffs)
                self.assertEqual(['+ new'], row.diffs, "Empty before should produce only additions")

        def test_06_SubmissionRow_CellValuesDiffer(self):
                print("\nTEST: SubmissionRow._CellValuesDiffer")

                class MockSubmission: pass
                table = SubmissionTable(MockSubmission())
                row = SubmissionRow(table, 'Test Label')

                # TEST 1 - Empty left_cell fragments -> 0
                row.left_cell = MockCell()
                row.right_cell = MockCell('NOVEL')
                value = row._CellValuesDiffer()
                print("  Empty left fragments:", value)
                self.assertEqual(0, value, "Empty left_cell fragments should return 0")

                # TEST 2 - Empty right_cell fragments -> 0
                row.left_cell = MockCell('NOVEL')
                row.right_cell = MockCell()
                value = row._CellValuesDiffer()
                print("  Empty right fragments:", value)
                self.assertEqual(0, value, "Empty right_cell fragments should return 0")

                # TEST 3 - Same values -> 0
                row.left_cell = MockCell('NOVEL')
                row.right_cell = MockCell('NOVEL')
                value = row._CellValuesDiffer()
                print("  Same values:", value)
                self.assertEqual(0, value, "Same values should return 0")

                # TEST 4 - Different values -> 1
                row.left_cell = MockCell('NOVEL')
                row.right_cell = MockCell('SHORTFICTION')
                value = row._CellValuesDiffer()
                print("  Different values:", value)
                self.assertEqual(1, value, "Different values should return 1")

        def test_07_SubmissionRow_TitleTypeMismatch(self):
                print("\nTEST: SubmissionRow._TitleTypeMismatch")

                class MockSubmission: pass
                table = SubmissionTable(MockSubmission())
                row = SubmissionRow(table, 'Test Label')

                # TEST 1 - Same types -> 0
                row.left_cell = MockCell('NOVEL')
                row.right_cell = MockCell('NOVEL')
                value = row._TitleTypeMismatch()
                print("  Same types:", value)
                self.assertEqual(0, value, "Same types should return 0")

                # TEST 2 - SERIAL + NOVEL -> 0 (allowed)
                row.left_cell = MockCell('SERIAL')
                row.right_cell = MockCell('NOVEL')
                value = row._TitleTypeMismatch()
                print("  SERIAL+NOVEL:", value)
                self.assertEqual(0, value, "SERIAL+NOVEL should return 0")

                # TEST 3 - SERIAL + SHORTFICTION -> 0 (allowed)
                row.left_cell = MockCell('SERIAL')
                row.right_cell = MockCell('SHORTFICTION')
                value = row._TitleTypeMismatch()
                print("  SERIAL+SHORTFICTION:", value)
                self.assertEqual(0, value, "SERIAL+SHORTFICTION should return 0")

                # TEST 4 - INTERIORART + COVERART -> 0 (allowed)
                row.left_cell = MockCell('INTERIORART')
                row.right_cell = MockCell('COVERART')
                value = row._TitleTypeMismatch()
                print("  INTERIORART+COVERART:", value)
                self.assertEqual(0, value, "INTERIORART+COVERART should return 0")

                # TEST 5 - COVERART + INTERIORART -> 0 (allowed)
                row.left_cell = MockCell('COVERART')
                row.right_cell = MockCell('INTERIORART')
                value = row._TitleTypeMismatch()
                print("  COVERART+INTERIORART:", value)
                self.assertEqual(0, value, "COVERART+INTERIORART should return 0")

                # TEST 6 - NOVEL + SHORTFICTION -> 1 (uncommon mismatch)
                row.left_cell = MockCell('NOVEL')
                row.right_cell = MockCell('SHORTFICTION')
                value = row._TitleTypeMismatch()
                print("  NOVEL+SHORTFICTION:", value)
                self.assertEqual(1, value, "NOVEL+SHORTFICTION should return 1")

                # TEST 7 - Empty parent_type -> 0
                row.left_cell = MockCell('NOVEL')
                row.right_cell = MockCell('')
                value = row._TitleTypeMismatch()
                print("  Empty parent type:", value)
                self.assertEqual(0, value, "Empty parent type should return 0")

        def test_08_SubmissionViewer_smoke(self):
                print("\nTEST: SubmissionViewer smoke (DisplayTitleEdit, submission 6522377)")
                output = captureOutput(SubmissionViewer, 'DisplayTitleEdit', 6522377)
                print("  Output length:", len(output))
                self.assertGreater(len(output), 0, "SubmissionViewer produced no output")
                self.assertIn('<table', output, "Missing table in output")
                self.assertIn('Field', output, "Missing Field header in output")
                self.assertIn('Title', output, "Missing Title row in output")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
