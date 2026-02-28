#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2007-2026   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1247 $
#     Date: $Date: 2026-02-09 10:25:26 -0500 (Mon, 09 Feb 2026) $


from awardClass import *
from awardtypeClass import *
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from SQLparsing import *
from login import *
from library import *
from isfdblib_print import *


if __name__ == '__main__':

        title_id = SESSION.Parameter(0, 'int')
        # If the passed in ID is not 0, i.e. this is a title-based award, load the associated title data
        if title_id:
                title = SQLloadTitle(title_id)
                if not title:
                        SESSION.DisplayError('Title ID Does Not Exist')

        awardType = award_type()
        awardType.award_type_id = SESSION.Parameter(1, 'int')
        awardType.load()
        if not awardType.award_type_name:
                SESSION.DisplayError('Award Type ID Does Not Exist')

        if title_id:
                PrintPreSearch('Award Editor for a Title')
        else:
                PrintPreSearch('Award Editor')
        PrintNavBar('edit/addaward.cgi', title_id)

        help = HelpAward(awardType.award_type_poll)

        print('<div id="HelpBox">')
        print('<b>Help on adding an award: </b>')
        print('<a href="%s://%s/index.php/Help:Screen:AddAward">Help:Screen:AddAward</a><p>' % (PROTOCOL, WIKILOC))
        print('</div>')

        if title_id:
                print('<h3>You are entering an award for Title record %s</h3>' % ISFDBLinkNoName('title.cgi', title[TITLE_PUBID], title[TITLE_PUBID]))
        else:
                print('<h3>This data entry form is for awards that are given to people (for instance, Best Artist)')
                print('or works not eligible for inclusion in ISFDB (for instance, Best Dramatic Presentation).')
                print('If you want to add an award to a title in ISFDB, go to that title\'s page and use the')
                print('Add Award link found there.</h3>')
                print('<p>')

        print('<form id="data" method="POST" action="/cgi-bin/edit/submitnewaward.cgi">')
        print('<table border="0">')
        print('<tbody id="titleBody">')

        if title_id:
                printfield("Title", "award_title", help, title[TITLE_TITLE], 1)
                authors = SQLTitleAuthors(title_id)
                printmultiple(authors, "Author", "title_author", help, 1)

        else:
                printfield("Title", "award_title", help)
                printmultiple([], "Author", "title_author", help)

        printfield("Year", "award_year", help)

        # Award name is read-only because the list of categories depends on it. If we were to make it editable,
        # we would need to implement JavaScript-based logic to change categories based on the selected award type.
        printfield("Award Name", "award_type", help, awardType.award_type_name, 1)

        printAwardCategory("award_cat_id", "Category", awardType.award_type_id, '', help)

        printAwardLevel("Award Level", '0', awardType.award_type_poll, help)

        # Only allow entering IMDB information for non-title awards
        if not title_id:
                printfield("IMDB Title", "award_movie", help)

        printtextarea('Note', 'award_note', help)

        printtextarea('Note to Moderator', 'mod_note', help)

        print('</tbody>')
        print('</table>')
        print('<p>')

        print('<input name="title_id" value="%d" type="HIDDEN">' % (title_id))
        print('<input name="award_type_id" value="%d" type="HIDDEN">' % (awardType.award_type_id))
        print('<input type="SUBMIT" value="Submit Award" tabindex="1">')
        print('</form>')

        PrintPostSearch(tableclose=False)
