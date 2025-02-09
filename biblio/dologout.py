#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2017-10-31 19:57:53 -0400 (Tue, 31 Oct 2017) $


import sys
from common import *
from login import *
from SQLparsing import *

if __name__ == '__main__':

	clearCookies()

	PrintHeader("Logout")
	PrintNavbar('logout', 0, 0, 0, 0)
	print "<h2>Log Out</h2>"
	print "You are now logged out. You can continue to browse the ISFDB, but you will be unable to perform edits."
	PrintTrailer('logout', 0, 0)
