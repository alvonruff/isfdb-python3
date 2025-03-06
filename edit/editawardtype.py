#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2013-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 649 $
#     Date: $Date: 2021-06-18 22:05:24 -0400 (Fri, 18 Jun 2021) $


from awardtypeClass import *
from isfdblib import *
from isfdblib_help import *
from isfdb import *
from SQLparsing import *
from isfdblib_print import *


if __name__ == '__main__':

        award_type_id = SESSION.Parameter(0, 'int')

        award_type = award_type()
        award_type.award_type_id = award_type_id
        award_type.load()
        if not award_type.award_type_short_name:
                SESSION.DisplayError('Award Type Does Not Exist')

        PrintPreSearch('Award Type Editor')
        PrintNavBar('edit/editawardtype.cgi', award_type_id)

        help = HelpAwardType()

        printHelpBox('Award Type', 'AwardType')

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitawardtype.cgi">')

        print('<table border="0">')
        print('<tbody id="tagBody">')

        printfield('Short Name',      'award_type_short_name', help, award_type.award_type_short_name)

        printfield('Full Name',       'award_type_name',       help, award_type.award_type_name)

        printfield('Awarded For',     'award_type_for',        help, award_type.award_type_for)

        printfield('Awarded By',      'award_type_by',         help, award_type.award_type_by)

        values = {}
        if award_type.award_type_poll == 'Yes':
                values['Yes'] = 1
                values['No'] = 0
        else:
                values['Yes'] = 0
                values['No'] = 1
        printdropdown('Poll', 'award_type_poll', values, help)

        values = {}
        if award_type.award_type_non_genre == 'Yes':
                values['Yes'] = 1
                values['No'] = 0
        else:
                values['Yes'] = 0
                values['No'] = 1
        printdropdown('Non-Genre', 'award_type_non_genre', values, help)

        printWebPages(award_type.award_type_webpages, 'award_type', help)

        printtextarea('Note', 'award_type_note', help, award_type.award_type_note)

        print('</table>')

        print('<p>')
        print('<input NAME="award_type_id" VALUE="' + str(award_type.award_type_id) + '" TYPE="HIDDEN">')
        print('<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">')
        print('</form>')
        print('<p>')

        PrintPostSearch(0, 0, 0, 0, 0)

