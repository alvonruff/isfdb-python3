#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 954 $
#     Date: $Date: 2022-07-10 19:46:14 -0400 (Sun, 10 Jul 2022) $


from isfdb import *
from common import *
from login import *
from SQLparsing import *
from library import *

results_per_page=200


if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)
        sub_type = SESSION.Parameter(1, 'str', 'I', ('I', 'N', 'R', 'P'))

        if sub_type == 'I':
                PrintHeader("My Recent Edits - Last 3 Months")
        elif sub_type == 'N':
                PrintHeader("My Pending Edits")
        elif sub_type == 'R':
                PrintHeader("My Rejected Edits")
        elif sub_type == 'P':
                PrintHeader("My Errored Out Edits")

        PrintNavbar('recent', 0, 0, 'recent.cgi', 0)

        if start:
                print('<p> %s<p>' % ISFDBLinkNoName('myrecent.cgi', '%d+%s' % (start-results_per_page, sub_type), 'NEWER', True))

        (myID, username, usertoken) = GetUserData()

        if sub_type == 'N':
                queuesize = SQLQueueSize()
                print("The current number of pending edits by all editors (not held by a moderator) is %d." % queuesize)

        if sub_type == 'I':
                query = """select * from submissions
                        where sub_state='%s'
                        and sub_submitter=%d
                        and sub_reviewed > DATE_ADD(NOW(), INTERVAL -3 MONTH)
                        order by sub_reviewed desc, sub_id desc
                        limit %d,%d""" % (db.escape_string(sub_type), int(myID), start, results_per_page+1)
        else:
                query = """select * from submissions
                        where sub_state='%s'
                        and sub_submitter=%d
                        order by sub_reviewed desc, sub_id desc
                        limit %d,%d""" % (db.escape_string(sub_type), int(myID), start, results_per_page+1)
        db.query(query)
        result = db.store_result()
        numRows = result.num_rows()
        if numRows == 0:
                print('<h3>No matching submissions present</h3>')
                PrintTrailer('recent', 0, 0)
                sys.exit(0)
        elif sub_type == 'N':
                wikipointer = """<br>If your edits seem to be taking a long time to be approved,
                please check your <a href="%s://%s/index.php/User_talk:%s">Talk page</a>
                for comments or questions.""" % (PROTOCOL, WIKILOC, username)
                print(wikipointer)
        elif sub_type == 'R':
                wikipointer = """The moderator may have left additional comments on your 
                <a href="%s://%s/index.php/User_talk:%s">Talk page</a>.<br>
                Please check your wiki Talk page frequently for comments or questions.""" % (PROTOCOL, WIKILOC, username)
                print(wikipointer)

        ISFDBprintSubmissionTable(result, sub_type)
        
        # Check if there is more since "results_per_page+1" was requested from the database
        if numRows > results_per_page:
                print('<p>')
                print(ISFDBLinkNoName('myrecent.cgi', '%d+%s' % (start+results_per_page, sub_type), 'OLDER', True))
        PrintTrailer('recent', 0, 0)

