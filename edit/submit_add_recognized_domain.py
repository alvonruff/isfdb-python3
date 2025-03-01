#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023-2025   Ahasuerus, Al von Ruff
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
from recognizeddomainClass import RecognizedDomain
from SQLparsing import *


if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('The ability to add recognized domains is limited to ISFDB Bureaucrats')

        submission = Submission()
        submission.header = 'Add Recognized Domain Submission'
        submission.cgi_script = 'add_recognized_domain'
        submission.type = MOD_REC_DOMAIN_ADD

        domain = RecognizedDomain()
        domain.cgi2obj()
        if domain.error:
                submission.error(domain.error)

        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="%s" ?>\n' % UNICODE
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <AddRecognizedDomain>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name))
        update_string += "    <Subject>%s</Subject>\n" % CNX.DB_ESCAPE_STRING(domain.domain_name)
        update_string += "    <DomainName>%s</DomainName>\n" % CNX.DB_ESCAPE_STRING(domain.domain_name)
        update_string += "    <SiteName>%s</SiteName>\n" % CNX.DB_ESCAPE_STRING(domain.site_name)
        update_string += "    <SiteURL>%s</SiteURL>\n" % CNX.DB_ESCAPE_STRING(domain.site_url)
        update_string += "    <LinkingAllowed>%s</LinkingAllowed>\n" % CNX.DB_ESCAPE_STRING(domain.linking_allowed_display)
        update_string += "    <RequiredSegment>%s</RequiredSegment>\n" % CNX.DB_ESCAPE_STRING(domain.required_segment)
        update_string += "    <ExplicitLinkRequired>%s</ExplicitLinkRequired>\n" % CNX.DB_ESCAPE_STRING(domain.explicit_link_required_display)
        update_string += "  </AddRecognizedDomain>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
