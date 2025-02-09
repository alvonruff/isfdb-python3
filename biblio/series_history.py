#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus
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

        series_id = SESSION.Parameter(0, 'int')
	PrintHeader('Series Edit History')
	PrintNavbar('series_history', 0, 0, 'series_history.cgi', series_id)

        print """<h3>The list below displays the following types of submissions:
                Edit Series, Delete Series. Note that series records are created
                automatically when title records are created/edited; related
                submissions are not displayed on this page.</h3>"""

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d)
                order by sub_reviewed desc
                """ % (series_id, MOD_SERIES_UPDATE, MOD_DELETE_SERIES)
	db.query(query)
	result = db.store_result()
	if not result.num_rows():
		print '<h3>No submission data on file for this series</h3>'
        else:
                ISFDBprintSubmissionTable(result, 'I')

	PrintTrailer('series_history', 0, 0)

