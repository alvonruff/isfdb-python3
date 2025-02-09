#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2022   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1009 $
#     Date: $Date: 2022-09-17 20:44:05 -0400 (Sat, 17 Sep 2022) $

from front_page_pubs import front_page_pubs
from nightly_cleanup import nightly_cleanup
from html_cleanup import html_cleanup

def nightly_weekly_common():
        front_page_pubs()
        nightly_cleanup()
        html_cleanup()
