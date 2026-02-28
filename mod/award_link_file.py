#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2026   Ahasuerus, Klaus Elsbernd, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1260 $
#     Date: $Date: 2026-02-18 08:27:14 -0500 (Wed, 18 Feb 2026) $


import cgi
import sys
import string
from isfdb import *
from isfdblib import *
from SQLparsing import *
from common import *
from library import *

debug = 0

def DoError(text):
        print('<div id="ErrorBox">')
        print('<h3>%s</h3>' % text)
        print('</div>')
        PrintPostMod()
        sys.exit(0)

def DoSubmission(db, submission):
        title_id =0
        award_id = 0
        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('LinkAward'):
                merge = doc.getElementsByTagName('LinkAward')

                print("<ul>")

                if TagPresent(merge, 'Title'):
                        title_id = int(GetElementValue(merge, 'Title'))
                else:
                        DoError('No Title record specified')

                if TagPresent(merge, 'Award'):
                        award_id = int(GetElementValue(merge, 'Award'))
                        if award_id < 1:
                                raise
                else:
                        DoError('No valid award record specified')

                CNX = MYSQL_CONNECTOR()
                update = "delete from title_awards where award_id='%d';" % award_id
                print("<li> ", update)
                if debug == 0:
                        CNX.DB_QUERY(update)

                if int(title_id):
                        update = "insert into title_awards(title_id, award_id) values(%d, %d);" % (title_id, award_id)
                        print("<li> ", update)
                        if debug == 0:
                                CNX.DB_QUERY(update)

                submitter = GetElementValue(merge, 'Submitter')
                if debug == 0:
                        markIntegrated(db, submission, award_id)
        return (title_id, award_id)


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Link Award - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print('<h1>SQL Updates:</h1>')
        print('<hr>')

        (title_id, award_id) = DoSubmission(db, submission)

        if title_id > 0:
                print(ISFDBLinkNoName('title.cgi', title_id, 'View Title record', True))
        if award_id > 0:
                print(ISFDBLinkNoName('award_details.cgi', award_id, 'View Award record', True))

        print('<p>')

        PrintPostMod(0)
        
