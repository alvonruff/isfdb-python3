#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
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
        # 0 stands for 'Win' and 1 stands for 'All awards and nominations'. The default is 0
        win_nom = SESSION.Parameter(1, 'int', 0, (0, 1))

        cat.load()
        if not cat.award_cat_name:
                if SQLDeletedAwardCategory(cat.award_cat_id):
                        SESSION.DisplayError('This award category has been deleted. See %s for details.' % ISFDBLink('award_category_history.cgi', cat.award_cat_id, 'Edit History'))
                else:
                        SESSION.DisplayError('Award Category Record Does Not Exist')

        awardType = award_type()
        awardType.award_type_id = cat.award_cat_type_id
        awardType.load()
        if not awardType.award_type_name:
                SESSION.DisplayError('Invalid Award Category')

        PrintHeader('Award Category: %s (%s)' % (cat.award_cat_name, awardType.award_type_name))
        PrintNavbar('award_cat', cat.award_cat_id, cat.award_cat_id, 'award_category.cgi', cat.award_cat_id)

        cat.PrintAwardCatSummary(win_nom)

        PrintTrailer('award_cat', cat.award_cat_id, cat.award_cat_id)
