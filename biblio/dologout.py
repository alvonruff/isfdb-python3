#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2026   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


import sys
from common import *
from login import *
from SQLparsing import *

if __name__ == '__main__':

        clearCookies()

        PrintHeader("Logout")
        PrintNavbar('logout', 0, 0, 0, 0)
        print("<h2>Log Out</h2>")
        print("You are now logged out. You can continue to browse the ISFDB, but you will be unable to perform edits.")
        PrintTrailer('logout', 0, 0)
