#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2009-2026   Ahasuerus, Bill Longley, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


from isfdb import *
from common import *
from login import *


if __name__ == '__main__':

        user = User()
        user.load()
        if not user.id:
                SESSION.DisplayError('You must be logged in to modify your user preferences')

        PrintHeader("User Preferences")
        PrintNavbar('mypreferences', 0, 0, 'mypreferences.cgi', 0)
       
        print('<p>')
        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/submitpreferences.cgi">')
        print('<ul>')
        print('<li>%s</li>' % ISFDBLink('edit/keygen.cgi', '', 'Key Maintenance'))
        print('<li>%s</li>' % ISFDBLink('mywebsites.cgi', '', 'My Web Sites'))

        print('<li><b>Publication Pages</b>')
        
        print('<ul>')
        concise_checked = ''
        if user.concise_display:
                concise_checked = 'checked'
        print('<li><input type="checkbox" name="concise_display" value="on" %s>%s</li>' % (concise_checked,
                                                                                           "Use concise Publication listing by default"))
        print('</ul>')

        print('<li><b>Title Pages</b>')
        print('<ul>')
        
        covers_checked = ''
        if user.covers_display:
                covers_checked = 'checked'
        print('<li><input type="checkbox" name="covers_display" value="on" %s>%s</li>' % (covers_checked,
                                                                                          "Display cover images on Title pages"))

        suppress_bibliographic_warnings = ''
        if user.suppress_bibliographic_warnings:
                suppress_bibliographic_warnings = 'checked'
        print('<li><input type="checkbox" name="suppress_bibliographic_warnings" value="on" %s>%s</li>' % (suppress_bibliographic_warnings,
                                                                                                           "Do not display bibliographic warnings on Title pages"))

        suppress_awards = ''
        if user.suppress_awards:
                suppress_awards = 'checked'
        print('<li><input type="checkbox" name="suppress_awards" value="on" %s>%s</li>' % (suppress_awards,
                                                                                           "Do not display awards on Title pages"))

        suppress_reviews = ''
        if user.suppress_reviews:
                suppress_reviews = 'checked'
        print('<li><input type="checkbox" name="suppress_reviews" value="on" %s>%s</li>' % (suppress_reviews,
                                                                                            "Do not display reviews on Title pages"))

        cover_links_display = ''
        if user.cover_links_display:
                cover_links_display = 'checked'
        print('<li><input type="checkbox" name="cover_links_display" value="on" %s>%s</li>' % (cover_links_display,
                                                                                               "Display cover scan indicators on Title and search pages"))
        print('</ul>')

        print('<li><b>Searching</b>')
        print('<ul>')
        
        keep_spaces_in_searches = ''
        if user.keep_spaces_in_searches:
                keep_spaces_in_searches = 'checked'
        print('<li><input type="checkbox" name="keep_spaces_in_searches" value="on" %s>%s</li>' % (keep_spaces_in_searches,
                                                                                                   "Keep leading and trailing spaces when searching"))
        print('</ul>')

        print('<li><b>Editing</b>')
        print('<ul>')
        
        suppress_help_bubbles = ''
        if user.suppress_help_bubbles:
                suppress_help_bubbles = 'checked'
        print('<li><input type="checkbox" name="suppress_help_bubbles" value="on" %s>%s</li>' % (suppress_help_bubbles,
                                                                                                 "Do not display mouseover help on Edit pages"))

        if SQLisUserModerator(user.id):
                display_post_submission = ''
                if user.display_post_submission:
                        display_post_submission = 'checked'
                print('<li><input type="checkbox" name="display_post_submission" value="on" %s>%s</li>' % (display_post_submission,
                                                                                                           "Display post-submission review pages"))

        print('<li>Default author/title language when editing records: ')
        print('<select name="default_language">')

        # Iterate over an alphabetized list of language names (excluding 'None' in the 0th position)
        # and display them in a drop-down list
        for language_name in sorted(LANGUAGES[1:]):
                language_id = list(LANGUAGES).index(language_name)
                # If this language is the user's current default language, then select it
                if language_name == LANGUAGES[user.default_language]:
                        print('<option selected="selected" value="%s">%s</option>' % (language_id, language_name))
                # Otherwise this language is displayed, but is not "selected"
                else:
                        print('<option value="%s">%s</option>' % (language_id, language_name))
        print('</select>')

        print('</ul>')

        print('<li><b>Translations</b>')
        print('<ul>')

        print('<li>Display translations on Author and Series pages: ')
        print('<select name="display_all_languages">')
        for value in ('All', 'None', 'Selected'):
                if value == user.display_all_languages:
                        print('<option selected="selected">%s</option>' % value)
                else:
                        print('<option>%s</option>' % value)
        print('</select>')
        print(' (if you chose "Selected", you should also set up %s)' % ISFDBLink('mylanguages.cgi', '', 'Translation Preferences'))

        display_title_translations = ''
        if user.display_title_translations:
                display_title_translations = 'checked'
        print('<li><input type="checkbox" name="display_title_translations" value="on" %s>%s</li>' % (display_title_translations,
                                                                                                      "Display translations on Title pages"))

        suppress_translation_warnings = ''
        if user.suppress_translation_warnings:
                suppress_translation_warnings = 'checked'
        print('<li><input type="checkbox" name="suppress_translation_warnings" value="on" %s>%s</li>' % (suppress_translation_warnings,
                                                                                                         "Do not display translation warnings on Author and Series pages"))

        print('</ul>')

        print('</ul>')
        print('<p>')
        print('<input type="SUBMIT" value="Update Preferences">')
        print('</form>')

        PrintTrailer('mypreferences', 0, 0)

