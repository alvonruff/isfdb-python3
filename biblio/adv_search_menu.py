#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Ahasuerus and Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 917 $
#     Date: $Date: 2022-05-15 17:54:21 -0400 (Sun, 15 May 2022) $


from isfdb import *
from SQLparsing import *
from common import *
from login import User

class AdvancedSearchMenu:
        def __init__(self):
                self.user = User()
                self.user.load()
        
        def display_selection(self):
                PrintHeader('Advanced Search')
                PrintNavbar('adv_search_menu', 0, 0, 0, 0)
                print('<ul>')
                print('<li>A downloadable version of the ISFDB database is available <a href="%s://%s/index.php/ISFDB_Downloads">here</a>' % (PROTOCOL, WIKILOC))
                print('</ul>')

                if not self.user.id:
                        print('<h3>For performance reasons, Advanced Searches are currently restricted to registered users.</h3>')
                else:
                        print('<hr>')
                        print('<ul>')
                        print('<li><b>Custom Searches of Individual Record Types:</b>')
                        print('<ul>')
                        print('<li>%s' % ISFDBLink('adv_search_selection.cgi', 'author', 'Authors'))
                        print('<li>%s' % ISFDBLink('adv_search_selection.cgi', 'title', 'Titles'))
                        print('<li>%s' % ISFDBLink('adv_search_selection.cgi', 'series', 'Series'))
                        print('<li>%s' % ISFDBLink('adv_search_selection.cgi', 'pub', 'Publications'))
                        print('<li>%s' % ISFDBLink('adv_search_selection.cgi', 'publisher', 'Publishers'))
                        print('<li>%s' % ISFDBLink('adv_search_selection.cgi', 'pub_series', 'Publication Series'))
                        print('<li>%s' % ISFDBLink('adv_search_selection.cgi', 'award_type', 'Award Types'))
                        print('<li>%s' % ISFDBLink('adv_search_selection.cgi', 'award_cat', 'Award Categories'))
                        print('<li>%s' % ISFDBLink('adv_search_selection.cgi', 'award', 'Awards'))
                        print('</ul>')
                        print('<li><b>Other Searches:</b>')
                        print('<ul>')
                        print('<li>%s' % ISFDBLink('adv_identifier_search.cgi', '', 'Publication Search by External Identifier'))
                        print('<li>%s' % ISFDBLink('adv_notes_search.cgi', '', 'Notes Search'))
                        print('<li>%s' % ISFDBLink('adv_web_page_search.cgi', '', 'Web Page Search'))
                        print('<li>%s' % ISFDBLink('adv_user_search.cgi', '', 'User Search'))
                        print('</ul>')
                        print('</ul>')
                print('<p><hr><p>')
                self.print_google_search()
                PrintTrailer('adv_search_menu', 0, 0)

        def print_google_search(self):
                print('<h2>Search the ISFDB database using Google:</h2>')
                print('<form METHOD="GET" action="%s:/%s/google_search_redirect.cgi" accept-charset="utf-8">' % (PROTOCOL, HTFAKE))
                print('<p>')
                print('<select NAME="PAGE_TYPE">')
                print('<option VALUE="name">Name')
                print('<option VALUE="title">Title')
                print('<option VALUE="series">Series')
                print('<option VALUE="publication">Publication')
                print('<option VALUE="pubseries">Publication Series')
                print('<option VALUE="publisher">Publisher')
                print('<option VALUE="award_category">Award Category')
                print('</select>')

                print('<select NAME="OPERATOR">')
                print('<option VALUE="exact">contains exact word')
                print('<option SELECTED VALUE="approximate">contains approximate word')
                print('</select>')

                print('<input NAME="SEARCH_VALUE" SIZE="50">')
                print('<p>')

                print('<input TYPE="SUBMIT" VALUE="Submit Query">')
                print('</form>')

        
if __name__ == '__main__':
        search = AdvancedSearchMenu()
        search.display_selection()
