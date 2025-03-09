#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2024   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 460 $
#     Date: $Date: 2019-10-04 21:29:45 -0400 (Fri, 04 Oct 2019) $

import string
from SQLparsing import *
from library import *
from shared_cleanup_lib import *

def transliterations():
        #   Report 85: Non-Latin authors with Latin characters in legal names
        query = """select a.author_id from authors a, languages l
                where a.author_language = l.lang_id
                and l.latin_script='No'
                and author_legalname regexp'[[:alpha:]]'
                """
        standardReport(query, 85)

        #   Report 97: Pub series with non-Latin Title records 
        #   where the pub series name contains Latin characters
        query = """select distinct ps.pub_series_id
                from pub_series ps, pubs p, pub_content pc, titles t use index (language), languages l
                where ps.pub_series_id = p.pub_series_id
                and p.pub_id = pc.pub_id
                and pc.title_id = t.title_id
                and t.title_language = l.lang_id
                and l.latin_script = 'No'
                and ps.pub_series_name regexp'[[:alpha:]]'
                """
        standardReport(query, 97)

        #   Report 99: Non-Latin Title records with 
        #   the publisher name containing Latin characters
        query = """select distinct pb.publisher_id
                from publishers pb, pubs p, pub_content pc, titles t use index (language), languages l
                where pb.publisher_id = p.publisher_id
                and p.pub_id = pc.pub_id
                and pc.title_id = t.title_id
                and t.title_language = l.lang_id
                and l.latin_script = 'No'
                and pb.publisher_name regexp'[[:alpha:]]'
                """
        standardReport(query, 99)

        #   Report 121: Publication series names with non-Latin characters without
        #   a transliterated name '[[:alpha:]]'
        query = """select pub_series_id from pub_series
                where pub_series_name regexp '&#'
                and not exists
                  (select 1 from trans_pub_series tps where tps.pub_series_id = pub_series.pub_series_id)
                """
        standardReport(query, 121)

        #   Report 122: Publisher names with non-Latin characters without
        #   a transliterated name
        query = """select publisher_id from publishers
                where publisher_name regexp '&#'
                and not exists
                  (select 1 from trans_publisher tp where tp.publisher_id = publishers.publisher_id)
                """
        standardReport(query, 122)

        #   Report 123: Authors with values in the trans_legal_names table that have no
        #               value in the author_legalname field
        query = """select a.author_id from authors a
                where (a.author_legalname = '' or a.author_legalname IS NULL)
                and exists
                 (select 1 from trans_legal_names tr
                 where tr.author_id = a.author_id)
                """
        standardReport(query, 123)

        #   Reports 124-136: Titles with non-Latin characters without
        #   a transliterated title for common languages
        reports = transliteratedReports('titles')
        for report in reports:
                report_id = report[1]
                language_name = report[0]
                query = """select t.title_id from titles t, languages l
                        where t.title_title regexp '&#'
                        and t.title_language = l.lang_id
                        and l.lang_name = '%s'
                        and not exists
                          (select 1 from trans_titles tt where tt.title_id = t.title_id)
                        """ % language_name
                standardReport(query, report_id)

        #   Report 137: Titles with non-Latin characters without
        #   a transliterated title for uncommon languages
        reports = transliteratedReports('titles')
        languages = []
        for report in reports:
                language_name = report[0]
                languages.append(language_name)
        languages_in_clause = list_to_in_clause(languages)
        query = """select distinct t.title_id from titles t, languages l
                where t.title_title regexp '&#'
                and ((t.title_language = l.lang_id and l.lang_name not in (%s))
                      or t.title_language is null)
                and not exists
                  (select 1 from trans_titles tt where tt.title_id = t.title_id)
                """ % languages_in_clause
        standardReport(query, 137)

        nonLatiTitlesWithLatinChars()

        #   Report 145: Romanian titles with s-cedilla or t-cedilla in the title
        query = """select title_id from titles
                   where title_language = 54
                   and (
                           title_title like '%&#350%'
                           or title_title like '%&#351%'
                           or title_title like '%&#354%'
                           or title_title like '%&#355%'
                        )
                   """
        standardReport(query, 145)

        #   Report 146: Pubs with Romanian titles with s-cedilla or t-cedilla in the pub title
        query = """select distinct p.pub_id from pubs p, pub_content pc, titles t
                   where p.pub_id = pc.pub_id
                   and pc.title_id = t.title_id
                   and t.title_language = 54
                   and (
                           pub_title like '%&#350%'
                           or pub_title like '%&#351%'
                           or pub_title like '%&#354%'
                           or pub_title like '%&#355%'
                        )
                   """
        standardReport(query, 146)

        #   Report 147: Pubs with fullwidth yen signs
        query = """select distinct pub_id from pubs
                   where pub_price like '%&#65509;%'
                   """
        standardReport(query, 147)

        pubsWithNonLatin()

        #   Reports 162-166: Pubs with non-Latin titles with Latin characters
        # in pub titles for common non-Latin languages
        reports = popularNonLatinLanguages('pubs')
        for report in reports:
                report_id = report[1]
                language_name = report[0]
                query = """select distinct p.pub_id
                        from pubs p, pub_content pc, titles t, languages l
                        where p.pub_title regexp'[[:alpha:]]'
                        and p.pub_id = pc.pub_id
                        and pc.title_id = t.title_id
                        and t.title_language = l.lang_id
                        and t.title_ttype != 'COVERART'
                        and t.title_ttype != 'INTERIORART'
                        and l.lang_name = '%s'
                        """ % language_name
                standardReport(query, report_id)

        #   Report 167: Pubs with non-Latin titles with Latin characters
        # in pub titles for less common non-Latin languages
        reports = popularNonLatinLanguages('pubs')
        languages = []
        for report in reports:
                language_name = report[0]
                languages.append(language_name)
        languages_in_clause = list_to_in_clause(languages)
        query = """select distinct p.pub_id
                   from pubs p, pub_content pc, titles t USE INDEX (language), languages l
                   where p.pub_title regexp'[[:alpha:]]'
                   and p.pub_id = pc.pub_id
                   and pc.title_id = t.title_id
                   and t.title_language = l.lang_id
                   and t.title_ttype != 'COVERART'
                   and t.title_ttype != 'INTERIORART'
                   and l.lang_name not in (%s)
                   and l.latin_script = 'No'
                """ % languages_in_clause
        standardReport(query, 167)

        #   Report 168: Authors with only one title and that title is
        #               in a non-Latin language
        query = """select a.author_id
                   from authors a, languages l, canonical_author ca1, titles t
                   where (select count(*) from canonical_author ca2
                          where ca2.author_id = a.author_id) = 1
                   and ca1.author_id = a.author_id
                   and ca1.title_id = t.title_id
                   and t.title_language = l.lang_id
                   and l.latin_script = 'No'
                   and not exists(select 1 from trans_authors ta
                                  where ta.author_id = a.author_id)"""
        standardReport(query, 168)

        #   Reports 169-181: Authors whose working language is one of the "popular" ones
        #   and no transliterated names on file for common languages 
        reports = transliteratedReports('authors')
        for report in reports:
                report_id = report[1]
                language_name = report[0]
                query = """select a.author_id from authors a, languages l
                           where not exists (
                             select 1 from trans_authors ta
                             where ta.author_id = a.author_id)
                           and a.author_canonical regexp '&#'
                           and a.author_language = l.lang_id
                           and l.lang_name = '%s'
                        """ % language_name
                standardReport(query, report_id)

        #   Report 182: Authors whose working language is one of the "popular" ones
        #   and no transliterated names on file for uncommon languages
        reports = transliteratedReports('authors')
        languages = []
        for report in reports:
                language_name = report[0]
                languages.append(language_name)
        languages_in_clause = list_to_in_clause(languages)
        query = """select a.author_id from authors a, languages l
                           where not exists (
                             select 1 from trans_authors ta
                             where ta.author_id = a.author_id)
                           and a.author_canonical regexp '&#'
                           and a.author_language = l.lang_id
                           and l.lang_name not in (%s)
                """ % languages_in_clause
        standardReport(query, 182)

        #   Reports 183-187: Non-Latin Language Titles with a Latin
        #   Author Name for common non-Latin languages
        reports = popularNonLatinLanguages('authors')
        for report in reports:
                report_id = report[1]
                language_name = report[0]
                query = """select distinct t.title_id
                        from titles t, languages l, authors a, canonical_author ca
                        where t.title_language = l.lang_id
                        and l.lang_name = '%s'
                        and a.author_canonical not regexp '&#'
                        and a.author_canonical not in ('unknown', 'uncredited')
                        and ca.title_id = t.title_id
                        and ca.author_id = a.author_id
                        and ca.ca_status = 1
                        """ % language_name
                standardReport(query, report_id)

        #   Report 188: Non-Latin Language Titles with a Latin Author Name
        #               for less common non-Latin languages
        reports = popularNonLatinLanguages('authors')
        languages = []
        for report in reports:
                language_name = report[0]
                languages.append(language_name)
        languages_in_clause = list_to_in_clause(languages)
        query = """select distinct t.title_id
                   from titles t USE INDEX (language), languages l, authors a, canonical_author ca
                   where t.title_language = l.lang_id
                   and l.lang_name not in (%s)
                   and l.latin_script = 'No'
                   and a.author_canonical not regexp '&#'
                   and a.author_canonical not in ('unknown', 'uncredited')
                   and ca.title_id = t.title_id
                   and ca.author_id = a.author_id
                   and ca.ca_status = 1
                """ % languages_in_clause
        standardReport(query, 188)

        #   Report 257: Series with non-Latin Characters in the Series Name without a Transliterated Name
        query = """select s.series_id from series s
                 where s.series_title regexp '&#'
                 and not exists
                 (select 1 from trans_series ts
                 where ts.series_id = s.series_id)"""
        standardReport(query, 257)

        #   Reports 258-262: Series without Unicode characters in the series names and
        # with constituent titles written in common non-Latin languages
        reports = popularNonLatinLanguages('series')
        for report in reports:
                report_id = report[1]
                language_name = report[0]
                query = """select distinct s.series_id
                        from series s, titles t, languages l
                        where s.series_title not regexp '&#'
                        and s.series_id = t.series_id
                        and t.title_language = l.lang_id
                        and t.title_ttype != 'COVERART'
                        and t.title_ttype != 'INTERIORART'
                        and l.lang_name = '%s'
                        """ % language_name
                standardReport(query, report_id)

        #   Report 263: Series without Unicode characters in the series names and
        # with constituent titles written in less common non-Latin languages
        reports = popularNonLatinLanguages('series')
        languages = []
        for report in reports:
                language_name = report[0]
                languages.append(language_name)
        languages_in_clause = list_to_in_clause(languages)
        query = """select distinct s.series_id
                   from series s, titles t USE INDEX (language), languages l
                   where s.series_title not regexp '&#'
                   and s.series_id = t.series_id
                   and t.title_language = l.lang_id
                   and t.title_ttype != 'COVERART'
                   and t.title_ttype != 'INTERIORART'
                   and l.lang_name not in (%s)
                   and l.latin_script = 'No'
                """ % languages_in_clause
        standardReport(query, 263)

