#
#     (C) COPYRIGHT 2013-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


import sys
import os
import string

if __name__ == '__main__':

        try:
                basename  = sys.argv[1]
                directory = sys.argv[2]
                python = sys.argv[3]
        except:
                print("Usage: install_nightly.py <basename> <directory> <pythonloc>")
                sys.exit(0)

        fd = open(basename+ '.py')
        image = fd.read()
        fd.close()

        image = str.replace(image, '_PYTHONLOC', python)
        fd = open(directory +'/' +basename+ '.py', 'w+')
        fd.write(image)
        fd.close

        os.system('chmod 755 '+directory+ '/' +basename+'.py')
        


