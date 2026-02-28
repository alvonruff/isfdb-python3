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

from xml.dom import minidom
from SQLparsing import *
from isfdb import *
from library import *
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
# UNTESTED Functions
##############################################################
# IsfdbFieldStorage             - requires input from cgi
# ISFDBExternalRedirect         - calls sys.exit(0)
# ISFDBLocalRedirect            - calls sys.exit(0)
# ISFDBHostCorrection           - This doesn't work anywhere but at isfdb.org - Needs HTMLLOC ??
# ISFDBLinkNoName               - This just calls ISFDBLink; nothing to test
# ISFDBprintSubmissionRecord    - prints to stdout
# ISFDBprintSubmissionTable     - prints to stdout
# ISFDBprintTime                - prints to stdout
# ISFDBSubmissionDoc            - Sufficiently tested via ISFDBSubmissionDisplayType
# ISFDBSubmissionType           - Sufficiently tested via ISFDBSubmissionDisplayType
# ISFDBTable                    - prints to stdout
# ISFDBtranslatedReports        - Too simple to test. Returns a static dictionary.
# ISFDBUnicodeTranslation       - Too simple to test. Returns a static dictionary.
# ISFDBunpublishedDate          - Sufficiently tested vie ISFDBconvertYear
# ISFDBWikiPage                 - Too simple to test. One line of code.
# ISFDBWikiTemplate             - Too simple to test. One line of code.
#   7 LIBbuildRecordList
#   3 LIBsameParentAuthors
# printRecordID                 - prints to stdout
# WikiLink                      - Too simple to test. One line of code.

