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
    query = """select webpage_id, url from webpages where url like 'http:\/\/%'"""

    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    while record:
        webpage_id = record[0][0]
        url = record[0][1]
        url_segments = url[7:]
        domain = url_segments.split('/')[0]
        if domain not in ('en.wikipedia.org',
                        'www.sf-encyclopedia.com',
                        'www.goodreads.com',
                        'www.imdb.com',
                        'sf-encyclopedia.com',
                        'librivox.org',
                        'www.drabblecast.org',
                        'catalogue.bnf.fr',
                        'www.austlit.edu.au',
                        'pseudopod.org',
                        'escapepod.org',
                        'www.twitter.com',
                        'podcastle.org',
                        'www.nature.com',
                        'bibliowiki.com.pt',
                        'archive.org',
                        'www.tor.com',
                        'www.perrypedia.proc.org',
                        'd-nb.info',
                        'www.castofwonders.org',
                        'fancyclopedia.org',
                        'www.facebook.com',
                        'dailysciencefiction.com',
                        'news.ansible.uk',
                        'www.librarything.com',
                        'www.findagrave.com',
                        'talestoterrify.com',
                        'www.bdfi.net',
                        'de.wikipedia.org',
                        'catalog.hathitrust.org',
                        'twitter.com',
                        'tellersofweirdtales.blogspot.com',
                        'dunesteef.com',
                        'instagram.com',
                        'fr.wikipedia.org',
                        'nl.wikipedia.org',
                        'ja.wikipedia.org',
                        'pl.wikipedia.org',
                        'www.pulpartists.com',
                        'www.lightspeedmagazine.com',
                        'www.locusmag.com',
                        'www.nytimes.com',
                        'zinewiki.com',
                        'www.worldcat.org',
                        'www.fantascienza.com',
                        'fantlab.ru',
                        'theovercast.libsyn.com',
                        'es.wikipedia.org',
                        'www.encyclopedia.com',
                        'www.michaelwhelan.com',
                        'www.amazon.com',
                        'www.bigecho.org',
                        'clarkesworldmagazine.com',
                        'www.tercerafundacion.net',
                        'www.pinterest.com',
                        'www.alisoneldred.com',
                        'www.legacy.com',
                        'biography.jrank.org',
                        'lccn.loc.gov',
                        'file770.com',
                        'www.borisjulie.com',
                        'www.nightmare-magazine.com',
                        'www.sfsite.com',
                        'worldcat.org',
                        'bizarrocast.blogspot.com',
                        'www.zauberspiegel-online.de',
                        'www.independent.co.uk',
                        'www.beneath-ceaseless-skies.com',
                        'pinterest.com',
                        'www.answers.com',
                        'memory-alpha.wikia.com',
                        'en.wikisource.org',
                        'www.smashwords.com',
                        'www.sfadb.com',
                        'facebook.com',
                        'www.britannica.com',
                        'tardis.wikia.com',
                        'prabook.com',
                        'www.grantvillegazette.com',
                        'bearalley.blogspot.com',
                        'www.perrypedia.de',
                        'www.bpib.com',
                        'www.nndb.com',
                        'www.gutenberg.org',
                        'ameqlist.com',
                        'pt.wikipedia.org',
                        'hu.wikipedia.org',
                        'ru.wikipedia.org',
                        'it.wikipedia.org',
                        'www.deboekenplank.nl',
                        'us.macmillan.com',
                        'fanac.org',
                        'seananmcguire.com',
                        'www.christinefeehan.com',
                        'www.linkedin.com',
                        'starwars.wikia.com',
                        'www.erbzine.com',
                        'www.guardian.co.uk',
                        'web.archive.org',
                        'www.myspace.com',
                        'data.bnf.fr',
                        'en.memory-alpha.org',
                        'www.ilona-andrews.com',
                        'id.ndl.go.jp',
                        'www.victorianweb.org',
                        'www.shannonassociates.com',
                        'desturmobed.blogspot.com',
                        'id.loc.gov',
                        'www.babelio.com',
                        'www.goblinfruit.net',
                        'www.heroicfantasyquarterly.com',
                        'www.noosfere.org',
                        'www.archive.org',
                        'www.donatoart.com',
                        'ro.wikipedia.org',
                        'openlibrary.org',
                        'da.wikipedia.org',
                        'sv.wikipedia.org'):
            pass
        else:
            domains[domain] = domains.get(domain, 0) + 1
            print webpage_id, url
            new_url = 'https://%s' % url_segments
            print new_url
            update = """update webpages set url = '%s' where webpage_id = %d""" % (db.escape_string(new_url), webpage_id)
            db.query(update)
        record = result.fetch_row()

    domains_list = sorted(domains.items(), key=lambda x: x[1], reverse=True)
    for domain in domains_list:
        print domain[0], domain[1]

