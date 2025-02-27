#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 416 $
#     Date: $Date: 2019-05-13 16:46:36 -0400 (Mon, 13 May 2019) $


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
