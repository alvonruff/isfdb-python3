#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2026   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1259 $
#     Date: $Date: 2026-02-15 16:59:31 -0500 (Sun, 15 Feb 2026) $


import cgi
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

        form = IsfdbFieldStorage()
        try:
                record = int(form['record'].value)
        except:
                submission.error("Integer title number required")

        titlename = SQLgetTitle(record)
        if not titlename:
                submission.error("Specified title number doesn't exist")

        if not submission.user.id:
                submission.error("", record)

        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <TitleUnmerge>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(titlename)))
        update_string += "    <Record>%d</Record>\n" % (record)

        entry = 1
        pub_count = 0
        while entry < 2000:
                name = 'pub%d' % entry
                if name in form:
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

        if 'mod_note' in form:
                update_string += "    <ModNote>%s</ModNote>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(form['mod_note'].value)))

        update_string += "  </TitleUnmerge>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
