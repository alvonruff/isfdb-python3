#!/usr/bin/python3
#
#     (C) COPYRIGHT 2005-2006   Al von Ruff
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
                version  = sys.argv[1]
        except:
                print("Usage: setver.py <version>")
                sys.exit(0)

        fd = open("localdefs.py")
        image = fd.read()
        fd.close()

        if version == '2':
                image = str.replace(image, 'python3', 'python2')
        elif version == '3':
                image = str.replace(image, 'python2', 'python3')
        else:
                sys.exit(1)

        fd = open('localdefs.py', 'w+')
        fd.write(image)
        fd.close

        


