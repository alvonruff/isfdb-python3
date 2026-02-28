#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2020-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 528 $
#     Date: $Date: 2020-05-13 17:06:08 -0400 (Wed, 13 May 2020) $


from isfdb import *
from common import *
from isfdblib import *
from library import *
from SQLparsing import *


if __name__ == '__main__':

        sub_id = SESSION.Parameter(0, 'int')
        sub_data = SQLloadSubmission(sub_id)
        if not sub_data:
                SESSION.DisplayError('Specified submission ID does not exist')

        if sub_data[SUB_STATE] != 'R':
                SESSION.DisplayError('This submission is not in the Rejected state')

        PrintPreMod('UnReject Submission')
        PrintNavBar()

        update = """update submissions
                set sub_state='N', sub_reason=NULL, sub_reviewer=0, sub_reviewed=NULL, sub_holdid=0
                where sub_id=%d""" % int(sub_id)
        print('<ul>')
        print('<li> ', update)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)
        print('</ul>')
        print('<p>')
        print(ISFDBLink('view_submission.cgi', sub_id, 'View Submission'))
        PrintPostMod(0)
