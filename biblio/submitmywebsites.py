#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2009-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended serieslication of such source code.
#
#     Version: $Revision: 713 $
#     Date: $Date: 2021-08-27 10:38:44 -0400 (Fri, 27 Aug 2021) $

        
import cgi
import sys
from login import *
from SQLparsing import *
from common import *

def DoError(message):        
        PrintHeader("Preferences Update")
        PrintNavbar("preferences", 0, 0, 0, 0)
        print("<h3>%s.</h3>" % message)
        PrintTrailer('preferences', 0, 0)
        sys.exit(0)

if __name__ == '__main__':

        
        sys.stderr = sys.stdout
        form = cgi.FieldStorage()

        (user_id, username, usertoken) = GetUserData()
        if not user_id:
                DoError('You must be logged in to modify your Web site preferences')

        user_id = int(user_id)

        counter = 1
        sites = []
        choices = []
        try:
                for key in form.keys():
                        key_type = key.split('.')[0]
                        key_number = int(key.split('.')[1])
                        if key_type == 'site_id':
                                site_name = form[key].value
                                sites.append((key_number,site_name))
                        if key_type == 'site_choice':
                                choice = form[key].value
                                choices.append((key_number,choice))
        except:
                DoError('Invalid preferences submitted')

        amazon = 0
        updates = []
        for site in sites:
                site_id = site[0]
                site_name = site[1]
                status = 0
                for choice in choices:
                        if site_id == choice[0]:
                                if choice[1] == 'on':
                                        status = 1
                                break
                updates.append((site_id,status))
                if (site_name.find('Amazon') > -1) and (status == 1):
                        amazon = 1
        if amazon == 0:
                DoError('At least one Amazon store must be specified since ISFDB links to Amazon-hosted images')

        for update in updates:
                site_id = update[0]
                status = update[1]
                query = "select user_site_id from user_sites where site_id=%d and user_id=%d" % (site_id, user_id)
                db.query(query)
                result = db.store_result()

                #If this user/site combination is not already on file, create a new one
                if result.num_rows() < 1:
                        update = "insert into user_sites(site_id,user_id,user_choice) values(%d,%d,%d)" % (site_id, user_id, status)

                #If this user/site combination is already on file, retrieve the row ID
                else:
                        record = result.fetch_row()
                        user_site_id = int(record[0][0])
                        update = "update user_sites set user_choice = %d where user_site_id = %d" % (status, user_site_id)
                db.query(update)

        ISFDBLocalRedirect('mypreferences.cgi')
