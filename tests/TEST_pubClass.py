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
from pubClass import pubs
from xml.dom import minidom
from xml.dom import Node
import unittest

#####################################################################################
# Test for pubClass.py. This indirectly tests the following SQLparsing methods:
#
# SQLGetPageNumber
# SQLLoadAllLanguages
# SQLLoadIdentifiers
# SQLLoadIdentifierTypes
# SQLloadPubWebpages
# SQLloadTitle
# SQLloadTitlesXBT
# SQLloadTransPubTitles
# SQLTitleAuthors
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

def printPubRecord(pub):
        print("-------------------------------------------------")
        TryPrint("ID              =", pub.pub_id)
        TryPrint("TITLE           =", pub.pub_title)
        TryPrint("TAG             =", pub.pub_tag)
        TryPrint("YEAR            =", pub.pub_year)
        TryPrint("PAGES           =", pub.pub_pages)
        TryPrint("PTYPE           =", pub.pub_ptype)
        TryPrint("CTYPE           =", pub.pub_ctype)
        TryPrint("ISBN            =", pub.pub_isbn)
        TryPrint("CATALOG         =", pub.pub_catalog)
        TryPrint("IMAGE           =", pub.pub_image)
        TryPrint("PRICE           =", pub.pub_price)
        TryPrint("PUBLISHER ID    =", pub.pub_publisher_id)
        TryPrint("PUBLISHER       =", pub.pub_publisher)
        TryPrint("SERIES          =", pub.pub_series)
        TryPrint("SERIES ID       =", pub.pub_series_id)
        TryPrint("SERIES NUM      =", pub.pub_series_num)
        TryPrint("NOTE            =", pub.pub_note)

        # Lists
        print("AUTHORS:")
        for author in pub.pub_authors:
                TryPrint("  AUTHOR          =", author)
        print("ARTISTS:")
        for artist in pub.pub_artists:
                TryPrint("  ARTIST          =", artist)
        print("TRANSTITLES:")
        for trans_title in pub.pub_trans_titles:
                TryPrint("  TRANSTITLE      =", trans_title)
        print("WEBPAGES:")
        for webpage in pub.pub_webpages:
                TryPrint("  WEBPAGE         =", webpage)
        print("-------------------------------------------------")

def printPubRecordTypes(pub):
        TryPrint("ID              =", str(type(pub.pub_id)))
        TryPrint("TITLE           =", str(type(pub.pub_title)))
        TryPrint("TAG             =", str(type(pub.pub_tag)))
        TryPrint("YEAR            =", str(type(pub.pub_year)))
        TryPrint("PAGES           =", str(type(pub.pub_pages)))
        TryPrint("PTYPE           =", str(type(pub.pub_ptype)))
        TryPrint("CTYPE           =", str(type(pub.pub_ctype)))
        TryPrint("ISBN            =", str(type(pub.pub_isbn)))
        TryPrint("CATALOG         =", str(type(pub.pub_catalog)))
        TryPrint("IMAGE           =", str(type(pub.pub_image)))
        TryPrint("PRICE           =", str(type(pub.pub_price)))
        TryPrint("PUBLISHER ID    =", str(type(pub.pub_publisher_id)))
        TryPrint("PUBLISHER       =", str(type(pub.pub_publisher)))
        TryPrint("SERIES          =", str(type(pub.pub_series)))
        TryPrint("SERIES ID       =", str(type(pub.pub_series_id)))
        TryPrint("SERIES NUM      =", str(type(pub.pub_series_num)))
        TryPrint("NOTE            =", str(type(pub.pub_note)))
        TryPrint("AUTHORS         =", str(type(pub.pub_authors)))
        TryPrint("ARTISTS         =", str(type(pub.pub_artists)))
        TryPrint("TRANSTITLES     =", str(type(pub.pub_trans_titles)))
        TryPrint("WEBPAGES        =", str(type(pub.pub_webpages)))

class TestStorage(dict):
        def __init__(self, s=None):
                self.value = s
        def getvalue(self, theKey):
                return self[theKey]