def nonLatiTitlesWithLatinChars():
        #   Reports 138-143: Non-Latin titles with Latin characters
        reports = popularNonLatinLanguages('titles')
        reports_dict = {}
        for report in reports:
                language = report[0]
                report_id = report[1]
                reports_dict[language] = report_id
                standardDelete(report_id)

        query = """select t.title_id, l.lang_name
                from titles t, languages l
                where t.title_language = l.lang_id
                and l.latin_script = 'No'
                and t.title_title regexp'[[:alpha:]]'"""
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        cleanup_ids = {}
        record = CNX.DB_FETCHMANY()
        while record:
                title_id = record[0][0]
                lang_name = record[0][1]
                if lang_name in reports_dict:
                        report_id = reports_dict[lang_name]
                else:
                        report_id = 143
                if report_id not in cleanup_ids:
                        cleanup_ids[report_id] = []
                cleanup_ids[report_id].append(title_id)
                record = CNX.DB_FETCHMANY()

        for report_id in sorted(cleanup_ids):
                standardReportFromList(cleanup_ids[report_id], report_id)
  
def pubsWithNonLatin():
        #   Reports 148-161: Pub titles with non-Latin characters without
        #   an associated transliterated title
        reports = transliteratedReports('pubs')
        reports_dict = {}
        for report in reports:
                language = report[0]
                report_id = report[1]
                reports_dict[language] = report_id
                standardDelete(report_id)
        
        query = """select distinct p.pub_id
               from pubs p
               where p.pub_title regexp '&#'
               and not exists
               (select 1 from trans_pubs tp where p.pub_id = tp.pub_id)"""
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        pub_ids = []
        record = CNX.DB_FETCHMANY()
        while record:
                pub_ids.append(record[0][0])
                record = CNX.DB_FETCHMANY()
        if not pub_ids:
                return
        pub_ids_clause = list_to_in_clause(pub_ids)

        query = """select distinct p.pub_id, l.lang_name
               from pubs p, titles t, pub_content pc, languages l
               where p.pub_id in (%s)
               and p.pub_id = pc.pub_id
               and pc.title_id = t.title_id
               and t.title_language = l.lang_id""" % pub_ids_clause
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        cleanup_ids = {}
        while record:
                pub_id = record[0][0]
                lang_name = record[0][1]
                if lang_name in reports_dict:
                        report_id = reports_dict[lang_name]
                else:
                        report_id = 161
                if report_id not in cleanup_ids:
                        cleanup_ids[report_id] = []
                cleanup_ids[report_id].append(pub_id)
                record = CNX.DB_FETCHMANY()
        
        for report_id in sorted(cleanup_ids):
                standardReportFromList(cleanup_ids[report_id], report_id)
