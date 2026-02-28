#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2009-2026   Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1264 $
#         Date: $Date: 2026-02-21 11:58:41 -0500 (Sat, 21 Feb 2026) $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        query_main = "select * from titles where title_ttype = 'SERIAL' and title_parent =0;"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query_main)
        serials = CNX.DB_FETCHONE()
        count_well_formed = 0
        total = 0
        count_with_matches = 0
        count_matching_authors = 0
        for serial in serials:
                total = total + 1
                found = 0
                serial_title = serial[1]
                serial_id = serial[0]
                # Check if this Serial's title follows the standard naming convention
                if serial_title.find("(Complete Novel)") > -1:
                        found = 1
                if serial_title.find("(Part ") > -1:
                        found = 1
                # If this Serial's title doesn't follow the standard naming conventions, skip it
                if found == 0:
                        continue
                count_well_formed = count_well_formed + 1
                #
                # Strip " (Complete Novel") and " (Part X of Y)"
                title = serial_title.split(" (Part ")[0]
                title = title.split(" (Complete Novel")[0]
                #
                # Now find all Novels/Shortfiction that match this Serial's title
                query = "select * from titles where title_title = '" + CNX.DB_ESCAPE_STRING(title)
                query += "' and title_parent = 0 and (title_ttype = 'NOVEL' or title_ttype = 'SHORTFICTION');"
                CNX.DB_QUERY(query)
                number_of_matches = CNX.DB_NUMROWS()
                #
                # Skip Serials that have no matching Novel/Shortfiction titles
                if number_of_matches == 0:
                        continue
                #print number_of_matches
                count_with_matches = count_with_matches + 1
                # Save the Novel/Shortfiction Title record
                novels = CNX.DB_FETCHONE()
                #
                # Retrieve the author(s) for this Serial record
                query = "select author_id from canonical_author where title_id = %d;" % (serial_id)
                CNX.DB_QUERY(query)
                serial_authors = CNX.DB_FETCHONE()[0]
                #
                # Retrieve the authors for the matching Novel/Shortfiction
                novel_id = 0
                for novel in novels:
                        query = "select author_id from canonical_author where title_id = %d;" % (novel[0])
                        CNX.DB_QUERY(query)
                        novel_authors = CNX.DB_FETCHONE()[0]
                        # If the number of Serial authors doesn't match the number of Novel/SF authors, skip this Novel
                        if len(serial_authors) != len(novel_authors):
                                continue
                        # Check whether all Serial Authors match the Novel/SF authors
                        skip_novel = 0
                        for author in serial_authors:
                                if author not in novel_authors:
                                        skip_novel = 1
                        if skip_novel:
                                continue
                        #
                        # Save the found matching Novel/SF ID in "novel_id"
                        novel_id = novel[0]
                # If no Novel/SF with matching authors was found, skip this Serial
                if novel_id == 0:
                        continue
                count_matching_authors = count_matching_authors + 1
                update = "update titles set title_parent = %d where title_id = %d" % (novel_id,serial_id)
                print(update)
                if debug == 0:
                        CNX.DB_QUERY(update)
                #sys.exit(0)
        print("Total non-VT serial records: %d" % (total))
        print("Total well formed serial records: %d" % (count_well_formed))
        print("Total serials with matching Novels/Shortfiction titles: %d" % (count_with_matches))
        print("Total serials with matching authors : %d" % (count_matching_authors))
