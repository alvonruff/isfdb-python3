#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2026   Al von Ruff, Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1258 $
#     Date: $Date: 2026-02-13 16:16:41 -0500 (Fri, 13 Feb 2026) $


import sys
import os
import string
from SQLparsing import *
from biblio import *

class Stats:
        def __init__(self):
                self.headers = {
                                1: 'Top Moderators',
                                2: 'Top Verifiers',
                                4: 'ISFDB Statistics',
                                5: 'Titles by Year of First Publication',
                                6: 'Publications by Year',
                                7: 'Titles by Author Age',
                                8: 'Percent of Titles in Series by Year',
                                9: 'Percent of Book Titles by Type by Year',
                                10: 'Percent of Publications by Format by Year',
                                11: 'Submissions per Year',
                                12: 'Top Novels as Voted by ISFDB Users',
                                13: 'Most-Viewed Authors',
                                14: 'Most-Viewed Novels',
                                15: 'Most-Viewed Short Fiction',
                                16: 'Oldest Living Authors',
                                17: 'Oldest Non-Living Authors',
                                18: 'Youngest Living Authors',
                                19: 'Youngest Non-Living Authors',
                                20: 'Authors by Working Language',
                                21: 'Titles by Language',
                                22: 'Top Taggers',
                                23: 'Top Voters',
                                24: 'Top Forthcoming',
                                25: 'Top Short Fiction Titles as Voted by ISFDB Users'
                                }

        def params(self):
                self.report_id = SESSION.Parameter(0, 'int')
                self.header = self.headers.get(self.report_id, '')
                if not self.header:
                        SESSION.DisplayError('Invalid Report Number')

        def output(self):
                query = 'select report_data from reports where report_id = %d' % stats.report_id
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                if CNX.DB_NUMROWS():
                        print('<h3>This report is generated once a week</h3>')
                        record = CNX.DB_FETCHONE()
                        print(record[0][0])
                else:
                        print('<h3>This report is currently unavailable. It will be regenerated later.</h3>')

if __name__ == '__main__':

        stats = Stats()
        stats.params()
        PrintHeader(stats.header)
        PrintNavbar('stats', 0, 0, 'stats.cgi', 0)
        stats.output()
        PrintTrailer('frontpage', 0, 0)
