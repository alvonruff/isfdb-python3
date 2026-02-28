#!/usr/bin/python
#
#     (C) COPYRIGHT 2009-2017   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1244 $
#     Date: $Date: 2026-02-08 08:15:28 -0500 (Sun, 08 Feb 2026) $

import os
import sys

list = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
lastBanner = 11

if __name__ == '__main__':

	os.chdir('/var/www/html/banners')

	# Load the current banner number
	fd = open('CurrentBanner')
	current = fd.readline()

	# Calculate the next banner number
	next = int(current)+1;
	#if next in list:
	if next <= lastBanner:
		pass
	else:
		next = int(list[0])

	# Copy the banner
	nextFile = 'IsfdbBanner'+str(next)+'.jpg'
	cmd = 'cp %s ../IsfdbBanner.jpg' % nextFile
	os.system(cmd)

	# Update CurrentBanner file
	fd.close();
	fd = open('CurrentBanner', 'r+')
	fd.write(str(next))
	fd.close()

	sys.exit(0)
