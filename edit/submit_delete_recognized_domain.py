#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 972 $
#     Date: $Date: 2022-08-23 16:44:48 -0400 (Tue, 23 Aug 2022) $

	
from isfdb import *
from isfdblib import *
from login import *
from library import *
from recognizeddomainClass import RecognizedDomain
from SQLparsing import *
from navbar import *
	
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Recognized Domain Delete Submission'
        submission.cgi_script = 'edit_delete_recognized_domain'
        submission.type = MOD_REC_DOMAIN_DELETE

        domain_id = SESSION.Parameter(0, 'int')

	if not submission.user.id:
                submission.error('', domain_id)

        domain = RecognizedDomain()
        domain.load(domain_id)
        if domain.error:
                SESSION.DisplayError(domain.error)

	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <DeleteRecognizedDomain>\n"
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(domain.domain_name)))
	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
	update_string += "    <Record>%d</Record>\n" % domain_id
	update_string += "  </DeleteRecognizedDomain>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
