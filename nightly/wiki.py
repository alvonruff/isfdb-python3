#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 495 $
#     Date: $Date: 2020-01-07 21:18:11 -0500 (Tue, 07 Jan 2020) $

from SQLparsing import *
from library import *
from shared_cleanup_lib import *

def wiki():
        if WikiExists():
                #   Report 101: Finds publications with Publication Wiki pages
                wiki_report(101, 108, 'pub_id', 'pub_tag', 'pubs')

                #   Report 102: Finds publications with Publication Talk Wiki pages
                wiki_report(102, 109, 'pub_id', 'pub_tag', 'pubs')

                #   Report 103: Finds Publication pages in the ISFDB Wiki that
                #       do not have a corresponding tag in the pubs table
                query = """select mw_page.page_id from mw_page
                        where mw_page.page_namespace = 108
                        and mw_page.page_id not in (
                        select m.page_id from pubs p, mw_page m
                        where p.pub_tag = m.page_title and m.page_namespace = 108
                        )"""
                standardReport(query, 103)

                #   Report 104: Finds Publication Talk pages in the ISFDB Wiki that
                #       do not have a corresponding tag in the pubs table
                query = """select mw_page.page_id from mw_page
                        where mw_page.page_namespace=109
                        and not exists
                                (select 1 from pubs
                                where mw_page.page_title=pubs.pub_tag)"""
                standardReport(query, 104)

                #   Report 105: Finds series records with Series Wiki pages that
                #               are not linked from the Webpages field
                wiki_report(105, 112, 'series_id', 'series_title', 'series')

                #   Report 106: Finds series records with Series Talk Wiki pages that
                #               are not linked from the Webpages field
                wiki_report(106, 113, 'series_id', 'series_title', 'series')

                #   Report 107: Finds Series pages in the ISFDB Wiki that
                #       do not have a corresponding series record in the database
                query = """select mw_page.page_id from mw_page
                        where mw_page.page_namespace=112
                        and not exists
                                (select 1 from series
                                where mw_page.page_title=REPLACE(series.series_title,' ','_'))"""
                standardReport(query, 107)

                #   Report 108: Finds Series Talk pages in the ISFDB Wiki that
                #       do not have a corresponding series record in the database
                query = """select mw_page.page_id from mw_page
                        where mw_page.page_namespace=113
                        and not exists
                                (select 1 from series
                                where mw_page.page_title=REPLACE(series.series_title,' ','_'))"""
                standardReport(query, 108)

                #   Report 109: Finds Publisher pages in the ISFDB Wiki that
                #               are not linked from the Webpages field
                wiki_report(109, 110, 'publisher_id', 'publisher_name', 'publishers')

                #   Report 110: Finds Publisher Talk pages in the ISFDB Wiki that
                #               are not linked from the Webpages field
                wiki_report(110, 111, 'publisher_id', 'publisher_name', 'publishers')

                #   Report 111: Finds Publisher pages in the ISFDB Wiki that
                #       do not have a corresponding publisher record in the database
                query = """select mw_page.page_id from mw_page
                        where mw_page.page_namespace=110
                        and not exists
                                (select 1 from publishers p
                                where mw_page.page_title=REPLACE(p.publisher_name,' ','_'))"""
                standardReport(query, 111)

                #   Report 112: Finds Publisher Talk pages in the ISFDB Wiki that
                #       do not have a corresponding publisher record in the database
                query = """select mw_page.page_id from mw_page
                        where mw_page.page_namespace=111
                        and not exists
                                (select 1 from publishers p
                                where mw_page.page_title=REPLACE(p.publisher_name,' ','_'))"""
                standardReport(query, 112)

                #   Report 113: Finds Magazines with pages in the ISFDB Wiki
                wiki_report(113, 106, 'series_id', 'series_title', 'series')

                #   Report 114: Finds Magazines with Talk pages in the ISFDB Wiki
                wiki_report(114, 107, 'series_id', 'series_title', 'series')

                #   Report 115: Finds Magazine pages in the ISFDB Wiki that
                #       do not have a corresponding series record in the database
                query = """select mw_page.page_id from mw_page
                        where mw_page.page_namespace=106
                        and mw_page.page_title not like '19%-19%'
                        and mw_page.page_title not like '2000-20%'
                        and mw_page.page_title not like '\_%'
                        and not exists
                                (select 1 from series
                                where mw_page.page_title=REPLACE(series.series_title,' ','_'))"""
                standardReport(query, 115)

                #   Report 116: Finds Magazine Talk pages in the ISFDB Wiki that
                #       do not have a corresponding series record in the database
                query = """select mw_page.page_id from mw_page
                        where mw_page.page_namespace=107
                        and not exists
                                (select 1 from series
                                where mw_page.page_title=REPLACE(series.series_title,' ','_'))"""
                standardReport(query, 116)

                #   Report 117: Finds Fanzines with pages in the ISFDB Wiki
                wiki_report(117, 104, 'series_id', 'series_title', 'series')

                #   Report 118: Finds Fanzines with Talk pages in the ISFDB Wiki
                wiki_report(118, 105, 'series_id', 'series_title', 'series')

                #   Report 119: Finds Fanzine pages in the ISFDB Wiki that
                #       do not have a corresponding series record in the database
                query = """select mw_page.page_id from mw_page
                        where mw_page.page_namespace=104
                        and not exists
                                (select 1 from series
                                where mw_page.page_title=REPLACE(series.series_title,' ','_'))"""
                standardReport(query, 119)

                #   Report 120: Finds Fanzine Talk pages in the ISFDB Wiki that
                #       do not have a corresponding series record in the database
                query = """select mw_page.page_id from mw_page
                        where mw_page.page_namespace=105
                        and not exists
                                (select 1 from series
                                where mw_page.page_title=REPLACE(series.series_title,' ','_'))"""
                standardReport(query, 120)
                
                #   Report 200: Finds authors with Author pages in the ISFDB Wiki that
                #               are not linked from the Webpages field
                wiki_report(200, 100, 'author_id', 'author_canonical', 'authors')

                #   Report 201: Finds authors with Authors Talk Wiki pages that
                #               are not linked from the Webpages field
                wiki_report(201, 101, 'author_id', 'author_canonical', 'authors')

                #   Report 202: Finds Author pages in the ISFDB Wiki that
                #       do not have a corresponding author record in the database
                wiki_stranded(202, 100, 'authors', 'author_canonical')

                #   Report 203: Finds Author Talk pages in the ISFDB Wiki that
                #       do not have a corresponding author record in the database
                wiki_stranded(203, 101, 'authors', 'author_canonical')

                #   Report 204: Finds authors with Bio pages in the ISFDB Wiki that
                #               are not linked from the Webpages field
                wiki_report(204, 102, 'author_id', 'author_canonical', 'authors')

                #   Report 205: Finds authors with Bio Talk Wiki pages that
                #               are not linked from the Webpages field
                wiki_report(205, 103, 'author_id', 'author_canonical', 'authors')

                #   Report 206: Finds Bio pages in the ISFDB Wiki that
                #       do not have a corresponding author record in the database
                wiki_stranded(206, 102, 'authors', 'author_canonical')

                #   Report 207: Finds Bio Talk pages in the ISFDB Wiki that
                #       do not have a corresponding author record in the database
                wiki_stranded(207, 103, 'authors', 'author_canonical')

