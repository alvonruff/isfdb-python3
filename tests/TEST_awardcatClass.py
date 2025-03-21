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
from awardcatClass import award_cat
from xml.dom import minidom
from xml.dom import Node
import unittest

#####################################################################################
# Test for awardcatClass.py. This indirectly tests the following SQLparsing methods:
#
# SQLGetAwardCatById
# SQLGetAwardTypeById
# SQLgetNotes
# SQLLoadAllLanguages
# SQLLoadAllTemplates
# SQLloadAwardCatWebpages
# SQLloadAwards
# SQLloadAwardsForCat
# SQLloadAwardsForCatYear
# SQLloadAwardTypeWebpages
# SQLloadTitleFromAward
# SQLloadTitle
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

def printAwardCatRecord(awardcat):
        print("-------------------------------------------------")
        TryPrint("ID              =", awardcat.award_cat_id)
        TryPrint("NAME            =", awardcat.award_cat_name)
        TryPrint("TYPE_ID         =", awardcat.award_cat_type_id)
        TryPrint("ORDER           =", awardcat.award_cat_order)
        TryPrint("NOTE_ID         =", awardcat.award_cat_note_id)
        TryPrint("NOTE            =", awardcat.award_cat_note)
        # Lists
        print("WEBPAGES:")
        for webpage in awardcat.award_cat_webpages:
                TryPrint("  WEBPAGE         =", webpage)
        print("-------------------------------------------------")

def printAwardCatRecordTypes(awardcat):
        TryPrint("ID              =", str(type(awardcat.award_cat_id)))
        TryPrint("NAME            =", str(type(awardcat.award_cat_name)))
        TryPrint("TYPE_ID         =", str(type(awardcat.award_cat_type_id)))
        TryPrint("ORDER           =", str(type(awardcat.award_cat_order)))
        TryPrint("NOTE_ID         =", str(type(awardcat.award_cat_note_id)))
        TryPrint("NOTE    E       =", str(type(awardcat.award_cat_note)))
        TryPrint("WEBPAGES        =", str(type(awardcat.award_cat_webpages)))

class TestStorage(dict):
        def __init__(self, s=None):
                self.value = s
        def getvalue(self, theKey):
                return self[theKey]

class MyTestCase(unittest.TestCase):

        def test_001_load(self):
                print("TEST: awardcatClass::load")
                cat = award_cat()
                cat.award_cat_id = 261
                cat.load()

                if debug:
                        printAwardCatRecord(cat)
                        printAwardCatRecordTypes(cat)

                self.assertEqual(INT_TYPE, str(type(cat.award_cat_id)))
                self.assertEqual(INT_TYPE, str(type(cat.award_cat_type_id)))
                self.assertEqual(INT_TYPE, str(type(cat.award_cat_order)))
                self.assertEqual(INT_TYPE, str(type(cat.award_cat_note_id)))
                self.assertEqual(STR_TYPE, str(type(cat.award_cat_name)))
                self.assertEqual(STR_TYPE, str(type(cat.award_cat_note)))
                self.assertEqual(LIST_TYPE, str(type(cat.award_cat_webpages)))

        def test_002_PrintAwardCatYear(self):
                print("TEST: awardcatClass::PrintAwardCatYear")
                cat = award_cat()
                cat.award_cat_id = 261
                cat.load()
                cat.PrintAwardCatYear(2023)

        def test_003_PrintAwardCatTable(self):
                print("TEST: awardcatClass::PrintAwardCatTable")
                cat = award_cat()
                cat.award_cat_id = 261
                cat.load()

                year = 2022
                years = {}
                padded_year = '%d-00-00' % year
                years[padded_year] = SQLloadAwardsForCatYear(cat.award_cat_id, year)
                cat.PrintAwardCatTable(years)

        def test_004_PrintAwardCatSummary(self):
                print("TEST: awardcatClass::PrintAwardCatSummary")
                cat = award_cat()
                cat.award_cat_id = 261
                cat.load()
                cat.PrintAwardCatSummary(0)

        def test_005_PrintAwardCatPageHeader(self):
                print("TEST: awardcatClass::PrintAwardCatPageHeader")
                cat = award_cat()
                cat.award_cat_id = 261
                cat.load()
                cat.PrintAwardCatPageHeader()

        def test_006_cgi2obj(self):
                print("TEST: awardcatClass::cgi2obj")

                # Test 1 - Missing author ID
                form = {
                    'award_cat_id': TestStorage("261"),
                }
                cat = award_cat()
                cat.cgi2obj(form)
                self.assertEqual(cat.error, "Valid award type is required for award categories")

                # Test 2 - Bad category name
                form = {
                    'award_cat_id': TestStorage("261"),
                    'award_cat_type_id': TestStorage("23"),
                }
                cat = award_cat()
                cat.cgi2obj(form)
                self.assertEqual(cat.error, "Award category name is required")

                # Test 3 - Valid CGI
                form = {
                    'award_cat_id': TestStorage("261"),
                    'award_cat_type_id': TestStorage("23"),
                    'award_cat_name': TestStorage("Best Novel"),
                }
                cat = award_cat()
                cat.cgi2obj(form)

                self.assertEqual(INT_TYPE, str(type(cat.award_cat_id)))
                self.assertEqual(INT_TYPE, str(type(cat.award_cat_type_id)))
                self.assertEqual(INT_TYPE, str(type(cat.award_cat_order)))
                self.assertEqual(INT_TYPE, str(type(cat.award_cat_note_id)))
                self.assertEqual(STR_TYPE, str(type(cat.award_cat_name)))
                self.assertEqual(STR_TYPE, str(type(cat.award_cat_note)))
                self.assertEqual(LIST_TYPE, str(type(cat.award_cat_webpages)))

        def test_100_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()

if __name__ == '__main__':
        unittest.main()
