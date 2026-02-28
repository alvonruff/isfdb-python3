#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2015-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1264 $
#         Date: $Date: 2026-02-21 11:58:41 -0500 (Sat, 21 Feb 2026) $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

def convertDiacritics(title):
        replace = combiningDiacritics()
        for key in replace:
                while key in title:
                        title = title.replace(key, replace[key])
        if ('&#7' in title) or ('&#8' in title):
                print(title)
        return title

def combiningDiacritics():
        replace = {
                'A&#768;': chr(192), # A grave accent
                'A&#769;': chr(193), # A acute accent
                'A&#770;': chr(194), # A cirmuflex accent
                'A&#771;': chr(195), # A tilde
                'A&#772;': '&#256;', # A macron
                'A&#774;': '&#258;', # A breve
                'A&#775;': '&#550;', # A dot above
                'A&#776;': chr(196), # A diaresis/umlaut
                'A&#778;': chr(197), # A ring above
                'A&#780;': '&#461;', # A caron
                'A&#783;': '&#512;', # A double grave
                'A&#785;': '&#514;', # A inverted breve
                'A&#808;': '&#260;', # A ogonek
                'C&#769;': '&#262;', # C acute accent
                'C&#770;': '&#264;', # C cirmuflex accent
                'C&#775;': '&#266;', # C dot above
                'C&#780;': '&#268;', # C caron
                'C&#807;': chr(199), # C cedilla
                'D&#780;': '&#270;', # D caron
                'E&#768;': chr(200), # E grave accent
                'E&#769;': chr(201), # E acute accent
                'E&#770;': chr(202), # E cirmuflex accent
                'E&#772;': '&#274;', # E macron
                'E&#774;': '&#276;', # E breve
                'E&#775;': '&#278;', # E dot above
                'E&#776;': chr(203), # E diaresis/umlaut
                'E&#780;': '&#282;', # E caron
                'E&#783;': '&#516;', # E double grave
                'E&#785;': '&#518;', # E inverted breve
                'E&#807;': '&#552;', # E cedilla
                'E&#808;': '&#280;', # E ogonek
                'G&#769;': '&#500;', # G acute accent
                'G&#770;': '&#284;', # G cirmuflex accent
                'G&#774;': '&#286;', # G breve
                'G&#775;': '&#288;', # G dot above
                'G&#780;': '&#486;', # G caron
                'G&#807;': '&#290;', # G cedilla
                'H&#770;': '&#292;', # H cirmuflex accent
                'H&#780;': '&#542;', # H caron
                'I&#768;': chr(204), # I grave accent
                'I&#769;': chr(205), # I acute accent
                'I&#770;': chr(206), # I cirmuflex accent
                'I&#771;': '&#296;', # I tilde
                'I&#772;': '&#298;', # I macron
                'I&#774;': '&#300;', # I breve
                'I&#775;': '&#304;', # I dot above
                'I&#776;': chr(207), # I diaresis/umlaut
                'I&#780;': '&#463;', # I caron
                'I&#783;': '&#520;', # I double grave
                'I&#785;': '&#522;', # I inverted breve
                'I&#808;': '&#302;', # I ogonek
                'J&#770;': '&#308;', # J cirmuflex accent
                'K&#780;': '&#488;', # K caron
                'K&#807;': '&#310;', # K cedilla
                'L&#769;': '&#313;', # L acute accent
                'L&#780;': '&#317;', # L caron
                'L&#807;': '&#315;', # L cedilla
                'N&#768;': '&#504;', # N grave accent
                'N&#769;': '&#323;', # N acute accent
                'N&#771;': chr(209), # N tilde
                'N&#780;': '&#327;', # N caron
                'N&#807;': '&#325;', # N cedilla
                'O&#768;': chr(210), # O grave accent
                'O&#769;': chr(211), # O acute accent
                'O&#770;': chr(212), # O cirmuflex accent
                'O&#771;': chr(213), # O tilde
                'O&#772;': '&#332;', # O macron
                'O&#774;': '&#334;', # O breve
                'O&#775;': '&#558;', # O dot above
                'O&#776;': chr(214), # O diaresis/umlaut
                'O&#779;': '&#336;', # O double acute
                'O&#780;': '&#465;', # O caron
                'O&#783;': '&#524;', # O double grave
                'O&#785;': '&#526;', # O inverted breve
                'O&#808;': '&#490;', # O ogonek
                'R&#769;': '&#340;', # R acute accent
                'R&#780;': '&#344;', # R caron
                'R&#783;': '&#528;', # R double grave
                'R&#785;': '&#530;', # R inverted breve
                'R&#807;': '&#342;', # R cedilla
                'S&#769;': '&#346;', # S acute accent
                'S&#770;': '&#348;', # S cirmuflex accent
                'S&#780;': '&#352;', # S caron
                'S&#806;': '&#536;', # S comma below
                'S&#807;': '&#350;', # S cedilla
                'T&#780;': '&#356;', # T caron
                'T&#806;': '&#538;', # T comma below
                'T&#807;': '&#354;', # T cedilla
                'U&#768;': chr(217), # U grave accent
                'U&#769;': chr(218), # U acute accent
                'U&#770;': chr(219), # U cirmuflex accent
                'U&#771;': '&#360;', # U tilde
                'U&#772;': '&#362;', # U macron
                'U&#774;': '&#364;', # U breve
                'U&#776;': chr(220), # U diaresis/umlaut
                'U&#778;': '&#366;', # U ring above
                'U&#779;': '&#368;', # U double acute
                'U&#780;': '&#467;', # U caron
                'U&#783;': '&#532;', # U double grave
                'U&#785;': '&#534;', # U inverted breve
                'U&#808;': '&#370;', # U ogonek
                'W&#770;': '&#372;', # W cirmuflex accent
                'Y&#769;': chr(221), # Y acute accent
                'Y&#770;': '&#374;', # Y cirmuflex accent
                'Y&#776;': '&#376;', # Y diaresis/umlaut
                'Y&#772;': '&#562;', # Y macron
                'Z&#769;': '&#377;', # Z acute accent
                'Z&#775;': '&#379;', # Z dot above
                'Z&#780;': '&#381;', # Z caron
                'a&#768;': chr(224), # a grave accent
                'a&#769;': chr(225), # a acute accent
                'a&#770;': chr(226), # a cirmuflex accent
                'a&#771;': chr(227), # a tilde
                'a&#772;': '&#257;', # a macron
                'a&#774;': '&#259;', # a breve
                'a&#775;': '&#551;', # a dot above
                'a&#776;': chr(228), # a diaresis/umlaut
                'a&#778;': chr(229), # a ring above
                'a&#780;': '&#462;', # a caron
                'a&#783;': '&#513;', # a double grave
                'a&#785;': '&#515;', # a inverted breve
                'a&#808;': '&#261;', # a ogonek
                'c&#769;': '&#263;', # c acute accent
                'c&#770;': '&#265;', # c cirmuflex accent
                'c&#775;': '&#267;', # c dot above
                'c&#780;': '&#269;', # c caron
                'c&#807;': chr(231), # c cedilla
                'd&#780;': '&#271;', # d caron (displayed as an apostrophe)
                'e&#768;': chr(232), # e grave accent
                'e&#769;': chr(233), # e acute accent
                'e&#770;': chr(234), # e cirmuflex accent
                'e&#772;': '&#275;', # e macron
                'e&#774;': '&#277;', # e breve
                'e&#775;': '&#279;', # e dot above
                'e&#776;': chr(235), # e diaresis/umlaut
                'e&#780;': '&#283;', # e caron
                'e&#783;': '&#517;', # e double grave
                'e&#785;': '&#519;', # e inverted breve
                'e&#807;': '&#553;', # e cedilla
                'e&#808;': '&#281;', # e ogonek
                'g&#769;': '&#501;', # g acute accent
                'g&#770;': '&#285;', # g cirmuflex accent
                'g&#774;': '&#287;', # g breve
                'g&#775;': '&#289;', # g dot above
                'g&#780;': '&#487;', # g caron
                'g&#807;': '&#291;', # g cedilla
                'h&#770;': '&#293;', # h cirmuflex accent
                'h&#780;': '&#543;', # h caron
                'i&#768;': chr(236), # i grave accent
                'i&#769;': chr(237), # i acute accent
                'i&#770;': chr(238), # i cirmuflex accent
                'i&#771;': '&#297;', # i tilde
                'i&#772;': '&#299;', # i macron
                'i&#774;': '&#301;', # i breve
                'i&#776;': chr(239), # i diaresis/umlaut
                'i&#780;': '&#464;', # i caron
                'i&#783;': '&#521;', # i double grave
                'i&#785;': '&#523;', # i inverted breve
                'i&#808;': '&#303;', # i ogonek
                'j&#770;': '&#309;', # j cirmuflex accent
                'j&#780;': '&#496;', # j caron
                'k&#780;': '&#489;', # k caron
                'k&#807;': '&#311;', # k cedilla
                'l&#769;': '&#314;', # l acute accent
                'l&#780;': '&#318;', # L caron
                'l&#807;': '&#316;', # l cedilla
                'n&#768;': '&#505;', # n grave accent
                'n&#769;': '&#324;', # n acute accent
                'n&#771;': chr(241), # n tilde
                'n&#780;': '&#328;', # n caron
                'n&#807;': '&#326;', # n cedilla
                'o&#768;': chr(242), # o grave accent
                'o&#769;': chr(243), # o acute accent
                'o&#770;': chr(244), # o cirmuflex accent
                'o&#771;': chr(245), # o tilde
                'o&#772;': '&#333;', # o macron
                'o&#774;': '&#335;', # o breve
                'o&#775;': '&#559;', # o dot above
                'o&#776;': chr(246), # o diaresis/umlaut
                'o&#779;': '&#337;', # o double acute
                'o&#780;': '&#466;', # o caron
                'o&#783;': '&#525;', # o double grave
                'o&#785;': '&#527;', # o inverted breve
                'o&#808;': '&#491;', # o ogonek
                'r&#769;': '&#341;', # r acute accent
                'r&#780;': '&#345;', # r caron
                'r&#783;': '&#529;', # r double grave
                'r&#785;': '&#531;', # r inverted breve
                'r&#807;': '&#343;', # r cedilla
                's&#769;': '&#347;', # s acute accent
                's&#770;': '&#349;', # s cirmuflex accent
                's&#780;': '&#353;', # s caron
                's&#806;': '&#537;', # s comma below
                's&#807;': '&#351;', # s cedilla
                't&#780;': '&#357;', # t caron
                't&#806;': '&#539;', # t comma below
                't&#807;': '&#355;', # t cedilla
                'u&#768;': chr(249), # u grave accent
                'u&#769;': chr(250), # u acute accent
                'u&#770;': chr(251), # u cirmuflex accent
                'u&#771;': '&#361;', # u tilde
                'u&#772;': '&#363;', # u macron
                'u&#774;': '&#365;', # u breve
                'u&#776;': chr(252), # u diaresis/umlaut
                'u&#778;': '&#367;', # u ring above
                'u&#779;': '&#369;', # u double acute
                'u&#780;': '&#468;', # u caron
                'u&#783;': '&#533;', # u double grave
                'u&#785;': '&#535;', # u inverted breve
                'u&#808;': '&#371;', # u ogonek
                'w&#770;': '&#373;', # w cirmuflex accent
                'y&#769;': chr(253), # y acute accent
                'y&#770;': '&#375;', # y cirmuflex accent
                'y&#772;': '&#563;', # y macron
                'y&#776;': chr(255), # y diaresis/umlaut
                'z&#769;': '&#378;', # z acute accent
                'z&#775;': '&#380;', # z dot above
                'z&#780;': '&#382;'  # z caron
                }
        return replace

if __name__ == '__main__':

        # Retrieve all titles with suspected combining diacritics
        query = "select title_id, title_title from titles where title_title like '%&#7%' or title_title like '%&#8%'"

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        titles = []
        while record:
                titles.append(record[0])
                record = CNX.DB_FETCHMANY()

        for title in titles:
                title_id = int(title[0])
                print(title_id)
                title_title = title[1]
                new_title = convertDiacritics(title_title)
                update = "update titles set title_title='%s' where title_id=%d" % (CNX.DB_ESCAPE_STRING(new_title), title_id)
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)

        # Retrieve all publication records with suspected combining diacritics
        query = "select pub_id, pub_title from pubs where pub_title like '%&#7%' or pub_title like '%&#8%'"
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        titles = []
        while record:
                titles.append(record[0])
                record = CNX.DB_FETCHMANY()

        for title in titles:
                title_id = int(title[0])
                print(title_id)
                title_title = title[1]
                new_title = convertDiacritics(title_title)
                update = "update pubs set pub_title='%s' where pub_id=%d" % (CNX.DB_ESCAPE_STRING(new_title), title_id)
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)

