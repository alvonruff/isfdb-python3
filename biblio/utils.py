#
#     (C) COPYRIGHT 2004-2026   Al von Ruff and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1251 $
#     Date: $Date: 2026-02-10 15:00:23 -0500 (Tue, 10 Feb 2026) $


import string
from isfdb import *


#==========================================================
#                 U T I L I T I E S
#==========================================================

def DecodeArg(arg):
        arg = str.replace(arg, '_', ' ')
        arg = str.replace(arg, '\\', '')
        return arg


