from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2026   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1271 $
#     Date: $Date: 2026-02-27 16:20:27 -0500 (Fri, 27 Feb 2026) $


import sys
import os

if __name__ == '__main__':

        try:
                basename  = sys.argv[1]
                directory = sys.argv[2]
                python    = sys.argv[3]
        except IndexError:
                print("Usage: install.py <basename> <directory> <pythonloc>")
                sys.exit(0)

        fd = open(basename+ '.py')
        image = fd.read()
        fd.close()

        image = str.replace(image, '_PYTHONLOC', python)
        fd = open(directory +'/' +basename+ '.cgi', 'w+')
        fd.write(image)
        fd.close()

        os.chmod(directory +'/' +basename+ '.cgi', 0o755)
