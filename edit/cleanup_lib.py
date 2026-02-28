#
#     (C) COPYRIGHT 2012-2025 Ahasuerus
#     ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1240 $
#     Date: $Date: 2026-02-07 07:25:49 -0500 (Sat, 07 Feb 2026) $


def reportsDict():
        reports = {}
        reports[1] = ("Titles without Authors")
        reports[2] = ("Variant Title-Alternate Name Mismatches")
        reports[3] = ("Titles without Pubs")
        reports[5] = ("Mismatched Angle Brackets")
        reports[6] = ("Authors with Invalid Directory Entries")
        reports[7] = ("Author Names with Invalid or Suspect Data")
        reports[8] = ("Authors That Exist Only Due to Reviews")
        reports[9] = ("Variant Titles in Series")
        reports[10] = ("Alternate Names with Canonical Titles")
        reports[11] = ("Prolific Authors without a Defined Language")
        reports[12] = ("EDITOR Records not in a Series")
        reports[13] = ("Variant EDITOR Records in a Series")
        reports[14] = ("Missing EDITOR Records")
        reports[15] = ("Publications with Extra EDITOR Records")
        reports[16] = ("Empty Series")
        reports[17] = ("Series with Duplicate Numbers")
        reports[18] = ("Titles with Bad Ellipses")
        reports[19] = ("Interviews of Alternate Names")
        reports[20] = ("Variant Titles of Variant Titles")
        reports[21] = ("Variant Titles of Missing Titles")
        reports[22] = ("SERIALs without a Parent Title")
        reports[23] = ("Awards Associated with Invalid Titles")
        reports[24] = ("Suspect Untitled Awards")
        reports[25] = ("Empty Award Types")
        reports[26] = ("Empty Award Categories")
        reports[27] = ("Series with Chapbooks")
        reports[28] = ("Chapbooks with Synopses")
        reports[29] = ("Chapbooks without Contents Titles")
        reports[30] = ("Chapbooks with Mismatched Variant Types")
        reports[31] = ("Pre-2005 ISBN-13s and post-2007 ISBN-10s")
        reports[32] = ("Duplicate Publication Tags")
        reports[33] = ("Publication Authors That Are Not the Title Author")
        reports[34] = ("Publications Without Titles")
        reports[35] = ("Invalid Publication Formats")
        reports[36] = ("Pubs with Images We Don't Have Permission to Link to")
        reports[37] = ("Omnibuses without Contents Titles")
        reports[38] = ("Publications with Duplicate Titles")
        reports[39] = ("Publications with Bad Ellipses")
        reports[40] = ("Reviews without Reviewed Authors")
        reports[41] = ("Reviews not Linked to Titles")
        reports[42] = ("Reviews of Uncommon Title Types")
        reports[43] = ("Publishers with Identical Names")
        reports[44] = ("Publishers with Similar Names")
        reports[45] = ("Variant Title Type Mismatches")
        reports[46] = ("EDITOR records not in MAGAZINE/FANZINE publications")
        reports[47] = ("Title Dates after Publication Dates (first 1000)")
        reports[48] = ("Series with Numbering Gaps")
        reports[49] = ("Publications with Invalid ISBN Formats")
        reports[50] = ("Publications with Invalid ISBN Checksums")
        reports[51] = ("Publications with Identical ISBNs and Different Titles")
        reports[52] = ("Publications with 0 or 2+ Reference Titles")
        reports[53] = ("Authors with Duplicate Alternate Names")
        reports[54] = ("Container Titles in Publications with no Contents")
        reports[55] = ("Title records with HTML in Titles")
        reports[56] = ("Publications with HTML in Titles")
        reports[57] = ("Invalid SFE Image Links")
        reports[58] = ("Suspected Dutch Authors without a Language Code")
        reports[59] = ("Suspected French Authors without a Language Code")
        reports[60] = ("Suspected German Authors without a Language Code")
        reports[61] = ("Suspected Other Non-English Authors without a Language Code")
        reports[62] = ("Titles with Invalid Length Values")
        reports[63] = ("Genre/Non-Genre Mismatches")
        reports[64] = ("Series with EDITOR and non-EDITOR Titles")
        reports[65] = ("Publishers with Invalid Unicode Characters")
        reports[66] = ("Publication Series with Invalid Unicode Characters")
        reports[67] = ("Series with Invalid Unicode Characters")
        reports[68] = ("Authors with Invalid Unicode Characters")
        reports[69] = ("Titles with Invalid Unicode Characters")
        reports[70] = ("Publications with Invalid Unicode Characters")
        reports[71] = ("Forthcoming Titles")
        reports[72] = ("Forthcoming Publications")
        reports[73] = ("Publishers with Suspect Unicode Characters")
        reports[74] = ("Titles with Suspect Unicode Characters")
        reports[75] = ("Publications with Suspect Unicode Characters")
        reports[76] = ("Series with Suspect Unicode Characters")
        reports[77] = ("Publication Series with Suspect Unicode Characters")
        reports[78] = ("Authors with Suspect Unicode Characters")
        reports[79] = ("Novel Publications with Fewer Than 80 Pages")
        reports[80] = ("Duplicate SHORTFICTION in Magazines/Fanzines")
        reports[81] = ("Series with Slashes and No Spaces")
        reports[82] = ("Invalid Record URLs in Notes")
        reports[83] = ("Serials without Standard Parenthetical Disambiguators")
        reports[84] = ("Serials with Potentially Unnecessary Disambiguation")
        reports[85] = ("Non-Latin Authors with Latin Characters in Legal Names")
        reports[86] = ("Primary-Verified Publications with Unknown Format")
        reports[87] = ("Author/Title Language Mismatches")
        reports[88] = ("Pubs with Multiple COVERART Titles")
        reports[89] = ("Authors with Invalid Birthplaces")
        reports[90] = ("Duplicate Sub-series Numbers within a Series")
        reports[91] = ("Non-Art Titles by Non-English Authors without a Language")
        reports[92] = ("Primary-Verified Anthologies and Collections without Contents Titles")
        reports[93] = ("Publication Title-Reference Title Mismatches")
        reports[94] = ("Authors Without Titles")
        reports[95] = ("Authors With Dangling Publications")
        reports[96] = ("COVERART Titles with a 'Cover:' Prefix")
        reports[97] = ("Publication Series with Latin Names and Non-Latin Titles")
        reports[98] = ("Publication Series with Identical Names")
        reports[99] = ("Publishers with Latin Names and Non-Latin Titles")
        reports[100] = ("Publications with Invalid Prices")
        reports[101] = ("Publications with Wiki pages")
        reports[102] = ("Publications with Talk pages")
        reports[103] = ("Publication Wiki pages not linked to Publication records")
        reports[104] = ("Publication Talk Wiki pages not linked to Publication records")
        reports[105] = ("Series with Wiki pages")
        reports[106] = ("Series with Talk pages")
        reports[107] = ("Series Wiki pages not linked to Series records")
        reports[108] = ("Series Talk Wiki pages not linked to Series records")
        reports[109] = ("Publishers with Wiki pages")
        reports[110] = ("Publishers with Talk pages")
        reports[111] = ("Publisher Wiki pages not linked to Publisher records")
        reports[112] = ("Publisher Talk Wiki pages not linked to Publisher records")
        reports[113] = ("Magazines with Wiki pages")
        reports[114] = ("Magazines with Talk pages")
        reports[115] = ("Magazine Wiki pages not linked to Magazine records")
        reports[116] = ("Magazine Talk Wiki pages not linked to Magazine records")
        reports[117] = ("Fanzines with Wiki pages")
        reports[118] = ("Fanzines with Talk pages")
        reports[119] = ("Fanzine Wiki pages not linked to Fanzine records")
        reports[120] = ("Fanzine Talk Wiki pages not linked to Fanzine records")
        reports[121] = ("Publication Series with non-Latin Names without Transliterated Names")
        reports[122] = ("Publishers with non-Latin Names without Transliterated Names")
        reports[123] = ("Authors with Transliterated Legal Names and no Legal Names")
        reports[124] = ("Bulgarian Titles without Transliterated Titles")
        reports[125] = ("Chinese Titles without Transliterated Titles")
        reports[126] = ("Czech Titles without Transliterated Titles")
        reports[127] = ("English Titles with non-Latin characters and without Transliterated Titles")
        reports[128] = ("Greek Titles without Transliterated Titles")
        reports[129] = ("Hungarian Titles without Transliterated Titles")
        reports[130] = ("Japanese Titles without Transliterated Titles")
        reports[131] = ("Lithuanian Titles without Transliterated Titles")
        reports[132] = ("Polish Titles without Transliterated Titles")
        reports[133] = ("Romanian Titles without Transliterated Titles")
        reports[134] = ("Russian Titles without Transliterated Titles")
        reports[135] = ("Serbian Titles without Transliterated Titles")
        reports[136] = ("Turkish Titles without Transliterated Titles")
        reports[137] = ("Other Titles without Transliterated Titles")
        reports[138] = ("Bulgarian Titles with Latin characters")
        reports[139] = ("Chinese Titles with Latin characters")
        reports[140] = ("Greek Titles with Latin characters")
        reports[141] = ("Japanese Titles with Latin characters")
        reports[142] = ("Russian Titles with Latin characters")
        reports[143] = ("Other Non-Latin Language Titles with Latin characters")
        reports[144] = ("Series Names That May Need Disambiguation")
        reports[145] = ("Romanian titles with s-cedilla or t-cedilla")
        reports[146] = ("Pubs with Romanian titles with s-cedilla or t-cedilla")
        reports[147] = ("Pubs with fullwidth yen signs")
        reports[148] = ("Bulgarian Publications without Transliterated Titles")
        reports[149] = ("Chinese Publications without Transliterated Titles")
        reports[150] = ("Czech Publications without Transliterated Titles")
        reports[151] = ("English Publications with non-Latin characters and without Transliterated Titles")
        reports[152] = ("Greek Publications without Transliterated Titles")
        reports[153] = ("Hungarian Publications without Transliterated Titles")
        reports[154] = ("Japanese Publications without Transliterated Titles")
        reports[155] = ("Lithuanian Publications without Transliterated Titles")
        reports[156] = ("Polish Publications without Transliterated Titles")
        reports[157] = ("Romanian Publications without Transliterated Titles")
        reports[158] = ("Russian Publications without Transliterated Titles")
        reports[159] = ("Serbian Publications without Transliterated Titles")
        reports[160] = ("Turkish Publications without Transliterated Titles")
        reports[161] = ("Other Publications without Transliterated Titles")
        reports[162] = ("Bulgarian Publications with Latin characters")
        reports[163] = ("Chinese Publications with Latin characters")
        reports[164] = ("Greek Publications with Latin characters")
        reports[165] = ("Japanese Publications with Latin characters")
        reports[166] = ("Russian Publications with Latin characters")
        reports[167] = ("Other Non-Latin Language Publications with Latin characters")
        reports[168] = ("Authors with Author Data and One Non-Latin Title")
        reports[169] = ("Bulgarian Authors without Transliterated Names")
        reports[170] = ("Chinese Authors without Transliterated Names")
        reports[171] = ("Czech Authors without Transliterated Names")
        reports[172] = ("English Authors with non-Latin characters and without Transliterated Names")
        reports[173] = ("Greek Authors without Transliterated Names")
        reports[174] = ("Hungarian Authors without Transliterated Names")
        reports[175] = ("Japanese Authors without Transliterated Names")
        reports[176] = ("Lithuanian Authors without Transliterated Names")
        reports[177] = ("Polish Authors without Transliterated Names")
        reports[178] = ("Romanian Authors without Transliterated Names")
        reports[179] = ("Russian Authors without Transliterated Names")
        reports[180] = ("Serbian Authors without Transliterated Names")
        reports[181] = ("Turkish Authors without Transliterated Names")
        reports[182] = ("Other Authors without Transliterated Names")
        reports[183] = ("Bulgarian Titles with a Latin Author Name")
        reports[184] = ("Chinese Titles with a Latin Author Name")
        reports[185] = ("Greek Titles with a Latin Author Name")
        reports[186] = ("Japanese Titles with a Latin Author Name")
        reports[187] = ("Russian Titles with a Latin Author Name")
        reports[188] = ("Other Non-Latin Language Titles with a Latin Author Name")
        reports[189] = ("Publication Series Names That May Need Disambiguation")
        reports[190] = ("Awards with Invalid IMDB Links")
        reports[191] = ("Invalid HREFs in Notes")
        reports[192] = ("Authors without a Working Language")
        reports[193] = ("Multilingual Publications")
        reports[194] = ("Titles without a Language")
        reports[195] = ("Invalid Title Content Values")
        reports[196] = ("Juvenile/Non-Juvenile Mismatches")
        reports[197] = ("Novelization/Non-Novelization Mismatches")
        reports[198] = ("Author/Alternate Name Language Mismatches")
        reports[199] = ("Author Notes to be Migrated from ISFDB 1.0")
        reports[200] = ("Authors with 'Author' Wiki pages")
        reports[201] = ("Authors with 'Author Talk' Wiki pages")
        reports[202] = ("Author Wiki pages not linked to Author records")
        reports[203] = ("Author Talk pages not linked to Author records")
        reports[204] = ("Authors with 'Bio' Wiki pages")
        reports[205] = ("Authors with 'Bio Talk' Wiki pages")
        reports[206] = ("Bio pages not linked to Author records")
        reports[207] = ("Bio Talk pages not linked to Author records")
        reports[208] = ("Publications with unsupported HTML in Notes")
        reports[209] = ("Titles with unsupported HTML in Notes")
        reports[210] = ("Publishers with unsupported HTML in Notes")
        reports[211] = ("Series with unsupported HTML in Notes")
        reports[212] = ("Publication Series with unsupported HTML in Notes")
        reports[213] = ("Awards with unsupported HTML in Notes")
        reports[214] = ("Award Types with unsupported HTML in Notes")
        reports[215] = ("Award Categories with unsupported HTML in Notes")
        reports[216] = ("Titles with unsupported HTML in Synopses")
        reports[217] = ("Authors with unsupported HTML in Notes")
        reports[218] = ("Publications with ASINs in Notes")
        reports[219] = ("Publications with British library IDs in Notes")
        reports[220] = ("Publications with direct SFBG links in Notes")
        reports[221] = ("Publications with direct Deutsche Nationalbibliothek links in Notes")
        reports[222] = ("Publications with direct FantLab links in Notes")
        reports[223] = ("Publications with direct Amazon links in Notes")
        reports[224] = ("Publications with direct BNF links in Notes")
        reports[225] = ("Publications with direct Library of Congress links in Notes")
        reports[226] = ("Publications with direct OCLC/WorldCat links in Notes")
        reports[227] = ("Titles with mismatched parentheses")
        reports[228] = ("ISBN-less e-pubs without an ASIN")
        reports[229] = ("Mismatched HTML tags in Publication Notes")
        reports[230] = ("Mismatched OCLC URLs in Publication Notes")
        reports[231] = ("Missing Required Web Pages for Cover Images")
        reports[232] = ("Award Years with Month/Day Data")
        reports[233] = ("Potential Duplicate E-book Publications")
        reports[234] = ("Publications with direct De Nederlandse Bibliografie links in Notes")
        reports[235] = ("Publications with invalid BNF identifiers")
        reports[236] = ("SFBC Publications with an ISBN and no Catalog ID")
        reports[237] = ("Publications with non-template Library of Congress numbers in notes")
        reports[238] = ("Translations without Notes - Less Common Languages")
        reports[239] = ("Translations without the Tr Template in Notes (first 1000)")
        reports[240] = ("Anthologies and Collections without Fiction Titles")
        reports[241] = ("Magazines without Fiction Titles")
        reports[242] = ("CHAPBOOK/SHORTFICTION Juvenile Flag Mismatches")
        reports[243] = ("Publication Images with Potentially Problematic Amazon URLs")
        reports[244] = ("Publications with Invalid Non-numeric External IDs")
        reports[245] = ("Publications with Non-standard ASINs")
        reports[246] = ("Publications with Non-standard Barnes & Noble IDs")
        reports[247] = ("Publications with Non-standard LCCNs")
        reports[248] = ("Publications with Invalid Open Library IDs")
        reports[249] = ("Publications with Invalid BNB IDs")
        reports[250] = ("Publications with OCLC IDs matching ISBNs")
        reports[251] = ("Publications with an OCLC Verification, no ISBN and no OCLC External ID")
        reports[252] = ("Publications with an OCLC Verification, an ISBN and no OCLC External ID (first 1000)")
        reports[253] = ("Publications with non-linking External IDs in Notes")
        reports[254] = ("Publications with direct NooSFere links in Notes")
        reports[255] = ("Publications with direct NILF links in Notes")
        reports[256] = ("Publications with direct Fantascienza links in Notes")
        reports[257] = ("Series with non-Latin Characters in the Series Name without a Transliterated Name")
        reports[258] = ("Series with Bulgarian titles and without Unicode characters in the Series Name")
        reports[259] = ("Series with Chinese titles and without Unicode characters in the Series Name")
        reports[260] = ("Series with Greek titles and without Unicode characters in the Series Name")
        reports[261] = ("Series with Japanese titles and without Unicode characters in the Series Name")
        reports[262] = ("Series with Russian titles and without Unicode characters in the Series Name")
        reports[263] = ("Series with titles in less popular non-Latin languages and without Unicode characters in the Series Name")
        reports[264] = ("English Translations without Notes (first 1000)")
        reports[265] = ("Italian Translations without Notes (first 1000)")
        reports[266] = ("French Translations without Notes (first 1000)")
        reports[267] = ("German Translations without Notes (first 1000)")
        reports[268] = ("Dutch Translations without Notes (first 1000)")
        reports[269] = ("Portuguese Translations without Notes (first 1000)")
        reports[270] = ("Spanish Translations without Notes (first 1000)")
        reports[271] = ("Japanese Translations without Notes (first 1000)")
        reports[272] = ("Publications with incomplete contents and no Incomplete template")
        reports[273] = ("Mismatched Braces")
        reports[274] = ("References to Non-Existent Templates")
        reports[275] = ("Title Dates Before First Publication Date (first 1000)")
        reports[276] = ("Variant Title Dates Before Canonical Title Dates")
        reports[277] = ("Publications with the 'Incomplete' Template in Notes")
        reports[278] = ("Anthology Publications with Invalid Title Types")
        reports[279] = ("Collection Publications with Invalid Title Types")
        reports[280] = ("Chapbook Publications with Invalid Title Types")
        reports[281] = ("Magazine Publications with Invalid Title Types")
        reports[282] = ("Fanzine Publications with Invalid Title Types")
        reports[283] = ("Nonfiction Publications with Invalid Title Types")
        reports[284] = ("Novel Publications with Invalid Title Types")
        reports[285] = ("Omnibus Publications with Invalid Title Types")
        reports[286] = ("Variant Title Length Mismatches (first 1000)")
        reports[287] = ("Publications with Invalid Page Numbers")
        reports[288] = ("Publications with an Invalid Page Count")
        reports[289] = ("CHAPBOOK Publications with Multiple Fiction Titles")
        reports[290] = ("Suspected Ineligible Reviewed NONFICTION Titles (first 1000)")
        reports[291] = ("Suspected Invalid Uses of the Narrator Template")
        reports[292] = ("Audio Books without the Narrator Template")
        reports[293] = ("Titles with Suspect English Capitalization (first 1000)")
        reports[294] = ("Publications with Suspect English Capitalization (first 1000)")
        reports[295] = ("Publications with the WatchPrePub Template in Notes")
        reports[296] = ("Select Unverified Publications with 'First Printing' in Notes")
        reports[297] = ("Short Fiction Title Records with '(Part' in the Title field")
        reports[298] = ("Title-Based Awards with a Different Stored Author Name")
        reports[299] = ("Publications with Swedish Titles with no Libris XL ID")
        reports[300] = ("Publications with Swedish Titles with a Libris ID and no Libris XL ID")
        reports[301] = ("Reviews Whose Language Doesn't Match the Language of the Reviewed Title")
        reports[302] = ("Author Names with an Unrecognized Suffix")
        reports[303] = ("COVERART titles with 'uncredited' Author")
        reports[304] = ("Publications with COBISS references in notes and no template/External ID")
        reports[305] = ("Publications with Biblioman references in notes and no template/External ID")
        reports[306] = ("Publications with Duplicate Authors")
        reports[307] = ("Awards linked to Uncommon Title Types")
        reports[308] = ("English book-length titles with no publications and with a translation")
        reports[309] = ("French book-length titles with no publications and with a translation")
        reports[310] = ("German book-length titles with no publications and with a translation")
        reports[311] = ("Italian book-length titles with no publications and with a translation")
        reports[312] = ("Japanese book-length titles with no publications and with a translation")
        reports[313] = ("Russian book-length titles with no publications and with a translation")
        reports[314] = ("Spanish book-length titles with no publications and with a translation")
        reports[315] = ("Book-length titles with no publications and with a translation in other languages")
        reports[316] = ("English short titles with no publications and with a translation")
        reports[317] = ("French short titles with no publications and with a translation")
        reports[318] = ("German short titles with no publications and with a translation")
        reports[319] = ("Italian short titles with no publications and with a translation")
        reports[320] = ("Japanese short titles with no publications and with a translation")
        reports[321] = ("Russian short titles with no publications and with a translation")
        reports[322] = ("Spanish short titles with no publications and with a translation")
        reports[323] = ("Short titles with no publications and with a translation in other languages")
        reports[324] = ("Pubs without an ISBN and with an Audible ASIN which is an ISBN-10")
        reports[325] = ("Digital audio download pubs with a regular ASIN and no Audible ASIN")
        reports[326] = ("Pubs with an Audible ASIN and a non-Audible format")
        reports[327] = ("Authors with Images We Don't Have Permission to Link to")
        reports[328] = ("Variant Title with Synopsis Data")
        reports[329] = ("Translations with Tr template in Pub Notes and no Tr template in Title notes")
        reports[330] = ("Pre-1967 publications with an ISBN")
        reports[331] = ("Publications with PV# in notes")
        reports[332] = ("Pre-2020 publications with a 979 ISBN-13")
        reports[333] = ("Interior art titles with embedded [1] or (1)")
        reports[9999] = ("Suspected Duplicate Authors (monthly)")

        wiki_cleanup = (101, 102, 103, 104, 105, 106, 107, 108, 109,
                        110, 111, 112, 113, 114, 115, 116, 117, 118,
                        119, 120, 200, 201, 202, 203, 204, 205, 206,
                        207)
        containers = (29, 37, 54, 92, 240, 241)
        translations = (238, 239, 264, 265, 266, 267, 268, 269, 270,
                        271, 308, 309, 310, 311, 312, 313, 314, 315,
                        316, 317, 318, 319, 320, 321, 322, 323, 329)
        transliterations = (85, 97, 99, 121, 122, 123, 124, 125, 126,
                            127, 128, 129, 130, 131, 132, 133, 134, 135,
                            136, 137, 138, 139, 140, 141, 142, 143, 145,
                            146, 147, 148, 149, 150, 151, 152, 153, 154,
                            155, 156, 157, 158, 159, 160, 161, 162, 163,
                            164, 165, 166, 167, 169, 170, 171, 172, 173,
                            174, 175, 176, 177, 178, 179, 180, 181, 182,
                            257, 258, 259, 260, 261, 262, 263)

        sections = [('Authors', (6, 7, 8, 10, 53, 68, 78, 89, 94, 95, 198, 199, 302,
                                 327, 9999)), ]
        sections.append(('Magazines', (12, 13, 14, 15, 46)), )
        sections.append(('Containers (weekly)', containers), )
        sections.append(('Publications', (32, 33, 31, 34, 35, 36, 38, 39, 49, 50,
                                          51, 52, 56, 57, 70, 75, 79, 86, 88, 93,
                                          100, 193, 228, 231, 233, 235, 236, 243,
                                          244, 245, 246, 247, 248, 249, 250, 251,
                                          252, 272, 277, 278, 279, 280, 281,
                                          282, 283, 284, 285, 287, 288, 291, 292,
                                          294, 295, 299, 300, 306, 324, 325, 326,
                                          330, 331, 332)), )
        sections.append(('Series', (16, 17, 48, 64, 67, 76, 81, 90, 144)), )
        sections.append(('Titles', (19, 1, 3, 18, 47, 55, 62, 63, 69, 74, 80, 87,
                                    91, 96, 194, 195, 196, 197, 227, 275, 276, 290,
                                    293, 297, 303, 333)), )
        sections.append(('Variant Titles', (20, 21, 9, 2, 45, 286)), )
        sections.append(('Translations (weekly)', translations), )
        sections.append(('Chapbooks', (27, 28, 30, 242, 289)), )
        sections.append(('Serials', (22, 83, 84)), )
        sections.append(('Awards', (23, 24, 25, 26, 190, 232, 298, 307)), )
        sections.append(('Notes and Synopses', (5, 82, 191, 217, 208, 209, 216, 210, 211,
                                            212, 213, 214, 215, 218, 219, 220, 221, 222,
                                            223, 224, 225, 226, 229, 230, 234, 237, 253,
                                            254, 255, 256, 273, 274, 296, 304, 305, 328)), )
        sections.append(('Reviews', (40, 41, 42, 301)), )
        sections.append(('Publishers', (43, 44, 65, 73)), )
        sections.append(('Publication Series', (66, 77, 98, 189)), )
        sections.append(('Author Languages', (192, 11, 58, 59, 60, 61, 168, 183, 184, 185,
                                                186, 187, 188)), )
        sections.append(('Transliterations (weekly)', transliterations), )
        sections.append(('Wiki Cleanup (weekly)', wiki_cleanup), )
        sections.append(('Forthcoming Books', (71, 72)), )

        # A tuple of report IDs which non-moderators are allowed to view
        non_moderator = (1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16, 19,
                         20, 22, 29, 33, 34, 37, 38, 41, 45, 46, 48, 49, 54,
                         58, 59, 60, 61, 71, 72, 82, 83, 84, 85, 86, 87, 88,
                         91, 92, 93, 95, 97, 99,
                         100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                         110, 111, 112, 113, 114, 115, 116, 117, 118, 119,
                         120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
                         130, 131, 132, 133, 134, 135, 136, 137, 138, 139,
                         140, 141, 142, 143, 144, 145, 146, 147, 148, 149,
                         150, 151, 152, 153, 154, 155, 156, 157, 158, 159,
                         160, 161, 162, 163, 164, 165, 166, 167, 168, 169,
                         170, 171, 172, 173, 174, 175, 176, 177, 178, 179,
                         180, 181, 182, 183, 184, 185, 186, 187, 188, 189,
                         190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200,
                         201, 202, 203, 204, 205, 206, 207, 208, 209, 210,
                         211, 212, 213, 214, 215, 216, 217, 218, 219, 220,
                         221, 222, 223, 224, 225, 226, 227, 228, 229, 230,
                         232, 233, 234, 235, 236, 237, 238, 239, 240, 241,
                         242, 243, 244, 245, 246, 247, 248, 249, 250, 251,
                         252, 253, 254, 255, 256, 257, 264, 265, 266, 267,
                         268, 269, 270, 271, 272, 273, 274, 275, 276, 277,
                         278, 279, 280, 281, 282, 283, 284, 285, 286, 287,
                         288, 289, 291, 292, 293, 294, 295, 296, 297, 298,
                         299, 300, 301, 302, 303, 304, 305, 306, 307, 308,
                         309, 310, 311, 312, 313, 314, 315, 316, 317, 318,
                         319, 320, 321, 322, 323, 324, 325, 326, 327, 328,
                         329, 330, 331, 332, 333, 9999)

        transliterations = (85, 97, 99, 121, 122, 123, 124, 125, 126,
                            127, 128, 129, 130, 131, 132, 133, 134, 135,
                            136, 137, 138, 139, 140, 141, 142, 143, 145,
                            146, 147, 148, 149, 150, 151, 152, 153, 154,
                            155, 156, 157, 158, 159, 160, 161, 162, 163,
                            164, 165, 166, 167, 169, 170, 171, 172, 173,
                            174, 175, 176, 177, 178, 179, 180, 181, 182,
                            257, 258, 259, 260, 261, 262, 263)

        weeklies = [1, 3, 9, 13, 14, 15, 18, 20, 21, 23, 24, 27, 28, 32, 34, 35,
                    38, 40, 43, 46, 48, 52, 53, 58, 59, 60, 61, 62, 65, 66, 67, 68,
                    69, 70, 73, 74, 75, 76, 77, 78, 80, 84, 87, 88, 94, 95, 98,
                    144, 168, 183, 184, 185, 186, 187, 188, 189,
                    193, 218, 219, 220, 221, 222, 223, 224, 225,
                    226, 230, 233, 234, 237, 243, 251, 252, 253, 254, 255,
                    256, 277, 278, 279, 280, 281, 282, 283, 284, 285,
                    290, 291, 293, 294, 295, 296, 301, 304, 305, 306, 324,
                    331]
        weeklies.extend(wiki_cleanup)
        weeklies.extend(containers)
        weeklies.extend(translations)
        weeklies.extend(transliterations)

        monthlies = (9999, )

        return (reports, sections, non_moderator, tuple(weeklies), monthlies)
