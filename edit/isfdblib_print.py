#!_PYTHONLOC
#
#     (C) COPYRIGHT 2010-2025   Ahasuerus, Dirk Stoecker, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 923 $
#     Date: $Date: 2022-05-28 15:13:55 -0400 (Sat, 28 May 2022) $


import cgi
import sys
import MySQLdb
from SQLparsing import *
from isfdb import *
from library import *
from isfdblib import *

def _question_mark():
        return '<img src="%s://%s/question_mark_icon.gif" alt="Question mark" class="help">' % (PROTOCOL, HTMLLOC)

def printtitletype(current_value, help):
        print('<tr>')
        printContentHeader('Title Type', help)
        print('<td><select tabindex="1" name="title_ttype">')
        for ttype in ['ANTHOLOGY', 'CHAPBOOK', 'COLLECTION', 'COVERART',
                      'EDITOR', 'ESSAY', 'INTERIORART', 'NONFICTION',
                      'NOVEL', 'OMNIBUS', 'POEM', 'SERIAL', 'SHORTFICTION']:
                if current_value == ttype:
                        print('<option value="%s" selected="selected">%s</option>' % (ttype, ttype))
                else:
                        print('<option value="%s">%s</option>' % (ttype, ttype))
                
        print('</select></td></tr>')

def printlength(current_value, help):
        print('<tr>')
        printContentHeader('Length', help)
        print('<td><select tabindex="1" name="title_storylen">')
        for storylen in SESSION.db.storylen_codes:
                if current_value == storylen:
                        print('<option selected>%s</option>' % storylen)
                else:
                        print('<option>%s</option>' % storylen)
        print('</select></td>')
        print('</tr>')

def printlanguage(current_language_code='', field='language', label='Language', help = None):
        (myID, username, usertoken) = GetUserData()
        # Get the currently defined preferences for the logged-in user
        preferences = SQLLoadUserPreferences(myID)
        # Get this user's default language code and name
        default_language_code = preferences[USER_DEFAULT_LANGUAGE]
        default_language_name = LANGUAGES[default_language_code]

        current_language_name = ''
        # If we are basing the language data on an existing record, get that record's language code and name
        if current_language_code:
                current_language_name = LANGUAGES[current_language_code]

        print('<tr>')
        printfieldlabel(label, help)

        print('<td><select tabindex="1" class="metainputselect" name="%s">' %(field))

        # Iterate over an alphabetized list of language names (excluding 'Unknown' in the 0th position)
        # and display them in a drop-down list
        for language_name in sorted(LANGUAGES[1:]):
                # If the current record's language is defined and we are processing it, then select it
                if current_language_name and language_name == current_language_name:
                        print('<option value="%s" selected="selected">%s</option>' % (language_name, language_name))
                # If the current title has no language code and this language is the user's default language, then select it
                elif not current_language_name and language_name == default_language_name:
                        print('<option value="%s" selected="selected">%s</option>' % (language_name, language_name))
                # Otherwise this language is displayed, but is not "selected"
                else:
                        print('<option value="%s">%s</option>' % (language_name, language_name))

        print('</select>')
        print('</td>')
        print('</tr>')

def printformat(field='pub_ptype', label='Format', help = None, value='unknown'):
        if not value:
                value = 'unknown'
        print('<tr>')
        printfieldlabel(label, help)

        print('<td><select tabindex="1" name="%s">' %(field))

        # Iterate over the list of recognized formats and display them in a drop-down list
        for format in SESSION.db.formats:
                if format.lower() == value.lower():
                        print('<option value="%s" selected="selected">%s</option>' % (format, format))
                else:
                        print('<option value="%s">%s</option>' % (format, format))

        print('</select>')
        print('</td>')
        print('</tr>')

def printExternalIDs(external_ids = None, label = 'External ID', field = 'external_id', help = None, readonly = 0):
        if not external_ids:
                external_ids = {}
        if not help:
                help = {}
        identifier_types = SQLLoadIdentifierTypes()

        print('<tr>')
        printfieldlabel('%ss' % label, help)
        print('<td>&nbsp;</td>')
        print('</tr>')

        counter = 0
        if readonly:
                for id_type in sorted(external_ids.keys()):
                        for id_value in external_ids[id_type]:
                                counter += 1
                                type_id = external_ids[id_type][id_value][0]
                                print('<tr>')
                                print('<td>')
                                print('<input type="hidden" name="%s_type.%d" VALUE="%d">' % (field, counter, type_id))
                                print('<b>%s</b>' % id_type)
                                print('</td>')
                                print('<td>')
                                print('<INPUT name="%s.%d" id="%s.%d" READONLY class="titlemultiple metainput" value="%s">' % (field, counter, field, counter, id_value))
                                print('</td>')
                                print('</tr>')
                return

        # Create a list of ID types to display as mouse-over help
        type_list = 'The following external identifier types are currently supported:&#13;'
        for identifier_type in sorted(identifier_types, key = identifier_types.get):
                type_name = identifier_types[identifier_type][0]
                type_full_name = identifier_types[identifier_type][1]
                type_list += ' %s: %s&#13;' % (type_name, type_full_name)
        type_list += 'To add another external identifier, click the + button'

        id_count = 0
        # Find the count of external IDs so that we could display the '+' sign for the last one
        for id_type in sorted(external_ids.keys()):
                for id_value in external_ids[id_type]:
                        id_count += 1

        for id_type in sorted(external_ids.keys()):
                for id_value in external_ids[id_type]:
                        counter += 1
                        type_id = external_ids[id_type][id_value][0]
                        printOneExternalID(identifier_types, type_list, type_id, id_value, id_count, field, counter)

        counter += 1
        printOneExternalID(identifier_types, type_list, None, '', id_count, field, counter)

