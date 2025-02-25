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
import MySQLdb
from isfdb import *
from isfdblib import *
from library import *
from publisherClass import *
from SQLparsing import *


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Publisher Change Submission'
        submission.cgi_script = 'editpublisher'
        submission.type = MOD_PUBLISHER_UPDATE

        new = publishers(db)
        new.cgi2obj()
        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error('', new.publisher_id)
        
        old = publishers(db)
        old.load(int(new.publisher_id))
        
        changes = 0
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <PublisherUpdate>\n"
        update_string += "    <Record>%d</Record>\n" % (int(new.publisher_id))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(old.publisher_name)))
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        
        (changes, update) = submission.CheckField(new.used_name, old.used_name, new.publisher_name, old.publisher_name, 'Name', 0)
        if changes:
                update_string += update

        (changes, update) = submission.CheckField(new.used_trans_names, old.used_trans_names,
                                                  new.publisher_trans_names, old.publisher_trans_names, 'PublisherTransName', 1)
        if changes:
                update_string += update

        (changes, update) = submission.CheckField(new.used_note, old.used_note, new.publisher_note, old.publisher_note, 'Note', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_webpages, old.used_webpages, new.publisher_webpages, old.publisher_webpages, 'Webpage', 1)
        if changes:
                update_string += update

        if 'mod_note' in new.form:
                update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))
                
        update_string += "  </PublisherUpdate>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
