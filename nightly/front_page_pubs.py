#!_PYTHONLOC
#
#     (C) COPYRIGHT 2022   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 863 $
#     Date: $Date: 2022-03-08 18:35:10 -0500 (Tue, 08 Mar 2022) $

from isfdb import *
from SQLparsing import *

def front_page_pubs():
        pubs = SQLGetNextMonthPubs(10)

        delete = "delete from front_page_pubs"
        db.query(delete)
        insert = "insert into front_page_pubs (pub_id) VALUES"
        for pub in pubs:
                insert += '(%d),' % pub[PUB_PUBID]
        insert = '%s' % insert[:-1]
        db.query(insert)
        
