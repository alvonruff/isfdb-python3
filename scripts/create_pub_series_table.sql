/* 
   create_pub_series_tables.sql is a MySQL script intended to add
   table "pub_series" to the MySQL database.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2010   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS pub_series (
  pub_series_id int(11) NOT NULL auto_increment,
  pub_series_name varchar(64),
  pub_series_wikipedia mediumtext,
  pub_series_note_id int(11),
  PRIMARY KEY  (pub_series_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

ALTER TABLE `webpages` ADD pub_series_id int(11);

ALTER TABLE `pubs` ADD pub_series_id int(11);
ALTER TABLE `pubs` ADD pub_series_num varchar(64);
