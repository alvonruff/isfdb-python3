#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2016   Al von Ruff, Ahasuerus and Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2017-10-31 19:57:53 -0400 (Tue, 31 Oct 2017) $


import sys
import os
import string
from SQLparsing import *
from biblio import *


if __name__ == '__main__':

	bib = Bibliography()
	bib.page_type = 'Summary'
        bib.displayBiblio()
