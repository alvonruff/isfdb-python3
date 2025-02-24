#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2009-2025   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2009/10/20 03:07:27 $


import cgi
import sys
import os
import string
import MySQLdb
from localdefs import *

def Date_or_None(s):
    return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)

def populate():

    pop = [('afr', 'Afrikaans')]
    pop.append(('alb', 'Albanian'))
    pop.append(('grc', 'Ancient Greek'))
    pop.append(('ara', 'Arabic'))
    pop.append(('arm', 'Armenian'))
    pop.append(('aze', 'Azerbaijani'))
    pop.append(('baq', 'Basque'))
    pop.append(('bel', 'Belarusian'))
    pop.append(('ben', 'Bengali'))
    pop.append(('bul', 'Bulgarian'))
    pop.append(('bur', 'Burmese'))
    pop.append(('cat', 'Catalan'))
    pop.append(('chi', 'Chinese'))
    pop.append(('cze', 'Czech'))
    pop.append(('dan', 'Danish'))
    pop.append(('dut', 'Dutch'))
    pop.append(('eng', 'English'))
    pop.append(('epo', 'Esperanto'))
    pop.append(('est', 'Estonian'))
    pop.append(('fil', 'Filipino'))
    pop.append(('fin', 'Finnish'))
    pop.append(('fre', 'French'))
    pop.append(('fry', 'Frisian'))
    pop.append(('glg', 'Galician'))
    pop.append(('geo', 'Georgian'))
    pop.append(('ger', 'German'))
    pop.append(('gre', 'Greek'))
    pop.append(('guj', 'Gujarati'))
    pop.append(('heb', 'Hebrew'))
    pop.append(('hin', 'Hindi'))
    pop.append(('hrv', 'Croatian'))
    pop.append(('hun', 'Hungarian'))
    pop.append(('ice', 'Icelandic'))
    pop.append(('ind', 'Indonesian'))
    pop.append(('gle', 'Irish'))
    pop.append(('ita', 'Italian'))
    pop.append(('jpn', 'Japanese'))
    pop.append(('kaz', 'Kazakh'))
    pop.append(('khm', 'Khmer'))
    pop.append(('kir', 'Kyrgyz'))
    pop.append(('kor', 'Korean'))
    pop.append(('lav', 'Latvian'))
    pop.append(('lat', 'Latin'))
    pop.append(('lit', 'Lithuanian'))
    pop.append(('mac', 'Macedonian'))
    pop.append(('may', 'Malay'))
    pop.append(('mal', 'Malayalam'))
    pop.append(('mar', 'Marathi'))
    pop.append(('mon', 'Mongolian'))
    pop.append(('nor', 'Norwegian'))
    pop.append(('per', 'Persian'))
    pop.append(('pol', 'Polish'))
    pop.append(('por', 'Portuguese'))
    pop.append(('rum', 'Romanian'))
    pop.append(('rus', 'Russian'))
    pop.append(('gla', 'Scottish Gaelic'))
    pop.append(('slo', 'Slovak'))
    pop.append(('slv', 'Slovenian'))
    pop.append(('spa', 'Spanish'))
    pop.append(('srp', 'Serbian'))
    pop.append(('sin', 'Sinhalese'))
    pop.append(('swe', 'Swedish'))
    pop.append(('tgk', 'Tajik'))
    pop.append(('tam', 'Tamil'))
    pop.append(('tha', 'Thai'))
    pop.append(('tib', 'Tibetan'))
    pop.append(('tur', 'Turkish'))
    pop.append(('ukr', 'Ukrainian'))
    pop.append(('urd', 'Urdu'))
    pop.append(('uzb', 'Uzbek'))
    pop.append(('vie', 'Vietnamese'))
    pop.append(('wel', 'Welsh'))
    pop.append(('yid', 'Yiddish'))
    return pop

if __name__ == '__main__':

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    pop = populate()
    for lang in pop:
        lang_code = db.escape_string(lang[0])
        lang_name = db.escape_string(lang[1])
        update = "insert into languages (lang_name, lang_code) values('%s','%s')" % (lang_name, lang_code)
        print(update)
        db.query(update)
