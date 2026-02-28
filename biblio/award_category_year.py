#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1238 $
#     Date: $Date: 2026-02-06 05:59:25 -0500 (Fri, 06 Feb 2026) $

from SQLparsing import *
from common import *
from awardcatClass import *
from awardtypeClass import *


if __name__ == '__main__':

        cat = award_cat()
        cat.award_cat_id = SESSION.Parameter(0, 'int')
        cat.load()
        if not cat.award_cat_name:
                SESSION.DisplayError('Award Category Record Does Not Exist')
        awardType = award_type()
        awardType.award_type_id = cat.award_cat_type_id
        awardType.load()
        if not awardType.award_type_name:
                SESSION.DisplayError('Award Category Record Does Not Exist')
        year = SESSION.Parameter(1, 'int')

        PrintHeader('Award Category: %d %s (%s)' % (year, cat.award_cat_name, awardType.award_type_name))
        PrintNavbar('award_cat', cat.award_cat_id, cat.award_cat_id, 'award_category.cgi', cat.award_cat_id)

        cat.PrintAwardCatYear(year)

        PrintTrailer('award_category_year', cat.award_cat_id, cat.award_cat_id)
