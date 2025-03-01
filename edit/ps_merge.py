#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 972 $
#     Date: $Date: 2022-08-23 16:44:48 -0400 (Tue, 23 Aug 2022) $


import cgi
import sys
from isfdb import *
from isfdblib import *
from publisherClass import *
from SQLparsing import *
from login import *
from library import *

records = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MaxRecords = 0

def DoColumn(column, tag):
        if column in form:
                value = form[column].value
                index = int(value)-1
                retval = "    <%s>%d</%s>\n" % (tag, records[index], tag)
                return retval
        else:
                return ""

if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Publisher Merge Results'
        submission.cgi_script = 'pv_merge'
        submission.type = MOD_PUBLISHER_MERGE

        if not submission.user.id:
                submission.error()

        submission.user.load_moderator_flag()
        if not submission.user.moderator:
                submission.error('Only moderators can merge publishers')

        form = IsfdbFieldStorage()

        index = 1
        targetID = 1000000000
        while index:
                target = "record%d" % (index)
                if target in form:
                        records[MaxRecords] = int(form[target].value)
                        if records[MaxRecords] < targetID:
                                targetID = records[MaxRecords]
                else:
                        break
                MaxRecords += 1
                index += 1

        merge_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        merge_string += "<IsfdbSubmission>\n"
        merge_string += "  <PublisherMerge>\n"

        if MaxRecords == 0:
                submission.error('No records')

        index = 0
        while index < MaxRecords:
                if records[index] == targetID:
                        merge_string += "    <KeepId>%d</KeepId>\n" % (records[index])
                else:
                        merge_string += "    <DropId>%d</DropId>\n" % (records[index])
                index += 1

        try:
                record = SQLGetPublisher(targetID)
                publishername = record[1]
        except:
                submission.error('Invalid publisher ID')

        CNX = MYSQL_CONNECTOR()
        merge_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))
        merge_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(publishername)))


        merge_string += DoColumn('publisher_name',        'Publisher')
        merge_string += DoColumn('publisher_note',        'Note')
        merge_string += DoColumn('publisher_webpages',        'Webpages')

        merge_string += "  </PublisherMerge>\n"
        merge_string +=  "</IsfdbSubmission>\n"

        submission.file(merge_string)
