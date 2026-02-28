#
#     (C) COPYRIGHT 2022-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 203 $
#     Date: $Date: 2018-09-12 17:38:34 -0400 (Wed, 12 Sep 2018) $

from isfdb import *
from library import XMLescape, XMLunescape, IsfdbFieldStorage
from SQLparsing import SQLGetTemplate, SQLGetTemplateByName


class Template():
        def __init__(self):
                self.used_id = 0
                self.used_name = 0
                self.used_displayed_name = 0
                self.used_type = 0
                self.used_url = 0
                self.used_mouseover = 0

                self.id = ''
                self.name = ''
                self.displayed_name = ''
                self.type = ''
                self.url = ''
                self.mouseover = ''

                self.error = ''

        def load(self, record_id):
                if not record_id:
                        return
                self.id = record_id
                self.used_id = 1
                record = SQLGetTemplate(self.id)
                if not record:
                        return
                if record[TEMPLATE_NAME]:
                        self.name = record[TEMPLATE_NAME]
                        self.used_name = 1
                if record[TEMPLATE_DISPLAYED_NAME]:
                        self.displayed_name = record[TEMPLATE_DISPLAYED_NAME]
                        self.used_displayed_name = 1
                if record[TEMPLATE_TYPE]:
                        self.type = record[TEMPLATE_TYPE]
                        self.used_type = 1
                if record[TEMPLATE_URL]:
                        self.url = record[TEMPLATE_URL]
                        self.used_url = 1
                if record[TEMPLATE_MOUSEOVER]:
                        self.mouseover = record[TEMPLATE_MOUSEOVER]
                        self.used_mouseover = 1

        def cgi2obj(self):
                self.form = IsfdbFieldStorage()
                if 'template_id' in self.form:
                        self.id = int(self.form['template_id'].value)
                        self.used_id = 1
                        if not SQLGetTemplate(self.id):
                                self.error = 'This Template ID is not on file'
                                return

                if 'template_name' in self.form:
                        self.name = XMLescape(self.form['template_name'].value)
                        self.used_name = 1
                else:
                        self.error = "Template name is a required field"
                        return

                # Unescape the name to ensure that the lookup finds it in the database
                current_template = SQLGetTemplateByName(XMLunescape(self.name))
                if current_template:
                        if (self.id != int(current_template[TEMPLATE_ID])) and (current_template[TEMPLATE_NAME] == XMLunescape(self.name)):
                                self.error = "Entered template name is already associated with another ISFDB template"
                                return

                if 'template_displayed_name' in self.form:
                        self.displayed_name = XMLescape(self.form['template_displayed_name'].value)
                        self.used_displayed_name = 1

                if 'template_type' in self.form:
                        self.type = XMLescape(self.form['template_type'].value)
                        self.used_type = 1
                        if self.type not in ('Internal URL', 'External URL', 'Substitute String'):
                                self.error = 'Template Type must be Internal URL, External URL or Substitute String'
                                return
                else:
                        self.error = 'Template Type is a required field'
                        return

                if 'template_url' in self.form:
                        self.url = XMLescape(self.form['template_url'].value)
                        self.used_url = 1
                elif self.type in ('Internal URL', 'External URL'):
                        self.error = 'Internal/External Templates must have a URL defined'
                        return

                if 'template_mouseover' in self.form:
                        self.mouseover = XMLescape(self.form['template_mouseover'].value)
                        self.used_mouseover = 1

##                if self.type == 'Substitute String' and self.url:
##                        self.error = 'Templates with Substitute Strings can not have URLs'

