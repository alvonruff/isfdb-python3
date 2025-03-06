#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2019-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 582 $
#     Date: $Date: 2020-12-25 17:51:33 -0500 (Fri, 25 Dec 2020) $


import cgi
import sys
from SQLparsing import *
from isfdb import *
from library import *
from isfdblib import *


class ExternalIdRanges:
        def __init__(self):
                self.types_with_ranges = {}
                self.ranges = {}
                self.load_types_with_ranges()
                self.in_clause = dict_to_in_clause(self.types_with_ranges)
                self.id_values = {}

        def load_types_with_ranges(self):
                # Create a disctionary of External ID Type Names/IDs for types that have meaningful ranges
                # At this time only the two Reginald ID types and the 3 Bleiler ID types are eligible
                all_types = SQLLoadIdentifierTypes()
                for type_number in all_types:
                        type_name = all_types[type_number][0]
                        if 'Reginald' in type_name or 'Bleiler' in type_name:
                                self.types_with_ranges[type_number] = type_name
                                self.ranges[type_name] = []

        def load_ids(self):
                query = """select distinct identifier_type_id, CAST(identifier_value as UNSIGNED)
                        from identifiers
                        where identifier_type_id in (%s)
                        and identifier_value regexp '^[[:digit:]]{1,30}$'
                        order by CAST(identifier_value as UNSIGNED)""" % self.in_clause
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        type_number = record[0][0]
                        type_name = self.types_with_ranges[type_number]
                        id_value = record[0][1]
                        if type_name not in self.id_values:
                                self.id_values[type_name] = []
                        self.id_values[type_name].append(id_value)
                        record = CNX.DB_FETCHMANY()

        def create_ranges(self):
                for type_name in sorted(self.id_values):
                        range_start = 1
                        if self.id_values[type_name]:
                                range_start = self.id_values[type_name][0]
                        range_end = range_start
                        for id_value in self.id_values[type_name][1:]:
                                # If this value continues the current range, reset the range end point
                                if (id_value - 1) == range_end:
                                        range_end = id_value
                                # If this is the start of a new ID range, save the old range
                                else:
                                        self.ranges[type_name].append((range_start, range_end))
                                        range_start = id_value
                                        range_end = id_value
                        # Save the last found ID range
                        self.ranges[type_name].append((range_start, range_end))

        def display_ranges(self):
                for type_name in sorted(self.ranges):
                        bgcolor = 0
                        print('<h3>%s</h3>' % type_name)
                        print('<table class="externalidranges">')
                        count = 0
                        for range_span in self.ranges[type_name]:
                                count += 1
                                if (count % 10) == 1:
                                        print('<tr class="table%d">' % (bgcolor + 1))
                                        bgcolor ^= 1
                                range_start = range_span[0]
                                range_end = range_span[1]
                                print('<td>')
                                print(range_start)
                                if range_end != range_start:
                                        print(' - ', range_end)
                                print('</td>')
                                if (count % 10) == 0:
                                        print('</tr>')
                        if count % 10:
                                for i in range(count % 10, 10):
                                        print('<td>')
                                        print('&nbsp;')
                                        print('</td>')
                        print('</table>')

if __name__ == '__main__':

        PrintPreSearch('Numeric External Identifier Ranges')
        PrintNavBar('edit/numeric_external_id_ranges.cgi', 0)

        external_id_ranges = ExternalIdRanges()
        external_id_ranges.load_ids()
        external_id_ranges.create_ranges()
        external_id_ranges.display_ranges()
        PrintPostSearch(0, 0, 0, 0, 0, 0)
