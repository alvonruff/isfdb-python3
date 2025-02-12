#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 676 $
#     Date: $Date: 2021-07-05 12:14:45 -0400 (Mon, 05 Jul 2021) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from recognizeddomainClass import RecognizedDomain


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Recognized Domain Delete - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('DeleteRecognizedDomain')
        if not merge:
                print('<div id="ErrorBox">')
                print('<h3>Error: Bad argument</h3>')
                print('</div>')
                PrintPostMod()
                sys.exit(0)

        print('<h1>SQL Updates:</h1>')
        print('<hr>')
        print('<ul>')

        domain_id = int(GetElementValue(merge, 'Record'))

        delete = "delete from recognized_domains where domain_id = %d" % domain_id
        print('<li> %s' % delete)
        db.query(delete)

        markIntegrated(db, submission, domain_id)

        PrintPostMod(0)
