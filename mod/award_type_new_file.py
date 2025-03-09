#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2014-2025   Ahasuerus, Klaus Elsbernd, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 752 $
#     Date: $Date: 2021-09-17 18:33:04 -0400 (Fri, 17 Sep 2021) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from awardtypeClass import *


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Add New Award Type - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('NewAwardType')
        if not merge:
                print('<div id="ErrorBox">')
                print('<h3>Error: Bad argument</h3>')
                print('</div>')
                PrintPostMod()
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")
        subname = GetElementValue(merge, 'Submitter')
        submitter = SQLgetSubmitterID(subname)
        ShortName = GetElementValue(merge, 'ShortName')
        FullName = GetElementValue(merge, 'FullName')
        AwardedBy = GetElementValue(merge, 'AwardedBy')
        AwardedFor = GetElementValue(merge, 'AwardedFor')
        Poll = GetElementValue(merge, 'Poll')
        NonGenre = GetElementValue(merge, 'NonGenre')

        #####################################
        # Insert into the award types table
        #####################################
        CNX = MYSQL_CONNECTOR()
        insert = "insert into award_types(award_type_name, award_type_by, award_type_for, award_type_short_name, award_type_poll, award_type_non_genre) values('%s', '%s', '%s', '%s', '%s', '%s')" % (CNX.DB_ESCAPE_STRING(FullName), CNX.DB_ESCAPE_STRING(AwardedBy), CNX.DB_ESCAPE_STRING(AwardedFor), CNX.DB_ESCAPE_STRING(ShortName), CNX.DB_ESCAPE_STRING(Poll), CNX.DB_ESCAPE_STRING(NonGenre))
        print("<li> ", insert)
        CNX.DB_QUERY(insert)
        award_type_id = int(CNX.DB_INSERT_ID())

        #####################################
        # NOTE
        #####################################
        note_id = ''
        note = GetElementValue(merge, 'Note')
        if note:
                insert = "insert into notes(note_note) values('%s');" % CNX.DB_ESCAPE_STRING(note)
                print("<li> ", insert)
                CNX.DB_QUERY(insert)
                note_id = int(CNX.DB_INSERT_ID())
                update = "update award_types set award_type_note_id = %d where award_type_id=%d" % (note_id, award_type_id)
                print("<li> ", update)
                CNX.DB_QUERY(update)

        ##########################################################
        # Insert the new webpages
        ##########################################################

        value = GetElementValue(merge, 'Webpages')
        if value:
                webpages = doc.getElementsByTagName('Webpage')
                for webpage in webpages:
                        if PYTHONVER == 'python2':
                                address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                        else:
                                address = XMLunescape(webpage.firstChild.data)
                        update = "insert into webpages(award_type_id, url) values(%d, '%s')" % (award_type_id, CNX.DB_ESCAPE_STRING(address))
                        print("<li> ", update)
                        CNX.DB_QUERY(update)

        markIntegrated(db, submission, award_type_id)

        print(ISFDBLinkNoName('edit/editawardtype.cgi', award_type_id, 'Edit This Award Type', True))
        print(ISFDBLinkNoName('awardtype.cgi', award_type_id, 'View This Award Type', True))

        PrintPostMod(0)
