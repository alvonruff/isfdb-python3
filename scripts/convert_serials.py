#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2025   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 15 $
#     Date: $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $


import cgi
import sys
import os
import string
import MySQLdb
from localdefs import *

def Date_or_None(s):
    return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)

if __name__ == '__main__':

        db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
        db.select_db(DBASE)
        
        query_main = "select * from titles where title_ttype = 'SERIAL' and title_parent =0;"
        db.query(query_main)
        result_main = db.store_result()
        serials = result_main.fetch_row(0)
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
            query = "select * from titles where title_title = '" + db.escape_string(title)
            query += "' and title_parent = 0 and (title_ttype = 'NOVEL' or title_ttype = 'SHORTFICTION');"
            db.query(query)
            result = db.store_result()
            number_of_matches = result.num_rows()
            #
            # Skip Serials that have no matching Novel/Shortfiction titles
            if number_of_matches == 0:
                continue
            #print number_of_matches
            count_with_matches = count_with_matches + 1
            # Save the Novel/Shortfiction Title record
            novels = result.fetch_row(0)
            #
            # Retrieve the author(s) for this Serial record
            query = "select author_id from canonical_author where title_id = %d;" % (serial_id)
            db.query(query)
            result = db.store_result()
            serial_authors = result.fetch_row(0)[0]
            #
            # Retrieve the authors for the matching Novel/Shortfiction
            novel_id = 0
            for novel in novels:
                query = "select author_id from canonical_author where title_id = %d;" % (novel[0])
                db.query(query)
                result = db.store_result()
                novel_authors = result.fetch_row(0)[0]
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
            print update
            db.query(update)
            #sys.exit(0)
        print "Total non-VT serial records: %d" % (total)
        print "Total well formed serial records: %d" % (count_well_formed)
        print "Total serials with matching Novels/Shortfiction titles: %d" % (count_with_matches)
        print "Total serials with matching authors : %d" % (count_matching_authors)
