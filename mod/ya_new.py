#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2026   Al von Ruff, Ahasuerus, Bill Longley and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1260 $
#     Date: $Date: 2026-02-18 08:27:14 -0500 (Wed, 18 Feb 2026) $

from isfdb import *
from isfdblib import *
from common import *
from library import *
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Make Alternate Name - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")

        submitter = ''
        try:
                xml = SQLloadXML(submission)
                doc = minidom.parseString(XMLunescape2(xml))
                if doc.getElementsByTagName('MakePseudonym'):
                        merge = doc.getElementsByTagName('MakePseudonym')
                        Record = GetElementValue(merge, 'Record')
                        submitter = GetElementValue(merge, 'Submitter')
                        if TagPresent(merge, 'Parent'):
                                parent = GetElementValue(merge, 'Parent')
                                insert = "insert into pseudonyms(author_id, pseudonym) values(%d,%d)" % (int(parent), int(Record))
                                print("<li> ", insert)
                                if debug == 0:
                                        CNX = MYSQL_CONNECTOR()
                                        CNX.DB_QUERY(insert)
                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission, Record)
        except:
                submitter = 'unknown'

        print(ISFDBLinkNoName('ea.cgi', parent, 'View Canonical Name', True))
        print(ISFDBLinkNoName('ea.cgi', Record, 'View Alternate Name', True))
        print('<p>')

        PrintPostMod(0)
