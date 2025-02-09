#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
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

def translations_cleanup():
        #   Report 238: Translations without Notes - Less Common Languages
        query = """select t3.title_id from
                (select t1.title_id
                from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and t1.title_ttype not in ('COVERART','INTERIORART')
                and t1.title_language != t2.title_language
                and t1.title_language not in (17, 36, 22, 26, 16, 53, 59, 37)
                and not exists (select 1 from notes n where t1.note_id = n.note_id))
                as t3, titles t4
                where t3.title_id = t4.title_id
                order by t4.title_title"""
        standardReport(query, 238)

        #   Report 239: Translations without the Tr Template in Notes
        query = """select t1.title_id
                from titles t1, titles t2, notes n
                where t1.title_parent = t2.title_id
                and t1.title_ttype not in ('COVERART','INTERIORART')
                and t1.title_language != t2.title_language
                and t1.note_id = n.note_id
                and n.note_note not like '%{{Tr|%'
                order by t1.title_title
                limit 1000"""
        standardReport(query, 239)
        
        #   Reports 264-271: Language-specific Translations without Notes
        reports = ISFDBtranslatedReports()
        for report_id in sorted(reports):
                language_id = reports[report_id]
                translationsWithoutNotes(report_id, language_id)

        #   Report 308: English book-length titles with no publications and with a translation
        translationsWithoutOriginalPubs(308, 'English')

        #   Report 309: French book-length titles with no publications and with a translation
        translationsWithoutOriginalPubs(309, 'French')

        #   Report 310: German book-length titles with no publications and with a translation
        translationsWithoutOriginalPubs(310, 'German')

        #   Report 311: Italian book-length titles with no publications and with a translation
        translationsWithoutOriginalPubs(311, 'Italian')

        #   Report 312: Japanese book-length titles with no publications and with a translation
        translationsWithoutOriginalPubs(312, 'Japanese')

        #   Report 313: Russian book-length titles with no publications and with a translation
        translationsWithoutOriginalPubs(313, 'Russian')

        #   Report 314: Spanish book-length titles with no publications and with a translation
        translationsWithoutOriginalPubs(314, 'Spanish')

        #   Report 315: Other book-length titles with no publications and with a translation
        otherTranslationsWithoutOriginalPubs(315, 'long')
        
        #   Report 316: English short titles with no publications and with a translation
        translationsWithoutOriginalPubs(316, 'English', 'short')

        #   Report 317: French short titles with no publications and with a translation
        translationsWithoutOriginalPubs(317, 'French', 'short')

        #   Report 318: German short titles with no publications and with a translation
        translationsWithoutOriginalPubs(318, 'German', 'short')

        #   Report 319: Italian short titles with no publications and with a translation
        translationsWithoutOriginalPubs(319, 'Italian', 'short')

        #   Report 320: Japanese short titles with no publications and with a translation
        translationsWithoutOriginalPubs(320, 'Japanese', 'short')

        #   Report 321: Russian short titles with no publications and with a translation
        translationsWithoutOriginalPubs(321, 'Russian', 'short')

        #   Report 322: Spanish short titles with no publications and with a translation
        translationsWithoutOriginalPubs(322, 'Spanish', 'short')

        #   Report 323: Other short titles with no publications and with a translation
        otherTranslationsWithoutOriginalPubs(323, 'short')

        #   Report 329: Translations with Tr template in Pub Notes and no Tr template in Title notes
        query = """select distinct(t.title_id)
                   from titles t, pubs p, pub_content pc, notes n_t, notes n_p
                   where t.title_id=pc.title_id
                   and p.pub_id=pc.pub_id
                   and t.note_id=n_t.note_id
                   and n_t.note_note not like '%{{Tr|%'
                   and p.note_id=n_p.note_id
                   and n_p.note_note like '%{{Tr|%'
                   and t.title_ttype=p.pub_ctype"""
        standardReport(query, 329)


def translationsWithoutOriginalPubs(report_id, lang_name, length = 'long'):
        if length == 'short':
                in_clause = 'not in'
        else:
                in_clause = 'in'
        query = """select t1.title_id
                from titles t1, languages l
                where exists
                        (select 1 from titles t2
                        where t2.title_parent = t1.title_id
                        and t2.title_language != t1.title_language)
                and not exists
                        (select 1 from pub_content pc
                        where pc.title_id = t1.title_id)
                and not exists
                        (select 1 from titles t3
                        where t3.title_parent = t1.title_id
                        and t3.title_language = t1.title_language)
                and t1.title_language = l.lang_id
                and l.lang_name = '%s'
                and t1.title_copyright not in ('8888-00-00', '0000-00-00')
                and t1.title_ttype %s ('NOVEL', 'COLLECTION', 'ANTHOLOGY', 'NONFICTION', 'OMNIBUS')""" % (lang_name, in_clause)
        standardReport(query, report_id)

def otherTranslationsWithoutOriginalPubs(report_id, length = 'long'):
        if length == 'short':
                in_clause = 'not in'
        else:
                in_clause = 'in'
        query = """select t1.title_id
                from titles t1, languages l
                where exists
                        (select 1 from titles t2
                        where t2.title_parent = t1.title_id
                        and t2.title_language != t1.title_language)
                and not exists
                        (select 1 from pub_content pc
                        where pc.title_id = t1.title_id)
                and not exists
                        (select 1 from titles t3
                        where t3.title_parent = t1.title_id
                        and t3.title_language = t1.title_language)
                and t1.title_language = l.lang_id
                and l.lang_name not in ('English', 'French', 'German', 'Italian', 'Japanese', 'Russian', 'Spanish')
                and t1.title_copyright not in ('8888-00-00', '0000-00-00')
                and t1.title_ttype %s ('NOVEL', 'COLLECTION', 'ANTHOLOGY', 'NONFICTION', 'OMNIBUS')""" % in_clause
        standardReport(query, report_id)

def translationsWithoutNotes(report_id, language_id):
        query = """select t3.title_id from
                (select t1.title_id
                from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and t1.title_ttype not in ('COVERART','INTERIORART')
                and t1.title_language != t2.title_language
                and t1.title_language = %d
                and not exists (select 1 from notes n where t1.note_id = n.note_id))
                as t3, titles t4
                where t3.title_id = t4.title_id
                order by t4.title_title
                limit 1000""" % language_id
        standardReport(query, report_id)
