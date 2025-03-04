#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 768 $
#     Date: $Date: 2021-10-03 18:13:32 -0400 (Sun, 03 Oct 2021) $


from isfdb import *
from isfdblib import *
from titleClass import *
from SQLparsing import *
from common import *
from library import *

debug = 0


def DoSubmission(db, submission):
        ParentRecord =0
        ChildRecord = 0
        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('LinkReview'):
                merge = doc.getElementsByTagName('LinkReview')

                print("<ul>")

                if TagPresent(merge, 'Parent'):
                        ParentRecord = int(GetElementValue(merge, 'Parent'))
                else:
                        print('<div id="ErrorBox">')
                        print("<h3>: No Parent listed</h3>")
                        print('</div>')
                        PrintPostMod()
                        sys.exit(0)

                if TagPresent(merge, 'Record'):
                        ChildRecord = int(GetElementValue(merge, 'Record'))
                else:
                        print('<div id="ErrorBox">')
                        print("<h3>: No Review record listed</h3>")
                        print('</div>')
                        PrintPostMod()
                        sys.exit(0)

                CNX = MYSQL_CONNECTOR()
                update = "delete from title_relationships where review_id='%d';" % (int(ChildRecord))
                print("<li> ", update)
                if debug == 0:
                        CNX.DB_QUERY(update)

                if int(ParentRecord):
                        update = "insert into title_relationships(title_id, review_id) values(%d, %d);" % (int(ParentRecord), int(ChildRecord))
                        print("<li> ", update)
                        if debug == 0:
                                CNX.DB_QUERY(update)

                submitter = GetElementValue(merge, 'Submitter')
                if debug == 0:
                        markIntegrated(db, submission, ChildRecord)
        return (ParentRecord, ChildRecord)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Link Review - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print('<h1>SQL Updates:</h1>')
        print('<hr>')

        (ParentRecord, ChildRecord) = DoSubmission(db, submission)

        if ParentRecord > 0:
                print(ISFDBLinkNoName('title.cgi', ParentRecord, 'View Reviewed Title', True))
        if ChildRecord > 0:
                print(ISFDBLinkNoName('title.cgi', ChildRecord, 'View Review Title', True))

        print('<p>')

        PrintPostMod(0)
        
