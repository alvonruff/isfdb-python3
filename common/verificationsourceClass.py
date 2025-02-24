#
#     (C) COPYRIGHT 2023-2025  Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 203 $
#     Date: $Date: 2018-09-12 17:38:34 -0400 (Wed, 12 Sep 2018) $

import cgi
from isfdb import *
from library import XMLescape, XMLunescape, IsfdbFieldStorage
from SQLparsing import SQLGetVerificationSource, SQLGetVerificationSourceByLabel


class VerificationSource():
        def __init__(self):
                self.used_id = 0
                self.used_label = 0
                self.used_name = 0
                self.used_url = 0

                self.id = ''
                self.label = ''
                self.name = ''
                self.url = ''

                self.error = ''

        def load(self, record_id):
                if not record_id:
                        return
                self.id = record_id
                self.used_id = 1
                record = SQLGetVerificationSource(self.id)
                if not record:
                        return
                if record[REFERENCE_LABEL]:
                        self.label = record[REFERENCE_LABEL]
                        self.used_label = 1
                if record[REFERENCE_NAME]:
                        self.name = record[REFERENCE_NAME]
                        self.used_name = 1
                if record[REFERENCE_URL]:
                        self.url = record[REFERENCE_URL]
                        self.used_url = 1

        def cgi2obj(self):
                self.form = IsfdbFieldStorage()
                if 'source_id' in self.form:
                        self.id = int(self.form['source_id'].value)
                        self.used_id = 1
                        if not SQLGetVerificationSource(self.id):
                                self.error = 'This Verification Source ID is not on file'
                                return

                try:
                        self.label = XMLescape(self.form['source_label'].value)
                        self.used_label = 1
                        if not self.label:
                                raise
                        # Unescape the label to ensure that the lookup finds it in the database
                        current_source = SQLGetVerificationSourceByLabel(XMLunescape(self.label))
                        if current_source:
                                if (self.id != int(current_source[REFERENCE_ID])) and (current_source[REFERENCE_LABEL] == XMLunescape(self.label)):
                                        self.error = "Entered label is aready associated with another Verification Source"
                                        return
                except:
                        self.error = "Verification Source Label is a required field"
                        return

                if 'source_name' in self.form:
                        self.name = XMLescape(self.form['source_name'].value)
                        self.used_name = 1
                else:
                        self.error = 'Verification Source Name is a required field'
                        return

                if 'source_url' in self.form:
                        self.url = XMLescape(self.form['source_url'].value)
                        self.used_url = 1
                else:
                        self.error = 'Verification Source URL is a required field'
                        return
