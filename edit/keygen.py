#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1003 $
#     Date: $Date: 2022-09-15 14:36:33 -0400 (Thu, 15 Sep 2022) $


import random
from isfdb import *
from isfdblib import *
from SQLparsing import *
from library import ISFDBLink

def GenerateKey(plain):
        if PYTHONVER == 'python2':
                import md5
                hash = md5.new()
                hash.update(plain)
        else:
                import hashlib
                hash = hashlib.md5()
                hash.update(plain.encode('UTF-8'))
        return hash.hexdigest()

if __name__ == '__main__':

        mode = SESSION.Parameter(0, 'str', 'view_key', ('view_key', 'new_key'))

        (userid, username, usertoken) = GetUserData()
        if userid == 0:
                SESSION.DisplayError('You must be logged in to perform key maintenance')

        PrintPreSearch('Key Maintenance')
        PrintNavBar(0, 0)

        print('A license key is only required to submit data programmatically.')
        print('It is not needed for manual editing.<p>')

        print('<b>License Key info for</b>: [%s]<br>' % WikiLink(username))
        CNX = MYSQL_CONNECTOR()
        if mode == 'view_key':
                query = "select * from license_keys where user_id=%d" % int(userid)
                CNX.DB_QUERY(query)
                if CNX.DB_NUMROWS() > 0:
                        record = CNX.DB_FETCHMANY()
                        print("<b>License Key:</b> %s" % (record[0][2]))
                else:
                        print("<b>License Key:</b> NOT SET") 
        elif mode == 'new_key':
                number = random.random()
                number = number * 1000000.0
                intnum = int(number)
                strnum = str(intnum)
                license_key = GenerateKey(strnum)
                print("<b>License Key:</b> %s" % (license_key))

                query = "select * from license_keys where user_id=%d" % int(userid)
                CNX.DB_QUERY(query)
                if CNX.DB_NUMROWS() > 0:
                        query = "update license_keys set license_key='%s' where user_id=%d" % (license_key, int(userid))
                else:
                        query = "insert into license_keys(license_key, user_id) values('%s', %d)" % (license_key, int(userid))
                CNX.DB_QUERY(query)

        print('<br><p>')
        print(ISFDBLink('edit/keygen.cgi', 'new_key', 'Generate New Key', True))
        PrintPostSearch(0, 0, 0, 0, 0, 0)
