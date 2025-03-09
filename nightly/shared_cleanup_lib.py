#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 861 $
#     Date: $Date: 2022-03-07 15:31:47 -0500 (Mon, 07 Mar 2022) $

from SQLparsing import *
from library import *

class elapsedTime:
        def __init__(self):
                self.start = time()
                # Save the system stdout
                self.stdout = sys.stdout
                # Only print a message if the execution time of a report exceeds this threshold
                self.threshold = 0

        def print_elapsed(self, report_name, record_count = 0):
                sys.stdout = self.stdout
                elapsed = time() - self.start
                if elapsed > self.threshold:
                        print('%s: Rpt %s: %.2f seconds, %d records' % (strftime('%H:%M:%S', localtime()), report_name, elapsed, record_count))
                self.start = time()

def standardDelete(report_type):
        # Delete unresolved cleanup records for this report number/type
        query = 'delete from cleanup where resolved IS NULL and report_type = %d' % int(report_type)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)

def standardReport(query, report_type):
        elapsed = elapsedTime()
        standardDelete(report_type)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()

        records = []
        while record:
                records.append(record[0][0])
                record = CNX.DB_FETCHMANY()

        standardReportInsert(records, report_type)
        elapsed.print_elapsed(report_type, len(records))

def standardReportFromList(id_list, report_type):
        elapsed = elapsedTime()
        standardDelete(report_type)
        standardReportInsert(id_list, report_type)
        elapsed.print_elapsed(report_type)

def standardReportInsert(id_list, report_type):
        # First remove previously resolved/ignored records from the passed-in list of IDs
        query = "select record_id from cleanup where report_type=%d and resolved=1" % int(report_type)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        while record:
                resolved_id = record[0][0]
                if resolved_id in id_list:
                        id_list.remove(resolved_id)
                record = CNX.DB_FETCHMANY()

        # Next add the new IDs to the cleanup table
        for record_id in id_list:
                update = "insert into cleanup (record_id, report_type) values(%d, %d)" % (int(record_id), int(report_type))
                CNX.DB_QUERY(update)
