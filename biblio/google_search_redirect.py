#!_PYTHONLOC
#
#     (C) COPYRIGHT 2018-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1263 $
#     Date: $Date: 2026-02-19 16:39:39 -0500 (Thu, 19 Feb 2026) $


from isfdb import *
import cgi
from library import ISFDBExternalRedirect

class GoogleSearch:
        def __init__(self):
                self.page_type = ''
                self.page_types = {'name': 'Summary Bibliography',
                                   'title': 'Title',
                                   'series': 'Series',
                                   'publication': 'Publication',
                                   'pubseries': 'Publication Series',
                                   'publisher': 'Publisher',
                                   'award_category': 'Award Category'}
                self.search_value = ''
                self.operator = ''
                self.operators = ('exact', 'approximate')

        def get_search_parameters(self):
                form = IsfdbFieldStorage()
                try:
                        self.page_type = self.page_types[form['PAGE_TYPE'].value]
                except:
                        SESSION.DisplayError('Invalid Page Type')

                try:
                        self.search_value = form['SEARCH_VALUE'].value
                        self.search_value = Portable_urllib_quote(str.strip(self.search_value))
                except:
                        SESSION.DisplayError('No search value specified')

                try:
                        self.operator = form['OPERATOR'].value
                        if self.operator not in self.operators:
                                raise
                except:
                        SESSION.DisplayError('Invalid operator specified')

        def redirect(self):
                url = 'https://www.google.com/search?q='
                if self.operator == 'approximate':
                        url += '+intitle:"%s:"+~intitle:%s+' % (self.page_type, self.search_value)
                else:
                        url += '+allintitle:"%s:"+~intitle:"%s"+' % (self.page_type, self.search_value)
                url += 'site:www.isfdb.org+filetype:cgi'
                url += '+-intitle:"Publications not in a Publication Series"'
                url += '+-intitle:"Publisher Directory"'
                url += '&filter=0'
                ISFDBExternalRedirect(url)

if __name__ == '__main__':

        search = GoogleSearch()
        search.get_search_parameters()
        search.redirect()

