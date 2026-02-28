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

import sys
if sys.version_info.major == 3:
        PYTHONVER = "python3"
elif sys.version_info.major == 2:
        PYTHONVER = "python2"

from SQLparsing import *
from library import *
from shared_cleanup_lib import *

def nightly_cleanup():
        # Regenerate nightly cleanup reports
        #
        #   Report 2: VT-Pseudonym mismatches
        # Exclude VTs whose author credit is a pseudonym of the parent's author credit
        # Exclude VTs of:
        #    uncredited, unknown, The Editor, Afred Hitchcock, V. C. Andrews
        #    Warren Murphy, Richard Sapir, Bruce Boxleitner, The Editors, Anonymous
        # Exclude VTs whose parent has a credit to the same author.  These cases will be
        # variant where title text is different but author is the same and variant between
        # a single-author credit and a collaboration credit.
        query = "select t.title_id as vt from titles t \
                where t.title_parent is not null and t.title_parent <> 0 \
                and not exists ( \
                  select * from canonical_author vca, canonical_author pca \
                  where vca.title_id = t.title_id and pca.title_id = t.title_parent \
                  and vca.author_id = pca.author_id \
                ) \
                and not exists ( \
                  select * from canonical_author vca, canonical_author pca, pseudonyms p \
                  where vca.title_id = t.title_id and pca.title_id = t.title_parent \
                  and p.pseudonym = vca.author_id and p.author_id = pca.author_id \
                ) \
                and not exists ( \
                  select * from canonical_author vca, canonical_author pca \
                  where vca.title_id = t.title_id and pca.title_id = t.title_parent \
                  and (pca.author_id = 20754 or pca.author_id = 2862 or pca.author_id = 38721 \
                  or vca.author_id = 20754 or vca.author_id = 2862 or vca.author_id = 38721 \
                  or vca.author_id = 7977 or vca.author_id = 1449 or vca.author_id = 1414 \
                  or vca.author_id = 3781 or vca.author_id = 6358 or vca.author_id = 38941 \
                  or pca.author_id = 6677 or vca.author_id = 6677) \
                )"
        standardReport(query, 2)

        #   Report 5: Notes with an odd number of angle brackets
        query = "select note_id, LENGTH(note_note) - LENGTH(REPLACE(note_note, '<', '')) openquote, \
                LENGTH(note_note) - LENGTH(REPLACE(note_note, '>', '')) closequote \
                from notes having openquote != closequote"
        standardReport(query, 5)

        #   Report 6: Authors with invalid Directory Entries
        query = """select author_id from authors
                   where author_lastname like '%&#%'
                   or not hex(author_lastname) regexp '^([0-7][0-9A-F])*$'"""
        standardReport(query, 6)

        #   Report 7: Authors with invalid spaces
        query = """select author_id from authors
                where author_canonical like ' %'
                or author_canonical like '% '
                or author_canonical like '%  %'
                or author_canonical like '%\"%'
                or (
                author_canonical NOT LIKE '%.com'
                and author_canonical NOT LIKE '%.co.uk'
                and """

        suffixes = []
        for suffix in SESSION.recognized_suffixes:
                if suffix.count('.') < 2:
                        continue
                period_letter = 0
                for fragment in suffix.split('.'):
                        if not fragment.startswith(' '):
                                period_letter = 1
                                break
                if period_letter:
                        suffixes.append(suffix)

        subquery = ''
        for suffix in suffixes:
                if not subquery:
                        subquery = """replace(author_canonical, ', %s', '')""" % suffix
                else:
                        subquery = """replace(%s, ', %s', '')""" % (subquery, suffix)

        query += subquery
        query += """ REGEXP '\\\\.[a-z]' = 1)"""
        standardReport(query, 7)

        #   Report 8: Authors that exist only due to reviews
        query =  "select ca.title_id from canonical_author ca, authors a, titles t"
        query += " WHERE ca.ca_status = 3 and ca.author_id = a.author_id and ca.title_id = t.title_id"
        query += " AND NOT EXISTS (SELECT 1 from canonical_author ca2, titles t"
        query += "                 where ca.author_id = ca2.author_id"
        query += "                 AND  ca2.title_id = t.title_id"
        query += "                 AND  t.title_ttype != 'REVIEW'"
        query += "                 and  ca2.ca_status = 1)"
        standardReport(query, 8)

        #   Report 10: Pseudonyms with Canonical Titles
        # First retrieve all pseudonyms on file
        query = 'select distinct(pseudonym) from pseudonyms'
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        pseudos = {}
        record = CNX.DB_FETCHMANY()
        while record:
                pseudo_id = record[0][0]
                # Retrieve the number of canonical titles for this pseudonym
                query2 = 'select count(t.title_id) from canonical_author c, titles t where c.author_id=%s \
                        and c.ca_status=1 and c.title_id=t.title_id and t.title_parent=0' % pseudo_id
                CNX2 = MYSQL_CONNECTOR()
                CNX2.DB_QUERY(query2)
                record2 = CNX2.DB_FETCHONE()
                # If there are canonical titles for this pseudonym, then add it to the list of "problem pseudonyms"
                if record2[0][0] != 0:
                        if PYTHONVER == 'python2':
                                pseudos[unicode(pseudo_id)] = record2[0][0]
                        else:
                                pseudos[str(pseudo_id)] = record2[0][0]
                record = CNX.DB_FETCHMANY()

        if pseudos:
                # Build a pseudo-query to be passed to standardReport()
                query = ''
                for pseudo_id in pseudos:
                        if query:
                                query += ',%s' % pseudo_id
                        else:
                                query = pseudo_id
                query = 'select author_id from authors where author_id in (%s)' % query
                standardReport(query, 10)

        #   Report 11: Prolific Authors without a Defined Language
        # Ignore the following authors: unknown, Anonymous, various, uncredited, The Readers, The Editors, Traditional
        query = 'select c.author_id from canonical_author as c, authors as a \
                where c.author_id=a.author_id and a.author_language IS NULL \
                and a.author_id not in (20754, 7311, 25179, 2862, 38941, 6677, 17640) \
                group by c.author_id order by count(c.author_id) desc limit 300'
        standardReport(query, 11)

        #   Report 12: Editor Records not in a Series
        query = "select title_id from titles where title_ttype = 'EDITOR' and series_id IS NULL and title_parent = 0"
        standardReport(query, 12)

        #   Report 16: Empty Series
        query =  """select series_id from series s1
                    where not exists
                    (select 1 from titles t where t.series_id = s1.series_id)
                    and not exists
                    (select 1 from series s2 where s2.series_parent = s1.series_id)"""
        standardReport(query, 16)

        #   Report 17: Series with Duplicate Series Numbers
        query = """select distinct series_id from titles
                where series_id IS NOT NULL
                and title_seriesnum IS NOT NULL
                group by series_id, title_seriesnum, title_seriesnum_2
                having count(*) >1"""
        standardReport(query, 17)

        #   Report 19: Interviews of Pseudonyms
        query = "select ca.title_id from titles t, canonical_author ca, authors a \
                where t.title_ttype = 'INTERVIEW' and ca.title_id = t.title_id \
                and ca.author_id = a.author_id and ca.ca_status = 2 \
                and a.author_canonical != 'uncredited' and exists \
                (select 1 from pseudonyms p where a.author_id = p.pseudonym)"
        standardReport(query, 19)

        #   Report 22: SERIALs without a Parent Title
        query = "select title_id from titles where title_ttype='SERIAL' and title_parent=0"
        standardReport(query, 22)

        #   Report 25: Empty Award Types
        query = 'select award_type_id from award_types where NOT EXISTS \
                (select 1 from awards where awards.award_type_id=award_types.award_type_id)'
        standardReport(query, 25)

        #   Report 26: Empty Award categories
        query = 'select award_cat_id from award_cats where NOT EXISTS \
                (select 1 from awards where awards.award_cat_id=award_cats.award_cat_id)'
        standardReport(query, 26)

        #   Report 30: Chapbooks with Mismatched Variant Types
        query = "select t1.title_id from titles t1, titles t2 where t1.title_ttype='CHAPBOOK' \
                and t2.title_parent=t1.title_id and t2.title_ttype!='CHAPBOOK' \
                UNION select t1.title_id from titles t1, titles t2 where t1.title_ttype!='CHAPBOOK' \
                and t2.title_parent=t1.title_id and t2.title_ttype='CHAPBOOK'"
        standardReport(query, 30)

        #   Report 31: Pre-2005 pubs with ISBN-13s and post-2007 pubs with ISBN-10s
        query = """select pub_id from pubs
                where (pub_isbn like '97%'
                and length(replace(pub_isbn,'-',''))=13
                and pub_year<'2005-00-00'
                and pub_year !='0000-00-00')
                or
                (length(replace(pub_isbn,'-',''))=10
                and pub_year>'2008-00-00'
                and pub_year !='8888-00-00'
                and pub_year !='9999-00-00')"""
        standardReport(query, 31)

        #   Report 33: Publication Authors that are not the Title Author
        query = """select distinct p.pub_id
                from pub_authors pa, pubs p, pub_content pc, titles t, authors a
                where pa.pub_id = p.pub_id
                and pa.author_id = a.author_id
                and pc.title_id = t.title_id
                and pc.pub_id = p.pub_id
                and p.pub_ctype in ('ANTHOLOGY','NOVEL','COLLECTION','NONFICTION','OMNIBUS','CHAPBOOK')
                and t.title_ttype in ('ANTHOLOGY','NOVEL','COLLECTION','OMNIBUS','NONFICTION','CHAPBOOK')
                and t.title_ttype = p.pub_ctype
                and not exists (select 1 from canonical_author ca
                where ca.title_id = t.title_id and pa.author_id = ca.author_id)
                UNION
                select distinct p.pub_id
                from pub_authors pa, pubs p, pub_content pc, titles t, authors a
                where pa.pub_id = p.pub_id
                and pa.author_id = a.author_id
                and pc.title_id = t.title_id
                and pc.pub_id = p.pub_id
                and p.pub_ctype in ('FANZINE','MAGAZINE')
                and t.title_ttype = 'EDITOR'
                and t.title_language != 26
                and not exists (select 1 from canonical_author ca
                where ca.title_id = t.title_id and ca.author_id = pa.author_id)"""
        standardReport(query, 33)

        #   Report 36: Images Which We Don't Have Permission to Link to
        query = BuildRecognizedDomainsQuery('pubs', 'pub_id', 'pub_frontimage')
        standardReport(query, 36)

        #   Report 39: Publications with Bad Ellipses
        query = "select pub_id from pubs where pub_title like '%. . .%'"
        standardReport(query, 39)

        #   Report 41: Reviews not Linked to Titles
        query = """select t1.title_id from titles t1 where title_ttype='REVIEW'
                and not exists (select 1 from title_relationships tr where tr.review_id=t1.title_id)
                and not exists (select 1 from titles t2 where t2.title_parent=t1.title_id)"""
        standardReport(query, 41)

        #   Report 42: Reviews of uncommon title types
        query = "select t1.title_id from titles t1 where t1.title_ttype='REVIEW' and exists \
                (select 1 from title_relationships tr, titles t2 where t1.title_id=tr.review_id \
                and t2.title_id=tr.title_id and t2.title_ttype in \
                ('CHAPBOOK', 'COVERART', 'INTERIORART', 'INTERVIEW', 'REVIEW'))"
        standardReport(query, 42)

        #   Report 44: Similar publishers
        elapsed = elapsedTime()
        standardDelete(44)
        suffixes = ('Inc', 'LLC', 'Books', 'Press', 'Publisher', 'Publishers', 'Publishing')
        separators = (' ', ',', ', ')
        post_suffixes = ('', '.')
        query = """select distinct p1.publisher_id, p2.publisher_id
                from publishers p1, publishers p2 where
                p1.publisher_id != p2.publisher_id
                and p1.publisher_name != p2.publisher_name
                and p1.publisher_name = replace(replace(p2.publisher_name, ' ',''), '/', '')
                UNION
                select distinct p1.publisher_id, p2.publisher_id
                from publishers p1, publishers p2 where
                p1.publisher_id != p2.publisher_id
                and p1.publisher_name != p2.publisher_name
                and substr(p2.publisher_name,1,4) = 'The '
                and p1.publisher_name=substr(p2.publisher_name,5,999)"""

        for separator in separators:
                for suffix in suffixes:
                        for post_suffix in post_suffixes:
                                full_suffix = separator + suffix + post_suffix
                                query += """ UNION
                                            select distinct p1.publisher_id, p2.publisher_id
                                            from publishers p1, publishers p2
                                            where p1.publisher_id != p2.publisher_id
                                            and p1.publisher_name != p2.publisher_name
                                            and p1.publisher_name = substr(p2.publisher_name,1,length(p2.publisher_name)-%d)
                                            and substr(p2.publisher_name,length(p2.publisher_name)-%d, 999) = '%s'
                                            """ % (len(full_suffix), len(full_suffix)-1, full_suffix)
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        while record:
                publisher_id1 = int(record[0][0])
                publisher_id2 = int(record[0][1])
                query2 = """select 1 from cleanup where report_type=44
                        and ((record_id=%d and record_id_2=%d)
                        or (record_id=%d and record_id_2=%d))
                        """ % (publisher_id1, publisher_id2, publisher_id2, publisher_id1)
                CNX2 = MYSQL_CONNECTOR()
                CNX2.DB_QUERY(query2)
                # Only add to the cleanup table if this publisher pair isn't in "cleanup"
                if not CNX2.DB_NUMROWS():
                        update = """insert into cleanup (record_id, report_type, record_id_2)
                        values(%d, 44, %d)""" % (publisher_id1, publisher_id2)
                        CNX2.DB_QUERY(update)
                record = CNX.DB_FETCHMANY()
        elapsed.print_elapsed(44, CNX.DB_NUMROWS())

        #   Report 45: Variant Title Type Mismatches
        query = """select v.title_id from titles v, titles p
                where v.title_parent > 0
                and v.title_parent=p.title_id
                and v.title_ttype!=p.title_ttype
                and not (v.title_ttype='SERIAL' and p.title_ttype in ('NOVEL', 'SHORTFICTION', 'COLLECTION'))
                and not (v.title_ttype='INTERIORART' and p.title_ttype='COVERART')
                and not (v.title_ttype='COVERART' and p.title_ttype='INTERIORART')"""
        standardReport(query, 45)

        #   Report 47: Title Dates after Publication Dates
        query = """select distinct t.title_id from titles t, pubs p, pub_content pc
                where pc.title_id = t.title_id
                and pc.pub_id = p.pub_id
                and p.pub_year != '0000-00-00'
                and p.pub_year != '8888-00-00'
                and t.title_copyright != '0000-00-00'
                and t.title_copyright != '0000-00-00'
                and
                (
                        YEAR(t.title_copyright) > YEAR(p.pub_year)
                or
                        (
                                YEAR(p.pub_year) = YEAR(t.title_copyright)
                                and MONTH(p.pub_year) != '00'
                                and MONTH(t.title_copyright) > MONTH(p.pub_year)
                        )
                or
                        (
                                YEAR(p.pub_year) = YEAR(t.title_copyright)
                                and MONTH(p.pub_year) = MONTH(t.title_copyright)
                                and MONTH(p.pub_year) != '00'
                                and DAY(p.pub_year) != '00'
                                and DAY(t.title_copyright) > DAY(p.pub_year)
                        )
                )
                limit 1000"""
        standardReport(query, 47)

        #   Report 49: Publications with Invalid ISBN Formats
        query = """select p.pub_id from pubs p
                where p.pub_isbn is not NULL
                and p.pub_isbn != ''
                and
                (
                     (
                     REPLACE(p.pub_isbn,'-','') not REGEXP '^[[:digit:]]{9}[Xx]{1}$'
                     and REPLACE(p.pub_isbn,'-','') not REGEXP '^[[:digit:]]{10}$'
                     and REPLACE(p.pub_isbn,'-','') not REGEXP '^[[:digit:]]{13}$'
                     )
                     or
                     (
                     REPLACE(p.pub_isbn,'-','') REGEXP '^[[:digit:]]{13}$'
                     and LEFT(REPLACE(p.pub_isbn,'-',''), 3) != '978'
                     and LEFT(REPLACE(p.pub_isbn,'-',''), 3) != '979'
                     )
                )
                """
        standardReport(query, 49)

        #   Report 50: Publications with Invalid ISBN Checksums
        query = "(select tmp.pub_id from \
                 (select pub_id, REPLACE(pub_isbn,'-','') AS isbn \
                 from pubs \
                 where LENGTH(REPLACE(pub_isbn,'-',''))=10) tmp \
                 where CONVERT((11-MOD( \
                 (substr(isbn,1,1)*10) \
                +(substr(isbn,2,1)*9) \
                +(substr(isbn,3,1)*8) \
                +(substr(isbn,4,1)*7) \
                +(substr(isbn,5,1)*6) \
                +(substr(isbn,6,1)*5) \
                +(substr(isbn,7,1)*4) \
                +(substr(isbn,8,1)*3) \
                +(substr(isbn,9,1)*2) \
                , 11)),CHAR) \
                 != REPLACE(REPLACE(SUBSTR(tmp.isbn,10,1),0,11),'X',10)) \
                union \
                (select tmp.pub_id from \
                 (select pub_id, REPLACE(pub_isbn,'-','') AS isbn \
                 from pubs \
                 where LENGTH(REPLACE(pub_isbn,'-',''))=13) tmp \
                 where MOD(10-MOD( \
                 (substr(isbn,1,1)*1) \
                +(substr(isbn,2,1)*3) \
                +(substr(isbn,3,1)*1) \
                +(substr(isbn,4,1)*3) \
                +(substr(isbn,5,1)*1) \
                +(substr(isbn,6,1)*3) \
                +(substr(isbn,7,1)*1) \
                +(substr(isbn,8,1)*3) \
                +(substr(isbn,9,1)*1) \
                +(substr(isbn,10,1)*3) \
                +(substr(isbn,11,1)*1) \
                +(substr(isbn,12,1)*3) \
                ,10),10) \
                 != SUBSTR(isbn,13,1))"
        standardReport(query, 50)

        #   Report 51: Publications with Identical ISBNs and Different Titles
        # Note that we have to store publication IDs rather than ISBNs in the
        # "cleanup" table because ISBNs can be non-numeric and the record_id
        # column can only store integers
        query = """select record_id from cleanup where
                report_type=51 and resolved IS NOT NULL"""
        CNX.DB_QUERY(query)
        resolved_ids = []
        record = CNX.DB_FETCHMANY()
        while record:
                resolved_ids.append(str(record[0][0]))
                record = CNX.DB_FETCHMANY()
        resolved_string = "','".join(resolved_ids)

        query = """select pub_isbn
                from pubs
                where pub_isbn IS NOT NULL
                and pub_isbn != ''
                and pub_ctype != 'MAGAZINE'
                and pub_id not in ('%s')
                group by pub_isbn
                having count(distinct(REPLACE(pub_title,'-',''))) > 1
                AND INSTR(MIN(pub_title), MAX(pub_title)) = 0
                AND INSTR(MAX(pub_title), MIN(pub_title)) = 0""" % resolved_string
        CNX.DB_QUERY(query)
        isbns = []
        record = CNX.DB_FETCHMANY()
        while record:
                isbns.append(str(record[0][0]))
                record = CNX.DB_FETCHMANY()

        # Only run the report if there are matching ISBNs; if the 'isbns; list is empty,
        # then running this report would display thousands of pubs with empty ISBN values
        if isbns:
                isbns_string = "','".join(isbns)
                query = "select distinct pub_id from pubs where pub_isbn in ('%s')" % isbns_string
                standardReport(query, 51)

        #   Report 57: Invalid SFE image links
        query = """select pub_id from pubs
                   where (pub_frontimage like '%sf-encyclopedia.uk%' or pub_frontimage like '%sf-encyclopedia.com%')
                   and pub_frontimage not like '%/clute/%'
                   and pub_frontimage not like '%/clute_uk/%'
                   and pub_frontimage not like '%/langford/%'
                   and pub_frontimage not like '%/robinson/%'"""
        standardReport(query, 57)

        #   Report 63: Non-genre/genre VT mismatches
        query = """select distinct t1.title_id from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and t1.title_non_genre != t2.title_non_genre
                """
        standardReport(query, 63)

        #   Report 64: Series with a mix of EDITOR and non-EDITOR titles
        query = """select s.series_id from series s
                 where exists(select 1 from titles t where t.series_id = s.series_id and t.title_ttype = 'EDITOR')
                 and exists(select 1 from titles t where t.series_id = s.series_id and t.title_ttype != 'EDITOR')"""
        standardReport(query, 64)

        #   Report 71: Forthcoming Titles: 9999-00-00 and more than 3 months out
        query = """select title_id from titles where title_copyright >
                DATE_ADD(NOW(), INTERVAL 3 MONTH)
                and title_copyright != '8888-00-00'"""
        standardReport(query, 71)

        #   Report 72: Forthcoming (9999-00-00) Publications
        query = """select pub_id from pubs where pub_year >
                DATE_ADD(NOW(), INTERVAL 3 MONTH)
                and pub_year != '8888-00-00'"""
        standardReport(query, 72)

        #   Report 79: NOVEL publications with fewer than 80 pages
        query = """select pub_id from pubs
                where
                (
                  (REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(pub_pages,'[',''),']',''),'+',''),'v',''),'i',''),'x','') < 80
                  and pub_pages!='' and pub_pages!='0'
                  and pub_pages not like '%+%')
                or
                  (pub_pages like '%+%' and pub_pages not REGEXP '[[:digit:]]{3}')
                )
                and pub_ctype='NOVEL'"""
        standardReport(query, 79)

        #   Report 81: Series with Slashes and no Spaces
        query = """select series_id from series
                where series_title like '%/%'
                and series_title not like '% / %'"""
        standardReport(query, 81)

        #   Report 82: Invalid Record URLs in Notes
        query = """select note_id, note_note from notes
                where note_note like '%isfdb.org%'"""
        CNX.DB_QUERY(query)
        problems = []
        notes = {}
        pub_tag_notes = {}
        ignored_scripts = ('se', 'note')
        scripts = {'title': ('titles', 'title_id'),
                   'pl': ('pubs', 'pub_id'),
                   'ea': ('authors', 'author_id'),
                   'publisher': ('publishers', 'publisher_id'),
                   'pubseries': ('pub_series', 'pub_series_id'),
                   'pe': ('series', 'series_id'),
                   'seriesgrid': ('series', 'series_id'),
                   'ay': ('award_types', 'award_type_id'),
                   'awardtype': ('award_types', 'award_type_id'),
                   'award_details': ('awards', 'award_id'),
                   'award_category': ('award_cats', 'award_cat_id'),
                   'publisheryear': ('publishers', 'publisher_id')
                   }
        for script in scripts:
                notes[script] = {}
        pub_tag_notes[script] = {}
        record = CNX.DB_FETCHMANY()
        while record:
                note_id = record[0][0]
                note_body = record[0][1].lower()
                link_list = note_body.split("isfdb.org/cgi-bin/")
                for link in link_list:
                        if ".cgi?" not in link:
                                continue
                        split_link = link.split('.cgi?')
                        if len(split_link) != 2:
                                continue
                        script = split_link[0]
                        if script in ignored_scripts:
                                continue
                        record_id = split_link[1]
                        # If the record ID is followed by a double quote, strip everything to the right of the ID
                        if '"' in record_id:
                                record_id = record_id.split('"')[0]
                        # If the record ID is followed by a single quote, strip everything to the right of the ID
                        if "'" in record_id:
                                record_id = record_id.split("'")[0]
                        # If the record ID is followed by a plus sign, strip everything to the right of the ID
                        if '+' in record_id:
                                record_id = record_id.split('+')[0]
                        # If the script is not one of the recognized script types, report it
                        if script not in scripts:
                                if note_id not in problems:
                                        problems.append(note_id)
                                continue
                        # For numeric record IDs, add them to the main record list and continue the loop
                        if record_id.isdigit():
                                if record_id not in notes[script]:
                                        notes[script][record_id] = []
                                notes[script][record_id].append(note_id)
                                continue
                        # If the record ID is not numeric and it's not a Publication record, it is bad
                        if script != 'pl':
                                if note_id not in problems:
                                        problems.append(note_id)
                                continue
                        # For publication records, record IDs may also be alphanumeric tags, but
                        # if the string contains punctuation, then it is not a valid ID or tag
                        if not record_id.isalnum():
                                if note_id not in problems:
                                        problems.append(note_id)
                                continue
                        # Otherwise this is a publication tag, so we add it to a special list of tag notes
                        if record_id not in pub_tag_notes:
                                pub_tag_notes[record_id] = []
                        pub_tag_notes[record_id].append(note_id)

                record = CNX.DB_FETCHMANY()

        for script in notes:
                if notes[script]:
                        in_clause = ''
                        for record_id in notes[script]:
                                if in_clause:
                                        in_clause += ", "
                                in_clause += "'%s'" % str(record_id)
                        table_name = scripts[script][0]
                        field_name = scripts[script][1]
                        query = """select %s from %s where %s in (%s)""" % (field_name, table_name, field_name, in_clause)
                        CNX.DB_QUERY(query)
                        record = CNX.DB_FETCHMANY()
                        while record:
                                existing_id = str(record[0][0])
                                del notes[script][existing_id]
                                record = CNX.DB_FETCHMANY()
                        for record_id in notes[script]:
                                for note_id in notes[script][record_id]:
                                        if note_id not in problems:
                                                problems.append(note_id)

        if pub_tag_notes:
                in_clause = ''
                for record_id in pub_tag_notes:
                        if in_clause:
                                in_clause += ", "
                        in_clause += "'%s'" % str(record_id)
                query = """select pub_tag from pubs where pub_tag in (%s)""" % in_clause
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        existing_tag = record[0][0].lower()
                        del pub_tag_notes[existing_tag]
                        record = CNX.DB_FETCHMANY()
                for record_id in pub_tag_notes:
                        for note_id in pub_tag_notes[record_id]:
                                if note_id not in problems:
                                        problems.append(note_id)

        in_clause = ''
        for problem in problems:
                if in_clause:
                        in_clause += ", "
                in_clause += str(problem)
        if in_clause:
                query = "select note_id from notes where note_id in (%s)" % in_clause
                standardReport(query, 82)

        #   Report 83: Serials without parenthetical disambiguations
        query = """select title_id from titles where
                (title_title not like '%(Complete Novel)')
                and (title_title not like '%(Part % of %)')
                and title_ttype='SERIAL'"""
        standardReport(query, 83)

        #   Report 86: Primary-verified pubs with "unknown" format
        query = """select distinct p.pub_id
                from pubs p, primary_verifications pv
                where p.pub_id = pv.pub_id
                and p.pub_ptype = 'unknown'"""
        standardReport(query, 86)

        #   Report 89: Authors with Invalid Birthplaces
        query = """select author_id from authors
                where
                (author_birthplace like '%, US')
                or
                  (author_birthplace like "%England%"
                  and author_birthplace not like "%Kingdom of England"
                  and author_birthplace not like "%England, Kingdom of Great Britain"
                  and author_birthplace not like "%England, UK")
                or
                  (author_birthplace like "%Scotland%"
                  and author_birthplace not like "%Kingdom of Scotland"
                  and author_birthplace not like "%Scotland, Kingdom of Great Britain"
                  and author_birthplace not like "%Scotland, UK")
                or
                  (YEAR(author_birthdate) <1801 and YEAR(author_birthdate) != '0000'
                  and author_birthplace like '%, UK')
                or (author_birthplace like '%United Kingdom')
                or
                  (YEAR(author_birthdate) < 1917 and YEAR(author_birthdate) != '0000'
                  and
                    (author_birthplace like '%, Russia%'
                    or
                    author_birthplace like '%, Ukraine%')
                  and author_birthplace not like '%Russian Empire')
                or
                  (YEAR(author_birthdate) > 1922 and YEAR(author_birthdate) < 1992
                  and YEAR(author_birthdate) != '0000'
                  and author_birthplace like '%, Russia%'
                  and author_birthplace not like '%, USSR')
                or
                  (YEAR(author_birthdate) < 1923 and YEAR(author_birthdate) != '0000'
                  and author_birthplace like '%, USSR')
                or
                  (YEAR(author_birthdate) > 1991 and author_birthplace like '%, USSR')
                or
                  (author_birthplace like '%Russian Federation%')
                """
        british_provinces = ('Connecticut',
                             'Delaware',
                             'Maryland',
                             'Massachusetts',
                             'New Hampshire',
                             'New Jersey',
                             'New York',
                             'North Carolina',
                             'Pennsylvania',
                             'Rhode Island',
                             'South Carolina',
                             'Virginia')
        for province in british_provinces:
                query += """ or (author_birthplace like '%%%s%%'
                                and author_birthplace not like '%%, USA'
                                and author_birthplace not like '%%, British Empire')
                         """ % province
        # 'Georgia' can be either:
        # 1. a British province which became a US state, or
        # 2. a country that was a part of the Russian Empire in 1801-1971 and the USSR in 1922-1991
        query += """ or (author_birthplace like '%Georgia%'
                         and author_birthplace not like '%, USA'
                         and author_birthplace not like '%, British Empire'
                         and author_birthplace not like '%, USSR'
                         and author_birthplace not like '%, Russian Empire'
                         and author_birthplace not like '%, Georgia')"""

        # 'California' can be either a US state or 'Baja California', a Mexican state
        query += """ or (author_birthplace like '%California%'
                         and author_birthplace not like '%, USA'
                         and author_birthplace not like '%Baja California%')"""

        # 'Maine' can be either a US state or a French town or a French province or an Australian city
        query += """ or (author_birthplace like '%Maine%'
                    and author_birthplace not like '%, USA'
                    and author_birthplace not like '%Maine-et-Loire%'
                    and author_birthplace not like '%Domaine de la Devi%'
                    and author_birthplace not like '%Castlemaine%'
                    and author_birthplace not like '%Chalons-du-Maine%')"""

        # 'Hawaii' can be a US state or an independent kingdom or an independent republic
        query += """ or (author_birthplace like '%Hawaii%'
                    and author_birthplace not like '%, USA'
                    and author_birthplace not like '%Kingdom of Hawaii'
                    and author_birthplace not like '%Republic of Hawaii')"""

        # 'Montana' can be a US state or a town in Bulgaria
        query += """ or (author_birthplace like '%Montana%'
                    and author_birthplace not like '%, USA'
                    and author_birthplace not like '%, Bulgaria')"""

        # 'Florida' can be a US state, a town in the state of Missouri (USA) or a municipality in Brazil
        query += """ or (author_birthplace like '%Florida%'
                    and author_birthplace not like '%, USA'
                    and author_birthplace not like '%, Brazil')"""

        other_us_states = ('Alabama',
                           'Alaska',
                           'Arizona',
                           'Arkansas',
                           'Colorado',
                           'Idaho',
                           'Illinois',
                           'Indiana',
                           'Iowa',
                           'Kansas',
                           'Kentucky',
                           'Louisiana',
                           'Michigan',
                           'Minnesota',
                           'Mississippi',
                           'Missouri',
                           'Nebraska',
                           'Nevada',
                           'New Mexico',
                           'North Dakota',
                           'Ohio',
                           'Oklahoma',
                           'Oregon',
                           'South Dakota',
                           'Tennessee',
                           'Texas',
                           'Utah',
                           'Vermont',
                           'Washington',
                           'West Virginia',
                           'Wisconsin',
                           'Wyoming')

        for us_state in other_us_states:
                query += """ or (author_birthplace like '%%%s%%'
                                and author_birthplace not like '%%, USA')""" % us_state

        standardReport(query, 89)

        #   Report 90: Duplicate sub-series numbers within a series
        query = """select series_id from series
                where series_parent_position is not null
                group by series_parent, series_parent_position
                having count(*) >1
                """
        standardReport(query, 90)

        #   Report 91: Non-Art Titles by Non-English Authors without a Language
        query = """select distinct t.title_id from authors a, titles t, canonical_author ca
                   where a.author_language != 17
                   and a.author_language is not null
                   and a.author_id = ca.author_id
                   and ca.title_id = t.title_id
                   and ca.ca_status = 1
                   and t.title_ttype not in ('COVERART', 'INTERIORART')
                   and t.title_language is null
                """
        standardReport(query, 91)

        #   Report 93: Publication Title/Reference Title Mismatches
        query = """select distinct p.pub_id
          from pubs p
          where p.pub_ctype in ('CHAPBOOK', 'OMNIBUS', 'ANTHOLOGY', 'COLLECTION', 'NONFICTION', 'NOVEL')
          and not exists
           (select 1 from titles t, pub_content pc
           where p.pub_id = pc.pub_id
           and pc.title_id = t.title_id
           and t.title_ttype = p.pub_ctype
           and p.pub_title = t.title_title
           )
           limit 1000"""
        standardReport(query, 93)

        #   Report 96: COVERART titles with a "Cover:" prefix
        query = """select title_id from titles
                   where title_ttype = 'COVERART'
                   and title_title like 'Cover:%'
                   UNION
                   select tt.title_id from trans_titles tt, titles t
                   where trans_title_title like 'Cover:%'
                   and tt.title_id = t.title_id
                   and t.title_ttype = 'COVERART'"""
        standardReport(query, 96)

        #   Report 100: Invalid prices
        query = """select pub_id from pubs
                where pub_price like '%$ %'
                or pub_price like concat('%',CHAR(0xA3),' ','%')
                or pub_price like concat('%',CHAR(0xA5),' ','%')
                or pub_price like concat('%',CHAR(0x80),'%',' ','%')
                or pub_price like concat('%','_',CHAR(0x80),'%')
                or pub_price like concat('%',CHAR(0x80),'%',',','%')
                or pub_price like '%CDN%'
                or pub_price like '%EUR%'
                or (pub_price like '$%,%'
                        and pub_price not like '$%.%')
                or (pub_price like 'C$%,%'
                        and pub_price not like 'C$%.%')
                or (pub_price like concat(CHAR(0xA3),'%',',','%')
                        and pub_price not like concat(CHAR(0xA3),'%',".",'%'))
                or pub_price regexp '^[[:digit:]]{1,}[,.]{0,}[[:digit:]]{0,}$'
                or (pub_price regexp '[.]{1}[[:digit:]]{3,}'
                        and pub_price not like 'BD %'
                        and pub_price not like '$0.__5'
                        and pub_price not like concat(CHAR(0xA3),'0.__5'))
                or (pub_price regexp '^[[:digit:]]{1,}'
                        and pub_price not like '%/%')
                or pub_price regexp '[[:digit:]]{4,}$'
                or pub_price like 'http%'
                or pub_price like '%&#20870;%'
                or pub_price like '%JP%'
                or pub_price like '% % %'
                or pub_price like '% $%'
                or pub_price like '%+%'
                or pub_price regexp '[[:digit:]]{1,} '
                """
        standardReport(query, 100)

        #   Report 190: Awards with Invalid IMDB Links
        query = """select award_id from awards
                   where award_movie is not NULL
                   and award_movie != ''
                   and SUBSTRING(award_movie, 1, 2) != 'tt'
                   """
        standardReport(query, 190)

        #   Report 191: Invalid hrefs in notes
        query = """select note_id from notes
                where REPLACE(note_note, ' ', '') like '%<ahref=""%'
                or REPLACE(note_note, ' ', '') regexp 'ahref=http'
                or REPLACE(note_note, ' ', '') regexp 'ahref="http{1}[^\"\>]{1,}>'
                or REPLACE(note_note, ' ', '') regexp 'ahref="http{1}[^\"\>]{1,}"">'"""
        standardReport(query, 191)

        #   Report 192: Authors without a Working Language
        query = """select author_id from authors
                   where author_language is null
                   and substring(author_lastname,1,1) > 'V'
                """
        standardReport(query, 192)

        #   Report 194: Titles without a language
        query = "select title_id from titles where title_language is null"
        standardReport(query, 194)

        #   Report 195: Invalid Title Content values
        query = """select title_id from titles
                   where (title_ttype != 'OMNIBUS' and title_content is not null)
                   or SUBSTRING(title_content,1,1) = '/'
                """
        standardReport(query, 195)

        #   Report 196: Juvenile VT mismatches
        query = """select distinct t1.title_id from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and t1.title_jvn != t2.title_jvn
                """
        standardReport(query, 196)

        #   Report 197: Novelization VT mismatches
        query = """select distinct t1.title_id from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and t1.title_nvz != t2.title_nvz
                """
        standardReport(query, 197)

        #   Report 198: Author-pseudonym language mismatches
        query = """select distinct a2.author_id
                from authors a1, authors a2, pseudonyms p
                where a1.author_id = p.author_id
                and p.pseudonym = a2.author_id
                and (
                        (a1.author_language != a2.author_language)
                        or (a1.author_language is NULL and a2.author_language is not null)
                        or (a1.author_language is not NULL and a2.author_language is null)
                )
                """
        standardReport(query, 198)

        #   Report 227: Titles with mismatched parentheses
        query = """select title_id,
                LENGTH(REPLACE(title_title, ')', '')) - LENGTH(REPLACE(title_title, '(', '')) as cnt
                from titles having cnt != 0"""
        standardReport(query, 227)

        #   Report 228: E-books without ASINs
        # Ignore Project Gutenberg publications
        query = """select p.pub_id from pubs p, publishers pb
                where p.pub_isbn is null
                and p.publisher_id = pb.publisher_id
                and pb.publisher_name not like '%Project Gutenberg%'
                and p.pub_ptype = 'ebook'
                and p.pub_ctype not in ('FANZINE','MAGAZINE')
                and not exists(
                         select 1 from identifiers
                         where identifier_type_id = 1 and pub_id = p.pub_id)"""
        standardReport(query, 228)

        #   Report 231: Missing Required Web Pages for Cover Images
        query = "select pub_id from pubs where pub_frontimage not like '%|%' and ("
        for domain in SQLLoadRecognizedDomains():
                if domain[DOMAIN_EXPLICIT_LINK_REQUIRED]:
                        query += "pub_frontimage like '%%%s/%%' or " % domain[DOMAIN_NAME]
        query = '%s)' % query [:-4]
        standardReport(query, 231)

        #   Report 232: Award Years with Month/Day Data
        query = "select award_id from awards where award_year not like '%-00-00'"
        standardReport(query, 232)

        #   Report 235: Publications with invalid BNF identifiers
        query = """select distinct p.pub_id from pubs p, identifiers i
                 where p.pub_id = i.pub_id
                 and i.identifier_type_id = 4
                 and i.identifier_value not regexp '^cb[[:digit:]]{8}[[:alnum:]]{1}$'"""
        standardReport(query, 235)

        #   Report 236: SFBC publications with an ISBN and no catalog ID
        query = """select distinct p.pub_id from pubs p, publishers pu
                 where p.publisher_id = pu.publisher_id
                 and (pu.publisher_name like '%SFBC%'
                      or pu.publisher_name = 'Science Fiction Book Club')
                 and p.pub_isbn is not NULL and p.pub_isbn != ""
                 and p.pub_catalog is NULL"""
        standardReport(query, 236)

        #   Report 242: CHAPBOOK/SHORTFICTION Juvenile Flag Mismatches
        query = """select distinct t1.title_id
                from titles t1, titles t2, pub_content pc1, pub_content pc2
                where t1.title_id = pc1.title_id
                and pc1.pub_id = pc2.pub_id
                and pc2.title_id = t2.title_id
                and t1.title_ttype = 'CHAPBOOK'
                and t2.title_ttype = 'SHORTFICTION'
                and t1.title_jvn != t2.title_jvn"""
        standardReport(query, 242)

        #   Report 244: Publications with Invalid Non-numeric External IDs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and
                (
                (it.identifier_type_name in
                ('Biblioman', 'BL', 'Bleiler Early Years', 'Bleiler Gernsback',
                'COBISS.BG', 'COBISS.SR', 'COPAC (defunct)', 'FantLab',
                'Goodreads', 'JNB/JPNO', 'KBR', 'Libris', 'LTF', 'NILF', 'NLA',
                'OCLC/WorldCat', 'PORBASE', 'SF-Leihbuch')
                and i.identifier_value not regexp '^[[:digit:]]{1,30}$')
                or
                (it.identifier_type_name in ('DNB', 'PPN')
                and i.identifier_value not regexp '^[[:digit:]]{1,30}[Xx]{0,1}$')
                or
                (it.identifier_type_name = 'NDL'
                and i.identifier_value not regexp '^[b]{0,1}[[:digit:]]{1,30}$')
                or
                (it.identifier_type_name in ('Reginald-1', 'Reginald-3', 'Bleiler Supernatural')
                and i.identifier_value not regexp '^[[:digit:]]{1,6}[[:alpha:]]{0,1}$')
                or
                (it.identifier_type_name = 'NooSFere'
                and i.identifier_value not regexp '^[-]{0,1}[[:digit:]]{1,30}$')
                )
                """
        standardReport(query, 244)

        #   Report 245: Publications with non-standard ASINs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and (
                        (
                                it.identifier_type_name = 'ASIN'
                                and i.identifier_value not like 'B%'
                        )
                        or (
                                it.identifier_type_name = 'Audible-ASIN'
                                and i.identifier_value not like 'B%'
                                and i.identifier_value not regexp '^[[:digit:]]{9}[0-9Xx]{1}$'
                        )
                )
                """
        standardReport(query, 245)

        #   Report 246: Publications with non-standard Barnes & Noble IDs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'BN'
                and i.identifier_value not like '294%'"""
        standardReport(query, 246)

        #   Report 247: Publications with Non-Standard LCCNs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'LCCN'
                and replace(i.identifier_value,'-','') not regexp '^[[:digit:]]{1,30}$'"""
        standardReport(query, 247)

        #   Report 248: Publications with Invalid Open Library IDs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'Open Library'
                and i.identifier_value not like 'O%'"""
        standardReport(query, 248)

        #   Report 249: Publications with Invalid BNB IDs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'BNB'
                and i.identifier_value like 'BLL%'"""
        standardReport(query, 249)

        #   Report 250: Publications with OCLC IDs matching ISBNs
        # Note that the query currently uses idenitifier type IDs instead of
        # idenitifier type names in order to avoid a costly join
        query = """select distinct p.pub_id
                from pubs p, identifiers i
                where p.pub_id = i.pub_id
                and i.identifier_type_id = 12
                and replace(i.identifier_value,'-','') = replace(p.pub_isbn,'-','')"""
        standardReport(query, 250)

        #   Report 272: Publications with incomplete contents and no Incomplete template
        query = """select p.pub_id from pubs p,
                (select n.note_id from notes n
                where note_note not like '%{{Incomplete}}%' and
                (note_note like '%not complete%'
                or REPLACE(LOWER(note_note), 'incomplete number line', '') like '%incomplete%'
                or note_note like '%partial content%'
                or note_note like '%partial data%'
                or note_note like '%to be entered%'
                or note_note like '%to be added%'
                or note_note like '%more%added%'
                or note_note like '%not entered yet%')
                ) x
                where p.note_id = x.note_id
                """
        standardReport(query, 272)

        #   Report 273: Mismatched Braces
        query = """select note_id, LENGTH(note_note) - LENGTH(REPLACE(note_note, '{', '')) openbraces,
                LENGTH(note_note) - LENGTH(REPLACE(note_note, '}', '')) closebraces
                from notes having openbraces != closebraces"""
        standardReport(query, 273)

        #   Report 274: References to Non-Existent Templates
        query = "select note_id from notes where "
        replace_string = "REPLACE(lower(note_note), '{{break', '')"
        for template in SQLLoadAllTemplates():
                query += "REPLACE("
                replace_string += ", '{{%s', '')" % CNX.DB_ESCAPE_STRING(template.lower())
        query += "%s like '%%{{%%'" % replace_string
        standardReport(query, 274)

        #   Report 275: Title Dates Before First Publication Dates
        query = """select t1.title_id from titles t1
                where t1.title_ttype in ('ANTHOLOGY', 'CHAPBOOK', 'COLLECTION', 'COVERART', 'OMNIBUS', 'SERIAL')
                and t1.title_parent > 0
                and YEAR(t1.title_copyright) <
                (select YEAR(min(p.pub_year))
                from pubs p, pub_content pc
                where pc.pub_id = p.pub_id
                and pc.title_id = t1.title_id)
                limit 1000"""
        standardReport(query, 275)

        #   Report 276: Variant Title Dates Before Canonical Title Dates
        query = """select t1.title_id from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and t1.title_copyright < t2.title_copyright
                and t1.title_copyright != '0000-00-00'
                and t2.title_copyright != '0000-00-00'
                and month(t1.title_copyright) != '00'
                and month(t2.title_copyright) != '00'
                and t1.title_ttype != 'SERIAL'"""
        standardReport(query, 276)

        #   Report 286: Variant Title Length Mismatches
        query = """select distinct t1.title_id
                from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and (
                        (t1.title_storylen != t2.title_storylen)
                        or
                        (t1.title_storylen is not NULL and t2.title_storylen is NULL)
                )
                limit 1000
                """
        standardReport(query, 286)

        #   Report 287: Publications with Invalid Page Numbers
        query = """select distinct pub_id
                from pub_content
                where pubc_page like '%del%'
                or pubc_page like '%&#448;%'
                or pubc_page REGEXP '[\|]{1}[^0-9\.]'
                or pubc_page REGEXP '[\|]{1}$'
                or pubc_page like 'fp'
                or pubc_page like 'fp|%'
                or pubc_page like '%`%'"""
        standardReport(query, 287)

        #   Report 288: Publications with an Invalid Page Count
        sql_version = SQLMajorVersion()
        if sql_version < 6:
                query = """select distinct pub_id from pubs
                        where pub_pages REGEXP '[^\]\[0-9ivxlcdm+ ,]'"""
        else:
                query = """select distinct pub_id from pubs
                        where pub_pages REGEXP '[^\\\\]\\\\[0-9ivxlcdm+ ,]'"""
        standardReport(query, 288)

        #   Report 289: CHAPBOOKs with Multiple Fiction Titles
        query = """select distinct p.pub_id
                from pubs p
                where p.pub_ctype='CHAPBOOK'
                and
                        (select count(t.title_id)
                        from pub_content pc, titles t
                        where p.pub_id = pc.pub_id
                        and pc.title_id = t.title_id
                        and t.title_ttype in ('SHORTFICTION', 'POEM', 'SERIAL'))
                > 1"""
        standardReport(query, 289)

        #   Report 292: Audio Books without the Narrator Template
        query = """select distinct p.pub_id
                from pubs p, notes n
                where p.pub_ptype like '%audio%'
                and p.note_id = n.note_id
                and n.note_note not like '%{{narrator%'
                limit 1000"""
        standardReport(query, 292)

        #   Report 297: Short Fiction Title Records with '(Part' in the Title field
        query = """select title_id, title_title, title_ttype from titles
                where title_title like '%(Part %'
                and title_ttype = 'SHORTFICTION'"""
        standardReport(query, 297)

        #   Report 298: Title-Based Awards with a Different Stored Author Name
        query = """select a.award_id, a.award_author from awards a
                where exists(select 1 from title_awards ta1 where ta1.award_id = a.award_id)
                and not exists(
                select 1 from title_awards ta2, titles t, canonical_author ca, authors au
                where ta2.award_id = a.award_id
                and ta2.title_id = t.title_id
                and t.title_id = ca.title_id
                and ca.ca_status = 1
                and ca.author_id = au.author_id
                and (
                (au.author_canonical = a.award_author)
                or (a.award_author like concat(au.author_canonical, '+%'))
                or (a.award_author like concat('%+', au.author_canonical))
                or (a.award_author like concat('%+', au.author_canonical, '+%'))
                )) """
        standardReport(query, 298)

        #   Report 299: Publications with Swedish Titles with no Libris XL ID
        query = """select distinct p.pub_id
            from pubs p, titles t, pub_content pc, languages l
            where p.pub_id = pc.pub_id
            and pc.title_id = t.title_id
            and t.title_language = l.lang_id
            and l.lang_name = 'Swedish'
            and p.pub_ctype not in ('MAGAZINE', 'FANZINE')
            and t.title_ttype not in ('INTERIORART')
            and not exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'Libris XL')"""
        standardReport(query, 299)

        #   Report 300: Publications with Swedish Titles with a Libris ID and no Libris XL ID
        query = """select distinct p.pub_id
            from pubs p, titles t, pub_content pc, languages l
            where p.pub_id = pc.pub_id
            and pc.title_id = t.title_id
            and t.title_language = l.lang_id
            and l.lang_name = 'Swedish'
            and p.pub_ctype not in ('MAGAZINE', 'FANZINE')
            and t.title_ttype not in ('INTERIORART')
            and exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'Libris')
            and not exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'Libris XL')"""
        standardReport(query, 300)

        #   Report 302: Author Names with an Unrecognized Suffix
        query = """select author_id from authors
                where """

        subquery = ''
        for suffix in SESSION.recognized_suffixes:
                if not subquery:
                        subquery = """replace(author_canonical, ', %s', '')""" % suffix
                else:
                        subquery = """replace(%s, ', %s', '')""" % (subquery, suffix)

        query += subquery
        query += """ like '%,%'"""
        standardReport(query, 302)

        #   Report 303: COVERART titles with 'uncredited' Author
        query = """select t.title_id
                from titles t, authors a, canonical_author ca
                where t.title_id = ca.title_id
                and t.title_ttype = 'COVERART'
                and ca.author_id = a.author_id
                and ca.ca_status = 1
                and a.author_canonical = 'uncredited'"""
        standardReport(query, 303)

        #   Report 307: Awards Linked to Uncommon Title Types (currently limited to CHAPBOOK titles)
        query = """select ta.award_id
                from titles t, title_awards ta
                where ta.title_id = t.title_id
                and t.title_ttype in ('CHAPBOOK')"""
        standardReport(query, 307)

        #   Report 325: Digital audio download pubs with regular ASINs and no Audible ASINs
        query = """select p.pub_id
                from pubs p
                where p.pub_ptype = 'digital audio download'
                and (p.pub_price like '$%' or p.pub_price is NULL or p.pub_price = '')
                and exists
                        (select 1
                        from identifiers i, identifier_types it
                        where p.pub_id = i.pub_id
                        and i.identifier_type_id = it.identifier_type_id
                        and it.identifier_type_name = 'ASIN'
                        )
                and not exists
                        (select 1
                        from identifiers i, identifier_types it
                        where p.pub_id = i.pub_id
                        and i.identifier_type_id = it.identifier_type_id
                        and it.identifier_type_name = 'Audible-ASIN'
                        )
                """
        standardReport(query, 325)

        #   Report 326: Pubs with an Audible ASIN and a non-Audible format
        query = """select p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_ptype != 'digital audio download'
                and p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'Audible-ASIN'
                """
        standardReport(query, 326)

        #   Report 327: Author Images Which We Don't Have Permission to Link to
        query = BuildRecognizedDomainsQuery('authors', 'author_id', 'author_image')
        standardReport(query, 327)

        #   Report 328: VTs with Synopsis data
        query = """select title_id from titles
                where (title_synopsis is not null and title_synopsis != 0)
                and title_parent != 0"""
        standardReport(query, 328)

        #   Report 330: Pre-1967 publications with an ISBN
        query = """select pub_id from pubs
                where pub_isbn is not null
                and pub_isbn != ''
                and pub_year != '0000-00-00'
                and pub_year < '1967-00-00'"""
        standardReport(query, 330)

        #   Report 332: Pre-2020 publications with a 979 ISBN-13
        query = """select pub_id from pubs
                where pub_isbn like '979%'
                and pub_year != '0000-00-00'
                and pub_year < '2020-00-00'"""
        standardReport(query, 332)

        #   Report 333: Interior art titles with embedded [1] or (1)
        query = """select title_id from titles
                where title_ttype='INTERIORART'
                and (title_title like '%[1]%' or title_title like '%(1)%')"""
        standardReport(query, 333)

