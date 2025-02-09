#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019-2021   Ahasuerus
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

        pub_id = SESSION.Parameter(0, 'int')

	PrintHeader('Publication Edit History')
	PrintNavbar('pub_history', 0, 0, 'pub_history.cgi', pub_id)

        print """<h3>The list below displays the following types of submissions: Edit Publication,
                Delete Publication, Import Titles, Remove Titles. The submission which created
                this publication is displayed if the publication was created after 2016-10-24.</h3>"""

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d, %d, %d, %d)
                order by sub_reviewed desc
                """ % (pub_id, MOD_PUB_NEW, MOD_PUB_CLONE, MOD_PUB_UPDATE, MOD_RMTITLE, MOD_PUB_DELETE)
	db.query(query)
	result = db.store_result()
	if not result.num_rows():
		print '<h3>No submission data on file for this publication.</h3>'
        else:
                ISFDBprintSubmissionTable(result, 'I')

	PrintTrailer('pub_history', 0, 0)

