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

def containers_cleanup():
        #   Report 29: Chapbooks without Contents Titles
        query = "select pub_id from pubs where pub_ctype='CHAPBOOK' and NOT EXISTS \
                (select 1 from pub_content,titles where pubs.pub_id=pub_content.pub_id \
                and pub_content.title_id=titles.title_id and (titles.title_ttype='SHORTFICTION' \
                or titles.title_ttype='POEM' or titles.title_ttype='SERIAL'))"
        standardReport(query, 29)

        #   Report 37: Omnibuses without Contents Titles
        query = "select pub_id from pubs where pub_ctype='OMNIBUS' and NOT EXISTS \
                (select 1 from pub_content,titles where pubs.pub_id=pub_content.pub_id \
                and pub_content.title_id=titles.title_id and (titles.title_ttype='NOVEL' \
                or titles.title_ttype='COLLECTION' \
                or titles.title_ttype='ANTHOLOGY' or titles.title_ttype='NONFICTION'))"
        standardReport(query, 37)

        #   Report 54: Container Titles in Publications with no Contents
        query = """select tmp.good from 
                (select distinct t1.title_id as good from titles t1, pub_content pc1
                 where t1.title_ttype in ('ANTHOLOGY','COLLECTION')
                 and t1.title_id=pc1.title_id
                 and exists
                        (select 1 from pub_content pc2, titles t2
                        where pc1.pubc_id!=pc2.pubc_id
                        and pc1.pub_id=pc2.pub_id
                        and pc2.title_id=t2.title_id
                        and t2.title_ttype in ('SHORTFICTION','POEM','SERIAL'))) tmp
                where tmp.good in 
                (select distinct t1.title_id from titles t1, pub_content pc1
                 where t1.title_ttype in ('ANTHOLOGY','COLLECTION')
                 and t1.title_id=pc1.title_id
                 and not exists
                        (select 1 from pub_content pc2, titles t2
                        where pc1.pubc_id!=pc2.pubc_id
                        and pc1.pub_id=pc2.pub_id
                        and pc2.title_id=t2.title_id
                        and t2.title_ttype in ('SHORTFICTION','POEM','SERIAL')))"""
        standardReport(query, 54)

        #   Report 92: Primary-verified Anthologies/Collections without Contents Titles
        query = """select distinct p.pub_id
                from pubs p, primary_verifications pv
                where p.pub_ctype in ('ANTHOLOGY', 'COLLECTION')
                and p.pub_id = pv.pub_id
                and NOT EXISTS
                (select 1 from pub_content pc, titles t
                where p.pub_id=pc.pub_id 
                and pc.title_id=t.title_id
                and (t.title_ttype in ('NOVEL', 'SHORTFICTION', 'POEM', 'SERIAL'))
                )"""
        standardReport(query, 92)

        #   Report 240: Anthologies and Collections without Fiction Titles
        query = emptyContainers(240, "'ANTHOLOGY', 'COLLECTION'")

        #   Report 241: Magazines without Fiction Titles
        query = emptyContainers(241, "'MAGAZINE'")

def emptyContainers(report_id, container_types):
        elapsed = elapsedTime()
        standardDelete(report_id)
        query = """select xx.pub_id, IF(xx.pub_year='0000-00-00', 0, REPLACE(SUBSTR(xx.pub_year, 1,7),'-',''))
                from (
                select p.pub_id, p.pub_year
                from pubs p
                where p.pub_ctype in (%s)
                and p.pub_year != '8888-00-00'
                and NOT EXISTS
                        (select 1 from pub_content pc, titles t
                        where p.pub_id=pc.pub_id 
                        and pc.title_id=t.title_id
                        and (t.title_ttype in ('NOVEL', 'SHORTFICTION', 'POEM', 'SERIAL'))
                )) as xx""" % container_types
        db.query(query)
        result = db.store_result()
        containers = {}
        record = result.fetch_row()
        while record:
                pub_id = record[0][0]
                pub_month = record[0][1]
                containers[pub_id] = pub_month
                record = result.fetch_row()

        # Remove previously resolved/ignored records from the dictionary of IDs
        query = "select record_id from cleanup where report_type=%d and resolved=1" % int(report_id)
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
                resolved_id = record[0][0]
                if resolved_id in containers:
                        del containers[resolved_id]
                record = result.fetch_row()

        # Insert the new pub IDs and their months into the cleanup table
        for record_id in containers:
                update = "insert into cleanup (record_id, report_type, record_id_2) values(%d, %d, %d)" % (int(record_id), int(report_id), int(containers[record_id]))
                db.query(update)
        elapsed.print_elapsed(report_id, len(containers))
