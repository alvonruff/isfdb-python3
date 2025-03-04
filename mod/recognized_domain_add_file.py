#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023-2025   Ahasuerus, Al von Ruff
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

        PrintPreMod('Add New Recognized Domain - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('AddRecognizedDomain')
        if not merge:
                SESSION.DisplayError('Invalid Submission', 0)

        print('<h1>SQL Updates:</h1>')
        print('<hr>')
        print('<ul>')

        domain_name = GetElementValue(merge, 'DomainName')
        site_name = GetElementValue(merge, 'SiteName')
        site_url = GetElementValue(merge, 'SiteURL')
        if GetElementValue(merge, 'LinkingAllowed') == 'Yes':
                linking_allowed = 1
        else:
                linking_allowed = 0
        required_segment = GetElementValue(merge, 'RequiredSegment')
        if GetElementValue(merge, 'ExplicitLinkRequired') == 'Yes':
                explicit_link_required = 1
        else:
                explicit_link_required = 0

        CNX = MYSQL_CONNECTOR()
        insert = """insert into recognized_domains(domain_name, site_name, site_url, linking_allowed, required_segment, explicit_link_required)
                    values('%s', '%s', '%s', %d, '%s', %d)""" % (CNX.DB_ESCAPE_STRING(domain_name),
                                                                CNX.DB_ESCAPE_STRING(site_name),
                                                                CNX.DB_ESCAPE_STRING(site_url),
                                                                linking_allowed,
                                                                CNX.DB_ESCAPE_STRING(required_segment),
                                                                explicit_link_required)
        print('<li> %s' % insert)
        CNX.DB_QUERY(insert)
        new_record = CNX.DB_INSERT_ID()

        markIntegrated(db, submission, new_record)

        print(ISFDBLink('edit/edit_delete_recognized_domain.cgi', new_record, 'Edit This Recognized Domain', 1))
        print(ISFDBLink('mod/list_recognized_domains.cgi', '', 'View Recognized Domains', 1))

        PrintPostMod(0)
