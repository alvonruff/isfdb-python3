#!_PYTHONLOC
#
#     (C) COPYRIGHT 2017-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 730 $
#     Date: $Date: 2021-09-02 13:09:43 -0400 (Thu, 02 Sep 2021) $

        
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from SQLparsing import *
from login import *
from library import *
from pubClass import pubs


class verifications:
        def __init__(self):
                self.user_id = 0
                self.pub_id = 0
                self.current_status = ''
                self.new_status = ''
                self.transient = 0
        
        def insert_ver(self):
                insert = SQLInsertPrimaryVerification(self.pub_id, self.transient, self.user_id)
                print("<li> %s" % insert)

        def update_ver(self):
                if self.transient:
                        update = """update primary_verifications
                                    set ver_transient=%d,
                                    ver_time=NOW()
                                    where pub_id=%d and user_id = %d""" % (self.transient, self.pub_id, self.user_id)
                else:
                        update = """update primary_verifications
                                    set ver_transient = NULL,
                                    ver_time=NOW()
                                    where pub_id=%d and user_id = %d""" % (self.pub_id, self.user_id)
                print("<li> %s" % update)
                db.query(update)

        def delete_ver(self):
                delete = """delete from primary_verifications
                            where user_id = %d and pub_id = %d""" % (self.user_id, self.pub_id)
                print("<li> %s" % delete)
                db.query(delete)

if __name__ == '__main__':
        ##################################################################
        # Output the leading HTML stuff
        ##################################################################
        PrintPreSearch("Primary Verification Submission")
        PrintNavBar(0, 0)
        
        sys.stderr = sys.stdout
        form = IsfdbFieldStorage()

        try:
                ver = verifications()
                ver.pub_id = int(form['pubid'].value)
                ver.new_status = form['ver_status'].value
                if ver.new_status == 'Transient':
                        ver.transient = 1
        except:
                print('An error has occurred')
                PrintPostSearch(0, 0, 0, 0, 0)
                sys.exit(0)

        pub = pubs(db)
        pub.load(ver.pub_id)
        print('<h2>Primary verification of %s</h2>' % ISFDBLink('pl.cgi', pub.pub_id, pub.pub_title))
        print('<ul>')
        (user_id, username, usertoken) = GetUserData()
        ver.user_id = int(user_id)
        ver.current_status = SQLPrimaryVerStatus(ver.pub_id, ver.user_id)
        # Permanent and transient verifications
        if ver.new_status in ('Permanent', 'Transient'):
                if not ver.current_status:
                        ver.insert_ver()
                else:
                        ver.update_ver()
        # No verification
        elif ver.new_status == 'No':
                ver.delete_ver()
        else:
                print('An error has occurred')
                sys.exit(0)
        print('</ul>')

        print(ISFDBLinkNoName('pl.cgi', ver.pub_id, 'View This Pub', True))
        print(ISFDBLinkNoName('edit/editpub.cgi', ver.pub_id, 'Edit This Pub', True))
        print(ISFDBLinkNoName('edit/verify.cgi', ver.pub_id, 'View/Add Verifications', True))

        PrintPostSearch(0, 0, 0, 0, 0)
