#!_PYTHONLOC
#
#     (C) COPYRIGHT 2022-2026   Ahasuerus, Al von Ruff
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
from templateClass import Template
from SQLparsing import *


if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('The ability to edit templates is limited to ISFDB Bureaucrats')

        submission = Submission()
        submission.header = 'Edit Template Submission'
        submission.cgi_script = 'edit_template'
        submission.type = MOD_TEMPLATE_EDIT

        new = Template()
        new.cgi2obj()
        if new.error:
                submission.error(new.error)
        current = Template()
        current.load(new.id)
        if current.error:
                submission.error(new.error)

        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="%s" ?>\n' % UNICODE
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <TemplateUpdate>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name))
        update_string += "    <Subject>%s</Subject>\n" % CNX.DB_ESCAPE_STRING(new.name)
        update_string += "    <Record>%d</Record>\n" % int(new.id)
        (changes, update) = submission.CheckField(new.used_name, current.used_name,
                                                  new.name, current.name, 'TemplateName', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_displayed_name, current.used_displayed_name,
                                                  new.displayed_name, current.displayed_name, 'TemplateDisplayedName', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_type, current.used_type,
                                                  new.type, current.type, 'TemplateType', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_url, current.used_url,
                                                  new.url, current.url, 'TemplateURL', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_mouseover, current.used_mouseover,
                                                  new.mouseover, current.mouseover, 'TemplateMouseoverHelp', 0)
        if changes:
                update_string += update
        update_string += "  </TemplateUpdate>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
