#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2009-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 725 $
#     Date: $Date: 2021-08-30 17:07:32 -0400 (Mon, 30 Aug 2021) $


from isfdb import *
from common import *
from login import *
from SQLparsing import *

user = User()
user.load()

if not user.id:
        SESSION.DisplayError('You must be logged in to modify your translation preferences')

PrintHeader('My Translation Preferences')
PrintNavbar('mylanguages', 0, 0, 'mylanguages.cgi', 0)

langs = SQLLoadFullLanguages()
print('<p>')
print('<form id="data" METHOD="POST" ACTION="/cgi-bin/submitmylanguages.cgi">')
print('<ul>')
for lang in langs:
        if lang[0] in user.languages:
                checked = 'checked'
        else:
                checked = ''
        print('<li><input type="checkbox" name="lang_choice.%s" value="on" %s>%s' % (lang[0], checked, lang[1]))
        print('<input name="lang_id.%d" value="%s" type="HIDDEN"></li>' % (lang[0], lang[1]))

print('</ul>')
print('<p>')
print('<input type="SUBMIT" value="Update Translation Preferences">')
print('</form>')

PrintTrailer('mylanguages', 0, 0)
