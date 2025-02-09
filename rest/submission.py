#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2023   Al von Ruff, Ahasuerus and Dirk Stoecker
#	 ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1135 $
#     Date: $Date: 2023-06-29 19:33:23 -0400 (Thu, 29 Jun 2023) $

import cgi
import sys
from isfdb import *
from SQLparsing import *
from library import normalizeInput, XMLunescape, XMLescape
from login import User
from xml.dom import minidom
from xml.dom import Node
	

class Submission:
        def __init__ (self):
                self.doc = ''
                self.holder = ''
                self.holder_id = 0
                self.merge = ''
                self.submitter = ''
                self.submitter_id = 0
                self.submission_id = ''
                self.valid_submitters = []
                web_api_user_data = SQLGetWebAPIUsers()
                for web_api_user in web_api_user_data:
                        self.valid_submitters.append(web_api_user[1])
                self.XMLdata = ''

        def process_submission(self):
                self.get_input()
                self.get_submitter()
                self.get_license()
                self.get_holder()
                self.remove_API_fields()
                self.normalize_input()
                self.file_submission()

        def get_input(self):
                input = sys.stdin.read()
                index = string.find(input, "<?xml ")
                self.XMLdata = input[index:]
                try:
                        self.doc = minidom.parseString(self.XMLdata)
                        sub.merge = self.doc.getElementsByTagName('IsfdbSubmission')
                        if not self.merge:
                                raise
                except:
                        self.send_error('Malformed XML data.', 400)

        def get_submitter(self):
                self.submitter = self.get_element_value('Submitter')
                if not self.submitter:
                        self.send_error('No Submitter Field.', 401)
                if self.submitter not in self.valid_submitters:
                        self.send_error("""This user is not authorized to create submissions via the ISFDB Web API.
                                        Post on the ISFDB Moderator Noticeboard if you need access.""", 403)
                try:
                        self.submitter_id = int(SQLgetSubmitterID(self.submitter))
                        if not self.submitter_id:
                                raise
                except:
                        self.send_error('Invalid submitter.', 403)

        def get_license(self):
                key = self.get_element_value('LicenseKey')
                if key == '':
                        self.send_error('No LicenseKey Field.', 403)
                query = "select * from license_keys where user_id=%d and license_key='%s'" % (self.submitter_id, db.escape_string(key))
                db.query(query)
                result = db.store_result()
                if result.num_rows() == 0:
                        self.send_error('Invalid License Key.', 403)

        def get_holder(self):
                self.holder = self.get_element_value('Holder')
                if not self.holder:
                        return
                try:
                        self.holder_id = int(SQLgetSubmitterID(self.holder))
                        if not self.holder_id:
                                raise
                except:
                        self.send_error('Invalid holding moderator.', 422)
                if not SQLisUserModerator(self.holder_id):
                        self.send_error('Specified holder is not a moderator.', 422)

        def remove_API_fields(self):
                self.delete_field('LicenseKey')
                self.delete_field('Holder')

        def normalize_input(self):
                try:
                        pieces = self.XMLdata.split('>')
                        new_pieces = []
                        for piece in pieces:
                                if not piece:
                                        continue
                                subpieces = piece.split('<')
                                if len(subpieces) !=2:
                                        continue
                                data = subpieces[0]
                                tag = subpieces[1]
                                unescaped_data = XMLunescape(data, 1)
                                normalized_data = normalizeInput(unescaped_data)
                                # second parameter controls the use of ISFDB-specific non-XML-standard aspostrophe encoding
                                re_escaped_data = XMLescape(normalized_data, 0)
                                new_piece = re_escaped_data + '<' + tag
                                new_pieces.append(new_piece)
                        result = '>'.join(new_pieces)
                        self.XMLdata = result.replace('><', '> <') + '>'
                except:
                        self.send_error('XML parsing failed', 400)

        def file_submission(self):
                for sub_type in SUBMAP:
                        merge = self.doc.getElementsByTagName(SUBMAP[sub_type][1])
                        if merge:
                                if self.holder_id:
                                        submission = """insert into submissions(sub_state, sub_type, sub_data, sub_time, sub_submitter, sub_holdid)
                                                        values('N', %d, '%s', NOW(), %d, %d)""" % (sub_type, db.escape_string(self.XMLdata), self.submitter_id, self.holder_id)
                                else:
                                        submission = """insert into submissions(sub_state, sub_type, sub_data, sub_time, sub_submitter)
                                                        values('N', %d, '%s', NOW(), %d)""" % (sub_type, db.escape_string(self.XMLdata), self.submitter_id)
                                db.query(submission)
                                self.submission_id = db.insert_id()
                                self.send_success()
                self.send_error('Unknown Submission Type.', 422)

        def send_error(self, error, code = 200):
                self.response_headers(code)
                print('<Status>FAIL</Status>')
                print('<Error>%s</Error>' % error)
                self.response_footers()

        def send_success(self):
                self.response_headers()
                print('<Status>OK</Status>')
                print('<SubmissionID>%s</SubmissionID>' % self.submission_id)
                self.response_footers()

        def response_headers(self, code = 200):
                print('Status: %d' % code)
                print('Content-type: text/html\n')
                print('<?xml version="1.0" encoding="%s" ?>' % UNICODE)
                print('<ISFDB>')

        def response_footers(self):
                print('</ISFDB>')
                sys.exit(0)
                
        def get_element_value(self, tag):
                document = self.merge[0].getElementsByTagName(tag)
                try:
                        value = document[0].firstChild.data.encode(UNICODE)
                except:
                        value = ''
                return value

        def delete_field(self, field_name):
                index = string.find(self.XMLdata, '<%s>' % field_name)
                if index == -1:
                        return
                newxml = self.XMLdata[:index]
                index = string.find(self.XMLdata, '</%s>' % field_name)
                if index == -1:
                        return
                index += len(field_name) + 3
                newxml += self.XMLdata[index:]
                self.XMLdata = newxml


if __name__ == '__main__':
        sub = Submission()
        sub.process_submission()
