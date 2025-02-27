#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2020-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2019-12-01 19:57:53 -0400 (Tue, 31 Oct 2017) $


from isfdb import *
from common import *
from SQLparsing import *


if __name__ == '__main__':

        title_id = SESSION.Parameter(0, 'int')

        PrintHeader('Title Edit History')
        PrintNavbar('title_history', 0, 0, 'title_history.cgi', title_id)

        print("""<h3>The list below displays all Edit Title, Make Variant, 
                Delete Title, Title Merge, Title Unmerge, and Link Review submissions
                for this title record. Add Variant Title submissions are listed if
                approved after 2021-01-11. Note that title records are created
                automatically when publications are created/edited; related
                submissions are not displayed on this page.</h3>""")

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d, %d, %d, %d, %d, %d)
                order by sub_reviewed desc
                """ % (title_id, MOD_TITLE_UPDATE, MOD_TITLE_DELETE,
                       MOD_TITLE_MKVARIANT, MOD_REVIEW_LINK,
                       MOD_VARIANT_TITLE, MOD_TITLE_UNMERGE, MOD_TITLE_MERGE)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        if not CNX.DB_NUMROWS():
                print('<h3>No submission data on file for this title.</h3>')
        else:
                ISFDBprintSubmissionTable(CNX, 'I')

        PrintTrailer('title_history', 0, 0)

