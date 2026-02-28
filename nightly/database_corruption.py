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

def database_corruption():
        #   Report 1: List of titles without authors
        query = """select title_id from titles
                where not exists
                (select title_id from canonical_author
                where canonical_author.title_id=titles.title_id)
                """
        standardReport(query, 1)

        #   Report 9: Variant Titles in Series
        query = "select title_id from titles where series_id IS NOT NULL and series_id !=0 and title_parent !=0"
        standardReport(query, 9)

        #   Report 13: Variant Editor Records in a Series
        query = "select t.* from titles t where t.title_ttype = 'EDITOR' and t.series_id IS NOT NULL and t.title_parent != 0"
        standardReport(query, 13)

        #   Report 14: Missing Editors
        query = "select DISTINCT pu.pub_id from pubs pu, pub_authors pa, authors a \
                where pu.pub_id = pa.pub_id and pa.author_id = a.author_id and a.author_canonical != 'unknown' \
                and pub_ctype in ( 'MAGAZINE', 'FANZINE' ) and not exists (select * from titles t, pub_content pc \
                where pu.pub_id = pc.pub_id and pc.title_id = t.title_id and t.title_ttype = 'EDITOR')"
        standardReport(query, 14)

        #   Report 15: Publications with Multiple EDITOR Records
        query =  "select pc.pub_id from titles t, pub_content pc, pubs p \
                where pc.title_id = t.title_id and pc.pub_id = p.pub_id  and t.title_ttype = 'EDITOR' \
                group by pc.pub_id, p.pub_title HAVING COUNT(*) > 1"
        standardReport(query, 15)

        #   Report 18: Titles with Bad Ellipses
        query = "select title_id from titles where title_title like '%. . .%'"
        standardReport(query, 18)

        #   Report 20: Variant Titles of Variant Titles
        query = "select t.title_id from titles t, titles tp \
                where tp.title_id = t.title_parent and tp.title_parent != 0"
        standardReport(query, 20)

        #   Report 21: Variants of Missing Titles
        query = "select t.title_id from titles t where t.title_parent<>0 and \
                not exists (select 1 from titles pt where t.title_parent=pt.title_id)"
        standardReport(query, 21)

        #   Report 23: Awards Associated with Invalid Titles
        query = "select awards.award_id from awards, title_awards where \
                awards.award_id=title_awards.award_id and not exists \
                (select 1 from titles where titles.title_id=title_awards.title_id)"
        standardReport(query, 23)

        #   Report 27: Series with Chapbooks in them
        query = "select DISTINCT series_id from titles where title_ttype='CHAPBOOK' and series_id != 0"
        standardReport(query, 27)

        #   Report 28: Chapbooks with Synopses
        query = "select title_id from titles where title_ttype='CHAPBOOK' and title_synopsis !=0"
        standardReport(query, 28)

        #   Report 32: Duplicate Publication Tags
        query = "select p1.pub_id from pubs p1, \
                (select pub_tag, count(*) from pubs group by pub_tag having count(*) > 1) p2 \
                where p1.pub_tag = p2.pub_tag"
        standardReport(query, 32)

        #   Report 34: Publications without Titles
        query =  """select pub_id from pubs where not exists
                (select 1 from pub_content pc, titles t
                where pubs.pub_id = pc.pub_id
                and pc.title_id = t.title_id
                and t.title_ttype != 'COVERART')"""
        standardReport(query, 34)

        #   Report 35: Invalid Publication Formats
        formats = "'" + "','".join(SESSION.db.formats) + "'"
        query = "select pub_id from pubs where pub_ptype not in (%s) \
                and pub_ptype IS NOT NULL and pub_ptype!='' \
                order by pub_ptype, pub_title" % (formats)
        standardReport(query, 35)

        #   Report 38: Publications with Duplicate Titles
        query = 'select pub_id from pub_content where pub_id IS NOT NULL group by pub_id, title_id having count(*)>1'
        standardReport(query, 38)

        #   Report 40: Reviews without 'Reviewed authors'
        query = "select title_id from titles where title_ttype='REVIEW' and not exists \
                (select 1 from canonical_author ca where ca.title_id=titles.title_id and ca.ca_status=3)"
        standardReport(query, 40)

        #   Report 43: Identical publishers
        query = "select p1.publisher_id from publishers p1, publishers p2 where \
                p1.publisher_id!=p2.publisher_id and p1.publisher_name=p2.publisher_name \
                group by p1.publisher_name"
        standardReport(query, 43)

        #   Report 46: EDITOR records not in MAGAZINE/FANZINE publications
        query = "select DISTINCT t.title_id from titles t, pubs p, pub_content pc where t.title_ttype='EDITOR' \
                and t.title_id=pc.title_id and p.pub_id=pc.pub_id and p.pub_ctype not in ('MAGAZINE','FANZINE')"
        standardReport(query, 46)

        #   Report 53: Authors with Duplicate Pseudonyms
        query = "select p.author_id \
                from pseudonyms p, authors a1, authors a2 \
                where p.pseudonym = a1.author_id \
                and p.author_id = a2.author_id \
                group by p.author_id, p.pseudonym \
                having count(*) > 1"
        standardReport(query, 53)

        #   Report 62: Titles with Invalid Story Length Values
        # Valid story length values are all values in SESSION.sb.storylen_codes except ''
        valid_values = str(SESSION.db.storylen_codes[1:])
        query = """select title_id from titles
                where (title_storylen is not null
                and title_storylen not in %s)
                or
                (title_storylen in %s
                and title_ttype != 'SHORTFICTION')""" % (valid_values, valid_values)
        standardReport(query, 62)

        #   Report 80: Duplicate SHORTFICTION in Magazines/Fanzines
        query = """select distinct p.pub_id from pubs p, pub_content pc, titles t
                where pc.pub_id = p.pub_id
                and (p.pub_ctype = 'MAGAZINE' or p.pub_ctype = 'FANZINE')
                and pc.title_id = t.title_id and t.title_ttype = 'SHORTFICTION'
                GROUP BY p.pub_id, p.pub_title, t.title_title HAVING count(*) > 1"""
        standardReport(query, 80)

        #   Report 94: Authors Without Titles
        query = """select a.author_id from authors a
                 where (not exists (select 1 from canonical_author ca
                    where ca.author_id = a.author_id)
                 and not exists (select 1 from pub_authors pa
                    where pa.author_id = a.author_id)
                    )
                """
        standardReport(query, 94)

        #   Report 95: Authors with Stray Publications
        query = """select a.author_id from authors a
                 where (not exists (select 1 from canonical_author ca
                    where ca.author_id = a.author_id)
                 and exists (select 1 from pub_authors pa
                    where pa.author_id = a.author_id)
                    )
                """
        standardReport(query, 95)

        #   Report 98: Identical publication series names
        query = """select ps1.pub_series_id from pub_series ps1, pub_series ps2 where
                ps1.pub_series_id != ps2.pub_series_id and ps1.pub_series_name=ps2.pub_series_name
                group by ps1.pub_series_name"""
        standardReport(query, 98)

        #   Report 278-285: Publications with Invalid Title Types
        exclusions = {278: ('ANTHOLOGY', ('CHAPBOOK','NONFICTION','OMNIBUS','EDITOR')),
                      279: ('COLLECTION', ('ANTHOLOGY','CHAPBOOK','NONFICTION','OMNIBUS','EDITOR')),
                      280: ('CHAPBOOK', ('ANTHOLOGY','COLLECTION','NONFICTION','OMNIBUS','EDITOR','NOVEL')),
                      281: ('MAGAZINE', ('CHAPBOOK','NONFICTION','OMNIBUS')),
                      282: ('FANZINE', ('ANTHOLOGY','CHAPBOOK','NONFICTION','OMNIBUS')),
                      283: ('NONFICTION', ('ANTHOLOGY','COLLECTION','EDITOR','NOVEL','OMNIBUS','SERIAL','CHAPBOOK')),
                      284: ('NOVEL', ('ANTHOLOGY','COLLECTION','EDITOR','NONFICTION','OMNIBUS','SERIAL','CHAPBOOK')),
                      285: ('OMNIBUS', ('EDITOR','SERIAL','CHAPBOOK'))
                      }

        for report_id in sorted(exclusions):
                pub_type = exclusions[report_id][0]
                title_list = exclusions[report_id][1]
                title_types = list_to_in_clause(title_list)
                query = """(select p.pub_id from pubs p
                        where p.pub_ctype='%s'
                        and exists
                        (select 1 from pub_content pc, titles t
                        where pc.pub_id=p.pub_id
                        and t.title_id=pc.title_id
                        and t.title_ttype in (%s)))""" % (pub_type, title_types)
                standardReport(query, report_id)

        #   Report 306: Publications with Duplicate Authors
        query = """select pub_id
                from pub_authors
                group by author_id, pub_id
                having count(pub_id) > 1"""
        standardReport(query, 306)

