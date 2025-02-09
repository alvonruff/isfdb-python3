#!_PYTHONLOC
#
#     (C) COPYRIGHT 2018-2021   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 669 $
#     Date: $Date: 2021-06-29 15:17:13 -0400 (Tue, 29 Jun 2021) $

from isfdb import *
from SQLparsing import *
from pub_output import pubOutput


if __name__ == '__main__':

	print 'Content-type: text/html\n'

        ext_id_name = SESSION.Parameter(0, 'str')
        ext_id_value = SESSION.Parameter(1, 'str')
	if not ext_id_name or not ext_id_value:
		print """getpub_by_ID.cgi: Bad query.
                        The first parameter should be the External ID type name
                        (see Advanced Publication Search by External Identifier for a list.)
                        The second parameter should be the External ID value."""
		sys.exit(1)

        ext_id_types = SQLLoadIdentifierTypes()
        ext_id_type = 0
        for ext_type_number in ext_id_types:
                ext_type_name = ext_id_types[ext_type_number][0]
                if ext_type_name == ext_id_name:
                        ext_id_type = ext_type_number
                        break
        if not ext_id_type:
		print "getpub_by_ID.cgi: Non-existent External ID Type"
		sys.exit(1)
                
        pub_bodies = SQLFindPubByExternalID(ext_id_type, ext_id_value)
        pubOutput(pub_bodies)
