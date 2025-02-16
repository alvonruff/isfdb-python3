#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 778 $
#     Date: $Date: 2021-10-11 22:42:01 -0400 (Mon, 11 Oct 2021) $


from isfdb import *
from isfdblib import *
from common import *
from pubClass import *
from titleClass import *
from SQLparsing import *
from library import *

debug = 0

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Remove Titles from Publication - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")

        submitter = ''
        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('TitleRemove'):
                merge = doc.getElementsByTagName('TitleRemove')
                Record = GetElementValue(merge, 'Record')
                pub_id = int(Record)
                submitter = GetElementValue(merge, 'Submitter')
                titles = SQLloadTitlesXBT(Record)

                if doc.getElementsByTagName('CoverRecord'):
                        children = doc.getElementsByTagName('CoverRecord')
                        if len(children):
                                for child in children:
                                        record = int(child.firstChild.data)
                                        query = "delete from pub_content where pubc_id = %d and pub_id = %d" % (record, pub_id)
                                        print("<li> ", query)
                                        if debug == 0:
                                                db.query(query)

                if doc.getElementsByTagName('TitleRecord'):
                        children = doc.getElementsByTagName('TitleRecord')
                        if len(children):
                                for child in children:
                                        record = int(child.firstChild.data)
                                        query = "delete from pub_content where pubc_id = '%d' and pub_id = '%d'" % (record, pub_id)
                                        print("<li> ", query)
                                        if debug == 0:
                                                db.query(query)

                if doc.getElementsByTagName('ReviewRecord'):
                        children = doc.getElementsByTagName('ReviewRecord')
                        if len(children):
                                for child in children:
                                        record = int(child.firstChild.data)
                                        
                                        query = "delete from pub_content where pubc_id = '%d' and pub_id = '%d'" % (record, pub_id)
                                        print("<li> ", query)
                                        if debug == 0:
                                                db.query(query)
                                        
                if doc.getElementsByTagName('InterviewRecord'):
                        children = doc.getElementsByTagName('InterviewRecord')
                        if len(children):
                                for child in children:
                                        record = int(child.firstChild.data)
                                        query = "delete from pub_content where pubc_id = '%d' and pub_id = '%d'" % (record, pub_id)
                                        print("<li> ", query)
                                        if debug == 0:
                                                db.query(query)

        if debug == 0:
                markIntegrated(db, submission, pub_id)

        print(ISFDBLinkNoName('edit/editpub.cgi', Record, 'Edit This Pub', True))
        print(ISFDBLinkNoName('pl.cgi', Record, 'View This Pub', True))

        PrintPostMod(0)
