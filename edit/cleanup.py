#!_PYTHONLOC
#
#     (C) COPYRIGHT 2012-2025 Bill Longley, Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 946 $
#     Date: $Date: 2022-07-04 12:24:21 -0400 (Mon, 04 Jul 2022) $


from cleanup_lib import reportsDict
from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *
from sfe3 import Sfe3


class CleanupMenu():
        def __init__(self):
                self.user = User()
                self.user.load()
                self.user.load_moderator_flag()
                self.all_reports = SESSION.Parameter(0, 'int', 0, (0, 1))
                if self.all_reports == 1 and not self.user.moderator:
                        self.all_reports = 0
                self.counts = {}
                self.displayed_sections = []
                self.weeklies = ()
                self.monthlies = ()

        def load_report_definitions(self):
                (self.reports, self.sections, self.non_moderator, self.weeklies, self.monthlies) = reportsDict()
                for report_type in list(self.reports.keys()):
                        self.counts[int(report_type)] = 0
                        # Report 199 is temporary and not regenerated nightly
                        if int(report_type) == 199:
                                self.counts[int(report_type)] = 586

        def display_legend(self):
                print('<b>Legend:</b>')
                print('<ul>')
                print("""<li>The numbers in parentheses show how many potentially problematic records were found when each report
                        was last regenerated; the current numbers may be lower.""")

                if self.user.moderator:
                        print("""<li>Reports that can be viewed by non-moderators have asterisks next to their names.
                                <li>Note that non-moderators can't mark records as "ignored".
                                <li>For an explanation of the "ignore" functionality see
                                <a href="%s://%s/index.php/Help:Screen:IgnoreCleanupRecords">this Help page.</a>""" % (PROTOCOL, WIKILOC))
                else:
                        print("""<li>Some cleanup reports allow moderators to mark records as "ignored".
                                 Note that moderators have access to additional reports. """)

                if self.all_reports:
                        print("""<li>Displaying all reports. You can also limit the list to
                                %s.""" % ISFDBLink('edit/cleanup.cgi', '0', 'reports with identified potential problems'))
                else:
                        if self.user.moderator:
                                print("""<li>Only reports with identified potential problems are displayed. You can 
                                also view a %s""" % ISFDBLink('edit/cleanup.cgi', '1', 'full list of reports'))
                print('</ul>')

        def load_record_count(self):
                # Determine the number of outstanding records for each report type that is regenerated every night
                CNX = MYSQL_CONNECTOR()
                query = "select count(*), report_type from cleanup where resolved is null group by report_type"
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        count = record[0][0]
                        report_type = record[0][1]
                        if self.user.moderator or (report_type in self.non_moderator):
                                self.counts[report_type] = count
                        record = CNX.DB_FETCHMANY()

        def build_displayed_sections(self):
                for section in self.sections:
                        report_numbers = section[1]
                        # If there are no reports with identified problems in this section and
                        # the list is limited to reports with identified problems, skip the whole section
                        problems = 0
                        report_count = 0
                        for report_id in report_numbers:
                                problems += self.counts[report_id]
                                if self.counts[report_id] or self.all_reports:
                                        report_count += 1
                        if not problems and not self.all_reports:
                                continue
                        self.displayed_sections.append((section, report_count))

        def display_header(self):
                PrintPreSearch('ISFDB Data Cleanup Reports')
                PrintNavBar('edit/cleanup.cgi', 0)

        def display_list_of_sections(self):
                if self.displayed_sections:
                        print('<ul>')
                        for section in self.displayed_sections:
                                report_count = section[1]
                                section_name = section[0][0]
                                fragment = section_name.replace(' ', '_')
                                plural = 's'
                                if report_count == 1:
                                        plural = ''
                                print('<li><a href="#%s">%s (%d report%s)</a>' % (fragment, section_name, report_count, plural))
                        print('</ul>')

        def display_sections(self):
                for section in self.displayed_sections:
                        section_name = section[0][0]
                        fragment = section_name.replace(' ', '_')
                        print('<h3 id="%s" class="centered">%s</h3>' % (fragment, section_name))
                        report_numbers = section[0][1]
                        for report_id in report_numbers:
                                # Skip reports with no identified problem records unless explicitly
                                # requested to display them
                                if not self.counts[report_id] and not self.all_reports:
                                        continue
                                if report_id in self.weeklies:
                                        weekly = '(weekly) '
                                else:
                                        weekly = ''
                                if self.user.moderator and report_id in self.non_moderator:
                                        non_mod_flag = ' *'
                                else:
                                        non_mod_flag = ''
                                print(ISFDBLink('edit/cleanup_report.cgi', report_id,
                                                '%s %s(%d)%s' % (self.reports[report_id],
                                                                 weekly, self.counts[report_id], non_mod_flag),
                                                False, 'class="button"'))
                                print('<p>')
                        print('<hr>')

        def display_other_sources(self):
                print('<h3 class="centered">Reconciliation with Other Sources</h3>')
                sfe3 = Sfe3()
                print(ISFDBLink('edit/sfe3_authors.cgi', '',
                                'SFE Author Articles without Matching ISFDB Author Records (%d)' % sfe3.count_of_unresolved(),
                                False, 'class="button"'))
                print('<p>')
                print('<hr>')

                print('<h3 class="centered">Reports That Are Not Regenerated Nightly</h3>')

                if self.user.moderator:
                        # Determine the number of suspect pub images
                        CNX = MYSQL_CONNECTOR()
                        query = "select count(*) from bad_images"
                        CNX.DB_QUERY(query)
                        record = CNX.DB_FETCHONE()
                        if int(record[0][0]) or self.all_reports:
                                print(ISFDBLink('mod/bad_images.cgi', '',
                                                'Publications with Suspect Images (%d)' % int(record[0][0]),
                                                False, 'class="button"'))
                                print('<p>')

                print(ISFDBLink('edit/numeric_external_id_ranges.cgi', '',
                                'View Ranges of Numeric External Identifiers',
                                False, 'class="button"'))
                print('<p>')

if __name__ == '__main__':
        menu = CleanupMenu()
        menu.load_report_definitions()
        menu.load_record_count()
        menu.build_displayed_sections()

        menu.display_header()
        menu.display_legend()
        menu.display_list_of_sections()
        menu.display_sections()
        menu.display_other_sources()

        PrintPostSearch(0, 0, 0, 0, 0, 0)
