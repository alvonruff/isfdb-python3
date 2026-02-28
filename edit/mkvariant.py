#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2026   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1247 $
#     Date: $Date: 2026-02-09 10:25:26 -0500 (Mon, 09 Feb 2026) $


from isfdb import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *
from library import *
from titleClass import titles


if __name__ == '__main__':

        title_id = SESSION.Parameter(0, 'int')
        title = titles(db)
        title.load(title_id)
        if not title.title_title:
                SESSION.DisplayError('Record Does Not Exist')

        PrintPreSearch('Make Variant Title')
        PrintNavBar('edit/mkvariant.cgi', title_id)

        help = HelpMakeVariant()

        print('<div id="HelpBox">')
        print('<b>Help on making variant titles: </b>')
        print('<a href="%s://%s/index.php/Help:Screen:MakeVariant">Help:Screen:MakeVariant</a><p>' % (PROTOCOL, WIKILOC))
        print('</div>')

        print('Current Title:<br>')

        print('<b>Title:</b>', ISFDBLink('title.cgi', title.title_id, title.title_title))
        print('<br>')

        print('<b>Author:</b>', FormatAuthors(title.title_author_tuples))
        print('<br>')

        print('<b>Date:</b>', title.title_year)
        print('<br>')
        print('<b>Type:</b>', title.title_ttype)
        print('<p>')

        ##################################################################
        # Data Entry Form 1
        ##################################################################
        print('<hr class="divider">')
        print('<p>')
        print('<h2>Option 1</h2>')
        print('<p>')

        print('If the parent title already exists, enter its record number below.')
        print('To BREAK an existing Variant link, enter 0.')
        print('<p>')

        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitmkvar1.cgi">')
        print('<table border="0">')
        print('<tbody>')
        if title.title_parent:
                printfield("Parent #", "Parent", help, title.title_parent)
        else:
                printfield("Parent #", "Parent", help)

        printtextarea('Note to Moderator', 'mod_note', help)

        print('</tbody>')
        print('</table>')
        print('<p>')

        print('<input NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % (title_id))
        print('<input TYPE="SUBMIT" VALUE="Link to Existing Parent" tabindex="1">')
        print('</form>')

        print('<p>')

        ##################################################################
        # Data Entry Form 2
        ##################################################################
        print('<hr class="divider">')
        print('<p>')
        print('<h2>Option 2</h2>')
        print('If the parent title does not exist, enter the title information below to create it.')
        print('<p>')

        print('<form id="data2" METHOD="POST" ACTION="/cgi-bin/edit/submitmkvar2.cgi">')
        print('<table border="0">')
        print('<tbody id="titleBody">')

        printfield('Title', 'title_title', help, title.title_title)

        printmultiple(title.title_trans_titles, 'Transliterated Title', 'trans_titles', help)

        printmultiple(title.title_authors, 'Author', 'title_author', help)

        printfield('Date', 'title_copyright', help, title.title_year)

        if (title.title_ttype == 'CHAPBOOK') or title.title_series:
                readonly = 1
        else:
                readonly = 0
        printfield('Series', 'title_series', help, title.title_series, readonly)
        printfield('Series Num', 'title_seriesnum',  help, title.title_seriesnum, readonly)

        printWebPages(title.title_webpages, 'title', help)

        printlanguage(title.title_language_id, 'language', 'Language', help)

        print('<tr>')
        printfieldlabel('Title Type', help)
        print('<td><select name="title_ttype" tabindex="1">')
        for ttype in SESSION.db.all_title_types:
                if ttype == title.title_ttype:
                        print('<option selected="selected">%s</option>' % ttype)
                else:
                        print('<option>%s</option>' % ttype)
        print('</select></td>')
        print('</tr>')

        printtextarea('Title Note', 'title_note', help)
        
        printtextarea('Note to Moderator', 'mod_note', help)

        print('</tbody>')
        print('</table>')
        print('<p>')

        print('<input NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % title.title_id)
        print('<input TYPE="SUBMIT" VALUE="Create New Parent Title" tabindex="1">')
        print('</form>')


        PrintPostSearch(tableclose=False)
