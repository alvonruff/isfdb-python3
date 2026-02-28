#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2014/01/10 04:12:16 $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        BINDINGS = ('unknown','hc','tp','pb','ph','digest','dos','ebook','webzine','pulp','bedsheet','tabloid','A4','A5','quarto','octavo','audio CD','audio MP3 CD','audio cassette','audio LP','digital audio player','digital audio download','other')
        for binding in BINDINGS:
                update = "update pubs set pub_ptype='%s' where pub_ptype = '%s'" % (binding, binding)
                print(update)
                if debug == 0:
                        CNX = MYSQL_CONNECTOR()
                        CNX.DB_QUERY(update)
