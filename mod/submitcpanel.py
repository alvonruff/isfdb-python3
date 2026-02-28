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
from isfdb import *
from isfdblib import *
from SQLparsing import *
from library import *


if __name__ == '__main__':
        PrintPreMod('ISFDB Control Panel Submission')
        PrintNavBar()
        
        query = "select * from metadata"
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()

        oldVersion = record[0][0]
        oldDbOnline = record[0][2]
        oldEditOnline = record[0][3]

        sys.stderr = sys.stdout
        form = IsfdbFieldStorage()

        print('<pre>')
        changes = 0
        if 'VERSION' in form:
                newVersion = XMLescape(form['VERSION'].value)
                if newVersion != oldVersion:
                        query = "update metadata set metadata_schemaversion='%s'" % CNX.DB_ESCAPE_STRING(newVersion)
                        print(query)
                        CNX.DB_QUERY(query)
                        changes += 1

        if 'ONLINE' in form:
                newDbOnline = int(form['ONLINE'].value)
                if newDbOnline != oldDbOnline:
                        query = "update metadata set metadata_dbstatus=%d" % newDbOnline
                        print(query)
                        CNX.DB_QUERY(query)
                        changes += 1

        if 'EDITING' in form:
                newEditOnline = int(form['EDITING'].value)
                if newEditOnline != oldEditOnline:
                        query = "update metadata set metadata_editstatus=%d" % newEditOnline
                        print(query)
                        CNX.DB_QUERY(query)
                        changes += 1

        print('%d changes made.' % changes)
        print('</pre>')

        PrintPostMod(0)
