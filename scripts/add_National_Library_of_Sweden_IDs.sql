/* 
   add_National_Library_of_Sweden_IDs.sql is a MySQL script intended to add
   National Library of Sweden IDs (Libris and Libris XL) as external identifier types


   Version: $Revision: 418 $
   Date:    $Date: 2021-09-13 10:10:07 -0400 (Mon, 13 Sep 2021) $

  (C) COPYRIGHT 2021 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Libris', 'Libris - National Library of Sweden');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (30, 1, 'https://libris.kb.se/bib/%s', 'Web view');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (30, 2, 'https://libris.kb.se/resource/bib/%s', 'Other formats');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Libris XL', 'Libris XL - National Library of Sweden (new interface)');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (31, 1, 'https://libris.kb.se/katalogisering/%s', 'Web view');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (31, 2, 'https://libris.kb.se/%s', 'Other formats');
