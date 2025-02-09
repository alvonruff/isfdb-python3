#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


import cgi
import sys
import os
import string
import MySQLdb
from localdefs import *
from library import RecognizedDomains

def Date_or_None(s):
        return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)


if __name__ == '__main__':

        db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
        db.select_db(DBASE)

        domains = RecognizedDomains()
        count = 1
        for domain in domains:
                domain_id = count
                domain_name = domain[0]
                site_name = domain[1]
                site_url = domain[2]
                linking_allowed = domain[3]

                required_segment = ''
                try:
                        required_segment = domain[4]
                except:
                        pass

                explicit_link_required = 0
                try:
                        explicit_link_required =domain[5]
                except:
                        pass

                insert = """insert into
                            recognized_domains(domain_id, domain_name, site_name, site_url, linking_allowed, required_segment, explicit_link_required)
                            values(%d, '%s', '%s', '%s', %d, '%s', %d)""" % (domain_id,
                                                                             db.escape_string(domain_name),
                                                                             db.escape_string(site_name),
                                                                             db.escape_string(site_url),
                                                                             linking_allowed,
                                                                             db.escape_string(required_segment),
                                                                             explicit_link_required)
                db.query(insert)
                count += 1
