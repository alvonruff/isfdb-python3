#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2010-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 729 $
#     Date: $Date: 2021-09-02 12:08:46 -0400 (Thu, 02 Sep 2021) $

from isfdb import *
from common import *
from isfdblib import *
from library import *
from SQLparsing import *

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Remove Alternate Name - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print('<h1>SQL Updates:</h1>')
        print('<hr>')
        print('<ul>')

        submitter = ''
        try:
                xml = SQLloadXML(submission)
                doc = minidom.parseString(XMLunescape2(xml))
                if doc.getElementsByTagName('RemovePseud'):
                        merge = doc.getElementsByTagName('RemovePseud')
                        Record = GetElementValue(merge, 'Record')
                        submitter = GetElementValue(merge, 'Submitter')
                        if TagPresent(merge, 'Parent'):
                                parent = GetElementValue(merge, 'Parent')
                                #Retrieve the last pseudonym row id that matches this canonical/alternate pair
                                pseud_id = SQLGetPseudIdByAuthorAndPseud(parent,Record)
                                if not pseud_id:
                                        print('<div id="ErrorBox">')
                                        print('<h3>Error: This alternate name association no longer exists.</h3>')
                                        print('<h3>Please use %s to reject this submission.</h3>' % (ISFDBLink('mod/hardreject.cgi', submission, 'Hard Reject')))
                                        print('</div>')
                                        PrintPostMod()
                                        sys.exit(0)
                                insert = "delete from pseudonyms where pseudo_id = %d" % int(pseud_id)
                                print('<li> ', insert)
                                CNX = MYSQL_CONNECTOR()
                                CNX.DB_QUERY(insert)
                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission, Record)
        except:
                submitter = 'unknown'

        print(ISFDBLinkNoName('ea.cgi', parent, 'View Former Canonical Name', True))
        print(ISFDBLinkNoName('ea.cgi', Record, 'View Former Alternate Name', True))
        print('<p>')

        PrintPostMod(0)
