#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 735 $
#     Date: $Date: 2021-09-06 16:25:55 -0400 (Mon, 06 Sep 2021) $

	
from isfdb import *
from isfdblib import *
from SQLparsing import *
	
if __name__ == '__main__':

        series_id = SESSION.Parameter(0, 'int')
	seriesRecord = SQLget1Series(series_id)
	if not seriesRecord:
                SESSION.DisplayError('Record Does Not Exist')
	
	PrintPreSearch('Delete Series Submission')
	PrintNavBar('edit/deleteseries.cgi', series_id)

	# Find sub-series of this series
	subseries = SQLFindSeriesChildren(series_id)
	# Find any titles that belong to this series
	titles = SQLloadTitlesXBS(series_id)
        seriesname = SQLgetSeriesName(series_id)

	if subseries:
		print '<h2>Error: Series with sub-series cannot be deleted until all sub-series have been removed.</h2>'
		print '<h2>This series still has %d sub-series.</h2>' % len(subseries)

        elif titles:
		print '<h2>Error: Non-empty series can\'t be deleted.</h2>'
		print '<h2>This series still has %d titles:</h2>' % len(titles)
		print '<ul>'
		for title in titles:
			print '<li>'
                        print '%s (%s)' % (ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE]), title[TITLE_YEAR])
		print '</ul>'
        else:
                print '<b>Request to Delete:</b> <i>%s</i>' % seriesname
                print '<form METHOD="POST" ACTION="/cgi-bin/edit/submitdelseries.cgi">'
                print '<p>'
                print '<b>Deletion Reason</b><br>'
                print '<textarea name="reason" rows="4" cols="45"></textarea>'
                print '<p>'
                print '<input name="series_id" value="%d" type="HIDDEN">' % series_id
                print '<input name="series_name" value="%s" type="HIDDEN">' % seriesname
                print '<input type="SUBMIT" value="Delete">'
                print '</form>'
	
	PrintPostSearch(0, 0, 0, 0, 0, 0)
