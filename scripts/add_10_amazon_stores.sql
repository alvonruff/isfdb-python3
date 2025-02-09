/* 
   add_10_amazon_stores.sql is a MySQL script intended to add 
   10 Amazon stores as "Amazon Links" option and change the spelling
   of 4 other Amazon store names.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url) VALUES (33, 'Amazon Australia','https://www.amazon.com.au/dp/%s');
INSERT INTO websites (site_id, site_name, site_url) VALUES (34, 'Amazon Brazil','https://www.amazon.com.br/dp/%s');
INSERT INTO websites (site_id, site_name, site_url) VALUES (35, 'Amazon China','https://www.amazon.cn/dp/%s');
INSERT INTO websites (site_id, site_name, site_url) VALUES (36, 'Amazon India','https://www.amazon.in/dp/%s');
INSERT INTO websites (site_id, site_name, site_url) VALUES (37, 'Amazon Italy','https://www.amazon.it/dp/%s');
INSERT INTO websites (site_id, site_name, site_url) VALUES (38, 'Amazon Mexico','https://www.amazon.com.mx/dp/%s');
INSERT INTO websites (site_id, site_name, site_url) VALUES (39, 'Amazon Netherlands','https://www.amazon.nl/dp/%s');
INSERT INTO websites (site_id, site_name, site_url) VALUES (40, 'Amazon Spain','https://www.amazon.es/dp/%s');
INSERT INTO websites (site_id, site_name, site_url) VALUES (41, 'Amazon Turkey','https://www.amazon.com.tr/dp/%s');
INSERT INTO websites (site_id, site_name, site_url) VALUES (42, 'Amazon UAE','https://www.amazon.ae/dp/%s');
UPDATE websites SET site_name = 'Amazon Canada' WHERE site_name = 'Amazon CA';
UPDATE websites SET site_name = 'Amazon Germany' WHERE site_name = 'Amazon DE';
UPDATE websites SET site_name = 'Amazon France' WHERE site_name = 'Amazon FR';
UPDATE websites SET site_name = 'Amazon Japan' WHERE site_name = 'Amazon JP';
