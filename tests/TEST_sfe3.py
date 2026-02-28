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
from sfe3 import *
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
# process                          - orchestrates network + DB writes; not safe to run in tests
# delete_newly_entered_unresolved_URLs - executes DELETE SQL
# download_URLs_from_SFE3          - makes live HTTP requests to sf-encyclopedia.com
# file_new_urls                    - executes INSERT SQL
# display_report                   - prints to stdout; also calls load_moderator_flag
# load_moderator_flag              - requires CGI login context
# print_table_columns              - requires self.user (set by load_moderator_flag)
# print_record                     - requires self.user (set by load_moderator_flag)

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

        def test_01_init(self):
                print("\nTEST: Sfe3.__init__")
                sfe = Sfe3()

                self.assertEqual({}, sfe.online_URLs, "Bad online_URLs init")
                self.assertEqual({}, sfe.unresolved_URLs, "Bad unresolved_URLs init")
                self.assertEqual({}, sfe.resolved_URLs, "Bad resolved_URLs init")
                self.assertEqual([], sfe.URLs_in_author_records, "Bad URLs_in_author_records init")
                self.assertEqual([], sfe.urls_to_delete_from_sfe3_authors, "Bad urls_to_delete init")
                self.assertEqual('sf-encyclopedia.com', sfe.host, "Bad host")
                self.assertEqual('https', sfe.protocol, "Bad protocol")
                self.assertIn(sfe.host, sfe.base_category_url, "host not in base_category_url")
                self.assertEqual(6, len(sfe.categories), "Bad categories length")
                self.assertIn('author', sfe.categories, "author missing from categories")
                print("  Init state verified.")

        def test_02_normalize_author_name_no_comma(self):
                print("\nTEST: Sfe3.normalize_author_name - no comma")
                sfe = Sfe3()

                # No comma: name returned as-is (stripped)
                value = sfe.normalize_author_name('Stephen King')
                print("  Received:", value)
                self.assertEqual('Stephen King', value, "Bad author name normalization")

                value = sfe.normalize_author_name('  H.G. Wells  ')
                print("  Received:", value)
                self.assertEqual('H.G. Wells', value, "Bad author name normalization")

        def test_03_normalize_author_name_with_comma(self):
                print("\nTEST: Sfe3.normalize_author_name - with comma")
                sfe = Sfe3()

                # TEST 1 - Simple last, first
                value = sfe.normalize_author_name('King, Stephen')
                print("  Received:", value)
                self.assertEqual('Stephen King', value, "Bad author name normalization")

                # TEST 2 - Single initial gets a period appended
                value = sfe.normalize_author_name('Asimov, I')
                print("  Received:", value)
                self.assertEqual('I. Asimov', value, "Bad author name normalization")

                # TEST 3 - Multi-part first name with single initial
                value = sfe.normalize_author_name('Clarke, Arthur C')
                print("  Received:", value)
                self.assertEqual('Arthur C. Clarke', value, "Bad author name normalization")

                # TEST 4 - Title abbreviation 'Dr' gets a period appended
                value = sfe.normalize_author_name('Smith, Dr')
                print("  Received:", value)
                self.assertEqual('Dr. Smith', value, "Bad author name normalization")

                # TEST 5 - Title abbreviation 'Mr' gets a period appended
                value = sfe.normalize_author_name('Jones, Mr')
                print("  Received:", value)
                self.assertEqual('Mr. Jones', value, "Bad author name normalization")

                # TEST 6 - Multi-word last name (two commas)
                value = sfe.normalize_author_name('Le Guin, Ursula K')
                print("  Received:", value)
                self.assertEqual('Ursula K. Le Guin', value, "Bad author name normalization")

        def test_04_reconcile_newly_entered_URLs(self):
                print("\nTEST: Sfe3.reconcile_newly_entered_URLs")
                sfe = Sfe3()

                sfe.URLs_in_author_records = ['url1', 'url2', 'url3']
                sfe.unresolved_URLs = {'url1': 'Author One', 'url2': 'Author Two', 'url4': 'Author Four'}

                sfe.reconcile_newly_entered_URLs()

                # url1 and url2 appear in both lists; they should be removed from unresolved
                # and added to urls_to_delete_from_sfe3_authors
                # url3 is not in unresolved; url4 is not in author_records
                print("  Remaining unresolved_URLs:", sfe.unresolved_URLs)
                self.assertEqual({'url4': 'Author Four'}, sfe.unresolved_URLs, "Bad unresolved_URLs after reconcile")

                print("  urls_to_delete:", sfe.urls_to_delete_from_sfe3_authors)
                self.assertEqual(2, len(sfe.urls_to_delete_from_sfe3_authors), "Bad urls_to_delete length")
                self.assertIn('url1', sfe.urls_to_delete_from_sfe3_authors, "url1 missing from urls_to_delete")
                self.assertIn('url2', sfe.urls_to_delete_from_sfe3_authors, "url2 missing from urls_to_delete")

        def test_05_remove_known_urls(self):
                print("\nTEST: Sfe3.remove_known_urls")
                sfe = Sfe3()

                sfe.online_URLs = {
                        'url1': 'Author One',   # in author records -> removed
                        'url2': 'Author Two',   # in unresolved -> removed
                        'url3': 'Author Three', # in resolved -> removed
                        'url4': 'Author Four',  # not in any list -> kept
                }
                sfe.URLs_in_author_records = ['url1']
                sfe.unresolved_URLs        = {'url2': 'Author Two'}
                sfe.resolved_URLs          = {'url3': 'Author Three'}

                captureOutput(sfe.remove_known_urls)  # suppress stdout

                print("  Remaining online_URLs:", sfe.online_URLs)
                self.assertEqual({'url4': 'Author Four'}, sfe.online_URLs, "Bad online_URLs after remove_known_urls")

        def test_06_count_of_unresolved(self):
                print("\nTEST: Sfe3.count_of_unresolved")
                sfe = Sfe3()
                count = sfe.count_of_unresolved()
                print("  Received count:", count)
                self.assertIsInstance(count, int, "count_of_unresolved should return an int")
                self.assertGreaterEqual(count, 0, "count_of_unresolved should be >= 0")

        def test_07_load_URLs_in_author_records(self):
                print("\nTEST: Sfe3.load_URLs_in_author_records")
                sfe = Sfe3()
                sfe.load_URLs_in_author_records()
                print("  Received URL count:", len(sfe.URLs_in_author_records))
                self.assertIsInstance(sfe.URLs_in_author_records, list, "URLs_in_author_records should be a list")
                self.assertGreater(len(sfe.URLs_in_author_records), 0, "URLs_in_author_records should not be empty")

        def test_08_print_header(self):
                print("\nTEST: Sfe3.print_header")
                sfe = Sfe3()
                output = captureOutput(sfe.print_header)
                print("  Output length:", len(output))
                self.assertIn('sf-encyclopedia.com', output, "Missing sf-encyclopedia.com in header")
                self.assertIn('https', output, "Missing protocol in header")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
