#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2022-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 646 $
#     Date: $Date: 2021-06-18 13:06:11 -0400 (Fri, 18 Jun 2021) $

from login import *
from isfdb import *
from common import *
from SQLparsing import *
from library import *

class MyVerifications:
        def __init__(self):
                self.bgcolor = 1
                self.displayed_count = 0
                self.per_page = 200
                self.pub_id = ''
                self.record = []
                self.retrieved_count = 0
                self.user = User()
                self.user.load()

        def display(self):
                start = SESSION.Parameter(0, 'int', 0)
                self.displayed_index = start
                script = SESSION.cgi_script
                if script == 'userver':
                        query = """select p.pub_id, p.pub_title, p.pub_ctype, 
                                date_format(pv.ver_time,'%%Y-%%m-%%d') date,
                                pv.ver_transient, p.pub_frontimage
                                from pubs p, primary_verifications pv
                                where pv.pub_id = p.pub_id
                                and pv.user_id = %d
                                order by date desc, pv.verification_id desc
                                limit %d,%d""" % (int(self.user.id), start, self.per_page +1)
                        none_found = 'No primary verifications'
                elif script == 'my_unstable_ISBN_verifications':
                        query = """select p.pub_id, p.pub_title, p.pub_ctype, 
                                date_format(pv.ver_time,'%%Y-%%m-%%d') date,
                                pv.ver_transient, p.pub_frontimage
                                from pubs p, primary_verifications pv
                                where pv.pub_id = p.pub_id
                                and pv.user_id = %d
                                and p.pub_frontimage like '%%amazon.com%%'
                                and p.pub_frontimage like '%%amazon.com/images/P/%%'
                                order by date desc, pv.verification_id desc
                                limit %d,%d""" % (int(self.user.id), start, self.per_page + 1)
                        none_found = 'No primary verifications with unstable ISBN-based Amazon URLs'
                elif script == 'my_unstable_verifications':
                        query = """select p.pub_id, p.pub_title, p.pub_ctype, 
                                date_format(pv.ver_time,'%%Y-%%m-%%d') date,
                                pv.ver_transient, p.pub_frontimage
                                from pubs p, primary_verifications pv
                                where pv.pub_id = p.pub_id
                                and pv.user_id = %d
                                and p.pub_frontimage like '%%amazon.com%%'
                                and p.pub_frontimage like '%%amazon.com/images/G/%%'
                                order by date desc, pv.verification_id desc
                                limit %d,%d""" % (int(self.user.id), start, self.per_page + 1)
                        none_found = 'No primary verifications with unstable "/G/" Amazon URLs'
                else:
                        print('<h2>A software error has occurred. Please post this URL on the ISFDB Community Portal.</h2>')
                        return
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                SQLlog("myverificationsClass::query: %s" % query)
                self.retrieved_count = CNX.DB_NUMROWS()

                if self.retrieved_count:
                        last_displayed = self.retrieved_count
                        if self.retrieved_count > self.per_page:
                                last_displayed = self.per_page
                        print('<h3>Displaying primary verifications %d - %d:</h3>' % (start + 1, start + last_displayed))
                        self.record = CNX.DB_FETCHMANY()
                        self.printTableColumns()
                        while self.record:
                                self.displayed_count += 1
                                if self.displayed_count > self.per_page:
                                        break
                                self.printPubRecord()
                                self.record = CNX.DB_FETCHMANY()
                        print('</table>')
                        if self.retrieved_count > self.per_page:
                                print(ISFDBLink('%s.cgi' % script, start + self.per_page,
                                                '%d - %d' % (start + self.per_page + 1, start + (2 * self.per_page)),
                                                True))
                else:
                        print('<h2>%s found</h2>' % none_found)

        def printTableColumns(self):
                print('<table class="userverifications">')
                print('<tr class="table2">')
                print('<th>#</th>')
                print('<th>Type</th>')
                print('<th>Ver. Date</th>')
                print('<th>Publication</th>')
                print('<th>Author(s) or Editor(s)</th>')
                print('<th>Transient?</th>')
                print('<th>Artist(s)</th>')
                print('<th>Cover</th>')
                print('</tr>')

        def printPubRecord(self):
                self.displayed_index += 1
                data = self.record[0]
                self.pub_id = data[0]
                if self.bgcolor:
                        print('<tr align=left class="table1">')
                else:
                        print('<tr align=left class="table2">')
                self.bgcolor ^= 1

                print('<td>%d</td>' % self.displayed_index)
                print('<td>%s</td>' % data[2])
                print('<td>%s</td>' % data[3])
                print('<td>%s</td>' % ISFDBLink('pl.cgi', self.pub_id, data[1]))
                output = '' 
                if data[2] in ('MAGAZINE', 'ANTHOLOGY', 'FANZINE', 'NONFICTION'):
                        output = "Ed. "
                output += self.pubAuthors()
                print('<td>%s</td>' % output)

                if data[4]:
                        print('<td>Transient</td>')
                else:
                        print('<td>&nbsp;</td>')

                cover_artists = self.pubArtists()
                print('<td>')
                if self.pub_id in cover_artists:
                        displayAuthorList(cover_artists[self.pub_id])
                else:
                        print('&nbsp;')
                print('</td>')

                if data[5]:
                        print('<td>%s</td>' % CoverInfo(data[5]))
                else:
                        print('<td>&nbsp;</td>')

                print('</tr>')

        def pubAuthors(self):
                retval = ''
                authors = SQLPubBriefAuthorRecords(self.pub_id)
                for counter, author in enumerate(authors):
                        if counter:
                                retval += ', '
                        retval += ISFDBLink('ea.cgi', author[0], author[1])
                return retval

        def pubArtists(self):
                list_of_pub_ids = []
                list_of_pub_ids.append(str(self.pub_id))
                cover_artists = SQLGetCoverAuthorsForPubs(list_of_pub_ids)
                return cover_artists
