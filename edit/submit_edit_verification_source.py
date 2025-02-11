#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 18 $
#     Date: $Date: 2017-10-31 19:18:05 -0400 (Tue, 31 Oct 2017) $

        
from isfdb import *
from isfdblib import Submission
from library import XMLescape
from login import User
from verificationsourceClass import VerificationSource
from SQLparsing import *


if __name__ == '__main__':

        user = User()
        user.load()
        user.load_bureaucrat_flag()
        if not user.bureaucrat:
                SESSION.DisplayError('The ability to edit verification sources is limited to ISFDB Bureaucrats')

        submission = Submission()
        submission.header = 'Edit Verification Source Submission'
        submission.cgi_script = 'edit_verification_source'
        submission.type = MOD_VER_SOURCE_EDIT

        new = VerificationSource()
        new.cgi2obj()
        if new.error:
                submission.error(new.error)
        current = VerificationSource()
        current.load(new.id)
        if current.error:
                submission.error(new.error)

        update_string =  '<?xml version="1.0" encoding="%s" ?>\n' % UNICODE
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <VerificationSource>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % db.escape_string(XMLescape(submission.user.name))
        update_string += "    <Subject>%s</Subject>\n" % db.escape_string(new.name)
        update_string += "    <Record>%d</Record>\n" % int(new.id)
        (changes, update) = submission.CheckField(new.used_label, current.used_label, new.label, current.label, 'SourceLabel', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_name, current.used_name, new.name, current.name, 'SourceName', 0)
        if changes:
                update_string += update
        (changes, update) = submission.CheckField(new.used_url, current.used_url, new.url, current.url, 'SourceURL', 0)
        if changes:
                update_string += update
        update_string += "  </VerificationSource>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
