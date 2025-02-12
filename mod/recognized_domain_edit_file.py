#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023-2025   Ahasuerus 
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


submission    = 0
submitter     = 0
reviewer      = 0

def UpdateYesNoColumn(doc, tag, column, record_id):
        if TagPresent(doc, tag):
                value = GetElementValue(doc, tag)
                if value == 'Yes':
                        update = "update recognized_domains set %s = 1 where domain_id = %d" % (column, record_id)
                else:
                        update = "update recognized_domains set %s = 0 where domain_id = %d" % (column, record_id)
                print('<li> %s' % update)
                db.query(update)

def UpdateColumn(doc, tag, column, record_id):
        if TagPresent(doc, tag):
                value = GetElementValue(doc, tag)
                if value:
                        update = "update recognized_domains set %s = '%s' where domain_id = %d" % (column, db.escape_string(value), record_id)
                else:
                        update = "update recognized_domains set %s = NULL where domain_id = %d" % (column, record_id)
                print('<li> %s' % update)
                db.query(update)

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Recognized Domain Update - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print('<h1>SQL Updates:</h1>')
        print('<hr>')
        print('<ul>')

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('EditRecognizedDomain'):
                merge = doc.getElementsByTagName('EditRecognizedDomain')
                Record = int(GetElementValue(merge, 'Record'))
                subname = GetElementValue(merge, 'Submitter')
                submitter = SQLgetSubmitterID(subname)

                UpdateColumn(merge, 'DomainName', 'domain_name',  Record)
                UpdateColumn(merge, 'SiteName',  'site_name',  Record)
                UpdateColumn(merge, 'SiteURL',   'site_url',  Record)
                UpdateYesNoColumn(merge, 'LinkingAllowed', 'linking_allowed',  Record)
                UpdateColumn(merge, 'RequiredSegment', 'required_segment',  Record)
                UpdateYesNoColumn(merge, 'ExplicitLinkRequired', 'explicit_link_required',  Record)

                markIntegrated(db, submission, Record)

        print ISFDBLink('edit/edit_delete_recognized_domain.cgi', Record, 'Edit This Recognized Domain', 1)
        print ISFDBLink('mod/list_recognized_domains.cgi', '', 'View Recognized Domains', 1)

        PrintPostMod(0)
