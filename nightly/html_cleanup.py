#!_PYTHONLOC
#
#     (C) COPYRIGHT 2017-2022   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 863 $
#     Date: $Date: 2022-03-08 18:35:10 -0500 (Tue, 08 Mar 2022) $

import string
from SQLparsing import *
from library import *
from shared_cleanup_lib import *

def html_cleanup():
        ui = isfdbUI()
        #   Report 55: Title records with HTML in titles
        query = "select title_id from titles where "
        query += ui.goodHtmlClause('titles', 'title_title')
        standardReport(query, 55)

        #   Report 56: Publications with HTML in titles
        query = "select pub_id from pubs where "
        query += ui.goodHtmlClause('pubs', 'pub_title')
        standardReport(query, 56)

        #   Report 208-216: Records with unsupported HTML in Notes
        query = "select note_id from notes where "
        query += ui.badHtmlClause('notes', 'note_note')
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        num = CNX.DB_NUMROWS()
        note_list = []
        while record:
                note_id = record[0][0]
                note_list.append(note_id)
                record = CNX.DB_FETCHMANY()
        in_clause = list_to_in_clause(note_list)
        record_types = (('pubs', 'note_id', 'pub_id', 208),
                    ('titles', 'note_id', 'title_id', 209),
                    ('publishers', 'note_id', 'publisher_id', 210),
                    ('series', 'series_note_id', 'series_id', 211),
                    ('pub_series', 'pub_series_note_id', 'pub_series_id', 212),
                    ('awards', 'award_note_id', 'award_id', 213),
                    ('award_types', 'award_type_note_id', 'award_type_id', 214),
                    ('award_cats', 'award_cat_note_id', 'award_cat_id', 215),
                    ('titles', 'title_synopsis', 'title_id', 216))
        for record_data in record_types:
                table = record_data[0]
                note_field = record_data[1]
                record_id_field = record_data[2]
                report_id = record_data[3]
                query = "select %s from %s where %s in (%s)" % (record_id_field, table, note_field, in_clause)
                standardReport(query, report_id)

        #   Report 217: Author Notes with unsupported HTML
        # NB: Author notes are processed separately since they are stored in the main author table
        query = "select author_id from authors where "
        query += ui.badHtmlClause('authors', 'author_note')
        standardReport(query, 217)

        #   Report 229: Mismatched HTML tags in publication Notes
        query = "select p.pub_id from pubs p, notes n where p.note_id = n.note_id and ("
        count = 0
        for tag in ui.required_paired_tags:
                if count:
                        query += " or "
                query += """round((length(lower(n.note_note)) - length(replace(lower(n.note_note),'<%s>','')))/%d) !=
                round((length(lower(n.note_note)) - length(replace(lower(n.note_note),'</%s>','')))/%d)""" % (tag, len(tag)+2, tag, len(tag)+3)
                count += 1
        query += ")"
        standardReport(query, 229)
