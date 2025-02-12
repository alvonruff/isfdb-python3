#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020-2025   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 419 $
#     Date: $Date: 2019-05-15 10:54:53 -0400 (Wed, 15 May 2019) $

from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import SQLgetTitleByTagId, SQLDeleteTagMapping
from library import ISFDBLocalRedirect
from login import User

        
if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('This option can only be accessed by ISFDB Bureaucrats')

        tagmap_id = SESSION.Parameter(0, 'int')

        try:
                title_id = SQLgetTitleByTagId(tagmap_id)[0]
        except:
                SESSION.DisplayError("Specified Tag ID doesn't exist")

        SQLDeleteTagMapping(tagmap_id)
        
        ISFDBLocalRedirect('mod/tag_breakdown.cgi?%d' % int(title_id))
