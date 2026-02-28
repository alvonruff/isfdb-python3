#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023-2026   Ahasuerus, Al von Ruff
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
                SESSION.DisplayError('The ability to edit recognized domains is limited to ISFDB Bureaucrats')

        submission = Submission()
        submission.header = 'Edit Recognized Domain Submission'
        submission.cgi_script = 'edit_delete_recognized_domain'
        submission.type = MOD_REC_DOMAIN_EDIT

        new = RecognizedDomain()
        new.cgi2obj()
        if new.error:
                submission.error(new.error)
        current = RecognizedDomain()
        current.load(new.domain_id)
        if current.error:
                submission.error(new.error)

        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="%s" ?>\n' % UNICODE
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <EditRecognizedDomain>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name))
        update_string += "    <Subject>%s</Subject>\n" % CNX.DB_ESCAPE_STRING(new.domain_name)
        update_string += "    <Record>%d</Record>\n" % int(new.domain_id)
        (changes, update) = submission.CheckField(new.used_domain_name, current.used_domain_name, new.domain_name, current.domain_name, 'DomainName', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_site_name, current.used_site_name, new.site_name, current.site_name, 'SiteName', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_site_url, current.used_site_url, new.site_url, current.site_url, 'SiteURL', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_linking_allowed_display, current.used_linking_allowed_display,
                                                  new.linking_allowed_display, current.linking_allowed_display, 'LinkingAllowed', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_required_segment, current.used_required_segment,
                                                  new.required_segment, current.required_segment, 'RequiredSegment', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_explicit_link_required_display, current.used_explicit_link_required_display,
                                                  new.explicit_link_required_display, current.explicit_link_required_display,
                                                  'ExplicitLinkRequired', 0)
        if changes:
                update_string += update
        update_string += "  </EditRecognizedDomain>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
