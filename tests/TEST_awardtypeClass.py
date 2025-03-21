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
from awardtypeClass import award_type
from xml.dom import minidom
from xml.dom import Node
import unittest

#####################################################################################
# Test for awardtypeClass.py. This indirectly tests the following SQLparsing methods:
#
# SQLgetAuthorData
# SQLGetAwardCatBreakdown
# SQLGetAwardCatById
# SQLGetAwardTypeByCode
# SQLGetAwardTypeById
# SQLGetAwardTypeByName
# SQLGetAwardTypeByShortName
# SQLGetAwardYears
# SQLGetEmptyAwardCategories
# SQLgetNotes
# SQLLoadAllLanguages
# SQLLoadAllTemplates
# SQLloadAwards
# SQLloadAwardsForYearType
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

def printAwardTypeRecord(awardtype):
        print("-------------------------------------------------")
        TryPrint("ID              =", awardtype.award_type_id)
        TryPrint("CODE            =", awardtype.award_type_code)
        TryPrint("BY              =", awardtype.award_type_by)
        TryPrint("NAME            =", awardtype.award_type_name)
        TryPrint("SHORT NAME      =", awardtype.award_type_short_name)
        TryPrint("POLL            =", awardtype.award_type_poll)
        TryPrint("NOTE ID         =", awardtype.award_type_note_id)
        TryPrint("NOTE            =", awardtype.award_type_note)
        TryPrint("NON GENRE       =", awardtype.award_type_non_genre)
        # Lists
        print("WEBPAGES:")
        for webpage in awardtype.award_type_webpages:
                TryPrint("  WEBPAGE         =", webpage)
        print("-------------------------------------------------")

def printAwardTypeRecordTypes(awardtype):
        TryPrint("ID              =", str(type(awardtype.award_type_id)))
        TryPrint("CODE            =", str(type(awardtype.award_type_code)))
        TryPrint("BY              =", str(type(awardtype.award_type_by)))
        TryPrint("NAME            =", str(type(awardtype.award_type_name)))
        TryPrint("SHORT NAME      =", str(type(awardtype.award_type_short_name)))
        TryPrint("POLL            =", str(type(awardtype.award_type_poll)))
        TryPrint("NOTE ID         =", str(type(awardtype.award_type_note_id)))
        TryPrint("NOTE            =", str(type(awardtype.award_type_note)))
        TryPrint("NON GENRE       =", str(type(awardtype.award_type_non_genre)))
        TryPrint("WEBPAGE         =", str(type(awardtype.award_type_webpages)))

class TestStorage(dict):
        def __init__(self, s=None):
                self.value = s
        def getvalue(self, theKey):
                return self[theKey]

class MyTestCase(unittest.TestCase):

        def test_001_load(self):
                print("TEST: awardtypeClass::load")
                atype = award_type()
                atype.award_type_code = 'Hu'
                atype.load()
                print("ERROR: ", atype.error)

                if debug:
                        printAwardTypeRecord(atype)
                        printAwardTypeRecordTypes(atype)

                self.assertEqual(INT_TYPE, str(type(atype.award_type_id)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_code)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_by)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_name)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_short_name)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_poll)))
                self.assertEqual(INT_TYPE, str(type(atype.award_type_note_id)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_note)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_non_genre)))
                self.assertEqual(LIST_TYPE, str(type(atype.award_type_webpages)))

        def test_002_load(self):
                print("TEST: awardtypeClass::load")
                atype = award_type()
                atype.award_type_id = 23
                atype.load()
                print("ERROR: ", atype.error)

                if debug:
                        printAwardTypeRecord(atype)
                        printAwardTypeRecordTypes(atype)

                self.assertEqual(INT_TYPE, str(type(atype.award_type_id)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_code)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_by)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_name)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_short_name)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_poll)))
                self.assertEqual(INT_TYPE, str(type(atype.award_type_note_id)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_note)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_non_genre)))
                self.assertEqual(LIST_TYPE, str(type(atype.award_type_webpages)))

        def test_003_load(self):
                print("TEST: awardtypeClass::load")
                atype = award_type()
                atype.load()
                self.assertEqual(atype.error, "Award type not specified")

        def test_004_DisplayCategories(self):
                print("TEST: awardtypeClass::DisplayCategories")
                atype = award_type()
                atype.award_type_id = 23
                atype.load()
                atype.display_categories()

        def test_005_DisplayAwardsForYear(self):
                print("TEST: awardtypeClass::DisplayAwardsForYear")
                atype = award_type()
                atype.award_type_id = 23
                atype.load()
                atype.display_awards_for_year(2022)

        def test_006_cgi2obj(self):
                print("TEST: awardtypeClass::cgi2obj")

                # Test 1 - Award Type Name
                form = {
                    'award_year': TestStorage('0000-00-00'),
                }
                atype = award_type()
                atype.cgi2obj(form)
                self.assertEqual(atype.error, "Full name is required for Award types")

                # Test 2 - Award Full Name
                form = {
                    'award_type_name': TestStorage('Hugo Award'),
                }
                atype = award_type()
                atype.cgi2obj(form)
                self.assertEqual(atype.error, "Award type with full name 'Hugo Award' already exists")

                # Test 3 - Award Short Name
                form = {
                    'award_type_name': TestStorage('Bogus Award'),
                }
                atype = award_type()
                atype.cgi2obj(form)
                self.assertEqual(atype.error, "Short name is required for Award types")

                # Test 4 - Award Short Name
                form = {
                    'award_type_name': TestStorage('Bogus Award'),
                    'award_type_short_name': TestStorage('Hugo'),
                }
                atype = award_type()
                atype.cgi2obj(form)
                self.assertEqual(atype.error, "Award type with short name 'Hugo' already exists")

                # Test 5 - Bad Webpage
                form = {
                    'award_type_id': TestStorage(23),
                    'award_type_name': TestStorage('Bogus Award'),
                    'award_type_short_name': TestStorage('Bogus'),
                    'award_type_by': TestStorage('Bogus'),
                    'award_type_for': TestStorage('Bogus'),
                    'award_type_poll': TestStorage('Bogus'),
                    'award_type_note': TestStorage('Bogus'),
                    'award_type_non_genre': TestStorage('Bogus'),
                    'award_type_webpages': TestStorage("amazon.com"),
                }
                atype = award_type()
                atype.cgi2obj(form)
                self.assertEqual(atype.error, " URLs must start with http or https")

                # Test 6 - Success
                form = {
                    'award_type_id': TestStorage(23),
                    'award_type_name': TestStorage('Bogus Award'),
                    'award_type_short_name': TestStorage('Bogus'),
                    'award_type_by': TestStorage('Bogus'),
                    'award_type_for': TestStorage('Bogus'),
                    'award_type_poll': TestStorage('Bogus'),
                    'award_type_note': TestStorage('Bogus'),
                    'award_type_non_genre': TestStorage('Bogus'),
                    'award_type_webpages': TestStorage("http://amazon.com"),
                }
                atype = award_type()
                atype.cgi2obj(form)

                if debug:
                        printAwardTypeRecord(atype)
                        printAwardTypeRecordTypes(atype)

                self.assertEqual(INT_TYPE, str(type(atype.award_type_id)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_code)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_by)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_name)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_short_name)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_poll)))
                self.assertEqual(INT_TYPE, str(type(atype.award_type_note_id)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_note)))
                self.assertEqual(STR_TYPE, str(type(atype.award_type_non_genre)))
                self.assertEqual(LIST_TYPE, str(type(atype.award_type_webpages)))

        def test_100_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()

if __name__ == '__main__':
        unittest.main()
