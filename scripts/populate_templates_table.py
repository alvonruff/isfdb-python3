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


import cgi
import sys
import os
import string
import MySQLdb
from localdefs import *
from library import *

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

    # Dictionary of supported templates. The structure is:
    #   key = template name
    #   1st tuple value = HTML link
    #   2nd tuple value = displayed name, e.g. the "OCLC" in "OCLC 123456"
    #   3rd tuple value = hover-over display value
    templates = {
        'ASIN': ('https://www.amazon.com/dp/%s', 'ASIN',
                 'Amazon Standard Identification Number'),
        'Audible-ASIN': ('https://www.audible.com/pd/%s', 'Audible-ASIN',
                 'Audible ASIN'),
        'Biblioman': ('https://biblioman.chitanka.info/books/%s', 'Biblioman',
                '&#1041;&#1080;&#1073;&#1083;&#1080;&#1086;&#1084;&#1072;&#1085; (Biblioman)'),
        'BL': ('http://explore.bl.uk/primo_library/libweb/action/dlDisplay.do?vid=BLVU1&docId=BLL01%s',
               'BL', 'British Library'),
        'BNB': ('http://search.bl.uk/primo_library/libweb/action/dlSearch.do?vid=BLBNB&institution=BL&query=any,exact,%s',
                'BNB', 'British National Bibliography'),
        'BNF': ('https://catalogue.bnf.fr/ark:/12148/%s', 'BNF',
                'Biblioth&egrave;que nationale de France'),
        'COBISS.BG': ('https://plus.bg.cobiss.net/opac7/bib/%s#full', 'COBISS.BG',
                'Co-operative Online Bibliographic Systems and Services - Bulgaria'),
        'COBISS.SR': ('https://plus.sr.cobiss.net/opac7/bib/%s#full', 'COBISS.SR',
                'Co-operative Online Bibliographic Systems and Services - Serbia'),
        'Contento': ('http://www.philsp.com/resources/isfac/0start.htm', 'Contento',
                           'Index to Science Fiction Anthologies and Collections, Combined Edition, William G. Contento'),
        'DNB': ('https://d-nb.info/%s', 'DNB',
                'Deutsche Nationalbibliothek'),
        'FantLab': ('https://fantlab.ru/', 'FantLab'),
        'FantLab-author': ('https://fantlab.ru/autor%s', 'FantLab author'),
        'FantLab-pub': ('https://fantlab.ru/edition%s', 'FantLab publication'),
        'FantLab-title': ('https://fantlab.ru/work%s', 'FantLab title'),
        'Goodreads': ('https://www.goodreads.com/book/show/%s', 'Goodreads'),
        'JNB': ('https://iss.ndl.go.jp/api/openurl?ndl_jpno=%s&locale=en', 'JNB',
                'Japanese National Bibliography'),
        'KBR': ('https://opac.kbr.be/Library/doc/SYRACUSE/%s/', 'KBR',
                 'De Belgische Bibliografie/La Bibliographie de Belgique'),
        'LCCN': ('https://lccn.loc.gov/%s', 'LCCN',
                 'Library of Congress Control Number'),
        'Libris': ('https://libris.kb.se/bib/%s', 'Libris (National Library of Sweden)',
                 'Libris - National Library of Sweden'),
        'Libris-XL': ('https://libris.kb.se/katalogisering/%s', 'Libris XL (National Library of Sweden, new interface)',
                 'Libris XL - National Library of Sweden (new interface)'),
        'LTF-pub': ('https://tercerafundacion.net/biblioteca/ver/libro/%s', 'La Tercera Fundaci&#243;n publication'),
        'LTF-title': ('https://tercerafundacion.net/biblioteca/ver/ficha/%s', 'La Tercera Fundaci&#243;n title'),
        'Locus1': ('https://www.locusmag.com/index', 'Locus1',
                   'The Locus Index to Science Fiction'),
        'NDL': ('https://id.ndl.go.jp/bib/%s/eng', 'NDL',
                'National Diet Library'),
        'NILF': ('http://nilf.it/%s/', 'NILF',
                 'Numero Identificativo della Letteratura Fantastica'),
        'NLA': ('https://nla.gov.au/nla.cat-vn%s', 'NLA',
                 'National Library of Australia ID'),
        'NooSFere': ('https://www.noosfere.org/livres/niourf.asp?numlivre=%s', 'NooSFere',
                'NooSFere'),
        'OCLC': ('https://www.worldcat.org/oclc/%s', 'OCLC',
                 'WorldCat/Online Computer Library Center'),
        'OpenLibrary': ('https://openlibrary.org/books/%s', 'Open Library'),
        'PORBASE': ('http://id.bnportugal.gov.pt/bib/porbase/%s',
                    'PORBASE', 'Biblioteca Nacional de Portugal'),
        'PPN': ('http://picarta.pica.nl/xslt/DB=3.9/XMLPRS=Y/PPN?PPN=%s', 'PPN',
                'De Nederlandse Bibliografie Pica Productie Nummer'),
        'SF-Leihbuch': ('http://www.sf-leihbuch.de/index.cfm?bid=%s', 'SF-Leihbuch', 'Science Fiction-Leihbuch-Datenbank'),
        'SFBG': ('http://www.sfbg.us', 'SFBG',
                 'Bulgarian SF'),
        'SFBG-pub': ('http://www.sfbg.us/book/%s', 'SFBG publication',
                     'Bulgarian SF - publication'),
        'SFBG-publisher': ('http://www.sfbg.us/publisher/%s', 'SFBG publisher',
                           'Bulgarian SF - publisher'),
        'SFBG-title': ('http://www.sfbg.us/pubsequence/%s', 'SFBG title',
                       'Bulgarian SF - title'),
        'SFE': ('https://www.sf-encyclopedia.com/', 'SFE',
                 'Online Edition of the Encyclopedia of Science Fiction'),
    }

    #   key = template name
    #   1st tuple value = HTML link
    #   2nd tuple value = displayed name, e.g. the "OCLC" in "OCLC 123456"
    #   3rd tuple value = hover-over display value
    for template_name in sorted(templates):
        data = templates[template_name]
        template_url = data[0]
        template_display = data[1]
        template_mouseover = ''
        if len(data) > 2:
            template_mouseover = data[2]
