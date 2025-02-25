#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 751 $
#     Date: $Date: 2021-09-17 17:33:29 -0400 (Fri, 17 Sep 2021) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from common import Queue
import cgi


if __name__ == '__main__':

        form = IsfdbFieldStorage()
        try:
                submitter_name = form['submitter_name'].value
        except:
                SESSION.DisplayError('User name not specified')

        try:
                status = form['status'].value
        except:
                SESSION.DisplayError('Status must be specified')

        if status == 'Approved':
                status_flag = 'I'
        elif status == 'Pending':
                status_flag = 'N'
        elif status == 'Rejected':
                status_flag = 'R'
        else:
                SESSION.DisplayError('Status must be "Approved" or "Rejected"')

        submitter_id = SQLgetSubmitterID(submitter_name)
        if not submitter_id:
                SESSION.DisplayError('An ISFDB user with this name does not exist. Note that user names are case sensitive and the first letter is always capitalized.')

        try:
                start = int(form['start'].value)
        except:
                start = 0

        PrintPreMod('Submission Search Results')
        PrintNavBar()

        if status_flag in ('I', 'R'):
                query = """select *
                        from submissions
                        where sub_submitter = %d
                        and sub_state = '%s'
                        order by sub_reviewed desc
                        limit %d, 200""" % (submitter_id, status_flag, start)

                db.query(query)
                result = db.store_result()
                if result.num_rows() == 0:
                        print('<h3>No submissions present for the specified search criteria.</h3>')
                else:
                        print('<h3>%s submissions created by user %s (%d - %d)</h3>' % (status, submitter_name, start+1, start+200))
                        ISFDBprintSubmissionTable(result, status_flag)
                        if result.num_rows() > 199:
                                print('<p> %s' % ISFDBLinkNoName('mod/submission_search_results.cgi',
                                                                 'submitter_name=%s&amp;start=%d&amp;status=%s' % (submitter_name, start+200, status),
                                                                 'Next page (%d - %d)' % (start+201, start+400), True))
        else:
                print('<h3>Pending submissions created by user %s</h3>' % submitter_name)
                queue = Queue()
                queue.display_pending_for_editor(submitter_id)

        PrintPostMod(0)

