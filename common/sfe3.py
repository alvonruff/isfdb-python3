from __future__ import print_function
#
#     (C) COPYRIGHT 2009-2025   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1192 $
#     Date: $Date: 2024-08-28 16:16:18 -0400 (Wed, 28 Aug 2024) $

import os
import sys
import shutil
import string
import urllib2
from library import *
from SQLparsing import *

class Sfe3:
        def __init__(self):
                self.online_URLs = {}
                self.unresolved_URLs = {}
                self.resolved_URLs = {}
                self.URLs_in_author_records = []
                self.urls_to_delete_from_sfe3_authors = []
                #
                self.host = 'sf-encyclopedia.com'
                self.protocol = 'https'
                self.base_category_url = '%s://www.%s/category/' % (self.protocol, self.host)
                self.categories = ['art', 'author', 'critic', 'editor', 'house%20name', 'people']
                self.sleep_seconds = 1
                self.user = None

        def process(self):
                self.load_URLs_in_author_records()
                print('Links in "webpages": ',len(self.URLs_in_author_records))
                self.load_resolved_and_unresolved_URLs()
                print('Unresolved URLs: ',len(self.unresolved_URLs))
                print('Resolved URLs: ',len(self.resolved_URLs))
                self.reconcile_newly_entered_URLs()
                self.delete_newly_entered_unresolved_URLs()
                print('Removed %d newly entered SFE links' % len(self.urls_to_delete_from_sfe3_authors))

                self.download_URLs_from_SFE3()
                self.remove_known_urls()
                self.file_new_urls()

        def load_URLs_in_author_records(self):
                query = """select distinct url
                        from webpages
                        where author_id is not null
                        and url like '%%%s/%%'""" % db.escape_string(self.host)
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        full_url = record[0][0]
                        url_segments = full_url.split('/')
                        last_segment = url_segments[-1]
                        self.URLs_in_author_records.append(last_segment)
                        record = result.fetch_row()

        def count_of_unresolved(self):
                query = "select count(*) from sfe3_authors where resolved is null"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                return record[0][0]
        
        def load_resolved_and_unresolved_URLs(self):
                query = "select url, author_name, resolved from sfe3_authors"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        url = record[0][0]
                        author_name = record[0][1]
                        resolved = record[0][2]
                        if resolved:
                                self.resolved_URLs[url] = author_name
                        else:
                                self.unresolved_URLs[url] = author_name
                        record = result.fetch_row()

        def reconcile_newly_entered_URLs(self):
                for url in self.URLs_in_author_records:
                        if url in self.unresolved_URLs:
                                del self.unresolved_URLs[url]
                                self.urls_to_delete_from_sfe3_authors.append(url)

        def delete_newly_entered_unresolved_URLs(self):
                for url in self.urls_to_delete_from_sfe3_authors:
                        delete = "delete from sfe3_authors where url = '%s'" % db.escape_string(url)
                        db.query(delete)

        def download_URLs_from_SFE3(self):
                fragment_separator = 'a href="/entry/'
                author_separator1 = '">'
                author_separator2 = "</a>"
                for category in self.categories:
                        category_url = self.base_category_url + category
                        try:
                                page_contents = urllib2.urlopen(category_url).read()
                        except:
                                continue
                        fragments = page_contents.split(fragment_separator)
                        count = 0
                        for fragment in fragments[1:]:
                                if author_separator1 not in fragment:
                                        continue
                                count += 1
                                url = fragment.split(author_separator1)[0]
                                author_name = ''
                                remainder = fragment.split(author_separator1)[1]
                                if author_separator2 in remainder:
                                        author_name = remainder.split(author_separator2)[0]
                                        if len(author_name) > 200:
                                                author_name = '' # If the author name is longer than 200, something is wrong
                                self.online_URLs[url] = author_name
                        print('%s: %d ' % (category, count), end=' ')
                        sleep(self.sleep_seconds)

        def remove_known_urls(self):
                print('Downloaded from the Web site: ',len(self.online_URLs))
                for url in self.URLs_in_author_records:
                        if url in self.online_URLs:
                                del self.online_URLs[url]
                print('New URLs after removing URLs already linked to author records: ',len(self.online_URLs))
                for url in self.unresolved_URLs:
                        if url in self.online_URLs:
                                del self.online_URLs[url]
                for url in self.resolved_URLs:
                        if url in self.online_URLs:
                                del self.online_URLs[url]
                print('New URLs after removing URLs in sfe3_authors: ',len(self.online_URLs))

        def file_new_urls(self):
                for segment in self.online_URLs:
                        author_name = self.online_URLs[segment]
                        update = "insert into sfe3_authors(url, author_name) values('%s', '%s')" % (db.escape_string(segment), db.escape_string(author_name))
                        db.query(update)
                print('Updated')

        def display_report(self):
                self.load_URLs_in_author_records()
                self.load_resolved_and_unresolved_URLs()
                self.reconcile_newly_entered_URLs()
                self.delete_newly_entered_unresolved_URLs()
                self.print_header()
                if not self.unresolved_URLs:
                        print('<h2>No unresolved SFE author Web pages found</h2>')
                        return
                self.load_moderator_flag()
                self.print_table_columns(('#', 'SFE URL', 'SFE Author Name', 'Possible ISFDB Name', 'Ignore'))
                self.bgcolor = 1
                self.count = 1
                for unresolved_url in sorted(self.unresolved_URLs.keys(), key=lambda x: x.lower()):
                        self.print_record(unresolved_url)
                        self.bgcolor ^= 1
                        self.count += 1
                print('</table>')

        def load_moderator_flag(self):
                from login import User
                self.user = User()
                self.user.load()
                self.user.load_moderator_flag()

        def print_header(self):
                print("""<h3>This cleanup report lists all  
                        <a href="%s://sf-encyclopedia.com/category/everyone">SFE author/editor/etc articles</a>
                        without a matching author URL in the ISFDB database. Note that some SFE authors may not
                        be eligible on the ISFDB side, e.g. if their only SF works are comics.
                        Also, the SFE spelling or canonical name may not match what's used in
                        the ISFDB database. For these reasons, this report lets moderators ignore SFE author
                        URLs.</h3>""" % self.protocol)

        def print_table_columns(self, columns):
                print('<table class="generic_table">')
                print('<tr class="table2">')
                for column in columns:
                        if not column:
                                data = '&nbsp;'
                        else:
                                data = column
                        # Skip 'Ignore' and 'Resolve' columns if the user is not a moderator
                        if ('Ignore' in column or 'Resolve' in column) and not self.user.moderator:
                                continue
                        print('<td><b>%s</b></td>' % data)
                print('</tr>')

        def print_record(self, unresolved_url):
                if self.bgcolor:
                        print('<tr align=left class="table1">')
                else:
                        print('<tr align=left class="table2">')

                url = '%s://www.%s/entry/%s' % (self.protocol, self.host, unresolved_url)
                sf3_author_name = self.unresolved_URLs[unresolved_url]
                isfdb_author_name = self.normalize_author_name(sf3_author_name)
                author_link = AdvSearchLink((('TYPE', 'Author'),
                                     ('USE_1', 'author_canonical'),
                                     ('O_1', 'exact'),
                                     ('TERM_1', isfdb_author_name),
                                     ('ORDERBY', 'author_lastname'),
                                     ('C', 'AND')))

                print('<td>%d</td>' % self.count)
                print('<td><a href="%s" target="_blank">%s</a></td>' % (url, url))
                print('<td>%s</td>' % sf3_author_name)
                print('<td>%s%s</a></td>' % (author_link, isfdb_author_name))
                if self.user.moderator:
                        print('<td>%s</a></td>' % ISFDBLink('mod/resolve_sfe3_url.cgi', unresolved_url, 'Ignore'))
                print('</tr>')

        def normalize_author_name(self, sf3_author_name):
                isfdb_author_name = sf3_author_name
                last_name = ''
                if ',' in isfdb_author_name:
                        # Remove and save the last name to be appended to the string later
                        name_fragments  = isfdb_author_name.split(',')
                        last_name = name_fragments[0]
                        isfdb_author_name = ' '.join(name_fragments[1:])
                        space_fragments = isfdb_author_name.split(' ')
                        
                        # Add periods to initials without a trailing period 
                        new_space_fragments = []
                        for space_fragment in space_fragments:
                                if len(space_fragment) == 1 or space_fragment in ('Dr', 'Mr', 'Mrs'):
                                        new_space_fragment = space_fragment + '.'
                                else:
                                        new_space_fragment = space_fragment
                                new_space_fragments.append(new_space_fragment)
                        isfdb_author_name = ' '.join(new_space_fragments)
                        # Append the previously saved last name
                        if last_name:
                                isfdb_author_name = isfdb_author_name + ' ' + last_name
                return str.strip(isfdb_author_name)
