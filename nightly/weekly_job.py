#!_PYTHONLOC
#
#     (C) COPYRIGHT 2022   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 844 $
#     Date: $Date: 2022-02-15 16:06:20 -0500 (Tue, 15 Feb 2022) $

from containers_cleanup import containers_cleanup
from database_corruption import database_corruption
from database_stats import database_stats
from links_in_notes import links_in_notes
from nightly_weekly_common import nightly_weekly_common
from sfe3 import Sfe3
from slow_queries import slow_queries
from suspect_data import suspect_data
from translations_cleanup import translations_cleanup
from transliterations import transliterations
from unicode_cleanup import unicode_cleanup
from wiki import wiki


if __name__ == '__main__':
        database_stats()
        nightly_weekly_common()
        slow_queries()
        containers_cleanup()
        wiki()
        transliterations()
        translations_cleanup()
        database_corruption()
        links_in_notes()
        unicode_cleanup()
        suspect_data()
        sfe3 = Sfe3()
        sfe3.process()
