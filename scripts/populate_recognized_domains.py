#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2023-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


from SQLparsing import *
from isfdb import *

debug = 0

if __name__ == '__main__':

        CNX = MYSQL_CONNECTOR()

        domains = SQLLoadRecognizedDomains()
        count = 1
        for domain in domains:
                domain_id       = domain[DOMAIN_ID]
                domain_name     = domain[DOMAIN_NAME]
                site_name       = domain[DOMAIN_SITE_NAME]
                site_url        = domain[DOMAIN_SITE_URL]
                linking_allowed = domain[DOMAIN_LINKING_ALLOWED]

                required_segment = ''
                try:
                        required_segment = domain[DOMAIN_REQUIRED_SEGMENT]
                except:
                        pass

                explicit_link_required = 0
                try:
                        explicit_link_required =domain[DOMAIN_EXPLICIT_LINK_REQUIRED]
                except:
                        pass

                insert = """insert into
                            recognized_domains(domain_id, domain_name, site_name, site_url, linking_allowed, required_segment, explicit_link_required)
                            values(%d, '%s', '%s', '%s', %d, '%s', %d)""" % (domain_id,
                                                                             CNX.DB_ESCAPE_STRING(domain_name),
                                                                             CNX.DB_ESCAPE_STRING(site_name),
                                                                             CNX.DB_ESCAPE_STRING(site_url),
                                                                             linking_allowed,
                                                                             CNX.DB_ESCAPE_STRING(required_segment),
                                                                             explicit_link_required)
                if debug == 0:
                        CNX.DB_QUERY(insert)
                else:
                        print(insert)
                count += 1
