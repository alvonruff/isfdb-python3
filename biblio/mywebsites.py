#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2019   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 469 $
#     Date: $Date: 2019-10-24 14:34:11 -0400 (Thu, 24 Oct 2019) $


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from login import *
from SQLparsing import *

if __name__ == '__main__':

	PrintHeader("My Web Sites")
	PrintNavbar('mywebsites', 0, 0, 'mywebsites.cgi', 0)

	(myID, username, usertoken) = GetUserData()
	myID = int(myID)
	if not myID:
                print 'You must be logged in to modify your list of preferred Web sites'
                sys.exit(0)
        	PrintTrailer('mywebsites', 0, 0)

	#Get a list of currently defined Web sites
        query = "select site_id, site_name from websites order by site_name"
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	websites = []
	while row:
		websites.append(row[0])
		row = result.fetch_row()

	# Get the currently defined site preferences for the logged-in user
	query = "select site_id,user_choice from user_sites where user_id='%d'" % (myID)
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	user_sites = []
	while row:
		user_sites.append(row[0])
		row = result.fetch_row()

        print '<h3>Select Web Sites to link Publications to. At least one Amazon site needs to be selected since ISFDB links to Amazon-hosted images.</h3>'
        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/submitmywebsites.cgi">'
        print '<ul>'
        for website in websites:
                checked = 'checked'
                for user_site in user_sites:
                        if user_site[0] == website[0]:
                                if user_site[1] == 0:
                                        checked = ''
                                        break
        	print '<li><input type="checkbox" name="site_choice.%s" value="on" %s>%s ' % (website[0], checked, website[1])
        	print '<input name="site_id.%d" value="%s" type="HIDDEN"></li>' % (website[0], website[1])
        print '</ul>'
        print '<p>'
	print '<input type="SUBMIT" value="Update List of Web Sites">'
        print '</form>'

	PrintTrailer('mywebsites', 0, 0)

