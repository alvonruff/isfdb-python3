#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 91 $
#     Date: $Date: 2018-03-21 15:28:47 -0400 (Wed, 21 Mar 2018) $


from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *


if __name__ == '__main__':

        PrintPreMod('Recognized Domains')
        PrintNavBar()

        table = ISFDBTable()
        table.headers.extend(('Domain', 'Site Name', 'Linking Allowed', 'URL Segment', 'Link Required'))
        table.row_align = 'left'

        domains = SQLLoadRecognizedDomains()
        for domain in sorted(domains, key = lambda x: x[1]):
                if domain[DOMAIN_LINKING_ALLOWED]:
                        linking_allowed = 'Yes'
                else:
                        linking_allowed = 'No'
                if domain[DOMAIN_EXPLICIT_LINK_REQUIRED]:
                        explicit_link_required = 'Yes'
                else:
                        explicit_link_required = 'No'
                table.rows.append((ISFDBLink('edit/edit_delete_recognized_domain.cgi', domain[DOMAIN_ID], domain[DOMAIN_NAME]),
                                   domain[DOMAIN_SITE_NAME],
                                   linking_allowed,
                                   domain[DOMAIN_REQUIRED_SEGMENT],
                                   explicit_link_required))

        table.PrintTable()

        PrintPostMod(0)

