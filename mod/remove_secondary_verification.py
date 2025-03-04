#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2020-2025   Ahasuerus, Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


from isfdb import *
from isfdblib import *
from SQLparsing import *
from login import *


if __name__ == '__main__':

        ver_id = SESSION.Parameter(0, 'int')
        verification = SQLGetSecondaryVerificationByVerID(ver_id)
        if not verification:
                SESSION.DisplayError('Invalid Verification')
        ver_data = verification[0]
        pub_id = ver_data[VERIF_PUB_ID]
        reference_id = ver_data[VERIF_REF_ID]
        verifier_id = ver_data[VERIF_USER_ID]
        verification_time = ver_data[VERIF_TIME]
        
        pub_data = SQLGetPubById(pub_id)
        if not pub_data:
                SESSION.DisplayError('Invalid Publication')

        PrintPreMod('Remove Secondary Verification')
        PrintNavBar()

        (deleter_id, username, usertoken) = GetUserData()

        delete = 'delete from verification where verification_id = %d' % ver_id
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(delete)

        insert = """insert into deleted_secondary_verifications(pub_id, reference_id, verifier_id, verification_time, deleter_id, deletion_time)
                    values(%d, %d, %d, '%s', %d, NOW())
                    """ % (int(pub_id), int(reference_id), int(verifier_id), verification_time, int(deleter_id))
        CNX.DB_QUERY(insert)

        print('Secondary Verification removed. <br>')
        print('[%s]' % ISFDBLink('pl.cgi', pub_id, 'View This Pub'))
        print('[%s]' % ISFDBLink('edit/verify.cgi', pub_id, 'View/Add Verifications'))

        PrintPostMod(0)

