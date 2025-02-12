#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Ahasuerus and Lokal_Profil
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 901 $
#     Date: $Date: 2022-04-04 15:24:03 -0400 (Mon, 04 Apr 2022) $

import sys
import string
from isfdb import *
from SQLparsing import *
from library import XMLescape, ISFDBconvertDate, ISFDBHostCorrection
from pubClass import pubs


def pubOutput(pub_bodies):
        print '<?xml version="1.0" encoding="iso-8859-1" ?>'
        print '<ISFDB>'
        print '  <Records>%d</Records>' % len(pub_bodies)
        print '  <Publications>'
        for pub_body in pub_bodies:
                onePubOutput(pub_body)
        print '  </Publications>'
        print '</ISFDB>'

def onePubOutput(publication):        

        pub = pubs(db)
        pub.pub_id = publication[PUB_PUBID]

        print '    <Publication>'
        print '      <Record>%s</Record>' % pub.pub_id
        print '      <Title>%s</Title>' % XMLescape(publication[PUB_TITLE], 1)
        authors = SQLPubAuthors(pub.pub_id)
        printMultiValued(authors, 'Authors', 'Author')

        if publication[PUB_YEAR]:
                printTag(ISFDBconvertDate(publication[PUB_YEAR], 1), 'Year')
        printTag(publication[PUB_ISBN], 'Isbn')
        printTag(publication[PUB_CATALOG], 'Catalog')
        if publication[PUB_PUBLISHER]:
                publisher = SQLGetPublisher(publication[PUB_PUBLISHER])
                printTag(publisher[PUBLISHER_NAME], 'Publisher')
        if publication[PUB_SERIES]:
                pubseries = SQLGetPubSeries(publication[PUB_SERIES])
                printTag(pubseries[PUB_SERIES_NAME], 'PubSeries')
        printTag(publication[PUB_SERIES_NUM], 'PubSeriesNum')
        printTag(publication[PUB_PRICE], 'Price')
        printTag(publication[PUB_PAGES], 'Pages')
        printTag(publication[PUB_PTYPE], 'Binding')
        printTag(publication[PUB_CTYPE], 'Type')
        printTag(publication[PUB_TAG], 'Tag')
        printTag(ISFDBHostCorrection(publication[PUB_IMAGE]), 'Image')

        artists = SQLPubArtists(pub.pub_id)
        printMultiValued(artists, 'CoverArtists', 'Artist')

        if publication[PUB_NOTE]:
                notes = SQLgetNotes(publication[PUB_NOTE])
                printTag(notes, 'Note')

        pub.loadExternalIDs()
        if pub.identifiers:
                print pub.xmlIdentifiers(1)
        
        pub.loadPubWebpages()
        printMultiValued(pub.pub_webpages, 'Webpages', 'Webpage')
        
        pub.loadTransTitles()
        printMultiValued(pub.pub_trans_titles, 'TransTitles', 'TransTitle')
        print '    </Publication>'

def printTag(value, tag):
        if not value:
                return
        print '      <%s>%s</%s>' % (tag, XMLescape(value, 1), tag)

def printMultiValued(values, outer_tag, inner_tag):
        if not values:
                return
        print '      <%s>' % outer_tag
        for value in values:
                print '        <%s>%s</%s>' % (inner_tag, XMLescape(value, 1), inner_tag)
        print '      </%s>' % outer_tag
