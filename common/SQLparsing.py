from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2026   Al von Ruff, Ahasuerus, Bill Longley, Dirk Stoecker and Lokal_Profil
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1268 $
#     Date: $Date: 2026-02-25 16:55:22 -0500 (Wed, 25 Feb 2026) $

##############################################################################
#  Imports (Recommended to be top-level in Python3
##############################################################################
import sys
if sys.version_info.major == 3:
        PYTHONVER = "python3"
elif sys.version_info.major == 2:
        PYTHONVER = "python2"

import os
import string
import traceback
from isfdb import *
from time import *
from datetime import datetime

db_python2  = 2
db_python3  = 3

if PYTHONVER == "python2":
        db_connector = db_python2
        import MySQLdb
elif PYTHONVER == "python3":
        db_connector = db_python3
        import mysql.connector

##############################################################################

if PYTHONVER == "python2":
        def _Date_or_None(s):
                return s

        def _IsfdbConvSetup():
                import MySQLdb.converters
                IsfdbConv = MySQLdb.converters.conversions
                IsfdbConv[10] = _Date_or_None
                return IsfdbConv

############################################################################
# This class abstracts the APIs for the two different MYSQL connectors
# used with the ISFDB (MySQLdb for python2 and mysql.connector for python3.
# This provides a single unified API for all database operations. The
# connector can by changed by altering the db_connector variable below.
############################################################################

class MYSQL_CONNECTOR():
        def __init__(self):
                if db_connector == db_python3:
                        self.cursor = db.cursor(buffered=True)
                        self.formats = []
                        self.fmt_idx = 0
                else:
                        self.cursor = 0

        def DB_FORMAT(self, input):
                self.formats = input
                self.fmt_idx = 0

        def DB_QUERY(self, query):
                if db_connector == db_python2:
                        db.query(query)
                        self.result = db.store_result()
                elif db_connector == db_python3:
                        self.cursor.execute(query)
                else:
                        print("Unsupported Connector")

        def DB_FETCHONE(self):
                if db_connector == db_python2:
                        record = self.result.fetch_row()
                elif db_connector == db_python3:
                        record = self.cursor.fetchone()
                        # MySQLdb fetch_row delivered the record within 2 tuples
                        #if record != None:
                        if record is not None:
                                record = tuple([tuple(record)])
                else:
                        print("Unsupported Connector")
                        record = 0
                #print("<li>DEBUG: FETCHONE:", record)
                return record

        def DB_FETCHMANY(self):
                if db_connector == db_python2:
                        record = self.result.fetch_row()
                elif db_connector == db_python3:
                        record = self.cursor.fetchmany()
                        # MySQLdb fetchmany delivered the record within 1 tuple
                        #if record != None:
                        if record is not None:
                                record = tuple(record)
                else:
                        print("Unsupported Connector")
                        record = 0
                #print("DEBUG: FETCHMANY:", record)
                return record

        def DB_NUMROWS(self):
                if db_connector == db_python2:
                        return self.result.num_rows()
                elif db_connector == db_python3:
                        return self.cursor.rowcount
                else:
                        print("Unsupported Connector")
                        return 0

        def DB_INSERT_ID(self):
                if db_connector == db_python2:
                        return db.insert_id()
                elif db_connector == db_python3:
                        return self.cursor.lastrowid
                else:
                        print("Unsupported Connector")
                        return 0

        def DB_ESCAPE_STRING(self, target):
                if db_connector == db_python2:
                        return db.escape_string(target)
                elif db_connector == db_python3:
                        return db.converter.escape(target)
                else:
                        print("Unsupported Connector")
                        return 0

if GLOBAL_DEBUG:
        SQLlogging = 1
else:
        SQLlogging = 0

def SQLlog(arg):
        if SQLlogging > 0:
                SESSION.SQLlog.append(arg)

def SQLoutputLog():
        if len(SESSION.SQLlog) > 0:
                for item in SESSION.SQLlog:
                        print("<li>", item)

def SQLflushOutputLog():
        if len(SESSION.SQLlog) > 0:
                for item in SESSION.SQLlog:
                        print("<li>", item)
        SESSION.SQLlog = []

CNX_AUTHORS_STAR = "author_id, author_canonical, author_legalname, author_birthplace, DATE_FORMAT(author_birthdate, '%Y-%m-%d'), DATE_FORMAT(author_deathdate, '%Y-%m-%d'), note_id, author_wikipedia, author_views, author_imdb, author_marque, author_image, author_annualviews, author_lastname, author_language, author_note"
CNX_ADOT_AUTHORS_STAR = "a.author_id, a.author_canonical, a.author_legalname, a.author_birthplace, DATE_FORMAT(a.author_birthdate, '%Y-%m-%d'), DATE_FORMAT(a.author_deathdate, '%Y-%m-%d'), a.note_id, a.author_wikipedia, a.author_views, a.author_imdb, a.author_marque, a.author_image, a.author_annualviews, a.author_lastname, a.author_language, a.author_note"
CNX_ADV_AUTHORS_STAR = "authors.author_id, authors.author_canonical, authors.author_legalname, authors.author_birthplace, DATE_FORMAT(authors.author_birthdate, '%Y-%m-%d'), DATE_FORMAT(authors.author_deathdate, '%Y-%m-%d'), authors.note_id, authors.author_wikipedia, authors.author_views, authors.author_imdb, authors.author_marque, authors.author_image, authors.author_annualviews, authors.author_lastname, authors.author_language, authors.author_note"

CNX_TITLES_STAR = "title_id, title_title, title_translator, title_synopsis, note_id, series_id, title_seriesnum, DATE_FORMAT(title_copyright, '%Y-%m-%d'), title_storylen, title_ttype, title_wikipedia, title_views, title_parent, title_rating, title_annualviews, title_ctl, title_language, title_seriesnum_2, title_non_genre, title_graphic, title_nvz, title_jvn, title_content"
CNX_TDOT_TITLES_STAR = "t.title_id, t.title_title, t.title_translator, t.title_synopsis, t.note_id, t.series_id, t.title_seriesnum, DATE_FORMAT(t.title_copyright, '%Y-%m-%d'), t.title_storylen, t.title_ttype, t.title_wikipedia, t.title_views, t.title_parent, t.title_rating, t.title_annualviews, t.title_ctl, t.title_language, t.title_seriesnum_2, t.title_non_genre, t.title_graphic, t.title_nvz, t.title_jvn, t.title_content"
CNX_ADV_TITLES_STAR = "titles.title_id, titles.title_title, titles.title_translator, titles.title_synopsis, titles.note_id, titles.series_id, titles.title_seriesnum, DATE_FORMAT(titles.title_copyright, '%Y-%m-%d'), titles.title_storylen, titles.title_ttype, titles.title_wikipedia, titles.title_views, titles.title_parent, titles.title_rating, titles.title_annualviews, titles.title_ctl, titles.title_language, titles.title_seriesnum_2, titles.title_non_genre, titles.title_graphic, titles.title_nvz, titles.title_jvn, titles.title_content"

CNX_PUBS_STAR = "pub_id, pub_title, pub_tag, DATE_FORMAT(pub_year, '%Y-%m-%d'), publisher_id, pub_pages, pub_ptype, pub_ctype, pub_isbn, pub_frontimage, pub_price, note_id, pub_series_id, pub_series_num, pub_catalog"
CNX_PDOT_PUBS_STAR = "p.pub_id, p.pub_title, p.pub_tag, DATE_FORMAT(p.pub_year, '%Y-%m-%d'), p.publisher_id, p.pub_pages, p.pub_ptype, p.pub_ctype, p.pub_isbn, p.pub_frontimage, p.pub_price, p.note_id, p.pub_series_id, p.pub_series_num, p.pub_catalog"
CNX_ADV_PUBS_STAR = "pubs.pub_id, pubs.pub_title, pubs.pub_tag, DATE_FORMAT(pubs.pub_year, '%Y-%m-%d'), pubs.publisher_id, pubs.pub_pages, pubs.pub_ptype, pubs.pub_ctype, pubs.pub_isbn, pubs.pub_frontimage, pubs.pub_price, pubs.note_id, pubs.pub_series_id, pubs.pub_series_num, pubs.pub_catalog"

CNX_AWARDS_STAR = "award_id, award_title, award_author, DATE_FORMAT(award_year, '%Y-%m-%d'), award_ttype, award_atype, award_level, award_movie, award_type_id, award_cat_id, award_note_id"
CNX_ADV_AWARDS_STAR = "awards.award_id, awards.award_title, awards.award_author, DATE_FORMAT(awards.award_year, '%Y-%m-%d'), awards.award_ttype, awards.award_atype, awards.award_level, awards.award_movie, awards.award_type_id, awards.award_cat_id, awards.award_note_id"

def _StandardQuery(query):
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = []
        record = CNX.DB_FETCHMANY()
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def _BinaryQuery(query):
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS():
                return 1
        else:
                return 0

def _OneRow(query):
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                return record[0]
        else:
                return None

def _OneField(query):
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0][0])
                record = CNX.DB_FETCHMANY()
        return results

def _SingleNumericField(query):
        numeric_value = 0
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS():
                record = CNX.DB_FETCHONE()
                numeric_value = record[0][0]
        return numeric_value

def SQLUpdateQueries():
        SQLlog("SQLUpdateQueries")
        query = "select metadata_counter from metadata"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        retvalue = record[0][0]
        newvalue = retvalue + 1
        update = "update metadata set metadata_counter='%d'" % (newvalue)
        CNX.DB_QUERY(update)
        return retvalue

def SQLMajorVersion():
        SQLlog("SQLMajorVersion")
        query = "select version()"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        full_version = record[0][0]
        try:
                major_version = int(full_version.split('.')[0])
        except:
                major_version = 0
        return major_version

def SQLLoadAllLanguages():
        SQLlog("SQLLoadAllLanguages")
        languages = _StandardQuery("select lang_name from languages order by lang_id")
        return_list = ['None']
        for language in languages:
                return_list.append(language[0])
        return tuple(return_list)

def SQLLoadFullLanguages():
        SQLlog("SQLLoadFullLanguages")
        return _StandardQuery("select * from languages order by lang_name")

def SQLgetDatabaseStatus():
        SQLlog("SQLgetDatabaseStatus")
        query = "select metadata_dbstatus from metadata"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        version = record[0][0]
        return version

def SQLgetEditingStatus():
        SQLlog("SQLgetEditingStatus")
        query = "select metadata_editstatus from metadata"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        version = record[0][0]
        return version

def SQLgetSchemaVersion():
        SQLlog("SQLgetSchemaVersion")
        query = "select metadata_schemaversion from metadata"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        version = record[0][0]
        return version

def SQLMultipleAuthors(name):
        SQLlog("SQLMultipleAuthors, name=%s" % name)
        name = name.replace('_','\_')
        # If the author name ends with a ')', then drop everything to the right of the LAST " ("
        if name.endswith(')') and ' (' in name:
                location = name.rfind(' (')
                name_root = name[:location]
        else:
                name_root = name
        name_root = name_root.strip()
        CNX = MYSQL_CONNECTOR()
        query = """select 1 from authors
                where author_canonical != '%s'
                and (author_canonical = '%s'
                or author_canonical like '%s (%%)'
                )""" % (CNX.DB_ESCAPE_STRING(name),
                        CNX.DB_ESCAPE_STRING(name_root),
                        CNX.DB_ESCAPE_STRING(name_root))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                return record[0]
        else:
                return 0

def SQLgetAuthorData(author):
        SQLlog("SQLgetAuthorData, author=%s" % author)
        CNX = MYSQL_CONNECTOR()
        query = "select %s from authors where author_canonical='%s'" % (CNX_AUTHORS_STAR, CNX.DB_ESCAPE_STRING(author))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                return record[0]
        else:
                return 0

