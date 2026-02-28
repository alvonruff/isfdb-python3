#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


from SQLparsing import *
from common import *
from awardClass import *


if __name__ == '__main__':

        award_id = SESSION.Parameter(0, 'int')

        award = awards(db)
        award.load(award_id)
        if not award.award_id:
                if SQLDeletedAward(award_id):
                        SESSION.DisplayError('This award has been deleted. See %s for details.' % ISFDBLink('award_history.cgi', award_id, 'Edit History'))
                else:
                        SESSION.DisplayError('Award Record Does Not Exist')

        PrintHeader('Award Details')
        PrintNavbar('award', award.award_id, award.award_type_id, 'award_details.cgi', award.award_id)

        award.PrintAwardSummary()

        print('<p>')

        PrintTrailer('award', award_id, award_id)
