#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus, Al von Ruff 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 696 $
#     Date: $Date: 2021-08-13 16:03:00 -0400 (Fri, 13 Aug 2021) $

from isfdb import *
from SQLparsing import *
from library import GetElementValue, ISFDBLink, XMLunescape2, TagPresent
from isfdblib import PrintPreMod, PrintNavBar, PrintPostMod, NotApprovable, markIntegrated
from xml.dom import minidom


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Add New Verification Source - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('VerificationSource')
        if not merge:
                SESSION.DisplayError('Invalid Submission', 0)

        print('<h1>SQL Updates:</h1>')
        print('<hr>')
        print('<ul>')

        reference_label = GetElementValue(merge, 'SourceLabel')
        reference_fullname = GetElementValue(merge, 'SourceName')
        reference_url = GetElementValue(merge, 'SourceURL')

        insert = """insert into reference(reference_label, reference_fullname, reference_url)
                    values('%s', '%s', '%s')""" % (db.escape_string(reference_label),
                                                   db.escape_string(reference_fullname),
                                                   db.escape_string(reference_url))
        print('<li> ', insert)
        db.query(insert)
        new_record = db.insert_id()

        markIntegrated(db, submission, new_record)

        print(ISFDBLink('edit/edit_verification_source.cgi', new_record, 'Edit This Verification Source', 1))
        print(ISFDBLink('mod/list_verification_sources.cgi', '', 'View Verification Sources', 1))

        PrintPostMod(0)
