#!_PYTHONLOC
#
#     (C) COPYRIGHT 2025    Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 717 $
#     Date: $Date: 2021-08-28 11:04:26 -0400 (Sat, 28 Aug 2021) $


from SQLparsing import *
from awardClass import awards
from xml.dom import minidom
from xml.dom import Node
import unittest

#####################################################################################
# Test for awardClass.py. This indirectly tests the following SQLparsing methods:
#
# SQLGetAwardCatById
# SQLGetAwardTypeById
# SQLLoadAllLanguages
# SQLloadAwards
# SQLloadTitle
# SQLloadTitleFromAward
# SQLloadTransAuthorNames
# SQLloadTransTitles
# SQLTitleBriefAuthorRecords
# SQLUpdateQueries
#
#####################################################################################

def TryPrint(label, value):
        try:
                print("%s %s" % (label, value))
        except:
                pass

INT_TYPE  = "<class 'int'>"
STR_TYPE  = "<class 'str'>"
DICT_TYPE = "<class 'dict'>"
NONE_TYPE = "<class 'NoneType'>"
LIST_TYPE = "<class 'list'>"
TUPLE_TYPE = "<class 'tuple'>"

debug = 1

def printAwardRecord(award):
        TryPrint("ID               =", award.award_id)
        TryPrint("TITLE            =", award.title_id)
        TryPrint("AWARD TITLE      =", award.award_title)
        TryPrint("AWARD YEAR       =", award.award_year)
        TryPrint("AWARD CAT ID     =", award.award_cat_id)
        TryPrint("AWARD CAT NAME   =", award.award_cat_name)
        TryPrint("AWARD LEVEL      =", award.award_level)
        TryPrint("AWARD DISP LEVEL =", award.award_displayed_level)
        TryPrint("AWARD MOVIE      =", award.award_movie)
        TryPrint("AWARD TYPE NAME  =", award.award_type_name)
        TryPrint("AWARD SHORT NAME =", award.award_type_short_name)
        TryPrint("AWARD TYPE ID    =", award.award_type_id)
        TryPrint("AWARD TYPE POLL  =", award.award_type_poll)
        TryPrint("AWARD NOTE ID    =", award.award_note_id)
        TryPrint("AWARD NOTE       =", award.award_note)
        TryPrint("SPECIAL AWARDS   =", award.special_awards)
        # Lists
        print("AUTHORS:")
        for author in award.award_authors:
                TryPrint("  AUTHOR         =", author)

def printAwardRecordTypes(award):
        TryPrint("ID               =", str(type(award.award_id)))
        TryPrint("TITLE            =", str(type(award.title_id)))
        TryPrint("AWARD TITLE      =", str(type(award.award_title)))
        TryPrint("AWARD YEAR       =", str(type(award.award_year)))
        TryPrint("AWARD CAT ID     =", str(type(award.award_cat_id)))
        TryPrint("AWARD CAT NAME   =", str(type(award.award_cat_name)))
        TryPrint("AWARD LEVEL      =", str(type(award.award_level)))
        TryPrint("AWARD DISP LEVEL =", str(type(award.award_displayed_level)))
        TryPrint("AWARD MOVIE      =", str(type(award.award_movie)))
        TryPrint("AWARD TYPE NAME  =", str(type(award.award_type_name)))
        TryPrint("AWARD SHORT NAME =", str(type(award.award_type_short_name)))
        TryPrint("AWARD TYPE ID    =", str(type(award.award_type_id)))
        TryPrint("AWARD TYPE POLL  =", str(type(award.award_type_poll)))
        TryPrint("AWARD NOTE ID    =", str(type(award.award_note_id)))
        TryPrint("AWARD NOTE       =", str(type(award.award_note)))
        TryPrint("SPECIAL AWARDS   =", str(type(award.special_awards)))
        TryPrint("AUTHORS          =", str(type(award.award_authors)))

class TestStorage(dict):
        def __init__(self, s=None):
                self.value = s
        def getvalue(self, theKey):
                return self[theKey]

