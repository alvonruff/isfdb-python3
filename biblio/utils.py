#
#     (C) COPYRIGHT 2004-2025   Al von Ruff and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2017-10-31 19:57:53 -0400 (Tue, 31 Oct 2017) $


import string
from isfdb import *


#==========================================================
#                 U T I L I T I E S
#==========================================================

def DecodeArg(arg):
        arg = str.replace(arg, '_', ' ')
        arg = str.replace(arg, '\\', '')
        return arg