class MyTestCase(unittest.TestCase):

        def test_01_AdvSearchLink(self):
                print("\nTEST: AdvSearchLink")

                # TEST 1 - Author
                link = AdvSearchLink(('TYPE', 'Author'))
                expected = '<a href="https://%s/cgi-bin/adv_search_results.cgi?START=0&amp;T=Y&amp;A=u">' % HTMLLOC
                print("  Received:", link)
                self.assertEqual(expected, link, "Bad Link")

                # TEST 2 - Publication
                link = AdvSearchLink(('TYPE', 'Publication'))
                expected = '<a href="https://%s/cgi-bin/adv_search_results.cgi?START=0&amp;T=Y&amp;P=u">' % HTMLLOC
                print("  Received:", link)
                self.assertEqual(expected, link, "Bad Link")

                # TEST 3 - Author Directory
                params = (('USE_1', 'author_lastname'), ('OPERATOR_1', 'starts_with'), ('TERM_1', 'key'), ('ORDERBY', 'author_lastname'), ('TYPE', 'Author'), ('C', 'AND'))
                link = AdvSearchLink(params)
                expected = '<a href="https://%s/cgi-bin/adv_search_results.cgi?START=0&amp;USE_1=author_lastname&amp;OPERATOR_1=starts_with&amp;TERM_1=key&amp;ORDERBY=author_lastname&amp;TYPE=Author&amp;C=AND">' % HTMLLOC
                print("  Received:", link)
                self.assertEqual(expected, link, "Bad Link")

        def test_02_AutoVivification(self):
                print("\nTEST: AutoVivification")
                test = AutoVivification()
                test[1][2][3][4] = 'xxx'
                test[1][2][3][5] = 'yyy'
                value = test[1][2][3][4]
                self.assertEqual('xxx', value, "Bad Dict")

        def test_03_AwardLevelDescription(self):
                print("\nTEST: AwardLevelDescription")
                aw_level   = '12'
                aw_type_id = 28         # Locus Poll
                descr = AwardLevelDescription(aw_level, aw_type_id)
                print("  Received:", descr)
                self.assertEqual('12', descr, "Bad Description")

                aw_level   = '2'
                aw_type_id = 9         # BSFA
                descr = AwardLevelDescription(aw_level, aw_type_id)
                print("  Received:", descr)
                self.assertEqual('Nomination', descr, "Bad Description")

                aw_level   = '1'
                aw_type_id = 9         # BSFA
                descr = AwardLevelDescription(aw_level, aw_type_id)
                print("  Received:", descr)
                self.assertEqual('Win', descr, "Bad Description")

                aw_level   = '92'
                aw_type_id = 9         # BSFA
                descr = AwardLevelDescription(aw_level, aw_type_id)
                print("  Received:", descr)
                self.assertEqual('Preliminary Nominees', descr, "Bad Description")

        def test_04_buildRecordID(self):
                print("\nTEST: buildRecordID")
                record_type = 'Title'
                record_id   = 123
                user_id     = 0
                output = buildRecordID(record_type, record_id, user_id)
                print("  Received:", output)
                expected = '<span class="recordID"><b>Title Record # </b>123</span>'
                self.assertEqual(expected, output, "Bad record ID")

                record_type = 'Title'
                record_id   = 123
                user_id     = 1
                output = buildRecordID(record_type, record_id, user_id)
                print("  Received:", output)
                expected = '<span class="recordID"><b>Title Record # </b>123 [<a href="https://%s/cgi-bin/edit/edittitle.cgi?123">Edit</a>] [<a href="https://%s/cgi-bin/title_history.cgi?123">Edit History</a>]</span>' % (HTMLLOC, HTMLLOC)
                self.assertEqual(expected, output, "Bad record ID")

        def test_05_ConvertPageNumber(self):
                print("\nTEST: ConvertPageNumber")
                page = 'fc'
                output = ConvertPageNumber(page)
                print("  Received:", output)
                group = output[0]
                npn   = output[1]
                dec   = output[2]
                self.assertEqual(2, group, "Bad page number")
                self.assertEqual(1, npn, "Bad page number")
                self.assertEqual('', dec, "Bad page number")

                page = 'rj'
                output = ConvertPageNumber(page)
                print("  Received:", output)
                group = output[0]
                npn   = output[1]
                dec   = output[2]
                self.assertEqual(2, group, "Bad page number")
                self.assertEqual(2, npn, "Bad page number")
                self.assertEqual('', dec, "Bad page number")

                page = 'fep'
                output = ConvertPageNumber(page)
                print("  Received:", output)
                group = output[0]
                npn   = output[1]
                dec   = output[2]
                self.assertEqual(2, group, "Bad page number")
                self.assertEqual(3, npn, "Bad page number")
                self.assertEqual('', dec, "Bad page number")

                page = 'bp'
                output = ConvertPageNumber(page)
                print("  Received:", output)
                group = output[0]
                npn   = output[1]
                dec   = output[2]
                self.assertEqual(2, group, "Bad page number")
                self.assertEqual(4, npn, "Bad page number")
                self.assertEqual('', dec, "Bad page number")

                page = 'ep'
                output = ConvertPageNumber(page)
                print("  Received:", output)
                group = output[0]
                npn   = output[1]
                dec   = output[2]
                self.assertEqual(5, group, "Bad page number")
                self.assertEqual(1, npn, "Bad page number")
                self.assertEqual('', dec, "Bad page number")

                page = 'bep'
                output = ConvertPageNumber(page)
                print("  Received:", output)
                group = output[0]
                npn   = output[1]
                dec   = output[2]
                self.assertEqual(5, group, "Bad page number")
                self.assertEqual(2, npn, "Bad page number")
                self.assertEqual('', dec, "Bad page number")

                page = 'bc'
                output = ConvertPageNumber(page)
                print("  Received:", output)
                group = output[0]
                npn   = output[1]
                dec   = output[2]
                self.assertEqual(5, group, "Bad page number")
                self.assertEqual(3, npn, "Bad page number")
                self.assertEqual('', dec, "Bad page number")

                page = 'xii.503'
                output = ConvertPageNumber(page)
                print("  Received:", output)
                group = output[0]
                npn   = output[1]
                dec   = output[2]
                self.assertEqual(3, group, "Bad page number")
                self.assertEqual(12, npn, "Bad page number")
                self.assertEqual('503', dec, "Bad page number")

        def test_06_dict_to_in_clause(self):
                print("\nTEST: dict_to_in_clause")
                dict1 = {"a": 1, "b": 2, "c": 3}
                dict2 = {"d": 4, "e": 5, "f": 6}
                output = dict_to_in_clause(dict1, dict2)
                print("  Received:", output)
                # It would be interesting to investigate why this is true:
                if PYTHONVER == "python2":
                        expected = "'a','c','b','e','d','f'"
                else:
                        expected = "'a','b','c','d','e','f'"
                self.assertEqual(expected, output, "Bad in clause")

        def test_07_FormatAuthors(self):
                print("\nTEST: FormatAuthors")
                authors = ['xxx', 'yyy']
                output = FormatAuthors(authors)
                print("  Received:", output)
                expected = '<a href="https://%s/cgi-bin/ea.cgi?x" dir="ltr">x</a> <b>and</b> <a href="https://%s/cgi-bin/ea.cgi?y" dir="ltr">y</a>' % (HTMLLOC, HTMLLOC)
                self.assertEqual(expected, output, "Bad author format")

        def test_08_FormatExternalIDSite(self):
                print("\nTEST: FormatExternalIDSite")

                sites = SQLLoadIdentifierSites()
                type_id = 21
                id_value = 27280
                formatted_id = FormatExternalIDSite(sites, type_id, id_value)
                print("  Received:", formatted_id)
                self.assertEqual(27280, formatted_id, "Bad formatted ID")

        def test_09_FormatExternalIDType(self):
                print("\nTEST: FormatExternalIDType")

                ext_ids = SQLLoadIdentifiers(504)
                id_types = SQLLoadIdentifierTypes()

                # Build the identifiers dictionary
                self_identifiers = {}
                for ext_id in ext_ids:
                        type_id = ext_id[IDENTIFIER_TYPE_ID]
                        type_name = id_types[type_id][0]
                        type_full_name = id_types[type_id][1]
                        id_value = ext_id[IDENTIFIER_VALUE]
                        if type_name not in self_identifiers:
                                self_identifiers[type_name] = {}
                        self_identifiers[type_name][id_value] = (type_id, type_full_name)

                types = SQLLoadIdentifierTypes()
                for type_name in sorted(self_identifiers.keys()):
                        formatted_line = FormatExternalIDType(type_name, types)

                expected = '<abbr class="template" title="Online Computer Library Center">OCLC/WorldCat</abbr>:'
                print("  Received:", formatted_line)
                self.assertEqual(expected, formatted_line, "Bad formatted Line")

        def test_10_FormatNote(self):
                print("\nTEST: FormatNote")

                # NOTE: This is not an exhaustive test

                # TEST 1 - Short
                test_note = 'Some text.{{BREAK}} Some more text.<br>Final text.'
                test_id   = 504
                test_class = 'Note'
                formatted_note = FormatNote(test_note, test_class, 'short', test_id, 'Series')
                print("  Received:", formatted_note)
                expected = '<div class="notes"><b>Note:</b> Some text. ... <big><a class="inverted" href="https://%s/cgi-bin/note.cgi?Series+504">view\n                        full Note</a></big></div>' % HTMLLOC
                self.assertEqual(expected, formatted_note, "Bad formatted Note")

                # TEST 2 - Full
                formatted_note = FormatNote(test_note, test_class, 'full', test_id, 'Series')
                print("  Received:", formatted_note)
                expected = '<div class="notes"><b>Note:</b> Some text. Some more text.\nFinal text.</div>'
                self.assertEqual(expected, formatted_note, "Bad formatted Note")

                # TEST 3 - Template
                test_note = '{{A|Jules Verne}}'
                test_id   = 504
                test_class = 'Note'
                formatted_note = FormatNote(test_note, test_class, 'short', test_id, 'Series')
                print("  Received:", formatted_note)
                formatted_note = formatted_note.replace(HTMLLOC, 'HTMLLOC')
                expected = '<div class="notes"><b>Note:</b> <a href="https://HTMLLOC/cgi-bin/se.cgi?arg=Jules%20Verne&amp;type=Name&amp;mode=exact">Jules Verne</a></div>'
                self.assertEqual(expected, formatted_note, "Bad formatted Note")

        def test_11_GetChildValue(self):
                print("\nTEST: GetChildValue")
                xmlData = """<?xml version="1.0" encoding="UTF-8"?>
                          <record>
                              <book category="cooking">
                                  <title lang="en">Bogus Title</title>
                                  <author>Target Author</author>
                                  <year>2026</year>
                              </book>
                          </record>"""
                xmlDoc = minidom.parseString(xmlData)
                child = GetChildValue(xmlDoc, 'author')
                print("  Received:", child)
                expected = "Target Author"
                self.assertEqual(expected, child, "Bad Child")

        def test_12_GetElementValue(self):
                print("\nTEST: GetElementValue")
                xmlData = """<?xml version="1.0" encoding="UTF-8"?>
                          <record>
                              <title lang="en">Target Title</title>
                              <author>Bogus Author</author>
                              <year>2026</year>
                          </record>"""
                xmlDoc = minidom.parseString(xmlData)
                doc2   = xmlDoc.getElementsByTagName('record')
                value = GetElementValue(doc2, 'title')
                print("  Received:", value)
                expected = "Target Title"
                self.assertEqual(expected, value, "Bad Value")

        def test_13_getPubContentList(self):
                print("\nTEST: getPubContentList")
                pub_content_list = getPubContentList(24052)

                pageNo = pub_content_list[2][3]
                print("  Received page number:", pageNo)
                expected = "viii"
                self.assertEqual(expected, pageNo, "Bad Page Number")

                pageNo = pub_content_list[3][3]
                print("  Received page number:", pageNo)
                expected = "xi"
                self.assertEqual(expected, pageNo, "Bad Page Number")

        def test_14_getSortedTitlesInPub(self):
                print("\nTEST: getSortedTitlesInPub")
                pub_titles = getSortedTitlesInPub(24052)

                title = pub_titles[5][1]
                print("  Received title:", title)
                expected = "Graveyard Shift"
                self.assertEqual(expected, title, "Bad Title")

                title = pub_titles[8][1]
                print("  Received title:", title)
                expected = "The Mangler"
                self.assertEqual(expected, title, "Bad Title")

        def test_15_getSubjectLink(self):
                print("\nTEST: getSubjectLink")
                xmlData = """<?xml version="1.0" encoding="UTF-8"?>
                          <record>
                              <subject lang="en">Test Subject</subject>
                          </record>"""
                xmlDoc = minidom.parseString(xmlData)
                doc2   = xmlDoc.getElementsByTagName('record')
                record = [0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 123]
                subj_link = getSubjectLink(record, doc2, 7)

                print("  Received subject link:", subj_link)
                expected = '<a href="https://%s/cgi-bin/pl.cgi?123"></a>' % HTMLLOC
                self.assertEqual(expected, subj_link[0], "Bad Subject Link")

        def test_16_IMDBLink(self):
                print("\nTEST: IMDBLink")
                imdb_link = IMDBLink("TestCode")
                print("  Received IMDB link:", imdb_link)
                expected = '<a href="https://www.imdb.com/title/TestCode/" target="_blank">IMDB</a>'
                self.assertEqual(expected, imdb_link, "Bad IMDB Link")

        def test_17_invalidURL(self):
                print("\nTEST: invalidURL")

                valid = invalidURL("http://www.isfdb.org")
                print("  Received URL eval:", valid)
                expected = ''
                self.assertEqual(expected, valid, "Bad URL eval")

                valid = invalidURL("ftp://www.isfdb.org")
                print("  Received URL eval:", valid)
                expected = ' URLs must start with http or https'
                self.assertEqual(expected, valid, "Bad URL eval")

                valid = invalidURL("http://")
                print("  Received URL eval:", valid)
                expected = ' Domain name not specified'
                self.assertEqual(expected, valid, "Bad URL eval")

        def test_18_invalidURLcharacters(self):
                print("\nTEST: invalidURLcharacters")

                valid = invalidURLcharacters("http://<isfdb>", "testField", "bogus")
                print("  Received URL eval:", valid)
                expected = 'Software issue - contact the site administrator'
                self.assertEqual(expected, valid, "Bad URL eval")

                valid = invalidURLcharacters("http://<isfdb>", "testField", "unescaped")
                print("  Received URL eval:", valid)
                expected = 'Invalid testField. < not allowed in testFields'
                self.assertEqual(expected, valid, "Bad URL eval")

                valid = invalidURLcharacters("http://<isfdb>", "testField", "escaped")
                print("  Received URL eval:", valid)
                expected = ''
                self.assertEqual(expected, valid, "Bad URL eval")

        def test_19_ISFDBAuthorError(self):
                print("\nTEST: ISFDBAuthorError")
                authError = ISFDBAuthorError("Bob+Dave")
                print("  Received author error:", authError)
                expected = 'Plus signs are currently not allowed in author names'
                self.assertEqual(expected, authError, "Bad author error")

        def test_20_ISFDBAuthorInAuthorList(self):
                print("\nTEST: ISFDBAuthorInAuthorList")
                title_authors = []
                title_authors.append("xxx")
                title_authors.append("yyy")
                title_authors.append("zzz")

                value = ISFDBAuthorInAuthorList('aaa', title_authors)
                print("  Received search value:", value)
                expected = 0
                self.assertEqual(expected, value, "Bad author search")

                value = ISFDBAuthorInAuthorList('yyy', title_authors)
                print("  Received search value:", value)
                expected = 1
                self.assertEqual(expected, value, "Bad author search")

        def test_21_ISFDBBadUnicodePatternMatch(self):
                print("\nTEST: ISFDBBadUnicodePatternMatch")
                value = ISFDBBadUnicodePatternMatch('publisher_name')
                #print(value)
                expected = "publisher_name like binary"
                expected_len = len(expected)
                value = value[:expected_len]
                print("  Received substring:", value)
                self.assertEqual(expected, value, "Bad unicode pattern")

        def test_22_ISFDBCompare2Dates(self):
                print("\nTEST: ISFDBCompare2Dates")

                value = ISFDBCompare2Dates('2026-01-01', '2025-01-01')
                print("  Received value:", value)
                expected = 0
                self.assertEqual(expected, value, "Bad date compare")

                value = ISFDBCompare2Dates('1999-01-01', '2026-01-01')
                print("  Received value:", value)
                expected = 1
                self.assertEqual(expected, value, "Bad date compare")

                value = ISFDBCompare2Dates('2026-02-01', '2026-01-01')
                print("  Received value:", value)
                expected = 0
                self.assertEqual(expected, value, "Bad date compare")

                value = ISFDBCompare2Dates('2026-01-01', '2026-02-01')
                print("  Received value:", value)
                expected = 1
                self.assertEqual(expected, value, "Bad date compare")

                value = ISFDBCompare2Dates('2026-02-02', '2026-02-01')
                print("  Received value:", value)
                expected = 0
                self.assertEqual(expected, value, "Bad date compare")

                value = ISFDBCompare2Dates('2026-02-01', '2026-02-02')
                print("  Received value:", value)
                expected = 1
                self.assertEqual(expected, value, "Bad date compare")

                value = ISFDBCompare2Dates('2026-00-01', '2026-02-02')
                print("  Received value:", value)
                expected = 0
                self.assertEqual(expected, value, "Bad date compare")

                value = ISFDBCompare2Dates('2026-20-01', '2026-00-00')
                print("  Received value:", value)
                expected = 2
                self.assertEqual(expected, value, "Bad date compare")

                value = ISFDBCompare2Dates('2026-02-00', '2026-02-01')
                print("  Received value:", value)
                expected = 0
                self.assertEqual(expected, value, "Bad date compare")

                value = ISFDBCompare2Dates('2026-02-02', '2026-02-00')
                print("  Received value:", value)
                expected = 2
                self.assertEqual(expected, value, "Bad date compare")

        def test_23_ISFDBCompareTwoTitles(self):
                print("\nTEST: ISFDBCompareTwoTitles")
                title1 = SQLloadTitle(1050)
                title2 = SQLloadTitle(22035)
                title2[TITLE_TITLE] = "The Talisman"
                #print(title1)
                #print(title2)

                value = ISFDBCompareTwoTitles(title1, title2, 0)
                print("  Received value:", value)
                expected = 1
                self.assertEqual(expected, value, "Bad title compare")

                title2[TITLE_TITLE] = "The Talismen"
                value = ISFDBCompareTwoTitles(title1, title2, 2)
                print("  Received value:", value)
                expected = 1
                self.assertEqual(expected, value, "Bad title compare")

        def test_24_ISFDBconvertDate(self):
                print("\nTEST: ISFDBconvertDate")

                value = ISFDBconvertDate('0000-00-00')
                print("  Received value:", value)
                expected = 'date unknown'
                self.assertEqual(expected, value, "Bad date conversion")

                value = ISFDBconvertDate('8888-00-00')
                print("  Received value:", value)
                expected = 'unpublished'
                self.assertEqual(expected, value, "Bad date conversion")

                value = ISFDBconvertDate('9999-00-00')
                print("  Received value:", value)
                expected = 'forthcoming'
                self.assertEqual(expected, value, "Bad date conversion")

                value = ISFDBconvertDate('2026-02-28')
                print("  Received value:", value)
                expected = 'Feb 2026'
                self.assertEqual(expected, value, "Bad date conversion")

        def test_25_ISFDBconvertForthcoming(self):
                print("\nTEST: ISFDBconvertForthcoming")

                value = ISFDBconvertForthcoming('2026-12-25')
                print("  Received value:", value)
                expected = 'Dec 25 2026'
                self.assertEqual(expected, value, "Bad forthcoming conversion")

                value = ISFDBconvertForthcoming('2026-12-00')
                print("  Received value:", value)
                expected = 'Dec 2026'
                self.assertEqual(expected, value, "Bad forthcoming conversion")

                value = ISFDBconvertForthcoming('2026-00-00')
                print("  Received value:", value)
                expected = '2026'
                self.assertEqual(expected, value, "Bad forthcoming conversion")

        def test_26_ISFDBconvertYear(self):
                print("\nTEST: ISFDBconvertYear")

                value = ISFDBconvertYear('0000-00-00')
                print("  Received value:", value)
                expected = 'unknown'
                self.assertEqual(expected, value, "Bad year conversion")

                value = ISFDBconvertYear('8888-00-00')
                print("  Received value:", value)
                expected = 'unpublished'
                self.assertEqual(expected, value, "Bad year conversion")

                value = ISFDBconvertYear('9999-00-00')
                print("  Received value:", value)
                expected = 'forthcoming'
                self.assertEqual(expected, value, "Bad year conversion")

                value = ISFDBconvertYear('2026-02-02')
                print("  Received value:", value)
                expected = '2026'
                self.assertEqual(expected, value, "Bad year conversion")

        def test_27_ISFDBDate(self):
                print("\nTEST: ISFDBDate")

                value = ISFDBDate()
                print("  Received value:", value)
                expected = datetime.today().strftime('%Y-%m-%d')
                self.assertEqual(expected, value, "Bad date")

        def test_28_ISFDBdaysFromToday(self):
                print("\nTEST: ISFDBdaysFromToday")

                from datetime import date, timedelta

                value = ISFDBdaysFromToday('8888-00-00')
                print("  Received value:", value)
                expected = 0
                self.assertEqual(expected, value, "Bad days from today")

                value = ISFDBdaysFromToday('0000-00-00')
                print("  Received value:", value)
                expected = 0
                self.assertEqual(expected, value, "Bad days from today")

                today = date.today()
                tomorrow = str(today + timedelta(days=1))
                value = ISFDBdaysFromToday(tomorrow)
                print("  Received value:", value)
                expected = 1
                self.assertEqual(expected, value, "Bad days from today")

        def test_29_ISFDBDifferentAuthorLists(self):
                print("\nTEST: ISFDBDifferentAuthorLists")

                list1 = ('aaa', 'bbb', 'ccc')
                list2 = ('aaa', 'bbb', 'ccc')
                value = ISFDBDifferentAuthorLists(list1, list2)
                print("  Received value:", value)
                expected = 0
                self.assertEqual(expected, value, "Bad diff author list")

                list1 = ('aaa', 'bbb', 'ccc')
                list2 = ('aaa', 'bbb', 'ccd')
                value = ISFDBDifferentAuthorLists(list1, list2)
                print("  Received value:", value)
                expected = 1
                self.assertEqual(expected, value, "Bad diff author list")

        def test_30_ISFDBDifferentAuthorStrings(self):
                print("\nTEST: ISFDBDifferentAuthorStrings")

                list1 = 'aaa+bbb+ccc'
                list2 = 'aaa+bbb+ccc'
                value = ISFDBDifferentAuthorStrings(list1, list2)
                print("  Received value:", value)
                expected = 0
                self.assertEqual(expected, value, "Bad diff author strings")

                list1 = 'aaa+bbb+ccc'
                list2 = 'aaa+bbb+ccd'
                value = ISFDBDifferentAuthorStrings(list1, list2)
                print("  Received value:", value)
                expected = 1
                self.assertEqual(expected, value, "Bad diff author strings")

        def test_31_ISFDBFormatAllAuthors(self):
                print("\nTEST: ISFDBFormatAllAuthors")

                value = ISFDBFormatAllAuthors(1050)
                print("  Received value:", value)
                expected = '<a href="https://%s/cgi-bin/ea.cgi?70" dir="ltr">Stephen King</a> <b>and</b> <a href="https://%s/cgi-bin/ea.cgi?1031" dir="ltr">Peter Straub</a>' % (HTMLLOC, HTMLLOC)
                self.assertEqual(expected, value, "Bad author format")

        def test_32_ISFDBScan(self):
                print("\nTEST: ISFDBScan")

                pubId = 48332
                pub = SQLGetPubById(pubId)
                value = ISFDBScan(pubId, pub[PUB_IMAGE])
                print("  Received value:", value)
                expected = '<a href="https://%s/cgi-bin/pl.cgi?48332" dir="ltr"><img src="https://m.media-amazon.com/images/I/5188HF2BRSL.jpg" alt="Image" class="scans"></a>' % (HTMLLOC)
                self.assertEqual(expected, value, "Bad cover scan")

        def test_33_ISFDBFormatImage(self):
                print("\nTEST: ISFDBFormatImage")

                pubId = 48332
                pub = SQLGetPubById(pubId)
                value = ISFDBFormatImage(pub[PUB_IMAGE], pubId)
                print("  Received value:", value)
                expected = '<a href="https://%s/cgi-bin/pl.cgi?48332" dir="ltr"><img src="https://m.media-amazon.com/images/I/5188HF2BRSL.jpg" alt="Image" class="tallscan"></a><br>[https://m.media-amazon.com/images/I/5188HF2BRSL.jpg]' % (HTMLLOC)
                self.assertEqual(expected, value, "Bad format image")

                pubId = 39149
                pub = SQLGetPubById(pubId)
                value = ISFDBFormatImage(pub[PUB_IMAGE], pubId)
                print("  Received value:", value)
                expected = '<a href="https://%s/cgi-bin/pl.cgi?39149" dir="ltr"><img src="https://%s/wiki/images/5/56/BKTG17165.jpg" alt="Image" class="tallscan"></a><br>[http://www.isfdb.org/wiki/images/5/56/BKTG17165.jpg]' % (HTMLLOC, HTMLLOC)
                self.assertEqual(expected, value, "Bad format image")

        def test_34_ISFDBLink(self):
                print("\nTEST: ISFDBLink")
                value = ISFDBLink('ea.cgi', 70, "uncredited")
                print("  Received value:", value)
                expected = "uncredited"
                self.assertEqual(expected, value, "Bad link")

                value = ISFDBLink('ea.cgi', 70, "xxx")
                print("  Received value:", value)
                expected = '<a href="https://%s/cgi-bin/ea.cgi?70" dir="ltr">xxx</a>' % (HTMLLOC)
                self.assertEqual(expected, value, "Bad link")

        def test_35_ISFDBMouseover(self):
                print("\nTEST: ISFDBMouseover")

                mouseover_values = ('xxx', 'yyy')
                display_value = 'zzz'
                value = ISFDBMouseover(mouseover_values, display_value)
                print("  Received value:", value)
                expected = '<td><div class="tooltip tooltipright">zzz<sup class="mouseover">?</sup><span class="tooltiptext tooltipnarrow tooltipright">xxx<br>yyy</span></div></td>'
                self.assertEqual(expected, value, "Bad Mouseover")

        def test_36_ISFDBnormalizeAuthor(self):
                print("\nTEST: ISFDBnormalizeAuthor")

                author = "  Stephen         King       "
                value = ISFDBnormalizeAuthor(author)
                print("  Received value:", value)
                expected = "Stephen King"
                self.assertEqual(expected, value, "Bad author norm")

                author = '"Doc" Savage'
                value = ISFDBnormalizeAuthor(author)
                print("  Received value:", value)
                expected = "'Doc' Savage"
                self.assertEqual(expected, value, "Bad author norm")

        def test_37_ISFDBnormalizeDate(self):
                print("\nTEST: ISFDBnormalizeDate")

                # TEST 1 - Big Fat Zero
                testDate = '0'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('0000-00-00', newDate, "Bad Date")

                # TEST 2 - YYYY
                testDate = '2026'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('2026-00-00', newDate, "Bad Date")

                # TEST 3 - YYYY-MM
                testDate = '2026-03'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('2026-03-00', newDate, "Bad Date")

                # TEST 4 - YYYY-MM-D
                testDate = '2026-03-1'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('0000-00-00', newDate, "Bad Date")

                # TEST 5 - YYYYMMDD
                testDate = '20260301'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('0000-00-00', newDate, "Bad Date")

                # TEST 6 - xxxx-MM-DD
                testDate = 'xxxx-03-01'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('0000-00-00', newDate, "Bad Date")

                # TEST 7 - YYYY-xx-DD
                testDate = '2026-xx-01'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('0000-00-00', newDate, "Bad Date")

                # TEST 8 - YYYY-MM-xx
                testDate = '2026-03-xx'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('0000-00-00', newDate, "Bad Date")

                # TEST 9 - 7777-MM-DD
                testDate = '7777-03-01'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('0000-00-00', newDate, "Bad Date")

                # TEST 10 - YYYY-13-DD
                testDate = '2026-13-01'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('0000-00-00', newDate, "Bad Date")

                # TEST 11 - YYYY-MM-32
                testDate = '2026-12-32'
                newDate = ISFDBnormalizeDate(testDate)
                print("  Received:", newDate)
                self.assertEqual('0000-00-00', newDate, "Bad Date")

        def test_37_ISFDBPossibleDuplicates(self):
                print("\nTEST: ISFDBPossibleDuplicates")

                # This is not fully testable, as it requires an actual duplicate.
                # So we'll just test for same title, same author, and show that it
                # doesn't flag that instance as a dup.
                titlerec = SQLloadTitle(2914974)
                value = ISFDBPossibleDuplicates(titlerec)
                print("  Received:", value)
                expected = []
                self.assertEqual(expected, value, "Bad Dup")

        def test_38_ISFDBPrice(self):
                print("\nTEST: ISFDBPrice")

                value = ISFDBPrice("P$")
                print("  Received:", value)
                expected = '<div class="tooltip tooltipright">P$<sup class="mouseover">?</sup><span class="tooltiptext tooltipnarrow tooltipright">P$: Portuguese escudo. ISO code: PTE</span></div>'
                self.assertEqual(expected, value, "Bad Price")

        def test_39_ISFDBPubFormat(self):
                print("\nTEST: ISFDBPubFormat")

                value = ISFDBPubFormat('hc')
                print("  Received:", value)
                expected = '<div class="tooltip tooltipright">hc<sup class="mouseover">?</sup><span class="tooltiptext tooltipnarrow tooltipright">Hardcover. Used for all hardbacks of any size.</span></div>'
                self.assertEqual(expected, value, "Bad Format")

        def test_39_ISFDBSubmissionDisplayType(self):
                print("\nTEST: ISFDBSubmissionDisplayType")

                submission = SQLloadSubmission(6522377)
                sub_data = submission[SUB_DATA]
                sub_type = submission[SUB_TYPE]
                xml_tag = SUBMAP[sub_type][1]
                doc2 = ISFDBSubmissionDoc(sub_data, xml_tag)
                display_tag = ISFDBSubmissionType(xml_tag, sub_type, doc2)
                value = ISFDBSubmissionDisplayType(display_tag, xml_tag, sub_type)
                print("  Received:", value)
                expected = 'Title Update'
                self.assertEqual(expected, value, "Bad Submission")

        def test_40_ISFDBText(self):
                print("\nTEST: ISFDBText")

                testInput = "xxx < yyy"
                value = ISFDBText(testInput)
                print("  Received:", value)
                expected = 'xxx &lt; yyy'
                self.assertEqual(expected, value, "Bad Escape")

                testInput = "xxx > yyy"
                value = ISFDBText(testInput)
                print("  Received:", value)
                expected = 'xxx &gt; yyy'
                self.assertEqual(expected, value, "Bad Escape")

                testInput = "xxx & yyy"
                value = ISFDBText(testInput)
                print("  Received:", value)
                expected = 'xxx &amp; yyy'
                self.assertEqual(expected, value, "Bad Escape")

        def test_41_XMLescape(self):
                print("\nTEST: XMLescape")

                # TEST 1 - & escaping
                value = XMLescape('a & b')
                print("  Received:", value)
                self.assertEqual('a &amp; b', value, "Bad & escape")

                # TEST 2 - single quote (non-compliant) -> &rsquo;
                value = XMLescape("it's")
                print("  Received:", value)
                self.assertEqual("it&rsquo;s", value, "Bad ' escape")

                # TEST 3 - single quote (compliant) -> &apos;
                value = XMLescape("it's", compliant=1)
                print("  Received:", value)
                self.assertEqual("it&apos;s", value, "Bad compliant ' escape")

                # TEST 4 - double quote -> &quot;
                value = XMLescape('"quoted"')
                print("  Received:", value)
                self.assertEqual('&quot;quoted&quot;', value, 'Bad " escape')

                # TEST 5 - < and > escaping
                value = XMLescape('<tag>')
                print("  Received:", value)
                self.assertEqual('&lt;tag&gt;', value, "Bad < > escape")

                # TEST 6 - \r removal
                value = XMLescape('a\rb')
                print("  Received:", value)
                self.assertEqual('ab', value, "Bad \\r removal")

                # TEST 7 - whitespace stripping
                value = XMLescape('  spaces  ')
                print("  Received:", value)
                self.assertEqual('spaces', value, "Bad whitespace strip")

        def test_42_XMLunescape(self):
                print("\nTEST: XMLunescape")

                # TEST 1 - &amp; -> &
                value = XMLunescape('a &amp; b')
                print("  Received:", value)
                self.assertEqual('a & b', value, "Bad &amp; unescape")

                # TEST 2 - &rsquo; -> ' (non-compliant)
                value = XMLunescape("it&rsquo;s")
                print("  Received:", value)
                self.assertEqual("it's", value, "Bad &rsquo; unescape")

                # TEST 3 - &apos; -> ' (compliant)
                value = XMLunescape("it&apos;s", compliant=1)
                print("  Received:", value)
                self.assertEqual("it's", value, "Bad &apos; unescape")

                # TEST 4 - &quot; -> "
                value = XMLunescape('&quot;quoted&quot;')
                print("  Received:", value)
                self.assertEqual('"quoted"', value, "Bad &quot; unescape")

                # TEST 5 - &lt; and &gt;
                value = XMLunescape('a &lt; b &gt; c')
                print("  Received:", value)
                self.assertEqual('a < b > c', value, "Bad &lt; &gt; unescape")

        def test_43_XMLunescape2(self):
                print("\nTEST: XMLunescape2")

                # TEST 1 - &rsquo; -> '
                value = XMLunescape2("it&rsquo;s")
                print("  Received:", value)
                self.assertEqual("it's", value, "Bad &rsquo; unescape2")

                # TEST 2 - &quot; -> "
                value = XMLunescape2('&quot;text&quot;')
                print("  Received:", value)
                self.assertEqual('"text"', value, "Bad &quot; unescape2")

                # TEST 3 - \r removal
                value = XMLunescape2('a\rb')
                print("  Received:", value)
                self.assertEqual('ab', value, "Bad \\r removal in unescape2")

        def test_44_TagPresent(self):
                print("\nTEST: TagPresent")
                xmlData = """<?xml version="1.0"?><record><title>Test</title></record>"""
                xmlDoc = minidom.parseString(xmlData)

                # TEST 1 - Tag present
                value = TagPresent(xmlDoc, 'title')
                print("  Received (tag present):", value)
                self.assertEqual(1, value, "Tag should be present")

                # TEST 2 - Tag absent
                value = TagPresent(xmlDoc, 'author')
                print("  Received (tag absent):", value)
                self.assertEqual(0, value, "Tag should be absent")

        def test_45_normalizeInput(self):
                print("\nTEST: normalizeInput")

                # TEST 1 - '. . .' -> '...'
                value = normalizeInput('. . .')
                print("  Received ('. . .'):", value)
                self.assertEqual('...', value, "Bad '. . .' normalization")

                # TEST 2 - '. . . .' -> '....'
                value = normalizeInput('. . . .')
                print("  Received ('. . . .'):", value)
                self.assertEqual('....', value, "Bad '. . . .' normalization")

                # TEST 3 - double space -> single space
                value = normalizeInput('a  b')
                print("  Received ('a  b'):", value)
                self.assertEqual('a b', value, "Bad double-space normalization")

        def test_46_replaceDict(self):
                print("\nTEST: replaceDict")

                # TEST 1 - Key substitution
                retval = 'hello world'
                replace_dict = {'hello': 'goodbye', 'world': 'earth'}
                value = replaceDict(retval, replace_dict)
                print("  Received:", value)
                self.assertEqual('goodbye earth', value, "Bad replaceDict substitution")

                # TEST 2 - Empty dict leaves string unchanged
                value = replaceDict('unchanged', {})
                print("  Received (empty dict):", value)
                self.assertEqual('unchanged', value, "replaceDict with empty dict should be unchanged")

        def test_47_roman2int(self):
                print("\nTEST: roman2int")

                # TEST 1 - Simple values
                self.assertEqual(1, roman2int('i'), "i != 1")
                self.assertEqual(5, roman2int('v'), "v != 5")
                self.assertEqual(10, roman2int('x'), "x != 10")

                # TEST 2 - Subtractive notation
                self.assertEqual(4, roman2int('iv'), "iv != 4")
                self.assertEqual(9, roman2int('ix'), "ix != 9")
                self.assertEqual(14, roman2int('xiv'), "xiv != 14")
                self.assertEqual(42, roman2int('xlii'), "xlii != 42")

                # TEST 3 - Uppercase input
                self.assertEqual(12, roman2int('XII'), "XII != 12")

                # TEST 4 - Invalid character -> 0
                value = roman2int('z')
                print("  Received (invalid 'z'):", value)
                self.assertEqual(0, value, "Invalid roman numeral should return 0")

        def test_48_EscapeParams(self):
                print("\nTEST: EscapeParams")

                # TEST 1 - Single param, no special chars
                params = (('TYPE', 'Author'),)
                value = EscapeParams(params)
                print("  Received:", value)
                self.assertIn('&amp;TYPE=Author', value, "Missing TYPE param")

                # TEST 2 - Multiple params, space encoded as %20
                params = (('USE_1', 'author_lastname'), ('TERM_1', 'John Doe'))
                value = EscapeParams(params)
                print("  Received:", value)
                self.assertIn('&amp;USE_1=author_lastname', value, "Missing USE_1 param")
                self.assertIn('John%20Doe', value, "Space should be encoded as %20")

        def test_49_suspectUnicodePatternMatch(self):
                print("\nTEST: suspectUnicodePatternMatch")

                value = suspectUnicodePatternMatch('title_title')
                print("  Received:", value)
                self.assertIn('title_title', value, "Field name missing from pattern")
                self.assertIn('&#699;', value, "&#699; missing from pattern")
                self.assertIn('&#700;', value, "&#700; missing from pattern")

        def test_50_list_to_in_clause(self):
                print("\nTEST: list_to_in_clause")

                # TEST 1 - Empty list
                value = list_to_in_clause([])
                print("  Received (empty):", value)
                self.assertEqual('', value, "Empty list should return ''")

                # TEST 2 - One item
                value = list_to_in_clause(['abc'])
                print("  Received (one item):", value)
                self.assertEqual("'abc'", value, "Bad single-item in clause")

                # TEST 3 - Multiple items
                value = list_to_in_clause(['a', 'b', 'c'])
                print("  Received (three items):", value)
                self.assertEqual("'a','b','c'", value, "Bad multi-item in clause")

        def test_51_FormatExternalIDLink(self):
                print("\nTEST: FormatExternalIDLink")

                url = 'https://example.com/item/%s'
                value = FormatExternalIDLink(url, '12345', 'Example Site')
                print("  Received:", value)
                expected = '<a href="https://example.com/item/12345" target="_blank">Example Site</a>'
                self.assertEqual(expected, value, "Bad FormatExternalIDLink")

        def test_52_Portable_urllib(self):
                print("\nTEST: Portable_urllib_quote / Portable_urllib_unquote")

                # TEST 1 - Quote space as %20
                value = Portable_urllib_quote('hello world')
                print("  Received (quote):", value)
                self.assertEqual('hello%20world', value, "Bad urllib quote")

                # TEST 2 - Unquote %20 as space
                value = Portable_urllib_unquote('hello%20world')
                print("  Received (unquote):", value)
                self.assertEqual('hello world', value, "Bad urllib unquote")

                # TEST 3 - Round-trip
                original = 'Stephen King & Peter Straub'
                quoted = Portable_urllib_quote(original)
                unquoted = Portable_urllib_unquote(quoted)
                print("  Received (round-trip):", unquoted)
                self.assertEqual(original, unquoted, "Bad urllib round-trip")

        def test_53_popularNonLatinLanguages(self):
                print("\nTEST: popularNonLatinLanguages")

                # TEST 1 - 'titles' returns 5 languages with correct report IDs
                results = popularNonLatinLanguages('titles')
                print("  Received (titles):", results)
                self.assertEqual(5, len(results), "Should have 5 languages")
                lang_dict = dict(results)
                self.assertEqual(138, lang_dict['Bulgarian'], "Bad Bulgarian titles report ID")
                self.assertEqual(142, lang_dict['Russian'], "Bad Russian titles report ID")

                # TEST 2 - 'pubs' returns correct report IDs
                results = popularNonLatinLanguages('pubs')
                lang_dict = dict(results)
                self.assertEqual(162, lang_dict['Bulgarian'], "Bad Bulgarian pubs report ID")

                # TEST 3 - 'series' returns correct report IDs
                results = popularNonLatinLanguages('series')
                lang_dict = dict(results)
                self.assertEqual(258, lang_dict['Bulgarian'], "Bad Bulgarian series report ID")

        def test_54_transliteratedReports(self):
                print("\nTEST: transliteratedReports")

                # TEST 1 - 'titles' returns 13 languages with correct report IDs
                results = transliteratedReports('titles')
                print("  Received (titles) count:", len(results))
                self.assertEqual(13, len(results), "Should have 13 languages")
                lang_dict = dict(results)
                self.assertEqual(124, lang_dict['Bulgarian'], "Bad Bulgarian titles report ID")
                self.assertEqual(134, lang_dict['Russian'], "Bad Russian titles report ID")

                # TEST 2 - 'pubs' returns correct report IDs
                results = transliteratedReports('pubs')
                lang_dict = dict(results)
                self.assertEqual(148, lang_dict['Bulgarian'], "Bad Bulgarian pubs report ID")

                # TEST 3 - 'authors' returns correct report IDs
                results = transliteratedReports('authors')
                lang_dict = dict(results)
                self.assertEqual(169, lang_dict['Bulgarian'], "Bad Bulgarian authors report ID")

        def test_55_isfdbUI(self):
                print("\nTEST: isfdbUI")
                ui = isfdbUI()

                # TEST 1 - goodHtmlTagsPresent
                value = ui.goodHtmlTagsPresent('<b>bold</b>')
                print("  goodHtmlTagsPresent (<b>bold</b>):", value)
                self.assertEqual(1, value, "Should detect valid HTML tag")
                value = ui.goodHtmlTagsPresent('plain text')
                print("  goodHtmlTagsPresent (plain text):", value)
                self.assertEqual(0, value, "Should not detect HTML tag in plain text")

                # TEST 2 - badHtmlTagsPresent
                value = ui.badHtmlTagsPresent('<b>bold</b>')
                print("  badHtmlTagsPresent (<b>bold</b>):", value)
                self.assertFalse(value, "Valid HTML tag should not flag as bad")
                value = ui.badHtmlTagsPresent('<b>bold</b><script>bad</script>')
                print("  badHtmlTagsPresent (with <script>):", value)
                self.assertEqual(1, value, "Unrecognized HTML tag should flag as bad")

                # TEST 3 - mismatchedBraces
                value = ui.mismatchedBraces('{{BREAK}}')
                print("  mismatchedBraces (matched):", value)
                self.assertEqual('', value, "Matched braces should return ''")
                value = ui.mismatchedBraces('{open only')
                print("  mismatchedBraces (unmatched):", value)
                self.assertEqual('Mismatched braces', value, "Unmatched braces should return error")

                # TEST 4 - mismatchedDoubleQuote
                value = ui.mismatchedDoubleQuote('"matched"')
                print("  mismatchedDoubleQuote (matched):", value)
                self.assertEqual('', value, "Matched quotes should return ''")
                value = ui.mismatchedDoubleQuote('"unmatched')
                print("  mismatchedDoubleQuote (unmatched):", value)
                self.assertEqual('Mismatched double quotes', value, "Unmatched quote should return error")

                # TEST 5 - mismatchedHtmlTagsPresent
                value = ui.mismatchedHtmlTagsPresent('<b>matched</b>')
                print("  mismatchedHtmlTagsPresent (matched):", value)
                self.assertEqual(0, value, "Matched HTML tags should return 0")
                value = ui.mismatchedHtmlTagsPresent('<b>unmatched')
                print("  mismatchedHtmlTagsPresent (unmatched):", value)
                self.assertEqual(1, value, "Unmatched HTML tags should return 1")

                # TEST 6 - invalidHtmlInNotes
                value = ui.invalidHtmlInNotes('<b>valid</b>')
                print("  invalidHtmlInNotes (valid):", value)
                self.assertEqual('', value, "Valid HTML should return ''")
                value = ui.invalidHtmlInNotes('<script>bad</script>')
                print("  invalidHtmlInNotes (bad tag):", value)
                self.assertEqual('Unrecognized HTML tag(s) present', value, "Unrecognized tag should return error")
                value = ui.invalidHtmlInNotes('<li>item</li>')
                print("  invalidHtmlInNotes (li without ul):", value)
                self.assertEqual('HTML tags: li without ul or ol', value, "li without ul should return error")
                value = ui.invalidHtmlInNotes('<b>unmatched')
                print("  invalidHtmlInNotes (mismatched):", value)
                self.assertEqual('Mismatched HTML tags', value, "Mismatched tags should return error")

                # TEST 7 - unrecognizedTemplate
                value = ui.unrecognizedTemplate('{{BREAK}}')
                print("  unrecognizedTemplate (BREAK):", value)
                self.assertEqual('', value, "Standard template should return ''")
                value = ui.unrecognizedTemplate('{{UNKNOWN_TEMPLATE_XYZ_999}}')
                print("  unrecognizedTemplate (unknown):", value)
                self.assertEqual('Unrecognized template', value, "Unknown template should return error")

        def test_56_WikiExists(self):
                print("\nTEST: WikiExists")
                value = WikiExists()
                print("Received:", value)
                self.assertEqual(1, value, "Wiki should exist")

        def test_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()


if __name__ == '__main__':
        unittest.main()
