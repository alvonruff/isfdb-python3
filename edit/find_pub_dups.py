#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1166 $
#     Date: $Date: 2024-02-08 14:50:44 -0500 (Thu, 08 Feb 2024) $


from isfdb import *
from isfdblib import *


if __name__ == '__main__':

        pub_id = SESSION.Parameter(0, 'int')
        pub_data = SQLGetPubById(pub_id)
        if not pub_data:
                SESSION.DisplayError('Record Does Not Exist')
        titles = SQLloadTitlesXBT(pub_id)
        if not titles:
                SESSION.DisplayError('Publication Record Contains No Titles')

        ##################################################################
        # Output the leading HTML stuff
        ##################################################################
        PrintPreSearch('Duplicate Finder for %s' % pub_data[PUB_TITLE])
        PrintNavBar('edit/find_pub_dups.cgi', pub_id)

        print('<div id="HelpBox">')
        print('<b>Help on merging titles: </b>')
        print('<a href="%s://%s/index.php/Help:How to merge titles">Help:How to merge titles</a><p>' % (PROTOCOL, WIKILOC))
        print('</div>')

        print('<h3>Note: Unlike the Duplicate Finder for author records, the Duplicate Finder for \
                publication records does not identify potential duplicates with different capitalization. \
                Also, be sure to check the title types and languages carefully before merging.</h3>')
        print('<p>')
        print('<hr>')

        found = 0

        for title in titles:
                if title[TITLE_TTYPE] != 'REVIEW':
                        found += CheckOneTitleForDuplicates(title)

        if not found:
                print('<h2>No duplicate candidates found.</h2>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)
