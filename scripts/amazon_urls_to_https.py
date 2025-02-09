#!_PYTHONLOC
#
#     (C) COPYRIGHT 2022   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $
 
import MySQLdb
from localdefs import *

def Date_or_None(s):
    return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)

if __name__ == "__main__":

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    domains = {}
    query = """select pub_id, pub_frontimage from pubs where pub_frontimage like '%http:\/\/%'"""

    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    while record:
        pub_id = record[0][0]
        pub_frontimage = record[0][1]
        url_segments = pub_frontimage[7:]
        domain = url_segments.split('/')[0]

        if domain in ('ecx.images-amazon.com',
                      'images.amazon.com',
                      'g-ecx.images-amazon.com',
                      'images-eu.amazon.com',
                      'ec1.images-amazon.com',
                      'g-ec2.images-amazon.com',
                      'img.amazon.ca',
                      'ec5.images-amazon.com',
                      'ec2.images-amazon.com',
                      'g-ec5.images-amazon.com'):
            domains[domain] = domains.get(domain, 0) + 1
            new_url = 'https://m.media-amazon.com/%s' % '/'.join(url_segments.split('/')[1:])
##            print pub_id, pub_frontimage
##            print new_url

            update = """update pubs set pub_frontimage = '%s' where pub_id = %d""" % (db.escape_string(new_url), pub_id)
            db.query(update)
        record = result.fetch_row()

    domains_list = sorted(domains.items(), key=lambda x: x[1], reverse=True)
    for domain in domains_list:
        print domain[0], domain[1]

