#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

        
from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *

class Language():
        def __init__(self):
                self.name = ''
                self.code = ''
                self.latin = ''

        def cgi2obj(self):
                self.form = IsfdbFieldStorage()
                if 'language_name' in self.form:
                        self.name = XMLescape(self.form['language_name'].value)
                else:
                        SESSION.DisplayError('Language Name is a required field')
                if SQLGetLangIdByName(self.name):
                        SESSION.DisplayError('This ISO 639-2 language name is already on file')

                if 'language_code' in self.form:
                        self.code = XMLescape(self.form['language_code'].value)
                else:
                        SESSION.DisplayError('Language Code is a required field')
                if len(self.code) != 3:
                        SESSION.DisplayError('Language Code must be a 3-character value')
                if SQLGetLangIdByCode(self.code):
                        SESSION.DisplayError('This ISO 639-2 language code is already on file')

                if 'language_latin' in self.form:
                        self.latin = XMLescape(self.form['language_latin'].value)
                else:
                        SESSION.DisplayError('Latin-Derived is a required field')
                if self.latin not in ('No', 'Yes'):
                        SESSION.DisplayError('Latin value must be either Yes or No')

if __name__ == '__main__':
        
        submission = Submission()
        if not submission.user.id:
                submission.error()
        submission.header = 'New Language Submission'
        submission.cgi_script = 'new_language'
        submission.type = MOD_LANGUAGE_NEW

        language = Language()
        language.cgi2obj()

        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <NewLanguage>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(language.name))
        update_string += "    <LanguageName>%s</LanguageName>\n" % (db.escape_string(language.name))
        update_string += "    <LanguageCode>%s</LanguageCode>\n" % (db.escape_string(language.code))
        update_string += "    <Latin>%s</Latin>\n" % (db.escape_string(language.latin))
        update_string += "  </NewLanguage>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
