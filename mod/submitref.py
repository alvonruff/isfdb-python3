#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 17 $
#     Date: $Date: 2017-10-31 18:57:31 -0400 (Tue, 31 Oct 2017) $

        
import cgi
import string
import sys
import MySQLdb
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

        print 'Reference table editing is temporarily disabled.'
        PrintPostMod()


        sys.stderr = sys.stdout
        form = cgi.FieldStorage()

        print '<pre>'

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

                if form.has_key(label_str):
                        id_value = form[id_str].value
                        if form.has_key(label_str):
                                label_value = form[label_str].value
                                fields += 'reference_label'
                                values += "'%s'" % label_value
                        else:
                                label_value = 0
                        if form.has_key(fullname_str):
                                fullname_value = form[fullname_str].value
                                fields += ', reference_fullname'
                                values += ", '%s'" % fullname_value
                        else:
                                fullname_value = 0
                        if form.has_key(pub_str):
                                pub_value = form[pub_str].value
                                fields += ', pub_id'
                                values += ", '%s'" % pub_value
                        else:
                                pub_value = 0
                        if form.has_key(url_str):
                                url_value = form[url_str].value
                                fields += ', reference_url'
                                values += ", '%s'" % url_value
                        else:
                                url_value = 0

                        query = "select * from reference where reference_id='%d'" % index
                        db.query(query)
                        result = db.store_result()
                        if result.num_rows() > 0: 
                                record = result.fetch_row()
                                if record[0][1] != label_value:
                                        update = "update reference set reference_label='%s' where reference_id='%d'" % (label_value, index)
                                        print update
                                        db.query(update)
                                if record[0][2] != fullname_value:
                                        update = "update reference set reference_fullname='%s' where reference_id='%d'" % (fullname_value, index)
                                        print update
                                        db.query(update)
                                if record[0][3] != pub_value:
                                        update = "update reference set pub_id='%s' where reference_id='%d'" % (pub_value, index)
                                        print update
                                        db.query(update)
                                if record[0][4] != url_value:
                                        try:
                                                if url_value[0] != 'h':
                                                        url_value = ''
                                        except:
                                                url_value = ''
                                        update = "update reference set reference_url='%s' where reference_id='%d'" % (url_value, index)
                                        print update
                                        db.query(update)
                        else:
                                insert = "insert into reference(%s) values(%s)" % (fields, values)
                                print insert
                                db.query(insert)
                else:
                        skips += 1
                        if skips > 5:
                                break
                index += 1

        print '</pre>'

        PrintPostMod()
