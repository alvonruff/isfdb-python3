/* 
   create_front_page_pubs.sql is a MySQL script intended to add
   table "front_page_pubs" to the MySQL database.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2022   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS front_page_pubs (
  pub_id int(11) NOT NULL,
  PRIMARY KEY  (pub_id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
