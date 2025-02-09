#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2024   Al von Ruff, Ahasuerus and Dirk Stoecker
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

def slow_queries():
        #   Report 3: Titles without Pubs. Note that the logic ignores pub-less titles that have VTs.
        query = """select t1.title_id from titles t1
                where t1.title_copyright != '8888-00-00'
                and not exists (select 1 from pub_content where t1.title_id=pub_content.title_id)
                and not exists (select 1 from titles t2 where t1.title_id=t2.title_parent)"""
        standardReport(query, 3)

        #   Report 52: Publications with 0 or 2+ Reference Titles
        only_one = {'ANTHOLOGY': ['ANTHOLOGY'],
                    'COLLECTION': ['COLLECTION'],
                    'CHAPBOOK': ['CHAPBOOK'],
                    'MAGAZINE': ['EDITOR'],
                    'FANZINE': ['EDITOR'],
                    'NONFICTION': ['NONFICTION'],
                    'NOVEL': ['NOVEL'],
                    'OMNIBUS': ['OMNIBUS']}
                      
        query = ""
        for pub_type in only_one:
                if query:
                        query += " UNION "
                query += "(select p.pub_id from pubs p where p.pub_ctype='%s'" % pub_type
                query += " and (select count(*) from pub_content pc, titles t"
                query += " where pc.pub_id=p.pub_id and t.title_id=pc.title_id"
                query += " and "
                subquery = ""
                for title_type in only_one[pub_type]:
                        if subquery:
                                subquery += " or "
                        subquery += "(t.title_ttype='%s')" % title_type
                query += "(" + subquery + "))!=1)"
        standardReport(query, 52)

        #   Report 243: Publication Images with Extra Formatting in Amazon URLs
        query = """select pub_id from pubs
                where pub_frontimage like '%amazon.com/%'
                and not
                (REPLACE(pub_frontimage,'%2B','+') REGEXP '/images/[PIG]/[0-9A-Za-z+-]{10}[LS]?(\._CR[0-9]+,[0-9]+,[0-9]+,[0-9]+)?\.(gif|png|jpg)$'
                or
                pub_frontimage REGEXP '\.images(\-|\.)amazon\.com/images/G/0[1-3]/ciu/[0-9a-f]{2}/[0-9a-f]{2}/[0-9a-f]{22,24}\.L\.(gif|png|jpg)$'
                or
                pub_frontimage REGEXP '(m\.media-amazon|\.ssl-images-amazon)\.com/images/S/amzn-author-media-prod/[0-9a-z]{26}\.(gif|png|jpg)$')
                """
        standardReport(query, 243)

        #   Report 324: Pubs without an ISBN and with an Audible ASIN which is an ISBN-10
        query = """select p.pub_id
                from pubs p
                where (p.pub_isbn is NULL or p.pub_isbn = '')
                and exists
                        (select 1
                        from identifiers i, identifier_types it
                        where p.pub_id = i.pub_id
                        and i.identifier_type_id = it.identifier_type_id
                        and it.identifier_type_name = 'Audible-ASIN'
                        and i.identifier_value regexp '^[[:digit:]]{9}[0-9Xx]{1}$'
                        )
                """
        standardReport(query, 324)

