#!_PYTHONLOC
#
#     (C) COPYRIGHT 2022   Ahasuerus 
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

	PrintPreMod('Add ISFDB Template - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

	xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('NewTemplate')
        if not merge:
                SESSION.DisplayError('Invalid Submission', 0)

	print '<h1>SQL Updates:</h1>'
	print '<hr>'
	print '<ul>'

        template_name = GetElementValue(merge, 'TemplateName')
        template_display = GetElementValue(merge, 'TemplateDisplayedName')
        template_type = GetElementValue(merge, 'TemplateType')
        template_url = GetElementValue(merge, 'TemplateURL')
        template_mouseover = GetElementValue(merge, 'TemplateMouseoverHelp')

        insert = """insert into
                    templates(template_name, template_display, template_type, template_url, template_mouseover)
                    values('%s', '%s', '%s', '%s', '%s')""" % (db.escape_string(template_name),
                                                               db.escape_string(template_display),
                                                               db.escape_string(template_type),
                                                               db.escape_string(template_url),
                                                               db.escape_string(template_mouseover))
        print '<li> ', insert
        db.query(insert)
        new_record = db.insert_id()

        markIntegrated(db, submission, new_record)

	PrintPostMod(0)
