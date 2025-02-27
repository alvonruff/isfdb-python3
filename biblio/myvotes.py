#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1039 $
#     Date: $Date: 2022-10-18 16:34:51 -0400 (Tue, 18 Oct 2022) $


from isfdb import *
from common import *
from login import *
from SQLparsing import *


if __name__ == '__main__':

        titles_per_page = 50
        start = SESSION.Parameter(0, 'int', 0)
        all_sort_orders = ('Vote', 'Title', 'Date', 'MostRecentVote')
        current_sort_order = SESSION.Parameter(1, 'str', None, all_sort_orders)

        alternative_sort_orders = []
        for sort_order in all_sort_orders:
                if sort_order != current_sort_order:
                        sort_order_link = ISFDBLink('myvotes.cgi', '0+%s' % sort_order, sort_order)
                        alternative_sort_orders.append(sort_order_link)

        PrintHeader('My Votes')
        PrintNavbar('myvotes', 0, 0, 'myvotes.cgi', 0)

        (myID, username, usertoken) = GetUserData()
        myID = int(myID)
        if not myID:
                print('<h3>You have to be logged in to view your votes</h3>')
                PrintTrailer('votes', 0, 0)
                sys.exit(0)

        if current_sort_order == 'Vote':
                order_by = 'v.rating desc, t.title_title, t.title_copyright desc'
        elif current_sort_order == 'Title':
                order_by = 't.title_title, t.title_copyright desc, v.rating desc'
        elif current_sort_order == 'Date':
                order_by = 't.title_copyright desc, t.title_title, v.rating desc'
        elif current_sort_order == 'MostRecentVote':
                order_by = 'v.vote_id desc'
        # Get the (next) set of votes.  We join over the titles table to avoid picking
        # up any votes for titles that have been deleted.
        query = """select v.*
                from votes v, titles t
                where v.user_id=%d
                and t.title_id = v.title_id
                order by %s
                limit %d, %d""" % (myID, order_by, start, titles_per_page)
        CNX = MYSQL_CONNECTOR()
        SQLlog("myvotes::query: %s" % query)
        CNX.DB_QUERY(query)
        result_count = CNX.DB_NUMROWS()
        if not result_count:
                print('<h3>No votes present for the specified title range</h3>')
                PrintTrailer('votes', 0, 0)
                sys.exit(0)

        print('<h3>Sorted by %s. You can also sort by %s.</h3>' % (current_sort_order, ' or '.join(alternative_sort_orders)))
        print('<table class="vote_table">')
        print('<tr class="table1">')
        print('<th>Vote</th>')
        print('<th>Title</th>')
        print('<th>Type</th>')
        print('<th>Year</th>')
        print('<th>Author</th>')
        print('</tr>')

        record = CNX.DB_FETCHMANY()
        color = 0
        while record:
                title_id = record[0][1]
                vote = record[0][3]
                title = SQLloadTitle(title_id)
                authors = SQLTitleBriefAuthorRecords(title_id)
                if color:
                        print('<tr align=left class="table1">')
                else:
                        print('<tr align=left class="table2">')
                print('<td>%d</td>' % vote)
                print('<td>%s</td>' % ISFDBLink('title.cgi', title_id, title[TITLE_TITLE]))
                print('<td>%s</td>' % title[TITLE_TTYPE])
                print('<td>%s</td>' % title[TITLE_YEAR])
                print('<td>%s</td>' % FormatAuthors(authors))
                print('</tr>')
                color = color ^ 1
                record = CNX.DB_FETCHMANY()

        print('</table>')
        print('<p>')
        if result_count == titles_per_page:
                print(ISFDBLinkNoName('myvotes.cgi', '%d+%s' % (start + titles_per_page, current_sort_order),
                                      '%d-%d' % (start + titles_per_page, start + (titles_per_page * 2) +1),
                                      True))

        PrintTrailer('myvotes', 0, 0)

