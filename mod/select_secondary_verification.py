#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020-2025   Ahasuerus and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *


if __name__ == '__main__':

        pub_id = SESSION.Parameter(0, 'int')
        pub_data = SQLGetPubById(pub_id)
        if not pub_data:
                SESSION.DisplayError('Invalid Publication')

        PrintPreMod('Select Secondary Verification to Remove')
        PrintNavBar()

        print 'Removing a secondary verification for %s' % ISFDBLink('pl.cgi', pub_id, pub_data[PUB_TITLE])

        # Retrieve secondary verifications for the current publication
        secondary_verifications = SQLSecondaryVerifications(pub_id)
        # Retrieve the reference/source list for secondary verifications
        references = SQLGetRefDetails()

        print '<h2>Secondary Verifications</h2>'
        print '<table>'
        print '<tr>'
        print '<th>Reference</th>'
        print '<th>Verifier</th>'
        print '<th>Remove</th>'
        print '</tr>'

        for reference in references:
                ref_id = reference[REFERENCE_ID]
                print '<tr class="generic_table_header">'
                if not reference[REFERENCE_URL]:
                        print '<td class="label">%s</td>' % (reference[REFERENCE_LABEL])
                else:
                        print '<td class="label"><a href="%s">%s</a></td>' % (reference[REFERENCE_URL], reference[REFERENCE_LABEL])

                ver_status = 0
                ver_id = 0
                for verification in secondary_verifications:
                        if verification[VERIF_REF_ID] == ref_id:
                                ver_status = verification[VERIF_STATUS]
                                ver_id = verification[VERIF_ID]
                                break

                if ver_status == 1:
                        # Retrieve the name of the user who verified this pub/source combination
                        verifier_name = SQLgetUserName(verification[VERIF_USER_ID])
                        print '<td>%s</td>' % WikiLink(verifier_name)
                        print '<td>%s</td>' % ISFDBLink('mod/remove_secondary_verification.cgi', ver_id, 'Remove Verification')
                else:
                        print '<td>&nbsp;</td>'
                        print '<td>&nbsp;</td>'
                print '</tr>'

        print '</table>'
        print '<p>'

        PrintPostMod(0)

