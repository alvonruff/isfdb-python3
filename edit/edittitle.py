#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Bill Longley, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1161 $
#     Date: $Date: 2023-12-05 19:08:38 -0500 (Tue, 05 Dec 2023) $


from isfdb import *
from isfdblib import *
from isfdblib_help import *
from library import *
from SQLparsing import *
from isfdblib_print import *


def printReadOnlyTitleType(title_type):
        print '<tr>'
        print '<td><b>Title Type</b></td>'
        print '<td><input name="title_ttype" value="%s" READONLY class="titletype displayonly"></td>' % title_type
        print '</tr>'


def printCommonSection(record, help):
        printfield("Date", "title_copyright",        help, record[TITLE_YEAR])

        series_name = ''
        if record[TITLE_SERIES]:
                series = SQLget1Series(record[TITLE_SERIES])
                series_name = series[SERIES_NAME]
        # Variant titles and CHAPBOOKS can't be in series. Consequently, the two
        # series-related fields are displayed as read-only for VTs and CHAPBOOKs
        # ***if*** these fields have no value. If there is a value on file, then
        # the field is editable to make it easy for editors to remove the value.
        if (record[TITLE_PARENT] or record[TITLE_TTYPE] == 'CHAPBOOK') and not series_name:
                readonly = 1
        else:
                readonly = 0
        printfield("Series", "title_series", help, series_name, readonly)
        if (record[TITLE_PARENT] or record[TITLE_TTYPE] == 'CHAPBOOK') and (series_number is None):
                readonly = 1
        else:
                readonly = 0
        printfield("Series Num", "title_seriesnum",  help, series_number, readonly)

        webpages = SQLloadTitleWebpages(record[TITLE_PUBID])
        printWebPages(webpages, 'title', help)

        printlanguage(record[TITLE_LANGUAGE], 'language', 'Language', help)


def printtitlerecord(record, series_number, help):
        authors = SQLTitleAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Author", "title_author", help)

        printCommonSection(record, help)

        printtitletype(record[TITLE_TTYPE], help)
        
        printlength(record[TITLE_STORYLEN], help)

        printfield('Content', 'title_content', help, record[TITLE_CONTENT])

        printTitleFlags(record, help)

        # Variant titles and CHAPBOOKS can't have synopses. Consequently the Synopsis
        # field is displayed as read-only ***if*** there is no pre-existing value.
        # If there is a value on file, then the field is editable to make it easy
        # for editors to remove the value.
        if (record[TITLE_PARENT] or record[TITLE_TTYPE] == 'CHAPBOOK') and not record[TITLE_SYNOP]:
                readonly = 1
        else:
                readonly = 0
        printtextarea('Synopsis', 'title_synopsis', help, SQLgetNotes(record[TITLE_SYNOP]), 10, readonly)


def printreviewrecord(record, series_number, help):
        authors = SQLReviewAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Author", "review_author1.", help)

        authors = SQLTitleAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Reviewer", "review_reviewer1.", help)

        printCommonSection(record, help)

        printReadOnlyTitleType('REVIEW')


def printinterviewrecord(record, series_number, help):
        authors = SQLInterviewAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Interviewee", "interviewee_author1.", help)

        authors = SQLTitleAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Interviewer", "interviewer_author1.", help)

        printCommonSection(record, help)

        printReadOnlyTitleType('INTERVIEW')


if __name__ == '__main__':

        title_id = SESSION.Parameter(0, 'int')
        title_data = SQLloadTitle(title_id)
        if not title_data:
                SESSION.DisplayError('Record Does Not Exist')

        help = HelpTitle(title_data[TITLE_TTYPE])

        PrintPreSearch('Title Editor')
        PrintNavBar('edit/edittitle.cgi', title_id)

        printHelpBox('title', 'EditTitle')

        # Pass the title type to the form validation function so that it would know which fields exist in the form
        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submittitle.cgi">'

        # Combine the two series number fields into one for display purposes
        series_number = title_data[TITLE_SERIESNUM]
        if title_data[TITLE_SERIESNUM_2] is not None:
                series_number = '%s.%s' % (title_data[TITLE_SERIESNUM], title_data[TITLE_SERIESNUM_2])

        if title_data[TITLE_TTYPE] == 'REVIEW':
                review = 1
        else:
                review = 0
        if title_data[TITLE_TTYPE] == 'INTERVIEW':
                interview = 1
        else:
                interview = 0

        print '<table border="0">'
        print '<tbody>'
        
        if review:
                title_field = 'Review of'
        elif interview:
                title_field = 'Interview Title'
        else:
                title_field = 'Title'
        printfield(title_field, 'title_title', help, title_data[TITLE_TITLE])

        trans_titles = SQLloadTransTitles(title_id)
        printmultiple(trans_titles, "Transliterated Title", "trans_titles", help)

        if interview:
                printinterviewrecord(title_data, series_number, help)
        elif review:
                printreviewrecord(title_data, series_number, help)
        else:
                printtitlerecord(title_data, series_number, help)

        printtextarea('Note', 'title_note', help, SQLgetNotes(title_data[TITLE_NOTE]), 10)

        printtextarea('Note to Moderator', 'mod_note', help, '')

        print '</tbody>'
        print '</table>'

        print '<p>'
        print '<hr>'
        print '<p>'
        print '<input NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % (title_id)
        print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
        print '</form>'
        print '<p>'
        print '<hr>'
        print ISFDBLink("edit/deletetitle.cgi", title_id, "Delete record")

        PrintPostSearch(tableclose=False)
