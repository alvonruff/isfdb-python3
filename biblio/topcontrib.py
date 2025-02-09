#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2022   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 862 $
#     Date: $Date: 2022-03-08 11:57:29 -0500 (Tue, 08 Mar 2022) $


from isfdb import *
from common import *
from SQLparsing import *


def output_data(sub_type):
	query = 'select report_data from reports where report_id = 3 and report_param = %d' % sub_type
	db.query(query)
        result = db.store_result()
        if result.num_rows():
                record = result.fetch_row()
                print record[0][0]
        else:
                print '<h3>This report is currently unavailable. It is regenerated once a week.</h3>'

if __name__ == '__main__':

        sub_type = SESSION.Parameter(0, 'int', 0)

	PrintHeader('Top Contributors')
	PrintNavbar('top', 0, 0, 'topcontrib.cgi', 0)

	if sub_type == 0:
		print '<h2>Top ISFDB contributors (All Submission Types)</h2>'
		print '<h3>This report is generated once a week</h3>'
		output_data(0)
	elif sub_type in SUBMAP and SUBMAP[sub_type][3]:
                print '<h2>Top ISFDB contributors (%s)</h2>' % (SUBMAP[sub_type][3])
                print '<h3>This report is generated once a week</h3>'
                output_data(sub_type)
        else:
		print '<h3>Specified submission type is currently inactive</h3>'
        	PrintTrailer('top', 0, 0)
		sys.exit(0)

	PrintTrailer('top', 0, 0)

