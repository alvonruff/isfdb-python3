#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2016-2025  Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1003 $
#     Date: $Date: 2022-09-15 14:36:33 -0400 (Thu, 15 Sep 2022) $

from SQLparsing import *
from common import *
from library import *
from login import *


def PubAuthors(pub_id):
        retval = ''
        authors = SQLPubBriefAuthorRecords(pub_id)
        counter = 0
        for author in authors:
                if counter:
                        retval += ", "
                retval += ISFDBLink('ea.cgi', author[0], author[1])
                counter += 1
        return retval

def PrintPubRecord(count, record, previous_last_viewed, bgcolor):
        pub_id = record[0]
        pub_title = record[1]
        ver_date = record[2]
        change_date = record[3]
        sub_id = record[4]
        sub_data = record[5]
        submitter_name = record[6]
        transient = record[7]
        if bgcolor:
                print('<tr align=left class="table1">')
        else:
                print('<tr align=left class="table2">')

        print('<td>%d</td>' % count)
        new = 'New'
        if change_date and previous_last_viewed and change_date < previous_last_viewed:
                new = '&nbsp;'
        print('<td>%s</td>' % new)
        print('<td>%s</td>' % ISFDBLinkNoName('view_submission.cgi', sub_id, change_date))
        print('<td>%s</td>' % WikiLink(submitter_name))
        xml = SQLloadXML(sub_id)
        doc = minidom.parseString(XMLunescape2(xml))
        fields = ''
        # Process Import/Export submissions first because they contain XML tags for
        # fields that were NOT modified (a known quirk)
        if doc.getElementsByTagName('ClonedTo'):
                fields = 'Import/Export'
        # Otherwise this is an Edit Publication submission
        else:
                for field in sorted(('Title', 'TransTitles', 'Authors', 'Year', 'Publisher',
                              'PubSeries', 'PubSeriesNum', 'Pages', 'Binding', 'PubType',
                              'Isbn', 'Price', 'Image', 'Note', 'ContentTitle',
                              'ContentReview', 'ContentInterview', 'Cover', 'External_ID',
                              'Catalog', 'Webpage')):
                        if doc.getElementsByTagName(field):
                                if fields:
                                        fields += ', '
                                if field in SUBMISSION_DISPLAY:
                                        display_field = SUBMISSION_DISPLAY[field]
                                else:
                                        display_field = field
                                fields += display_field
                if not fields:
                        fields = '&nbsp;'
        print('<td>%s</td>' % fields)
        print('<td>%s</td>' % ver_date)
        print('<td>%s</td>' % ISFDBLink('pl.cgi', pub_id, pub_title))
        print('<td>%s</td>' % PubAuthors(pub_id))
        if transient:
                print('<td>Transient</td>')
        else:
                print('<td>&nbsp;</td>')

        print('</tr>')

def PrintTableColumns():
        print('<table class="userverifications">')
        print('<tr class="table2">')
        print('<th>Count</th>')
        print('<th>New?</th>')
        print('<th>Submission Link</th>')
        print('<th>Submitter</th>')
        print('<th>Changed Fields</th>')
        print('<th>Verification Date</th>')
        print('<th>Publication</th>')
        print('<th>Author/Editor</th>')
        print('<th>Transient?</th>')
        print('</tr>')

if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)

        PrintHeader("My Recently Changed Primary Verifications")
        PrintNavbar('changed_verified_pubs', 0, 0, 'changed_verified_pubs.cgi', 0)

        user = User()
        user.load()
        previous_last_viewed = user.update_last_viewed_verified_pubs_DTS()

        # date_format(c.change_time,'%%Y-%%m-%%d')
        query = """select p.pub_id, p.pub_title,
                date_format(pv.ver_time,'%%Y-%%m-%%d') ver_date,
                c.change_time, c.sub_id, s.sub_data, u.user_name, pv.ver_transient
                from pubs p, primary_verifications pv, changed_verified_pubs c,
                mw_user u, submissions s
                where pv.pub_id = p.pub_id
                and c.sub_id = s.sub_id
                and s.sub_submitter = u.user_id
                and c.pub_id = p.pub_id
                and c.verifier_id = %d
                and pv.user_id = %d
                order by c.change_time desc, sub_id desc
                limit %d,%d""" % (int(user.id), int(user.id), start, 200)

        db.query(query)
        result = db.store_result()
        num = result.num_rows()

        if num > 0:
                last = num
                if last > 200:
                        last = 200
                print('<h3>Displaying changed primary verifications %d-%d:</h3>' % (start+1, start+last))
                record = result.fetch_row()
                bgcolor = 1
                PrintTableColumns()
                count = start + 1
                while record:
                        PrintPubRecord(count, record[0], previous_last_viewed, bgcolor)
                        bgcolor ^= 1
                        count += 1
                        record = result.fetch_row()
                print('</table>')
                if num > 199:
                        print(ISFDBLinkNoName('changed_verified_pubs.cgi', start+200, '%d-%d' % (start+201, start+400), True))
        else:
                print('<h2>No changed primary verifications found</h2>')

        PrintTrailer('changed_verified_pubs', 0, 0)

