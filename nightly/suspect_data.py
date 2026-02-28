#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2026   Al von Ruff, Ahasuerus and Dirk Stoecker
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

def suspect_data():
        #   Report 24: Suspect Untitled Awards
        # Ignore Locus awards for years prior to 2011, Aurealis awards for 2008, and Hugo awards for 1964
        # because they are known exceptions due to a single award given to multiple title records
        query = "select a.award_id from awards as a, award_cats as c where c.award_cat_id=a.award_cat_id and \
                 (c.award_cat_name like '%novel%' or c.award_cat_name like '% story%' \
                 or c.award_cat_name like '% book%' or c.award_cat_name like '%collection%' or c.award_cat_name like \
                 '%antholog%' or a.award_title like '%^%') and c.award_cat_name not like '%Traduction%' and \
                 c.award_cat_name not like '%graphic%' and c.award_cat_name not like '%novelist%' and c.award_cat_name \
                 not like '%publisher%' and c.award_cat_name not like '%editor%' and c.award_cat_name not like \
                 '%illustrator%' and a.award_level<100 and not exists(select 1 from title_awards where a.award_id= \
                 title_awards.award_id) and award_author not like '%****%' and award_title!='No Award' and \
                 award_title!='untitled'"
        standardReport(query, 24)

        #   Report 48: Series with Numbering Gaps
        query = """select series_id from titles
                where series_id IS NOT NULL
                and title_seriesnum IS NOT NULL
                and title_seriesnum != 8888
                group by series_id
                having count(title_seriesnum) < (max(title_seriesnum) - min(title_seriesnum) + 1)
                union
                select s.series_id from series s
                where not exists
                        (select 1 from titles t
                        where t.series_id = s.series_id
                        and t.title_seriesnum = 1
                )
                and exists
                         (select 1 from titles t
                         where t.series_id = s.series_id
                         and t.title_seriesnum > 1
                         and t.title_seriesnum < 1800
                )"""
        standardReport(query, 48)

        # Excluded authors are 'uncredited', 'unknown', 'various' and 'The Readers'
        excluded_authors = '2862, 20754, 7311, 25179'
        #   Report 58: Suspected Dutch Authors without a Language Code
        query = """select a.author_id from authors a where a.author_language is null
                   and a.author_id not in (%s)
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and ca.ca_status = 1
                 and t.title_language is not null
                 and t.title_language = 16
                 )>0""" % excluded_authors
        standardReport(query, 58)

        #   Report 59: Suspected French Authors without a Language Code
        query = """select a.author_id from authors a where a.author_language is null
                   and a.author_id not in (%s)
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and ca.ca_status = 1
                 and t.title_language is not null
                 and t.title_language = 22
                 )>0""" % excluded_authors
        standardReport(query, 59)

        #   Report 60: Suspected German Authors without a Language Code
        query = """select a.author_id from authors a where a.author_language is null
                   and a.author_id not in (%s)
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and ca.ca_status = 1
                 and t.title_language is not null
                 and t.title_language = 26
                 )>0""" % excluded_authors
        standardReport(query, 60)

        #   Report 61: Suspected Other Non-English Authors without a Language Code
        query = """select a.author_id from authors a where a.author_language is null
                   and a.author_id not in (%s)
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and ca.ca_status = 1
                 and t.title_language is not null
                 and t.title_language not in (16,17,22,26)
                 )>0""" % excluded_authors
        standardReport(query, 61)

        #   Report 84: Serials with Potentially Unnecessary Disambiguation
        query = """select x.title_id
                from (
                select min(t.title_id) as "title_id",
                substring(t.title_title,1,LOCATE("(", t.title_title)), count(*)
                from titles t
                where t.title_ttype = 'SERIAL'
                and t.title_title like '%(Part % of %)'
                group by substring(t.title_title,1,LOCATE("(", t.title_title))
                having count(*) = 1
                ) x"""
        standardReport(query, 84)

        #   Report 87: Author/title language mismatches
        query = """select distinct t.title_id from titles t,
                canonical_author ca, authors a
                where t.title_id=ca.title_id
                and ca.author_id=a.author_id
                and ca.ca_status=1
                and t.title_parent=0
                and t.title_language is not null
                and a.author_language is not null
                and t.title_language != a.author_language
                and a.author_canonical not in ('uncredited', 'unknown')
                and t.title_ttype in ('NOVEL', 'EDITOR', 'NONFICTION', 'SHORTFICTION')
                """
        standardReport(query, 87)

        #   Report 88: Pubs with multiple COVERART titles
        query = """select p.pub_id from pubs p,
                (select pc.pub_id, count(*)
                from titles t, pub_content pc
                where t.title_id = pc.title_id
                and t.title_ttype='COVERART'
                group by pc.pub_id
                having count(*) > 1) x
                where p.pub_id = x.pub_id"""
        standardReport(query, 88)

        #   Report 144: Series names potentially in need of disambiguation
        query = """select distinct s1.series_id
                   from series s1, series s2
                   where s1.series_id != s2.series_id
                   and s1.series_title = substring(s2.series_title, 1, LOCATE(' (', s2.series_title)-1)
                   and (
                           (s1.series_parent is not null and s1.series_parent != s2.series_id)
                           or (s2.series_parent is not null and s2.series_parent != s1.series_id)
                           or (s1.series_parent is null and s2.series_parent is null)
                        )
                   """
        standardReport(query, 144)

        #   Report 189: Publication series names potentially in need of disambiguation
        query = """select distinct ps1.pub_series_id from pub_series ps1, pub_series ps2
                   where ps1.pub_series_id != ps2.pub_series_id
                   and ps1.pub_series_name = substring(ps2.pub_series_name, 1, LOCATE(' (', ps2.pub_series_name)-1)
                   """
        standardReport(query, 189)

        #   Report 193: Multilingual publications
        query = """select p.pub_id from pubs p, (
                   select distinct pc.pub_id, t.title_language
                   from titles t, pub_content pc
                   where pc.title_id = t.title_id
                   and t.title_language is not null
                   and t.title_language != ''
                   ) x
                   where p.pub_id = x.pub_id
                   group by p.pub_id
                   having count(*) > 1
                   """
        standardReport(query, 193)

        #   Report 233: Potential Duplicate E-book Publications
        query = """select distinct p1.pub_id
                   from titles t, pub_content pc1, pub_content pc2, pubs p1, pubs p2
                   where t.title_id = pc1.title_id
                   and pc1.pubc_id != pc2.pubc_id
                   and pc1.pub_id = p1.pub_id
                   and p1.pub_ptype = 'ebook'
                   and t.title_id = pc2.title_id
                   and p2.pub_ptype = 'ebook'
                   and pc2.pub_id = p2.pub_id
                   and YEAR(p1.pub_year) = YEAR(p2.pub_year)
                   and MONTH(p1.pub_year) = MONTH(p2.pub_year)
                   and (p1.pub_isbn is null or p2.pub_isbn is null or p1.pub_isbn = p2.pub_isbn)
                   and not (p1.pub_catalog is not null and p2.pub_catalog is not null and p1.pub_catalog != p2.pub_catalog)
                   and p1.pub_ctype = p2.pub_ctype
                   and p1.pub_title = p2.pub_title
                   group by t.title_id"""
        standardReport(query, 233)

        #   Report 251: Publications with an OCLC Verification, no ISBN and no OCLC External ID
        query = """select distinct p.pub_id
            from pubs p, verification v, reference r
            where p.pub_id = v.pub_id
            and (p.pub_isbn is null or p.pub_isbn='')
            and v.reference_id = r.reference_id
            and r.reference_label = 'OCLC/Worldcat'
            and v.ver_status = 1
            and not exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'OCLC/WorldCat')"""
        standardReport(query, 251)

        #   Report 252: Publications with an OCLC Verification, no ISBN and no OCLC External ID
        query = """select distinct p.pub_id
            from pubs p, verification v, reference r
            where p.pub_id = v.pub_id
            and p.pub_isbn is not null
            and p.pub_isbn!=''
            and v.reference_id = r.reference_id
            and r.reference_label = 'OCLC/Worldcat'
            and v.ver_status = 1
            and not exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'OCLC/WorldCat')
            order by p.pub_title
            limit 1000"""
        standardReport(query, 252)

        #   Report 277: Publications with the 'Incomplete' Template in Notes
        elapsed = elapsedTime()
        standardDelete(277)
        query = """select p.pub_id,
                IF(p.pub_year='0000-00-00', 0, REPLACE(SUBSTR(p.pub_year, 1,7),'-',''))
                from pubs p, notes n
                where p.note_id = n.note_id
                and n.note_note like '%{{Incomplete}}%'
                """
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        containers = {}
        record = CNX.DB_FETCHMANY()
        while record:
                pub_id = record[0][0]
                pub_month = record[0][1]
                containers[pub_id] = pub_month
                record = CNX.DB_FETCHMANY()
        # Insert the new pub IDs and their months into the cleanup table
        for pub_id in containers:
                update = "insert into cleanup (record_id, report_type, record_id_2) values(%d, 277, %d)" % (int(pub_id), int(containers[pub_id]))
                CNX.DB_QUERY(update)
        elapsed.print_elapsed(277, CNX.DB_NUMROWS())

        #   Report 290: Suspected Ineligible Reviewed NONFICTION Titles (first 1000)
        query = """select distinct t1.title_id
                from titles t1, title_relationships tr, titles t2, pubs p, pub_content pc
                where t1.title_ttype = 'NONFICTION'
                and t1.title_id = tr.title_id
                and t2.title_id = tr.review_id
                and t2.title_ttype = 'REVIEW'
                and t1.title_id = pc.title_id
                and p.pub_id = pc.pub_id
                and not exists (
                        select 1 from cleanup c
                        where c.report_type = 290
                        and c.record_id = t1.title_id
                        and c.resolved is not NULL
                        )
                limit 1000"""
        standardReport(query, 290)

        #   Report 291: Suspected Invalid Uses of the Narrator Template
        query = """select distinct p.pub_id
                from pubs p, notes n
                where p.note_id = n.note_id
                and note_note like '%{{narrator%'
                and p.pub_ptype not like '%audio%'"""
        standardReport(query, 291)

        #   Report 293: Titles with Suspect English Capitalization
        query = """select t.title_id from titles t
                where binary title_title REGEXP "[^\:\.\!\;\/](%s)"
                and t.title_language = 17
                and not exists (
                        select 1 from cleanup c
                        where c.report_type = 293
                        and c.record_id = t.title_id
                        and c.resolved is not NULL
                        )
                limit 1000""" % requiredLowerCase()
        standardReport(query, 293)

        #   Report 294: Publications with Suspect English Capitalization
        query = """select distinct p.pub_id from pubs p
                where binary p.pub_title REGEXP "[^\:\.\!\;\/](%s)"
                and exists (
                        select 1 from titles t, pub_content pc
                        where t.title_id = pc.title_id
                        and p.pub_id = pc.pub_id
                        and t.title_language = 17
                )
                and not exists (
                        select 1 from cleanup c
                        where c.report_type = 294
                        and c.record_id = p.pub_id
                        and c.resolved is not NULL
                        )
                limit 1000""" % requiredLowerCase()
        standardReport(query, 294)

        #   Report 295: Publications with the 'WatchPrePub' Template in Notes
        query = """select p.pub_id
                from pubs p, notes n
                where p.note_id = n.note_id
                and n.note_note like '%{{WatchPrePub|%'"""
        standardReport(query, 295)

        #   Report 301: Reviews Whose Language Doesn't Match the Language of the Reviewed Title
        query = """select r.title_id
                   from titles r, title_relationships tr, titles t
                   where r.title_ttype = 'REVIEW'
                   and r.title_id = tr.review_id
                   and tr.title_id = t.title_id
                   and r.title_language != t.title_language"""
        standardReport(query, 301)

def requiredLowerCase():
        clause = ''
        for word in SESSION.english_lower_case:
                clause += ' %s |' % word.capitalize()
        clause = clause[:-1]
        return clause
