from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 20 $
#     Date: $Date: 2017-10-31 19:35:38 -0400 (Tue, 31 Oct 2017) $


import sys
import os
import string

if __name__ == '__main__':

        try:
                basename  = sys.argv[1]
                directory = sys.argv[2]
                python    = sys.argv[3]
        except:
                print("Usage: install.py <basename> <directory> <pythonloc>")
                sys.exit(0)

        fd = open(basename+ '.py')
        image = fd.read()
        fd.close()

        image = str.replace(image, '_PYTHONLOC', python)
        fd = open(directory +'/' +basename+ '.cgi', 'w+')
        fd.write(image)
        fd.close

        os.system('chmod 755 '+directory+ '/' +basename+'.cgi')
        


