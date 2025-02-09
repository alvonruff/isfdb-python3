#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2023   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1121 $
#     Date: $Date: 2023-05-18 16:31:48 -0400 (Thu, 18 May 2023) $


from isfdb import *
from isfdblib import *
from SQLparsing import *
from login import *
from library import *


class Form:
        def __init__(self):
                self.dropped_records = []
                self.form_data = None
                self.MaxRecords = 0
                self.parent_id = None
                self.payload = ''
                self.records = []
                self.targetID = 1000000000

        def get_form_data(self):
        	self.form_data = cgi.FieldStorage()

        def parse_form_data(self):
                # Retrieve all submitted IDs starting with "record" and sort them by number
                keys_dict = {}
                for key in self.form_data.keys():
                        if not key.startswith('record'):
                                continue
                        key_number = int(key.split('record')[1])
                        keys_dict[key_number] = ''

                # Retrieve the values of all submitted "record" IDs and put them into the "records" list
                for key in sorted(keys_dict.keys()):
                        target = "record%d" % (key)
                        self.records.append(int(self.form_data[target].value))
                        if self.records[self.MaxRecords] < self.targetID:
                                self.targetID = self.records[self.MaxRecords]
                        self.MaxRecords += 1

        def build_header(self):
                self.add_payload_line('<?xml version="1.0" encoding="%s" ?>\n' % UNICODE)
                self.add_payload_line('<IsfdbSubmission>\n')
                self.add_payload_line('  <TitleMerge>\n')

        def build_ids(self):
                index = 0
                while index < self.MaxRecords:
                        if self.records[index] == self.targetID:
                                self.add_payload_line('    <KeepId>%d</KeepId>\n' % self.records[index])
                        else:
                                self.add_payload_line('    <DropId>%d</DropId>\n' % self.records[index])
                                self.dropped_records.append(self.records[index])
                        index += 1

        def build_submit_data(self):
                titlename = SQLgetTitle(form.targetID)
                submitter = getSubmitter()
                self.add_payload_line('    <Submitter>%s</Submitter>\n' % (db.escape_string(XMLescape(submitter))))
                self.add_payload_line('    <Subject>%s</Subject>\n' % (db.escape_string(XMLescape(titlename))))

        def add_column(self, column, tag):
                if self.form_data.has_key(column):
                        value = self.form_data[column].value
                        index = int(value)-1
                        record_id = int(self.records[index])
                        self.add_payload_line('    <%s>%d</%s>\n' % (tag, record_id, tag))
                        if column == 'title_parent':
                                parent_title = SQLloadTitle(record_id)
                                self.parent_id = parent_title[TITLE_PARENT]

        def add_mod_note(self):
                if self.form_data.has_key('mod_note'):
                        mod_note = self.form_data['mod_note'].value
                        self.add_payload_line('    <ModNote>%s</ModNote>\n' % (db.escape_string(XMLescape(mod_note))))

        def build_footer(self):
                self.add_payload_line(' </TitleMerge>\n')
                self.add_payload_line('</IsfdbSubmission>\n')

        def add_payload_line(self, line):
                self.payload += line

        def self_parent(self):
                if self.parent_id and (self.parent_id == self.targetID):
                        return 1
                return 0

        def dropped_parent(self):
                if self.parent_id and (self.parent_id in self.dropped_records):
                        return 1
                return 0

if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Title Merge Results'
        submission.cgi_script = 'tv_merge'
        submission.type = MOD_TITLE_MERGE

        if not submission.user.id:
                submission.error()

        form = Form()
        form.get_form_data()
        form.parse_form_data()
        if not form.MaxRecords:
                submission.error()
        form.build_header()
        form.build_ids()
        form.build_submit_data()
        form.add_column('title_title',     'Title')
        form.add_column('title_author',    'Author')
        form.add_column('title_year',      'Year')
        form.add_column('title_series',    'Series')
        form.add_column('title_seriesnum', 'Seriesnum')
        form.add_column('title_storylen',  'Storylen')
        form.add_column('title_content',   'ContentIndicator')
        form.add_column('title_jvn',       'Juvenile')
        form.add_column('title_nvz',       'Novelization')
        form.add_column('title_non_genre', 'NonGenre')
        form.add_column('title_graphic',   'Graphic')
        form.add_column('title_language',  'Language')
        form.add_column('title_ttype',     'TitleType')
        form.add_column('title_synop',     'Synopsis')
        form.add_column('title_note',      'Note')
        form.add_column('title_parent',    'Parent')
        form.add_mod_note()
        form.build_footer()
        if form.self_parent():
                submission.error('This submission would result in a title that is a parent of itself, which is not allowed')
        if form.dropped_parent():
                submission.error('Specified parent title would be dropped, which would result in a title record with a non-existent parent')

	submission.file(form.payload)