def BuildRecognizedDomainsQuery(table, id_field, image_field):
        query =  "select %s from %s where %s != '' and %s is not null" % (id_field, table, image_field, image_field)
        domains = SQLLoadRecognizedDomains()
        for domain in domains:
                # Skip domains that are "recognized", but we don't have permission to link to
                if not domain[DOMAIN_LINKING_ALLOWED]:
                        continue
                query += " and SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(%s,'//',2),'//',-1),'/',1) not like '%%%s'" % (image_field, domain[DOMAIN_NAME])
        # Check for URL segments which must be present in the URL
        subquery = ''
        for domain in domains:
                if not domain[DOMAIN_REQUIRED_SEGMENT]:
                        continue
                if subquery:
                        subquery += ' or'
                subquery += """ (SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(%s,'//',2),'//',-1),'/',1) like '%%%s'
                            and %s not like '%%%s%%')""" % (image_field, domain[DOMAIN_NAME], image_field, domain[DOMAIN_REQUIRED_SEGMENT])
        query +=  """ UNION select %s from %s
                  where SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(%s,'//',2),'//',-1),'/',1) not like '%%sf-encyclopedia.uk'
                  and SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(%s,'//',2),'//',-1),'/',1) not like '%%sf-encyclopedia.com'
                  and (%s)""" % (id_field, table, image_field, image_field, subquery)
        return query
