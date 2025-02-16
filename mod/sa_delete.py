#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2009-2025   Ahasuerus, Klaus Elsbernd, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 750 $
#     Date: $Date: 2021-09-16 16:51:32 -0400 (Thu, 16 Sep 2021) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Series Delete - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('SeriesDelete'):
                merge = doc.getElementsByTagName('SeriesDelete')
                Record = GetElementValue(merge, 'Record')
                
                #Check if the series has already been deleted
                seriesRecord = SQLget1Series(int(Record))
                if seriesRecord == 0:
                        print('<div id="ErrorBox">')
                        print('<h3>Error: This series no longer exists.</h3>')
                        print('<h3>Please %s to reject it.</h3>' % ISFDBLinkNoName('mod/hardreject.cgi', submission, 'use Hard Reject'))
                        print('</div>')
                        PrintPostMod(0)
                        sys.exit(0)

                # Check if sub-series have been added to this series since the time the submission was created
                subseries = SQLFindSeriesChildren(int(Record))
                if len(subseries) > 0:
                        print('<div id="ErrorBox">')
                        print('<h2>Error: At least one sub-series has been added to this Series since the time this submission was created.</h2>')
                        print("<h2>This series can't be deleted until all sub-series are removed.</h2>")
                        print('<h3>If you do not want to remove the sub-series, please %s to reject the submission.</h3>' % ISFDBLinkNoName('mod/hardreject.cgi', submission, 'use Hard Reject'))
                        print('</div>')
                        PrintPostMod(0)
                        sys.exit(0)

                # Check if titles have been added to this series since the time the submission was created
                titles = SQLloadTitlesXBS(int(Record))
                if len(titles) > 0:
                        print('<div id="ErrorBox">')
                        print('<h2>Error: At least one title has been added to this series since the time this submission was created.</h2>')
                        print("<h2>This series can't be deleted until all titles are removed.</h2>")
                        print('<h3>If you do not want to remove the titles, please %s to reject the submission.</h3>' % ISFDBLinkNoName('mod/hardreject.cgi', submission, 'use Hard Reject'))
                        print('</div>')
                        PrintPostMod(0)
                        sys.exit(0)

                ##########################################################
                # Delete the series
                ##########################################################
                print("<h1>SQL Updates:</h1>")
                print("<hr>")
                print("<ul>")
                update = "delete from series where series_id=%d" % int(Record)
                print("<li> ", update)
                db.query(update)
                delete = 'delete from trans_series where series_id=%d' % int(Record)
                print("<li> ", delete)
                db.query(delete)
                update = "delete from webpages where series_id=%d" % int(Record)
                print("<li> ", update)
                db.query(update)
                if seriesRecord[SERIES_NOTE]:
                        update = "delete from notes where note_id=%d" % (int(seriesRecord[SERIES_NOTE]))
                        print("<li> ", update)
                        db.query(update)
                        
                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission, Record)

        print('<p>')

        PrintPostMod(0)
