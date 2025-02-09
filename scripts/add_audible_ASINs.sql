/* 
   add_audible_ASINs.sql is a MySQL script intended to
   add Audible ASIN as a new external idenifier type
	

   Version: $Revision: 15 $
   Date:    $Date: 2018-05-18 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Audible-ASIN', 'Audible ASIN');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (17, 1, 'https://www.audible.com/pd/%s');

