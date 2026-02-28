/* 
   add_NSK_Katalog_ID.sql is a MySQL script intended to add NSK Katalog (National
   and University Library in Zagreb) as an external idenifier type
	

   Version: $Revision: 418 $
   Date:    $Date: 2024-11-23 10:10:07 -0400 (Sat, 23 Nov 2024) $

  (C) COPYRIGHT 2025 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('NSK', 'National and University Library in Zagreb');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (36, 1, "https://katalog.nsk.hr/F/?func=direct&doc_number=%s");

