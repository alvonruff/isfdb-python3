#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2026   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1260 $
#     Date: $Date: 2026-02-18 08:27:14 -0500 (Wed, 18 Feb 2026) $

        
import cgi
import string
import sys
from isfdb import *
from isfdblib import *
from SQLparsing import *
from library import *
        
        
if __name__ == '__main__':
        ##################################################################
        # Output the leading HTML stuff
        ##################################################################
        PrintPreMod("ISFDB Reference Submission")
        PrintNavBar()

        print('Reference table editing is temporarily disabled.')
        PrintPostMod()


        sys.stderr = sys.stdout
        form = IsfdbFieldStorage()

        print('<pre>')

        index = 0
        skips = 0
        while 1:
                id_str = "ref_id%d" % index
                label_str = "ref_label%d" % index
                fullname_str = "ref_fullname%d" % index
                pub_str = "ref_pub%d" % index
                url_str = "ref_url%d" % index
                fields = ''
                values = ''

                if label_str in form:
                        id_value = form[id_str].value
                        if label_str in form:
                                label_value = form[label_str].value
                                fields += 'reference_label'
                                values += "'%s'" % label_value
                        else:
                                label_value = 0
                        if fullname_str in form:
                                fullname_value = form[fullname_str].value
                                fields += ', reference_fullname'
                                values += ", '%s'" % fullname_value
                        else:
                                fullname_value = 0
                        if pub_str in form:
                                pub_value = form[pub_str].value
                                fields += ', pub_id'
                                values += ", '%s'" % pub_value
                        else:
                                pub_value = 0
                        if url_str in form:
                                url_value = form[url_str].value
                                fields += ', reference_url'
                                values += ", '%s'" % url_value
                        else:
                                url_value = 0

                        query = "select * from reference where reference_id='%d'" % index
                        CNX = MYSQL_CONNECTOR()
                        CNX.DB_QUERY(query)
                        if CNX.DB_NUMROWS() > 0: 
                                record = CNX.DB_FETCHONE()
                                if record[0][1] != label_value:
                                        update = "update reference set reference_label='%s' where reference_id='%d'" % (label_value, index)
                                        print(update)
                                        CNX.DB_QUERY(update)
                                if record[0][2] != fullname_value:
                                        update = "update reference set reference_fullname='%s' where reference_id='%d'" % (fullname_value, index)
                                        print(update)
                                        CNX.DB_QUERY(update)
                                if record[0][3] != pub_value:
                                        update = "update reference set pub_id='%s' where reference_id='%d'" % (pub_value, index)
                                        print(update)
                                        CNX.DB_QUERY(update)
                                if record[0][4] != url_value:
                                        try:
                                                if url_value[0] != 'h':
                                                        url_value = ''
                                        except:
                                                url_value = ''
                                        update = "update reference set reference_url='%s' where reference_id='%d'" % (url_value, index)
                                        print(update)
                                        CNX.DB_QUERY(update)
                        else:
                                insert = "insert into reference(%s) values(%s)" % (fields, values)
                                print(insert)
                                CNX.DB_QUERY(insert)
                else:
                        skips += 1
                        if skips > 5:
                                break
                index += 1

        print('</pre>')

        PrintPostMod()
