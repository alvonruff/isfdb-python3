#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2013-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


from awardtypeClass import *
from SQLparsing import SQLloadAwardTypeWebpages, SQLgetNotes
from common import *


if __name__ == '__main__':

        award_type_id = SESSION.Parameter(0, 'int')
        award_type = award_type()
        award_type.award_type_id = award_type_id
        award_type.load()
        if not award_type.award_type_name:
                if SQLDeletedAwardType(award_type_id):
                        SESSION.DisplayError('This award type has been deleted. See %s for details.' % ISFDBLink('awardtype_history.cgi', award_type_id, 'Edit History'))
                else:
                        SESSION.DisplayError('Award Type Does Not Exist')

        title = 'Overview of %s' % award_type.award_type_name
        PrintHeader(title)
        PrintNavbar('award_type', award_type.award_type_id, 0, 'awardtype.cgi', award_type.award_type_id)

        print('<ul>')

        if award_type.award_type_short_name:
                print('<li><b>Short Name:</b>', ISFDBText(award_type.award_type_short_name))

        #Retrieve this user's data
        user = User()
        user.load()
        printRecordID('Award Type', award_type.award_type_id, user.id, user)

        if award_type.award_type_name:
                print('<li><b>Full Name:</b>', ISFDBText(award_type.award_type_name))

        if award_type.award_type_for:
                print('<li><b>Awarded For:</b>', ISFDBText(award_type.award_type_for))

        if award_type.award_type_by:
                print('<li><b>Awarded By:</b>', ISFDBText(award_type.award_type_by))

        if award_type.award_type_poll:
                print('<li><b>Poll:</b>', ISFDBText(award_type.award_type_poll))

        if award_type.award_type_non_genre:
                print('<li><b>Covers more than just SF:</b>', ISFDBText(award_type.award_type_non_genre))

        # Webpages
        webpages = SQLloadAwardTypeWebpages(award_type.award_type_id)
        PrintWebPages(webpages)

        # Note
        if award_type.award_type_note:
                print('<li>')
                print(FormatNote(award_type.award_type_note, 'Note', 'short', award_type.award_type_id, 'AwardType'))

        print('</ul>')

        print('<p>')

        # Display a grid of all years when the award was given
        award_type.display_table_grid()
        # Display a list of all categories for this award
        award_type.display_categories()

        PrintTrailer('award_type', award_type.award_type_id, award_type.award_type_id)