##        print template, url, displayed, mouseover
        insert = """insert into
                    templates(template_name, template_display, template_type, template_url, template_mouseover)
                    values('%s', '%s', 'External URL', '%s', '%s')""" % (db.escape_string(template_name),
                                                               db.escape_string(template_display),
                                                               db.escape_string(template_url),
                                                               db.escape_string(template_mouseover))
        db.query(insert)

    internal_links = {
        'A': ('se.cgi?arg=%s&amp;type=Name&amp;mode=exact', ),
        'Bleiler1': ('title.cgi?102825', 'Bleiler1',
                           'Science-Fiction: The Gernsback Years by Everett F. Bleiler and Richard J. Bleiler, 1998'),
        'Bleiler78': ('title.cgi?187785', 'Bleiler78',
                           'The Checklist of Science-Fiction and Supernatural Fiction by E. F. Bleiler, 1978'),
        'Clute/Grant': ('title.cgi?189435', 'Clute/Grant',
                           'The Encyclopedia of Fantasy, eds. John Clute and John Grant, 1997'),
        'Clute/Nicholls': ('title.cgi?102324', 'Clute/Nicholls',
                           'The Encyclopedia of Science Fiction, 2nd edition, eds. John Clute and Peter Nicholls, 1993'),
        'Currey': ('title.cgi?102939', 'Currey',
                           'Science Fiction and Fantasy Authors: A Bibliography of First Printings of Their Fiction and Selected Nonfiction by L. W. Currey, 1979'),
        'Miller/Contento': ('title.cgi?1088499', 'Miller/Contento',
                           'Science Fiction, Fantasy, & Weird Fiction Magazine Index (1890-2007) by Stephen T. Miller and William G. Contento'),
        'Publisher': ('se.cgi?arg=%s&amp;type=Publisher&amp;mode=exact', ),
        'PubS': ('se.cgi?arg=%s&amp;type=Publication+Series&amp;mode=exact', ),
        'Reginald1': ('title.cgi?102834', 'Reginald1',
                           'Science Fiction and Fantasy Literature: A Checklist, 1700-1974 by Robert Reginald, 1979'),
        'Reginald3': ('title.cgi?102835', 'Reginald3',
                           'Science Fiction and Fantasy Literature 1975 - 1991 by Robert Reginald, 1992'),
        'S': ('se.cgi?arg=%s&amp;type=Series&amp;mode=exact', ),
        'Tuck': ('pe.cgi?10230', 'Tuck',
                           'The Encyclopedia of Science Fiction and Fantasy through 1968 by Donald H. Tuck, 1974-1982'),
    }
    for template_name in sorted(internal_links):
        data = internal_links[template_name]
        template_url = data[0]
        template_display = ''
        if len(data) > 1:
            template_display = data[1]
        template_mouseover = ''
        if len(data) > 2:
            template_mouseover = data[2]
        insert = """insert into
                    templates(template_name, template_display, template_type, template_url, template_mouseover)
                    values('%s', '%s', 'Internal URL', '%s', '%s')""" % (db.escape_string(template_name),
                                                               db.escape_string(template_display),
                                                               db.escape_string(template_url),
                                                               db.escape_string(template_mouseover))
        db.query(insert)

    substitute_templates = {
        'Incomplete': ('', 'The Contents section of this record is incomplete; additional eligible titles still need to be added.', ),
        'ISBN': ('%s', 'Additional ISBN'),
        'MultiS': ('', 'Note that this title belongs to multiple series. Because of software limitations, only one of them currently appears in the Series field.', ),
        'MultiPubS': ('', 'Note that this publication belongs to multiple publication series. Because of software limitations, only one of them currently appears in the Publication Series field.', ),
        'Narrator': ('%s', 'Narrated by'),
        'Tr': ('%s', 'Translated by'),
        'WatchDate': ('', 'Publication date is based on questionable pre-publication information and may be incorrect.', )
    }
    for template_name in sorted(substitute_templates):
        data = substitute_templates[template_name]
        template_url = data[0]
        template_display = ''
        if len(data) > 1:
            template_display = data[1]
        template_mouseover = ''
        if len(data) > 2:
            template_mouseover = data[2]
        insert = """insert into
                    templates(template_name, template_display, template_type, template_url, template_mouseover)
                    values('%s', '%s', 'Substitute String', '%s', '%s')""" % (db.escape_string(template_name),
                                                               db.escape_string(template_display),
                                                               db.escape_string(template_url),
                                                               db.escape_string(template_mouseover))
        db.query(insert)
