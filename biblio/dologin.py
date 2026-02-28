#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2026   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1238 $
#     Date: $Date: 2026-02-06 05:59:25 -0500 (Fri, 06 Feb 2026) $


import sys
from common import *
from login import *
from SQLparsing import *

if __name__ == '__main__':

        PrintHeader('Login')
        PrintNavbar('login', 0, 0, 0, 0)
        executable = SESSION.Parameter(0, 'str')
        argument = SESSION.Parameter(1, 'str')
        LoginPage(executable, argument)
        PrintTrailer('login', 0, 0)
