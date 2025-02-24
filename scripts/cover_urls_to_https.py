#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2022-2025   Ahasuerus, Al von Ruff
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
    query = """select pub_id, pub_frontimage from pubs where pub_frontimage like '%http:\/\/%' limit 100000000"""

    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    while record:
        pub_id = record[0][0]
        pub_frontimage = record[0][1]
        url_segments = pub_frontimage[7:]
        domain = url_segments.split('/')[0]

##        # Skip current HTTP domains
##        # HTTP domains: 'sf-encyclopedia.uk', 'www.philsp.com', 'www.mondourania.com',
##        #   'people.uncw.edu', 'sf-leihbuch.de', 'books.ofearna.us', 'www.sf-leihbuch.de', 'art.ofearna.us'
##        # Special case: ISFDB, uses PROTOCOL
##        if domain in ('sf-encyclopedia.uk',
##                      'www.philsp.com',
##                      'philsp.com',
##                      'www.mondourania.com',
##                      'www.isfdb.org',
##                      'people.uncw.edu',
##                      'sf-leihbuch.de',
##                      'books.ofearna.us',
##                      'www.sf-leihbuch.de',
##                      'art.ofearna.us'):
##            pass
##        # Inconsistent URL change to HTTPS: covers.openlibrary.org
##        elif domain == 'covers.openlibrary.org':
##            pass
##        # Invalid URLs: www.grantvillegazette.com - see for current URLs
##                          'www.grantvillegazette.com',
##      # Fantasticfiction.co.uk is moving to img1.fantasticfiction.com
##                          'img1.fantasticfiction.co.uk',
##                          'www.fantasticfiction.co.uk',
        if domain in ('bookscans.com',
                          'www.fantascienza.com',
                          'www.deboekenplank.nl',
                          'www.uraniamania.com',
                          'www.collectorshowcase.fr',
                          'howardworks.com',
                          'armchairfiction.com',
                          'ofearna.us',
                          'www.sinistercinema.com',
                          'www.armchairfiction.com',
                          'bookscans.fatcow.com',
                          'fantlab.ru',
                          'data.fantlab.ru',
                          'thetrashcollector.com',
                          'i0.wp.com',
                          'i1.wp.com',
                          'www.luminist.org',
                          'deboekenplank.nl',
                          'pulpcovers.com',
                          'www.bookscans.com'):
            domains[domain] = domains.get(domain, 0) + 1
            print(pub_id, pub_frontimage)
            new_url = 'https://%s' % url_segments
            print(new_url)
            update = """update pubs set pub_frontimage = '%s' where pub_id = %d""" % (new_url, pub_id)
            db.query(update)
        record = result.fetch_row()

    domains_list = sorted(domains.items(), key=lambda x: x[1], reverse=True)
    for domain in domains_list:
        print(domain[0], domain[1])

