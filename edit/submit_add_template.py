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
                SESSION.DisplayError('The ability to add ISFDB templates is limited to ISFDB Bureaucrats')

        submission = Submission()
        submission.header = 'Add ISFDB Template Submission'
        submission.cgi_script = 'add_template'
        submission.type = MOD_TEMPLATE_ADD

        template = Template()
        template.cgi2obj()
        if template.error:
                submission.error(template.error)

        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="%s" ?>\n' % UNICODE
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <NewTemplate>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name))
        update_string += "    <Subject>%s</Subject>\n" % CNX.DB_ESCAPE_STRING(template.name)
        update_string += "    <TemplateName>%s</TemplateName>\n" % CNX.DB_ESCAPE_STRING(template.name)
        if template.displayed_name:
                update_string += "    <TemplateDisplayedName>%s</TemplateDisplayedName>\n" % CNX.DB_ESCAPE_STRING(template.displayed_name)
        update_string += "    <TemplateType>%s</TemplateType>\n" % CNX.DB_ESCAPE_STRING(template.type)
        if template.url:
                update_string += "    <TemplateURL>%s</TemplateURL>\n" % CNX.DB_ESCAPE_STRING(template.url)
        if template.mouseover:
                update_string += "    <TemplateMouseoverHelp>%s</TemplateMouseoverHelp>\n" % CNX.DB_ESCAPE_STRING(template.mouseover)
        update_string += "  </NewTemplate>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
