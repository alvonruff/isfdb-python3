#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2022   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 18 $
#     Date: $Date: 2017-10-31 19:18:05 -0400 (Tue, 31 Oct 2017) $

	
from isfdb import *
from isfdblib import Submission
from library import XMLescape
from login import User
from verificationsourceClass import VerificationSource
from SQLparsing import *


if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('The ability to add verification sources is limited to ISFDB Bureaucrats')

        submission = Submission()
        submission.header = 'Add Verification Source Submission'
        submission.cgi_script = 'add_verification_source'
        submission.type = MOD_VER_SOURCE_ADD

	source = VerificationSource()
	source.cgi2obj()
	if source.error:
                submission.error(source.error)

	update_string =  '<?xml version="1.0" encoding="%s" ?>\n' % UNICODE
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <VerificationSource>\n"
	update_string += "    <Submitter>%s</Submitter>\n" % db.escape_string(XMLescape(submission.user.name))
	update_string += "    <Subject>%s</Subject>\n" % db.escape_string(source.name)
        update_string += "    <SourceLabel>%s</SourceLabel>\n" % db.escape_string(source.label)
        update_string += "    <SourceName>%s</SourceName>\n" % db.escape_string(source.name)
        update_string += "    <SourceURL>%s</SourceURL>\n" % db.escape_string(source.url)
	update_string += "  </VerificationSource>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
