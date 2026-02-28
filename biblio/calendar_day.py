#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1258 $
#     Date: $Date: 2026-02-13 16:16:41 -0500 (Fri, 13 Feb 2026) $


import string
import sys
from isfdb import *
from common import *
from login import *
from library import *
from SQLparsing import *
from calendarClass import CalendarDay
        
if __name__ == '__main__':

        one_day = CalendarDay()
        one_day.display()
