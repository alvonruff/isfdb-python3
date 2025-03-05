from __future__ import print_function
#
#     (C) COPYRIGHT 2007-2025   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1176 $
#     Date: $Date: 2024-05-02 19:26:24 -0400 (Thu, 02 May 2024) $

import string
from SQLparsing import *

######################################################################
# Format an ISBN with hyphen separators.  For information about the
# ranges, see https://www.isbn-international.org/range_file_generation
######################################################################
def convertISBN(isbn):

        if validISBN(isbn) == 0:
                return isbn

        stripped_isbn = isbn.replace('-','').replace(' ','')
        checksum = stripped_isbn[-1:]
        if len(stripped_isbn) == 13:
                core_isbn = stripped_isbn[:11]
        else:
                core_isbn = '978' + stripped_isbn[:8]

        # Exception for ISBN-10 starting with 07653 (Tor), 07656 (M.E. Sharpe)
        # 08123 (Great Source Education Group) and 08125 (Tor): until 2007 and
        # the transition to ISBN-13s, they displayed the second hyphen after
        # the 4th digit even though the official rules said they should have
        # done it after the 5th digit. The exception below addresses this issue
        # although some books published in 2006-2007 may have used
        # rules-compliant hypehnation.
        if len(stripped_isbn) == 10 and stripped_isbn[:5] in ('07653', '07656', '08123', '08125'):
                prefix_length = 4
                publisher_length = 3
        else:
                formatting_rules = SQLFindISBNformat(int(core_isbn))
                # If the ISBN is not in a recognized range, just add 1 hyphen before the checksum
                if not formatting_rules:
                        return '%s-%s' % (stripped_isbn[:-1], checksum)
                prefix_length = formatting_rules[0]
                publisher_length = formatting_rules[1]

        # Add hypens after 978/979, the prefix, the publisher and before the checksum
        if len(stripped_isbn) == 13:
                formatted_isbn = '%s-%s-%s-%s-%s' % (stripped_isbn[:3],
                                                     stripped_isbn[3:prefix_length],
                                                     stripped_isbn[prefix_length:prefix_length + publisher_length],
                                                     stripped_isbn[prefix_length + publisher_length: 12],
                                                     checksum)
        else:
                prefix_length = prefix_length - 3
                formatted_isbn = '%s-%s-%s-%s' % (stripped_isbn[:prefix_length],
                                                  stripped_isbn[prefix_length:prefix_length + publisher_length],
                                                  stripped_isbn[prefix_length + publisher_length: 9],
                                                  checksum)
        return formatted_isbn

def isbnVariations(original):
        ######################################################################
        # Given a candidate ISBN, builds an array of
        # possible legitimate variations:
        # - Always check for the candidate as it was supplied
        # - If the passed in candidate was a valid ISBN, then also search for:
        #   - The hyphenated forms of the ISBN-10 and the ISBN-13
        #   - The unhyphenated forms of the ISBN-10 and the ISBN-13
        ######################################################################
        variations = []
        if original:
                original = str.replace(original, 'x', 'X')
                # Always original
                variations.append(original)
                if validISBN(original):
                        collapsedOrig = str.replace(original, '-', '')
                        collapsedOrig = str.replace(collapsedOrig, ' ', '')
                        origLen = len(original)
                        collapsedLen = len(collapsedOrig)
                        if collapsedLen == origLen:
                                # original not punctuated, add punctuated
                                variations.append(convertISBN(original))
                        else:
                                # original punctuated, add unpunctuated
                                variations.append(collapsedOrig)
                        if collapsedLen == 10:
                                # ISBN-10; need ISBN-13
                                otherISBN = toISBN13(collapsedOrig)
                        else:
                                # ISBN-13; need ISBN-10
                                otherISBN = toISBN10(collapsedOrig)
                        variations.append(otherISBN)
                        variations.append(convertISBN(otherISBN))
        return variations

