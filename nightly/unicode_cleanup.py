#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2022   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 844 $
#     Date: $Date: 2022-02-15 16:06:20 -0500 (Tue, 15 Feb 2022) $

from SQLparsing import *
from library import *
from shared_cleanup_lib import *

def unicode_cleanup():
        #   Reports 65-70: Publishers, pub series, series, authors, titles
        #                  pubs with invalid Unicode characters
        badUnicodeReport('publishers', 'publisher_name', 'publisher_id', 65)
        badUnicodeReport('pub_series', 'pub_series_name', 'pub_series_id', 66)
        badUnicodeReport('series', 'series_title', 'series_id', 67)
        badUnicodeReport('authors', 'author_canonical', 'author_id', 68)
        badUnicodeReport('titles', 'title_title', 'title_id', 69)
        badUnicodeReport('pubs', 'pub_title', 'pub_id', 70)

        #   Report 73: Publishers with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('publisher_name')
        query = """select publisher_id from publishers where %s""" % pattern_match
        standardReport(query, 73)

        #   Report 74: Titles with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('title_title')
        query = """select title_id from titles where %s""" % pattern_match
        standardReport(query, 74)

        #   Report 75: Publications with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('pub_title')
        query = """select pub_id from pubs where %s""" % pattern_match
        standardReport(query, 75)

        #   Report 76: Series with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('series_title')
        query = """select series_id from series where %s""" % pattern_match
        standardReport(query, 76)

        #   Report 77: Publication Series with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('pub_series_name')
        query = """select pub_series_id from pub_series where %s""" % pattern_match
        standardReport(query, 77)

        #   Report 78: Authors with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('author_canonical')
        query = """select author_id from authors where %s""" % pattern_match
        standardReport(query, 78)

def badUnicodeReport(table, record_title, record_id, report_number):
        pattern_match = ISFDBBadUnicodePatternMatch(record_title)
        where_clause = "%s like '%%&#%%' and (%s)" % (record_title, pattern_match)
        query = """select %s from %s where %s""" % (record_id, table, where_clause)
        standardReport(query, report_number)
