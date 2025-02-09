/* 
   add_amazon_identifier_sites.sql is a MySQL script intended to
   add links to Amazon web sites in a number of countries:
	

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update identifier_sites set site_position=1 where site_url like '%amazon%';

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.com.au/dp/%s', 'AU');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.com.br/dp/%s', 'BR');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.cn/dp/%s', 'CN');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.es/dp/%s', 'ES');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.in/dp/%s', 'IN');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.it/dp/%s', 'IT');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.com.mx/dp/%s', 'MX');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.nl/dp/%s', 'NL');
