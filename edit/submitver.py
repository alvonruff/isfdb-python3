#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 730 $
#     Date: $Date: 2021-09-02 13:09:43 -0400 (Thu, 02 Sep 2021) $

        
import cgi
import sys
from isfdb import *
from isfdblib import *
from SQLparsing import *
from login import *
from library import *
from pubClass import pubs
        
def insert_verif_record(pub_id, refID, status, userid):
        insert = """insert into verification(pub_id, reference_id, user_id, ver_time, ver_status)
                    values(%d, %d, %d, NOW(), %d)""" % (pub_id, refID, int(userid), int(status))
        print("<li> %s" % insert)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(insert)

def update_verif_record(verification_id, ver_status, userid):
        update = """update verification
                    set ver_status=%d,
                    user_id=%d,
                    ver_time=NOW()
                    where verification_id=%d""" % (ver_status, int(userid), verification_id)
        print("<li> "+update)
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(update)

if __name__ == '__main__':
        ##################################################################
        # Output the leading HTML stuff
        ##################################################################
        PrintPreSearch("Secondary Verification Submission")
        PrintNavBar(0, 0)
        
        sys.stderr = sys.stdout
        form = IsfdbFieldStorage()

        if 'pubid' in form:
                pub_id = int(form['pubid'].value)
        else:
                PrintPostSearch(0, 0, 0, 0, 0)
                sys.exit(0)

        pub = pubs(db)
        pub.load(pub_id)
        print('<h2>Secondary verification of %s</h2>' % ISFDBLink('pl.cgi', pub_id, pub.pub_title))
        print('<ul>')
        (userid, username, usertoken) = GetUserData()
        secondary_verifications = SQLSecondaryVerifications(pub_id)
        for name in form:
                if name[:2] == 'xx':
                        reference_id = int(name[2:])
                        value = form[name].value
                        verifmap = {'NOTVER':0, 'VER':1, 'NA':2}
                        ver_status = verifmap.get(value, 0)
                        found = 0
                        for verification in secondary_verifications:
                                if verification[VERIF_REF_ID] == reference_id:
                                        if ver_status != int(verification[VERIF_STATUS]):
                                                update_verif_record(verification[VERIF_ID], ver_status, userid)
                                        found = 1
                                        break
                        if not found and ver_status > 0:
                                insert_verif_record(pub_id, reference_id, ver_status, userid)

        print('</ul>')

        print(ISFDBLinkNoName('pl.cgi', pub_id, 'View This Pub', True))
        print(ISFDBLinkNoName('edit/editpub.cgi', pub_id, 'Edit This Pub', True))
        print(ISFDBLinkNoName('edit/verify.cgi', pub_id, 'View/Add Verifications', True))

        PrintPostSearch(0, 0, 0, 0, 0)
