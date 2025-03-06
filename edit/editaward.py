#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 735 $
#     Date: $Date: 2021-09-06 16:25:55 -0400 (Mon, 06 Sep 2021) $


from awardClass import *
from awardtypeClass import *
from isfdb import *
from library import *
from isfdblib import *
from isfdblib_help import *
from SQLparsing import *
from isfdblib_print import *


if __name__ == '__main__':

        award_id = SESSION.Parameter(0, 'int')
        award = awards(db)
        award.load(award_id)
        if not award.award_id:
                SESSION.DisplayError('Record Does Not Exist')
        awardType = award_type()
        awardType.award_type_id = award.award_type_id
        awardType.load()

        if award.title_id:
                PrintPreSearch("Award Editor for a Title")
        else:
                PrintPreSearch("Award Editor")
        PrintNavBar("edit/editaward.cgi", award_id)

        help = HelpAward(awardType.award_type_poll)

        printHelpBox('award', 'EditAward')

        # Print appropriate message depending on whether this is a title-based award
        if award.title_id:
                print('<h3>You are editing an award for Title record %s</h3>' % ISFDBLinkNoName('title.cgi', award.title_id, award.title_id))
        else:
                print('<h3>You are editing an award not associated with an ISFDB title</h3>')
        print('<p>')

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitaward.cgi">')

        print('<table border="0">')
        print('<tbody id="titleBody">')

        printfield("Title", "award_title", help, award.award_title, award.title_id)

        if award.title_id:
                no_edit = 1
        else:
                no_edit = 0
        printmultiple(award.award_authors, "Author", "title_author", help, no_edit)

        printfield("Year", "award_year", help, award.award_year)

        # Award name is read-only because the list of categories depends on it. If we were to make it editable,
        # we would need to implement JavaScript-based logic to change categories based on the selected award type.
        printfield("Award Name", "award_type", help, award.award_type_name, 1)

        printAwardCategory("award_cat_id", "Category", award.award_type_id, award.award_cat_id, help)

        printAwardLevel("Award Level", award.award_level, awardType.award_type_poll, help)

        # Only display the IMDB title field for non-title based awards
        if not award.title_id:
                printfield("IMDB Title", "award_movie", help, award.award_movie)

        printtextarea('Note', 'award_note', help, award.award_note)

        printtextarea('Note to Moderator', 'mod_note', help)

        print('</tbody>')
        print('</table>')

        print('<p>')
        print('<hr>')
        print('<p>')
        print('<input NAME="award_id" VALUE="%d" TYPE="HIDDEN">' % (award_id))
        print('<input name="award_type_id" value="%d" type="HIDDEN">' % (awardType.award_type_id))
        print('<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">')
        print('</form>')
        print('<p>')
        print('<hr>')
        print('<a href="/cgi-bin/edit/deleteaward.cgi?%d">Delete this award</a>' % (award_id))

        PrintPostSearch(tableclose=False)
