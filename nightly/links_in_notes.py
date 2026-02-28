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

def links_in_notes():
        #   Report 218: Publications with ASINs in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like binary '%ASIN%'"""
        standardReport(query, 218)

        #   Report 219: Publications with .bl. (British Library) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%.bl.%'"""
        standardReport(query, 219)

        #   Report 220: Publications with .sfbg.us (SFBG) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%.sfbg.us%'"""
        standardReport(query, 220)

        #   Report 221: Publications with d-nb.info (direct Deutsche Nationalbibliothek links) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%/d-nb.info/%'
                 order by p.pub_title"""
        standardReport(query, 221)

        #   Report 222: Publications with .fantlab.ru (FantLab) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%fantlab.ru/%'"""
        standardReport(query, 222)

        #   Report 223: Publications with .amazon.%dp (direct Amazon links) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%.amazon.%dp%'"""
        standardReport(query, 223)

        #   Report 224: Publications with .bnf.fr (BNF) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%catalogue.bnf.fr%'"""
        standardReport(query, 224)

        #   Report 225: Publications with lccn.loc (direct Library of Congress links) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%lccn.loc%'"""
        standardReport(query, 225)

        #   Report 226: Publications with worldcat.org (direct OCLC/WorldCat links) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%worldcat.org/%'
                 order by p.pub_title"""
        standardReport(query, 226)

        #   Report 230: Mismatched OCLC URLs in Publication Notes
        query = """select p.pub_id, n.note_note from notes n, pubs p
                where p.note_id = n.note_id and n.note_note regexp
                '<a href=\"https:\/\/www.worldcat.org\/oclc\/[[:digit:]]{1,11}"\>[[:digit:]]{1,11}\<\/a>'"""
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        pubs = []
        while record:
                pub_id = int(record[0][0])
                note_note = record[0][1]
                record = CNX.DB_FETCHMANY()
                two_numbers = note_note.lower().split('/oclc/')[1].split('</a>')[0]
                number_list = two_numbers.split('">')
                if number_list[0] != number_list[1]:
                        pubs.append(pub_id)
        if pubs:
                in_clause = list_to_in_clause(pubs)
                query = "select pub_id from pubs where pub_id in (%s)" % in_clause
                standardReport(query, 230)

        #   Report 234: Publications with direct De Nederlandse Bibliografie links in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%picarta.pica.nl/%'"""
        standardReport(query, 234)

        #   Report 237: Pubs with non-template LCCNs in notes
        query = """select p.pub_id from
                (select note_id from notes
                where note_note like '%LCCN:%'
                or note_note regexp 'LCCN [[:digit:]]{1}')
                as n, pubs p
                where p.note_id = n.note_id"""
        standardReport(query, 237)

        #   Report 253: Pubs with non-linking External IDs in Notes
        query = """select p.pub_id from pubs p, notes n
                where p.note_id = n.note_id
                and n.note_id in (select distinct note_id from notes
                where note_note like '%{{BREAK}}%Reginald1%'
                or note_note like '%{{BREAK}}%Reginald3%'
                or note_note like '%{{BREAK}}%Bleiler%Early Years%'
                or note_note like '%{{BREAK}}%Bleiler%Gernsback%'
                or note_note like '%{{BREAK}}%Bleiler%Guide to Supernatural%')"""
        standardReport(query, 253)

        #   Report 254: Publications with www.noosfere.org in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%www.noosfere.org%'"""
        standardReport(query, 254)

        #   Report 255: Publications with nilf.it in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%nilf.it/%'"""
        standardReport(query, 255)

        #   Report 256: Publications with fantascienza.com/catalogo in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%fantascienza.com/catalogo%'"""
        standardReport(query, 256)

        #   Report 296: Stonecreek's EditPub submissions with 'first printing' in notes
        query = """select user_id from mw_user where user_name='Stonecreek'"""
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        user_id = record[0][0]

        query = """select affected_record_id from submissions
                where sub_submitter=%d
                and sub_data like "%%first printing%%"
                and sub_data not like "%%apparent first printing%%"
                and sub_data not like "%%assumed first printing%%"
                and affected_record_id is not null
                and sub_type = 4""" % user_id
        CNX.DB_QUERY(query)
        count = CNX.DB_NUMROWS()
        pubs = []
        record = CNX.DB_FETCHMANY()
        while record:
                pub_id = record[0][0]
                pubs.append(pub_id)
                record = CNX.DB_FETCHMANY()

        in_clause = list_to_in_clause(pubs)
        if in_clause:
                query = """select p.pub_id
                        from pubs p
                        where p.pub_id in (%s)
                        and not exists(select 1 from primary_verifications pv
                                        where pv.pub_id = p.pub_id)""" % in_clause
                standardReport(query, 296)

        #   Report 304: Publications with COBISS references in notes and no template/External ID
        query = """select p.pub_id
                from pubs p, notes n 
                where p.note_id = n.note_id 
                and n.note_note like '%COBISS%' 
                and n.note_note not like '%{{COBISS%' 
                and not exists
                (select 1 from identifiers i, identifier_types it 
                where p.pub_id = i.pub_id 
                and i.identifier_type_id = it.identifier_type_id 
                and it.identifier_type_name like '%COBISS%')"""
        standardReport(query, 304)

        #   Report 305: Publications with Biblioman references in notes and no template/External ID
        query = """select p.pub_id
                from pubs p, notes n 
                where p.note_id = n.note_id 
                and n.note_note like '%Biblioman%' 
                and n.note_note not like '%{{Biblioman|%' 
                and not exists 
                (select 1 from identifiers i, identifier_types it 
                where p.pub_id = i.pub_id 
                and i.identifier_type_id = it.identifier_type_id 
                and it.identifier_type_name = 'Biblioman')"""
        standardReport(query, 305)

        #   Report 331: Publications with PV# in notes
        query = """select p.pub_id
                from notes n, pubs p
                where p.note_id = n.note_id
                and n.note_note regexp 'pv[[:blank:]]{0,}[[:digit:]]{1}'"""
        standardReport(query, 331)
