/* 
   add_2_more_amazon_identifier_sites.sql is a MySQL script intended to
   add ASIN links to the Amazon web sites in Turkey and UAE
	

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.com.tr/dp/%s', 'TR');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.ae/dp/%s', 'UAE');