class MyTestCase(unittest.TestCase):

        def test_001_load_Base(self):
                print("TEST: pubClass::load_Base")
                pub = pubs(db)
                pub.load(26549)

                if debug:
                        printPubRecord(pub)
                        printPubRecordTypes(pub)

                self.assertEqual(INT_TYPE, str(type(pub.pub_id)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_title)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_tag)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_year)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_pages)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_ptype)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_ctype)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_isbn)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_catalog)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_image)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_price)))
                self.assertEqual(INT_TYPE, str(type(pub.pub_publisher_id)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_publisher)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_series)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_series_id)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_series_num)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_note)))
                self.assertEqual(LIST_TYPE, str(type(pub.pub_authors)))
                self.assertEqual(LIST_TYPE, str(type(pub.pub_artists)))
                self.assertEqual(LIST_TYPE, str(type(pub.pub_trans_titles)))
                self.assertEqual(LIST_TYPE, str(type(pub.pub_webpages)))

        def test_002_load_TransWeb(self):
                print("TEST: pubClass::load_TransWeb")
                pub = pubs(db)
                pub.load(872624)

                if debug:
                        printPubRecord(pub)

        def test_003_load_Catalog(self):
                print("TEST: pubClass::load_Catalog")
                pub = pubs(db)
                pub.load(267729)

                if debug:
                        printPubRecord(pub)

        def test_004_load_PubSeries(self):
                print("TEST: pubClass::load_PubSeries")
                pub = pubs(db)
                pub.load(266473)

                if debug:
                        printPubRecord(pub)

        def test_005_authors(self):
                print("TEST: pubClass::authors")
                pub = pubs(db)
                pub.load(267729)
                retval = pub.authors()
                print("AUTHORS:", retval)

                if debug:
                        printPubRecord(pub)

        def test_006_artists(self):
                print("TEST: pubClass::artists")
                pub = pubs(db)
                pub.load(267729)
                retval = pub.artists()
                print("ARTISTS:", retval)

                if debug:
                        printPubRecord(pub)

        def test_007_obj2xml(self):
                print("TEST: pubClass::obj2xml")
                pub = pubs(db)
                pub.load(26549)
                xml = pub.obj2xml()
                print(xml)

                if debug:
                        printPubRecord(pub)
                        printPubRecordTypes(pub)

        def test_008_cgi2obj_requiredArgs(self):
                print("TEST: awardClass::cgi2obj_requiredArgs")
                print("==============================================")

                # Test 1 - Bad pub_id
                form = {
                    'pub_id': TestStorage('xyz'),
                    'pub_title': TestStorage('Bogus Title'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, "Publication ID must be an integer number")

                # Test 2 - No title ID
                form = {
                    'pub_id': TestStorage(26549),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, "No title specified")

                if debug:
                        printPubRecord(pub)

        def test_009_cgi2obj_Authors(self):
                print("TEST: awardClass::cgi2obj_Authors")
                print("==============================================")

                # Test 1 - No specified authors
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                if len(pub.error) > 1:
                        ChoppedError = pub.error[:25]
                self.assertEqual(ChoppedError, 'No authors were specified')

                # Test 2 - Successful authors
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_author2': TestStorage('Bill Simmons'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, "No year was specified")

        def test_010_cgi2obj_Meta(self):
                print("TEST: awardClass::cgi2obj_Meta")
                print("==============================================")

                # Test 1 - Mangled year
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_author2': TestStorage('Bill Simmons'),
                    'pub_year': TestStorage('Bogus'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.pub_year, '0000-00-00')

                # Test 2 - Good year
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_author2': TestStorage('Bill Simmons'),
                    'pub_year': TestStorage('1984'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.pub_year, '1984-00-00')

                # Test 3 - Bad ptype
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('xxxBOGUSxxx'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid Publication Format - xxxBOGUSxxx')

                # Test 4 - Bad ctype
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('xxxBOGUSxxx'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid Publication Type - xxxBOGUSxxx')

                # Test 5 - Bad image
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('yada.com'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, ' URLs must start with http or https')

                # Test 6 - Bad webpage
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('httttp://yada.com'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, ' URLs must start with http or https')

                # Test 7 - Bad external_id
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'external_id.xxx': TestStorage('ASIN'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid identifier type')

                # Test 8 - Success
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, '')

                if debug:
                        printPubRecord(pub)

                self.assertEqual(INT_TYPE, str(type(pub.pub_id)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_title)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_tag)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_year)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_pages)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_ptype)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_ctype)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_isbn)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_catalog)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_image)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_price)))
                self.assertEqual(INT_TYPE, str(type(pub.pub_publisher_id)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_publisher)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_series)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_series_id)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_series_num)))
                self.assertEqual(STR_TYPE, str(type(pub.pub_note)))
                self.assertEqual(LIST_TYPE, str(type(pub.pub_authors)))
                self.assertEqual(LIST_TYPE, str(type(pub.pub_artists)))
                self.assertEqual(LIST_TYPE, str(type(pub.pub_trans_titles)))
                self.assertEqual(LIST_TYPE, str(type(pub.pub_webpages)))

        def test_011_cgi2obj_CoverArt(self):

                # Test 1 - Invalid Cover ID
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id0': TestStorage(0),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid Cover ID')

                if debug:
                        printPubRecord(pub)

                # Test 2 - Invalid Cover ID Value
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('xyz'),
                    'X.cover_artist1.170': TestStorage('0'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid Cover ID Value')

                if debug:
                        printPubRecord(pub)

                # Test 3 - Invalid Cover ID
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('0'),
                    'X.cover_artist0.170': TestStorage('0'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid Cover ID')

                if debug:
                        printPubRecord(pub)

                # Test 3 - Invalid Artist ID
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('0'),
                    'X.cover_artist1.0': TestStorage('0'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid Artist ID')

                if debug:
                        printPubRecord(pub)
                    #'X.cover_artist1.170': TestStorage('170'),

                # Test 4 - Invalid Cover Title ID
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('0'),
                    'X.cover_artist1.170': TestStorage('0'),
                    'X.cover_title0': TestStorage('0'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid Cover Title ID')

                if debug:
                        printPubRecord(pub)

                # Test 5 - Invalid Cover Date ID
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('0'),
                    'X.cover_artist1.170': TestStorage('0'),
                    'X.cover_title1': TestStorage('0'),
                    'X.cover_date0': TestStorage('0'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid Cover Date ID')

                if debug:
                        printPubRecord(pub)

                # Test 6 - Invalid Cover Date ID
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('0'),
                    'X.cover_artist1.170': TestStorage('0'),
                    'X.cover_title1': TestStorage('0'),
                    'X.cover_date1': TestStorage('0'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, '')

                if debug:
                        printPubRecord(pub)

        def test_012_cgi2obj_Titles(self):

                # Test 1 - Missing Title with Page
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('0'),
                    'X.cover_artist1.170': TestStorage('0'),
                    'X.cover_title1': TestStorage('0'),
                    'X.cover_date1': TestStorage('0'),
                    'title_page1': TestStorage('42'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Entry must have a title. Page=42')
                if debug:
                        printPubRecord(pub)

                # Test 2 - Missing Title with Author
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('0'),
                    'X.cover_artist1.170': TestStorage('0'),
                    'X.cover_title1': TestStorage('0'),
                    'X.cover_date1': TestStorage('0'),
                    'title_author1.1': TestStorage('42'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Entry must have a title. Author=42')
                if debug:
                        printPubRecord(pub)

                # Test 3 - invalid Title Type
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('0'),
                    'X.cover_artist1.170': TestStorage('0'),
                    'X.cover_title1': TestStorage('0'),
                    'X.cover_date1': TestStorage('0'),
                    'title_title1': TestStorage('0'),
                    'title_id1': TestStorage('40762'),
                    'title_page1': TestStorage('15'),
                    'title_author1.1': TestStorage('170'),
                    'title_ttype1': TestStorage('xyz'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid title type')
                if debug:
                        printPubRecord(pub)

                # Test 4 - invalid Story Length
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('0'),
                    'X.cover_artist1.170': TestStorage('0'),
                    'X.cover_title1': TestStorage('0'),
                    'X.cover_date1': TestStorage('0'),
                    'title_title1': TestStorage('0'),
                    'title_id1': TestStorage('40762'),
                    'title_page1': TestStorage('15'),
                    'title_author1.1': TestStorage('170'),
                    'title_ttype1': TestStorage('SHORTFICTION'),
                    'title_storylen1': TestStorage('xyz'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, 'Invalid short fiction length')
                if debug:
                        printPubRecord(pub)

                # Test 5 - Success
                form = {
                    'pub_id': TestStorage(26549),
                    'pub_title': TestStorage('Prayers to Broken Stones'),
                    'pub_author1': TestStorage('Dan Simmons'),
                    'pub_year': TestStorage('1984'),
                    'pub_tag': TestStorage('PTBS1990'),
                    'pub_publisher': TestStorage('Dark Harvest'),
                    'pub_series_num': TestStorage('3'),
                    'pub_pages': TestStorage('viii+322+[7]'),
                    'pub_ptype': TestStorage('hc'),
                    'pub_ctype': TestStorage('COLLECTION'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_catalog': TestStorage('Nice Cat'),
                    'pub_image': TestStorage('http://yada.com/test.jpg'),
                    'pub_webpages': TestStorage('http://yada.com'),
                    'pub_price': TestStorage('$10.99'),
                    'external_id.1': TestStorage('1'),
                    'external_id_type.1': TestStorage('1'),
                    'X.cover_id1': TestStorage('0'),
                    'X.cover_artist1.170': TestStorage('0'),
                    'X.cover_title1': TestStorage('0'),
                    'X.cover_date1': TestStorage('0'),
                    'title_title1': TestStorage('0'),
                    'title_id1': TestStorage('40762'),
                    'title_page1': TestStorage('15'),
                    'title_author1.1': TestStorage('170'),
                    'title_ttype1': TestStorage('SHORTFICTION'),
                    'title_storylen1': TestStorage('novella'),
                }
                pub = pubs(db)
                pub.cgi2obj('explicit', form)
                self.assertEqual(pub.error, '')
                if debug:
                        printPubRecord(pub)

        def test_100_dumpLog(self):
                print(".")
                print("SQL Log")
                SQLoutputLog()

if __name__ == '__main__':
        unittest.main()
