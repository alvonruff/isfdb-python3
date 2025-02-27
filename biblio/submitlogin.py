#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley, Uzume and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 994 $
#     Date: $Date: 2022-09-08 21:18:38 -0400 (Thu, 08 Sep 2022) $
        
import cgi
import sys
from login import *
from SQLparsing import *
from common import *


def doError(message):
        PrintHeader('Login Failed')
        PrintNavbar('login', 0, 0, 0, 0)
        print('<h2>Login failed: %s</h2>' % (message))
        PrintTrailer('login', 0, 0)
        sys.exit(0)

if __name__ == '__main__':

        sys.stderr = sys.stdout
        form = IsfdbFieldStorage()

        try:
                login = form['login'].value
                password = form['password'].value
                executable = form['executable'].value
                argument = form['argument'].value
        except:
                doError('Required fields missing')

        CNX = MYSQL_CONNECTOR()
        query = "select user_id,user_password,user_name,user_token from mw_user where user_name='%s'" % (CNX.DB_ESCAPE_STRING(login))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if not record:
                doError("""User name not recognized.<br>Note that both user name and password are case
                sensitive and that the software forces the first character of the user name to uppercase.<br>
                If you don't have an ISFDB account, you can create one using the link at the top of
                this page.<br>
                Note that the ISFDB database and the ISFDB Wiki have different user authentication:
                although the userid and password are the same for both, so you can be logged in on
                one of them but logged out on the other. """)

        if LEGACY_PASSWORDS:
                ###################################################
                #$p = md5( $password);
                ###################################################
                hash = md5.new()
                hash.update(password)
                password = str(hash.hexdigest())
                ###################################################
                #return md5( "{$userid}-{$p}" );
                ###################################################
                newstr = '%s-%s' % (record[0][0], password)
                hash2 = md5.new()
                hash2.update(newstr)

                submitted_password = hash2.hexdigest()
                #real_password = str.split(str(record[0][1]), "'")[3]
                real_password = record[0][1]

                if submitted_password != real_password:
                        doError('Bad password')
        else:
                import binascii
                import base64
                try:
                    from backports.pbkdf2 import pbkdf2_hmac
                    #from hashlib import pbkdf2_hmac
                except:
                        doError('PBKDF2 Import FAILED')

                wikiPass = record[0][1]

                # Extract the various fields stored in the user_password field
                try:
                        fields = str.split(str(wikiPass), ":")
                        encryption = fields[1]
                        hashAlgo = fields[2]
                        cost   = int(fields[3])
                except:
                        doError('Login to the wiki first to re-encrypt your password')

                # Decode the salt and key fields
                base64_salt   = fields[5]
                base64_key    = fields[6]
                salt          = base64.b64decode(base64_salt)
                dbaseKey      = base64.b64decode(base64_key)

                submittedKey = pbkdf2_hmac(hashAlgo, password.encode('utf-8'), salt, cost)
                if binascii.hexlify(submittedKey) != binascii.hexlify(dbaseKey):
                        doError('Bad password')


        if executable != '0':
                if argument != '0':
                        uri = '%s?%s' % (executable, argument)
                else:
                        uri = executable
                location = '%s:/%s/%s' % (PROTOCOL, HTFAKE, uri)
        else:
                uri = None

        # If the calling module specified the name of the CGI module to pass control
        # to (and optionally an argument), then use status 303 (introduced in HTTP/1.1)
        # to redirect to that module
        if uri:
                print('Status: 303 See Other')
                print('Location: %s' % (location))
        
        # Set cookies -- this has to be done AFTER the redirect
        setCookies(record[0][0], record[0][2], record[0][3])

        PrintHeader('Logged In')
        PrintNavbar('login', 0, 0, 0, 0)
        print('<h2>Logged In</h2>')
        # Print a link to the post-login URI
        if uri:
                print('Continue to <a href="%s">%s</a>' % (location, uri))
        PrintTrailer('login', 0, 0)