def wiki_stranded(report_number, namespace, table_name, linking_field):
        # Step 1: Find all Wiki pages for this Wiki namespace and put them in a dictionary
        #         with the Wiki page name used as the key and the Wiki page ID used as the value
        query = """select mw_page.page_id, REPLACE(mw_page.page_title,'_',' ')
                   from mw_page where mw_page.page_namespace=%d""" % int(namespace)
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                return

        record = result.fetch_row()
        wiki_pages = {}
        while record:
                page_id = record[0][0]
                page_name = record[0][1]
                wiki_pages[page_name] = page_id
                record = result.fetch_row()

        # Step 2: Find all database records that match the Wiki pages in this namespace
        #         and delete them from the dictionary
        in_clause = ''
        for page_name in wiki_pages:
                escaped_name = db.escape_string(page_name)
                if not in_clause:
                        in_clause = "'%s'" % escaped_name
                else:
                        in_clause += ",'%s'" % escaped_name

        query = """select %s from %s where %s in (%s)""" % (linking_field, table_name, linking_field, in_clause)
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
                page_name = record[0][0]
                if page_name in wiki_pages:
                        del wiki_pages[page_name]
                record = result.fetch_row()

        # Step 3: Create a query that will put Wiki page IDs in the cleanup table
        page_ids = []
        for page_name in wiki_pages:
                page_ids.append(wiki_pages[page_name])
        if not page_ids:
                return
        page_ids_clause = list_to_in_clause(page_ids)
        query = """select page_id from mw_page where page_id in (%s)""" % page_ids_clause
        standardReport(query, report_number)

def wiki_report(report_number, namespace, record_id_field, linking_field, table_name):
        # Step 1: Find all record IDs with a matching Wiki page
        query = """select %s.%s from mw_page mw, %s
                where mw.page_namespace=%d
                and mw.page_title=REPLACE(%s.%s,' ','_')
                """ % (table_name, record_id_field, table_name, int(namespace), table_name, linking_field)
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                return
        
        record = result.fetch_row()
        records = []
        while record:
                record_id = record[0][0]
                records.append(record_id)
                record = result.fetch_row()

        # Step 2:
        query = """select distinct %s from webpages
                   where %s is not null
                   and url like '%%www.isfdb.org%%'
                   """ % (record_id_field, record_id_field)

        # Step 3:
        #  Retrieve records and delete them from the record ID list built in Step 1
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
                record_id = record[0][0]
                if record_id in records:
                        records.remove(record_id)
                record = result.fetch_row()

        if not records:
                return
        # Convert the trimmed list of records to a SQL "in" clause
        records_list = list_to_in_clause(records)
        query = """select %s from %s where %s in (%s)
                    """ % (record_id_field, table_name, record_id_field, records_list)
        standardReport(query, report_number)
