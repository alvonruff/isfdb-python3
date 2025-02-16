#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 419 $
#     Date: $Date: 2019-05-15 10:54:53 -0400 (Wed, 15 May 2019) $


import sys
import string
import cgi
from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from login import *


def PrintError(message):
        print('<h2>%s</h2>' % message)
        PrintPostMod(0)
        sys.exit(0)

        
if __name__ == '__main__':
        PrintPreMod('Manage Self-Approvers - SQL Statements')
        PrintNavBar()
        
        sys.stderr = sys.stdout
        form = cgi.FieldStorage()
        
        try:
                user_name = form['user_name'].value
        except:
                PrintError('User name not specified.')

        try:
                user_id = int(SQLgetSubmitterID(user_name, 1))
                if not user_id:
                        raise
        except:
                PrintError('Specified user name does not exist. Make sure the spelling and the case are correct.')

        try:
                self_approver = int(form["self_approver"].value)
                # Check that the submitted value is allowed
                if self_approver not in (0, 1):
                        raise
        except:
                PrintError('Invalid value in the drop-down list.')

        print('<ul>')

        query = 'delete from self_approvers where user_id = %d' % user_id
        db.query(query)
        print('<li>%s' % query)
        
        if self_approver:
                query = 'insert into self_approvers(user_id) values(%d)' % user_id
                db.query(query)
                print('<li>%s' % query)

        print('</ul>')
        message = '<h3>New settings: User %s is ' % user_name
        if not self_approver:
                message += 'NOT '
        message += 'a self-approver.</h3>'
        print(message)

        PrintPostMod(0)