class MyTestCase(unittest.TestCase):

        def test_001_load(self):
                print("TEST: awardClass::load")
                award = awards(db)
                award.load(7602)

                if debug:
                        printAwardRecord(award)
                        printAwardRecordTypes(award)

                self.assertEqual(INT_TYPE, str(type(award.award_id)))
                self.assertEqual(INT_TYPE, str(type(award.title_id)))
                self.assertEqual(STR_TYPE, str(type(award.award_title)))
                self.assertEqual(STR_TYPE, str(type(award.award_year)))
                self.assertEqual(INT_TYPE, str(type(award.award_cat_id)))
                self.assertEqual(STR_TYPE, str(type(award.award_cat_name)))
                self.assertEqual(STR_TYPE, str(type(award.award_level)))
                self.assertEqual(STR_TYPE, str(type(award.award_displayed_level)))
                self.assertEqual(STR_TYPE, str(type(award.award_movie)))
                self.assertEqual(STR_TYPE, str(type(award.award_type_name)))
                self.assertEqual(STR_TYPE, str(type(award.award_type_short_name)))
                self.assertEqual(INT_TYPE, str(type(award.award_type_id)))
                self.assertEqual(STR_TYPE, str(type(award.award_type_poll)))
                self.assertEqual(STR_TYPE, str(type(award.award_note_id)))
                self.assertEqual(STR_TYPE, str(type(award.award_note)))
                self.assertEqual(DICT_TYPE, str(type(award.special_awards)))
                self.assertEqual(LIST_TYPE, str(type(award.award_authors)))

        def test_002_authors(self):
                print("TEST: awardClass::authors")
                award = awards(db)
                award.load(7602)
                authors = award.authors()
                print("AUTHORS:", authors)
                self.assertEqual("Mark Clifton+Frank Riley", authors)

        def test_003_loadXML(self):
                print("TEST: awardClass::loadXML")
                award = awards(db)
                award.loadXML(7602)

                if debug:
                        printAwardRecord(award)
                        printAwardRecordTypes(award)

        def test_004_PrintAwardTable(self):
                print("TEST: awardClass::PrintAwardTable")
                record = SQLloadAwards(7602)
                award = awards(db)
                award.PrintAwardTable(record)

        def test_005_PrintYear(self):
                print("TEST: awardClass::PrintYear")
                award = awards(db)
                award.load(7602)
                award.PrintYear()

        def test_006_PrintLevel(self):
                print("TEST: awardClass::PrintLevel")
                award = awards(db)
                award.load(7602)
                award.PrintLevel(0)
                award.PrintLevel(1)

        def test_007_PrintTitle(self):
                print("TEST: awardClass::PrintTitle")
                award = awards(db)
                award.load(7602)
                award.PrintTitle()

        def test_008_PrintAwardSummary(self):
                print("TEST: awardClass::PrintAwardSummary")
                award = awards(db)
                award.load(7602)
                award.PrintAwardSummary()

        def test_009_PrintAwardAuthors(self):
                print("TEST: awardClass::PrintAwardAuthors")
                award = awards(db)
                award.load(7602)
                award.PrintAwardAuthors()

        def test_010_cgi2obj(self):
                print("TEST: awardClass::cgi2obj")
                print("==============================================")

                # Test 1 - Missing Year
                award = awards(db)
                form = {
                    'award_id': TestStorage(7602),
                }
                award.cgi2obj(form)
                self.assertEqual(award.error, "Missing YEAR value")

                # Test 2 - Missing Award Type ID
                award = awards(db)
                form = {
                    'award_year': TestStorage('1984'),
                }
                award.cgi2obj(form)
                self.assertEqual(award.error, "Missing Award Type ID")

                # Test 3 - Missing Award Category ID
                award = awards(db)
                form = {
                    'award_year': TestStorage('1984'),
                    'award_type_id': TestStorage(23),
                }
                award.cgi2obj(form)
                self.assertEqual(award.error, "Missing Award Category ID")

                # Test 3 - Missing Award Category ID
                award = awards(db)
                form = {
                    'award_id': TestStorage(7602),
                    'title_id': TestStorage(186614),
                    'award_title': TestStorage("They'd Rather Be Right"),
                    'award_year': TestStorage('1955'),
                    'award_type_id': TestStorage(23),
                    'award_cat_id': TestStorage(261),
                    'award_movie': TestStorage('tt1234567'),
                    'award_note': TestStorage('This is a test note'),
                    'LEVEL': TestStorage('WIN'),
                }
                award.cgi2obj(form)
                printAwardRecord(award)

                self.assertEqual(INT_TYPE, str(type(award.award_id)))
                self.assertEqual(INT_TYPE, str(type(award.title_id)))
                self.assertEqual(STR_TYPE, str(type(award.award_title)))
                self.assertEqual(STR_TYPE, str(type(award.award_year)))
                self.assertEqual(INT_TYPE, str(type(award.award_cat_id)))
                self.assertEqual(STR_TYPE, str(type(award.award_cat_name)))
                self.assertEqual(STR_TYPE, str(type(award.award_level)))
                self.assertEqual(STR_TYPE, str(type(award.award_displayed_level)))
                self.assertEqual(STR_TYPE, str(type(award.award_movie)))
                self.assertEqual(STR_TYPE, str(type(award.award_type_name)))
                self.assertEqual(STR_TYPE, str(type(award.award_type_short_name)))
                self.assertEqual(INT_TYPE, str(type(award.award_type_id)))
                self.assertEqual(STR_TYPE, str(type(award.award_type_poll)))
                self.assertEqual(STR_TYPE, str(type(award.award_note_id)))
                self.assertEqual(STR_TYPE, str(type(award.award_note)))
                self.assertEqual(DICT_TYPE, str(type(award.special_awards)))
                self.assertEqual(LIST_TYPE, str(type(award.award_authors)))


        def test_100_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()

if __name__ == '__main__':
        unittest.main()
