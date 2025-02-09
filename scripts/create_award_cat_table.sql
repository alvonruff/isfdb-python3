/* 
   create_award_cats_table.sql is a MySQL script intended to add
   table "award_cats" to the MySQL database.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS award_cats (
  award_cat_id int(11) NOT NULL auto_increment,
  award_cat_name mediumtext,
  award_cat_type_id int(11),
  PRIMARY KEY  (award_cat_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

ALTER TABLE awards ADD COLUMN award_cat_id INT(11);

