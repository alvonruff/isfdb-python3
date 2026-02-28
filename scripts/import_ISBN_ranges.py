#!_PYTHONLOC
from __future__ import print_function
#     (C) COPYRIGHT 2024-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 335 $
#     Date: $Date: 2019-02-09 15:35:36 -0500 (Sat, 09 Feb 2019) $

# import sys
import xml.etree.ElementTree as ET
from SQLparsing import *

debug = 0

class Process():
        def __init__(self):
                self.file_name = 'ISBN_ranges.xml'
                self.ranges = []

        def import_all(self):
                self.import_isbn_ranges()
                self.file_isbn_ranges()

        def import_isbn_ranges(self):
                range_count = 0
                registration_groups = 0
                for (event, node) in ET.iterparse(self.file_name, ('start', 'end')):
                        if node.tag == 'RegistrationGroups':
                                registration_groups = 1
                                continue
                        elif not registration_groups:
                                continue

                        if event == 'end':
                                if node.tag == 'Prefix':
                                        prefix = node.text.replace('-','')
                                elif node.tag == 'Range':
                                        range = node.text.split('-')
                                        start_value = '%s%s' % (prefix, range[0][:11-len(prefix)])
                                        end_value = '%s%s' % (prefix, range[1][:11-len(prefix)])
                                elif node.tag == 'Length':
                                        length = node.text
                                elif node.tag == 'Rule':
                                        if length != '0':
                                                self.ranges.append((int(start_value), int(end_value), len(prefix), int(length)),)
                                                range_count += 1

        def file_isbn_ranges(self):
                truncate = 'truncate table isbn_ranges'
                CNX = MYSQL_CONNECTOR()
                if debug == 0:
                        CNX.DB_QUERY(truncate)
                else:
                        print(truncate)

                insert = 'INSERT INTO isbn_ranges (start_value, end_value, prefix_length, publisher_length) VALUES'
                for range in self.ranges:
                        insert += '(%d, %d, %d, %d),' % (range[0], range[1], range[2], range[3])
                insert = insert[:-1]
                if debug == 0:
                        CNX.DB_QUERY(insert)
                else:
                        print(insert)

if __name__ == '__main__':
        process = Process()
        process.import_all()

