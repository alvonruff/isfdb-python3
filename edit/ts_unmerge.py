#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 972 $
#     Date: $Date: 2022-08-23 16:44:48 -0400 (Tue, 23 Aug 2022) $

        
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from titleClass import *
from SQLparsing import *
from login import *
from library import *


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Title Unmerge Submission'
        submission.cgi_script = 'tv_unmerge'
        submission.type = MOD_TITLE_UNMERGE

        form = cgi.FieldStorage()
        try:
                record = int(form['record'].value)
        except:
                submission.error("Integer title number required")
        
        titlename = SQLgetTitle(record)
        if not titlename:
                submission.error("Specified title number doesn't exist")

        if not submission.user.id:
                submission.error("", record)
        
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <TitleUnmerge>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(titlename)))
        update_string += "    <Record>%d</Record>\n" % (record)

        entry = 1
        pub_count = 0
        while entry < 2000:
                name = 'pub%d' % entry
                if form.has_key(name):
                        try:
                                val = int(form[name].value)
                        except:
                                submission.error("Invalid publication number")
                        update_string += "    <PubRecord>%d</PubRecord>\n" % (val)
                        pub_count += 1
                else:
                        pass
                entry += 1
        if not pub_count:
                submission.error("No publications selected to be unmerged")

        if form.has_key('mod_note'):
                update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(form['mod_note'].value)))

        update_string += "  </TitleUnmerge>\n"
        update_string += "</IsfdbSubmission>\n"
        
        submission.file(update_string)
