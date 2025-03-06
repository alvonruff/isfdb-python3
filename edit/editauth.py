#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 667 $
#     Date: $Date: 2021-06-28 18:30:46 -0400 (Mon, 28 Jun 2021) $


from isfdblib import *
from isfdb import *
from SQLparsing import *
from isfdblib_help import *
from isfdblib_print import *


if __name__ == '__main__':

        author_id = SESSION.Parameter(0, 'int')
        record = SQLloadAuthorData(author_id)
        if not record:
                SESSION.DisplayError('Record Does Not Exist')
        
        PrintPreSearch('Author Editor')
        PrintNavBar('edit/editauth.cgi', author_id)
        help = HelpAuthor()

        printHelpBox('author', 'AuthorData')

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitauth.cgi">')
        
        print('<table border="0">')
        print('<tbody id="tagBody">')

        # Limit the ability to edit canonical author names to moderators
        user = User()
        user.load()
        display_only = 1
        if SQLisUserModerator(user.id):
                display_only = 0
        printfield("Canonical Name", "author_canonical",  help, record[AUTHOR_CANONICAL], display_only)

        trans_names = SQLloadTransAuthorNames(record[AUTHOR_ID])
        printmultiple(trans_names, "Transliterated Name", "trans_names", help)

        printfield("Legal Name",     "author_legalname",  help, record[AUTHOR_LEGALNAME])
        trans_legal_names = SQLloadTransLegalNames(record[AUTHOR_ID])
        printmultiple(trans_legal_names, "Trans. Legal Name", "trans_legal_names", help)

        printfield("Directory Entry","author_lastname",   help, record[AUTHOR_LASTNAME])
        printfield("Birth Place",    "author_birthplace", help, record[AUTHOR_BIRTHPLACE])
        printfield("Birth Date",     "author_birthdate",  help, record[AUTHOR_BIRTHDATE])
        printfield("Death Date",     "author_deathdate",  help, record[AUTHOR_DEATHDATE])

        printlanguage(record[AUTHOR_LANGUAGE], "author_language", "Working Language", help)

        emails = SQLloadEmails(record[AUTHOR_ID])
        printmultiple(emails, "Email Address", "author_emails", help)

        webpages = SQLloadWebpages(record[AUTHOR_ID])
        printWebPages(webpages, 'author', help)

        printfield("Author Image",          "author_image",     help, record[AUTHOR_IMAGE])
        
        printtextarea('Note', 'author_note', help, record[AUTHOR_NOTE])

        printtextarea('Note to Moderator', 'mod_note', help)

        print('</table>')

        print('<p>')
        print('<input NAME="author_id" VALUE="%d" TYPE="HIDDEN">' % author_id)
        print('<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">')
        print('</form>')
        print('<p>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)

