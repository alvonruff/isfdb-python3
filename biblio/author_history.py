#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2021-2026   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2019-12-01 19:57:53 -0400 (Tue, 31 Oct 2017) $


from isfdb import *
from common import *
from login import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        author_id = SESSION.Parameter(0, 'int')

        user = User()
        user.load()
        if not user:
                SESSION.DisplayError('Only ISFDB moderators can view author edit history at this time')
        user.load_moderator_flag()
        if not user.moderator:
                SESSION.DisplayError('Only ISFDB moderators can view author edit history at this time')

        PrintHeader('Author Edit History')
        PrintNavbar('author_history', 0, 0, 'author_history.cgi', author_id)

        print("""<h3>The list below displays Edit Author, Merge Authors and Make/Remove
                Alternate Name submissions. Note that author records are created and
                deleted automatically when publications and titles are created/edited/deleted;
                related submissions are not displayed on this page.</h3>""")

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d, %d, %d)
                order by sub_reviewed desc
                """ % (author_id, MOD_AUTHOR_UPDATE, MOD_AUTHOR_PSEUDO, MOD_REMOVE_PSEUDO, MOD_AUTHOR_MERGE)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        SQLlog("author_history::query: %s" % query)
        if not CNX.DB_NUMROWS():
                print('<h3>No submission data on file for this author</h3>')
        else:
                ISFDBprintSubmissionTable(CNX, 'I')

        PrintTrailer('author_history', 0, 0)
