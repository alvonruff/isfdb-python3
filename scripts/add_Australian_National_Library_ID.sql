/* 
   add_Australian_National_Library_ID is a MySQL script intended to
   add Australian National Library as an external idenifier
	

   Version: $Revision: 418 $
   Date:    $Date: 2019-12-02 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('ANL', 'Australian National Library ID');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (28, 1, 'https://nla.gov.au/nla.cat-vn%s');

