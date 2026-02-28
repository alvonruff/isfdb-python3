#!_PYTHONLOC
#
#     (C) COPYRIGHT 2026   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 717 $
#     Date: $Date: 2021-08-28 11:04:26 -0400 (Sat, 28 Aug 2021) $


from SQLparsing import *
import unittest

def printAuthorRecord(record):
        print("ID              =", record[AUTHOR_ID])
        print("CANONICAL       =", record[AUTHOR_CANONICAL])
        print("LEGALNAME       =", record[AUTHOR_LEGALNAME])
        print("BIRTHPLACE      =", record[AUTHOR_BIRTHPLACE])
        print("BIRTHDATE       =", record[AUTHOR_BIRTHDATE])
        print("DEATHDATE       =", record[AUTHOR_DEATHDATE])
        print("NOTE_ID         =", record[AUTHOR_NOTE_ID])
        print("COUNTER         =", record[AUTHOR_COUNTER])
        print("MARQUE          =", record[AUTHOR_MARQUE])
        print("IMAGE           =", record[AUTHOR_IMAGE])
        print("ANNUALVIEWS     =", record[AUTHOR_ANNUALVIEWS])
        print("LASTNAME        =", record[AUTHOR_LASTNAME])
        print("LANGUAGE        =", record[AUTHOR_LANGUAGE])
        print("NOTE            =", record[AUTHOR_NOTE])

def TryPrint(label, value):
        try:
                print("%s %s" % (label, value))
        except:
                pass

def printAuthorRecordTypes(record):
        TryPrint("ID              =", str(type(record[AUTHOR_ID])))
        TryPrint("CANONICAL       =", str(type(record[AUTHOR_CANONICAL])))
        TryPrint("LEGALNAME       =", str(type(record[AUTHOR_LEGALNAME])))
        TryPrint("BIRTHPLACE      =", str(type(record[AUTHOR_BIRTHPLACE])))
        TryPrint("BIRTHDATE       =", str(type(record[AUTHOR_BIRTHDATE])))
        TryPrint("DEATHDATE       =", str(type(record[AUTHOR_DEATHDATE])))
        TryPrint("NOTE_ID         =", str(type(record[AUTHOR_NOTE_ID])))
        TryPrint("COUNTER         =", str(type(record[AUTHOR_COUNTER])))
        TryPrint("MARQUE          =", str(type(record[AUTHOR_MARQUE])))
        TryPrint("IMAGE           =", str(type(record[AUTHOR_IMAGE])))
        TryPrint("ANNUALVIEWS     =", str(type(record[AUTHOR_ANNUALVIEWS])))
        TryPrint("LASTNAME        =", str(type(record[AUTHOR_LASTNAME])))
        TryPrint("LANGUAGE        =", str(type(record[AUTHOR_LANGUAGE])))
        TryPrint("NOTE            =", str(type(record[AUTHOR_NOTE])))

if db_connector == db_python2:
        INT_TYPE  = "<type 'int'>"
        STR_TYPE  = "<type 'str'>"
        DICT_TYPE = "<type 'dict'>"
        NONE_TYPE = "<type 'NoneType'>"
        LIST_TYPE = "<type 'list'>"
        TUPLE_TYPE = "<type 'tuple'>"
else:
        INT_TYPE  = "<class 'int'>"
        STR_TYPE  = "<class 'str'>"
        DICT_TYPE = "<class 'dict'>"
        NONE_TYPE = "<class 'NoneType'>"
        LIST_TYPE = "<class 'list'>"
        TUPLE_TYPE = "<class 'tuple'>"