def ISBNValidFormat(isbn):
        # Returns 1 if the passed parameter follows the standard ISBN format, 0 otherwise
        # Note that only ISBN format is checked; checksum validation is not performed
        isbn = str.replace(str(isbn), '-', '')
        isbn = str.replace(isbn, ' ', '')
        if (len(isbn) != 10) and (len(isbn) != 13):
                return 0
        # ISBN-13s alway start with 978 or 979
        if (len(isbn) == 13) and (isbn[:3] not in ('978', '979')):
                return 0

        counter = 0
        while counter < len(isbn)-1:
                if isbn[counter] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        pass
                else:
                        return 0
                counter += 1

        if isbn[len(isbn)-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X']:
                pass
        else:
                return 0
        return 1

def ISBNlength(isbn):
        stripped_isbn = str.replace(isbn, '-', '')
        stripped_isbn = str.replace(isbn, ' ', '')
        return len(stripped_isbn)

def validISBN13(isbn):
        isbn = str.replace(isbn, '-', '')
        isbn = str.replace(isbn, ' ', '')
        if len(isbn) != 13:
                return 0

        if not isbn.startswith('978') and not isbn.startswith('979'):
                return 0

        try:
                testInt = int(isbn[0:12])
                newISBN = isbn[0:12]
        except:
                return 0

        sum1 = int(newISBN[0]) + int(newISBN[2]) + int(newISBN[4]) + int(newISBN[6]) + int(newISBN[8]) + int(newISBN[10])
        sum2 = int(newISBN[1]) + int(newISBN[3]) + int(newISBN[5]) + int(newISBN[7]) + int(newISBN[9]) + int(newISBN[11])
        checksum = sum1 + (sum2 * 3)
        remainder = checksum - (int(checksum/10)*10)
        if remainder:
                remainder = 10 - remainder
        newISBN = newISBN + str(remainder)
        if isbn == newISBN:
                return 1
        else:
                return 0

def validISBN(isbn):
        isbn = str.replace(str(isbn), '-', '')
        isbn = str.replace(isbn, ' ', '')
        if len(isbn) != 10:
                return validISBN13(isbn)

        # Look for non-integer catalog numbers
        try:
                testInt = int(isbn[0:9])
        except:
                return 0

        counter = 0
        sum = 0
        mult = 1
        while counter < 9:
                sum += (mult * int(isbn[counter]))
                mult += 1
                counter += 1
        remain = sum % 11
        if remain == 10:
                if isbn[9] != 'X':
                        return 0
        else:
                try:
                        lastdigit = int(isbn[9])
                except:
                        return 0
                if lastdigit != remain:
                        return 0
        return 1

def toISBN10(isbn13):
        if len(isbn13) != 13:
                return isbn13
        isbn = isbn13[3:12]
        counter = 0
        sum = 0
        mult = 1
        try:
                while counter < 9:
                        sum += (mult * int(isbn[counter]))
                        mult += 1
                        counter += 1
                remain = sum % 11
                if remain == 10:
                        isbn = isbn + 'X'
                else:
                        isbn = isbn + str(remain)
                return isbn
        except:
                return isbn13

def toISBN13(isbn):
        if len(isbn) != 10:
                return isbn
        newISBN = '978' + isbn[0:9]

        try:
                sum1 = int(newISBN[0]) + int(newISBN[2]) + int(newISBN[4]) + int(newISBN[6]) + int(newISBN[8]) + int(newISBN[10])
                sum2 = int(newISBN[1]) + int(newISBN[3]) + int(newISBN[5]) + int(newISBN[7]) + int(newISBN[9]) + int(newISBN[11])
                checksum = sum1 + (sum2 * 3)
                remainder = checksum - ((checksum/10)*10)
                if remainder:
                        remainder = 10 - remainder
                newISBN = newISBN + str(remainder)
                return newISBN
        except:
                return isbn
