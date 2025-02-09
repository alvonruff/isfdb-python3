/* 
   create_webpage_tables.sql is a MySQL script intended to add
   table "websites" to the MySQL database.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2009   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS languages (
  lang_id int(11) NOT NULL auto_increment,
  lang_name varchar(64),
  lang_code varchar(10),
  PRIMARY KEY  (lang_id),
  KEY lang_name (lang_name),
  KEY lang_code (lang_code)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
