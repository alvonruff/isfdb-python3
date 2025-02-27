#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2009-2025   Ahasuerus, Bill Longley, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended serieslication of such source code.
#
#     Version: $Revision: 713 $
#     Date: $Date: 2021-08-27 10:38:44 -0400 (Fri, 27 Aug 2021) $

        
import cgi
import sys
from login import *
from SQLparsing import *
from common import *

def DoError(message):
        PrintHeader("Preferences Update")
        PrintNavbar("preferences", 0, 0, 0, 0)
        print('<h2>%s</h2>' % message)
        sys.exit(0)
        
if __name__ == '__main__':

        user = User()
        user.load()
        if not user.id:
                DoError('You must be logged in to modify your preferences')
        user_id = int(user.id)
        
        sys.stderr = sys.stdout
        form = IsfdbFieldStorage()

        #Initialize the value of the "Display Concise publication listing by default" user preference
        concise_display = 0
        if "concise_display" in form:
                concise_display = 1

        #Initialize the value of the "Display cover images on the Title page by default" user preference
        covers_display = 0
        if "covers_display" in form:
                covers_display = 1

        # Set the default language to 17 (English) even though the HTML form should always have a language code defined
        default_language = 17
        if "default_language" in form:
                default_language = int(form["default_language"].value)

        #Initialize the value of the "Do not display translation warnings on Bibliography pages" user preference
        suppress_translation_warnings = 0
        if "suppress_translation_warnings" in form:
                suppress_translation_warnings = 1

        #Initialize the value of the "Do not display bibliographic warnings on Title pages" user preference
        suppress_bibliographic_warnings = 0
        if "suppress_bibliographic_warnings" in form:
                suppress_bibliographic_warnings = 1

        #Initialize the value of the "Do not display awards on Title pages" user preference
        suppress_awards = 0
        if "suppress_awards" in form:
                suppress_awards = 1

        #Initialize the value of the "Do not display reviews on Title pages" user preference
        suppress_reviews = 0
        if "suppress_reviews" in form:
                suppress_reviews = 1

        #Initialize the value of the "Display cover scan indicators on Title and search pages" user preference
        cover_links_display = 0
        if "cover_links_display" in form:
                cover_links_display = 1

        #Initialize the value of the "Keep leading and trailing spaces when searching" user preference
        keep_spaces_in_searches = 0
        if "keep_spaces_in_searches" in form:
                keep_spaces_in_searches = 1

        #Initialize the value of the "Do not display mouseover help on Edit pages" user preference
        suppress_help_bubbles = 0
        if "suppress_help_bubbles" in form:
                suppress_help_bubbles = 1

        #Initialize the value of the "Display post-submission review pages" user preference
        display_post_submission = 0
        if "display_post_submission" in form:
                display_post_submission = 1

        #Initialize the value of the "Display translations on Title pages" user preference
        display_title_translations = 0
        if "display_title_translations" in form:
                display_title_translations = 1

        #Retrieve the value of the "Display translations" drop-down list
        try:
                display_all_languages = form["display_all_languages"].value
                # Check that the submitted value is allowed
                if display_all_languages not in ('All', 'None', 'Selected'):
                        raise
        except:
                DoError('Invalid value of the "Display Translations" field')

        #If this user's preferences are currently not defined, create a new record
        if not user.preferences_id:
                update = """insert into user_preferences(user_id, concise_disp, display_all_languages,
                        default_language, covers_display, suppress_translation_warnings,
                        suppress_bibliographic_warnings, cover_links_display, keep_spaces_in_searches,
                        suppress_help_bubbles, suppress_awards, suppress_reviews, display_post_submission,
                        display_title_translations)
                        values(%d, %d, '%s', %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d
                        )""" % (user_id, concise_display, display_all_languages, default_language, covers_display,
                                suppress_translation_warnings, suppress_bibliographic_warnings,
                                cover_links_display, keep_spaces_in_searches, suppress_help_bubbles,
                                suppress_awards, suppress_reviews, display_post_submission,
                                display_title_translations)

        #If this user's preferences are currently defined, update them
        else:
                update = "update user_preferences set concise_disp = %d, " % concise_display
                update += "display_all_languages = '%s', " % display_all_languages
                update += "default_language = %d, " % default_language
                update += "covers_display = %d, " % covers_display
                update += "suppress_translation_warnings = %d, " % suppress_translation_warnings
                update += "suppress_bibliographic_warnings = %d, " % suppress_bibliographic_warnings
                update += "cover_links_display = %d, " % cover_links_display
                update += "keep_spaces_in_searches = %d, " % keep_spaces_in_searches
                update += "suppress_help_bubbles = %d, " % suppress_help_bubbles
                update += "suppress_awards = %d, " % suppress_awards
                update += "suppress_reviews = %d, " % suppress_reviews
                update += "display_post_submission = %d, " % display_post_submission
                update += "display_title_translations = %d " % display_title_translations
                update += "where user_pref_id =%d" % user.preferences_id
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)
        
        ISFDBLocalRedirect('index.cgi')