class MyTestCase(unittest.TestCase):

        def test_001_SQLgetAuthorData(self):
                print("TEST: SQLgetAuthorData")
                author = SQLgetAuthorData('Jules Verne')
                #printAuthorRecordTypes(author)
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ID])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_CANONICAL])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_LEGALNAME])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_BIRTHPLACE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_BIRTHDATE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_DEATHDATE])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_NOTE_ID])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_COUNTER])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_MARQUE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_IMAGE])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ANNUALVIEWS])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_LASTNAME])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_LANGUAGE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_NOTE])))

        def test_002_SQLloadAuthorData(self):
                print("TEST: SQLloadAuthorData")
                # ASCII Argument
                author = SQLloadAuthorData('159')
                #printAuthorRecordTypes(author)
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ID])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_CANONICAL])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_LEGALNAME])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_BIRTHPLACE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_BIRTHDATE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_DEATHDATE])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_NOTE_ID])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_COUNTER])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_MARQUE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_IMAGE])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ANNUALVIEWS])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_LASTNAME])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_LANGUAGE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_NOTE])))
                # INTEGER Argument
                author = SQLloadAuthorData(159)
                #printAuthorRecordTypes(author)
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ID])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_CANONICAL])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_LEGALNAME])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_BIRTHPLACE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_BIRTHDATE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_DEATHDATE])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_NOTE_ID])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_COUNTER])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_MARQUE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_IMAGE])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ANNUALVIEWS])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_LASTNAME])))
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_LANGUAGE])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_NOTE])))

        def test_003_SQLTitleBriefAuthorRecords(self):
                print("TEST: SQLTitleBriefAuthorRecords")
                # ASCII Argument
                author = SQLTitleBriefAuthorRecords('159')
                author = author[0]
                #printAuthorRecordTypes(author)
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ID])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_CANONICAL])))
                # INTEGER Argument
                author = SQLTitleBriefAuthorRecords(159)
                author = author[0]
                #printAuthorRecordTypes(author)
                self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ID])))
                self.assertEqual(STR_TYPE, str(type(author[AUTHOR_CANONICAL])))

        def test_004_SQLMultipleAuthors(self):
                print("TEST: SQLMultipleAuthorsitleBriefAuthorRecords")
                result = SQLMultipleAuthors('Steve Miller')
                self.assertEqual(1, result[0])
                result = SQLMultipleAuthors('Steve Miller (UK)')
                self.assertEqual(1, result[0])
                result = SQLMultipleAuthors('Steve Millard')
                self.assertEqual(0, result)

        def test_005_SQLgetBriefActualFromPseudo(self):
                print("TEST: SQLgetBriefActualFromPseudo")
                # ASCII Argument
                author = SQLgetBriefActualFromPseudo('177072')
                author = author[0]
                self.assertEqual(159, author[0])
                self.assertEqual("Jules Verne", author[1])
                # INTEGER Argument
                #author = SQLTitleBriefAuthorRecords(177072)
                #author = author[0]
                #print(author)
                #self.assertEqual(159, author[0])
                #self.assertEqual("Jules Verne", author[1])

        def test_006_SQLgetActualFromPseudo(self):
                print("TEST: SQLgetActualFromPseudo")
                # ASCII Argument
                authors = SQLgetActualFromPseudo('2859')
                knownList = [['Bill McCay'], ['Bridget McKenna'], ['Debra Doyle'], ['James D. Macdonald'], 
                        ['F. Gwynplaine MacIntyre'], ['Harriet Stratemeyer Adams'], ['Howard R. Garis'], 
                        ['Robert E. Vardeman'], ['Steven Grant'], ['unknown'], ['William Rotsler'], 
                        ['Sharman DiVono'], ['Thomas Moyston Mitchell'], ['John W. Duffield'], 
                        ['Bruce Holland Rogers'], ['Neal Barrett, Jr.'], ['Mike McQuay'], 
                        ['Greg Cox'], ['Michael Anthony Steele']]
                for i in knownList:
                        self.assertIn(i, authors)

        def test_007_SQLAuthorsBorn(self):
                print("TEST: SQLAuthorsBorn")
                authors = SQLAuthorsBorn('1564-04-00')
                for author in authors:
                        self.assertEqual(STR_TYPE, str(type(author[AUTHOR_BIRTHDATE])))

        def test_007_SQLAuthorsDied(self):
                print("TEST: SQLAuthorsDied")
                authors = SQLAuthorsDied('1564-04-00')
                for author in authors:
                        self.assertEqual(STR_TYPE, str(type(author[AUTHOR_DEATHDATE])))

        def test_008_SQLFindAuthors(self):
                print("TEST: SQLFindAuthors")
                authors = SQLFindAuthors('Asimov', 'contains')
                for author in authors:
                        self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ID])))
                        self.assertEqual(STR_TYPE, str(type(author[AUTHOR_CANONICAL])))
                authors = SQLFindAuthors('Asimov', 'exact')
                self.assertEqual([], authors)
                authors = SQLFindAuthors('Isaac Asimov', 'exact')
                for author in authors:
                        self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ID])))
                        self.assertEqual(STR_TYPE, str(type(author[AUTHOR_CANONICAL])))

        def test_009_SQLGetAllAuthorsForPublisher(self):
                print("TEST: SQLGetAllAuthorsForPublisher")
                authors = SQLGetAllAuthorsForPublisher('53666', 'name')
                for author in authors:
                        self.assertEqual(INT_TYPE, str(type(author[0])))
                        self.assertEqual(STR_TYPE, str(type(author[1])))
                        self.assertEqual(INT_TYPE, str(type(author[2])))
                authors = SQLGetAllAuthorsForPublisher('53666', 'count')
                for author in authors:
                        self.assertEqual(INT_TYPE, str(type(author[0])))
                        self.assertEqual(STR_TYPE, str(type(author[1])))
                        self.assertEqual(INT_TYPE, str(type(author[2])))

        def test_010_SQLGetAuthorDirectory(self):
                print("TEST: SQLGetAuthorDirectory")
                authors = SQLGetAuthorDirectory()
                self.assertEqual(DICT_TYPE, str(type(authors)))
                # Only authors As-Az and Oa-Oz exist in the full space
                # Spot-check authors Aa through Az
                first = 'a'
                for lower in range(0,26):
                        second = string.ascii_lowercase[lower:lower+1]
                        target = first+second
                        self.assertIn(target, authors)
                # Spot-check authors Oa through Oz
                Cap = 'o'
                for lower in range(0,26):
                        second = string.ascii_lowercase[lower:lower+1]
                        target = first+second
                        self.assertIn(target, authors)

        def test_011_SQLgetBriefPseudoFromActual(self):
                print("TEST: SQLgetBriefPseudoFromActual")
                # ASCII Argument
                authors = SQLgetBriefPseudoFromActual('5')
                for author in authors:
                        self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ID])))
                        self.assertEqual(STR_TYPE, str(type(author[AUTHOR_CANONICAL])))
                # INTEGER Argument
                authors = SQLTitleBriefAuthorRecords(8)
                authors = SQLgetBriefPseudoFromActual('5')
                for author in authors:
                        self.assertEqual(INT_TYPE, str(type(author[AUTHOR_ID])))
                        self.assertEqual(STR_TYPE, str(type(author[AUTHOR_CANONICAL])))

        def test_012_SQLLoadTransAuthorNamesList(self):
                print("TEST: SQLLoadTransAuthorNamesList")
                arg = [319360, 319366, 319390]
                entries = SQLLoadTransAuthorNamesList(arg)
                for entry in entries:
                        names = entries[entry]
                        for name in names:
                                self.assertEqual(STR_TYPE, str(type(name)))

        def test_013_SQLGetCoverAuthorsForPubs(self):
                print("TEST: SQLGetCoverAuthorsForPubs")
                author = SQLGetCoverAuthorsForPubs(['23000'])
                self.assertEqual(DICT_TYPE, str(type(author)))
                record = author[23000]
                record = record[0]
                self.assertEqual(record[0], 1070)
                self.assertEqual(record[1], 'Bob Eggleton')

        def test_014_SQLInterviewAuthors(self):
                print("TEST: SQLInterviewAuthors")
                author = SQLInterviewAuthors('1150778')
                self.assertEqual(LIST_TYPE, str(type(author)))
                self.assertEqual(author[0], 'Ursula K. Le Guin')

        def test_015_SQLInterviewBriefAuthorRecords(self):
                print("TEST: SQLInterviewBriefAuthorRecords")
                author = SQLInterviewBriefAuthorRecords('1150778')
                self.assertEqual(LIST_TYPE, str(type(author)))
                auTuple = author[0]
                self.assertEqual(INT_TYPE, str(type(auTuple[0])))
                self.assertEqual(STR_TYPE, str(type(auTuple[1])))
                self.assertEqual(auTuple[0], 37)
                self.assertEqual(auTuple[1], 'Ursula K. Le Guin')

        def test_016_SQLIntervieweeAuthors(self):
                print("TEST: SQLIntervieweeAuthors")
                author = SQLIntervieweeAuthors('1150778', '0')
                self.assertEqual(LIST_TYPE, str(type(author)))
                auTuple = author[0]
                self.assertEqual(INT_TYPE, str(type(auTuple[0])))
                self.assertEqual(STR_TYPE, str(type(auTuple[1])))
                self.assertEqual(auTuple[0], 37)
                self.assertEqual(auTuple[1], 'Ursula K. Le Guin')

        def test_017_SQLPubAuthors(self):
                print("TEST: SQLPubAuthors")
                author = SQLPubAuthors('47772')
                self.assertEqual(LIST_TYPE, str(type(author)))
                self.assertEqual(author[0], 'Stephen King')

        def test_018_SQLPubBriefAuthorRecords(self):
                print("TEST: SQLPubBriefAuthorRecords")
                author = SQLPubBriefAuthorRecords('47772')
                self.assertEqual(LIST_TYPE, str(type(author)))
                auTuple = author[0]
                self.assertEqual(INT_TYPE, str(type(auTuple[0])))
                self.assertEqual(STR_TYPE, str(type(auTuple[1])))
                self.assertEqual(auTuple[0], 70)
                self.assertEqual(auTuple[1], 'Stephen King')

        def test_018_SQLPubListBriefAuthorRecords(self):
                print("TEST: SQLPubListBriefAuthorRecords")
                pubs = [947182, 947788, 942373]
                authors = SQLPubListBriefAuthorRecords(pubs)
                for pub in pubs:
                        value = authors[pub][0]
                        self.assertEqual(INT_TYPE, str(type(value[0])))
                        self.assertEqual(STR_TYPE, str(type(value[1])))
                        self.assertEqual(STR_TYPE, str(type(value[2])))

        def test_019_SQLReviewAuthors(self):
                print("TEST: SQLReviewAuthors")
                authors = SQLReviewAuthors('1005915')
                self.assertEqual(STR_TYPE, str(type(authors[0])))
                self.assertEqual('William Gibson', authors[0])

        def test_020_SQLReviewAuthors(self):
                print("TEST: SQLReviewBriefAuthorRecords")
                authors = SQLReviewBriefAuthorRecords('1005915')
                self.assertEqual(TUPLE_TYPE, str(type(authors[0])))
                self.assertEqual(172, authors[0][0])
                self.assertEqual('William Gibson', authors[0][1])

        def test_021(self):
                print("TEST: SQLReviewedAuthors")
                authors = SQLReviewedAuthors('1005915')
                self.assertEqual(TUPLE_TYPE, str(type(authors[0])))
                self.assertEqual(172, authors[0][0])
                self.assertEqual('William Gibson', authors[0][1])

        def test_022(self):
                print("TEST: SQLTitleAuthors")
                authors = SQLTitleAuthors('1005915')
                self.assertEqual(STR_TYPE, str(type(authors[0])))
                self.assertEqual('Faren Miller', authors[0])

        def test_023(self):
                print("TEST: SQLTitleListBriefAuthorRecords")
                title_list = SQLTitleListBriefAuthorRecords('2128710, 2221574, 1376211', '0')
                self.assertEqual(DICT_TYPE, str(type(title_list)))

                record = title_list[1376211]
                record = record[0]
                self.assertEqual(record[0], 172)
                self.assertEqual(record[1], 'William Gibson')

                record = title_list[2128710]
                record = record[0]
                self.assertEqual(record[0], 172)

                record = title_list[2221574]
                record = record[0]
                self.assertEqual(record[0], 172)

        def test_024(self):
                print("TEST: SQLtransLegalNames")
                authors = SQLtransLegalNames([256279, 264664])
                self.assertEqual(DICT_TYPE, str(type(authors)))

                record = authors[256279]
                self.assertEqual(STR_TYPE, str(type(record[0])))
                self.assertEqual(STR_TYPE, str(type(record[1])))

                record = authors[264664]
                self.assertEqual(STR_TYPE, str(type(record[0])))
                self.assertEqual(STR_TYPE, str(type(record[1])))

        def test_025_SQLListAwardTypes(self):
                print("TEST: SQLListAwardTypes")
                types = SQLListAwardTypes()
                self.assertEqual(LIST_TYPE, str(type(types)))
                self.assertGreater(len(types), 0, "Should have at least one award type")
                award_type = types[14]
                self.assertEqual(INT_TYPE, str(type(award_type[AWARD_TYPE_ID])))
                self.assertEqual(STR_TYPE, str(type(award_type[AWARD_TYPE_CODE])))
                self.assertEqual(STR_TYPE, str(type(award_type[AWARD_TYPE_NAME])))

        def test_026_SQLGetAwardTypeById(self):
                print("TEST: SQLGetAwardTypeById")
                award_type = SQLListAwardTypes()[14]
                type_id = award_type[AWARD_TYPE_ID]
                result = SQLGetAwardTypeById(type_id)
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(type_id, result[AWARD_TYPE_ID])
                not_found = SQLGetAwardTypeById(999999999)
                self.assertEqual([], not_found)

        def test_027_SQLGetAwardTypeByCode(self):
                print("TEST: SQLGetAwardTypeByCode")
                award_type = SQLListAwardTypes()[14]
                code = award_type[AWARD_TYPE_CODE]
                result = SQLGetAwardTypeByCode(code)
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(code, result[AWARD_TYPE_CODE])
                not_found = SQLGetAwardTypeByCode('_NO_SUCH_CODE_')
                self.assertEqual([], not_found)

        def test_028_SQLGetAwardTypeByName(self):
                print("TEST: SQLGetAwardTypeByName")
                award_type = SQLListAwardTypes()[0]
                name = award_type[AWARD_TYPE_NAME]
                result = SQLGetAwardTypeByName(name)
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(name, result[AWARD_TYPE_NAME])
                not_found = SQLGetAwardTypeByName('_NO_SUCH_AWARD_')
                self.assertEqual([], not_found)

        def test_029_SQLGetAwardTypeByShortName(self):
                print("TEST: SQLGetAwardTypeByShortName")
                award_type = SQLListAwardTypes()[0]
                short_name = award_type[AWARD_TYPE_SHORT_NAME]
                result = SQLGetAwardTypeByShortName(short_name)
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(short_name, result[AWARD_TYPE_SHORT_NAME])

        def test_030_SQLGetAwardYears(self):
                print("TEST: SQLGetAwardYears")
                award_type = SQLListAwardTypes()[0]
                type_id = award_type[AWARD_TYPE_ID]
                years = SQLGetAwardYears(type_id)
                self.assertEqual(LIST_TYPE, str(type(years)))
                for year in years:
                        self.assertEqual(STR_TYPE, str(type(year)))
                        break

        def test_031_SQLGetAwardCategories(self):
                print("TEST: SQLGetAwardCategories")
                award_type = SQLListAwardTypes()[0]
                type_id = award_type[AWARD_TYPE_ID]
                cats = SQLGetAwardCategories(type_id)
                self.assertEqual(LIST_TYPE, str(type(cats)))
                if cats:
                        cat = cats[0]
                        self.assertEqual(INT_TYPE, str(type(cat[AWARD_CAT_ID])))
                        self.assertEqual(STR_TYPE, str(type(cat[AWARD_CAT_NAME])))
                        self.assertEqual(INT_TYPE, str(type(cat[AWARD_CAT_TYPE_ID])))

        def test_032_SQLGetAwardCatById(self):
                print("TEST: SQLGetAwardCatById")
                award_type = SQLListAwardTypes()[0]
                type_id = award_type[AWARD_TYPE_ID]
                cats = SQLGetAwardCategories(type_id)
                if cats:
                        cat_id = cats[0][AWARD_CAT_ID]
                        result = SQLGetAwardCatById(cat_id)
                        self.assertEqual(TUPLE_TYPE, str(type(result)))
                        self.assertEqual(cat_id, result[AWARD_CAT_ID])
                not_found = SQLGetAwardCatById(999999999)
                self.assertEqual((), not_found)

        def test_033_SQLGetAwardCatByName(self):
                print("TEST: SQLGetAwardCatByName")
                award_type = SQLListAwardTypes()[0]
                type_id = award_type[AWARD_TYPE_ID]
                cats = SQLGetAwardCategories(type_id)
                if cats:
                        cat_name = cats[0][AWARD_CAT_NAME]
                        result = SQLGetAwardCatByName(cat_name, type_id)
                        self.assertEqual(TUPLE_TYPE, str(type(result)))
                        self.assertEqual(cat_name, result[AWARD_CAT_NAME])
                not_found = SQLGetAwardCatByName('_NO_SUCH_CAT_', 999)
                self.assertEqual((), not_found)

        def test_034_SQLSearchAwards(self):
                print("TEST: SQLSearchAwards")
                results = SQLSearchAwards('Hugo')
                self.assertEqual(LIST_TYPE, str(type(results)))
                self.assertGreater(len(results), 0, "Expected at least one match for 'Hugo'")
                award = results[0]
                self.assertEqual(INT_TYPE, str(type(award[AWARD_TYPE_ID])))
                no_results = SQLSearchAwards('_NOMATCH_XYZZY_')
                self.assertEqual([], no_results)

        def test_035_SQLGetAwardCatBreakdown(self):
                print("TEST: SQLGetAwardCatBreakdown")
                award_type = SQLListAwardTypes()[0]
                type_id = award_type[AWARD_TYPE_ID]
                results = SQLGetAwardCatBreakdown(type_id)
                self.assertEqual(LIST_TYPE, str(type(results)))
                for row in results:
                        self.assertEqual(TUPLE_TYPE, str(type(row)))
                        break

        def test_036_SQLGetEmptyAwardCategories(self):
                print("TEST: SQLGetEmptyAwardCategories")
                award_type = SQLListAwardTypes()[0]
                type_id = award_type[AWARD_TYPE_ID]
                results = SQLGetEmptyAwardCategories(type_id)
                self.assertEqual(LIST_TYPE, str(type(results)))

        def test_037_SQLget1Series(self):
                print("TEST: SQLget1Series")
                result = SQLget1Series(3581)
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(3581, result[SERIES_PUBID])
                not_found = SQLget1Series(999999999)
                self.assertEqual(0, not_found)

        def test_038_SQLgetSeriesName(self):
                print("TEST: SQLgetSeriesName")
                name = SQLgetSeriesName(3581)
                self.assertEqual(STR_TYPE, str(type(name)))
                self.assertEqual("Isaac Asimov's Robot City", name)

        def test_039_SQLFindSeriesId(self):
                print("TEST: SQLFindSeriesId")
                series_id = SQLFindSeriesId("Isaac Asimov's Robot City")
                self.assertEqual(3581, series_id)
                not_found = SQLFindSeriesId('_NO_SUCH_SERIES_')
                self.assertEqual('', not_found)

        def test_040_SQLFindSeriesName(self):
                print("TEST: SQLFindSeriesName")
                name = SQLFindSeriesName(3581)
                self.assertEqual(STR_TYPE, str(type(name)))
                self.assertEqual("Isaac Asimov's Robot City", name)
                not_found = SQLFindSeriesName(999999999)
                self.assertEqual('', not_found)

        def test_041_SQLFindSeriesParent(self):
                print("TEST: SQLFindSeriesParent")
                parent = SQLFindSeriesParent(3581)
                self.assertEqual(647, parent)
                not_found = SQLFindSeriesParent(999999999)
                self.assertEqual('', not_found)

        def test_042_SQLFindSeriesParentPosition(self):
                print("TEST: SQLFindSeriesParentPosition")
                # Series 171 (Honor Harrington) has parent_position = 1
                pos = SQLFindSeriesParentPosition(171)
                self.assertEqual(1, pos)
                not_found = SQLFindSeriesParentPosition(999999999)
                self.assertEqual('', not_found)

        def test_043_SQLFindSeries(self):
                print("TEST: SQLFindSeries")
                results = SQLFindSeries('Asimov', 'contains')
                self.assertEqual(LIST_TYPE, str(type(results)))
                self.assertGreater(len(results), 0)
                exact = SQLFindSeries("Isaac Asimov's Robot City", 'exact')
                self.assertGreater(len(exact), 0)
                none = SQLFindSeries('_NO_SUCH_SERIES_XYZZY_', 'exact')
                self.assertEqual([], none)

        def test_044_SQLGetSeriesByName(self):
                print("TEST: SQLGetSeriesByName")
                result = SQLGetSeriesByName("Isaac Asimov's Robot City")
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(3581, result[SERIES_PUBID])
                not_found = SQLGetSeriesByName('_NO_SUCH_SERIES_')
                self.assertEqual(0, not_found)

        def test_045_SQLloadTransSeriesNames(self):
                print("TEST: SQLloadTransSeriesNames")
                # Series 35069 (Metro 2033) has trans name 'Metro 2033'
                names = SQLloadTransSeriesNames(35069)
                self.assertEqual(LIST_TYPE, str(type(names)))
                self.assertIn('Metro 2033', names)
                # Series 3581 has no trans names
                no_names = SQLloadTransSeriesNames(3581)
                self.assertEqual(LIST_TYPE, str(type(no_names)))

        def test_046_SQLloadSeriesWebpages(self):
                print("TEST: SQLloadSeriesWebpages")
                # Series 23 (Pellucidar) has a Wikipedia webpage
                urls = SQLloadSeriesWebpages(23)
                self.assertEqual(LIST_TYPE, str(type(urls)))
                self.assertIn('https://en.wikipedia.org/wiki/Pellucidar', urls)
                empty = SQLloadSeriesWebpages(999999999)
                self.assertEqual([], empty)

        def test_047_SQLLoadSeriesFromList(self):
                print("TEST: SQLLoadSeriesFromList")
                result = SQLLoadSeriesFromList([3581, 171])
                self.assertEqual(DICT_TYPE, str(type(result)))
                self.assertIn(3581, result)
                self.assertIn(171, result)
                empty = SQLLoadSeriesFromList([])
                self.assertEqual({}, empty)

        def test_048_SQLGetPubSeries(self):
                print("TEST: SQLGetPubSeries")
                result = SQLGetPubSeries(1)
                self.assertEqual(LIST_TYPE, str(type(result)))
                self.assertGreater(len(result), 0)
                self.assertEqual(1, result[PUB_SERIES_ID])
                not_found = SQLGetPubSeries(999999999)
                self.assertEqual([], not_found)

        def test_049_SQLGetPubSeriesByName(self):
                print("TEST: SQLGetPubSeriesByName")
                ps = SQLGetPubSeries(1)
                ps_name = ps[PUB_SERIES_NAME]
                results = SQLGetPubSeriesByName(ps_name)
                self.assertEqual(LIST_TYPE, str(type(results)))
                self.assertGreater(len(results), 0)
                not_found = SQLGetPubSeriesByName('_NO_SUCH_PUB_SERIES_')
                self.assertEqual([], not_found)

        def test_050_SQLGetPubSeriesList(self):
                print("TEST: SQLGetPubSeriesList")
                result = SQLGetPubSeriesList([1, 2])
                self.assertEqual(DICT_TYPE, str(type(result)))
                self.assertIn(1, result)
                empty = SQLGetPubSeriesList([])
                self.assertEqual({}, empty)

        def test_051_SQLCountPubsForPubSeries(self):
                print("TEST: SQLCountPubsForPubSeries")
                count = SQLCountPubsForPubSeries(1)
                self.assertEqual(INT_TYPE, str(type(count)))
                self.assertGreater(count, 0)

        def test_052_SQLFindPubSeries(self):
                print("TEST: SQLFindPubSeries")
                results = SQLFindPubSeries('Ace', 'contains')
                self.assertEqual(LIST_TYPE, str(type(results)))
                self.assertGreater(len(results), 0)
                none = SQLFindPubSeries('_NO_SUCH_PUB_SERIES_XYZZY_', 'exact')
                self.assertEqual([], none)

        def test_053_SQLFindPublisher(self):
                print("TEST: SQLFindPublisher")
                results = SQLFindPublisher('Tor', 'contains')
                self.assertEqual(LIST_TYPE, str(type(results)))
                self.assertGreater(len(results), 0)
                if results:
                        pub_name = results[0][PUBLISHER_NAME]
                        exact = SQLFindPublisher(pub_name, 'exact')
                        self.assertGreater(len(exact), 0)
                none = SQLFindPublisher('_NO_SUCH_PUB_XYZZY_', 'exact')
                self.assertEqual([], none)

        def test_054_SQLgetPublisherName(self):
                print("TEST: SQLgetPublisherName")
                name = SQLgetPublisherName(53666)
                self.assertEqual(STR_TYPE, str(type(name)))
                self.assertGreater(len(name), 0)
                not_found = SQLgetPublisherName(999999999)
                self.assertEqual('', not_found)

        def test_055_SQLCountPubsForPublisher(self):
                print("TEST: SQLCountPubsForPublisher")
                count = SQLCountPubsForPublisher(53666)
                self.assertEqual(INT_TYPE, str(type(count)))
                self.assertGreater(count, 0)

        def test_056_SQLGetPublisherYears(self):
                print("TEST: SQLGetPublisherYears")
                years = SQLGetPublisherYears(53666)
                self.assertEqual(LIST_TYPE, str(type(years)))
                self.assertGreater(len(years), 0)

        def test_057_SQLgetNotes(self):
                print("TEST: SQLgetNotes")
                # Series 23 (Pellucidar) has note_id 428890
                note = SQLgetNotes(428890)
                self.assertEqual(STR_TYPE, str(type(note)))
                self.assertIn("Earth", note)
                empty_note = SQLgetNotes(0)
                self.assertEqual('', empty_note)

        def test_058_SQLGetLangIdByName(self):
                print("TEST: SQLGetLangIdByName")
                lang_id = SQLGetLangIdByName('English')
                self.assertEqual(17, lang_id)
                not_found = SQLGetLangIdByName('_NO_SUCH_LANGUAGE_')
                self.assertEqual(0, not_found)

        def test_059_SQLGetLangIdByCode(self):
                print("TEST: SQLGetLangIdByCode")
                langs = SQLLoadFullLanguages()
                if langs:
                        code = langs[0][LANGUAGE_CODE]
                        lang_id = langs[0][LANGUAGE_ID]
                        result = SQLGetLangIdByCode(code)
                        self.assertEqual(lang_id, result)
                not_found = SQLGetLangIdByCode('_NO_SUCH_CODE_')
                self.assertEqual(0, not_found)

        def test_060_SQLGetLangIdByTitle(self):
                print("TEST: SQLGetLangIdByTitle")
                # Title 1050 (The Talisman) is English (lang_id 17)
                lang_id = SQLGetLangIdByTitle(1050)
                self.assertEqual(17, lang_id)
                empty = SQLGetLangIdByTitle(999999999)
                self.assertEqual('', empty)

        def test_061_SQLLoadRecognizedDomains(self):
                print("TEST: SQLLoadRecognizedDomains")
                domains = SQLLoadRecognizedDomains()
                self.assertEqual(LIST_TYPE, str(type(domains)))
                self.assertGreater(len(domains), 0)
                domain = domains[0]
                self.assertEqual(INT_TYPE, str(type(domain[DOMAIN_ID])))
                self.assertEqual(STR_TYPE, str(type(domain[DOMAIN_NAME])))

        def test_062_SQLGetRecognizedDomainByID(self):
                print("TEST: SQLGetRecognizedDomainByID")
                domains = SQLLoadRecognizedDomains()
                domain_id = domains[0][DOMAIN_ID]
                result = SQLGetRecognizedDomainByID(domain_id)
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(domain_id, result[DOMAIN_ID])
                not_found = SQLGetRecognizedDomainByID(999999999)
                self.assertIsNone(not_found)

        def test_063_SQLLoadIdentifierTypes(self):
                print("TEST: SQLLoadIdentifierTypes")
                result = SQLLoadIdentifierTypes()
                self.assertEqual(DICT_TYPE, str(type(result)))
                self.assertGreater(len(result), 0)
                for type_number in result:
                        self.assertEqual(INT_TYPE, str(type(type_number)))
                        info = result[type_number]
                        self.assertEqual(TUPLE_TYPE, str(type(info)))
                        break

        def test_064_SQLLoadIdentifiers(self):
                print("TEST: SQLLoadIdentifiers")
                result = SQLLoadIdentifiers(48332)
                self.assertEqual(LIST_TYPE, str(type(result)))
                empty = SQLLoadIdentifiers(999999999)
                self.assertEqual([], empty)

        def test_065_SQLLoadIdentifierSites(self):
                print("TEST: SQLLoadIdentifierSites")
                result = SQLLoadIdentifierSites()
                self.assertEqual(LIST_TYPE, str(type(result)))
                self.assertGreater(len(result), 0)

        def test_066_SQLFindPubByExternalID(self):
                print("TEST: SQLFindPubByExternalID")
                id_types = SQLLoadIdentifierTypes()
                if id_types:
                        first_type = list(id_types.keys())[0]
                        no_match = SQLFindPubByExternalID(first_type, '_NO_SUCH_ID_XYZZY_')
                        self.assertEqual(LIST_TYPE, str(type(no_match)))
                        self.assertEqual([], no_match)

        def test_067_SQLGetRefDetails(self):
                print("TEST: SQLGetRefDetails")
                results = SQLGetRefDetails()
                self.assertEqual(LIST_TYPE, str(type(results)))
                self.assertGreater(len(results), 0)
                ref = results[0]
                self.assertEqual(INT_TYPE, str(type(ref[REFERENCE_ID])))
                self.assertEqual(STR_TYPE, str(type(ref[REFERENCE_LABEL])))

        def test_068_SQLGetVerificationSource(self):
                print("TEST: SQLGetVerificationSource")
                refs = SQLGetRefDetails()
                ref_id = refs[0][REFERENCE_ID]
                result = SQLGetVerificationSource(ref_id)
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(ref_id, result[REFERENCE_ID])
                not_found = SQLGetVerificationSource(999999999)
                self.assertIsNone(not_found)

        def test_069_SQLGetVerificationSourceByLabel(self):
                print("TEST: SQLGetVerificationSourceByLabel")
                refs = SQLGetRefDetails()
                label = refs[0][REFERENCE_LABEL]
                result = SQLGetVerificationSourceByLabel(label)
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(label, result[REFERENCE_LABEL])
                not_found = SQLGetVerificationSourceByLabel('_NO_SUCH_LABEL_')
                self.assertIsNone(not_found)

        def test_070_SQLVerificationStatus(self):
                print("TEST: SQLVerificationStatus")
                status = SQLVerificationStatus(48332)
                self.assertIn(status, [0, 1, 2])

        def test_071_SQLPrimaryVerifiers(self):
                print("TEST: SQLPrimaryVerifiers")
                result = SQLPrimaryVerifiers(48332)
                self.assertEqual(LIST_TYPE, str(type(result)))

        def test_072_SQLSecondaryVerifications(self):
                print("TEST: SQLSecondaryVerifications")
                result = SQLSecondaryVerifications(48332)
                self.assertEqual(LIST_TYPE, str(type(result)))

        def test_073_SQLGetPubContentList(self):
                print("TEST: SQLGetPubContentList")
                result = SQLGetPubContentList(48332)
                self.assertEqual(LIST_TYPE, str(type(result)))
                self.assertGreater(len(result), 0)

        def test_074_SQLLoadRawTemplates(self):
                print("TEST: SQLLoadRawTemplates")
                result = SQLLoadRawTemplates()
                self.assertEqual(LIST_TYPE, str(type(result)))
                self.assertGreater(len(result), 0)
                template = result[0]
                self.assertEqual(INT_TYPE, str(type(template[TEMPLATE_ID])))
                self.assertEqual(STR_TYPE, str(type(template[TEMPLATE_NAME])))

        def test_075_SQLGetTemplate(self):
                print("TEST: SQLGetTemplate")
                templates = SQLLoadRawTemplates()
                template_id = templates[0][TEMPLATE_ID]
                result = SQLGetTemplate(template_id)
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(template_id, result[TEMPLATE_ID])
                not_found = SQLGetTemplate(999999999)
                self.assertIsNone(not_found)

        def test_076_SQLGetTemplateByName(self):
                print("TEST: SQLGetTemplateByName")
                templates = SQLLoadRawTemplates()
                template_name = templates[0][TEMPLATE_NAME]
                result = SQLGetTemplateByName(template_name)
                self.assertEqual(TUPLE_TYPE, str(type(result)))
                self.assertEqual(template_name, result[TEMPLATE_NAME])
                not_found = SQLGetTemplateByName('_NO_SUCH_TEMPLATE_')
                self.assertIsNone(not_found)

        def test_077_SQLLoadAllTemplates(self):
                print("TEST: SQLLoadAllTemplates")
                result = SQLLoadAllTemplates()
                self.assertEqual(DICT_TYPE, str(type(result)))
                self.assertGreater(len(result), 0)
                for name in result:
                        self.assertEqual(STR_TYPE, str(type(name)))
                        self.assertEqual(TUPLE_TYPE, str(type(result[name])))
                        break

        def test_078_SQLQueueSize(self):
                print("TEST: SQLQueueSize")
                size = SQLQueueSize()
                self.assertEqual(INT_TYPE, str(type(size)))
                self.assertGreaterEqual(size, 0)

        def test_079_SQLGetDbaseTime(self):
                print("TEST: SQLGetDbaseTime")
                from datetime import datetime
                result = SQLGetDbaseTime()
                if result is not None:
                        self.assertIsInstance(result, datetime)

        def test_080_SQLisUserModerator(self):
                print("TEST: SQLisUserModerator")
                result = SQLisUserModerator(0)
                self.assertEqual(0, result)

        def test_081_SQLisUserBureaucrat(self):
                print("TEST: SQLisUserBureaucrat")
                result = SQLisUserBureaucrat(0)
                self.assertEqual(0, result)

        def test_082_SQLisUserSelfApprover(self):
                print("TEST: SQLisUserSelfApprover")
                result = SQLisUserSelfApprover(0)
                self.assertEqual(0, result)

        def test_083_SQLisUserWebAPI(self):
                print("TEST: SQLisUserWebAPI")
                result = SQLisUserWebAPI(0)
                self.assertEqual(0, result)

        def test_084_SQLisUserBlocked(self):
                print("TEST: SQLisUserBlocked")
                result = SQLisUserBlocked(0)
                self.assertIn(result, [0, 1])

        def test_085_SQLUserPrivileges(self):
                print("TEST: SQLUserPrivileges")
                result = SQLUserPrivileges(0)
                self.assertEqual(STR_TYPE, str(type(result)))
                self.assertEqual('Editor', result)

        def test_086_SQLgetUserName(self):
                print("TEST: SQLgetUserName")
                name = SQLgetUserName(0)
                self.assertEqual(STR_TYPE, str(type(name)))
                self.assertEqual('UNKNOWN', name)

        def test_087_SQLgetSubmitterID(self):
                print("TEST: SQLgetSubmitterID")
                user_id = SQLgetSubmitterID('_NO_SUCH_USER_XYZZY_')
                self.assertEqual(INT_TYPE, str(type(user_id)))
                self.assertEqual(0, user_id)

        def test_088_SQLhasNewTalk(self):
                print("TEST: SQLhasNewTalk")
                result = SQLhasNewTalk(0)
                self.assertIn(result, [0, 1])

        def test_089_SQLLoadUserPreferences(self):
                print("TEST: SQLLoadUserPreferences")
                prefs = SQLLoadUserPreferences(0)
                self.assertEqual(TUPLE_TYPE, str(type(prefs)))
                self.assertEqual(13, len(prefs))
                self.assertEqual(17, prefs[1])

        def test_090_SQLLoadUserLanguages(self):
                print("TEST: SQLLoadUserLanguages")
                result = SQLLoadUserLanguages(0)
                self.assertEqual(LIST_TYPE, str(type(result)))
                self.assertEqual([17], result)

        def test_091_SQLCountPendingSubsForUser(self):
                print("TEST: SQLCountPendingSubsForUser")
                count = SQLCountPendingSubsForUser(0)
                self.assertEqual(INT_TYPE, str(type(count)))
                self.assertGreaterEqual(count, 0)

        def test_092_SQLsearchTags(self):
                print("TEST: SQLsearchTags")
                results = SQLsearchTags('fiction')
                self.assertEqual(LIST_TYPE, str(type(results)))
                for tag in results:
                        self.assertEqual(INT_TYPE, str(type(tag[TAG_ID])))
                        self.assertEqual(STR_TYPE, str(type(tag[TAG_NAME])))
                        break
                none = SQLsearchTags('_NO_SUCH_TAG_XYZZY_')
                self.assertEqual([], none)

        def test_093_SQLGetTagById(self):
                print("TEST: SQLGetTagById")
                tags = SQLsearchTags('fiction')
                if tags:
                        tag_id = tags[0][TAG_ID]
                        result = SQLGetTagById(tag_id)
                        self.assertEqual(TUPLE_TYPE, str(type(result)))
                        self.assertEqual(tag_id, result[TAG_ID])
                not_found = SQLGetTagById(999999999)
                self.assertEqual(0, not_found)

        def test_094_SQLLoadPrivateTags(self):
                print("TEST: SQLLoadPrivateTags")
                result = SQLLoadPrivateTags()
                self.assertEqual(LIST_TYPE, str(type(result)))

        def test_095_SQLauthorIsPseudo(self):
                print("TEST: SQLauthorIsPseudo")
                # Author 177072 is a pseudo of Jules Verne (159)
                is_pseudo = SQLauthorIsPseudo(177072)
                self.assertEqual(1, is_pseudo)
                not_pseudo = SQLauthorIsPseudo(159)
                self.assertEqual(0, not_pseudo)

        def test_096_SQLauthorHasPseudo(self):
                print("TEST: SQLauthorHasPseudo")
                # Jules Verne (159) has at least one pseudo
                has_pseudo = SQLauthorHasPseudo(159)
                self.assertEqual(1, has_pseudo)

        def test_097_SQLgetPseudoFromActual(self):
                print("TEST: SQLgetPseudoFromActual")
                pseudos = SQLgetPseudoFromActual(159)
                self.assertEqual(LIST_TYPE, str(type(pseudos)))
                self.assertGreater(len(pseudos), 0)
                for item in pseudos:
                        self.assertEqual(LIST_TYPE, str(type(item)))
                        break

        def test_098_SQLgetTitle(self):
                print("TEST: SQLgetTitle")
                title = SQLgetTitle(1050)
                self.assertEqual(STR_TYPE, str(type(title)))
                self.assertEqual('The Talisman', title)
                not_found = SQLgetTitle(999999999)
                self.assertEqual('', not_found)

        def test_099_SQLgetPubTitle(self):
                print("TEST: SQLgetPubTitle")
                title = SQLgetPubTitle(47772)
                self.assertEqual(STR_TYPE, str(type(title)))
                self.assertGreater(len(title), 0)
                not_found = SQLgetPubTitle(999999999)
                self.assertEqual('', not_found)

        def test_100_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()

if __name__ == '__main__':
        unittest.main()
