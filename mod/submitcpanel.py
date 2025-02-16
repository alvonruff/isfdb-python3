#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 693 $
#     Date: $Date: 2021-08-09 17:10:16 -0400 (Mon, 09 Aug 2021) $


import cgi
from isfdb import *
from isfdblib import *
from SQLparsing import *
from library import *


if __name__ == '__main__':
        PrintPreMod('ISFDB Control Panel Submission')
        PrintNavBar()
        
        query = "select * from metadata"
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()

        oldVersion = record[0][0]
        oldDbOnline = record[0][2]
        oldEditOnline = record[0][3]

        sys.stderr = sys.stdout
        form = cgi.FieldStorage()

        print('<pre>')
        changes = 0
        if form.has_key('VERSION'):
                newVersion = XMLescape(form['VERSION'].value)
                if newVersion != oldVersion:
                        query = "update metadata set metadata_schemaversion='%s'" % db.escape_string(newVersion)
                        print(query)
                        db.query(query)
                        changes += 1

        if form.has_key('ONLINE'):
                newDbOnline = int(form['ONLINE'].value)
                if newDbOnline != oldDbOnline:
                        query = "update metadata set metadata_dbstatus=%d" % newDbOnline
                        print(query)
                        db.query(query)
                        changes += 1

        if form.has_key('EDITING'):
                newEditOnline = int(form['EDITING'].value)
                if newEditOnline != oldEditOnline:
                        query = "update metadata set metadata_editstatus=%d" % newEditOnline
                        print(query)
                        db.query(query)
                        changes += 1

        print('%d changes made.' % changes)
        print('</pre>')

        PrintPostMod(0)
