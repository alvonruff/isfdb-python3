#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Ahasuerus and Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 722 $
#     Date: $Date: 2021-08-30 09:58:34 -0400 (Mon, 30 Aug 2021) $


from isfdb import *
from SQLparsing import *
from common import *
from advSearchClass import AdvancedSearch

class AdvancedWebPageSearch(AdvancedSearch):
        
        def display_selection(self):
                PrintHeader('Web Page Search')
                PrintNavbar('adv_web_page_search', 0, 0, 0, 0)
                self.print_full_header()
                self.print_web_page_search()
                PrintTrailer('adv_web_page_search', 0, 0)

        def print_web_page_search(self):
                print('<h2>Web Page Search</h2>')
                print('<form METHOD="GET" action="%s:/%s/webpages_search_results.cgi">' % (PROTOCOL, HTFAKE))
                print('<p>')
                print('Web Page ')
                print('<select NAME="OPERATOR">')
                print('<option SELECTED VALUE="contains">contains')
                print('<option VALUE="exact">is exactly')
                print('<option VALUE="starts_with">starts with')
                print('<option VALUE="ends_with">ends with')
                print('</select>')
                print('<input NAME="WEBPAGE_VALUE" SIZE="100">')
                print('<p>')
                print('<input TYPE="SUBMIT" VALUE="Submit Query">')
                print('</form>')

        
if __name__ == '__main__':
        search = AdvancedWebPageSearch()
        search.display_selection()
