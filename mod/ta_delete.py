#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 675 $
#     Date: $Date: 2021-07-04 17:13:03 -0400 (Sun, 04 Jul 2021) $


from isfdb import *
from isfdblib import *
from common import *
from titleClass import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Title Delete - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print '<h1>SQL Updates:</h1>'
        print '<hr>'
        print '<ul>'

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('TitleDelete'):
                merge = doc.getElementsByTagName('TitleDelete')
                Record = GetElementValue(merge, 'Record')
                title = titles(db)
                title.load(Record)
                success = title.delete()
                if not success:
                        print """<h3>Error: Title couldn't be deleted because
                        it's associated with a publication. You will need to
                        hard reject this submission</h3>"""
                else:
                        submitter = GetElementValue(merge, 'Submitter')
                        markIntegrated(db, submission, Record)

        print '<p>'

        PrintPostMod(0)
