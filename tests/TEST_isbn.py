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
from isbn import *
import unittest

#
# This test suite was create to provide some coverage for the Python2 to
# Python3 upgrade. The purpose is to drive the interpreter through the
# main code line to help find any required API changes or deprecations.
#
# These tests are not intended to exhaustively test all of a
# function's operational requirements.
#
# NOTE: toISBN13() uses (checksum/10)*10 without int(), which is integer
# division in Python2 but float division in Python3. This is a known
# Python2->Python3 portability issue. Tests for toISBN13() and any
# function that calls it (isbnVariations, convertISBN for ISBN-10 inputs)
# may fail under Python3 until the issue is resolved.
#

class MyTestCase(unittest.TestCase):

        def test_01_ISBNValidFormat(self):
                print("\nTEST: ISBNValidFormat")

                # TEST 1 - Valid ISBN-10
                value = ISBNValidFormat('0441013597')
                print("  Received (valid ISBN-10):", value)
                self.assertEqual(1, value, "Bad ISBN format")

                # TEST 2 - Valid ISBN-13
                value = ISBNValidFormat('9780441013593')
                print("  Received (valid ISBN-13):", value)
                self.assertEqual(1, value, "Bad ISBN format")

                # TEST 3 - Valid ISBN-10 with hyphens
                value = ISBNValidFormat('0-441-01359-7')
                print("  Received (hyphenated ISBN-10):", value)
                self.assertEqual(1, value, "Bad ISBN format")

                # TEST 4 - Valid ISBN-10 with X check digit
                value = ISBNValidFormat('000000000X')
                print("  Received (X check digit):", value)
                self.assertEqual(1, value, "Bad ISBN format")

                # TEST 5 - Too short
                value = ISBNValidFormat('044101359')
                print("  Received (9 digits):", value)
                self.assertEqual(0, value, "Bad ISBN format")

                # TEST 6 - Wrong length (11 digits)
                value = ISBNValidFormat('04410135970')
                print("  Received (11 digits):", value)
                self.assertEqual(0, value, "Bad ISBN format")

                # TEST 7 - ISBN-13 with invalid prefix
                value = ISBNValidFormat('1230441013593')
                print("  Received (bad prefix):", value)
                self.assertEqual(0, value, "Bad ISBN format")

                # TEST 8 - Non-digit in body
                value = ISBNValidFormat('044101A597')
                print("  Received (non-digit in body):", value)
                self.assertEqual(0, value, "Bad ISBN format")

                # TEST 9 - Invalid last character
                value = ISBNValidFormat('044101359Z')
                print("  Received (bad last char):", value)
                self.assertEqual(0, value, "Bad ISBN format")

        def test_02_ISBNlength(self):
                print("\nTEST: ISBNlength")

                # TEST 1 - ISBN-10, no punctuation
                value = ISBNlength('0441013597')
                print("  Received (ISBN-10, no punct):", value)
                self.assertEqual(10, value, "Bad ISBN length")

                # TEST 2 - ISBN-13, no punctuation
                value = ISBNlength('9780441013593')
                print("  Received (ISBN-13, no punct):", value)
                self.assertEqual(13, value, "Bad ISBN length")

                # TEST 3 - ISBN-10 with spaces stripped correctly
                value = ISBNlength('0441013597')
                print("  Received (ISBN-10 spaces):", value)
                self.assertEqual(10, value, "Bad ISBN length")

                # TEST 4 - ISBN-10 with hyphens (known bug: second replace uses
                #          original isbn instead of stripped_isbn, so hyphens are
                #          not removed and the returned length includes them)
                value = ISBNlength('0-441-01359-7')
                print("  Received (ISBN-10 with hyphens):", value)
                self.assertEqual(10, value, "Bad ISBN length")

        def test_03_validISBN13(self):
                print("\nTEST: validISBN13")

                # TEST 1 - Valid ISBN-13
                value = validISBN13('9780441013593')
                print("  Received (valid):", value)
                self.assertEqual(1, value, "Bad ISBN-13 validation")

                # TEST 2 - Valid 979 prefix
                value = validISBN13('9791032305690')
                print("  Received (979 prefix):", value)
                self.assertEqual(1, value, "Bad ISBN-13 validation")

                # TEST 3 - Wrong length
                value = validISBN13('978044101359')
                print("  Received (12 digits):", value)
                self.assertEqual(0, value, "Bad ISBN-13 validation")

                # TEST 4 - Invalid prefix
                value = validISBN13('9800441013593')
                print("  Received (980 prefix):", value)
                self.assertEqual(0, value, "Bad ISBN-13 validation")

                # TEST 5 - Bad checksum
                value = validISBN13('9780441013590')
                print("  Received (bad checksum):", value)
                self.assertEqual(0, value, "Bad ISBN-13 validation")

                # TEST 6 - Non-integer in body
                value = validISBN13('97804410135X3')
                print("  Received (non-integer in body):", value)
                self.assertEqual(0, value, "Bad ISBN-13 validation")

        def test_04_validISBN(self):
                print("\nTEST: validISBN")

                # TEST 1 - Valid ISBN-10
                value = validISBN('0441013597')
                print("  Received (valid ISBN-10):", value)
                self.assertEqual(1, value, "Bad ISBN validation")

                # TEST 2 - Valid ISBN-10 with hyphens
                value = validISBN('0-441-01359-7')
                print("  Received (hyphenated ISBN-10):", value)
                self.assertEqual(1, value, "Bad ISBN validation")

                # TEST 3 - Valid ISBN-13
                value = validISBN('9780441013593')
                print("  Received (valid ISBN-13):", value)
                self.assertEqual(1, value, "Bad ISBN validation")

                # TEST 4 - Bad ISBN-10 checksum
                value = validISBN('0441013596')
                print("  Received (bad ISBN-10 checksum):", value)
                self.assertEqual(0, value, "Bad ISBN validation")

                # TEST 5 - Bad ISBN-13 checksum
                value = validISBN('9780441013590')
                print("  Received (bad ISBN-13 checksum):", value)
                self.assertEqual(0, value, "Bad ISBN validation")

                # TEST 6 - Non-integer in ISBN-10 body
                value = validISBN('044101A597')
                print("  Received (non-integer in body):", value)
                self.assertEqual(0, value, "Bad ISBN validation")

                # TEST 7 - Valid ISBN-10 with X check digit
                value = validISBN('059048348X')
                print("  Received (X check digit):", value)
                self.assertEqual(1, value, "Bad ISBN validation")

        def test_05_toISBN10(self):
                print("\nTEST: toISBN10")

                # TEST 1 - Valid conversion
                value = toISBN10('9780441013593')
                print("  Received:", value)
                self.assertEqual('0441013597', value, "Bad ISBN-10 conversion")

                # TEST 2 - Wrong input length; returned unchanged
                value = toISBN10('978044101359')
                print("  Received (12 digits, unchanged):", value)
                self.assertEqual('978044101359', value, "Bad ISBN-10 conversion")

        def test_06_toISBN13(self):
                print("\nTEST: toISBN13")
                # NOTE: toISBN13() uses (checksum/10)*10 without int(), causing
                # incorrect float arithmetic in Python3. This test will fail
                # under Python3 until the division is corrected to use int().

                # TEST 1 - Valid conversion
                value = toISBN13('0441013597')
                print("  Received:", value)
                self.assertEqual('9780441013593', value, "Bad ISBN-13 conversion")

                # TEST 2 - Wrong input length; returned unchanged
                value = toISBN13('044101359')
                print("  Received (9 digits, unchanged):", value)
                self.assertEqual('044101359', value, "Bad ISBN-13 conversion")

        def test_07_convertISBN(self):
                print("\nTEST: convertISBN")

                # TEST 1 - Invalid ISBN; returned unchanged
                value = convertISBN('0441013596')
                print("  Received (invalid ISBN):", value)
                self.assertEqual('0441013596', value, "Bad ISBN conversion")

                # TEST 2 - Special case: Tor ISBN-10 prefix 07653.
                # Uses hardcoded formatting rules (no DB lookup required).
                value = convertISBN('0765312344')
                print("  Received (Tor ISBN-10):", value)
                self.assertEqual('0-765-31234-4', value, "Bad ISBN conversion")

        def test_08_isbnVariations(self):
                print("\nTEST: isbnVariations")

                # TEST 1 - Empty string
                value = isbnVariations('')
                print("  Received (empty):", value)
                self.assertEqual([], value, "Bad ISBN variations")

                # TEST 2 - Invalid ISBN; only the original is returned
                value = isbnVariations('1234567890')
                print("  Received (invalid ISBN):", value)
                self.assertEqual(['1234567890'], value, "Bad ISBN variations")

                # TEST 3 - Normalize lowercase x to uppercase X
                value = isbnVariations('155192831x')
                print("  Received (lowercase x):", value)
                self.assertEqual('155192831X', value[0], "Bad ISBN variations normalization")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
