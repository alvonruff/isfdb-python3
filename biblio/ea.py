#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2026   Al von Ruff, Ahasuerus and Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1238 $
#     Date: $Date: 2026-02-06 05:59:25 -0500 (Fri, 06 Feb 2026) $


import sys
import os
import string
from SQLparsing import *
from biblio import *


if __name__ == '__main__':

        bib = Bibliography()
        bib.page_type = 'Summary'
        bib.displayBiblio()
