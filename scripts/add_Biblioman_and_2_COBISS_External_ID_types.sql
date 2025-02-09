/* 
   add_Biblioman_and_2_COBISS_ External_ID_types.sql is a MySQL script intended to add
   Biblioman, COBISS.BG and COBISS.SR as external identifier types


   Version: $Revision: 418 $
   Date:    $Date: 2021-09-13 10:10:07 -0400 (Mon, 13 Sep 2021) $

  (C) COPYRIGHT 2021 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Biblioman', '&#1041;&#1080;&#1073;&#1083;&#1080;&#1086;&#1084;&#1072;&#1085; (Biblioman)');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (32, 1, 'https://biblioman.chitanka.info/books/%s');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('COBISS.BG', 'Co-operative Online Bibliographic Systems and Services - Bulgaria');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (33, 1, 'https://plus.bg.cobiss.net/opac7/bib/%s#full');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('COBISS.SR', 'Co-operative Online Bibliographic Systems and Services - Serbia');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (34, 1, 'https://plus.sr.cobiss.net/opac7/bib/%s#full');