def SQLloadAuthorData(author_id):
        SQLlog("SQLloadAuthorData, author_id=%s" % author_id)
        query = "select %s from authors where author_id=%d" % (CNX_AUTHORS_STAR, int(author_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                return record[0]
        else:
                return 0

def SQLauthorIsPseudo(au_id):
        SQLlog("SQLauthorIsPseudo, au_id=%s" % au_id)
        query = "select pseudo_id from pseudonyms where pseudonym=%d" % int(au_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                return 1
        else:
                return 0

def SQLauthorHasPseudo(au_id):
        SQLlog("SQLauthorHasPseudo, au_id=%s" % au_id)
        query = "select pseudo_id from pseudonyms where author_id=%d" % int(au_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                return 1
        else:
                return 0

def SQLgetBriefActualFromPseudo(au_id):
        SQLlog("SQLgetBriefActualFromPseudo, au_id=%s" % au_id)
        query = """select a.author_id, a.author_canonical
                   from authors a, pseudonyms p
                   where p.pseudonym = %d
                   and p.author_id = a.author_id
                   order by a.author_lastname, a.author_canonical""" % int(au_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        authors = []
        while record:
                authors.append(list(record[0]))
                record = CNX.DB_FETCHMANY()
        return authors

# Whitelist of valid (table, id_field, name_field) combinations for
# SQLGetDisambiguatedRecords. Identifiers are never safe to escape;
# they must be validated against known-good values instead.
_DISAMBIGUATED_RECORD_TYPES = {
        'publishers': ('publisher_id', 'publisher_name'),
        'pub_series': ('pub_series_id', 'pub_series_name'),
        'series':     ('series_id',     'series_title'),
}

def SQLGetDisambiguatedRecords(record_id, name, table, id_field, name_field):
        SQLlog("SQLGetDisambiguatedRecords, record_id=%s, name=%s, table=%s, id_field=%s, name_field=%s" % (record_id, name, table, id_field, name_field))
        # Validate identifiers against the whitelist. All current call sites
        # pass string literals, so a mismatch indicates a programming error.
        valid = _DISAMBIGUATED_RECORD_TYPES.get(table)
        if not valid or (id_field, name_field) != valid:
                SQLlog("SQLGetDisambiguatedRecords: rejected unknown identifiers: table=%s id_field=%s name_field=%s" % (table, id_field, name_field))
                return []
        # For new records not in the database, use record ID 0
        if not record_id:
                record_id = 0
        # If the record name ends with a ')', then drop everything to the right of the LAST " ("
        if name.endswith(')') and ' (' in name:
                location = name.rfind(' (')
                name = name[:location]
        name = name.strip()
        CNX = MYSQL_CONNECTOR()
        exact_name = CNX.DB_ESCAPE_STRING(name.replace('_','\_'))
        query = """select * from %s
                   where (%s = '%s' or %s like '%s (%%)')
                   and %s != %d
                   order by %s
                   """ % (table, name_field, exact_name, name_field, exact_name, id_field, int(record_id), name_field)
        return _StandardQuery(query)

def SQLgetActualFromPseudo(au_id):
        SQLlog("SQLgetActualFromPseudo, au_id=%s" % au_id)
        query = "select authors.author_canonical from authors,pseudonyms where pseudonyms.pseudonym=%d and pseudonyms.author_id=authors.author_id;" % int(au_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        authors = []
        while record:
                authors.append(list(record[0]))
                record = CNX.DB_FETCHMANY()
        return authors

def SQLgetBriefPseudoFromActual(au_id):
        SQLlog("SQLgetBriefPseudoFromActual, au_id=%s" % au_id)
        query = """select a.author_id, a.author_canonical
                   from authors a, pseudonyms p
                   where p.author_id = %d
                   and p.pseudonym = a.author_id
                   order by a.author_lastname""" % int(au_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        authors = []
        while record:
                authors.append(list(record[0]))
                record = CNX.DB_FETCHMANY()
        return authors

def SQLgetPseudoFromActual(au_id):
        SQLlog("SQLgetPseudoFromActual, au_id=%s" % au_id)
        query = "select authors.author_canonical from authors,pseudonyms where pseudonyms.author_id=%d and pseudonyms.pseudonym=authors.author_id;" % int(au_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        authors = []
        while record:
                authors.append(list(record[0]))
                record = CNX.DB_FETCHMANY()
        return authors

def SQLupdateAuthorViews(author_id):
        SQLlog("SQLupdateAuthorViews, author_id=%s" % author_id)
        # INSERT ... ON DUPLICATE KEY UPDATE is atomic: no SELECT needed and
        # no risk of lost increments under concurrent requests. Requires
        # author_id to be a PRIMARY KEY or UNIQUE KEY in author_views.
        query = """insert into author_views (author_id, views, annual_views)
                   values(%d, 1, 1)
                   on duplicate key update
                   views = views + 1, annual_views = annual_views + 1""" % int(author_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)

def SQLupdateTitleViews(title_id):
        SQLlog("SQLupdateTitleViews, title_id=%s" % title_id)
        # INSERT ... ON DUPLICATE KEY UPDATE is atomic: no SELECT needed and
        # no risk of lost increments under concurrent requests. Requires
        # title_id to be a PRIMARY KEY or UNIQUE KEY in title_views.
        query = """insert into title_views (title_id, views, annual_views)
                   values(%d, 1, 1)
                   on duplicate key update
                   views = views + 1, annual_views = annual_views + 1""" % int(title_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)

def SQLgetSeriesData(author_id):
        SQLlog("SQLgetSeriesData, author_id=%s" % author_id)
        query = """select distinct series.* from series, titles, canonical_author
                where titles.series_id=series.series_id
                and titles.title_id=canonical_author.title_id
                and canonical_author.author_id=%d
                order by series.series_title""" % int(author_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        records = []
        while record:
                records.append(list(record[0]))
                record = CNX.DB_FETCHMANY()
        return records

def SQLget1Series(seriesrec):
        SQLlog("SQLget1Series, seriesrec=%s" % seriesrec)
        query = "select * from series where series_id='%d'" % (int(seriesrec))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                return record[0]
        else:
                return 0

def SQLgetNotes(note_id):
        SQLlog("SQLgetNotes, note_id=%s" % note_id)
        if not note_id:
                return ''
        query = "select * from notes where note_id='%d'" % int(note_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        return record[0][1]

def SQLloadAllAuthorTitles(aurec, page_type, languages_all, languages):
        SQLlog("SQLloadAllAuthorTitles, aurec=%s, page_type=%s, languages_all=%s, languages=%s" % (aurec, page_type, languages_all, languages))
        if page_type == 'Summary':
                query = """select %s, IF(t.title_seriesnum IS NULL, 1, 0) AS isnull
                from titles t, canonical_author ca
                where (ca.author_id=%d and ca.title_id=t.title_id and ca.ca_status=1)
                and t.title_parent=0
                order by isnull, t.title_seriesnum, t.title_seriesnum_2,
                IF(t.title_copyright = '0000-00-00', 1, 0),
                t.title_copyright, t.title_title""" % (CNX_TDOT_TITLES_STAR, aurec)
        elif page_type == 'Chronological':
                query = """select %s from titles t, canonical_author ca
                where (ca.author_id=%d and ca.title_id=t.title_id and ca.ca_status=1)
                and t.title_parent=0
                order by IF(t.title_copyright = '0000-00-00', 1, 0),
                t.title_copyright, t.title_title""" % (CNX_TDOT_TITLES_STAR, aurec)
        else:
                query = """select %s from titles t, canonical_author ca
                where (ca.author_id=%d and ca.title_id=t.title_id and ca.ca_status=1)
                and t.title_parent=0
                order by t.title_title, t.title_copyright""" % (CNX_TDOT_TITLES_STAR, aurec)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        records = []
        # For alphabetical and award biblios, also build a comma-separated list to use in a SQL IN clause later
        in_clause = ''
        while record:
                records.append(list(record[0]))
                if page_type in ('Alphabetical', 'Award'):
                        title_id = str(record[0][0])
                        if not in_clause:
                                in_clause = title_id
                        else:
                                in_clause += ",%s" % title_id
                record = CNX.DB_FETCHMANY()
        # For alphabetical and award biblios, also retrieve the VTs of canonical titles
        if page_type in ('Alphabetical', 'Award') and in_clause:
                query = "select %s from titles t where title_parent in (%s)" % (CNX_TDOT_TITLES_STAR, in_clause)
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        # Only select this VT if it meets the current user's language pereferences
                        if ((languages_all == 'All') or
                            not record[0][TITLE_LANGUAGE] or
                            ((languages_all == 'Selected') and
                             (record[0][TITLE_LANGUAGE] in languages))):
                                records.append(list(record[0]))
                        record = CNX.DB_FETCHMANY()
                # Re-sort the list by title
                records.sort(key=lambda tup: (tup[TITLE_TITLE].lower(), tup[TITLE_YEAR]))
        return records


def SQLloadAnyTitles(aurec):
        SQLlog("SQLloadAnyTitles, aurec=%s" % (aurec))
        query = "select %s from titles,canonical_author where (canonical_author.author_id = %d and canonical_author.title_id = titles.title_id and canonical_author.ca_status = 1);" % (CNX_ADV_TITLES_STAR, aurec)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        records = []
        while record:
                records.append(list(record[0]))
                record = CNX.DB_FETCHMANY()
        return records

def SQLloadTitlesXBT(recno):
        SQLlog("SQLloadTitlesXBT, recno=%s" % (recno))
        query = "select %s from titles t,pub_content where pub_content.pub_id='%d' and pub_content.title_id = t.title_id order by t.title_title;" % (CNX_TDOT_TITLES_STAR, int(recno))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        records = []
        while record:
                records.append(list(record[0]))
                record = CNX.DB_FETCHMANY()
        return records

def SQLloadIntervieweeXBA(author):
        SQLlog("SQLloadIntervieweeXBA, author=%s" % (author))
        CNX = MYSQL_CONNECTOR()
        query = "select %s from titles where title_ttype='INTERVIEW' and title_subject_author like '%%%s%%';" % (CNX_TITLES_STAR, CNX.DB_ESCAPE_STRING(author))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        records = []
        while record:
                records.append(record[0])
                record = CNX.DB_FETCHMANY()
        return records

def SQLloadTitleFromAward(award_id):
        SQLlog("SQLloadTitleFromAward, award_id=%s" % (award_id))
        query = "select titles.* from titles,title_awards where titles.title_id=title_awards.title_id and title_awards.award_id='%d';" % int(award_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        return record

def SQLloadAwardsXBA(author, titles, pseudonyms):
        SQLlog("SQLloadAwardsXBA, author=%s, titles=%s, pseudonyms=%s" % (author, titles, pseudonyms))
        # Load all awards for one author
        #
        # Step 1: Create a list of author/pseudonym names for this person
        names = []
        names.append(author)
        for pseudonym in pseudonyms:
                names.append(pseudonym[1])
        # Step 2: Build an SQL IN clause for titles
        in_clause = ''
        for title in titles:
                title_id = str(title[TITLE_PUBID])
                if not in_clause:
                        in_clause = title_id
                else:
                        in_clause += ",%s" % title_id
        # Step 3: Create a query to retrieve:
        # untitled awards whose author name matches the canonical author name or an alternate name
        # AND all awards associated with this author's titles and VTs
        first = 1
        query = """(select a.award_id, a.award_title as title, a.award_author, DATE_FORMAT(a.award_year, '%Y-%m-%d') as year,
                   a.award_ttype, a.award_atype, a.award_level as level, a.award_movie,
                   a.award_type_id, a.award_cat_id, a.award_note_id
                   from awards a
                   where not exists(select 1 from title_awards ta where ta.award_id = a.award_id)
                   and ("""
        for name in names:
                CNX = MYSQL_CONNECTOR()
                value = CNX.DB_ESCAPE_STRING(name)
                if not first:
                        query += "or "
                query += "(a.award_author = '%s') or " % value
                query += "(a.award_author like '%s+%%') or " % value
                query += "(a.award_author like '%%+%s') or " % value
                query += "(a.award_author like '%%+%s+%%') " % value
                first = 0
        query += ')'
        if in_clause:
                query += """) UNION (select a.award_id, t.title_title as title, a.award_author,
                              DATE_FORMAT(a.award_year, '%%Y-%%m-%%d') as year, a.award_ttype, a.award_atype, a.award_level as level,
                              a.award_movie, a.award_type_id, a.award_cat_id, a.award_note_id
                              from awards as a, title_awards as ta, titles t
                              where t.title_id in (%s)
                              and a.award_id = ta.award_id
                              and ta.title_id = t.title_id)""" % in_clause
        query += " order by year, title, ABS(level)"
        return _StandardQuery(query)

def SQLloadAwardsForYearType(award_type_id, year):
        SQLlog("SQLloadAwardsForYearType, award_type_id=%s, year=%s" % (award_type_id, year))
        query = """(select a.award_id, a.award_title as title, a.award_author, DATE_FORMAT(a.award_year, '%%Y-%%m-%%d'),
                   a.award_ttype, a.award_atype, a.award_level as level, a.award_movie,
                   a.award_type_id, a.award_cat_id, a.award_note_id, c.award_cat_name as cat_name,
                   c.award_cat_order as cat_order
                   from awards a, award_cats c
                   where a.award_type_id = %d
                   and YEAR(a.award_year) = %d
                   and a.award_cat_id = c.award_cat_id
                   and not exists(select 1 from title_awards ta where ta.award_id = a.award_id)
                )
                UNION
                   (select a.award_id, t.title_title as title, a.award_author, DATE_FORMAT(a.award_year, '%%Y-%%m-%%d'),
                   a.award_ttype, a.award_atype, a.award_level as level, a.award_movie,
                   a.award_type_id, a.award_cat_id, a.award_note_id, c.award_cat_name as cat_name,
                   c.award_cat_order as cat_order
                   from awards a, award_cats c, title_awards ta, titles t
                   where a.award_type_id = %d
                   and YEAR(a.award_year) = %d
                   and a.award_cat_id = c.award_cat_id
                   and ta.award_id = a.award_id
                   and t.title_id = ta.title_id
                )
                   order by ISNULL(cat_order), cat_order, cat_name, ABS(level), title
                   """ % (int(award_type_id), int(year), int(award_type_id), int(year))
        return _StandardQuery(query)

def SQLloadAwardsForCat(award_cat_id, win_nom):
        SQLlog("SQLloadAwardsForCat, award_cat_id=%s, win_nom=%s" % (award_cat_id, win_nom))
        query = """(select a.award_id, a.award_title as title, a.award_author, DATE_FORMAT(a.award_year, '%%Y-%%m-%%d') as year,
                   a.award_ttype, a.award_atype, a.award_level as level, a.award_movie,
                   a.award_type_id, a.award_cat_id, a.award_note_id, c.award_cat_name
                   from awards a, award_cats c
                   where a.award_cat_id = %d
                   and a.award_cat_id = c.award_cat_id
                   and not exists(select 1 from title_awards ta where ta.award_id = a.award_id) """ % int(award_cat_id)
        # If the requested award list is limited to wins
        if not win_nom:
                query += "and a.award_level = '1'"
        query += """
                )
                UNION
                    (select a.award_id, t.title_title as title, a.award_author, DATE_FORMAT(a.award_year, '%%Y-%%m-%%d') as year,
                    a.award_ttype, a.award_atype, a.award_level as level, a.award_movie,
                    a.award_type_id, a.award_cat_id, a.award_note_id, c.award_cat_name
                    from awards a, award_cats c, title_awards ta, titles t
                    where a.award_cat_id = %d
                    and a.award_cat_id = c.award_cat_id
                    and ta.award_id = a.award_id
                    and t.title_id = ta.title_id """ % int(award_cat_id)
        # If the requested award list is limited to wins
        if not win_nom:
                query += "and a.award_level = '1'"
        query += ') order by year, ABS(level), title'

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        records = {}
        while record:
                year = record[0][AWARD_YEAR]
                if year not in records:
                        records[year] = []
                records[year].append(record[0])
                record = CNX.DB_FETCHMANY()
        return records

def SQLloadAwardsForCatYear(award_cat_id, award_year):
        SQLlog("SQLloadAwardsForCatYear, award_cat_id=%s, award_year=%d" % (award_cat_id, award_year))
        query = """(select a.award_id, a.award_title as title, a.award_author, DATE_FORMAT(a.award_year, '%%Y-%%m-%%d') as year,
                a.award_ttype, a.award_atype, a.award_level as level, a.award_movie,
                a.award_type_id, a.award_cat_id, a.award_note_id
                from awards a, award_cats c
                where a.award_cat_id = %d
                and a.award_cat_id = c.award_cat_id
                and not exists(select 1 from title_awards ta where ta.award_id = a.award_id)
                and YEAR(a.award_year) = %d""" % (int(award_cat_id), int(award_year))
        query += """)
                UNION
                (select a.award_id, t.title_title as title, a.award_author, a.award_year,
                a.award_ttype, a.award_atype, a.award_level as level, a.award_movie,
                a.award_type_id, a.award_cat_id, a.award_note_id
                from awards a, award_cats c, title_awards ta, titles t
                where a.award_cat_id = %d
                and a.award_cat_id = c.award_cat_id
                and YEAR(a.award_year) = %d
                and ta.award_id = a.award_id
                and t.title_id = ta.title_id""" % (int(award_cat_id), int(award_year))
        query += ') order by ABS(level), title'
        return _StandardQuery(query)

def SQLloadTitlesXBS(series):
        SQLlog("SQLloadTitlesXBS, series=%s" % (series))
        query = "select * from titles where series_id = '%d';" % (series)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        records = []
        while record:
                records.append(record[0])
                record = CNX.DB_FETCHMANY()
        return records


# Return a list of publications to be published in a specific month/year
def SQLGetForthcoming(month, year, day, all):
        SQLlog("SQLGetForthcoming, month=%s, year=%s, day=%s, all=%s" % (month, year, day, all))
        if month == 12:
                end    = "%d-01-00" % (int(year)+1)
        else:
                end    = "%s-%02d-00" % (year, month+1)
        target = "%s-%02d-%02d" % (year, month, int(day))
        CNX = MYSQL_CONNECTOR()
        if all:
                query = "select %s from pubs where pub_year>='%s' and pub_year<'%s' order by pub_year,pub_title" % (CNX_PUBS_STAR, CNX.DB_ESCAPE_STRING(target), CNX.DB_ESCAPE_STRING(end))
        else:
                query = "select %s from pubs where pub_year>='%s' and pub_year<'%s' and pub_frontimage is not NULL order by pub_year,pub_title" % (CNX_PUBS_STAR, CNX.DB_ESCAPE_STRING(target), CNX.DB_ESCAPE_STRING(end))
        return _StandardQuery(query)

def SQLGetFrontPagePubs(front_page):
        SQLlog("SQLGetFrontPagePubs, front_page=%s" % (front_page))
        common_subquery1 = """where p.pub_year between CURDATE() AND DATE_SUB(CURDATE(),INTERVAL -30 DAY)
                        and p.pub_ctype not in ('MAGAZINE', 'FANZINE')
                        and p.pub_frontimage != ''
                        and p.pub_frontimage is not NULL
                        and p.pub_year not like '%-00'"""
        common_subquery2 = """and not exists
                        (select 1 from notes n
                        where n.note_id = p.note_id
                        and n.note_note like '%{{WatchPrePub|cover%')
                        order by p.pub_year, p.pub_title"""

        if front_page:
                query = """select %s from pubs p, front_page_pubs fp
                        %s
                        and p.pub_id = fp.pub_id
                        %s
                        limit %d""" % (CNX_PDOT_PUBS_STAR, common_subquery1, common_subquery2, SESSION.front_page_pubs)
        else:
                query = """select distinct %s from pubs p, authors a, pub_authors pa
                        %s
                        and p.pub_id = pa.pub_id
                        and a.author_id = pa.author_id
                        and a.author_marque = 1
                        %s""" % (CNX_PDOT_PUBS_STAR, common_subquery1, common_subquery2)
        return _StandardQuery(query)

def SQLGetNextMonthPubs(additional_pubs = 0):
        SQLlog("SQLGetNextMonthPubs, front_page=%s" % (additional_pubs))
        from library import ISFDBCompare2Dates
        future_pubs = SQLGetFrontPagePubs(0)

        referral_titles = []
        selected_authors = {}
        selected_pubs = {}
        position = 1
        for pub in future_pubs:
                pub_id = pub[PUB_PUBID]

                # Retrieve the book's referral title ID
                title_id = SQLgetTitleReferral(pub_id, pub[PUB_CTYPE])
                if not title_id:
                        continue
                # If we have already selected a publication for this referral title, don't select another one
                if title_id in referral_titles:
                        continue
                # Add this referral title ID to the list of selected referral title IDs
                referral_titles.append(title_id)
                referral_title_date = SQLloadTitle(title_id)[TITLE_YEAR]

                authors = SQLPubBriefAuthorRecords(pub_id)
                if not authors:
                    continue
                # Get the first author of this pub from the author list sorted by author ID
                author_id = sorted(authors, key=lambda x: x[0])[0]
                # Do not attempt substitution for "buffer" pubs
                if (author_id not in selected_authors) or (position > SESSION.front_page_pubs):
                        selected_authors[author_id] = (referral_title_date, position)
                        selected_pubs[position] = pub
                else:
                        previous_pub_data = selected_authors[author_id]
                        previous_title_date = previous_pub_data[0]
                        # If the date of this pub's referral title is before the date
                        # of the referral title of the previously selected pub for this
                        # author, do not update the dictionary of selected pubs
                        if ISFDBCompare2Dates(referral_title_date, previous_title_date):
                                continue
                        old_position = previous_pub_data[1]
                        selected_authors[author_id] = (referral_title_date, old_position)
                        selected_pubs[old_position] = pub
                        continue

                selected_pubs[position] = pub
                position += 1
                if position > (SESSION.front_page_pubs + additional_pubs):
                        break

        pubs_list = []
        for position in sorted(selected_pubs.keys()):
                pubs_list.append(selected_pubs[position])

        # Re-sort by publication date and publication title
        return sorted(pubs_list, key=lambda x: (x[PUB_YEAR], x[PUB_TITLE]))

def SQLGetPubByTag(tag):
        SQLlog("SQLGetPubByTag, tag=%s" % (tag))
        CNX = MYSQL_CONNECTOR()
        query = "select * from pubs where pub_tag = '%s'" % (CNX.DB_ESCAPE_STRING(tag))
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                pub = CNX.DB_FETCHONE()
                return pub[0]
        else:
                return 0

def SQLGetPubById(id):
        SQLlog("SQLGetPubById, id=%s" % (id))
        query = "select %s from pubs where pub_id = '%d'" % (CNX_PUBS_STAR, int(id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                pub = CNX.DB_FETCHONE()
                return pub[0]
        else:
                return 0

def SQLGetCoverAuthorsForPubs(pub_list):
        SQLlog("SQLGetCoverAuthorsForPubs, pub_list=%s" % (pub_list))
        pub_string = ", ".join(pub_list)
        CNX = MYSQL_CONNECTOR()
        query = """select pc.pub_id, a.author_id, a.author_canonical
                from titles t, pub_content pc, canonical_author ca, authors a
                where pc.pub_id in (%s)
                and t.title_ttype = 'COVERART'
                and t.title_ttype = 'COVERART'
                and pc.title_id = t.title_id
                and ca.title_id = pc.title_id
                and ca.author_id = a.author_id""" % CNX.DB_ESCAPE_STRING(pub_string)
        CNX.DB_QUERY(query)
        row = CNX.DB_FETCHMANY()
        results = {}
        while row:
                pub_id = row[0][0]
                author_id = row[0][1]
                author_name = row[0][2]
                if pub_id not in results:
                        results[pub_id] = []
                results[pub_id].append((author_id, author_name))
                row = CNX.DB_FETCHMANY()
        return results

def SQLGetCoverPubsByTitle(titlerec):
        SQLlog("SQLGetCoverPubsByTitle, titlerec=%s" % (titlerec))
        query = "select title_id from titles where title_id=%d and title_ttype='COVERART' \
                UNION select title_id from titles where title_parent=%d \
                and title_ttype='COVERART'" % (titlerec, titlerec)
        results = _RetrievePubsQuery(query)
        return results

def SQLGetPubsByTitle(titlerec):
        SQLlog("SQLGetPubsByTitle, titlerec=%s" % (titlerec))
        query = "select title_id from titles where title_id=%d or title_parent=%d" % (titlerec, titlerec)
        results = _RetrievePubsQuery(query)
        return results

def SQLGetPubsByTitleNoParent(titlerec):
        SQLlog("SQLGetPubsByTitleNoParent, titlerec=%s" % (titlerec))
        query = "select title_id from titles where title_id=%d" % (titlerec)
        results = _RetrievePubsQuery(query)
        return results

def SQLGetPubsByTitleNoTranslations(titlerec):
        SQLlog("SQLGetPubsByTitleNoTranslations, titlerec=%s" % (titlerec))
        query = """select %d
                   UNION
                   select variant.title_id
                   from titles variant, titles parent
                   where variant.title_parent=%d
                   and parent.title_id = %d
                   and variant.title_language = parent.title_language
                """ % (int(titlerec), int(titlerec), int(titlerec))
        results = _RetrievePubsQuery(query)
        return results

def SQLGetPubsForChildTitles(titlerec):
        SQLlog("SQLGetPubsForChildTitles, titlerec=%s" % (titlerec))
        query = "select title_id from titles where title_parent=%d" % (titlerec)
        results = _RetrievePubsQuery(query)
        return results

def _RetrievePubsQuery(query):
        # Internal function, NOT TO BE CALLED DIRECTLY
        # Currently called by SQLGetPubsByTitle, SQLGetPubsByTitleNoParent,
        # SQLGetCoverPubsByTitle and SQLGetPubsForChildTitles
        #
        ############################################################
        # STEP 1 - Get the list of titles
        ############################################################
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        titles = []
        while title:
                titles.append(title[0])
                title = CNX.DB_FETCHMANY()
        # If no titles were found, which may happen if the title has been deleted, return the empty list
        if not titles:
                return titles

        ############################################################
        # STEP 2 - Form a query using those titles
        ############################################################
        query = "select distinct %s from pubs p,pub_content where pub_content.pub_id=p.pub_id " % (CNX_PDOT_PUBS_STAR)
        counter = 0
        for title in titles:
                if counter:
                        query += "or pub_content.title_id=%d " % title
                else:
                        query += "and (pub_content.title_id=%d " % title
                counter += 1
        # Display 0000 years last
        query += ") order by IF(p.pub_year = '0000-00-00', 1, 0), p.pub_year, p.pub_title, p.pub_id"

        results = []
        CNX.DB_QUERY(query)
        pub = CNX.DB_FETCHMANY()
        while pub:
                results.append(list(pub[0]))
                pub = CNX.DB_FETCHMANY()
        return results


def SQLGetPubsByPublisherYear(publisher_id, year):
        SQLlog("SQLGetPubsByPublisherYear, publisher_id=%s, year=%s" % (publisher_id, year))
        query = """select * from pubs
                   where publisher_id=%d and YEAR(pub_year)=%d
                   order by pub_year""" % (int(publisher_id), int(year))
        results = []
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        pub = CNX.DB_FETCHMANY()
        while pub:
                results.append(list(pub[0]))
                pub = CNX.DB_FETCHMANY()
        return results


def SQLGetPubsByAuthor(aurec):
        SQLlog("SQLGetPubsByAuthor, aurec=%s" % (aurec))
        query = "select pubs.* from pubs,pub_authors where pub_authors.author_id=%d and pubs.pub_id=pub_authors.pub_id;" % aurec
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        pub = CNX.DB_FETCHMANY()
        results = []
        while pub:
                results.append(pub[0])
                pub = CNX.DB_FETCHMANY()
        return results

def SQLGetPubContentByAuthor(aurec):
        SQLlog("SQLGetPubContentByAuthor, aurec=%s" % (aurec))
        query = "select pub_content.* from pub_content,canonical_author where canonical_author.author_id=%d and pub_content.title_id=canonical_author.title_id;" % aurec
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        pub = CNX.DB_FETCHMANY()
        results = []
        while pub:
                results.append(pub[0])
                pub = CNX.DB_FETCHMANY()
        return results

def SQLloadTitle(titlerec):
        SQLlog("SQLloadTitle, titlerec=%s" % (titlerec))
        query = "select %s from titles where title_id = %d" % (CNX_TITLES_STAR, int(titlerec))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHONE()
        if title:
                return list(title[0])
        else:
                return []

def SQLloadTitleList(title_ids):
        SQLlog("SQLloadTitleList, title_ids=%s" % (title_ids))
        from library import list_to_in_clause
        if not title_ids:
                return {}
        in_clause = list_to_in_clause(title_ids)
        query = "select %s from titles where title_id in (%s)" % (CNX_TITLES_STAR, in_clause)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = {}
        while record:
                title_id = record[0][0]
                results[title_id] = record[0]
                record = CNX.DB_FETCHMANY()
        return results

def SQLGetPublisher(pubrec):
        SQLlog("SQLGetPublisher, pubrec=%s" % (pubrec))
        if not pubrec:
                return []
        query = "select * from publishers where publisher_id = '%d'" % (int(pubrec))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        publisher = CNX.DB_FETCHONE()
        if publisher:
                return list(publisher[0])
        else:
                return []

def SQLGetPublisherList(publisher_list):
        SQLlog("SQLGetPublisherList, publisher_list=%s" % (publisher_list))
        from library import list_to_in_clause
        if not publisher_list:
                return {}
        publisher_string = list_to_in_clause(publisher_list)
        query = "select * from publishers where publisher_id in (%s)" % publisher_string
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = {}
        while record:
                publisher_id = record[0][0]
                publisher_name = record[0][1]
                results[publisher_id] = publisher_name
                record = CNX.DB_FETCHMANY()
        return results

def SQLGetPublisherDirectory():
        SQLlog("SQLGetPublisherDirectory")
        query = """select publisher_name from publishers
                UNION
                select trans_publisher_name from trans_publisher"""
        return _ASCIIDirectory(query)

def _ASCIIDirectory(query):
        import unicodedata
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        records_map = {}
        while record:
                two_latin1_letters = record[0][0]
                first_latin_letter = two_latin1_letters[0]
                if PYTHONVER == 'python2':
                        first_unicode_letter = first_latin_letter.decode('iso-8859-1')
                else:
                        first_unicode_letter = first_latin_letter
                first_normalized_letter = unicodedata.normalize('NFKD', first_unicode_letter).encode('ascii', 'ignore').decode('ascii', 'strict').lower()
                second_normalized_letter = ' '
                if len(two_latin1_letters) > 1:
                        second_latin_letter = two_latin1_letters[1]
                        if PYTHONVER == 'python2':
                                second_unicode_letter = second_latin_letter.decode('iso-8859-1')
                        else:
                                second_unicode_letter = second_latin_letter
                        second_normalized_letter = unicodedata.normalize('NFKD', second_unicode_letter).encode('ascii', 'ignore').decode('ascii', 'strict').lower()
                two_normalized_letters = first_normalized_letter + second_normalized_letter
                records_map[two_normalized_letters] = ''
                record = CNX.DB_FETCHMANY()
        return records_map

def SQLGetMagazineDirectory():
        SQLlog("SQLGetMagazineDirectory")
        query = """select s.series_title
        from series s, titles t
        where t.series_id = s.series_id
        and t.title_ttype = 'EDITOR'
        UNION
        select t.title_title
        from titles t
        where t.title_ttype='EDITOR'
        UNION
        select tt.trans_title_title
        from trans_titles tt, titles t
        where t.title_ttype = 'EDITOR'
        and t.title_id = tt.title_id"""
        return _ASCIIDirectory(query)

def SQLGetAuthorDirectory():
        SQLlog("SQLGetAuthorDirectory")
        query = """select lower(substring(author_lastname,1,2)) as xx, count(*)
        from authors group by xx"""
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        records_map = {}
        while record:
                records_map[record[0][0]] = record[0][1]
                record = CNX.DB_FETCHMANY()
        return records_map

def SQLGetPubSeries(pub_series_id):
        SQLlog("SQLGetPubSeries, pub_series_id=%s" % (pub_series_id))
        query = "select * from pub_series where pub_series_id = %d" % int(pub_series_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        pub_series = CNX.DB_FETCHONE()
        if pub_series:
                return list(pub_series[0])
        else:
                return []

def SQLGetPubSeriesByName(pub_series_name):
        SQLlog("SQLGetPubSeriesByName, pub_series_name=%s" % (pub_series_name))
        CNX = MYSQL_CONNECTOR()
        query = "select * from pub_series where pub_series_name = '%s'" % CNX.DB_ESCAPE_STRING(pub_series_name)
        CNX.DB_QUERY(query)
        pub_series = CNX.DB_FETCHONE()
        if pub_series:
                return list(pub_series[0])
        else:
                return []

def SQLGetPubSeriesList(pub_series_list):
        SQLlog("SQLGetPubSeriesList, pub_series_list=%s" % (pub_series_list))
        from library import list_to_in_clause
        if not pub_series_list:
                return {}
        pub_series_string = list_to_in_clause(pub_series_list)
        query = "select * from pub_series where pub_series_id in (%s)" % pub_series_string
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = {}
        while record:
                pub_series_id = record[0][0]
                pub_series_name = record[0][1]
                results[pub_series_id] = pub_series_name
                record = CNX.DB_FETCHMANY()
        return results

def SQLLoadPubSeries(pub_series_ids):
        SQLlog("SQLLoadPubSeries, pub_series_ids=%s" % (pub_series_ids))
        CNX = MYSQL_CONNECTOR()
        query = "select * from pub_series where pub_series_id in (%s) order by pub_series_name" % (CNX.DB_ESCAPE_STRING(pub_series_ids))
        CNX.DB_QUERY(query)
        pub_series = CNX.DB_FETCHMANY()
        results = []
        while pub_series:
                results.append(pub_series[0])
                pub_series = CNX.DB_FETCHMANY()
        return results

def SQLGetPubSeriesPubs(pub_series_id, display_order):
        SQLlog("SQLGetPubSeriesPubs, pub_series_id=%s, display_order=%s" % (pub_series_id, display_order))
        # Supported display_order values:
        #  0: Show earliest year first
        #  1: Show last year first
        #  2: Sort by series number
        results = []
        query = "select * from pubs where pub_series_id=%d order by " % int(pub_series_id)
        if display_order == 0:
                query += "IF(pub_year = '0000-00-00', 1, 0), pub_year, cast(pub_series_num as UNSIGNED), pub_series_num"
        elif display_order == 1:
                query += "IF(pub_year = '0000-00-00', 1, 0), pub_year desc, cast(pub_series_num as UNSIGNED), pub_series_num"
        elif display_order == 2:
                query += "IF(pub_series_num IS NULL, 1, 0), cast(pub_series_num as UNSIGNED), pub_series_num, pub_year"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        pub = CNX.DB_FETCHMANY()
        while pub:
                results.append(pub[0])
                pub = CNX.DB_FETCHMANY()
        return results

def SQLCountPubsNotInPubSeries(publisher_id):
        SQLlog("SQLCountPubsNotInPubSeries, publisher_id=%s" % (publisher_id))
        query = """select count(*) from pubs where publisher_id=%d
                   and pub_series_id is null""" % int(publisher_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        pubs = CNX.DB_FETCHONE()
        return pubs[0][0]

def SQLGetPubsNotInSeries(publisher_id, sort_order):
        SQLlog("SQLGetPubsNotInSeries, publisher_id=%s" % (publisher_id))
        results = []
        query = """select * from pubs where publisher_id = %d
                   and pub_series_id is NULL
                   order by IF(pub_year = '0000-00-00', 1, 0), pub_year %s""" % (int(publisher_id), sort_order)
        return _StandardQuery(query)

def SQLCountPubsForPublisher(publisher_id):
        SQLlog("SQLCountPubsForPublisher, publisher_id=%s" % (publisher_id))
        query = """select count(*) from pubs where publisher_id=%d""" % int(publisher_id)
        return _SingleNumericField(query)

def SQLCountPubsForPubSeries(pub_series_id):
        SQLlog("SQLCountPubsForPubSeries, pub_series_id=%s" % (pub_series_id))
        query = """select count(*) from pubs where pub_series_id=%d""" % int(pub_series_id)
        return _SingleNumericField(query)

##################################################################
# FIND ROUTINES
##################################################################

def SQLFindAuthors(target, mode = 'contains'):
        SQLlog("SQLFindAuthors, target=%s, mode=%s" % (target, mode))
        if PYTHONVER == 'python2':
                from string import maketrans
        CNX = MYSQL_CONNECTOR()
        if mode == 'exact':
                query = "select distinct %s from authors where author_canonical = '%s'""" % (CNX_AUTHORS_STAR, CNX.DB_ESCAPE_STRING(target))
        elif mode == 'contains':
                target = CNX.DB_ESCAPE_STRING('%'+target+'%')
                query = """select distinct %s from authors a
                             where a.author_canonical like '%s'
                           union select distinct a.* from authors a, trans_authors at
                                where at.trans_author_name like '%s' and at.author_id = a.author_id
                           order by author_canonical""" % (CNX_ADOT_AUTHORS_STAR, target, target)
        elif mode == 'approximate':
                punctuation = """'",.()"""
                target = target.translate(maketrans("",""), punctuation)
                prefix = ''
                for character in punctuation:
                        prefix += 'REPLACE('
                suffix = ''
                for character in punctuation:
                        if character == "'":
                                suffix += ""","%s",'')""" % character
                        else:
                                suffix += ",'%s','')" % character
                name1 = '%s%s%s' % (prefix, 'a.author_canonical', suffix)
                name2 = '%s%s%s' % (prefix, 'at.trans_author_name', suffix)
                target = CNX.DB_ESCAPE_STRING('%'+target+'%')
                query = """select distinct %s from authors a
                           where %s like '%s'
                           union select distinct %s from authors a, trans_authors at
                           where %s like '%s' and at.author_id = a.author_id
                           order by author_canonical""" % (CNX_ADOT_AUTHORS_STAR, name1, target, CNX_ADOT_AUTHORS_STAR, name2, target)
        return _StandardQuery(query)

def SQLFindTitles(target):
        SQLlog("SQLFindTitles, target=%s" % (target))
        boolean_word_string = _StringToBooleanWordList(target)
        CNX = MYSQL_CONNECTOR()
        target = CNX.DB_ESCAPE_STRING('%'+target+'%')
        query = """select distinct t.* from titles t
                        where t.title_title like '%s'
                        and match(t.title_title) against('%s' IN BOOLEAN MODE)
                union select distinct t.* from titles t, trans_titles tt
                        where tt.trans_title_title like '%s'
                        and tt.title_id = t.title_id
                        and match(tt.trans_title_title) against('%s' IN BOOLEAN MODE)
                order by title_title""" % (target, boolean_word_string, target, boolean_word_string)
        return _StandardQuery(query)

def _StringToBooleanWordList(value):
        if PYTHONVER == 'python2':
                table = string.maketrans("""',.;:?!/[]"~*<>-+()""", '                   ')
        else:
                table = str.maketrans("""',.;:?!/[]"~*<>-+()""", '                   ')
        word_string = value.translate(table)
        word_list = word_string.split()
        return '+%s' % ' +'.join(word_list)

def SQLFindExactTitles(target):
        SQLlog("SQLFindExactTitles, target=%s" % (target))
        CNX = MYSQL_CONNECTOR()
        query = "select * from titles where title_title = '%s' order by title_title" % CNX.DB_ESCAPE_STRING(target)
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        results = []
        while title:
                results.append(title[0])
                title = CNX.DB_FETCHMANY()
        return results

def SQLFindFictionTitles(target):
        SQLlog("SQLFindFictionTitles, target=%s" % (target))
        boolean_word_string = _StringToBooleanWordList(target)
        CNX = MYSQL_CONNECTOR()
        target = CNX.DB_ESCAPE_STRING('%'+target+'%')
        query = """select distinct t.* from titles t
                        where t.title_title like '%s'
                        and match(t.title_title) against('%s' IN BOOLEAN MODE)
                        and t.title_ttype in ('ANTHOLOGY','COLLECTION','EDITOR','NOVEL','OMNIBUS','POEM','SERIAL','SHORTFICTION','CHAPBOOK')
                union
                        select distinct t.* from titles t, trans_titles tt
                        where tt.trans_title_title like '%s'
                        and tt.title_id = t.title_id
                        and match(tt.trans_title_title) against('%s' IN BOOLEAN MODE)
                        and t.title_ttype in ('ANTHOLOGY','COLLECTION','EDITOR','NOVEL','OMNIBUS','POEM','SERIAL','SHORTFICTION','CHAPBOOK')
                order by title_title""" % (target, boolean_word_string, target, boolean_word_string)
        return _StandardQuery(query)

def SQLFindYear(target):
        SQLlog("SQLFindYear, target=%s" % (target))
        results = []
        try:
                year = int(target)
        except:
                return results

        query = "select * from titles where YEAR(title_copyright) = '%d' order by title_ttype,title_title" % (year)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        while title:
                results.append(title[0])
                title = CNX.DB_FETCHMANY()
        return results

def SQLFindPublisher(target, mode = 'contains'):
        SQLlog("SQLFindPublisher, target=%s, mode=%s" % (target, mode))
        CNX = MYSQL_CONNECTOR()
        if mode == 'exact':
                query = "select distinct * from publishers where publisher_name = '%s'" % CNX.DB_ESCAPE_STRING(target)
        else:
                target = CNX.DB_ESCAPE_STRING('%'+target+'%')
                query = """select distinct p.* from publishers p
                           where p.publisher_name like '%s'
                           union
                           select distinct p.* from publishers p, trans_publisher tp
                           where tp.trans_publisher_name like '%s' and
                           tp.publisher_id = p.publisher_id
                           order by publisher_name""" % (target, target)
        return _StandardQuery(query)

def SQLGetPublisherYears(publisher_id):
        SQLlog("SQLGetPublisherYears, publisher_id=%s" % (publisher_id))
        results = []
        query = "select distinct YEAR(pub_year) from pubs where publisher_id='%d' order by pub_year" % int(publisher_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        year = CNX.DB_FETCHMANY()
        while year:
                results.append(year[0][0])
                year = CNX.DB_FETCHMANY()
        return results

def SQLFindPubSeries(target, mode = 'contains'):
        SQLlog("SQLFindPubSeries, target=%s, mode=%s" % (target, mode))
        CNX = MYSQL_CONNECTOR()
        if mode == 'exact':
                query = "select * from pub_series where pub_series_name = '%s'" % CNX.DB_ESCAPE_STRING(target)
        else:
                target = CNX.DB_ESCAPE_STRING('%'+target+'%')
                query = """select distinct ps.* from pub_series ps
                           where ps.pub_series_name like '%s'
                           union
                           select distinct ps.* from pub_series ps, trans_pub_series tps
                           where tps.trans_pub_series_name like '%s'
                           and tps.pub_series_id = ps.pub_series_id
                           order by pub_series_name""" % (target, target)
        return _StandardQuery(query)

def SQLFindMagazine(arg, directory = 0):
        SQLlog("SQLFindMagazine, arg=%s, directory=%s" % (arg, directory))
        CNX = MYSQL_CONNECTOR()
        if directory:
                target = CNX.DB_ESCAPE_STRING(arg)
        else:
                target = CNX.DB_ESCAPE_STRING('%'+arg+'%')
        # First retrieve matching series names
        query = """select distinct s.series_id, s.series_title, s.series_parent
                from series s, titles t
                where t.series_id = s.series_id
                and t.title_ttype = 'EDITOR'
                and s.series_title like '%s'
                UNION
                select distinct s.series_id, s.series_title, s.series_parent
                from series s, titles t, trans_series ts
                where t.series_id = s.series_id
                and t.title_ttype = 'EDITOR'
                and s.series_id = ts.series_id
                and ts.trans_series_name like '%s'
                """ % (target, target)
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        series = {}
        series_by_id = {}
        while record:
                series_id = record[0][0]
                series_title = record[0][1]
                series_parent = record[0][2]
                if series_title not in series:
                        series[series_title] = {}
                series[series_title][series_id] = (series_parent, series_title)
                series_by_id[series_id] = series_title
                record = CNX.DB_FETCHMANY()

        # Next find magazine titles that match the search string, but whose
        # series titles don't match it
        query="""select distinct t.title_title, s.series_id, s.series_title,
                s.series_parent from series s, titles t
                where t.title_title like '%s'
                and t.title_ttype = 'EDITOR'
                and t.series_id=s.series_id
                and s.series_title not like '%s'
                UNION
                select distinct t.title_title, s.series_id, s.series_title,
                s.series_parent from series s, titles t, trans_titles tt
                where tt.trans_title_title like '%s'
                and tt.title_id=t.title_id
                and t.title_ttype = 'EDITOR'
                and t.series_id=s.series_id
                and s.series_title not like '%s'
                """ % (target, target, target, target)
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        while record:
                title = record[0][0]
                separator = title.rfind(" - ")
                if separator != -1:
                        title = title[:separator]
                series_id = record[0][1]
                series_title = record[0][2]
                series_parent = record[0][3]
                if series_id not in series_by_id:
                        if title not in series:
                                series[title] = {}
                        series[title][series_id] = (series_parent, series_title)
                        series_by_id[series_id] = series_title
                record = CNX.DB_FETCHMANY()

        count = 0
        for title in series:
                for series_id in series[title]:
                        count += 1
        return (series, count)

def SQLFindSeries(target, mode = 'contains'):
        SQLlog("SQLFindSeries, target=%s, mode=%s" % (target, mode))
        CNX = MYSQL_CONNECTOR()
        if mode == 'exact':
                query = "select distinct * from series where series_title = '%s'" % CNX.DB_ESCAPE_STRING(target)
        else:
                target = CNX.DB_ESCAPE_STRING('%'+target+'%')
                query = """select distinct s.* from series s
                           where s.series_title like '%s'
                           union
                           select distinct s.* from series s, trans_series ts
                           where ts.trans_series_name like '%s'
                           and ts.series_id = s.series_id
                           order by series_title""" % (target, target)
        return _StandardQuery(query)

def SQLFindSeriesChildren(id):
        SQLlog("SQLFindSeriesChildren, id=%s" % (id))
        query = """select series_id,IF(series.series_parent_position IS NULL or series.series_parent_position='', 1, 0)
                   AS isnull from series
                   where series_parent=%d
                   ORDER BY isnull, series_parent_position, series_title""" % id
        return _OneField(query)

def SQLgetSeriesName(id):
        SQLlog("SQLgetSeriesName, id=%s" % (id))
        query = "select series_title from series where series_id=%d" % int(id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        series = CNX.DB_FETCHONE()
        return series[0][0]

def SQLFindSeriesId(target):
        SQLlog("SQLFindSeriesId, target=%s" % (target))
        CNX = MYSQL_CONNECTOR()
        target = CNX.DB_ESCAPE_STRING(target)
        query = "select series_id from series where series_title='%s'" % (target)
        CNX.DB_QUERY(query)
        id = CNX.DB_FETCHONE()
        if CNX.DB_NUMROWS() > 0:
                return id[0][0]
        else:
                return ''

def SQLFindSeriesName(target):
        SQLlog("SQLFindSeriesName, target=%s" % (target))
        query = "select series_title from series where series_id=%d" % int(target)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        id = CNX.DB_FETCHONE()
        if CNX.DB_NUMROWS() > 0:
                return id[0][0]
        else:
                return ''

def SQLFindSeriesParent(target):
        SQLlog("SQLFindSeriesParent, target=%s" % (target))
        query = "select series_parent from series where series_id='%d'" % int(target)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                id = CNX.DB_FETCHONE()
                return id[0][0]
        else:
                return ''

def SQLFindSeriesParentPosition(target):
        SQLlog("SQLFindSeriesParentPosition, target=%s" % (target))
        query = "select series_parent_position from series where series_id='%d'" % int(target)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                id = CNX.DB_FETCHONE()
                return id[0][0]
        else:
                return ''

def SQLFindSeriesTitles(target):
        SQLlog("SQLFindSeriesTitles, target=%s" % (target))
        results = []
        CNX = MYSQL_CONNECTOR()
        target = CNX.DB_ESCAPE_STRING(target)
        query = "select titles.*,IF(titles.title_seriesnum IS NULL, 1, 0) AS isnull from titles,series where series.series_id=titles.series_id and series.series_title='%s' order by isnull,titles.title_seriesnum,titles.title_seriesnum_2,titles.title_copyright" % (target)
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        while title:
                results.append(title[0])
                title = CNX.DB_FETCHMANY()
        return results

def SQLLoadSeriesFromList(series_ids):
        SQLlog("SQLLoadSeriesFromList, series_ids=%s" % (series_ids))
        from library import list_to_in_clause
        if not series_ids:
                return {}
        series_id_list = list_to_in_clause(series_ids)
        query = "select * from series where series_id in (%s)" % series_id_list
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = {}
        while record:
                series_id = record[0][0]
                results[series_id] = record[0]
                record = CNX.DB_FETCHMANY()
        return results

def SQLLoadSeriesListTitles(series_list):
        SQLlog("SQLLoadSeriesListTitles, series_list=%s" % (series_list))
        CNX = MYSQL_CONNECTOR()
        series_list = CNX.DB_ESCAPE_STRING(series_list)
        query = """select %s,IF(t.title_seriesnum IS NULL, 1, 0) AS isnull
                from titles t where series_id in (%s) order by series_id,
                isnull, t.title_seriesnum, t.title_seriesnum_2,
                t.title_copyright""" % (CNX_TDOT_TITLES_STAR, series_list)
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        results_dict = {}
        results_list = []
        while title:
                results_list.append(title[0])
                series_id = title[0][TITLE_SERIES]
                if series_id not in results_dict:
                        results_dict[series_id] = []
                results_dict[series_id].append(title[0])
                title = CNX.DB_FETCHMANY()
        return (results_dict, results_list)

def SQLFindPubsByIsbn(targets, excluded_pub_id = 0):
        SQLlog("SQLFindPubsByIsbn, targets=%s, excluded_pub_id=%s" % (targets, excluded_pub_id))
        if not excluded_pub_id:
                excluded_pub_id = 0
        results = []
        CNX = MYSQL_CONNECTOR()
        if len(targets) > 0:
                first = 1
                query = "select * from pubs where (pub_isbn like '"
                for target in targets:
                        if not first:
                                query += "' or pub_isbn like '"
                        query += CNX.DB_ESCAPE_STRING(target)
                        first = 0
                query += "')"
                if excluded_pub_id:
                        query += " and pub_id != %d" % int(excluded_pub_id)
                query += " order by pub_isbn limit 300"
                CNX.DB_QUERY(query)
                pub = CNX.DB_FETCHMANY()
                while pub:
                        results.append(pub[0])
                        pub = CNX.DB_FETCHMANY()
        return results

def SQLFindPubsByCatalogId(value):
        SQLlog("SQLFindPubsByCatalogId, value=%s" % (value))
        CNX = MYSQL_CONNECTOR()
        query = "select * from pubs where pub_catalog ='%s'" % CNX.DB_ESCAPE_STRING(value)
        return _StandardQuery(query)

def SQLFindPubSeriesForPublisher(publisher_id):
        SQLlog("SQLFindPubSeriesForPublisher, publisher_id=%s" % (publisher_id))
        results = []
        query = "select distinct pub_series_id from pubs where publisher_id = '%d' and pub_series_id IS NOT NULL" % int(publisher_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        pub = CNX.DB_FETCHMANY()
        while pub:
                results.append(pub[0])
                pub = CNX.DB_FETCHMANY()
        return results

def SQLgetPublisherName(id):
        SQLlog("SQLgetPublisherName, id=%s" % (id))
        query = "select publisher_name from publishers where publisher_id=%d" % (int(id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                publisher = CNX.DB_FETCHONE()
                return publisher[0][0]
        else:
                return ''

def SQLReviewedAuthors(title_id):
        SQLlog("SQLReviewedAuthors, title_id=%s" % (title_id))
        query = """select authors.author_id, authors.author_canonical
                   from authors, canonical_author
                   where canonical_author.title_id = %d
                   and canonical_author.author_id = authors.author_id
                   and canonical_author.ca_status = 3""" % int(title_id)
        return _StandardQuery(query)

def SQLIntervieweeAuthors(title_id, author_id = 0):
        SQLlog("SQLIntervieweeAuthors, title_id=%s, author_id=%s" % (title_id, author_id))
        query = """select authors.author_id, authors.author_canonical
                   from authors, canonical_author
                   where canonical_author.title_id = %d
                   and canonical_author.author_id <> %d
                   and canonical_author.author_id = authors.author_id
                   and canonical_author.ca_status = 2""" % (int(title_id), int(author_id))
        return _StandardQuery(query)

def SQLTitleBriefAuthorRecords(title_id):
        SQLlog("SQLTitleBriefAuthorRecords, title_id=%s" % (title_id))
        query = """select a.author_id, a.author_canonical
                 from authors a, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.ca_status = 1
                 and ca.title_id=%d
                 order by a.author_lastname, a.author_canonical""" % int(title_id)
        return _StandardQuery(query)

def SQLTitleListBriefAuthorRecords(title_list, author_id = 0):
        SQLlog("SQLTitleListBriefAuthorRecords, title_list=%s, author_id=%s" % (title_list, author_id))
        if not title_list:
                return {}
        # Load author IDs and author names for a list of titles;
        # if a non-0 author ID was explicitly passed in, then skip it
        CNX = MYSQL_CONNECTOR()
        query = """select ca.title_id, a.author_id, a.author_canonical
                from authors a, canonical_author ca
                where a.author_id = ca.author_id
                and a.author_id <> %d
                and ca.ca_status = 1
                and ca.title_id in (%s)
                order by a.author_lastname, a.author_canonical""" % (int(author_id), CNX.DB_ESCAPE_STRING(title_list))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = {}
        while record:
                title_id = record[0][0]
                if title_id not in results:
                        results[title_id] = []
                results[title_id].append((record[0][1], record[0][2]))
                record = CNX.DB_FETCHMANY()
        return results

def SQLTitleAuthors(title_id):
        SQLlog("SQLTitleAuthors, title_id=%s" % (title_id))
        query = """select a.author_canonical
                from authors a, canonical_author ca
                where a.author_id = ca.author_id
                and ca.ca_status=1
                and ca.title_id=%d
                order by a.author_lastname, a.author_canonical""" % int(title_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        results = []
        while title:
                results.append(title[0][0])
                title = CNX.DB_FETCHMANY()
        return results

def SQLInterviewBriefAuthorRecords(title_id):
        SQLlog("SQLInterviewBriefAuthorRecords, title_id=%s" % (title_id))
        query = """select a.author_id, a.author_canonical
                from authors a, canonical_author ca
                where a.author_id=ca.author_id
                and ca.ca_status=2
                and ca.title_id=%d
                order by a.author_lastname, a.author_canonical""" % int(title_id)
        return _StandardQuery(query)

def SQLInterviewAuthors(title_id):
        SQLlog("SQLInterviewAuthors, title_id=%s" % (title_id))
        query = """select a.author_canonical
                from authors a, canonical_author ca
                where a.author_id = ca.author_id
                and ca.ca_status=2
                and ca.title_id=%d
                order by a.author_lastname, a.author_canonical""" % int(title_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        results = []
        while title:
                results.append(title[0][0])
                title = CNX.DB_FETCHMANY()
        return results

def SQLReviewBriefAuthorRecords(title_id):
        SQLlog("SQLReviewBriefAuthorRecords, title_id=%s" % (title_id))
        query = """select a.author_id, a.author_canonical
                from authors a, canonical_author ca
                where a.author_id=ca.author_id
                and ca.ca_status=3
                and ca.title_id=%d
                order by a.author_lastname, a.author_canonical""" % int(title_id)
        return _StandardQuery(query)

def SQLReviewAuthors(title_id):
        SQLlog("SQLReviewAuthors, title_id=%s" % (title_id))
        query = """select a.author_canonical
                from authors a, canonical_author ca
                where a.author_id=ca.author_id
                and ca.ca_status=3
                and ca.title_id=%d
                order by a.author_lastname, a.author_canonical""" % int(title_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        results = []
        while title:
                results.append(title[0][0])
                title = CNX.DB_FETCHMANY()
        return results

def SQLPubBriefAuthorRecords(pub_id):
        SQLlog("SQLPubBriefAuthorRecords, pub_id=%s" % (pub_id))
        query = """select a.author_id, a.author_canonical
                from authors a, pub_authors pa
                where a.author_id = pa.author_id
                and pa.pub_id = %d
                order by a.author_lastname, a.author_canonical""" % int(pub_id)
        return _StandardQuery(query)

def SQLPubListBriefAuthorRecords(pub_list):
        SQLlog("SQLPubListBriefAuthorRecords, pub_list=%s" % (pub_list))
        from library import list_to_in_clause
        pub_string = list_to_in_clause(pub_list)
        query = """select pa.pub_id, a.author_id, a.author_canonical, a.author_lastname
                from authors a, pub_authors pa
                where a.author_id = pa.author_id
                and pa.pub_id in (%s)
                order by a.author_lastname, a.author_canonical""" % pub_string
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = {}
        while record:
                pub_id = record[0][0]
                author_id = record[0][1]
                canonical_name = record[0][2]
                last_name = record[0][3]
                if pub_id not in results:
                        results[pub_id] = []
                results[pub_id].append((author_id, canonical_name, last_name))
                record = CNX.DB_FETCHMANY()
        return results

def SQLPubAuthors(pub_id):
        SQLlog("SQLPubAuthors, pub_id=%s" % (pub_id))
        query = """select a.author_canonical
                from authors a, pub_authors pa
                where a.author_id=pa.author_id
                and pa.pub_id=%d
                order by a.author_lastname, a.author_canonical""" % int(pub_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        results = []
        while title:
                results.append(title[0][0])
                title = CNX.DB_FETCHMANY()
        return results

def SQLTitleAwards(title_id):
        SQLlog("SQLTitleAwards, title_id=%s" % (title_id))
        ############################################################
        # Get variant titles including canonical one
        # as a string suitable for SQL's IN (...) clause
        ############################################################
        if not title_id:
                return ([])
        query = "select DISTINCT title_id from titles where title_id=%d or title_parent=%d" % (int(title_id), int(title_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        if not title:
                return([])
        title_set = ""
        counter = 0
        while title:
                if counter:
                        title_set += ", "
                title_set += str(title[0][0])
                title = CNX.DB_FETCHMANY()
                counter += 1

        query = """select distinct awards.*
                from title_awards, awards
                where title_awards.title_id in (%s)
                and title_awards.award_id=awards.award_id
                order by awards.award_year, awards.award_level""" % (CNX.DB_ESCAPE_STRING(title_set))
        return _StandardQuery(query)

def SQLloadAwards(award_id):
        SQLlog("SQLloadAwards, award_id=%s" % (award_id))
        CNX = MYSQL_CONNECTOR()
        query = "select %s from awards where award_id='%d'" % (CNX_AWARDS_STAR, award_id)
        CNX.DB_QUERY(query)
        award = CNX.DB_FETCHMANY()
        results = []
        while award:
                results.append(award[0])
                award = CNX.DB_FETCHMANY()
        return results

def SQLloadEmails(author_id):
        SQLlog("SQLloadEmails, author_id=%s" % (author_id))
        query = "select email_address from emails where author_id='%d'" % (author_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        email = CNX.DB_FETCHMANY()
        results = []
        while email:
                results.append(email[0][0])
                email = CNX.DB_FETCHMANY()
        return results

def SQLgetTitleReferral(pub_id, pub_ctype, include_editors=0):
        SQLlog("SQLgetTitleReferral, pub_id=%s, pub_ctype=%s, include_editors=%s" % (pub_id, pub_ctype, include_editors))
        query = "select c.title_id,t.title_ttype from pub_content c, titles t where c.pub_id=%d and c.title_id=t.title_id" % int(pub_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() < 1:
                return 0
        title_data = CNX.DB_FETCHMANY()
        while title_data:
                title_id = title_data[0][0]
                title_ttype = title_data[0][1]
                if title_ttype == pub_ctype:
                        return title_id
                # If "include_editors" was set to 1 and this pub is a magazine or fanzine, then return the first found EDITOR title
                elif (include_editors == 1) and ((pub_ctype == 'MAGAZINE') or (pub_ctype == 'FANZINE')) and (title_ttype == 'EDITOR'):
                        return title_id
                title_data = CNX.DB_FETCHMANY()
        return 0

def SQLgetTitleReferralList(pubs, include_editors=0):
        SQLlog("SQLgetTitleReferralList, pubs=%s, include_editors=%s" % (pubs, include_editors))
        from library import list_to_in_clause
        pub_ids = []
        pub_types = {}
        for pub in pubs:
                pub_id = pub[PUB_PUBID]
                pub_ids.append(pub_id)
                pub_type = pub[PUB_CTYPE]
                pub_types[pub_id] = pub_type

        referral_titles = {}
        if not pub_ids:
                return referral_titles
        pub_ids_string = list_to_in_clause(pub_ids)
        CNX = MYSQL_CONNECTOR()
        query = """select pc.pub_id, %s
                   from pub_content pc, titles t
                   where pc.pub_id in (%s)
                   and pc.title_id = t.title_id""" % (CNX_TDOT_TITLES_STAR, pub_ids_string)
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() < 1:
                return 0
        combined_data = CNX.DB_FETCHMANY()
        while combined_data:
                pub_id = combined_data[0][0]
                title_data = list(combined_data[0][1:])
                title_ttype = title_data[TITLE_TTYPE]
                if pub_id not in referral_titles:
                        pub_type = pub_types[pub_id]
                        if title_ttype == pub_type:
                                referral_titles[pub_id] = title_data
                        # If "include_editors" was set to 1 and this pub is
                        # a magazine or fanzine, then return the first found EDITOR title
                        elif (include_editors == 1) and (pub_type in ('MAGAZINE', 'FANZINE')) and (title_ttype == 'EDITOR'):
                                referral_titles[pub_id] = title_data
                combined_data = CNX.DB_FETCHMANY()
        return referral_titles

def SQLloadTransLegalNames(author_id):
        SQLlog("SQLloadTransLegalNames, author_id=%s" % (author_id))
        query = "select trans_legal_name from trans_legal_names where author_id='%d'" % int(author_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        row = CNX.DB_FETCHMANY()
        results = []
        while row:
                results.append(row[0][0])
                row = CNX.DB_FETCHMANY()
        return results

def SQLloadWebpages(author_id):
        SQLlog("SQLloadWebpages, author_id=%s" % (author_id))
        query = "select url from webpages where author_id='%d'" % (author_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        webpage = CNX.DB_FETCHMANY()
        results = []
        while webpage:
                results.append(webpage[0][0])
                webpage = CNX.DB_FETCHMANY()
        return results

def SQLloadPublisherWebpages(publisher_id):
        SQLlog("SQLloadPublisherWebpages, publisher_id=%s" % (publisher_id))
        query = "select url from webpages where publisher_id='%d'" % (publisher_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        webpage = CNX.DB_FETCHMANY()
        results = []
        while webpage:
                results.append(webpage[0][0])
                webpage = CNX.DB_FETCHMANY()
        return results

def SQLloadTransPubSeriesNames(pub_series_id):
        SQLlog("SQLloadTransPubSeriesNames, pub_series_id=%s" % (pub_series_id))
        query = "select trans_pub_series_name from trans_pub_series where pub_series_id=%d" % int(pub_series_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        row = CNX.DB_FETCHMANY()
        results = []
        while row:
                results.append(row[0][0])
                row = CNX.DB_FETCHMANY()
        return results

def SQLLoadTransPubSeriesList(pub_series_ids):
        SQLlog("SQLLoadTransPubSeriesList, pub_series_ids=%s" % (pub_series_ids))
        from library import list_to_in_clause
        if not pub_series_ids:
                return {}
        pub_series_ids_string = list_to_in_clause(pub_series_ids)
        query = """select p.pub_series_id, tps.trans_pub_series_name
                  from pub_series p, trans_pub_series tps
                  where p.pub_series_id = tps.pub_series_id
                  and p.pub_series_id in (%s)""" % pub_series_ids_string
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = {}
        record = CNX.DB_FETCHMANY()
        while record:
                  pub_series_id = record[0][0]
                  trans_pub_series_name = record[0][1]
                  if pub_series_id not in results:
                          results[pub_series_id] = []
                  results[pub_series_id].append(trans_pub_series_name)
                  record = CNX.DB_FETCHMANY()
        return results

def SQLloadTransPublisherNames(publisher_id):
        SQLlog("SQLloadTransPublisherNames, publisher_id=%s" % (publisher_id))
        query = "select trans_publisher_name from trans_publisher where publisher_id=%d" % int(publisher_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        row = CNX.DB_FETCHMANY()
        results = []
        while row:
                results.append(row[0][0])
                row = CNX.DB_FETCHMANY()
        return results

def SQLLoadTransPublisherList(publisher_ids):
        SQLlog("SQLLoadTransPublisherList, publisher_ids=%s" % (publisher_ids))
        from library import list_to_in_clause
        if not publisher_ids:
                return {}
        publisher_ids_string = list_to_in_clause(publisher_ids)
        query = """select p.publisher_id, tp.trans_publisher_name
                  from publishers p, trans_publisher tp
                  where p.publisher_id = tp.publisher_id
                  and p.publisher_id in (%s)""" % publisher_ids_string
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = {}
        record = CNX.DB_FETCHMANY()
        while record:
                  publisher_id = record[0][0]
                  trans_publisher_name = record[0][1]
                  if publisher_id not in results:
                          results[publisher_id] = []
                  results[publisher_id].append(trans_publisher_name)
                  record = CNX.DB_FETCHMANY()
        return results

def SQLloadTransSeriesNames(series_id):
        SQLlog("SQLloadTransSeriesNames, series_id=%s" % (series_id))
        query = "select trans_series_name from trans_series where series_id=%d" % int(series_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        row = CNX.DB_FETCHMANY()
        results = []
        while row:
                results.append(row[0][0])
                row = CNX.DB_FETCHMANY()
        return results

def SQLloadTransTitles(title_id):
        SQLlog("SQLloadTransTitles, title_id=%s" % (title_id))
        query = "select trans_title_title from trans_titles where title_id=%d" % int(title_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        row = CNX.DB_FETCHMANY()
        results = []
        while row:
                results.append(row[0][0])
                row = CNX.DB_FETCHMANY()
        return results

def SQLLoadTransTitlesList(title_ids):
        SQLlog("SQLLoadTransTitlesList, title_ids=%s" % (title_ids))
        from library import list_to_in_clause
        if not title_ids:
                return {}
        title_ids_string = list_to_in_clause(title_ids)
        query = """select t.title_id, tt.trans_title_title
                  from titles t, trans_titles tt
                  where t.title_id = tt.title_id
                  and t.title_id in (%s)""" % title_ids_string
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = {}
        record = CNX.DB_FETCHMANY()
        while record:
                  title_id = record[0][0]
                  trans_title_title = record[0][1]
                  if title_id not in results:
                          results[title_id] = []
                  results[title_id].append(trans_title_title)
                  record = CNX.DB_FETCHMANY()
        return results

def SQLloadTransAuthorNames(author_id):
        SQLlog("SQLloadTransAuthorNames, author_id=%s" % (author_id))
        query = "select trans_author_name from trans_authors where author_id=%d" % int(author_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        row = CNX.DB_FETCHMANY()
        results = []
        while row:
                results.append(row[0][0])
                row = CNX.DB_FETCHMANY()
        return results

def SQLLoadTransAuthorNamesList(author_ids):
        SQLlog("SQLLoadTransAuthorNamesList, author_ids=%s" % (author_ids))
        from library import list_to_in_clause
        if not author_ids:
                return {}
        author_ids_string = list_to_in_clause(author_ids)
        query = """select a.author_id, at.trans_author_name
                  from authors a, trans_authors at
                  where a.author_id = at.author_id
                  and a.author_id in (%s)""" % author_ids_string
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = {}
        record = CNX.DB_FETCHMANY()
        while record:
                  author_id = record[0][0]
                  trans_author_name = record[0][1]
                  if author_id not in results:
                          results[author_id] = []
                  results[author_id].append(trans_author_name)
                  record = CNX.DB_FETCHMANY()
        return results

def SQLloadTransPubTitles(pub_id):
        SQLlog("SQLloadTransPubTitles, pub_id=%s" % (pub_id))
        query = "select trans_pub_title from trans_pubs where pub_id=%d" % int(pub_id)
        return _OneField(query)

def SQLLoadTransPubTitlesList(pub_ids):
        SQLlog("SQLLoadTransPubTitlesList, pub_ids=%s" % (pub_ids))
        from library import list_to_in_clause
        if not pub_ids:
                return {}
        pub_ids_string = list_to_in_clause(pub_ids)
        query = """select p.pub_id, tp.trans_pub_title
                  from pubs p, trans_pubs tp
                  where p.pub_id = tp.pub_id
                  and p.pub_id in (%s)""" % pub_ids_string
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = {}
        record = CNX.DB_FETCHMANY()
        while record:
                  pub_id = record[0][0]
                  trans_pub_title = record[0][1]
                  if pub_id not in results:
                          results[pub_id] = []
                  results[pub_id].append(trans_pub_title)
                  record = CNX.DB_FETCHMANY()
        return results

def SQLloadPubSeriesWebpages(publisher_id):
        SQLlog("SQLloadPubSeriesWebpages, publisher_id=%s" % (publisher_id))
        query = "select url from webpages where pub_series_id='%d'" % (publisher_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        webpage = CNX.DB_FETCHMANY()
        results = []
        while webpage:
                results.append(webpage[0][0])
                webpage = CNX.DB_FETCHMANY()
        return results

def SQLloadTitleWebpages(title_id):
        SQLlog("SQLloadTitleWebpages, title_id=%s" % (title_id))
        query = "select url from webpages where title_id=%d" % int(title_id)
        return _OneField(query)

def SQLloadPubWebpages(pub_id):
        SQLlog("SQLloadPubWebpages, pub_id=%s" % (pub_id))
        query = "select url from webpages where pub_id=%d" % int(pub_id)
        return _OneField(query)

def SQLloadAwardTypeWebpages(award_type_id):
        SQLlog("SQLloadAwardTypeWebpages, award_type_id=%s" % (award_type_id))
        query = "select url from webpages where award_type_id='%d'" % (int(award_type_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        webpage = CNX.DB_FETCHMANY()
        results = []
        while webpage:
                results.append(webpage[0][0])
                webpage = CNX.DB_FETCHMANY()
        return results

def SQLloadAwardCatWebpages(award_cat_id):
        SQLlog("SQLloadAwardCatWebpages, award_cat_id=%s" % (award_cat_id))
        query = "select url from webpages where award_cat_id='%d'" % (int(award_cat_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        webpage = CNX.DB_FETCHMANY()
        results = []
        while webpage:
                results.append(webpage[0][0])
                webpage = CNX.DB_FETCHMANY()
        return results

def SQLloadSeriesWebpages(series_id):
        SQLlog("SQLloadSeriesWebpages, series_id=%s" % (series_id))
        query = "select url from webpages where series_id='%d'" % (int(series_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        webpage = CNX.DB_FETCHMANY()
        results = []
        while webpage:
                results.append(webpage[0][0])
                webpage = CNX.DB_FETCHMANY()
        return results

def SQLAuthorsBorn(date):
        SQLlog("SQLAuthorsBorn, date=%s" % (date))
        query = """select %s from authors
                where MONTH(author_birthdate)=MONTH('%s')
                and DAYOFMONTH(author_birthdate)=DAYOFMONTH('%s')
                order by author_birthdate""" % (CNX_AUTHORS_STAR, date, date)
        return _StandardQuery(query)

def SQLAuthorsDied(date):
        SQLlog("SQLAuthorsDied, date=%s" % (date))
        query = """select %s from authors
                where MONTH(author_deathdate)=MONTH('%s')
                and DAYOFMONTH(author_deathdate)=DAYOFMONTH('%s')
                order by author_birthdate""" % (CNX_AUTHORS_STAR, date, date)
        return _StandardQuery(query)

def SQLgetUserName(userId):
        SQLlog("SQLgetUserName, userId=%s" % (userId))
        query = "select user_name from mw_user where user_id=%d" % int(userId)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                user = CNX.DB_FETCHONE()
                return user[0][0]
        else:
                return "UNKNOWN"

def SQLgetUserNamesForDict(user_ids):
        SQLlog("SQLgetUserNamesForDict, user_ids=%s" % (user_ids))
        from library import dict_to_in_clause
        if not user_ids:
                return []
        # Retrieve user names for a list of user IDs
        in_clause = dict_to_in_clause(user_ids)
        query = "select user_id, user_name from mw_user where user_id in (%s)" % in_clause
        return _StandardQuery(query)

def SQLgetUserNameAndToken(userId):
        SQLlog("SQLgetUserNameAndToken, userId=%s" % (userId))
        query = "select user_name, user_token from mw_user where user_id=%d" % int(userId)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                user = CNX.DB_FETCHONE()
                return (user[0][0], user[0][1])
        else:
                return ('', '')

def SQLhasNewTalk(userId):
        SQLlog("SQLhasNewTalk, userId=%s" % (userId))
        query = "select 1 from dual where exists (select * from mw_user_newtalk where user_id=%d)" % int(userId)
        count = 0
        # The mw_user_newtalk table does not exist unless MediaWiki is installed,
        # so we trap the exception and treat it as no new messages.
        CNX = MYSQL_CONNECTOR()
        try:
                CNX.DB_QUERY(query)
                if CNX.DB_NUMROWS() > 0:
                        count = 1
        except:
                pass
        return count

def SQLgetTitle(titleId):
        SQLlog("SQLgetTitle, titleId=%s" % (titleId))
        query = "select title_title from titles where title_id=%d" % int(titleId)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS():
                record = CNX.DB_FETCHONE()
                return(record[0][0])
        else:
                return ('')

def SQLgetPubTitle(pubId):
        SQLlog("SQLgetPubTitle, pubId=%s" % (pubId))
        query = "select pub_title from pubs where pub_id=%d" % int(pubId)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS():
                record = CNX.DB_FETCHONE()
                return(record[0][0])
        else:
                return ('')

def SQLTitlesWithPubs(title_ids):
        SQLlog("SQLTitlesWithPubs, title_ids=%s" % (title_ids))
        if not title_ids:
                return []
        in_clause = ", ".join(str(int(tid)) for tid in title_ids)
        query = "select title_id from pub_content where title_id in (%s)" % in_clause
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        results = []
        while title:
                results.append(title[0][0])
                title = CNX.DB_FETCHMANY()
        return results

def SQLisUserBlocked(userId):
        SQLlog("SQLisUserBlocked, userId=%s" % (userId))
        # This query will error out for public backups since most MediaWiki tables have been dropped
        try:
                query = "select * from mw_ipblocks where ipb_user = %d" % int(userId)
                return _BinaryQuery(query)
        except:
                return 0

def SQLisUserSelfApprover(userId):
        SQLlog("SQLisUserSelfApprover, userId=%s" % (userId))
        query = "select * from self_approvers where user_id=%d" % int(userId)
        return _BinaryQuery(query)

def SQLisUserWebAPI(userId):
        SQLlog("SQLisUserWebAPI, userId=%s" % (userId))
        query = "select * from web_api_users where user_id=%d" % int(userId)
        return _BinaryQuery(query)

def SQLisUserModerator(userId):
        SQLlog("SQLisUserModerator, userId=%s" % (userId))
        query = "select * from mw_user_groups where ug_user='%d' and ug_group='sysop'" % (int(userId))
        return _BinaryQuery(query)

def SQLModeratorFlagsForUserList(user_ids):
        SQLlog("SQLModeratorFlagsForUserList, user_ids=%s" % (user_ids))
        from library import list_to_in_clause
        # Retrieve the subset of moderators for a list of user IDs
        in_clause = list_to_in_clause(user_ids)
        query = "select ug_user from mw_user_groups where ug_user in (%s) and ug_group='sysop'" % in_clause
        return _StandardQuery(query)

def SQLisUserBureaucrat(userId):
        SQLlog("SQLisUserBureaucrat, userId=%s" % (userId))
        query = "select * from mw_user_groups where ug_user=%d and ug_group='bureaucrat'" % int(userId)
        return _BinaryQuery(query)

def SQLGetUserBotFlagsForList(user_ids):
        SQLlog("SQLGetUserBotFlagsForList, user_ids=%s" % (user_ids))
        from library import list_to_in_clause
        # Retrieve bot flags for a list of user IDs
        in_clause = list_to_in_clause(user_ids)
        query = "select ug_user from mw_user_groups where ug_user in (%s) and ug_group='bot'" % in_clause
        return _StandardQuery(query)

def SQLUserPrivileges(userId):
        SQLlog("SQLUserPrivileges, userId=%s" % (userId))
        if SQLisUserBureaucrat(userId):
                privileges = 'Bureaucrat'
        elif SQLisUserModerator(userId):
                privileges = 'Moderator'
        elif SQLisUserSelfApprover(userId):
                privileges = 'Self-Approver'
        else:
                privileges = 'Editor'
        return privileges

def SQLWikiEditCountsForIDs(user_ids):
        SQLlog("SQLWikiEditCountsForIDs, user_ids=%s" % (user_ids))
        from library import list_to_in_clause
        # Retrieve the counts of Wiki edits for a list of user IDs
        in_clause = list_to_in_clause(user_ids)
        query = "select user_id, user_editcount from mw_user where user_id in (%s)" % in_clause
        return _StandardQuery(query)

def SQLWikiEditCount(submitter):
        SQLlog("SQLWikiEditCount, submitter=%s" % (submitter))
        # Retrieve the count of Wiki edits by a submitter
        CNX = MYSQL_CONNECTOR()
        query = "select user_editcount from mw_user where user_name='%s'" % (CNX.DB_ESCAPE_STRING(str(submitter)))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                editcount = record[0][0]
                if not editcount:
                        editcount = 0
        else:
                editcount = 0
        return editcount

def SQLgetTitleVariants(title_id):
        SQLlog("SQLgetTitleVariants, title_id=%s" % (title_id))
        CNX = MYSQL_CONNECTOR()
        query = "select %s from titles where title_parent='%d' order by titles.title_copyright, titles.title_title" % (CNX_TITLES_STAR, (title_id))
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        results = []
        while title:
                results.append(list(title[0]))
                title = CNX.DB_FETCHMANY()
        return results

def SQLloadVTsForAuthor(author_id):
        SQLlog("SQLloadVTsForAuthor, author_id=%s" % (author_id))
        CNX = MYSQL_CONNECTOR()
        query = """select %s from titles t, canonical_author ca
                   where t.title_parent = ca.title_id
                   and ca.author_id = %d
                   and ca.ca_status = 1
                   order by t.title_copyright, t.title_title""" % (CNX_TDOT_TITLES_STAR, int(author_id))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(list(record[0]))
                record = CNX.DB_FETCHMANY()
        return results

def SQLloadVTsForTitleList(title_list):
        SQLlog("SQLloadVTsForTitleList, title_list=%s" % (title_list))
        CNX = MYSQL_CONNECTOR()
        query = """select %s from titles t, titles parent
                   where t.title_parent = parent.title_id
                   and parent.title_id in (%s)
                   order by t.title_copyright, t.title_title""" % (CNX_TDOT_TITLES_STAR, CNX.DB_ESCAPE_STRING(title_list))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLgetSubmitterID(submitter, case_sensitive = 1):
        SQLlog("SQLgetSubmitterID, submitter=%s, case_sensitive=%s" % (submitter, case_sensitive))
        CNX = MYSQL_CONNECTOR()
        if case_sensitive:
                query = "select user_id from mw_user where user_name='%s'" % CNX.DB_ESCAPE_STRING(submitter)
        else:
                # We have to use LOWER because user_name in mw_user collates using latin1_bin
                query = "select user_id from mw_user where LOWER(user_name)='%s'" % CNX.DB_ESCAPE_STRING(submitter.lower())
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                userid =  record[0][0]
        else:
                userid =  0
        return(int(userid))

def SQLmarkInProgress(submission):
        SQLlog("SQLmarkInProgress, submission=%s" % (submission))
        update = "update submissions set sub_state='P' where sub_id=%d" %  int(submission)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)

def SQLGetPubContentList(pub_id):
        SQLlog("SQLGetPubContentList, pub_id=%s" % (pub_id))
        query = "select * from pub_content where pub_id=%d" % int(pub_id)
        return _StandardQuery(query)

def SQLGetRefDetails():
        SQLlog("SQLGetRefDetails")
        query = "select * from reference order by reference_label"
        return _StandardQuery(query)

def SQLGetVerificationSource(reference_id):
        SQLlog("SQLGetVerificationSource, reference_id=%s" % (reference_id))
        query = "select * from reference where reference_id = %d" % int(reference_id)
        return _OneRow(query)

def SQLGetVerificationSourceByLabel(reference_label):
        SQLlog("SQLGetVerificationSourceByLabel, reference_label=%s" % (reference_label))
        CNX = MYSQL_CONNECTOR()
        query = "select * from reference where reference_label = '%s'" % CNX.DB_ESCAPE_STRING(reference_label)
        return _OneRow(query)

def SQLGetTemplate(template_id):
        SQLlog("SQLGetTemplate, template_id=%s" % (template_id))
        query = "select * from templates where template_id = %d" % int(template_id)
        return _OneRow(query)

def SQLGetTemplateByName(template_name):
        SQLlog("SQLGetTemplateByName, template_name=%s" % (template_name))
        CNX = MYSQL_CONNECTOR()
        query = "select * from templates where template_name = '%s'" % CNX.DB_ESCAPE_STRING(template_name)
        return _OneRow(query)

def SQLLoadRawTemplates():
        SQLlog("SQLLoadRawTemplates")
        query = "select * from templates order by template_name"
        return _StandardQuery(query)

def SQLLoadAllTemplates():
        SQLlog("SQLLoadAllTemplates")
        # Dictionary of all supported templates. The structure is:
        #   key = template name
        #   1st tuple value = HTML link
        #   2nd tuple value = displayed name, e.g. the "OCLC" in "OCLC 123456"
        #   3rd tuple value = hover-over display value
        query = "select * from templates"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        templates = {}
        while record:
                template_name = record[0][TEMPLATE_NAME]
                template_display = record[0][TEMPLATE_DISPLAYED_NAME]
                template_type = record[0][TEMPLATE_TYPE]
                template_url = record[0][TEMPLATE_URL]
                template_mouseover = record[0][TEMPLATE_MOUSEOVER]
                if template_type == 'Internal URL':
                        template_url = '%s:/%s/%s' % (PROTOCOL, HTFAKE, template_url)
                template_list = [template_url, ]
                if template_display:
                        template_list.append(template_display)
                if template_mouseover:
                        template_list.append(template_mouseover)
                templates[template_name] = tuple(template_list)
                record = CNX.DB_FETCHMANY()
        return templates

def SQLVerificationStatus(pub_id):
        SQLlog("SQLVerificationStatus, pub_id=%s" % (pub_id))
        if SQLPrimaryVerifiers(pub_id):
                return 1
        secondary_verifications = SQLSecondaryVerifications(pub_id)
        for verification in secondary_verifications:
                if verification[VERIF_STATUS] == 1:
                        return 2
        return 0

def SQLSecondaryVerifications(pub_id):
        SQLlog("SQLSecondaryVerifications, pub_id=%s" % (pub_id))
        query = "select * from verification where pub_id=%d" % int(pub_id)
        return _StandardQuery(query)

def SQLActiveSecondaryVerifications(pub_id):
        SQLlog("SQLActiveSecondaryVerifications, pub_id=%s" % (pub_id))
        query = """select v.user_id, v.ver_time, r.reference_label, r.reference_url
                   from verification v, reference r
                   where v.pub_id=%d
                   and v.ver_status = 1
                   and v.reference_id = r.reference_id
                   order by r.reference_id""" % int(pub_id)
        return _StandardQuery(query)

def SQLPrimaryVerifiers(pub_id):
        SQLlog("SQLPrimaryVerifiers, pub_id=%s" % (pub_id))
        query = """select u.user_id, u.user_name, pv.ver_time, pv.ver_transient
                from primary_verifications pv, mw_user u
                where pv.pub_id = %d and pv.user_id = u.user_id
                order by pv.ver_time""" % int(pub_id)
        return _StandardQuery(query)

def SQLPrimaryVerStatus(pub_id, user_id):
        SQLlog("SQLPrimaryVerStatus, pub_id=%s, user_id=%s" % (pub_id, user_id))
        # Returns None if this user hasn't verified this publication;
        # returns 'permanent' or 'transient' otherwise
        query = """select ver_transient
                from primary_verifications pv
                where pub_id = %d and user_id = %d""" % (int(pub_id), int(user_id))
        results = _StandardQuery(query)
        if not results:
                return None
        elif not results[0][0]:
                return 'permanent'
        else:
                return 'transient'

def SQLInsertPrimaryVerification(pub_id, transient, userid):
        SQLlog("SQLInsertPrimaryVerification, pub_id=%s, transient=%s, userid=%s" % (pub_id, transient, userid))
        if transient:
                insert = """insert into primary_verifications(pub_id, user_id, ver_time, ver_transient)
                            values(%d, %d, NOW(), %d)""" % (int(pub_id), int(userid), int(transient))
        else:
                insert = """insert into primary_verifications(pub_id, user_id, ver_time)
                            values(%d, %d, NOW())""" % (int(pub_id), int(userid))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(insert)
        return insert

def SQLGetInterviews(author_id, page_type):
        SQLlog("SQLGetInterviews, author_id=%s, page_type=%s" % (author_id, page_type))
        CNX = MYSQL_CONNECTOR()
        query = """select %s from titles t, canonical_author
                 where t.title_ttype='INTERVIEW'
                 and t.title_id=canonical_author.title_id
                 and canonical_author.ca_status=2
                 and canonical_author.author_id=%d
                 and t.title_parent=0 """ % (CNX_TDOT_TITLES_STAR, int(author_id))
        if page_type == 'Alphabetical':
                query += 'order by t.title_title'
        else:
                query += 'order by t.title_copyright'
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(list(record[0]))
                record = CNX.DB_FETCHMANY()
        return results

def SQLCountPendingSubsForUser(user_id):
        SQLlog("SQLCountPendingSubsForUser, user_id=%s" % (user_id))
        query = """select count(sub_id) from submissions
                 where sub_submitter = %d
                 and sub_state = 'N'""" % int(user_id)
        return _SingleNumericField(query)

def SQLloadXML(recno):
        SQLlog("SQLloadXML, recno=%s" % (recno))
        query = "select sub_data from submissions where sub_id=%d;" % (int(recno))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        xml = record[0][0]
        return(xml)

def SQLloadState(recno):
        SQLlog("SQLloadState, recno=%s" % (recno))
        query = "select sub_state from submissions where sub_id=%d" % int(recno)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        try:
                state = record[0][0]
        except:
                state = None
        return state

def SQLloadSubmission(sub_id):
        SQLlog("SQLloadSubmission, sub_id=%s" % (sub_id))
        query = "select * from submissions where sub_id=%d" % int(sub_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        try:
                return record[0]
        except:
                return None

def SQLRecentSubmissions(pub_id, sub_creation_time):
        SQLlog("SQLRecentSubmissions, pub_id=%s, sub_creation_time=%s" % (pub_id, sub_creation_time))
        query = """select sub_id from submissions
                where sub_state = 'I'
                and sub_type = %d
                and affected_record_id = %d
                and sub_time > '%s'""" % (MOD_PUB_UPDATE, int(pub_id), sub_creation_time)
        return _OneField(query)

def SQLPendingSubmissions(sub_id, sub_type, pub_id, element_name):
        query = """select sub_id from submissions
                where sub_state = 'N'
                and sub_id != %d
                and sub_type = %d
                and sub_data like '%%<%s>%d</%s>%%'
                and sub_data not regexp '(<ContentTitle>|<Cover>)[[:space:]]*<%s>%d</%s>'""" % (sub_id, sub_type,
                                                                                      element_name, pub_id, element_name,
                                                                                      element_name, pub_id, element_name)
        return _OneField(query)

def SQLPendingPubUpdates(sub_id, pub_id):
        query = """select sub_id from submissions
                where sub_state = 'N'
                and sub_id != %d
                and sub_type = %d
                and sub_data like '%%<Record>%d</Record>%%'""" % (sub_id, MOD_PUB_UPDATE, pub_id)
        return _OneField(query)

def SQLPendingTitleRemovals(sub_id, pub_id):
        query = """select sub_id from submissions
                where sub_state = 'N'
                and sub_id != %d
                and sub_type = %d
                and sub_data like '%%<Record>%d</Record>%%'""" % (sub_id, MOD_RMTITLE, pub_id)
        return _OneField(query)

def SQLPendingVTs(sub_id, title_id):
        query = """select sub_id from submissions
                where sub_state = 'N'
                and sub_id != %d
                and sub_type = %d
                and sub_data like '%%<Record>%d</Record>%%'""" % (sub_id, MOD_TITLE_MKVARIANT, title_id)
        return _OneField(query)

def SQLPendingImports(sub_id, pub_id):
        query = """select sub_id from submissions
                where sub_state = 'N'
                and sub_id != %d
                and sub_type = %d
                and sub_data like '%%<ClonedTo>%d</ClonedTo>%%'""" % (sub_id, MOD_PUB_CLONE, pub_id)
        return _OneField(query)

def SQLPendingTitleMerges(sub_id, kept_title_id, dropped_title_ids):
        query = """select sub_id from submissions
                where sub_state = 'N'
                and sub_id != %d
                and sub_type = %d
                and (sub_data like '%%<KeepId>%d</KeepId>%%'""" % (sub_id, MOD_TITLE_MERGE, kept_title_id)
        for dropped_title_id in dropped_title_ids:
                query += """or sub_data like '%%<DropId>%d</DropId>%%'""" % dropped_title_id
        query += ')'
        return _OneField(query)

#############################################################################
# XXX These routine are new and need testing
#############################################################################

def SQLPendingTitleEdits(sub_id, title_ids):
        query = """select sub_id from submissions
                where sub_state = 'N'
                and sub_id != %d
                and sub_type = %d
                and (""" % (sub_id, MOD_TITLE_UPDATE)
        first = 1
        for title_id in title_ids:
                if not first:
                        query += ' or '
                query += """sub_data like '%%<Record>%d</Record>%%'""" % title_id
                first = 0
        query += ')'
        return _OneField(query)

def SQLPendingTitleChangesInPubEdits(sub_id, title_ids):
        query = """select sub_id from submissions
                where sub_state = 'N'
                and sub_id != %d
                and sub_type = %d
                and (""" % (sub_id, MOD_PUB_UPDATE)
        first = 1
        for title_id in title_ids:
                if not first:
                        query += ' or '
                query += """sub_data like '%%<ContentTitle>%%<Record>%d</Record>%%'""" % title_id
                first = 0
        query += ')'
        return _OneField(query)

#############################################################################
# XXX These routine are new and need testing
#############################################################################

def SQLloadNextSelfApproverSubmission(sub_id, reviewer_id):
        query = """select * from submissions s
                where s.sub_state = 'N'
                and s.sub_holdid = 0
                and s.sub_id > %d
                and s.sub_submitter = %d
                order by s.sub_id
                limit 1""" % (int(sub_id), int(reviewer_id))
        return _OneRow(query)

def SQLloadNextSubmission(sub_id, reviewer_id):
        SQLlog("SQLloadNextSubmission, sub_id=%s, reviewer_id=%s" % (sub_id, reviewer_id))
        query = """select * from submissions s
                where s.sub_state = 'N'
                and s.sub_holdid = 0
                and s.sub_id > %d
                and not exists (
                        select 1 from mw_user u, mw_user_groups g
                        where s.sub_submitter != %d
                        and s.sub_submitter = u.user_id
                        and u.user_id = g.ug_user
                        and g.ug_group = 'sysop'
                        )
                and not exists (
                        select 1 from self_approvers sa
                        where sa.user_id = s.sub_submitter
                        and sa.user_id != %d
                        )
                order by s.sub_id
                limit 1""" % (int(sub_id), int(reviewer_id), int(reviewer_id))
        return _OneRow(query)

def SQLwikiLinkExists(namespace, title):
        SQLlog("SQLwikiLinkExists, namespace=%s, title=%s" % (namespace, title))
        if namespace == 'Author':
                num = 100
        elif namespace == 'Bio':
                num = 102
        elif namespace == 'Fanzine':
                num = 104
        elif namespace == 'Magazine':
                num = 106
        elif namespace == 'Publication':
                num = 108
        elif namespace == 'Publisher':
                num = 110
        elif namespace == 'Series':
                num = 112
        else:
                num = 0

        CNX = MYSQL_CONNECTOR()
        newlink = str.replace(title, ' ', '_')
        query = "select page_id from mw_page where page_title='%s' and page_namespace='%d';" % (CNX.DB_ESCAPE_STRING(newlink), num)
        # Use try/except in case this ISFDB instance has no Wiki tables
        try:
                CNX.DB_QUERY(query)
        except:
                return 0

        if CNX.DB_NUMROWS() > 0:
                return 1
        else:
                return 0

def SQLgetTitleTags(title_id):
        SQLlog("SQLgetTitleTags, title_id=%s" % (title_id))
        query = "select distinct tag_mapping.tag_id,tags.tag_name,count(tag_mapping.tag_id) as xx from tag_mapping,tags where tags.tag_id=tag_mapping.tag_id and tag_mapping.title_id=%d group by tag_mapping.tag_id order by xx desc" % int(title_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLgetTagsByTitleForTitleList(title_ids, user_id):
        #SQLlog("SQLgetTagsByTitleForTitleList, title_ids=%s, user_id" % (title_ids, user_id))
        from library import list_to_in_clause
        if not title_ids:
                return {}
        title_list = list_to_in_clause(title_ids)
        query = """select distinct tm.title_id, t.*
                from tag_mapping tm, tags t
                where t.tag_id = tm.tag_id
                and tm.title_id in (%s)
                and (t.tag_status = 0 or tm.user_id = %d)
                """ % (title_list, int(user_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = {}
        while record:
                title_id = record[0][0]
                if title_id not in results:
                        results[title_id] = []
                results[title_id].append(record[0][1:])
                record = CNX.DB_FETCHMANY()
        return results

def SQLgetTitleListTags(title_list, user_id):
        SQLlog("SQLgetTitleListTags, title_list=%s, user_id=%s" % (title_list, user_id))
        CNX = MYSQL_CONNECTOR()
        query = """select distinct tm.tag_id, tags.tag_name, count(tm.tag_id) as xx
                from tag_mapping tm, tags
                where tags.tag_id=tm.tag_id and tm.title_id in (%s)
                and (tags.tag_status=0 or tm.user_id=%d)
                group by tm.tag_id order by xx desc""" % (CNX.DB_ESCAPE_STRING(title_list), int(user_id))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLgetUsersForTag(tag_id):
        SQLlog("SQLgetUsersForTag, tag_id=%s" % (tag_id))
        query = "select distinct tag_mapping.user_id, count(tag_mapping.user_id) as xx, user_name from"
        query += " tag_mapping, mw_user where tag_id=%d and mw_user.user_id=tag_mapping.user_id" % (int(tag_id))
        query += " group by tag_mapping.user_id order by xx desc;"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLgetTitlesForAuthorAndTag(tag_id, author_id):
        SQLlog("SQLgetTitlesForAuthorAndTag, tag_id=%s, author_id=%s" % (tag_id, author_id))
        query = "select distinct DATE_FORMAT(titles.title_copyright, '%Y-%m-%d'), titles.title_title, tag_mapping.title_id"
        query += " from tag_mapping, titles, authors, canonical_author where tag_mapping.tag_id='%d' and titles.title_id=tag_mapping.title_id" % int(tag_id)
        query += " and authors.author_id=canonical_author.author_id and canonical_author.title_id=tag_mapping.title_id and canonical_author.ca_status=1"
        query += " and canonical_author.author_id=%d order by YEAR(titles.title_copyright) desc, titles.title_title" % int(author_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLgetTitlesForTag(tag_id, start):
        SQLlog("SQLgetTitlesForTag, tag_id=%s, start=%s" % (tag_id, start))
        CNX = MYSQL_CONNECTOR()
        query = """select distinct %s from tag_mapping tm, titles t
                 where tm.tag_id=%d and t.title_id=tm.title_id
                 order by YEAR(t.title_copyright) desc, t.title_title
                 limit %d, 101
                 """ % (CNX_TDOT_TITLES_STAR, int(tag_id), int(start))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLgetTitlesForTagForUser(tag_id, user_id, start):
        SQLlog("SQLgetTitlesForTagForUser, tag_id=%s, user_id=%s, start=%s" % (tag_id, user_id, start))
        query = """select t.* from tag_mapping tm, titles t
                 where tm.tag_id=%d and tm.user_id=%d and t.title_id=tm.title_id
                 order by YEAR(t.title_copyright) desc, t.title_title
                 limit %d, 101
                 """ % (int(tag_id), int(user_id), int(start))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLgetAllTitleTags(title_id, parent_id, user_id):
        SQLlog("SQLgetAllTitleTags, title_id=%s, parent_id=%s, user_id=%s" % (title_id, parent_id, user_id))
        query = "select distinct tag_mapping.tag_id,tags.tag_name,count(tag_mapping.tag_id)"
        query += " as xx from tag_mapping,tags where tags.tag_id=tag_mapping.tag_id and"
        query += " (tag_mapping.title_id=%d or tag_mapping.title_id=%d)" % (int(title_id), int(parent_id))
        query += " and (tags.tag_status=0 or tag_mapping.user_id=%d)" % user_id
        query += " group by tag_mapping.tag_id order by xx desc"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLgetTitleTagsByUser(title_id):
        SQLlog("SQLgetTitleTagsByUser, title_id=%s" % (title_id))
        query = """select tm.tag_id, t.tag_name, tm.user_id, tm.tagmap_id
                from tag_mapping tm, tags t
                where t.tag_id = tm.tag_id
                and tm.title_id = %d
                order by t.tag_name""" % int(title_id)
        return _StandardQuery(query)

def SQLgetTagStatusHistory(tag_id):
        SQLlog("SQLgetTagStatusHistory, tag_id=%s" % (tag_id))
        query = """select u.user_name, sl.new_status, sl.timestamp
                from tag_status_log sl, mw_user u
                where sl.tag_id = %d
                and sl.user_id = u.user_id
                order by timestamp desc""" % tag_id
        return _StandardQuery(query)

def SQLgetTitleByTagId(tagmap_id):
        SQLlog("SQLgetTitleByTagId, tagmap_id=%s" % (tagmap_id))
        query = """select title_id from tag_mapping where tagmap_id = %d""" % int(tagmap_id)
        return _OneField(query)

def SQLgetUserTags(title_id, user_id):
        SQLlog("SQLgetUserTags, title_id=%s, user_id=%s" % (title_id, user_id))
        query = "select tags.tag_name from tags,tag_mapping where tag_mapping.title_id='%d' and tag_mapping.user_id='%d' and tag_mapping.tag_id=tags.tag_id;" % (int(title_id), int(user_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0][0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLGetTagById(tag_id):
        SQLlog("SQLGetTagById, tag_id=%s" % (tag_id))
        query = "select * from tags where tag_id = '%d'" % (int(tag_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                tag = CNX.DB_FETCHONE()
                return tag[0]
        else:
                return 0

def SQLgetPopularTags():
        SQLlog("SQLgetPopularTags")
        query = "select distinct tags.tag_id,tags.tag_name from tags,tag_mapping where tag_mapping.title_id='%d' and tag_mapping.tag_id=tags.tag_id;" % int(title_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLgetAuthorTags(author_id, user_id):
        SQLlog("SQLgetAuthorTags, author_id=%s, user_id=%s" % (author_id, user_id))
        query = "select distinct tag_mapping.tag_id,tags.tag_name,count(tag_mapping.tag_id) as xx"
        query += " from tag_mapping,tags,canonical_author where canonical_author.author_id=%d and" % int(author_id)
        query += " canonical_author.title_id=tag_mapping.title_id and tags.tag_id=tag_mapping.tag_id"
        query += " and (tags.tag_status=0 or tag_mapping.user_id=%d)" % user_id
        query += " group by tag_mapping.tag_id order by xx desc"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLsearchTags(tag):
        SQLlog("SQLsearchTags, tag=%s" % (tag))
        CNX = MYSQL_CONNECTOR()
        query = "select * from tags where tag_name like '%%%s%%' order by tag_name" % (CNX.DB_ESCAPE_STRING(tag))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLLoadTagStatusChanges():
        SQLlog("SQLLoadTagStatusChanges")
        query = """select tsl.tag_id, t.tag_name, tsl.new_status, tsl.timestamp, u.user_name
                from tag_status_log tsl, mw_user u, tags t
                where tsl.user_id = u.user_id
                and tsl.tag_id = t.tag_id
                order by tsl.timestamp desc"""
        return _StandardQuery(query)

def SQLLoadPrivateTags():
        SQLlog("SQLLoadPrivateTags")
        query = 'select tag_id, tag_name from tags where tag_status = 1 order by tag_name'
        return _StandardQuery(query)

def SQLaddTagToTitle(tag, title_id, user_id):
        SQLlog("SQLaddTagToTitle, tag=%s, title_id=%s, user_id=%s" % (tag, title_id, user_id))
        print_string = []
        CNX = MYSQL_CONNECTOR()
        query = "select tag_id from tags where tag_name='%s'" % (CNX.DB_ESCAPE_STRING(tag))
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() < 1:
                update = "insert into tags(tag_name) values('%s')" % (CNX.DB_ESCAPE_STRING(tag))
                print_string.append(update)
                CNX.DB_QUERY(update)
                tag_id = CNX.DB_INSERT_ID()
        else:
                record = CNX.DB_FETCHONE()
                tag_id = int(record[0][0])

        update = 'insert into tag_mapping(tag_id, title_id, user_id) values(%d,%d,%d)' % (int(tag_id), int(title_id), int(user_id))
        print_string.append(update)
        CNX.DB_QUERY(update)
        return print_string

def SQLDeleteDuplicateTags(title_id):
        SQLlog("SQLDeleteDuplicateTags, title_id=%s" % (title_id))
        query = "select tag_id, title_id, user_id, count(*) as xx from tag_mapping where title_id=%d group by tag_id,title_id,user_id having xx >1" % (int(title_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        tags = []
        while record:
                tags.append(record[0])
                record = CNX.DB_FETCHMANY()
        for tag in tags:
                tag_id = tag[0]
                title_id = tag[1]
                user_id = tag[2]
                update = "delete from tag_mapping where tag_id=%d and title_id=%d and user_id=%d" % (int(tag_id), int(title_id), int(user_id))
                CNX.DB_QUERY(update)
                update = "insert into tag_mapping(tag_id, title_id, user_id) values(%d, %d, %d)" % (int(tag_id), int(title_id), int(user_id))
                CNX.DB_QUERY(update)

def SQLDeleteTagMapping(tagmap_id):
        SQLlog("SQLDeleteTagMapping, tagmap_id=%s" % (tagmap_id))
        update = "delete from tag_mapping where tagmap_id = %d" % int(tagmap_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)
        SQLDeteleOrphanTags()

def SQLDeteleOrphanTags():
        SQLlog("SQLDeteleOrphanTags")
        update = 'delete from tags where NOT EXISTS (select 1 from tag_mapping where tags.tag_id = tag_mapping.tag_id)'
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)

def SQLFindReviewParent(title, author, referral_lang):
        SQLlog("SQLFindReviewParent, title=%s, author=%s, referral_lang=%s" % (title, author, referral_lang))
        # If the language of the referral title is not defined, do not auto-link the review
        if not referral_lang:
                return(0)
        # Attempt to find matching book-length works first, then short fiction
        for title_types in ("'ANTHOLOGY','COLLECTION','NOVEL','NONFICTION','OMNIBUS'", "'SHORTFICTION'"):
                CNX = MYSQL_CONNECTOR()
                query = """select t.*
                        from titles t, canonical_author ca, authors a
                        where t.title_ttype in (%s)
                        and t.title_title = '%s'
                        and t.title_language = %d
                        and ca.title_id = t.title_id
                        and ca.author_id = a.author_id
                        and a.author_canonical = '%s'""" % (title_types, CNX.DB_ESCAPE_STRING(title), int(referral_lang), CNX.DB_ESCAPE_STRING(author))
                CNX.DB_QUERY(query)
                # Auto-link reviews if there is one and only one title/author/language match
                if CNX.DB_NUMROWS() == 1:
                        title = CNX.DB_FETCHONE()
                        return(title[0][0])
        return(0)

def SQLLoadReviewsForTitle(title_id):
        SQLlog("SQLLoadReviewsForTitle, title_id=%s" % (title_id))
        query = """select review.*
                    from titles review, title_relationships tr
                    where tr.review_id = review.title_id
                    and tr.title_id = %d
                    order by review.title_copyright""" % title_id
        return _StandardQuery(query)

def SQLloadAllTitleReviews(title_id):
        SQLlog("SQLloadAllTitleReviews, title_id=%s" % (title_id))
        if not title_id:
                return
        # 1. Reviews of the main title
        query = """select review.title_id as review_id, DATE_FORMAT(review.title_copyright, '%%Y-%%m-%%d') as review_date,
                    review.title_language as language_id, review.title_parent as review_parent_id,
                    parent.title_copyright as review_parent_date, p.pub_id, p.pub_title, DATE_FORMAT(p.pub_year, '%%Y-%%m-%%d') as newpub_year
                    from title_relationships tr
                    inner join titles review on (tr.review_id = review.title_id and tr.title_id = %d)
                    inner join pub_content pc on (pc.title_id = tr.review_id)
                    inner join pubs p on (pc.pub_id = p.pub_id)
                    left join titles parent on (review.title_parent = parent.title_id)""" % title_id

        # 2. Reviews of VTs of the main title
        query += """ UNION
                select review.title_id as review_id, DATE_FORMAT(review.title_copyright, '%%Y-%%m-%%d') as review_date,
                review.title_language as language_id, review_parent.title_id as review_parent_id,
                review_parent.title_copyright as review_parent_date,
                p.pub_id, p.pub_title, p.pub_year
                from title_relationships tr
                inner join titles vt on (vt.title_parent = %d and tr.title_id = vt.title_id)
                inner join titles review on (tr.review_id = review.title_id)
                inner join pub_content pc on (pc.title_id = review.title_id)
                inner join pubs p on (pc.pub_id = p.pub_id)
                left join titles review_parent on (review.title_parent = review_parent.title_id)""" % title_id

        # 3. Variants of reviews of the main title
        query += """ UNION
                select variant_review.title_id as review_id, variant_review.title_copyright as review_date,
                variant_review.title_language as language_id,
                parent_review.title_id as review_parent_id, parent_review.title_copyright as review_parent_date,
                p.pub_id, p.pub_title, p.pub_year
                from titles variant_review, titles parent_review,
                title_relationships tr, pubs p, pub_content pc
                where tr.title_id = %d
                and tr.review_id = parent_review.title_id
                and parent_review.title_id = variant_review.title_parent
                and pc.title_id = variant_review.title_id
                and pc.pub_id = p.pub_id""" % title_id

        # 4. Variants of reviews of VTs of the main title
        query += """ UNION
                select variant_review.title_id as review_id, variant_review.title_copyright as review_date,
                variant_review.title_language as language_id,
                parent_review.title_id as parent_review_id, parent_review.title_copyright as parent_review_date,
                p.pub_id, p.pub_title, p.pub_year
                from titles variant_review, titles parent_review, titles variant_reviewed,
                title_relationships tr, pubs p, pub_content pc
                where variant_reviewed.title_parent = %d
                and tr.title_id = variant_reviewed.title_id
                and tr.review_id = parent_review.title_id
                and parent_review.title_id = variant_review.title_parent
                and pc.title_id = variant_review.title_id
                and pc.pub_id = p.pub_id""" % title_id
        return _StandardQuery(query)

def SQLfindReviewedTitle(review_id):
        SQLlog("SQLfindReviewedTitle, review_id=%s" % (review_id))
        query = "select title_id from title_relationships where review_id='%d'" % (review_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title_id = CNX.DB_FETCHONE()
        if title_id:
                return(title_id[0][0])
        else:
                return(0)

def SQLGetPseudIdByAuthorAndPseud(parent,pseudonym):
        SQLlog("SQLGetPseudIdByAuthorAndPseud, parent=%s, pseudonym=%s" % (parent,pseudonym))
        query = "select pseudo_id from pseudonyms where author_id = %d and pseudonym = %d order by pseudo_id desc limit 1" % (int(parent), int(pseudonym))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        pub = CNX.DB_FETCHONE()
        if pub:
                return pub[0][0]
        else:
                return []

def SQLLoadWebSites(isbn, user_id = None, format = None):
        SQLlog("SQLLoadWebSites, isbn=%s, user_id=%s, format=%s" % (isbn, user_id, format))
        if PYTHONVER == 'python2':
                from urlparse import urlparse
        else:
                from urllib.parse import urlparse
        from isbn import convertISBN, toISBN10, toISBN13
        newisbn = str.replace(str(isbn), '-', '')
        newisbn = str.replace(newisbn, ' ', '')
        isbn13 = toISBN13(newisbn)
        isbn10 = toISBN10(newisbn)

        if user_id:
                query = """select w.site_url, w.site_name, w.site_isbn13
                         from websites w
                         where exists(select 1 from user_sites u
                          where u.user_id = %d
                          and u.site_id = w.site_id
                          and u.user_choice = 1)
                         or not exists(select 1 from user_sites u
                          where u.user_id = %d
                          and u.site_id = w.site_id)
                          order by w.site_name""" % (int(user_id), int(user_id))
        else:
                query = "select site_url, site_name, site_isbn13 from websites order by site_name"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        site = CNX.DB_FETCHMANY()
        results = []
        while site:
                site_url = site[0][0]
                site_name = site[0][1]
                site_isbn13 = site[0][2]
                # For Amazon ebook links and 979 ISBN-13s, link to the Amazon search
                # page because direct links using ISBN-10s do not work
                if site_name[0:6] == 'Amazon' and (format == 'ebook' or (len(newisbn) == 13 and isbn13[:3] == '979')):
                        parsed_url = urlparse(site_url)
                        scheme = parsed_url[0]
                        # Extract the "domain:port" part of the URL
                        netloc = parsed_url[1]
                        url_string = '%s://%s/s?search-alias=stripbooks&field-isbn=%s' % (scheme, netloc, isbn13)
                        if site_name == 'Amazon US':
                                url_string += '&tag=isfdb-20'
                        elif site_name == 'Amazon UK':
                                url_string += '&tag=isfdb-21'
                # European Library requires ISBNs in search strings to be exact, i.e. ISBN-10s for
                # pre-2008 books and ISBN-13s for post-2008 books. Also, some of their records
                # include dashes and some don't, so we need to search for both forms of the ISBN.
                elif 'European Library' in site_name:
                        url_string = str.replace(site_url, "%s", newisbn + '+or+' + convertISBN(newisbn))
                # Some sites like Open Library and BnF require ISBNs in search strings
                # to be exact, i.e. ISBN-10s for pre-2008 books and ISBN-13s for post-2008 books.
                elif site_isbn13 == 2:
                        url_string = str.replace(site_url, "%s", newisbn)
                elif site_isbn13 == 1:
                        url_string = str.replace(site_url,"%s",isbn13)
                else:
                        url_string = str.replace(site_url,"%s",isbn10)
                url_string = str.replace(url_string, '&', '&amp;')
                results.append((site_name, url_string),)
                site = CNX.DB_FETCHMANY()
        return results

def SQLLoadRecognizedDomains():
        SQLlog("SQLLoadRecognizedDomains")
        query = "select * from recognized_domains"
        return _StandardQuery(query)

def SQLGetRecognizedDomainByID(domain_id):
        SQLlog("SQLGetRecognizedDomainByID, domain_id=%s" % (domain_id))
        query = "select * from recognized_domains where domain_id = %d" % int(domain_id)
        return _OneRow(query)

def SQLGetSubmissionHoldId(submission):
        SQLlog("SQLGetSubmissionHoldId, submission=%s" % (submission))
        query = "select sub_holdid from submissions where sub_id=%d" % int(submission)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                return record[0][0]
        else:
                return ''

def SQLGetSubmitterId(submission):
        SQLlog("SQLGetSubmitterId, submission=%s" % (submission))
        query = "select sub_submitter from submissions where sub_id='%d';" % (int(submission))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        submitter_id = record[0][0]
        return submitter_id

def SQLLoadUserPreferences(user_id):
        SQLlog("SQLLoadUserPreferences, user_id=%s" % (user_id))
        # Get the currently defined preferences for the logged-in user
        query = """select concise_disp, default_language, display_all_languages,
                covers_display, suppress_translation_warnings, suppress_bibliographic_warnings,
                cover_links_display, keep_spaces_in_searches, suppress_help_bubbles,
                suppress_awards, suppress_reviews, display_post_submission, display_title_translations
                from user_preferences where user_id=%d""" % int(user_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        # Set the default values; the default language is 17, i.e. "English"
        preferences = (0, 17, 'All', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
        if CNX.DB_NUMROWS() > 0:
                row = CNX.DB_FETCHONE()
                # Temporarily convert the tuple returned by the query to a list
                preferences = list(row[0])
                if not preferences[1]:
                        preferences[1] = 17
                # Convert the list back to a tuple
                preferences = tuple(preferences)
        return preferences

def SQLLoadUserLanguages(user_id):
        SQLlog("SQLLoadUserLanguages, user_id=%s" % (user_id))
        query = "select lang_id from user_languages where user_id = %d;" % int(user_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        languages = []
        record = CNX.DB_FETCHMANY()
        while record:
                languages.append(record[0][0])
                record = CNX.DB_FETCHMANY()
        return languages

def SQLGetLangIdByName(lang_name):
        SQLlog("SQLGetLangIdByName, lang_name=%s" % (lang_name))
        CNX = MYSQL_CONNECTOR()
        query = "select lang_id from languages where lang_name ='%s'" % (CNX.DB_ESCAPE_STRING(lang_name))
        return _SingleNumericField(query)

def SQLGetLangIdByCode(lang_code):
        SQLlog("SQLGetLangIdByCode, lang_code=%s" % (lang_code))
        CNX = MYSQL_CONNECTOR()
        query = "select lang_id from languages where lang_code ='%s'" % (CNX.DB_ESCAPE_STRING(lang_code))
        return _SingleNumericField(query)

def SQLUserPreferencesId(user_id):
        SQLlog("SQLUserPreferencesId, user_id=%s" % (user_id))
        query = "select user_pref_id from user_preferences where user_id='%d'" % (int(user_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() < 1:
                return 0
        record = CNX.DB_FETCHONE()
        user_pref_id = int(record[0][0])
        return user_pref_id

def SQLUpdate_last_viewed_verified_pubs_DTS(user_id):
        SQLlog("SQLUpdate_last_viewed_verified_pubs_DTS, user_id=%s" % (user_id))
        # Update the "last viewed changed primary verified pubs report" DTS
        # and return the previous DTS
        query = "select last_viewed_ver_pubs from user_status where user_id=%d" % (int(user_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() < 1:
                previous_last_viewed = None
                update = """insert into user_status(user_id, last_viewed_ver_pubs)
                          values(%d, NOW())""" % int(user_id)
        else:
                record = CNX.DB_FETCHONE()
                previous_last_viewed = record[0][0]
                update = """update user_status set last_viewed_ver_pubs =
                          NOW() where user_id = %d""" % int(user_id)
        CNX.DB_QUERY(update)
        return previous_last_viewed

def SQLUpdate_last_changed_verified_pubs_DTS(user_id):
        SQLlog("SQLUpdate_last_changed_verified_pubs_DTS, user_id=%s" % (user_id))
        query = "select user_id from user_status where user_id=%d" % (int(user_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() < 1:
                update = """insert into user_status(user_id, last_changed_ver_pubs)
                          values(%d, NOW())""" % int(user_id)
        else:
                update = """update user_status set last_changed_ver_pubs =
                          NOW() where user_id = %d""" % int(user_id)
        CNX.DB_QUERY(update)

def SQLListAwardTypes():
        SQLlog("SQLListAwardTypes")
        query = "select * from award_types order by award_type_name"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = []
        record = CNX.DB_FETCHMANY()
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLGetAwardTypeByCode(award_type_code):
        SQLlog("SQLGetAwardTypeByCode, award_type_code=%s" % (award_type_code))
        CNX = MYSQL_CONNECTOR()
        query = "select * from award_types where award_type_code='%s'" % (CNX.DB_ESCAPE_STRING(award_type_code))
        CNX.DB_QUERY(query)
        award_type = []
        if CNX.DB_NUMROWS() > 0:
                record = CNX.DB_FETCHONE()
                award_type = record[0]
        return award_type

def SQLGetAwardTypeByName(award_type_name):
        SQLlog("SQLGetAwardTypeByName, award_type_name=%s" % (award_type_name))
        CNX = MYSQL_CONNECTOR()
        query = "select * from award_types where award_type_name='%s'" % (CNX.DB_ESCAPE_STRING(award_type_name))
        CNX.DB_QUERY(query)
        award_type = []
        if CNX.DB_NUMROWS() > 0:
                record = CNX.DB_FETCHONE()
                award_type = record[0]
        return award_type

def SQLGetAwardTypeByShortName(award_type_short_name):
        SQLlog("SQLGetAwardTypeByShortName, award_type_short_name=%s" % (award_type_short_name))
        CNX = MYSQL_CONNECTOR()
        query = "select * from award_types where award_type_short_name='%s'" % (CNX.DB_ESCAPE_STRING(award_type_short_name))
        CNX.DB_QUERY(query)
        award_type = []
        if CNX.DB_NUMROWS() > 0:
                record = CNX.DB_FETCHONE()
                award_type = record[0]
        return award_type

def SQLGetAwardTypeById(award_type_id):
        SQLlog("SQLGetAwardTypeById, award_type_id=%s" % (award_type_id))
        query = "select * from award_types where award_type_id='%d'" % (int(award_type_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        award_type = []
        if CNX.DB_NUMROWS() > 0:
                record = CNX.DB_FETCHONE()
                award_type = record[0]
        return award_type

def SQLGetSeriesByName(series_name):
        SQLlog("SQLGetSeriesByName, series_name=%s" % (series_name))
        CNX = MYSQL_CONNECTOR()
        query = "select * from series where series_title='%s'" % (CNX.DB_ESCAPE_STRING(series_name))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                return record[0]
        else:
                return 0

def SQLGetAwardYears(award_type_id):
        SQLlog("SQLGetAwardYears, award_type_id=%s" % (award_type_id))
        query = "select distinct DATE_FORMAT(award_year, '%%Y-%%m-%%d') from awards where award_type_id=%d order by award_year" % (int(award_type_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = []
        record = CNX.DB_FETCHMANY()
        while record:
                results.append(record[0][0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLGetAwardCategories(award_type_id):
        SQLlog("SQLGetAwardCategories, award_type_id=%s" % (award_type_id))
        query = "select * from award_cats where award_cat_type_id=%d order by award_cat_name" % int(award_type_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = []
        record = CNX.DB_FETCHMANY()
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLGetAwardCatById(award_cat_id):
        SQLlog("SQLGetAwardCatById, award_cat_id=%s" % (award_cat_id))
        query = "select * from award_cats where award_cat_id=%d" % int(award_cat_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                return record[0]
        else:
                return ()

def SQLGetAwardCatByName(award_cat_name, award_cat_type_id):
        SQLlog("SQLGetAwardCatByName, award_cat_name=%s, award_cat_type_id=%s" % (award_cat_name, award_cat_type_id))
        CNX = MYSQL_CONNECTOR()
        query = "select * from award_cats where award_cat_name='%s' and award_cat_type_id=%d" % (CNX.DB_ESCAPE_STRING(award_cat_name), int(award_cat_type_id))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record:
                return record[0]
        else:
                return ()

def SQLSearchAwards(award):
        SQLlog("SQLSearchAwards, award=%s" % (award))
        CNX = MYSQL_CONNECTOR()
        query = "select * from award_types where award_type_name like '%%%s%%' or award_type_short_name like '%%%s%%' order by award_type_short_name" % (CNX.DB_ESCAPE_STRING(award), CNX.DB_ESCAPE_STRING(award))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        results = []
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLGetAwardCatBreakdown(award_type_id):
        SQLlog("SQLGetAwardCatBreakdown, award_type_id=%s" % (award_type_id))
        query = """select c.award_cat_name, a.award_cat_id, c.award_cat_order,
                   sum(if(a.award_level='1',1,0)), count(a.award_id),
                   IF(c.award_cat_order IS NULL, 1, 0) AS isnull
                   from awards a, award_cats c
                   where a.award_cat_id = c.award_cat_id
                   and a.award_type_id = %d
                   group by a.award_cat_id
                   order by isnull, c.award_cat_order, c.award_cat_name
                   """  % int(award_type_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = []
        record = CNX.DB_FETCHMANY()
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLGetEmptyAwardCategories(award_type_id):
        SQLlog("SQLGetEmptyAwardCategories, award_type_id=%s" % (award_type_id))
        query = """select *, IF(award_cat_order IS NULL, 1, 0) AS isnull from award_cats
                   where award_cat_type_id=%d
                   and NOT EXISTS
                     (select award_id from awards
                      where award_cat_id = award_cats.award_cat_id)
                   order by isnull, award_cat_order, award_cat_name
                   """ % int(award_type_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = []
        record = CNX.DB_FETCHMANY()
        while record:
                results.append(record[0])
                record = CNX.DB_FETCHMANY()
        return results

def SQLGetPageNumber(title_id, pub_id):
        SQLlog("SQLGetPageNumber, title_id=%s, pub_id=%s" % (title_id, pub_id))
        query = 'select pubc_page from pub_content where title_id=%d and pub_id=%d' % (int(title_id), int(pub_id))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        try:
                return record[0][0]
        except:
                return 0

def SQLtransLegalNames(author_ids):
        SQLlog("SQLtransLegalNames, author_ids=%s" % (author_ids))
        from library import list_to_in_clause
        if not author_ids:
                return {}
        author_ids_string = list_to_in_clause(author_ids)
        query = """select a.author_id, t.trans_legal_name
                from authors a, trans_legal_names t
                where a.author_id = t.author_id
                and a.author_id in (%s)""" % author_ids_string
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        results = {}
        record = CNX.DB_FETCHMANY()
        while record:
                author_id = record[0][0]
                trans_legal_name = record[0][1]
                if author_id not in results:
                        results[author_id] = []
                results[author_id].append(trans_legal_name)
                record = CNX.DB_FETCHMANY()
        return results

def SQLPubArtists(pubid):
        SQLlog("SQLPubArtists, pubid=%s" % (pubid))
        titles = SQLloadTitlesXBT(pubid)
        results = []
        for title in titles:
                if title[TITLE_TTYPE] == 'COVERART':
                        authors = SQLTitleAuthors(title[TITLE_PUBID])
                        for author in authors:
                                results.append(author)
        return results

def SQLPubCovers(pubid):
        SQLlog("SQLPubCovers, pubid=%s" % (pubid))
        query = """select t.* from titles t, pub_content pc
                   where pc.pub_id=%d and pc.title_id = t.title_id
                   and t.title_ttype='COVERART'""" % int(pubid)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        titles = []
        while title:
                titles.append(title[0])
                title = CNX.DB_FETCHMANY()
        return titles

def SQLFindMonth(target):
        SQLlog("SQLFindMonth, target=%s" % (target))
        results = []
        CNX = MYSQL_CONNECTOR()
        query = "select * from titles where title_copyright like '%s%%' order by title_title" % (CNX.DB_ESCAPE_STRING(target))
        CNX.DB_QUERY(query)
        title = CNX.DB_FETCHMANY()
        while title:
                results.append(title[0])
                title = CNX.DB_FETCHMANY()
        return results

def SQLChangedVerifications(user_id):
        SQLlog("SQLChangedVerifications, user_id=%s" % (user_id))
        import time
        # Returns 1 if one the logged-in user's primary verified publications has been changed by
        # another user since the logged-in user last looked at the report of changed verified pubs

        # Retrieve the "last viewed" and the "last changed" date/time stamps
        query = """select last_changed_ver_pubs, last_viewed_ver_pubs
                    from user_status where user_id = %d""" % int(user_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        # If the logged-in user has never checked this report and there are no changed verified pubs, return 0
        if not CNX.DB_NUMROWS():
                return 0

        value = CNX.DB_FETCHONE()
        last_viewed = value[0][1]
        last_changed = value[0][0]
        # If none of the logged-in user's primary verified pubs have been changed, return 0
        if not last_changed:
                return 0
        # If some verified pubs have been changed but the user hasn't displayed the report yet,
        # return 1
        if not last_viewed:
                return 1
        # If a verified pub has been changed since the logged in user last checked the report,
        # return 1
        if last_changed > last_viewed:
                # If the logged-in user last checked the report before the last change, return 1
                return 1
        return 0

def convertActivityDate(theDate):
        from datetime import datetime
        from calendar import timegm

        if theDate:
                year = theDate[:4]
                month = theDate[5:7]
                day = theDate[8:10]
                hours = theDate[11:13]
                minutes = theDate[14:16]
                seconds = theDate[17:19]
                theDate_utc = datetime.strptime('%s-%s-%s %s:%s:%s' % (year, month, day, hours, minutes, seconds), '%Y-%m-%d %H:%M:%S')
                theDate = timegm(theDate_utc.timetuple())
                theDate = datetime.fromtimestamp(theDate)
                return(theDate)
        else:
                return ''

def SQLLastUserActivity(user_id):
        SQLlog("SQLLastUserActivity, user_id=%s" % (user_id))
        query = """select DATE_FORMAT(ver_time, '%%Y-%%m-%%d %%H.%%m.%%S') from primary_verifications
                where user_id = %d order by ver_time desc limit 1""" % int(user_id)
        results = _StandardQuery(query)
        if results:
                primary_ver = results[0][0]
                primary_ver = convertActivityDate(primary_ver)
        else:
                primary_ver = ''

        query = """select DATE_FORMAT(ver_time, '%%Y-%%m-%%d %%H.%%m.%%S') from verification
                where user_id = %d order by ver_time desc limit 1""" % int(user_id)
        results = _StandardQuery(query)
        if results:
                sec_ver = results[0][0]
                sec_ver = convertActivityDate(sec_ver)
        else:
                sec_ver = ''

        query = """select DATE_FORMAT(sub_time, '%%Y-%%m-%%d %%H.%%m.%%S') from submissions
                   where sub_submitter = %d
                   and sub_state = 'I'
                   order by sub_id desc limit 1""" % int(user_id)
        results = _StandardQuery(query)
        if results:
                last_submission = results[0][0]
                last_submission = convertActivityDate(last_submission)
        else:
                last_submission = ''

        last_wiki = GetLastWiki(user_id)

        last_activity = primary_ver
        if sec_ver:
                if not last_activity:
                        last_activity = sec_ver
                elif sec_ver > last_activity:
                        last_activity = sec_ver
        if last_submission:
                if not last_activity:
                        last_activity = last_submission
                elif last_submission > last_activity:
                        last_activity = last_submission
        if last_wiki:
                if not last_activity:
                        last_activity = last_wiki
                elif last_wiki > last_activity:
                        last_activity = last_wiki

        if not last_activity:
                return None
        else:
                return last_activity.date()

def GetLastWiki(user_id):
        SQLlog("GetLastWiki, user_id=%s" % (user_id))
        from datetime import datetime
        from calendar import timegm
        # The mw_revision table may not exist unless MediaWiki is installed,
        # so we trap the exception and treat it as no Wiki activity.
        # mw_revision field structure was changed in version 1.35. In versions
        # 1 through 1.34 all data was stored in 'mw_revision'. In versions 1.35+
        # the data was split across 'mw_revision', 'mw_revision_actor_temp' and
        # 'mw_actor'.
        last_wiki = ''
        results = []
        try:
                query = "select max(rev_timestamp) from mw_revision where rev_user = %d" % int(user_id)
                results = _StandardQuery(query)
        except:
                pass

        if not results:
                try:
                        # split into 2 queries for performance reasons
                        query = """select max(at.revactor_rev)
                                from mw_revision_actor_temp at, mw_actor a
                                where at.revactor_actor = a.actor_id
                                and a.actor_id = %d""" % int(user_id)
                        revisions = _StandardQuery(query)
                        if revisions:
                                revision_id = revisions[0][0]
                                query = "select rev_timestamp from mw_revision where rev_id = %d" % revision_id
                                results = _StandardQuery(query)
                except:
                        pass

        if results:
                timestamp = results[0][0]
                if timestamp:
                        year = timestamp[:4]
                        month = timestamp[4:6]
                        day = timestamp[6:8]
                        hours = timestamp[8:10]
                        minutes = timestamp[10:12]
                        seconds = timestamp[12:14]
                        wiki_utc = datetime.strptime('%s-%s-%s %s:%s:%s' % (year, month, day, hours, minutes, seconds), '%Y-%m-%d %H:%M:%S')
                        timestamp = timegm(wiki_utc.timetuple())
                        last_wiki = datetime.fromtimestamp(timestamp)
        return last_wiki

def SQLLoadIdentifierTypes():
        SQLlog("SQLLoadIdentifierTypes")
        # Returns a dictionary of all supported external identifier types
        # The dictionary structure is:
        #       results[type_number] = (type_name, type_full_name)
        query = "select * from identifier_types"
        type_list = _StandardQuery(query)
        results = {}
        for id_type in type_list:
                type_number = id_type[IDTYPE_ID]
                type_name = id_type[IDTYPE_NAME]
                type_full_name = id_type[IDTYPE_FULL_NAME]
                results[type_number] = (type_name, type_full_name)
        return results

def SQLLoadIdentifiers(pub_id):
        SQLlog("SQLLoadIdentifiers, pub_id=%s" % (pub_id))
        query = "select * from identifiers where pub_id = %d" % int(pub_id)
        return _StandardQuery(query)

def SQLLoadIdentifierSites():
        SQLlog("SQLLoadIdentifierSites")
        query = "select * from identifier_sites order by site_position, site_name"
        return _StandardQuery(query)

def SQLFindPubByExternalID(id_type, id_value):
        SQLlog("SQLFindPubByExternalID, id_type=%s, id_value=%s" % (id_type, id_value))
        id_value = id_value.replace('*','%')
        CNX = MYSQL_CONNECTOR()
        query = """select p.* from pubs p, identifiers id
                   where p.pub_id = id.pub_id
                   and id.identifier_type_id = %d
                   and id.identifier_value like '%s'""" % (int(id_type), CNX.DB_ESCAPE_STRING(id_value))
        return _StandardQuery(query)

def SQLLoadVotes(title_id, variants, user_id):
        SQLlog("SQLLoadVotes, title_id=%s, variants=%s, user_id=%s" % (title_id, variants, user_id))
        from library import list_to_in_clause
        vote_count = 0
        average_vote = 0
        user_vote = 0
        query = "select count(vote_id), ROUND(AVG(rating),2) from votes where title_id = %d" % int(title_id)
        results = _StandardQuery(query)
        if results[0][0]:
                vote_count = int(results[0][0])
                average_vote = float(results[0][1])
                query = "select rating from votes where title_id = %d and user_id = %d" % (int(title_id), int(user_id))
                results = _StandardQuery(query)
                if results:
                        user_vote = int(results[0][0])

        composite_vote_count = vote_count
        composite_average_vote = average_vote
        if variants:
                variant_ids = []
                variant_ids.append(title_id)
                for variant in variants:
                        variant_id = variant[TITLE_PUBID]
                        variant_ids.append(variant_id)
                variant_clause = list_to_in_clause(variant_ids)
                query = "select count(vote_id), ROUND(AVG(rating),2) from votes where title_id in (%s)" % variant_clause
                results = _StandardQuery(query)
                if results[0][0]:
                        composite_vote_count = int(results[0][0])
                        composite_average_vote = float(results[0][1])

        return (vote_count, average_vote, composite_vote_count, composite_average_vote, user_vote)

def SQLQueueSize():
        SQLlog("SQLQueueSize")
        query = """select count(s.sub_id)
        from submissions s
        where s.sub_state='N'
        and s.sub_submitter!=13571
        and s.sub_holdid=0
        and not exists
        (select 1 from mw_user_groups g where g.ug_user=s.sub_submitter and g.ug_group='sysop')"""
        return _StandardQuery(query)[0][0]

def SQLCountPubsForTitle(title_id):
        SQLlog("SQLCountPubsForTitle, title_id=%s" % (title_id))
        # Retrieve the number of pubs that this title exists in
        query = "select count(*) from pub_content where title_id = %d" % int(title_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        result_record = CNX.DB_FETCHONE()
        if result_record and result_record[0][0] > 1:
                return 1
        return 0

def SQLGetLangIdByTitle(title_id):
        SQLlog("SQLGetLangIdByTitle, title_id=%s" % (title_id))
        query = "select title_language from titles where title_id=%d" % int(title_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        lang_id = ''
        if CNX.DB_NUMROWS():
                record = CNX.DB_FETCHONE()
                lang_id = record[0][0]
        if lang_id is None:
                lang_id = ''
        return lang_id

def SQLDeletedPub(pubid):
        SQLlog("SQLDeletedPub, pubid=%s" % (pubid))
        query = "select 1 from submissions where sub_type = %d and affected_record_id = %d" % (MOD_PUB_DELETE, pubid)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                return 1
        else:
                return 0

def SQLDeletedTitle(title_id):
        SQLlog("SQLDeletedTitle, title_id=%s" % (title_id))
        query = "select 1 from submissions where sub_type = %d and affected_record_id = %d" % (MOD_TITLE_DELETE, title_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                return 1
        else:
                return 0

def SQLDeletedAward(award_id):
        SQLlog("SQLDeletedAward, award_id=%s" % (award_id))
        query = "select 1 from submissions where sub_type = %d and affected_record_id = %d" % (MOD_AWARD_DELETE, award_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                return 1
        else:
                return 0

def SQLDeletedAwardType(award_type_id):
        SQLlog("SQLDeletedAwardType, award_type_id=%s" % (award_type_id))
        query = "select 1 from submissions where sub_type = %d and affected_record_id = %d" % (MOD_AWARD_TYPE_DELETE, award_type_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                return 1
        else:
                return 0

def SQLDeletedAwardCategory(award_cat_id):
        SQLlog("SQLDeletedAwardCategory, award_cat_id=%s" % (award_cat_id))
        query = "select 1 from submissions where sub_type = %d and affected_record_id = %d" % (MOD_AWARD_CAT_DELETE, award_cat_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                return 1
        else:
                return 0

def SQLDeletedSeries(series_id):
        SQLlog("SQLDeletedSeries, series_id=%s" % (series_id))
        query = "select 1 from submissions where sub_type = %d and affected_record_id = %d" % (MOD_DELETE_SERIES, series_id)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if CNX.DB_NUMROWS() > 0:
                return 1
        else:
                return 0

def SQLDuplicateImageURL(value):
        SQLlog("SQLDuplicateImageURL, value=%s" % (value))
        CNX = MYSQL_CONNECTOR()
        query = "select * from pubs where pub_frontimage = '%s'" % CNX.DB_ESCAPE_STRING(value)
        return _StandardQuery(query)

def SQLGetSecondaryVerificationByVerID(ver_id):
        SQLlog("SQLGetSecondaryVerificationByVerID, ver_id=%s" % (ver_id))
        query = "select * from verification where verification_id = %d" % int(ver_id)
        return _StandardQuery(query)

def SQLGetSelfApprovers():
        SQLlog("SQLGetSelfApprovers")
        query = """select u.user_id, u.user_name
                from self_approvers sa, mw_user u
                where sa.user_id = u.user_id
                order by u.user_name"""
        return _StandardQuery(query)

def SQLGetWebAPIUsers():
        query = """select u.user_id, u.user_name
                from web_api_users wau, mw_user u
                where wau.user_id = u.user_id
                order by u.user_name"""
        return _StandardQuery(query)

def SQLGetAllAuthorsForPublisher(publisher_id, sort_by):
        SQLlog("SQLGetAllAuthorsForPublisher, publisher_id=%s, sort_by=%s" % (publisher_id, sort_by))
        query = """select a.author_id aid, a.author_canonical, count(a.author_canonical) as cnt
        from authors a, pub_authors pa, pubs p
        where a.author_id = pa.author_id
        and pa.pub_id = p.pub_id
        and p.publisher_id = %d
        group by aid order by """  % int(publisher_id)
        if sort_by == 'count':
                query += 'cnt desc, a.author_lastname'
        else:
                query += 'a.author_lastname, cnt desc'
        return _StandardQuery(query)

def SQLGetPubsForAuthorPublisher(publisher_id, author_id):
        SQLlog("SQLGetPubsForAuthorPublisher, publisher_id=%s, author_id=%s" % (publisher_id, author_id))
        query = """select %s
        from pub_authors pa, pubs p
        where pa.pub_id = p.pub_id
        and p.publisher_id = %d
        and pa.author_id = %d
        order by p.pub_year, p.pub_title"""  % (CNX_PDOT_PUBS_STAR, publisher_id, author_id)
        return _StandardQuery(query)

def SQLFindISBNformat(value):
        query = """select prefix_length, publisher_length from isbn_ranges
                   where start_value <= %d and end_value >= %d""" % (value, value)
        return _OneRow(query)

def SQLFindSimilarPublishers(publisher_id, publisher_name):
        suffixes = ('inc', 'llc', 'books', 'press', 'publisher', 'publishers', 'publishing')
        separators = (' ', ',', ', ')
        post_suffixes = ('', '.')
        prefixes = ('the',)
        exclusions = ('tor publishing', 'ember publishing')

        # Extract the "seed" value from the publisher name
        publisher_seed = publisher_name.lower()
        if publisher_name.endswith('.'):
                publisher_seed = publisher_name[:-1]
        for separator in separators:
                publisher_seed = publisher_seed.replace(separator, '')
        for prefix in prefixes:
                if publisher_seed.startswith(prefix):
                        publisher_seed = publisher_seed[len(prefix):]
        for suffix in suffixes:
                if publisher_seed.endswith(suffix):
                        publisher_seed = publisher_seed[:-len(suffix)]

        query = """select distinct publisher_id, publisher_name from publishers where """

        CNX = MYSQL_CONNECTOR()
        if publisher_id:
                query += "publisher_id != %d and " % int(publisher_id)
        subquery = "TRIM(LEADING 'the' FROM replace(replace(lower(publisher_name), ' ',''), ',',''))"
        for suffix in suffixes:
                subquery = "TRIM(TRAILING '%s' FROM %s" % (CNX.DB_ESCAPE_STRING(suffix), subquery)
        for suffix in suffixes:
                subquery += ')'
        query += " %s = '%s'" % (subquery, CNX.DB_ESCAPE_STRING(publisher_seed))
        for excluded in exclusions:
                query += " and lower(publisher_name) != '%s'" % CNX.DB_ESCAPE_STRING(excluded)
        return _StandardQuery(query)

def SQLGetDbaseTime():
        # Get the update time from a table least likely to have been updated.
        # This is really here to track when the database was updated at isfdb2.org
        SQLlog("SQLGetDbaseTime")
        query = "select UPDATE_TIME from information_schema.tables where TABLE_SCHEMA = 'isfdb' and TABLE_NAME = 'self_approvers'"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        retvalue = record[0][0]
        return retvalue

#################################################################
# This section is executed when the file is imported by another
# file. The try section below is executed. If a successful
# connection to the database is made, the query count is updated
# via a call to SQLUpdateQueries(). If an exception occurs, html
# error code is emitted, and the application exits. Otherwise all
# supported languages are loaded in the global variable LANGUAGES
#################################################################
try:
        if db_connector == db_python2:
                db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=_IsfdbConvSetup())
                db.select_db(DBASE)
                db.set_character_set("latin1")
        elif db_connector == db_python3:
                db = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=DBASEHOST, database=DBASE, charset='latin1')
                db.set_charset_collation('latin1', 'latin1_swedish_ci')
                os.environ['LANG'] = ''
except:
        PrintHTMLHeaders('ISFDB Maintenance')
        print('</div>')
        print('<div id="nav">')
        print('<a href="%s:/%s/index.cgi">' % (PROTOCOL, HTFAKE))
        print('<img src="%s://%s/isfdb.gif" width="90%%" alt="ISFDB logo">' % (PROTOCOL, HTMLLOC))
        print('</a>')
        print('</div>')
        print('<div id="main2">')
        print('<div id="ErrorBox">')
        print("""The ISFDB database is currently unavailable. If this is due to the daily
                backups, check back in a few minutes. If this is unscheduled downtime,
                http://isfdb.blogspot.com/ may have more information.""")
        print('</div>')
        print('</div>')
        print('</div>')
        print('</body>')
        print('</html>')
        sys.exit(0)

SQLUpdateQueries()
LANGUAGES = SQLLoadAllLanguages()
