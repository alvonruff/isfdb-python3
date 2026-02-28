#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2026   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1249 $
#     Date: $Date: 2026-02-09 15:01:59 -0500 (Mon, 09 Feb 2026) $

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
