#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2013/06/03 06:31:14 $


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

	# Find all duplicate rows in the title_relationships table
	query_main = "select * from title_relationships group by title_id,review_id having count(*)>1 order by review_id;"
	db.query(query_main)
	result_main = db.store_result()
	row = result_main.fetch_row(0)
	print len(row)
	count = 0
	for record in row:
            print record
            count += 1
            # Remove ALL rows for this title/review combination
            delete = "delete from title_relationships where title_id=%d and review_id=%d;" % (int(record[1]), int(record[2]))
            print delete
            db.query(delete)
            # Insert a new record for this title/review combination into the table
            insert = "insert into title_relationships (title_id, review_id) values(%d,%d);" % (int(record[1]), int(record[2]))
            print insert
            db.query(insert)
        print "Total duplicate title_relationship entries processed : %d" % (count)
