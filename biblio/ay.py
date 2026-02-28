#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2026   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


import sys
import string

from isfdb import *
from SQLparsing import *
from common import *
from awardtypeClass import award_type


if __name__ == '__main__':

        award_Type = award_type()
        # If there were 2 parameters passed in, then they are "Award Type ID"+"YYYY"
        if len(SESSION.parameters) == 2:
                award_Type.award_type_id = SESSION.Parameter(0, 'int')
                award_Type.load()
                if not award_Type.award_type_name:
                        SESSION.DisplayError('Award Type Does Not Exist')
                year = SESSION.Parameter(1, 'int')
        # If there was one parameter passed in, then it must be "ZzYYYY" where 'Zz' is the award code
        elif len(SESSION.parameters) == 1:
                composite_value = SESSION.Parameter(0, 'str')
                try:
                        year = int(composite_value[2:])
                except Exception as e:
                        SESSION.DisplayError('Invalid Award Year')
                award_Type.award_type_code = composite_value[:2]
                award_Type.load()
                if not award_Type.award_type_id:
                        SESSION.DisplayError('Award Type Does Not Exist')
        else:
                SESSION.DisplayError('This Web Page requires one or two parameters')

        title = '%s %s' % (year, award_Type.award_type_name)
        PrintHeader(title)
        PrintNavbar('award', 0, award_Type.award_type_id, 'ay.cgi', 0)
        award_Type.display_awards_for_year(year)
        print('<p>')
        PrintTrailer('award', 0, 0)
