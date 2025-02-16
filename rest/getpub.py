#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 669 $
#     Date: $Date: 2021-06-29 15:17:13 -0400 (Tue, 29 Jun 2021) $

from isfdb import *
from isbn import *
from SQLparsing import *
from pub_output import pubOutput


if __name__ == '__main__':

        print('Content-type: text/html\n')

        isbns = isbnVariations(SESSION.Parameter(0, 'str'))
        if not isbns:
                print("getpub.cgi: Bad ISBN")
                sys.exit(1)

        pub_bodies = SQLFindPubsByIsbn(isbns)
        pubOutput(pub_bodies)