def printOneExternalID(identifier_types, type_list, type_id, id_value, id_count, field, counter):
        print('<tr id="external_id.row.%d">' % counter)
        print('<td class="hint" title="%s">' % type_list)
        print('<select tabindex="1" name="%s_type.%d" id="%s_type.%d">' % (field, counter, field, counter))
        # Display the default value (0)
        print('<option VALUE="0"> </option>')
        for identifier_type in sorted(identifier_types, key = identifier_types.get):
                if identifier_type == type_id:
                        selected = ' selected="selected"'
                else:
                        selected = ''
                print('<option%s VALUE="%d">%s</option>' % (selected, identifier_type, identifier_types[identifier_type][0]))
        print('</select>')
        button = ''
        if counter == (id_count + 1):
                button = createaddbutton('external_id')
        image = ''
        if counter == 1:
                image = _question_mark()
        print('%s%s' % (image, button))
        print('</td>')
        print('<td>')
        print('<INPUT tabindex="1" name="%s.%d" id="%s.%d" class="metainput" value="%s">' % (field, counter, field, counter, id_value))
        print('</td>')
        print('</tr>')


###################################################################
# This function outputs an existing title record in table format
###################################################################
def printtitlerecord(record, index, pub_id, help = None, reuse_page_numbers = 1):

        if not help:
                help = {}

        args = ' READONLY class="%s titlemultiple"'

        print("<tr><td>")
        print('<input name="title_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID]))
        page = SQLGetPageNumber(record[TITLE_PUBID], pub_id)
        if page and reuse_page_numbers:
                print('<input name="title_page%d" tabindex="1" value="%s" class="contentpageinput"></td>' % (index, escape_string(page)))
        else:
                print('<input name="title_page%d" tabindex="1" class="contentpageinput"></td>' % (index))

        print('<td><input name="title_title%d" value="%s"%s></td>' % (index, escape_string(record[TITLE_TITLE]), args % "contentinput"))
        print('<td><input name="title_date%d" value="%s"%s></td>' % (index, record[TITLE_YEAR], args % "contentyearinput"))
        print('<td><input name="title_ttype%d" value="%s"%s></td>' % (index, record[TITLE_TTYPE], args % "contenttypeinput"))

        ###################################
        # STORYLEN
        ###################################
        length = ''
        for storylen in SESSION.db.storylen_codes:
                if record and record[TITLE_STORYLEN] == storylen:
                        length = storylen
                        break
        print('<td><input name="title_storylen%d" value="%s"%s></td>' % (index, length, args % "contentleninput"))
        print('</tr>')

        authors = SQLTitleAuthors(record[TITLE_PUBID])
        counter = 1
        if len(authors):
                for author in authors:
                        print('<tr id="title_author%d.%d.row">' % (index, counter))
                        print('<td><b>Author%d:</b></td>' % (counter))
                        print("""<td><input id="title_author%d.%d" name="title_author%d.%d"
                        value="%s"%s></td>""" % (index, counter, index, counter, escape_string(author), args % "contentinput"))
                        print('</tr>')
                        counter += 1

        printSpacer(5, 'title', index)

def printblanktitlerecord(index, help = None, pub_type = 'NOVEL'):
        if not help:
                help = {}
        args = ' READONLY class="%s titlemultiple"'

        # Use the publication type to determine the default title type for
        # contents titles
        if pub_type == 'OMNIBUS':
                default_title_type = 'NOVEL'
        elif pub_type == 'NONFICTION':
                default_title_type = 'ESSAY'
        else:
                default_title_type = 'SHORTFICTION'

        print('<tr>')
        print('<td><input name="title_id%d" type="HIDDEN">' % (index))
        print('<input name="title_page%d" tabindex="1" class="contentpageinput"></td>' % (index))
        print('<td><input name="title_title%d" tabindex="1" class="contentinput"></td>' % (index))
        print('<td><input name="title_date%d" tabindex="1" class="contentyearinput"></td>' % (index))

        print('<td><select tabindex="1" name="title_ttype%d" class="contenttypeinput">' % (index))
        print('<option selected="selected">%s</option>' % default_title_type)
        for ttype in SESSION.db.regular_title_types:
                if ttype != default_title_type:
                        print('<option>%s</option>' % ttype)
        print('</select></td>')

        print('<td><select tabindex="1" name="title_storylen%d" class="contentleninput">' % (index))
        for storylen in SESSION.db.storylen_codes:
                print('<option>%s</option>' % storylen)
        print('</select></td>')
        print('</tr>')

        counter = 1
        print('<tr id="title_author%d.%d.row">' % (index, counter))
        printContentHeader('Author1:', help)
        print('<td><input tabindex="1" id="title_author%d.%d" name="title_author%d.%d" class="contentinput"></td>' % (index, counter, index, counter))
        print('</tr>')
        counter +=1

        printAddContentAuthor('Author', help, index)
        printSpacer(5, 'title', index)

def printeditabletitlerecord(record, index, container, help, pub_id):
        args = ' class="%s"'
        readonly = False
        # Find out if the title is in more than 1 publication
        manypubs = SQLCountPubsForTitle(record[TITLE_PUBID])
        if manypubs:
                readonly = True
                # Titles in multiple pubs are gray
                args = ' READONLY class="%s titlemultiple"'
        # Containers in just 1 publication are yellow
        elif container:
                args = ' class="%s titlecontainer"'

        if readonly:
                taborder = 0
        else:
                taborder = 1

        print('<tr><td>')
        print('<input name="title_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID]))
        page = SQLGetPageNumber(record[TITLE_PUBID], pub_id)
        # Container titles shouldn't have page numbers, so the page field is not editable
        if container:
                print('<input name="title_page%d" tabindex="0" READONLY class="contentpageinput titlemultiple"></td>' % index)
        # Non-container page numbers are always editable even for read-only titles
        else:
                if page:
                        print('<input name="title_page%d" tabindex="1" value="%s" class="contentpageinput"></td>' % (index, escape_string(page)))
                else:
                        print('<input name="title_page%d" tabindex="1" class="contentpageinput"></td>' % (index))

        print('<td><input name="title_title%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, escape_string(record[TITLE_TITLE]), args % "contentinput"))
        print('<td><input name="title_date%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, record[TITLE_YEAR], args % "contentyearinput"))

        ###################################
        # Title type
        ###################################
        if readonly:
                print('<td><input name="title_ttype%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, record[TITLE_TTYPE], args % "contenttypeinput"))
        else:
                print('<td><select name="title_ttype%d" tabindex="%d" %s>' % (index, taborder, args % "contenttypeinput"))
                for ttype in SESSION.db.regular_title_types:
                        if (record and record[TITLE_TTYPE] == ttype) or (not record and ttype == 'SHORTFICTION'):
                                print('<option selected="selected">%s</option>' % ttype)
                        else:
                                print('<option>%s</option>' % ttype)
                print('</select></td>')

        ###################################
        # STORYLEN
        ###################################
        length = ''
        if record[TITLE_STORYLEN]:
                length = record[TITLE_STORYLEN]
        if readonly:
                print('<td><input name="title_storylen%d" value="%s" tabindex="%d"%s></td>' % (index, length, taborder, args % "contentleninput"))
        else:
                print('<td><select name="title_storylen%d" tabindex="%d"%s>' % (index, taborder, args % "contentleninput"))
                for storylen in SESSION.db.storylen_codes:
                        if record and length == storylen:
                                print('<option selected="selected">%s</option>' % storylen)
                        else:
                                print('<option>%s</option>' % storylen)
                print('</select></td>')
        print('</tr>')

        ###################################
        # AUTHORS
        ###################################

        authors = SQLTitleAuthors(record[TITLE_PUBID])
        counter = 1
        if len(authors):
                for author in authors:
                        print('<tr id="title_author%d.%d.row">' % (index, counter))
                        printContentHeader('Author%d:'% counter, help)
                        print("""<td><input id="title_author%d.%d" name="title_author%d.%d" tabindex="%d"
                        value="%s"%s></td>""" % (index, counter, index, counter, taborder, escape_string(author), args % "contentinput"))
                        print('</tr>')
                        counter += 1
        else:
                print('<tr id="title_author%d.%d.row">' % (index, counter))
                printContentHeader('Author%d:'% counter, help)
                print("""<td><input id="title_author%d.%d" name="title_author%d.%d" tabindex="%d"
                        %s></td>""" % (index, counter, index, counter, taborder, args % "contentinput"))
                print('</tr>')
                counter += 1

        if not readonly:
                printAddContentAuthor('Author', help, index)

        printSpacer(5, 'title', index)

def printfullcoverart(cover, index, help = None, readonly = 0):
        if not help:
                help = {}

        if readonly:
                args = ' READONLY class="%s titlemultiple"'
        else:
                args = ' class="%s"'

        print('<tr>')
        print('<td><input name="cover_id%d" value="%s" type="HIDDEN"></td>' % (index, cover[TITLE_PUBID]))
        print("""<td><input id="cover_title%d" name="cover_title%d"
                 value="%s"%s></td>""" % (index, index, escape_string(cover[TITLE_TITLE]), args % "contentinput"))
        print('<td><input name="cover_date%d" value="%s"%s></td>' % (index, cover[TITLE_YEAR], args % "contentyearinput"))
        print('</tr>')
        artists = SQLTitleAuthors(cover[TITLE_PUBID])
        counter = 1
        if len(artists):
                for artist in artists:
                        print('<tr id="cover_artist%d.%d.row">' % (index, counter))
                        printContentHeader('Artist%d:'% counter, help)
                        print("""<td><input id="cover_artist%d.%d" name="cover_artist%d.%d"
                                 value="%s"%s></td>""" % (index, counter, index, counter, escape_string(artist), args % "contentinput"))
                        print('</tr>')
                        counter += 1
        if not readonly:
                printAddContentAuthor('Artist', help, index)
        printSpacer(3, 'cover', index)

def printbriefblankcoverart(index, help = None):
        if not help:
                help = {}
        counter = 1
        print('<tr>')
        print('<td>')
        print('<input name="cover_id%d" value="0" type="HIDDEN">' % (index))
        print('<input name="cover_title%d" type="HIDDEN">' % (index))
        print('<input name="cover_date%d" type="HIDDEN">' % (index))
        print('</td>')
        print('</tr>')
        print('<tr id="cover_artist%d.%d.row">' % (index, counter))
        printContentHeader('Artist1:', help)
        print('<td><input tabindex="1" id="cover_artist%d.%d" name="cover_artist%d.%d" class="contentinput"></td>' % (index, counter, index, counter))
        print('</tr>')
        counter += 1
        printAddContentAuthor('Artist', help, index)
        printSpacer(2, 'cover', index)

def printreviewrecord(record, index, pub_id, help = None, reuse_page_numbers = 1):
        if not help:
                help = {}
        args = ' READONLY class="%s titlemultiple"'

        print('<tr><td>')
        print('<input name="review_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID]))
        page = SQLGetPageNumber(record[TITLE_PUBID], pub_id)
        if page and reuse_page_numbers:
                print('<input name="review_page%d" tabindex="1" value="%s" class="contentpageinput"></td>' % (index, escape_string(page)))
        else:
                print('<input name="review_page%d" tabindex="1" class="contentpageinput"></td>' % index)

        print('<td><input name="review_title%d" value="%s"%s></td>' % (index, escape_string(record[TITLE_TITLE]), args % "contentinput"))
        print('<td><input name="review_date%d" value="%s"%s></td>' % (index, record[TITLE_YEAR], args % "contentyearinput"))
        print('</tr>')

        counter = 1
        authors = SQLReviewAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print('<tr id="review_author%d.%d.row">' % (index, counter))
                        print('<td><b>Author%d:</b></td>' % counter)
                        print("""<td><input id="review_author%d.%d" name="review_author%d.%d"
                        value="%s"%s></td>""" % (index, counter, index, counter, escape_string(author), args % "contentinput"))
                        print('</tr>')
                        counter += 1

        counter = 1
        authors = SQLTitleAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print('<tr id="review_reviewer%d.%d.row">' % (index, counter))
                        print('<td><b>Reviewer%d:</b></td>' % (counter))
                        print("""<td><input id="review_reviewer%d.%d" name="review_reviewer%d.%d"
                        value="%s"%s></td>""" % (index, counter, index, counter, escape_string(author), args % "contentinput"))
                        print('</tr>')
                        counter += 1

        printSpacer(3, 'review', index)

def printblankreviewrecord(index, help = None):
        if not help:
                help = {}

        print('<tr>')
        print('<td><input name="review_id%d" type="HIDDEN">' % int(index))
        print('<input name="review_page%d" tabindex="1" class="contentpageinput"></td>' % int(index))
        print('<td><input name="review_title%d" tabindex="1" class="contentinput"></td>' % int(index))
        print('<td><input name="review_date%d" tabindex="1" class="contentyearinput"></td>' % int(index))
        print('</tr>')

        counter = 1
        print('<tr id="review_author%d.%d.row">' % (index, counter))
        printContentHeader('Author1:', help)
        print("""<td><input id="review_author%d.%d" name="review_author%d.%d" tabindex="1"
                class="contentinput"></td>""" % (int(index), int(counter), int(index), int(counter)))
        print('</tr>')
        counter += 1
        printAddContentAuthor('Reviewee', help, index)

        counter = 1
        print('<tr id="review_reviewer%d.%d.row">' % (index, counter))
        printContentHeader('Reviewer1:', help)
        print("""<td><input id="review_reviewer%d.%d" name="review_reviewer%d.%d" tabindex="1"
                class="contentinput"></td>""" % (int(index), int(counter), int(index), int(counter)))
        print('</tr>')
        counter += 1
        printAddSecondaryAuthor('Reviewer', help, index)

        printSpacer(3, 'review', index)

def printeditablereviewrecord(record, index, help, pub_id):
        # Find out if this title is in more than 1 publication
        manypubs = SQLCountPubsForTitle(record[TITLE_PUBID])
        if manypubs:
                readonly = True
                args = ' READONLY class="%s titlemultiple"'
                taborder = 0
        else:
                readonly = False
                args = ' class="%s"'
                taborder = 1

        print('<tr><td>')
        print('<input name="review_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID]))
        page = SQLGetPageNumber(record[TITLE_PUBID], pub_id)
        # Page numbers are always editable and included in the tab order
        if page:
                print('<input name="review_page%d" value="%s" tabindex="1" class="contentpageinput"></td>' % (index, escape_string(page)))
        else:
                print('<input name="review_page%d" tabindex="1" class="contentpageinput"></td>' % (index))

        print('<td><input name="review_title%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, escape_string(record[TITLE_TITLE]), args % "contentinput"))
        print('<td><input name="review_date%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, record[TITLE_YEAR], args % "contentyearinput"))
        print('</tr>')

        counter = 1
        authors = SQLReviewAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print('<tr id="review_author%d.%d.row">' % (index, counter))
                        printContentHeader('Author%d:'% counter, help)
                        print("""<td><input id="review_author%d.%d" name="review_author%d.%d" tabindex="%d"
                        value="%s"%s></td>""" % (index, counter, index, counter, taborder, escape_string(author), args % "contentinput"))
                        print('</tr>')
                        counter += 1

        if not readonly:
                printAddContentAuthor('Reviewee', help, index)

        counter = 1
        authors = SQLTitleAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print('<tr id="review_reviewer%d.%d.row">' % (index, counter))
                        printContentHeader('Reviewer%d:'% counter, help)
                        print("""<td><input id="review_reviewer%d.%d" name="review_reviewer%d.%d" tabindex="%d"
                        value="%s"%s></td>""" % (index, counter, index, counter, taborder, escape_string(author), args % "contentinput"))
                        print('</tr>')
                        counter += 1

        if not readonly:
                printAddSecondaryAuthor('Reviewer', help, index)

        printSpacer(3, 'review', index)

def printinterviewrecord(record, index, pub_id, help = None, reuse_page_numbers = 1):
        if not help:
                help = {}

        args = ' READONLY class="%s titlemultiple"'
        print('<tr><td>')
        print('<input name="interview_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID]))

        page = SQLGetPageNumber(record[TITLE_PUBID], pub_id)
        if page and reuse_page_numbers:
                print('<input name="interview_page%d" tabindex="1" value="%s" class="contentpageinput"></td>' % (index, escape_string(page)))
        else:
                print('<input name="interview_page%d" tabindex="1" class="contentpageinput"></td>' % index)

        print('<td><input name="interview_title%d" value="%s"%s></td>' % (index, escape_string(record[TITLE_TITLE]), args % "contentinput"))
        print('<td><input name="interview_date%d" value="%s"%s></td>' % (index, record[TITLE_YEAR], args % "contentyearinput"))
        print('</tr>')

        counter = 1
        authors = SQLInterviewAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print('<tr id="interviewee_author%d.%d.row">' % (index, counter))
                        print('<td><b>Interviewee%d:</b></td>' % (counter))
                        print("""<td><input id="interviewee_author%d.%d" name="interviewee_author%d.%d"
                        value="%s"%s></td>""" % (index, counter, index, counter, escape_string(author), args % "contentinput"))
                        print('</tr>')
                        counter += 1

        counter = 1
        authors = SQLTitleAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print('<tr id="interviewer_author%d.%d.row">' % (index, counter))
                        print('<td><b>Interviewer%d:</b></td>' % (counter))
                        print("""<td><input id="interviewer_author%d.%d" name="interviewer_author%d.%d"
                        value="%s"%s></td>""" % (index, counter, index, counter, escape_string(author), args % "contentinput"))
                        print('</tr>')
                        counter += 1

        printSpacer(3, 'interview', index)

def printblankinterviewrecord(index, help = None):
        if not help:
                help = {}

        print('<tr>')
        print('<td><input name="interview_id%d" type="HIDDEN">' % int(index))
        print('<input name="interview_page%d" tabindex="1" class="contentpageinput"></td>' % int(index))
        print('<td><input name="interview_title%d" tabindex="1" class="contentinput"></td>' % int(index))
        print('<td><input name="interview_date%d" tabindex="1" class="contentyearinput"></td>' % int(index))
        print('</tr>')

        counter = 1
        print('<tr id="interviewee_author%d.%d.row">' % (index, counter))
        printContentHeader('Interviewee1:', help)
        print("""<td><input id="interviewee_author%d.%d" name="interviewee_author%d.%d" tabindex="1"
        class="contentinput"></td>""" % (int(index), int(counter), int(index), int(counter)))
        print('</tr>')
        counter += 1
        printAddContentAuthor('Interviewee', help, index)

        counter = 1
        print('<tr id="interviewer_author%d.%d.row">' % (index, counter))
        printContentHeader('Interviewer1:', help)
        print("""<td><input id="interviewer_author%d.%d" name="interviewer_author%d.%d" tabindex="1"
        class="contentinput"></td>""" % (int(index), int(counter), int(index), int(counter)))
        print('</tr>')
        counter += 1
        printAddSecondaryAuthor('Interviewer', help, index)

        printSpacer(3, 'interview', index)

def printeditableinterviewrecord(record, index, help, pub_id):
        # Find out if this title is in more than 1 publication
        manypubs = SQLCountPubsForTitle(record[TITLE_PUBID])
        if manypubs:
                readonly = True
                args = ' READONLY class="%s titlemultiple"'
                taborder = 0
        else:
                readonly = False
                args = ' class="%s"'
                taborder = 1

        print('<tr><td>')
        print('<input name="interview_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID]))
        page = SQLGetPageNumber(record[TITLE_PUBID], pub_id)
        # Page numbers are always editable and belong to the primary tab group
        if page:
                print('<input name="interview_page%d" value="%s" tabindex="1" class="contentpageinput"></td>' % (index, escape_string(page)))
        else:
                print('<input name="interview_page%d" tabindex="1" class="contentpageinput"></td>' % index)

        print('<td><input name="interview_title%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, escape_string(record[TITLE_TITLE]), args % "contentinput"))

        print('<td><input name="interview_date%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, record[TITLE_YEAR], args % "contentyearinput"))
        print("</tr>")

        counter = 1
        authors = SQLInterviewAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print('<tr id="interviewee_author%d.%d.row">' % (index, counter))
                        printContentHeader('Interviewee%d:'% counter, help)
                        print("""<td><input id="interviewee_author%d.%d" name="interviewee_author%d.%d" tabindex="%d"
                        value="%s"%s></td>""" % (index, counter, index, counter, taborder, escape_string(author), args % "contentinput"))
                        print('</tr>')
                        counter += 1

        if not readonly:
                printAddContentAuthor('Interviewee', help, index)

        counter = 1
        authors = SQLTitleAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print('<tr id="interviewer_author%d.%d.row">' % (index, counter))
                        printContentHeader('Interviewer%d:'% counter, help)
                        print("""<td><input id="interviewer_author%d.%d" name="interviewer_author%d.%d" tabindex="%d"
                        value="%s"%s></td>""" % (index, counter, index, counter, taborder, escape_string(author), args % "contentinput"))
                        print('</tr>')
                        counter += 1

        if not readonly:
                printAddSecondaryAuthor('Interviewer', help, index)

        printSpacer(3, 'interview', index)

def printtextarea(label, fieldname, help, notes = '', rows = 4, readonly = 0):
        print('<tr>')
        
        if readonly:
                args = ' READONLY class="%s titlemultiple"'
        else:
                args = ' class="%s"'

        printfieldlabel(label, help)
        print('<td>')
        print('<textarea tabindex="1" name="%s" rows="%s"%s cols="60">' % (fieldname, rows, args % "metainput"))
        if notes:
                print(ISFDBText(notes, True))
        print('</textarea>')
        print('</td>')
        print('</tr>')

def printsource(help):
        print('<tr>')
        if help.get("Source"):
                print('<td class="hint" title="%s"><b>Source of the data: </b>' % (help['Source'][0]))
                print(_question_mark())
                print('</td>')
        else:
                print('<td><b>Source of the data: </b></td>')
        print('<td>')
        print('<input type="radio" name="Source" value="Primary">I own this publication (will be auto-verified as Primary)<br>')
        print('<input type="radio" name="Source" value="Transient">I am working from this publication but will not have it permanently (will be auto-verified as Transient)<br>')
        print('<input type="radio" name="Source" value="PublisherWebsite">Publisher\'s website<br>')
        print('<input type="radio" name="Source" value="AuthorWebsite">Author\'s website<br>')
        print('<input type="radio" tabindex="1" name="Source" value="Other" CHECKED>Other website, later printing/edition or another source (please explain in Publication Note)')
        print('</td>')
        print('</tr>')

def printAddContentAuthor(type, help, index):
        print('<tr id="Add%s%d">' % (type, int(index)))
        print('<td>&nbsp;</td>')
        if type == 'Author':
                button_id = 'addContentTitleAuthor'
                label = 'Author'
        elif type == 'Reviewee':
                button_id = 'addReviewee'
                label = 'Author'
        elif type == 'Interviewee':
                button_id = 'addInterviewee'
                label = 'Interviewee'
        elif type == 'Artist':
                button_id = 'addArtist'
                label = 'Artist'

        # Only display the help pop-up for the first occurence of this button
        if help.get(('Add '+label)) and int(index) < 2:
                print('<td class="hint" title="%s">' % help[('Add '+label)][0])
                print('<input id="%s.button.%d" type="button" tabindex="1" value="Add %s">' % (button_id, int(index), label))
                print(_question_mark())
                print('</td>')
        else:
                print('<td><input id="%s.button.%d" type="button" tabindex="1" value="Add %s"></td>' % (button_id, int(index), label))
        print('</tr>')

def printAddSecondaryAuthor(type, help, index):
        print('<tr id="Add%s%d">' % (type, int(index)))
        print('<td>&nbsp;</td>')
        if help.get(('Add '+type)) and int(index) < 2:
                print('<td class="hint" title="%s">' % help[('Add '+type)][0])
                print('<input id="add%s.button.%d" type="button" tabindex="1" value="Add %s">' % (type, int(index), type))
                print(_question_mark())
                print('</td>')
        else:
                print('<td><input id="add%s.button.%d" type="button" tabindex="1" value="Add %s"></td>' % (type, int(index), type))
        print('</tr>')


def printContentHeader(label, help, index = 1):
        # The 4th parameter is '' in order to avoid displaying a colon
        printfieldlabel(label, help, index, '')

def printNewBriefCoverButton():
        printNewRecordButton('Cover', 'addNewBriefCover')

def printNewFullCoverButton():
        printNewRecordButton('Cover', 'addNewFullCover')

def printNewTitleButton():
        printNewRecordButton('Title', 'addNewTitle')

def printNewReviewButton():
        printNewRecordButton('Review', 'addNewReview')

def printNewInterviewButton():
        printNewRecordButton('Interview', 'addNewInterview')

def printNewRecordButton(record_type, listener):
        print('<tr id="Add%s">' % record_type)
        print('<td>&nbsp;</td>')
        print('<td><input type="button" id="%s" value="Add %s" tabindex="1"></td>' % (listener, record_type))
        print('</tr>')

def printfieldlabel(label, help, index = 1, colon = ':', addbutton = None):
        # Only display the help pop-up for the first occurrence of repeating fields
        if help and help.get(label) and (int(index) < 2):
                text = escape_string(help[label][0])
                display = '<td class="hint" title="%s"><b>%s%s </b>' % (text, label, colon)
                image = _question_mark()
                if help[label][1]:
                        display += '<a tabindex="0" href="%s">%s</a>' % (help[label][1], image)
                else:
                        display += image
        else:
                display = '<td><b>%s%s</b>' % (label, colon)
        if addbutton:
                display += addbutton
        display += '</td>'
        print(display)

def printfield(label, fieldname, help = None, value = '', readonly = 0, addbutton = None):
        if readonly:
                args = ' READONLY class="%s titlemultiple"'
        else:
                args = ' class="%s"'
        print('<tr id="%s.row">' % fieldname)

        printfieldlabel(label, help, 1, ":", addbutton)

        if value is not None:
                       print('<td><INPUT tabindex="1" name="%s" id="%s" value="%s"%s></td>' % (fieldname, fieldname, escape_string(value), args % "metainput"))
        else:
                       print('<td><INPUT tabindex="1" name="%s" id="%s"%s></td>' % (fieldname, fieldname, args % "metainput"))
        print('</tr>')

def printAwardName(field, label, help):
        print('<tr>')
        printfieldlabel(label, help)
        print('<td><select name="%s" tabindex="1">' % (field))
        award_types = SQLListAwardTypes()
        for award_type in award_types:
                print('<option value="%d">%s</option>' % (int(award_type[AWARD_TYPE_ID]), award_type[AWARD_TYPE_NAME]))
        print('</select></td>')
        print('</tr>')

def printAwardCategory(field, label, award_type_id, default_award_cat_id, help):
        print('<tr>')
        printfieldlabel(label, help)
        print('<td><select name="%s" tabindex="1">' % (field))
        award_cats = SQLGetAwardCategories(award_type_id)
        for award_cat in award_cats:
                if int(award_cat[AWARD_CAT_ID]) == default_award_cat_id:
                        print('<option selected="selected" value="%d">%s</option>' % (award_cat[AWARD_CAT_ID], award_cat[AWARD_CAT_NAME]))
                else:
                        print('<option value="%d">%s</option>' % (award_cat[AWARD_CAT_ID], award_cat[AWARD_CAT_NAME]))
        print('</select></td>')
        print('</tr>')

def printAwardLevel(label, value, poll, help):
        from awardClass import awardShared
        print('<tr>')
        printfieldlabel(label, help)
        print('<td>')
        # For non-poll awards, display Win/Nomination radio buttons
        if poll == 'No':
                if value == '1':
                        print('<INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_WIN" VALUE="WIN" CHECKED tabindex="1">Win')
                        print('<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_NOM" VALUE="NOM" tabindex="1">Nomination')
                elif int(value) < 71:
                        print('<INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_WIN" VALUE="WIN" tabindex="1">Win')
                        print('<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_NOM" VALUE="NOM" CHECKED tabindex="1">Nomination')
                else:
                        print('<INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_WIN" VALUE="WIN" tabindex="1">Win')
                        print('<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_NOM" VALUE="NOM" tabindex="1">Nomination')
        # For poll awards, display the level radio button and the "Poll place" field
        else:
                # '0' is the value for new poll awards, so the "Poll place" field should be blank
                if value == '0':
                        print('<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_LEVEL" VALUE="LEVEL" CHECKED tabindex="1">Poll place:')
                        print('<INPUT NAME="award_level" SIZE=5 VALUE="" tabindex="1">')
                elif int(value) < 71:
                        print('<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_LEVEL" VALUE="LEVEL" CHECKED tabindex="1">Poll place:')
                        print('<INPUT NAME="award_level" SIZE=5 VALUE="%s" tabindex="1">' % value)
                else:
                        print('<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_LEVEL" VALUE="LEVEL" tabindex="1">Poll place:')
                        print('<INPUT NAME="award_level" SIZE=5 VALUE="" tabindex="1">')
        # Special awards section
        if int(value)>70:
                print('<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_SPECIAL" VALUE="SPECIAL" CHECKED tabindex="1">Special:')
        else:
                print('<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_SPECIAL" VALUE="SPECIAL" tabindex="1">Special:')
        special_levels = awardShared.SpecialAwards()
        print('<select NAME="award_special" tabindex="1">')
        for special_level in sorted(special_levels.keys()):
                if special_level == value:
                        print('<option selected="selected" value="%s">%s</option>' % (special_level, special_levels[special_level]))
                else:
                        print('<option value="%s">%s</option>' % (special_level, special_levels[special_level]))
        print('</select></td>')
        print('</tr>')

def printSpacer(rows, row_id, index):
        print('<tr id="%s_id%d.row" class="titleeditspacer"><td colspan="%d"> </td></tr>' % (row_id, index, rows))

def printmultiple(values, label, field_name, help = None, readonly = 0):
        if not help:
                help = {}
        counter = 1
        for value in values:
                if not readonly and counter == len(values):
                        addbutton = createaddbutton(field_name)
                else:
                        addbutton = None
                printfield(("%s %d" % (label, counter)), ("%s%d" % (field_name, counter)), help, value, readonly, addbutton)
                counter += 1

        if not readonly and not values:
                addbutton = createaddbutton(field_name)
                printfield(("%s %d" % (label, counter)), ("%s%d" % (field_name, counter)), help, '', readonly, addbutton)

def createaddbutton(field_name):
        button_span = ' <span id="%s.addbutton"><input id="%s.addsign"' % (field_name, field_name)
        button_span += ' class="addbutton" type="button" value="+" tabindex="1"></span>'
        return button_span

def printWebPages(webpages, web_page_type, help, display_name = '', readonly = 0):
        if display_name:
                printmultiple(webpages, "%s Web Page" % display_name, "%s_webpages" % web_page_type, help, readonly)
        else:
                printmultiple(webpages, "Web Page", "%s_webpages" % web_page_type, help, readonly)

def printHelpBox(record_type, helplink, new_flag = 0):
        print('<div id="HelpBox">')
        if new_flag:
                print('<b>Help on adding new %s records:</b>' % record_type)
        else:
                print('<b>Help on editing %s records:</b>' % record_type)
        print('<ul>')
        print('<li><a href="%s://%s/index.php/Help:Screen:%s">Help:Screen:%s</a>' % (PROTOCOL, WIKILOC, helplink, helplink))
        print('<li><a href="%s://%s/index.php/Help:Using_Templates_and_HTML_in_Note_Fields">List of supported templates and HTML tags in notes</a>' % (PROTOCOL, WIKILOC))
        print('</ul>')
        print('</div>')

def printISBN(help, isbn):
        from isbn import convertISBN, validISBN
        if isbn:
                if not validISBN(isbn):
                        printfield("ISBN", "pub_isbn", help, isbn)
                else:
                        printfield("ISBN", "pub_isbn", help, convertISBN(isbn))
        else:
                printfield("ISBN", "pub_isbn", help)
        
def printdropdown(label, fieldname, values, help):
        # 'values' is a dictionary where the dictionary keys are the supported values
        # and the distionary values are 1 for "selected" and 0 for not selected.
        print('<tr>')
        printfieldlabel(label, help)
        print('<td>')
        print('<select name="%s" tabindex="1">' % fieldname)
        for value in values:
                if values[value]:
                        print('<option selected="selected">%s</option>' % value)
                else:
                        print('<option>%s</option>' % value)
        print('</select>')
        print('</td>')
        print('</tr>')

def printTitleFlags(record, help):
        if record:
                non_genre = record[TITLE_NON_GENRE]
        else:
                non_genre = ''
        if record:
                juvenile = record[TITLE_JVN]
        else:
                juvenile = ''
        if record:
                novelization = record[TITLE_NVZ]
        else:
                novelization = ''
        disabled = ''
        if record:
                graphic = record[TITLE_GRAPHIC]
                if record[TITLE_TTYPE] in ('COVERART', 'INTERIORART'):
                        disabled = 'disabled'
        else:
                graphic = ''

        print('<tr>')
        printfieldlabel('Title Flags', help)
        print('<td>')
        print('<table class="checkboxheaders">')
        print('<tbody>')
        printcheckboxheaders(('Non-Genre', 'Juvenile', 'Novelization', 'Graphic Format'), help)
        print('<tr>')
        printcheckbox('title_non_genre', non_genre, '', help)
        printcheckbox('title_jvn', juvenile, '', help)
        printcheckbox('title_nvz', novelization, '', help)
        printcheckbox('title_graphic', graphic, disabled, help)
        print('</tr>')
        print('</tbody>')
        print('</table>')
        print('</td>')
        print('</tr>')

def printcheckboxheaders(headers, help):
        print('<tr>')
        for header in headers:
                printfieldlabel(header, help, 1, '')
                print('<td class="checkboxseparator"></td>')
        print('</tr>')

def printcheckbox(fieldname, current_value, disabled, help):
        print('<td class="titleflags">')
        # Displays a checkbox. If "current_value" is "Yes", then it will be checked
        checked = ''
        if current_value == 'Yes':
                checked = 'checked'
        if disabled == 'disabled':
                disabled = 'disabled readonly'
                tabindex = '0'
        else:
                tabindex = '1'
        print('<input type="checkbox" tabindex="%s" name="%s" value="on" %s %s>' % (tabindex, fieldname, disabled, checked))
        print('</td>')
        print('<td class="checkboxseparator"></td>')
