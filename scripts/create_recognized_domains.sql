/* 
   create_recognized_domains.sql is a MySQL script intended to add
   table "recognized_domains" to the MySQL database.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 1 $
   Date:    $Date: 2023-07-03 16:32:38 -0400 (Mon, 7 Jul 2023) $

  (C) COPYRIGHT 2023   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS recognized_domains (
  domain_id int(11),
  domain_name text NOT NULL,
  site_name text NOT NULL,
  site_url mediumtext,
  linking_allowed tinyint(1),
  required_segment text,
  explicit_link_required tinyint(1),
  PRIMARY KEY (domain_id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
