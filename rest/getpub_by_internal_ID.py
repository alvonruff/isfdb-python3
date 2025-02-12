#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 669 $
#     Date: $Date: 2021-06-29 15:17:13 -0400 (Tue, 29 Jun 2021) $

from isfdb import *
from SQLparsing import SQLGetPubById
from pub_output import pubOutput


if __name__ == '__main__':

        print 'Content-type: text/html\n'

        id_value = SESSION.Parameter(0, 'int')
        if not id_value:
                print """getpub_by_internal_ID.cgi: Bad query.
                        The parameter should be the internal ID of the requested publication record."""
                sys.exit(1)

        pub_body = SQLGetPubById(id_value)
        if not pub_body:
                print """getpub_by_internal_ID.cgi: Bad query.
                        Requested internal publication ID does not exist."""
                sys.exit(1)

        pub_bodies = []
        pub_bodies.append(pub_body)
        pubOutput(pub_bodies)
